import copy
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import activity_data as data
import compare_activity as compare
import pace_chart as pace


def messages():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return {
        "session_mesgs": [{
            "start_time": start, "total_distance": 4000,
            "total_elapsed_time": 4000, "total_timer_time": 3900,
            "total_ascent": 44, "total_descent": 24,
        }],
        "record_mesgs": [
            {"timestamp": start + timedelta(seconds=i * 1000),
             "position_lat": round(30 * 2**31 / 180),
             "position_long": round((110 + i * .01) * 2**31 / 180),
             "distance": i * 1000}
            for i in range(5)
        ],
        "lap_mesgs": [
            {"start_time": start + timedelta(seconds=i * 2000),
             "total_distance": 2000, "total_ascent": 20 + i * 4,
             "total_descent": 10 + i * 4}
            for i in range(2)
        ],
    }


def route_file(folder, kml=False):
    path = Path(folder) / ("race.kml" if kml else "race.gpx")
    coords = [(30, 110 + i * .01, 100 + i * 20) for i in range(5)]
    if kml:
        path.write_text('<kml><Document><Placemark><LineString><altitudeMode>absolute'
                        '</altitudeMode><coordinates>' +
                        " ".join(f"{lon},{lat},{z}" for lat, lon, z in coords) +
                        '</coordinates></LineString></Placemark></Document></kml>')
    else:
        path.write_text('<gpx><wpt lat="30" lon="110.02"><name>CP1</name></wpt>'
                        '<trk><trkseg>' + "".join(
                            f'<trkpt lat="{lat}" lon="{lon}"><ele>{z}</ele></trkpt>'
                            for lat, lon, z in coords) + '</trkseg></trk></gpx>')
    return path


class ActivityDataTests(unittest.TestCase):
    def test_fit_totals_without_platform(self):
        activity = data.activity_from_messages(messages())
        self.assertEqual(activity["totals"]["ascent_m"], 44)
        self.assertEqual(activity["totals_source"], "FIT session")
        self.assertEqual(activity["records"][-1]["elapsed_seconds"], 4000)
        self.assertEqual(data.lap_value(activity["laps"], 1500, "ascent_m"), 15)

    def test_platform_finish_is_not_rescaled(self):
        activity = data.activity_from_messages(messages(), {
            "activityId": 123, "activityName": "Example",
            "summaryDTO": {"distance": 4001, "elapsedDuration": 4001.25,
                           "elevationGain": 45, "elevationLoss": 23},
        })
        self.assertEqual(activity["totals"]["ascent_m"], 45)
        self.assertEqual(data.lap_value(activity["laps"], 2000, "ascent_m"), 20)
        self.assertTrue(activity["warnings"])

    def test_missing_lap_metrics_propagate_unknown(self):
        raw = messages()
        del raw["lap_mesgs"][0]["total_ascent"]
        activity = data.activity_from_messages(raw)
        self.assertIsNone(data.lap_value(activity["laps"], 500, "ascent_m"))
        self.assertIsNone(data.lap_value(activity["laps"], 3000, "ascent_m"))
        self.assertEqual(data.lap_value(activity["laps"], 3000, "descent_m"), 17)

    def test_no_laps_is_valid_but_unknown_between_checkpoints(self):
        raw = messages()
        raw["lap_mesgs"] = []
        activity = data.activity_from_messages(raw)
        self.assertIsNone(data.lap_value(activity["laps"], 2000, "ascent_m"))

    def test_bad_sessions_and_record_order_are_rejected(self):
        for field, value in [
            ("session_mesgs", []),
            ("session_mesgs", messages()["session_mesgs"] * 2),
            ("record_mesgs", list(reversed(messages()["record_mesgs"]))),
        ]:
            raw = messages()
            raw[field] = value
            with self.subTest(field=field), self.assertRaises(pace.InputError):
                data.activity_from_messages(raw)

    def test_missing_records_are_reported_and_invalid_values_rejected(self):
        raw = messages()
        raw["record_mesgs"].insert(1, {"timestamp": raw["session_mesgs"][0]["start_time"]})
        self.assertEqual(data.activity_from_messages(raw)["skipped_records"], 1)
        raw["record_mesgs"][2]["distance"] = float("nan")
        with self.assertRaises(pace.InputError):
            data.activity_from_messages(raw)

    def test_invalid_laps_disable_estimation_instead_of_shifting_boundaries(self):
        raw = messages()
        del raw["lap_mesgs"][0]["total_distance"]
        activity = data.activity_from_messages(raw)
        self.assertEqual(activity["laps"], [])
        self.assertTrue(activity["warnings"])

    def test_direct_and_zipped_fit_and_decoder_failures(self):
        with tempfile.TemporaryDirectory() as folder:
            direct = Path(folder) / "activity.fit"
            direct.write_bytes(b"synthetic FIT")
            zipped = Path(folder) / "activity.zip"
            with ZipFile(zipped, "w") as archive:
                archive.writestr("nested/activity.fit", direct.read_bytes())
            with patch.object(data, "decode_fit", return_value=messages()) as decoder:
                self.assertEqual(data.read_activity(direct)["totals"]["distance_m"], 4000)
                self.assertEqual(data.read_activity(zipped)["totals"]["distance_m"], 4000)
                self.assertEqual(decoder.call_count, 2)
            with ZipFile(zipped, "a") as archive:
                archive.writestr("other.fit", b"other")
            with self.assertRaisesRegex(pace.InputError, "one FIT"):
                data.read_activity(zipped)
            zipped.write_bytes(b"broken zip")
            with self.assertRaises(pace.InputError):
                data.read_activity(zipped)
            with patch.object(data, "decode_fit", side_effect=pace.InputError("Damaged FIT")):
                with self.assertRaisesRegex(pace.InputError, "Damaged"):
                    data.read_activity(direct)


class FitRouteTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "activity.fit"
        self.path.write_bytes(b"synthetic FIT")
        self.raw = messages()
        for i, record in enumerate(self.raw["record_mesgs"]):
            record["enhanced_altitude"] = 100 + i * 20

    def load(self, **kwargs):
        with patch.object(data, "decode_fit", return_value=self.raw):
            return pace.load_route(self.path, **kwargs)

    def config(self):
        return {"targets": ["15:00", "16:00", "17:00"], "checkpoints": [
            {"name": "CP1", "distance_km": 2},
            {"name": "Finish", "distance_km": 4},
        ]}

    def test_route_preserves_recorded_distance_and_source_elevation(self):
        route = self.load()
        self.assertEqual([s.distance_m for s in route.samples], [0, 1000, 2000, 3000, 4000])
        self.assertEqual([s.elevation_m for s in route.samples], [100, 120, 140, 160, 180])
        self.assertNotAlmostEqual(sum(pace.haversine(a, b)
                                     for a, b in zip(route.points, route.points[1:])), route.total_m)
        self.assertEqual(route.diagnostics["distance_source"], "fit_recorded")
        self.assertEqual(route.candidates, [])

    def test_enhanced_altitude_precedes_altitude_with_fallback_and_negative_heights(self):
        for record in self.raw["record_mesgs"]:
            record["altitude"] = 900
        self.raw["record_mesgs"][0]["enhanced_altitude"] = None
        self.raw["record_mesgs"][1].pop("enhanced_altitude")
        self.raw["record_mesgs"][2]["enhanced_altitude"] = -10
        route = self.load()
        self.assertEqual([s.elevation_m for s in route.samples], [900, 900, -10, 160, 180])

    def test_repeated_distances_keep_last_record_before_terrain_processing(self):
        duplicate = {**self.raw["record_mesgs"][1],
                     "timestamp": self.raw["record_mesgs"][1]["timestamp"] - timedelta(seconds=1),
                     "enhanced_altitude": 999}
        self.raw["record_mesgs"].insert(1, duplicate)
        route = self.load()
        self.assertEqual(len(route.samples), 5)
        self.assertEqual(route.samples[1].elevation_m, 120)
        self.assertEqual(route.diagnostics["fit_duplicate_distance_records"], 1)
        self.assertTrue(any("duplicate" in warning for warning in route.warnings))
        processed = pace.prepare_route(route)
        self.assertEqual(processed.total_m, 4000)

    def test_fit_zip_is_a_route_input(self):
        self.path = Path(self.folder.name) / "activity.zip"
        with ZipFile(self.path, "w") as archive:
            archive.writestr("nested/activity.fit", b"synthetic FIT")
        self.assertEqual(self.load().total_m, 4000)

    def test_missing_and_nonfinite_elevations_fail_without_filling_zero(self):
        for value in (None, float("nan"), float("inf"), True, "100"):
            self.raw["record_mesgs"][2]["enhanced_altitude"] = value
            with self.subTest(value=value), self.assertRaisesRegex(pace.InputError, "elevation"):
                self.load()

    def test_incomplete_start_nonmonotonic_and_degenerate_distance_fail(self):
        for distances in ([5, 1000, 2000, 3000, 4000], [0, 1000, 999, 3000, 4000],
                          [0, 0, 0, 0, 0]):
            for record, distance in zip(self.raw["record_mesgs"], distances):
                record["distance"] = distance
            with self.subTest(distances=distances), self.assertRaises(pace.InputError):
                self.load()

    def test_incomplete_records_are_reported_and_session_totals_do_not_scale_route(self):
        self.raw["record_mesgs"].insert(1, {"timestamp": self.raw["session_mesgs"][0]["start_time"]})
        self.raw["session_mesgs"][0]["total_distance"] = 5000
        route = self.load()
        self.assertEqual(route.total_m, 4000)
        self.assertEqual(route.diagnostics["fit_skipped_records"], 1)
        self.assertTrue(any("distance" in warning for warning in route.warnings))

    def test_geometry_simplification_cannot_replace_fit_distance(self):
        route = self.load()
        with self.assertRaisesRegex(pace.InputError, "FIT.*distance_tolerance_m"):
            pace.prepare_route(route, distance_tolerance_m=2)

    def test_fit_rejects_irrelevant_track_or_kml_selection(self):
        for options in ({"track_index": 2}, {"track_index": True}, {"track_index": 1.0},
                        {"use_kml_altitudes": True}):
            with self.subTest(options=options), self.assertRaises(pace.InputError):
                self.load(**options)
        self.assertEqual(self.load(track_index=1).total_m, 4000)

    def test_fit_plan_and_comparison_share_checkpoint_distance_and_locked_passages(self):
        with patch.object(data, "decode_fit", return_value=self.raw):
            plan, route = compare.load_plan(self.path, self.config())
            activity = data.read_activity(self.path)
        result = compare.build_comparison(plan, route, activity, {"manual:1": 2000.25})
        self.assertEqual(plan["route"]["distance_m"], 4000)
        self.assertEqual(plan["route"]["ascent_m"], 80)
        self.assertNotEqual(plan["route"]["ascent_m"], activity["totals"]["ascent_m"])
        self.assertEqual(plan["targets_seconds"], [54000, 57600, 61200])
        self.assertEqual(result["checkpoints"][1]["elapsed_seconds"], 2000.25)
        for i, target in enumerate(plan["targets_seconds"]):
            self.assertAlmostEqual(sum(s["plans"][i]["seconds"] for s in result["segments"]), target)
        self.assertAlmostEqual(sum(t["planned_ascent_m"] for t in result["terrain"]), 80)
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        root = ET.fromstring(render_svg(result))
        metadata = json.loads(root.find("{*}metadata").text)
        self.assertEqual(metadata["route_diagnostics"]["distance_source"], "fit_recorded")
        self.assertEqual(metadata["route_diagnostics"]["fit_duplicate_distance_records"], 0)
        self.assertTrue(any("FIT" in note and "海拔" in note for note in metadata["data_notes"]))

    def test_standalone_fit_cli_reports_optional_dependency_as_json(self):
        script = Path(pace.__file__)
        result = subprocess.run([sys.executable, "-S", str(script), "inspect", str(self.path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("garmin-fit-sdk", json.loads(result.stderr)["error"])

    def test_fit_checkpoint_distances_are_recorded_not_official_in_pace_exports(self):
        with patch.object(data, "decode_fit", return_value=self.raw):
            plan = pace.build_plan(self.path, self.config())
        self.assertTrue(all(cp["official_distance_km"] is None for cp in plan["checkpoints"]))
        self.assertIn("基于实际 FIT 路线", pace.table_metadata(plan))
        for rendered in (pace.render_svg(plan), pace.render_html(plan)):
            self.assertIn("基于实际 FIT 路线", rendered)

    def test_fit_inspect_generate_and_comparison_are_offline(self):
        config = Path(self.folder.name) / "config.json"
        config.write_text(json.dumps(self.config()))
        output = Path(self.folder.name) / "out"
        with patch.object(data, "decode_fit", return_value=self.raw):
            with patch("activity_data.urlopen", side_effect=AssertionError("Must be offline")):
                with patch("sys.stdout", new_callable=io.StringIO) as stdout:
                    self.assertEqual(pace.main(["inspect", str(self.path)]), 0)
                self.assertEqual(json.loads(stdout.getvalue())["distance_m"], 4000)
                with patch("sys.stdout", new_callable=io.StringIO):
                    self.assertEqual(pace.main(["generate", str(self.path), "--config", str(config),
                                                "--output-dir", str(output)]), 0)
                    self.assertEqual(compare.main(["generate", str(self.path), "--config", str(config),
                                                   "--fit", str(self.path), "--output-dir", str(output)]), 0)
        self.assertEqual({p.name for p in output.iterdir()}, {"pace-chart.svg", "garmin-comparison.svg"})


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = route_file(self.folder.name)
        self.config = {"targets": ["01:00", "02:00"]}
        self.plan, self.route = compare.load_plan(self.path, self.config)
        self.activity = data.activity_from_messages(messages())

    def build(self, **kwargs):
        return compare.build_comparison(self.plan, self.route, self.activity, **kwargs)

    def test_segment_sums_and_signs(self):
        result = self.build()
        segments = result["segments"]
        self.assertEqual(len(segments), 2)
        self.assertAlmostEqual(sum(s["actual_seconds"] for s in segments), 4000)
        for j, target in enumerate((3600, 7200)):
            self.assertAlmostEqual(sum(s["plans"][j]["seconds"] for s in segments), target)
            for s in segments:
                self.assertAlmostEqual(s["plans"][j]["delta_seconds"],
                                       s["plans"][j]["seconds"] - s["actual_seconds"])
        self.assertAlmostEqual(result["checkpoints"][1]["ascent_m"], 20, places=3)
        self.assertAlmostEqual(result["terrain"][1]["actual_ascent_m"], 24, places=3)

    def test_rest_is_in_following_leg(self):
        self.config["checkpoint_overrides"] = {"wpt:1": {"rest_minutes": 5}}
        plan, route = compare.load_plan(self.path, self.config)
        result = compare.build_comparison(plan, route, self.activity)
        timing = plan["schedules"][0]["checkpoints"]
        self.assertAlmostEqual(result["segments"][1]["plans"][0]["seconds"],
                               timing[2]["moving_seconds"] + 300)

    def test_targets_override_without_mutating_config(self):
        original = copy.deepcopy(self.config)
        plan, _ = compare.load_plan(self.path, self.config, ["26:00"])
        self.assertEqual(plan["targets_seconds"], [93600])
        self.assertEqual(self.config, original)
        self.assertEqual(compare.clock(93600.5), "26:00:01")
        self.assertEqual(compare.time_delta(-.5), "-00:00:01")
        self.assertEqual(compare.time_delta(.1), "00:00:00")

    def test_manual_kml_positions_and_exact_target_list(self):
        path = route_file(self.folder.name, kml=True)
        total = pace.load_route(path).total_m
        plan, route = compare.load_plan(path, {
            "targets": ["01:00"], "checkpoints": [
                {"name": "Aid", "distance_km": total / 2000},
                {"name": "Finish", "distance_km": total / 1000},
            ],
        })
        result = compare.build_comparison(plan, route, self.activity)
        self.assertEqual(result["checkpoints"][1]["id"], "manual:1")
        self.assertAlmostEqual(result["checkpoints"][1]["elapsed_seconds"], 2000, places=2)

    def test_off_route_and_time_override(self):
        self.route.candidates[0]["lat"] += .01
        with self.assertRaisesRegex(pace.InputError, "100 m"):
            self.build()
        result = self.build(overrides={"wpt:1": "00:30"})
        self.assertEqual(result["checkpoints"][1]["elapsed_seconds"], 1800)
        self.assertEqual(result["checkpoints"][1]["match_method"], "elapsed override")
        self.assertTrue(result["warnings"])
        with self.assertRaisesRegex(pace.InputError, "Unknown"):
            self.build(overrides={"typo": "00:30"})
        with self.assertRaises(pace.InputError):
            self.build(overrides={"wpt:1": "02:00"})

    def test_repeated_route_occurrences_require_confirmation(self):
        activity = copy.deepcopy(self.activity)
        records = activity["records"]
        activity["records"] = records + [
            {**r, "elapsed_seconds": r["elapsed_seconds"] + 5000,
             "distance_m": r["distance_m"] + 5000} for r in records
        ]
        activity["totals"]["elapsed_seconds"] = 9000
        activity["totals"]["distance_m"] = 9000
        with self.assertRaisesRegex(pace.InputError, "ambiguous"):
            compare.build_comparison(self.plan, self.route, activity)
        result = compare.build_comparison(self.plan, self.route, activity,
                                          {"wpt:1": "00:33:20"})
        self.assertEqual(result["checkpoints"][1]["elapsed_seconds"], 2000)

    def test_stationary_passage_and_precise_numeric_override(self):
        activity = copy.deepcopy(self.activity)
        stationary = activity["records"][2]
        activity["records"].insert(3, {**stationary, "elapsed_seconds": 2200})
        with self.assertRaisesRegex(pace.InputError, "stationary"):
            compare.build_comparison(self.plan, self.route, activity)
        result = compare.build_comparison(self.plan, self.route, activity, {"wpt:1": 2000.25})
        self.assertEqual(result["checkpoints"][1]["elapsed_seconds"], 2000.25)
        self.assertEqual(result["passage_overrides"], {"wpt:1": 2000.25})
        for invalid in ([], {"wpt:1": True}, {"wpt:1": float("nan")}):
            with self.subTest(invalid=invalid), self.assertRaises(pace.InputError):
                compare.build_comparison(self.plan, self.route, activity, invalid)

    def test_processed_distance_override_is_authoritative(self):
        self.config["checkpoint_overrides"] = {"wpt:1": {"distance_km": self.route.total_m / 4000}}
        plan, route = compare.load_plan(self.path, self.config)
        result = compare.build_comparison(plan, route, self.activity)
        self.assertAlmostEqual(result["checkpoints"][1]["elapsed_seconds"], 1000, places=2)

    def test_reversed_station_order_rejected(self):
        plan = copy.deepcopy(self.plan)
        plan["checkpoints"].insert(2, {**plan["checkpoints"][1], "id": "extra", "distance_m": 100})
        with self.assertRaises(pace.InputError):
            compare.build_comparison(plan, self.route, self.activity)

    def test_missing_terrain_stays_unknown(self):
        self.activity["laps"] = []
        result = self.build()
        self.assertIsNone(result["terrain"][0]["actual_ascent_m"])
        self.assertIsNone(result["terrain"][1]["actual_ascent_m"])

    def test_time_charts_pair_cumulative_curves_and_segment_bars(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg, time_status
        result = self.build()
        root = ET.fromstring(render_svg(result))
        panels = root.findall(".//{*}g[@class='target-panel']")
        self.assertEqual(len(panels), len(self.plan["schedules"]))
        scales = {"cumulative": set(), "segment": set()}
        for panel, schedule in zip(panels, self.plan["schedules"]):
            cumulative = panel.find("{*}g[@data-kind='cumulative']")
            segment_plot = panel.find("{*}g[@data-kind='segment']")
            self.assertGreater(float(segment_plot.get("data-y-top")), float(cumulative.get("data-y-bottom")))
            self.assertEqual(segment_plot.get("data-x-min"), cumulative.get("data-x-min"))
            self.assertEqual(segment_plot.get("data-x-max"), cumulative.get("data-x-max"))
            for kind, plot in (("cumulative", cumulative), ("segment", segment_plot)):
                scales[kind].add(plot.get("data-limit-seconds"))
                self.assertIsNotNone(plot.find("{*}path[@data-role='zero-line']"))
            points = cumulative.findall(".//{*}circle[@data-delta-seconds]")
            self.assertEqual(len(points), len(result["checkpoints"]))
            zero = float(cumulative.get("data-zero-y"))
            scale = float(cumulative.get("data-pixels-per-second"))
            x0, x1 = float(cumulative.get("data-x-min")), float(cumulative.get("data-x-max"))
            for cp, actual, predicted, point in zip(self.plan["checkpoints"], result["checkpoints"], schedule["checkpoints"], points):
                delta = predicted["arrival_seconds"] - actual["elapsed_seconds"]
                self.assertAlmostEqual(float(point.get("data-delta-seconds")), delta)
                self.assertAlmostEqual(float(point.get("cx")), x0 + cp["distance_m"] /
                                       self.plan["route"]["distance_m"] * (x1 - x0), places=2)
                self.assertAlmostEqual(float(point.get("cy")), zero - delta * scale, places=2)
                self.assertIn(compare.clock(actual["elapsed_seconds"]), point.find("{*}title").text)
                self.assertIn(compare.clock(predicted["arrival_seconds"]), point.find("{*}title").text)
            bars = segment_plot.findall(".//{*}rect[@data-delta-seconds]")
            self.assertEqual(len(bars), len(result["segments"]))
            zero = float(segment_plot.get("data-zero-y"))
            scale = float(segment_plot.get("data-pixels-per-second"))
            target = schedule["target_seconds"]
            for segment, bar in zip(result["segments"], bars):
                predicted = next(p for p in segment["plans"] if p["target_seconds"] == target)
                delta = predicted["delta_seconds"]
                self.assertAlmostEqual(float(bar.get("data-delta-seconds")), delta)
                self.assertAlmostEqual(float(bar.get("height")), abs(delta) * scale, places=2)
                self.assertAlmostEqual(float(bar.get("y")), zero - max(0, delta) * scale, places=2)
                self.assertEqual(bar.get("fill"), time_status(delta)[1])
                self.assertIn(compare.clock(segment["actual_seconds"]), bar.find("{*}title").text)
                self.assertIn(compare.clock(predicted["seconds"]), bar.find("{*}title").text)
        self.assertTrue(all(len(values) == 1 for values in scales.values()))

    def test_time_readout_shows_segment_times_and_actual_minus_plan_differences(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        self.config["targets"] = ["15:00", "26:00"]
        self.config["checkpoint_overrides"] = {"wpt:1": {"rest_minutes": 5}}
        self.plan, self.route = compare.load_plan(self.path, self.config)
        result = self.build()
        root = ET.fromstring(render_svg(result))
        readout = root.find(".//{*}g[@id='checkpoint-times']")
        self.assertIsNotNone(readout)
        headers = readout.findall(".//{*}g[@class='checkpoint-header inspectable']")
        self.assertEqual(len(headers), len(result["segments"]))
        for header, cp, terrain in zip(headers, self.plan["checkpoints"][1:], result["terrain"]):
            self.assertEqual(header.get("data-cp-id"), cp["id"])
            self.assertAlmostEqual(float(header.get("data-distance-m")), cp["distance_m"])
            station = "".join(t.text or "" for t in header.findall("{*}text"))
            self.assertEqual(station, f'{cp["name"]} · {cp["distance_m"] / 1000:.1f} km')
            self.assertIn(f'{terrain["actual_distance_m"] / 1000:.3f}', header.find("{*}title").text)
        rows = readout.findall(".//{*}g[@class='time-row']")
        self.assertEqual([row.get("data-cp-id") for row in rows], [cp["id"] for cp in result["checkpoints"][1:]])
        self.assertIn("实际 − 预计", "".join(readout.itertext()))
        for i, row in enumerate(rows, 1):
            cells = row.findall("{*}g[@class='time-cell inspectable']")
            self.assertEqual([cell.get("data-series") for cell in cells], ["actual", "planned", "planned"])
            for j, cell in enumerate(cells):
                if j:
                    self.assertEqual(float(cell.get("data-target-seconds")), self.plan["targets_seconds"][j - 1])
                if j == 0:
                    elapsed = result["checkpoints"][i]["elapsed_seconds"]
                    segment = result["segments"][i - 1]["actual_seconds"]
                else:
                    elapsed = self.plan["schedules"][j - 1]["checkpoints"][i]["arrival_seconds"]
                    segment = result["segments"][i - 1]["plans"][j - 1]["seconds"]
                self.assertEqual(cell.get("data-cp-id"), result["checkpoints"][i]["id"])
                self.assertAlmostEqual(float(cell.get("data-elapsed-seconds")), elapsed)
                self.assertAlmostEqual(float(cell.get("data-segment-seconds")), segment)
                value = cell.find("{*}text[@data-role='time-values']")
                expected = compare.clock(segment)
                if j:
                    delta = result["segments"][i - 1]["actual_seconds"] - segment
                    expected += f"（{compare.time_delta(delta)}）"
                    self.assertAlmostEqual(float(cell.get("data-actual-minus-plan-seconds")), delta)
                self.assertEqual("".join(value.itertext()), expected)
                self.assertGreaterEqual(int(value.get("font-weight")), 650)
                self.assertEqual(cell.get("tabindex"), "0")
                self.assertIn(result["segments"][i - 1]["from_name"], cell.find("{*}title").text)
                self.assertIn(compare.clock(elapsed), cell.find("{*}title").text)

    def test_many_checkpoints_extend_readout_vertically_with_aligned_source_columns(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        total_km = self.route.total_m / 1000
        self.config["checkpoints"] = [
            {"name": f"Station {i}", "distance_km": total_km * i / 18}
            for i in range(1, 19)
        ]
        self.plan, self.route = compare.load_plan(self.path, self.config)
        result = self.build()
        root = ET.fromstring(render_svg(result))
        rows = root.findall(".//{*}g[@class='time-row']")
        self.assertEqual([row.get("data-cp-id") for row in rows], [cp["id"] for cp in result["checkpoints"][1:]])
        previous_y = -1
        columns = None
        for row in rows:
            cells = row.findall("{*}g[@class='time-cell inspectable']")
            self.assertEqual(len(cells), len(self.plan["schedules"]) + 1)
            values = [cell.find("{*}text[@data-role='time-values']") for cell in cells]
            current_columns = [value.get("x") for value in values]
            if columns is not None:
                self.assertEqual(current_columns, columns)
            columns = current_columns
            self.assertGreater(float(values[0].get("y")), previous_y)
            previous_y = float(values[0].get("y"))

    def test_segment_readout_and_delta_share_colors_using_unrounded_actual_minus_plan(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg, time_status
        self.config["targets"] = ["01:00", "01:30", "02:00"]
        self.plan, self.route = compare.load_plan(self.path, self.config)
        result = self.build()
        offsets = iter((-120, 120, 0, -.1, .1, 60))
        for segment in result["segments"]:
            for predicted in segment["plans"]:
                predicted["seconds"] = segment["actual_seconds"] + next(offsets)
        root = ET.fromstring(render_svg(result))
        rows = root.findall(".//{*}g[@class='time-row']")
        for row, segment in zip(rows, result["segments"]):
            cells = row.findall("{*}g[@class='time-cell inspectable']")
            actual_segment = cells[0].find(".//{*}tspan[@data-role='segment-time']")
            self.assertEqual(actual_segment.get("fill"), "#202A35")
            for cell, predicted in zip(cells[1:], segment["plans"]):
                value = cell.find("{*}text[@data-role='time-values']")
                leg = value.find("{*}tspan[@data-role='segment-time']")
                difference = value.find("{*}tspan[@data-role='segment-difference']")
                self.assertEqual(leg.text, compare.clock(predicted["seconds"]))
                slower = segment["actual_seconds"] > predicted["seconds"]
                self.assertEqual(leg.get("fill"), time_status(-1 if slower else 1)[1])
                self.assertEqual(difference.get("fill"), leg.get("fill"))
                delta = segment["actual_seconds"] - predicted["seconds"]
                self.assertEqual(difference.text, f"（{compare.time_delta(delta)}）")
                self.assertIn("实际 − 预计", cell.find("{*}title").text)

    def test_long_station_labels_fit_merged_column_and_keep_full_name_and_distance(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        result = self.build()
        result["checkpoints"][1]["name"] = "CP1–这是一个需要换行展示的很长的站点名字 <A> & B"
        root = ET.fromstring(render_svg(result))
        headers = root.findall(".//{*}g[@class='checkpoint-header inspectable']")
        texts = headers[0].findall("{*}text")
        expected = result["checkpoints"][1]["name"] + f' · {result["terrain"][0]["planned_distance_m"] / 1000:.1f} km'
        self.assertEqual("".join(t.text or "" for t in texts), expected)
        self.assertGreater(len(texts), 1)
        rows = root.findall(".//{*}g[@class='time-row']")
        background = rows[0].find("{*}rect")
        for text in texts:
            self.assertGreater(float(text.get("y")), float(background.get("y")))
            self.assertLess(float(text.get("y")), float(background.get("y")) + float(background.get("height")))

    def test_terrain_summary_and_grouped_elevation_charts_preserve_values(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        result = self.build()
        root = ET.fromstring(render_svg(result))
        summary = root.find(".//{*}g[@id='terrain-summary']")
        self.assertIsNotNone(summary)
        self.assertIn(f'{result["activity"]["totals"]["distance_m"] / 1000:.2f} / '
                      f'{self.plan["route"]["distance_m"] / 1000:.2f} km', "".join(summary.itertext()))
        scales = set()
        for key in ("ascent_m", "descent_m"):
            plot = root.find(f".//{{*}}g[@data-kind='{key}']")
            zero = float(plot.get("data-zero-y"))
            scale = float(plot.get("data-pixels-per-meter"))
            scales.add(scale)
            for source in ("actual", "planned"):
                bars = plot.findall(f".//{{*}}rect[@data-series='{source}']")
                self.assertEqual(len(bars), len(result["terrain"]))
                for metrics, bar in zip(result["terrain"], bars):
                    value = metrics[source + "_" + key]
                    self.assertAlmostEqual(float(bar.get("data-value-m")), value)
                    self.assertAlmostEqual(float(bar.get("height")), value * scale, places=2)
                    self.assertAlmostEqual(float(bar.get("y")), zero - value * scale, places=2)
        self.assertEqual(len(scales), 1)

    def test_close_elevation_labels_are_staggered_above_their_bars(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        result = self.build()
        for row in result["terrain"]:
            for key in ("ascent_m", "descent_m"):
                row["actual_" + key] = 500.0
                row["planned_" + key] = 501.0
        root = ET.fromstring(render_svg(result))
        for key in ("ascent_m", "descent_m"):
            plot = root.find(f".//{{*}}g[@data-kind='{key}']")
            for group in plot.findall("{*}g[@data-actual-available]"):
                actual, planned = group.findall("{*}text")[:2]
                self.assertGreaterEqual(abs(float(actual.get("y")) - float(planned.get("y"))), 26)
                for label, bar in zip((actual, planned), group.findall("{*}rect[@data-series]")):
                    self.assertEqual(label.get("text-anchor"), "middle")
                    self.assertLess(float(label.get("y")), float(bar.get("y")))

    def test_missing_terrain_shows_unknown_and_keeps_available_plan_values(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        result = self.build()
        for key in ("distance_m", "ascent_m", "descent_m"):
            result["terrain"][0]["actual_" + key] = None
            result["terrain"][1]["actual_" + key] = result["terrain"][1]["planned_" + key]
        root = ET.fromstring(render_svg(result))
        header = root.find(".//{*}g[@class='checkpoint-header inspectable']")
        self.assertIn("—", header.find("{*}title").text)
        for key in ("ascent_m", "descent_m"):
            unknown = root.find(f".//{{*}}g[@data-kind='{key}']/{{*}}g[@data-actual-available='false']")
            self.assertIn("—", "".join(unknown.itertext()))
            self.assertIsNone(unknown.find("{*}rect[@data-series='actual']"))
            self.assertIsNotNone(unknown.find("{*}rect[@data-series='planned']"))

    def test_svg_preserves_accessible_exact_values_and_escaped_provenance(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg
        result = self.build()
        result["warnings"] = ["GPS <gap> & station override"]
        result["activity"]["activity_name"] = "Race <A> & B"
        root = ET.fromstring(render_svg(result))
        metadata = json.loads(root.find("{*}metadata").text)
        self.assertEqual(metadata["warnings"], result["warnings"])
        self.assertIn("Race <A> & B", "".join(root.itertext()))
        tips = [e.text for e in root.findall(".//{*}title") if e.text]
        self.assertTrue(any("01:06:40" in tip for tip in tips))
        self.assertTrue(root.findall(".//*[@tabindex='0']/{*}title"))
        ids = [e.get("id") for e in root.iter() if e.get("id")]
        self.assertEqual(len(ids), len(set(ids)))

    def test_time_status_uses_actual_perspective_and_rounded_ties(self):
        from comparison_svg import time_status
        self.assertEqual(time_status(60)[0], "实际领先 00:01:00")
        self.assertEqual(time_status(-60)[0], "实际落后 00:01:00")
        self.assertEqual(time_status(60, True)[0], "本段快 00:01:00")
        self.assertEqual(time_status(-60, True)[0], "本段慢 00:01:00")
        for delta in (-.49, 0, .49):
            self.assertEqual(time_status(delta)[0], "持平 00:00:00")
            self.assertEqual(time_status(delta)[1:], time_status(0)[1:])
        self.assertEqual(time_status(.5)[0], "实际领先 00:00:01")
        self.assertEqual(time_status(-.5, True)[0], "本段慢 00:00:01")
        self.assertEqual(time_status(90000)[0], "实际领先 25:00:00")

    def test_line_crossings_split_at_interpolated_zero(self):
        from comparison_svg import split_at_zero
        pieces = split_at_zero([(10, 30), (50, -10), (70, 0), (90, 20)])
        self.assertEqual(pieces, [((10, 30), (40, 0)), ((40, 0), (50, -10)),
                                  ((50, -10), (70, 0)), ((70, 0), (90, 20))])
        for start, end in pieces:
            self.assertGreaterEqual(start[1] * end[1], 0)
        self.assertEqual(split_at_zero([(0, 0), (1, 0)]), [((0, 0), (1, 0))])
        self.assertEqual(split_at_zero([(0, 0)]), [])

    def test_small_segment_differences_preserve_direction_and_seconds(self):
        from comparison_svg import minute_delta_label
        for delta in (-.49, 0, .49):
            self.assertEqual(minute_delta_label(delta), "持平")
        self.assertEqual(minute_delta_label(.5), "快1秒")
        self.assertEqual(minute_delta_label(-2.1), "慢2秒")
        self.assertEqual(minute_delta_label(5.5), "快6秒")
        self.assertEqual(minute_delta_label(60), "+1.0")
        self.assertEqual(minute_delta_label(-60), "-1.0")

    def test_metric_labels_round_after_subtraction_and_scales_cover_data(self):
        from comparison_svg import axis_limit, metric_delta_label, metric_limit
        self.assertEqual(metric_delta_label(-.5), "仓库少 1 m")
        self.assertEqual(metric_delta_label(.49), "差值 0 m")
        self.assertEqual(metric_delta_label(125.5), "仓库多 126 m")
        self.assertEqual(metric_delta_label(None), "差值 —")
        self.assertEqual(axis_limit([106 * 60, -20 * 60]), 120 * 60)
        self.assertEqual(axis_limit([-43 * 60, 26 * 60]), 50 * 60)
        for values in ([0], [None], [-.4, .9], [-125.4, 256.7], [1105.2, 0]):
            limit = metric_limit(values)
            self.assertGreater(limit, 0)
            self.assertGreaterEqual(limit, max((abs(v) for v in values if v is not None), default=0))

    def test_many_targets_keep_every_panel_and_finish_status(self):
        import xml.etree.ElementTree as ET
        from comparison_svg import render_svg, time_status
        targets = [f"01:06:{second:02d}" for second in range(36, 48)]
        self.plan, self.route = compare.load_plan(self.path, self.config, targets)
        result = self.build()
        root = ET.fromstring(render_svg(result))
        panels = root.findall(".//{*}g[@class='target-panel']")
        self.assertEqual(len(panels), len(targets))
        texts = " ".join(root.itertext())
        actual = result["activity"]["totals"]["elapsed_seconds"]
        for target, panel in zip(self.plan["targets_seconds"], panels):
            self.assertIn(time_status(target - actual)[0], texts)
            self.assertIsNotNone(panel.find("{*}g[@data-kind='segment']"))
        cells = {(p.get("data-column"), p.get("data-row")) for p in panels}
        self.assertEqual(len(cells), len(targets))


class NetworkAndCliTests(unittest.TestCase):
    def test_env_precedence_and_no_shell_evaluation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / ".env"
            path.write_text("GARMIN_PERSONAL_API_KEY='file-key'\n")
            self.assertEqual(data.api_key(path, {"GARMIN_PERSONAL_API_KEY": "env-key"}), "env-key")
            self.assertEqual(data.api_key(path, {}), "file-key")
            path.write_text("GARMIN_PERSONAL_API_KEY=$(touch impossible)\n")
            with self.assertRaises(pace.InputError):
                data.api_key(path, {})
            with self.assertRaises(pace.InputError):
                data.api_key(None, {})

    def test_http_errors_and_timeouts_do_not_echo_secrets(self):
        for error in [
            HTTPError("https://example.test", 401, "private-key", {}, io.BytesIO(b"private-key")),
            URLError("private-key"), TimeoutError("private-key"),
        ]:
            with self.subTest(error=type(error).__name__):
                with patch("activity_data.urlopen", side_effect=error) as request:
                    with self.assertRaises(pace.InputError) as caught:
                        data.GarminClient("private-key").activities("2026-01-01", "2026-01-02")
                    self.assertNotIn("private-key", str(caught.exception))
                    self.assertEqual(request.call_count, 1)

    def test_auth_headers_and_regions(self):
        responses = []
        for payload in (b"bearer-value", b"[]"):
            response = unittest.mock.MagicMock()
            response.__enter__.return_value.read.return_value = payload
            responses.append(response)
        with patch("activity_data.urlopen", side_effect=responses) as request:
            self.assertEqual(data.GarminClient("key", region="cn").activities(
                "2026-01-01", "2026-01-02"), [])
            first, second = [c.args[0] for c in request.call_args_list]
            self.assertIn("garmin.cn", first.full_url)
            self.assertEqual(first.get_header("Authorization"), "ApiKey key")
            self.assertEqual(second.get_header("Authorization"), "Bearer bearer-value")
        with self.assertRaises(pace.InputError):
            data.GarminClient("key", region="other")

    def test_invalid_activity_id_and_dates_fail_before_network(self):
        with patch("activity_data.urlopen") as request:
            client = data.GarminClient("key")
            with self.assertRaises(pace.InputError):
                client.fetch("../12", Path("unused"))
            with self.assertRaises(pace.InputError):
                client.activities("2026-02-02", "2026-01-01")
            request.assert_not_called()

    def test_fetch_cache_permissions_and_overwrite_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            client = data.GarminClient("key")
            stream = io.BytesIO()
            with ZipFile(stream, "w") as archive:
                archive.writestr("activity.fit", b"synthetic")
            with patch.object(client, "get_json", return_value={"activityId": 123}) as details:
                with patch.object(client, "get", return_value=stream.getvalue()):
                    paths = client.fetch("123", Path(folder))
                    self.assertTrue(all(p.stat().st_mode & 0o777 == 0o600 for p in paths))
                    self.assertEqual(json.loads(paths[0].read_text()), {"activityId": 123})
                    with self.assertRaises(pace.InputError):
                        client.fetch("123", Path(folder))
                    self.assertEqual(details.call_count, 1)

    def test_inspect_diagnostics_and_invalid_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = route_file(folder)
            config = Path(folder) / "config.json"
            config.write_text(json.dumps({"targets": ["01:00"]}))
            args = ["inspect", str(path), "--config", str(config), "--fit", "local.fit"]
            activity = data.activity_from_messages(messages())
            activity["records"] = [{**r, "lat": r["lat"] + .1} for r in activity["records"]]
            with patch.object(compare, "read_activity", return_value=activity):
                with patch("sys.stderr", new_callable=io.StringIO) as stderr:
                    self.assertEqual(compare.main(args), 2)
                    error_text = stderr.getvalue()
                self.assertTrue(error_text, "inspect must emit a JSON diagnostic")
                self.assertTrue(error_text.startswith("{"), repr(error_text))
                self.assertIn("offset_m", json.loads(error_text)["details"])
            with self.assertRaises(pace.InputError):
                data.activity_from_messages(messages(), {"summaryDTO": []})

    def test_generate_is_offline_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = route_file(folder)
            config = Path(folder) / "config.json"
            config.write_text(json.dumps({"targets": ["01:00"]}))
            output = Path(folder) / "out"
            args = ["generate", str(path), "--config", str(config), "--fit", "local.fit",
                    "--targets", "01:00", "--output-dir", str(output)]
            with patch.object(compare, "read_activity", return_value=data.activity_from_messages(messages())):
                with patch("activity_data.urlopen", side_effect=AssertionError("Must be offline")):
                    with patch("sys.stdout", new_callable=io.StringIO):
                        self.assertEqual(compare.main(args), 0)
                    self.assertEqual([p.name for p in output.iterdir()], ["garmin-comparison.svg"])
                    with patch("sys.stderr", new_callable=io.StringIO):
                        self.assertEqual(compare.main(args), 2)
                    with patch("sys.stdout", new_callable=io.StringIO):
                        self.assertEqual(compare.main(args + ["--overwrite", "--export-json"]), 0)
                    self.assertTrue((output / "garmin-comparison.json").is_file())


if __name__ == "__main__":
    unittest.main()
