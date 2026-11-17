import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pace_chart.py"
sys.path.insert(0, str(SCRIPT.parent))
import pace_chart as pace


def gpx(points, waypoints=(), namespace="http://www.topografix.com/GPX/1/1"):
    def point(tag, values):
        lat, lon, elevation, *name = values
        ele = "" if elevation is None else f"<ele>{elevation}</ele>"
        label = "" if not name else f"<name>{name[0]}</name>"
        return f'<{tag} lat="{lat}" lon="{lon}">{ele}{label}</{tag}>'

    wpts = "".join(point("wpt", p) for p in waypoints)
    trk = "".join(point("trkpt", p) for p in points)
    return f'<gpx version="1.1" xmlns="{namespace}">{wpts}<trk><trkseg>{trk}</trkseg></trk></gpx>'


def kml(points, waypoints=(), geometry="LineString", altitude_mode="absolute", namespace="http://www.opengis.net/kml/2.2"):
    def coordinate(point, separator=","):
        lat, lon, elevation, *_ = point
        return separator.join(str(value) for value in (lon, lat, elevation) if value is not None)

    stations = "".join(
        f'<Placemark><name>{p[3]}</name><Point><coordinates>{coordinate(p)}</coordinates></Point></Placemark>'
        for p in waypoints
    )
    mode = "" if altitude_mode is None else f"<altitudeMode>{altitude_mode}</altitudeMode>"
    if geometry == "gx:Track":
        positions = "".join(f"<gx:coord>{coordinate(p, ' ')}</gx:coord>" for p in points)
    else:
        positions = "<coordinates>" + " ".join(coordinate(p) for p in points) + "</coordinates>"
    line = f"<Placemark><name>Course</name><{geometry}>{mode}{positions}</{geometry}></Placemark>"
    return (f'<kml xmlns="{namespace}" xmlns:gx="http://www.google.com/kml/ext/2.2">'
            f"<Document><Folder>{stations}{line}</Folder></Document></kml>")


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "course.gpx"
        self.points = [(0, 0, 0), (0, 0.01, 100), (0, 0.02, 0)]

    def write(self, points=None, waypoints=None, **kwargs):
        self.path.write_text(
            gpx(
                self.points if points is None else points,
                [(0, 0.01, None, "CP1")] if waypoints is None else waypoints,
                **kwargs,
            ),
            encoding="utf-8",
        )
        return self.path

    def plan(self, **config):
        return pace.build_plan(self.path, {"target": "04:00", **config})


class ConfigurationDefaultTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write()

    def test_omitted_options_match_explicit_documented_defaults(self):
        minimal = self.plan()
        explicit = self.plan(
            name="course", sample_m=5, smoothing_m=20, ascent_smoothing_m=0,
            ascent_method="hysteresis", ascent_threshold_m=10, elevation_spike_m=30, distance_tolerance_m=0,
            ascent_km_per_100m=1, fatigue_rate=0.08, water_ml_per_10km=700,
            target_step_minutes=30, start_time="06:00", output_formats=["svg"],
            secondary_display="pace", pace_basis="distance", track_index=1,
            use_kml_altitudes=False, distance_alignment="confirm",
            cp_selection=["wpt:1"], checkpoint_overrides={},
        )
        for key in ("name", "parameters", "route", "checkpoints", "targets_seconds", "schedules"):
            self.assertEqual(minimal[key], explicit[key], key)
        self.assertEqual(minimal["name"], self.path.stem)
        self.assertEqual(minimal["targets_seconds"], [10800, 12600, 14400, 16200, 18000])
        self.assertEqual([cp["id"] for cp in minimal["checkpoints"]], ["start", "wpt:1", "finish"])
        self.assertTrue(all(cp["rest_seconds"] == 0 and cp["cutoff_seconds"] is None
                            for cp in minimal["checkpoints"]))

    def test_each_omitted_numeric_option_keeps_its_default(self):
        expected = {
            "sample_m": 5, "smoothing_m": 20, "ascent_smoothing_m": 0,
            "ascent_threshold_m": 10, "elevation_spike_m": 30, "distance_tolerance_m": 0,
            "ascent_km_per_100m": 1, "fatigue_rate": 0.08,
            "water_ml_per_10km": 700, "target_step_minutes": 30,
        }
        for omitted in expected:
            with self.subTest(omitted=omitted):
                config = {key: value for key, value in expected.items() if key != omitted}
                plan = self.plan(**config)
                for key, value in expected.items():
                    self.assertEqual(plan["parameters"][key], value)

    def test_explicit_override_preserves_other_parameter_defaults(self):
        expected = {
            "sample_m": 5, "smoothing_m": 20, "ascent_smoothing_m": 0,
            "ascent_threshold_m": 10, "elevation_spike_m": 30, "distance_tolerance_m": 0,
            "ascent_km_per_100m": 1, "fatigue_rate": 0.08,
            "water_ml_per_10km": 700, "target_step_minutes": 30,
            "start_time": "06:00", "output_formats": ["svg"], "secondary_display": "pace",
        }
        for key, value in (
            ("sample_m", 10), ("smoothing_m", 40), ("ascent_smoothing_m", 60),
            ("ascent_threshold_m", 5), ("elevation_spike_m", 0), ("distance_tolerance_m", 2),
            ("ascent_km_per_100m", 0.5), ("fatigue_rate", 0.15),
            ("water_ml_per_10km", 900), ("target_step_minutes", 15),
            ("start_time", "07:30"), ("output_formats", ["json"]),
            ("secondary_display", "arrival_time"),
        ):
            with self.subTest(key=key):
                plan = self.plan(**{key: value})
                for other, default in expected.items():
                    self.assertEqual(plan["parameters"][other], value if other == key else default, other)

    def test_explicit_zero_is_preserved_instead_of_replaced_by_default(self):
        config = {key: 0 for key in (
            "smoothing_m", "ascent_smoothing_m", "ascent_km_per_100m",
            "ascent_threshold_m", "elevation_spike_m", "distance_tolerance_m",
            "fatigue_rate", "water_ml_per_10km",
        )}
        plan = self.plan(**config, checkpoint_overrides={"wpt:1": {"rest_minutes": 0}})
        for key in config:
            self.assertEqual(plan["parameters"][key], 0)
        self.assertEqual(plan["parameters"]["fatigue_exponent"], 1)
        self.assertEqual(plan["parameters"]["rest_total_seconds"], 0)
        self.assertTrue(all(cp["water_ml"] == 0 for cp in plan["checkpoints"]))
        self.assertAlmostEqual(plan["route"]["eq_distance_km"], plan["route"]["distance_m"] / 1000)

    def test_invalid_empty_values_do_not_silently_fall_back_to_defaults(self):
        for key in (
            "sample_m", "smoothing_m", "ascent_smoothing_m", "ascent_km_per_100m",
            "ascent_method", "ascent_threshold_m", "elevation_spike_m", "distance_tolerance_m",
            "fatigue_rate", "water_ml_per_10km", "target_step_minutes", "name",
            "start_time", "secondary_display", "pace_basis", "output_formats",
            "use_kml_altitudes", "distance_alignment", "checkpoint_overrides", "cp_selection",
        ):
            for value in (None, ""):
                with self.subTest(key=key, value=value), self.assertRaisesRegex(pace.InputError, key):
                    self.plan(**{key: value})
        with self.assertRaisesRegex(pace.InputError, "rest_minutes"):
            self.plan(checkpoint_overrides={"wpt:1": {"rest_minutes": None}})
        default = self.plan()
        nullable = self.plan(track_index=None, checkpoint_overrides={"wpt:1": {"cutoff": None}})
        for key in ("checkpoints", "route", "schedules"):
            self.assertEqual(nullable[key], default[key])

    def test_target_list_and_legacy_pace_are_explicit_priority_exceptions(self):
        plan = self.plan(target="05:00", targets=["03:00", "06:00"], target_step_minutes=15,
                         pace_basis="equivalent")
        self.assertEqual(plan["targets_seconds"], [10800, 21600])
        self.assertEqual(plan["parameters"]["secondary_display"], "equivalent_pace")
        selected = self.plan(pace_basis="equivalent", secondary_display="pace")
        self.assertEqual(selected["parameters"]["pace_basis"], "distance")
        self.assertEqual(selected["parameters"]["secondary_display"], "pace")
        with self.assertRaisesRegex(pace.InputError, "target"):
            pace.build_plan(self.path, {})

    def test_inspection_defaults_match_generation(self):
        inspected = pace.inspect_route(self.path)
        plan = self.plan()
        for key, expected in (("sample_m", 5), ("smoothing_m", 20), ("ascent_smoothing_m", 0),
                              ("ascent_method", "hysteresis"), ("ascent_threshold_m", 10),
                              ("elevation_spike_m", 30), ("distance_tolerance_m", 0)):
            self.assertEqual(inspected[key], expected)
            self.assertEqual(inspected[key], plan["parameters"][key])
        for key in ("distance_m", "ascent_m", "descent_m"):
            self.assertAlmostEqual(inspected[key], plan["route"][key])
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(self.path)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), inspected)

    def test_inspect_and_generate_share_processing_overrides_and_diagnostics(self):
        config = {"ascent_method": "window", "ascent_smoothing_m": 50,
                  "ascent_threshold_m": 4, "elevation_spike_m": 0, "distance_tolerance_m": 2}
        inspected = pace.inspect_route(self.path, **config)
        plan = self.plan(**config)
        self.assertEqual(inspected["diagnostics"], plan["route"]["diagnostics"])
        for key in ("distance_m", "ascent_m", "descent_m"):
            self.assertAlmostEqual(inspected[key], plan["route"][key])
        command = [sys.executable, str(SCRIPT), "inspect", str(self.path)]
        for key, value in config.items():
            command.extend(["--" + key.replace("_", "-"), str(value)])
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), inspected)

    def test_quality_metadata_is_reported_without_automatic_point_deletion(self):
        xml = self.path.read_text().replace(
            "<ele>100</ele>", "<ele>100</ele><hdop>25</hdop><vdop>bad</vdop><fix>none</fix>"
        )
        self.path.write_text(xml)
        inspected = pace.inspect_route(self.path)
        self.assertEqual(inspected["diagnostics"]["quality_flagged_points"], 1)
        self.assertEqual(inspected["diagnostics"]["quality_metadata_points"], 1)
        self.assertEqual(inspected["diagnostics"]["invalid_quality_fields"], 1)
        self.assertEqual(self.plan()["route"]["original_points"], 3)


class GeometryTests(Fixture):
    def test_gain_smoothing_is_independent_from_detailed_profile_and_carries_across_cps(self):
        points = [(0, i * 0.000045, 100 + (2 if i % 2 else -2)) for i in range(81)]
        self.write(points=points, waypoints=[(0, 0.0018, None, "CP1")])
        detailed = self.plan(ascent_method="window", ascent_smoothing_m=20)
        filtered = self.plan(ascent_method="window", ascent_smoothing_m=100)
        self.assertLess(filtered["route"]["ascent_m"], detailed["route"]["ascent_m"])
        self.assertEqual(filtered["checkpoints"][1]["profile"], detailed["checkpoints"][1]["profile"])
        self.assertEqual(filtered["route"]["grade_fractions"], detailed["route"]["grade_fractions"])
        self.assertAlmostEqual(sum(cp["ascent_m"] for cp in filtered["checkpoints"]),
                               filtered["route"]["ascent_m"])
        self.assertAlmostEqual(sum(cp["descent_m"] for cp in filtered["checkpoints"]),
                               filtered["route"]["descent_m"])
        self.assertEqual(filtered["parameters"]["ascent_smoothing_m"], 100)

    def test_default_gain_filter_preserves_long_climbs_and_short_hill_with_plateau(self):
        points = [(0, i * 0.000045, i * 0.2) for i in range(401)]
        self.write(points=points, waypoints=[(0, 0.009, None, "CP1")])
        plan = self.plan()
        self.assertAlmostEqual(plan["route"]["ascent_m"], 80)
        self.assertAlmostEqual(plan["route"]["descent_m"], 0)
        self.write(points=[(0, i * 0.000045, max(0, min(20, (i - 30) * 4, (50 - i) * 4)))
                           for i in range(81)],
                   waypoints=[(0, 0.0018, None, "CP1")])
        plan = self.plan()
        elevations = [p[1] for cp in plan["checkpoints"] for p in cp["profile"]]
        self.assertGreater(max(elevations), 1)
        self.assertAlmostEqual(plan["route"]["ascent_m"], 20)
        self.assertAlmostEqual(plan["route"]["descent_m"], 20)

    def test_default_gain_preserves_source_peaks_and_smoothing_is_opt_in(self):
        self.write(points=[(0, i * 0.000045, 20 if i == 40 else 0) for i in range(81)],
                   waypoints=[(0, 0.0018, None, "CP1")])
        filtered = self.plan(ascent_smoothing_m=40)
        unblurred = self.plan()
        self.assertAlmostEqual(filtered["route"]["ascent_m"], 0)
        self.assertAlmostEqual(filtered["route"]["descent_m"], 0)
        self.assertAlmostEqual(unblurred["route"]["ascent_m"], 20)
        self.assertAlmostEqual(unblurred["route"]["descent_m"], 20)
        self.assertEqual(unblurred["parameters"]["ascent_smoothing_m"], 0)
        self.assertEqual(filtered["parameters"]["ascent_smoothing_m"], 40)
        self.assertEqual(filtered["route"]["distance_m"], unblurred["route"]["distance_m"])
        self.assertEqual(filtered["route"]["grade_fractions"], unblurred["route"]["grade_fractions"])
        for filtered_cp, unblurred_cp in zip(filtered["checkpoints"], unblurred["checkpoints"]):
            self.assertEqual(filtered_cp["profile"], unblurred_cp["profile"])
        inspected = pace.inspect_route(self.path)
        self.assertAlmostEqual(inspected["ascent_m"], unblurred["route"]["ascent_m"])

    def test_distance_namespace_and_duplicate_coordinates(self):
        for ns in ("", "http://www.topografix.com/GPX/1/0", "http://www.topografix.com/GPX/1/1"):
            self.write(points=[self.points[0], self.points[0], *self.points[1:]], namespace=ns)
            route = pace.load_route(self.path)
            self.assertAlmostEqual(route.total_m, 2223.90, delta=0.1)
            self.assertEqual(len(route.points), 3)

    def test_missing_elevation_and_invalid_coordinates(self):
        for points in (
            [(0, 0, 0), (0, 0.01, None)],
            [(0, 0, 0), (91, 0.01, 0)],
            [(0, 0, 0), (0, float("nan"), 0)],
        ):
            self.write(points=points)
            with self.assertRaises(pace.InputError):
                pace.load_route(self.path)

    def test_multiple_routes_require_selection(self):
        self.write()
        xml = self.path.read_text()
        track = xml[xml.index("<trk>"):xml.index("</trk>") + 6]
        self.path.write_text(xml.replace("</gpx>", track + "</gpx>"))
        with self.assertRaisesRegex(pace.InputError, "track_index"):
            pace.load_route(self.path)
        self.assertGreater(pace.load_route(self.path, track_index=2).total_m, 0)

    def test_disconnected_segments_are_not_joined(self):
        self.write()
        self.path.write_text(
            self.path.read_text().replace(
                '</trkseg>', '</trkseg><trkseg><trkpt lat="1" lon="1"><ele>0</ele></trkpt></trkseg>'
            )
        )
        with self.assertRaisesRegex(pace.InputError, "segment"):
            pace.load_route(self.path)

    def test_route_points_and_embedded_cp(self):
        self.write(points=[(*p, "CP1") if i == 1 else p for i, p in enumerate(self.points)], waypoints=[])
        self.path.write_text(
            self.path.read_text().replace("<trk><trkseg>", "<rte>").replace("</trkseg></trk>", "</rte>")
            .replace("trkpt", "rtept")
        )
        plan = self.plan()
        self.assertEqual([p["name"] for p in plan["checkpoints"]], ["起点", "CP1", "终点"])

    def test_five_metre_sampling_and_exact_twenty_metre_window(self):
        route = pace.Route(
            [(0, 0, 0), (0, 0.001, 0)],
            [pace.Sample(0, 0), pace.Sample(10, 10), pace.Sample(20, 0), pace.Sample(40, 0)],
            [],
        )
        profile = pace.smooth_profile(route, 5, 20)
        self.assertEqual([p.distance_m for p in profile], list(range(0, 41, 5)))
        self.assertAlmostEqual(profile[2].elevation_m, 5)
        self.assertAlmostEqual(profile[0].elevation_m, 0)
        self.assertAlmostEqual(profile[-1].elevation_m, 0)
        self.assertGreater(profile[2].elevation_m, profile[4].elevation_m)

    def test_linear_elevation_and_zero_smoothing(self):
        route = pace.Route([], [pace.Sample(0, 0), pace.Sample(100, 100)], [])
        smoothed = pace.smooth_profile(route, 5, 20)
        self.assertAlmostEqual(smoothed[10].elevation_m, 50)
        original = pace.smooth_profile(route, 5, 0)
        self.assertEqual((original[0].elevation_m, original[-1].elevation_m), (0, 100))

    def test_grade_boundaries(self):
        self.assertEqual(
            [pace.grade_bin(value) for value in (-16, -15, -10, -5, 0, 5, 10, 15, 16)],
            [0, 0, 1, 2, 3, 4, 5, 6, 6],
        )


class KmlTests(Fixture):
    def test_equivalent_gpx_and_kml_share_statistics_and_schedules(self):
        self.write()
        original = self.plan()
        self.path.write_text(kml(self.points, [(0, 0.01, None, "CP1")]))
        converted = self.plan()
        for key in ("route", "targets_seconds", "schedules"):
            self.assertEqual(converted[key], original[key], key)
        self.assertEqual([cp["name"] for cp in converted["checkpoints"]], ["起点", "CP1", "终点"])
        self.assertEqual(converted["checkpoints"][1]["id"], "placemark:1:point:1")
        self.assertEqual(converted["parameters"], original["parameters"])

    def test_namespaces_gx_track_and_point_ids(self):
        for namespace in ("http://www.opengis.net/kml/2.2", ""):
            for geometry in ("LineString", "gx:Track"):
                with self.subTest(namespace=namespace, geometry=geometry):
                    self.path.write_text(kml(self.points, [(0, 0.01, None, "CP1")], geometry, namespace=namespace))
                    route = pace.load_route(self.path)
                    self.assertEqual(route.points, self.points)
                    self.assertEqual(route.candidates[0]["id"], "placemark:1:point:1")
                    self.assertTrue(route.candidates[0]["recognized"])
                    self.assertAlmostEqual(route.total_m, 2223.90, delta=0.1)

    def test_altitude_mode_requires_explicit_coordinate_override(self):
        for mode in (None, "clampToGround"):
            with self.subTest(mode=mode):
                self.path.write_text(kml(self.points, altitude_mode=mode))
                with self.assertRaisesRegex(pace.InputError, "use_kml_altitudes"):
                    pace.load_route(self.path)
                route = pace.load_route(self.path, use_kml_altitudes=True)
                self.assertEqual(route.points, self.points)
                self.assertTrue(any("altitude" in warning.lower() for warning in route.warnings))
        for mode in ("relativeToGround", "relativeToSeaFloor", "clampToSeaFloor", "unknown"):
            self.path.write_text(kml(self.points, altitude_mode=mode))
            with self.assertRaisesRegex(pace.InputError, "altitude"):
                pace.load_route(self.path, use_kml_altitudes=True)
        with self.assertRaisesRegex(pace.InputError, "boolean"):
            pace.load_route(self.path, use_kml_altitudes="yes")

    def test_missing_invalid_and_duplicate_coordinates(self):
        for point in ((0, 0.01, None), (91, 0.01, 0), (0, 181, 0), (0, 0.01, float("nan"))):
            self.path.write_text(kml([self.points[0], point, self.points[-1]]))
            with self.assertRaises(pace.InputError):
                pace.load_route(self.path, use_kml_altitudes=True)
        for coordinates in ("0,0,0 0.01,0,1,2", "0,0,0 bad,0,1", "0,0,0"):
            self.path.write_text(
                '<kml><Placemark><LineString><altitudeMode>absolute</altitudeMode>'
                f'<coordinates>{coordinates}</coordinates></LineString></Placemark></kml>'
            )
            with self.assertRaises(pace.InputError):
                pace.load_route(self.path)
        self.path.write_text(kml([self.points[0], *self.points]))
        self.assertEqual(pace.load_route(self.path).points, self.points)

    def test_multigeometry_and_multitrack_require_selection(self):
        xml = kml(self.points, [(0, 0.01, None, "CP1")])
        root = ET.fromstring(xml)
        namespace = {"k": "http://www.opengis.net/kml/2.2"}
        line = root.find(".//k:LineString", namespace)
        line_xml = ET.tostring(line, encoding="unicode")
        gx_root = ET.fromstring(kml([(0, 0, 0), (0.02, 0, 0)], geometry="gx:Track"))
        track = next(e for e in gx_root.iter() if pace.tag(e) == "Track")
        track_xml = ET.tostring(track, encoding="unicode")
        geometry = f'<MultiGeometry>{line_xml}<gx:MultiTrack>{track_xml}</gx:MultiTrack></MultiGeometry>'
        self.path.write_text(xml.replace(
            xml[xml.index("<LineString>"):xml.index("</LineString>") + len("</LineString>")], geometry
        ))
        with self.assertRaises(pace.InputError) as error:
            pace.load_route(self.path)
        self.assertEqual([item["track_index"] for item in error.exception.details], [1, 2])
        self.assertEqual(pace.load_route(self.path, 1).points, self.points)
        self.assertEqual(pace.load_route(self.path, 2).points, [(0, 0, 0), (0.02, 0, 0)])
        for index in (0, 3, True):
            with self.assertRaises(pace.InputError):
                pace.load_route(self.path, index)

    def test_named_landmarks_require_selection_and_cp_overrides_work(self):
        self.path.write_text(kml(self.points, [(0, 0.01, None, "Village")]))
        with self.assertRaisesRegex(pace.InputError, "cp_selection"):
            self.plan()
        plan = self.plan(cp_selection=["placemark:1:point:1"],
                         checkpoint_overrides={"placemark:1:point:1": {"rest_minutes": 5, "cutoff": "02:00"}})
        self.assertEqual(plan["checkpoints"][1]["rest_seconds"], 300)
        self.assertEqual(plan["checkpoints"][1]["cutoff_seconds"], 7200)
        self.assertAlmostEqual(plan["schedules"][0]["checkpoints"][-1]["departure_seconds"], 10800)

    def test_multitrack_inherits_altitude_mode(self):
        xml = kml(self.points, geometry="gx:Track", altitude_mode=None)
        self.path.write_text(xml.replace("<gx:Track>", "<gx:MultiTrack><altitudeMode>absolute</altitudeMode><gx:Track>")
                             .replace("</gx:Track>", "</gx:Track></gx:MultiTrack>"))
        self.assertEqual(pace.load_route(self.path).points, self.points)
        self.path.write_text(self.path.read_text().replace("absolute", "relativeToGround"))
        with self.assertRaisesRegex(pace.InputError, "altitude"):
            pace.load_route(self.path, use_kml_altitudes=True)

    def test_empty_invalid_xml_and_dtd_errors(self):
        for text in ("<kml><NetworkLink/></kml>", "<other/>", "<kml>", '<!DOCTYPE kml [<!ENTITY x "a">]><kml/>'):
            self.path.write_text(text)
            with self.assertRaises(pace.InputError):
                pace.load_route(self.path)

    def test_kml_cli_generates_all_formats_and_reports_height_errors(self):
        self.path = Path(self.temp.name) / "race.kml"
        self.path.write_text(kml(self.points, [(0, 0.01, None, "CP1")], altitude_mode=None))
        inspected = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(self.path), "--use-kml-altitudes"],
                                   capture_output=True, text=True)
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertEqual(json.loads(inspected.stdout)["cp_candidates"][0]["name"], "CP1")
        config = Path(self.temp.name) / "race.json"
        config.write_text(json.dumps({"targets": ["04:00"], "use_kml_altitudes": True,
                                     "output_formats": ["svg", "html", "csv", "json"]}))
        result = subprocess.run([sys.executable, str(SCRIPT), "generate", str(self.path),
                                 "--config", str(config), "--output-dir", str(Path(self.temp.name) / "out")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["outputs"]), 4)
        plan = json.loads((Path(self.temp.name) / "out/pace-chart.json").read_text())
        self.assertEqual(plan["source"]["filename"], "race.kml")
        self.assertEqual(plan["schedules"][0]["checkpoints"][-1]["departure_seconds"], 14400)
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(self.path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("use_kml_altitudes", json.loads(result.stderr)["error"])


class CheckpointTests(Fixture):
    def test_recognized_cp_excludes_landmarks_and_turns(self):
        self.write(waypoints=[
            (0, 0.015, None, "Right turn"),
            (0, 0.01, None, "CP1 水站"),
            (0, 0.012, None, "Scenic viewpoint"),
        ])
        plan = self.plan()
        self.assertEqual([p["name"] for p in plan["checkpoints"]], ["起点", "CP1 水站", "终点"])
        self.assertEqual(plan["checkpoints"][1]["id"], "wpt:2")

    def test_no_cp_requires_manual_list_and_ambiguous_names_require_confirmation(self):
        self.write(waypoints=[])
        with self.assertRaisesRegex(pace.InputError, "checkpoints"):
            self.plan()
        self.write(waypoints=[(0, 0.01, None, "Hilltop")])
        with self.assertRaisesRegex(pace.InputError, "cp_selection"):
            self.plan()
        self.assertEqual(self.plan(cp_selection=["wpt:1"])["checkpoints"][1]["name"], "Hilltop")

    def test_off_route_requires_explicit_override(self):
        self.write(waypoints=[(0.002, 0.01, None, "CP1")])
        with self.assertRaisesRegex(pace.InputError, "100"):
            self.plan()
        plan = self.plan(checkpoint_overrides={"wpt:1": {"allow_off_route": True}})
        self.assertEqual(plan["checkpoints"][1]["name"], "CP1")
        self.assertTrue(any("off-route" in warning for warning in plan["warnings"]))

    def test_out_and_back_cp_requires_distance_disambiguation(self):
        self.write(points=[(0, 0, 0), (0, 0.01, 100), (0, 0, 0)],
                   waypoints=[(0, 0.005, None, "CP1")])
        with self.assertRaisesRegex(pace.InputError, "ambiguous"):
            self.plan()
        plan = self.plan(checkpoint_overrides={"wpt:1": {"distance_km": 0.556}})
        self.assertAlmostEqual(plan["checkpoints"][1]["distance_m"], 556)

    def test_combined_start_finish_preserves_venue_and_checks_both_endpoints(self):
        for name in ("起终点-古城", "起終點-古城", "Start / Finish - Town"):
            self.write(points=[(0, 0, 0), (0, 0.01, 100), (0, 0, 0)],
                       waypoints=[(0, 0, None, name), (0, 0.01, None, "CP1")])
            plan = self.plan()
            cps = plan["checkpoints"]
            self.assertEqual(len(cps), 3)
            self.assertEqual((cps[0]["name"], cps[-1]["name"]), (name + "（起点）", name + "（终点）"))
            self.assertEqual((cps[0]["id"], cps[-1]["id"]), ("wpt:1:start", "wpt:1:finish"))
            self.assertEqual(cps[0]["distance_m"], 0)
            self.assertEqual(cps[-1]["distance_m"], plan["route"]["distance_m"])
        self.write(waypoints=[(0, 0, None, "起终点-古城")])
        with self.assertRaisesRegex(pace.InputError, "combined start/finish"):
            self.plan()

    def test_manual_distance_mismatch_requires_confirmed_scaling(self):
        self.write(waypoints=[])
        cps = [{"name": "CP1", "distance_km": 1}, {"name": "终点", "distance_km": 2}]
        with self.assertRaisesRegex(pace.InputError, "scale"):
            self.plan(checkpoints=cps)
        plan = self.plan(checkpoints=cps, distance_alignment="scale")
        self.assertAlmostEqual(plan["checkpoints"][1]["distance_m"], plan["route"]["distance_m"] / 2)
        self.assertAlmostEqual(plan["checkpoints"][1]["official_distance_km"], 1)
        self.assertAlmostEqual(plan["route"]["distance_scale"], plan["route"]["distance_m"] / 2000)

    def test_invalid_cp_lists(self):
        self.write()
        for cps in (
            [],
            [{"name": "CP1", "distance_km": -1}],
            [{"name": "CP1", "distance_km": 1}, {"name": "终点", "distance_km": 0.5}],
            [{"name": "终点", "distance_km": 2.2239, "rest_minutes": 5}],
        ):
            with self.assertRaises(pace.InputError):
                self.plan(checkpoints=cps)

    def test_cp_splits_preserve_route_statistics(self):
        self.write()
        plan = self.plan()
        cps = plan["checkpoints"]
        for key, route_key in (("segment_distance_m", "distance_m"), ("ascent_m", "ascent_m"),
                               ("descent_m", "descent_m"), ("eq_distance_km", "eq_distance_km")):
            self.assertAlmostEqual(sum(cp[key] for cp in cps), plan["route"][route_key])
        for cp in cps[1:]:
            self.assertAlmostEqual(sum(cp["grade_fractions"]), 1)


EXAMPLE_DIR = SCRIPT.parents[3] / "examples" / "huizhou-gucheng-100k"
REAL_GPX = EXAMPLE_DIR / "徽州古城100K.gpx"
KML_EXAMPLE_DIR = SCRIPT.parents[3] / "examples" / "大境门" / "DGW100K"
REAL_KML = KML_EXAMPLE_DIR / "2026京东大境门古长城越野赛by UTMB®DGW100K.kml"


@unittest.skipUnless(REAL_GPX.is_file(), "Repository example GPX is not present")
class RealRouteTests(unittest.TestCase):
    def test_real_course_automatic_cps_and_four_outputs(self):
        config = json.loads((EXAMPLE_DIR / "config.json").read_text(encoding="utf-8"))
        plan = pace.build_plan(REAL_GPX, config)
        self.assertEqual(plan["targets_seconds"], [hours * 3600 for hours in (12, 13, 14, 15, 16)])
        self.assertAlmostEqual(plan["route"]["distance_m"], 101248.68, delta=1)
        self.assertAlmostEqual(plan["route"]["ascent_m"], 5965.47, delta=0.01)
        self.assertAlmostEqual(plan["route"]["descent_m"], 5965.439, delta=0.01)
        self.assertEqual(plan["route"]["diagnostics"]["elevation_spikes_corrected"], 0)
        self.assertEqual(len(plan["checkpoints"]), 12)
        self.assertEqual(plan["checkpoints"][0]["name"], "起终点-徽州古城（起点）")
        self.assertEqual(plan["checkpoints"][-1]["name"], "起终点-徽州古城（终点）")
        self.assertEqual(plan["checkpoints"][-3]["name"], "CP12-瞻淇村")
        self.assertEqual(plan["checkpoints"][-2]["name"], "CP13-画家村")
        for schedule in plan["schedules"]:
            self.assertAlmostEqual(schedule["checkpoints"][-1]["departure_seconds"],
                                   schedule["target_seconds"])
            self.assertAlmostEqual(sum(t["moving_seconds"] for t in schedule["checkpoints"]),
                                   schedule["target_seconds"])
        for cp_key, route_key in (("segment_distance_m", "distance_m"), ("ascent_m", "ascent_m"),
                                  ("descent_m", "descent_m"), ("eq_distance_km", "eq_distance_km")):
            self.assertAlmostEqual(sum(cp[cp_key] for cp in plan["checkpoints"]), plan["route"][route_key])
        inspected = pace.inspect_route(REAL_GPX)
        self.assertAlmostEqual(inspected["ascent_m"], plan["route"]["ascent_m"])
        with tempfile.TemporaryDirectory() as output:
            paths = pace.write_outputs(plan, Path(output))
            self.assertEqual(len(paths), 4)
            ET.parse(Path(output) / "pace-chart.svg")
            with (Path(output) / "pace-chart.csv").open(encoding="utf-8-sig", newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 60)

    def test_window_method_remains_available_for_reference_comparison(self):
        plan = pace.build_plan(REAL_GPX, {
            "target": "14:00", "ascent_method": "window", "ascent_smoothing_m": 100,
        })
        reference_gains = [397, 394, 439, 666, 893, 583, 531, 403, 567, 233, 220]
        self.assertAlmostEqual(plan["route"]["ascent_m"], sum(reference_gains), delta=100)
        error = sum(abs(cp["ascent_m"] - expected)
                    for cp, expected in zip(plan["checkpoints"][1:], reference_gains))
        self.assertLess(error / len(reference_gains), 20)


@unittest.skipUnless(REAL_KML.is_file(), "Repository KML example is not present")
class RealKmlRouteTests(unittest.TestCase):
    def test_dajingmen_course_checkpoint_order_and_exports(self):
        config = json.loads((KML_EXAMPLE_DIR / "config.json").read_text(encoding="utf-8"))
        plan = pace.build_plan(REAL_KML, config)
        self.assertEqual(plan["targets_seconds"], [hour * 3600 for hour in range(10, 25)])
        self.assertEqual(plan["parameters"]["start_time"], "06:00")
        self.assertEqual(plan["parameters"]["fatigue_rate"], 0.08)
        self.assertEqual(plan["parameters"]["secondary_display"], "pace")
        self.assertAlmostEqual(plan["route"]["distance_m"], 99694.41, delta=1)
        self.assertAlmostEqual(plan["route"]["ascent_m"], 3729, delta=0.01)
        self.assertAlmostEqual(plan["route"]["descent_m"], 3765, delta=0.01)
        names = [cp["name"] for cp in plan["checkpoints"]]
        self.assertEqual(names, ["起终点-大境门（起点）", "D1四岔村7.9", "D2啕北营村21.3",
                                 "D3察汗陀螺村28.1", "D4窑子沟36.7", "D5五十家45.5",
                                 "SP1小红泥湾54.5", "D6黄土窑61.1", "D7土井子72.8",
                                 "D8清河村80.1", "D9翠屏庵89.5", "起终点-大境门（终点）"])
        self.assertTrue(any("altitude" in warning.lower() for warning in plan["warnings"]))
        for schedule in plan["schedules"]:
            self.assertAlmostEqual(schedule["checkpoints"][-1]["departure_seconds"], schedule["target_seconds"])
        with tempfile.TemporaryDirectory() as output:
            paths = pace.write_outputs(plan, Path(output))
            self.assertEqual(len(paths), 4)
            self.assertEqual(json.loads((Path(output) / "pace-chart.json").read_text())["configuration"], config)
            svg = ET.parse(Path(output) / "pace-chart.svg")
            self.assertEqual("".join(svg.getroot().itertext()).count("Target"), 15)
            with (Path(output) / "pace-chart.csv").open(encoding="utf-8-sig", newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))), 180)


class TimingTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write(points=[(0, 0, 0), (0, 0.01, 0), (0, 0.02, 0)])

    def test_default_targets_and_custom_step_and_list(self):
        self.assertEqual(self.plan()["targets_seconds"], [10800, 12600, 14400, 16200, 18000])
        self.assertEqual(self.plan(target_step_minutes=15)["targets_seconds"],
                         [12600, 13500, 14400, 15300, 16200])
        self.assertEqual(self.plan(targets=["30:00", "25:30"])["targets_seconds"], [91800, 108000])

    def test_zero_fatigue_linear_and_default_doubling(self):
        plan = self.plan(fatigue_rate=0, targets=["04:00"])
        schedule = plan["schedules"][0]["checkpoints"]
        self.assertAlmostEqual(schedule[1]["arrival_seconds"], 7200)
        self.assertAlmostEqual(schedule[2]["arrival_seconds"], 14400)
        b = pace.fatigue_exponent(0.08)
        self.assertAlmostEqual(2 ** (b - 1), 1.08)
        plan = self.plan(targets=["04:00"])
        times = plan["schedules"][0]["checkpoints"]
        self.assertGreater(times[2]["moving_seconds"], times[1]["moving_seconds"])

    def test_rests_are_included_and_cutoffs_mark_arrival_and_departure(self):
        plan = self.plan(targets=["04:00"], fatigue_rate=0,
                         checkpoint_overrides={"wpt:1": {"rest_minutes": 20, "cutoff": "02:00"}})
        times = plan["schedules"][0]["checkpoints"]
        self.assertAlmostEqual(times[1]["arrival_seconds"], 6600)
        self.assertAlmostEqual(times[1]["departure_seconds"], 7800)
        self.assertEqual(times[1]["cutoff_status"], "departure_late")
        self.assertAlmostEqual(times[-1]["departure_seconds"], 14400)
        self.assertAlmostEqual(sum(t["moving_seconds"] for t in times) + 1200, 14400)
        plan = self.plan(targets=["04:00"], fatigue_rate=0,
                         checkpoint_overrides={"wpt:1": {"cutoff": "01:59"}})
        self.assertEqual(plan["schedules"][0]["checkpoints"][1]["cutoff_status"], "arrival_late")
        plan = self.plan(targets=["04:00"], fatigue_rate=0,
                         checkpoint_overrides={"wpt:1": {"cutoff": "02:00"}})
        self.assertEqual(plan["schedules"][0]["checkpoints"][1]["cutoff_status"], "on_time")

    def test_invalid_targets_and_parameters(self):
        for config in (
            {"target": "00:30"}, {"targets": ["04:00", "04:00"]}, {"targets": []},
            {"target": "04:60"}, {"fatigue_rate": -0.1}, {"sample_m": 0},
            {"smoothing_m": -1}, {"sample_m": float("nan")}, {"typo": 1},
            {"ascent_smoothing_m": -1}, {"start_time": "invalid date"},
            {"targets": ["00:10"], "checkpoint_overrides": {"wpt:1": {"rest_minutes": 20}}},
        ):
            with self.assertRaises(pace.InputError):
                self.plan(**config)

    def test_water_and_extended_time_display(self):
        plan = self.plan(targets=["30:00"])
        self.assertAlmostEqual(sum(p["water_ml"] for p in plan["checkpoints"]),
                               plan["route"]["eq_distance_km"] * 70)
        self.assertEqual(pace.format_duration(91800), "25:30:00")
        self.assertEqual(pace.format_pace(359.6), "6:00")
        cps = plan["checkpoints"]
        self.assertAlmostEqual(cps[0]["water_ml"], cps[1]["eq_distance_km"] * 70)
        self.assertAlmostEqual(cps[1]["water_ml"], cps[2]["eq_distance_km"] * 70)
        self.assertEqual(cps[-1]["water_ml"], 0)

    def test_reference_interval_pace_uses_horizontal_distance_and_can_select_equivalent(self):
        self.write()
        plan = self.plan(targets=["04:00"])
        cp, timing = plan["checkpoints"][1], plan["schedules"][0]["checkpoints"][1]
        expected = timing["moving_seconds"] / (cp["segment_distance_m"] / 1000)
        self.assertAlmostEqual(timing["pace_seconds_per_km"], expected)
        self.assertGreater(timing["pace_seconds_per_km"], timing["eq_pace_seconds_per_km"])
        self.assertEqual(plan["parameters"]["pace_basis"], "distance")
        self.assertIn("括号内：区间配速", pace.render_svg(plan))
        equivalent = self.plan(targets=["04:00"], pace_basis="equivalent")
        alternate = equivalent["schedules"][0]["checkpoints"][1]
        self.assertAlmostEqual(alternate["pace_seconds_per_km"], alternate["eq_pace_seconds_per_km"])
        self.assertIn("括号内：区间等强配速", pace.render_svg(equivalent))
        self.assertEqual(plan["targets_seconds"], equivalent["targets_seconds"])
        self.assertEqual(timing["departure_seconds"], alternate["departure_seconds"])
        with self.assertRaises(pace.InputError):
            self.plan(pace_basis="typo")


class RuntimeContractTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write()

    def test_extreme_sampling_values_report_input_errors(self):
        for config, message in (
            ({"sample_m": 1e-320}, "sample_m"),
            ({"smoothing_m": 1e-20}, "smoothing"),
            ({"ascent_smoothing_m": 1e-20}, "smoothing"),
            ({"sample_m": 10 ** 400}, "finite"),
        ):
            with self.subTest(config=config), self.assertRaisesRegex(pace.InputError, message):
                self.plan(**config)

    def test_target_conflict_is_reported_without_changing_list_precedence(self):
        plan = self.plan(target="05:00", targets=["12:00", "13:00"])
        self.assertEqual(plan["targets_seconds"], [43200, 46800])
        self.assertTrue(any("target" in warning and "targets" in warning for warning in plan["warnings"]))

    def test_summary_reports_effective_defaults_and_verification(self):
        plan = self.plan(target="05:00")
        summary = pace.plan_summary(plan)
        self.assertEqual(summary["parameters"], plan["parameters"])
        self.assertEqual(summary["target_source"], "target")
        self.assertEqual(summary["targets_seconds"], [14400, 16200, 18000, 19800, 21600])
        self.assertEqual(summary["route"], plan["route"])
        self.assertEqual([cp["name"] for cp in summary["checkpoints"]],
                         [cp["name"] for cp in plan["checkpoints"]])
        checks = summary["verification"]
        self.assertTrue(checks["finish_targets_match"])
        self.assertTrue(checks["rests_match"])
        self.assertEqual(checks["cutoff_checked_stations"], 0)
        self.assertEqual(checks["cutoff_unchecked_stations"], 2)
        self.assertEqual(checks["cutoff_failures"], [])
        self.assertNotIn("profile", summary["checkpoints"][1])
        json.dumps(summary, allow_nan=False)

    def test_summary_detects_timing_mismatch_and_cutoff_failures(self):
        plan = self.plan(targets=["04:00"], checkpoint_overrides={
            "wpt:1": {"rest_minutes": 20, "cutoff": "00:30"},
        })
        summary = pace.plan_summary(plan)
        self.assertEqual(summary["target_source"], "targets")
        self.assertEqual(summary["verification"]["cutoff_checked_stations"], 1)
        self.assertEqual(summary["verification"]["cutoff_failures"], [
            {"target_seconds": 14400, "checkpoint_id": "wpt:1", "status": "arrival_late"},
        ])
        plan["schedules"][0]["checkpoints"][-1]["departure_seconds"] += 10
        summary = pace.plan_summary(plan)
        self.assertFalse(summary["verification"]["finish_targets_match"])
        self.assertFalse(summary["verification"]["rests_match"])

    def test_cli_returns_summary_without_extra_output_files(self):
        config = Path(self.temp.name) / "config.json"
        config.write_text('{"target":"05:00","start_time":"06:00"}')
        output = Path(self.temp.name) / "out"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.path),
             "--config", str(config), "--output-dir", str(output)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["parameters"]["secondary_display"], "pace")
        self.assertEqual(payload["summary"]["parameters"]["output_formats"], ["svg"])
        self.assertEqual(list(output.iterdir()), [output / "pace-chart.svg"])

    def test_invalid_later_output_preserves_existing_files(self):
        output = Path(self.temp.name) / "out"
        output.mkdir()
        svg = output / "pace-chart.svg"
        svg.write_text("original")
        (output / "pace-chart.html").mkdir()
        with self.assertRaises((pace.InputError, OSError)):
            pace.write_outputs(self.plan(output_formats=["svg", "html"]), output, overwrite=True)
        self.assertEqual(svg.read_text(), "original")

    def test_export_replace_failure_rolls_back_existing_and_new_files(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                output = Path(self.temp.name) / str(existing)
                output.mkdir()
                svg, html = output / "pace-chart.svg", output / "pace-chart.html"
                if existing:
                    svg.write_text("original svg")
                html.write_text("original html")
                original_replace = Path.replace

                def fail_html(source, destination):
                    if Path(destination) == html and source.name == "pace-chart.html":
                        raise OSError("simulated replacement failure")
                    return original_replace(source, destination)

                with mock.patch.object(Path, "replace", fail_html):
                    with self.assertRaisesRegex(OSError, "simulated"):
                        pace.write_outputs(self.plan(output_formats=["svg", "html"]), output, overwrite=True)
                self.assertEqual(svg.read_text() if existing else svg.exists(),
                                 "original svg" if existing else False)
                self.assertEqual(html.read_text(), "original html")
                self.assertEqual(set(output.iterdir()), {svg, html} if existing else {html})

    def test_staging_failure_leaves_all_outputs_unchanged(self):
        output = Path(self.temp.name) / "out"
        pace.write_outputs(self.plan(output_formats=["svg", "html"]), output)
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        original_open = Path.open

        def fail_staging_html(path, *args, **kwargs):
            if path.parent != output and path.name == "pace-chart.html" and args and args[0] == "w":
                raise OSError("simulated disk full")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", fail_staging_html):
            with self.assertRaisesRegex(OSError, "disk full"):
                pace.write_outputs(self.plan(output_formats=["svg", "html"]), output, overwrite=True)
        self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, before)

    def test_failed_rollback_retains_original_for_manual_recovery(self):
        output = Path(self.temp.name) / "out"
        output.mkdir()
        svg = output / "pace-chart.svg"
        svg.write_text("original svg")
        original_replace = Path.replace

        def fail_replace_and_recovery(source, destination):
            if source.name in ("pace-chart.html", "pace-chart.svg.bak"):
                raise OSError("simulated permission error")
            return original_replace(source, destination)

        with mock.patch.object(Path, "replace", fail_replace_and_recovery):
            with self.assertRaisesRegex(pace.InputError, "rollback incomplete") as context:
                pace.write_outputs(self.plan(output_formats=["svg", "html"]), output, overwrite=True)
        recovery = Path(context.exception.details["recovery_directory"])
        self.assertEqual((recovery / "pace-chart.svg.bak").read_text(), "original svg")
        self.assertEqual(context.exception.details["rollback_failures"][0]["path"], str(svg))

    def test_symlink_outputs_are_rejected_including_dangling_links(self):
        for exists in (False, True):
            output = Path(self.temp.name) / str(exists)
            output.mkdir()
            destination = output / "user-file"
            if exists:
                destination.write_text("original")
            (output / "pace-chart.svg").symlink_to(destination)
            with self.subTest(exists=exists), self.assertRaisesRegex(pace.InputError, "symlink"):
                pace.write_outputs(self.plan(), output, overwrite=True)
            self.assertEqual(destination.read_text() if exists else destination.exists(),
                             "original" if exists else False)


class ExportTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write()

    def test_five_hour_configuration_defaults_to_svg_and_pace(self):
        plan = self.plan(target="05:00", target_step_minutes=30, start_time="06:00")
        self.assertEqual(plan["targets_seconds"], [4 * 3600, 4.5 * 3600, 5 * 3600, 5.5 * 3600, 6 * 3600])
        self.assertEqual(plan["parameters"]["output_formats"], ["svg"])
        self.assertEqual(plan["parameters"]["secondary_display"], "pace")
        output_dir = Path(self.temp.name) / "default"
        paths = pace.write_outputs(plan, output_dir)
        self.assertEqual(paths, [output_dir / "pace-chart.svg"])
        self.assertEqual(set(output_dir.iterdir()), set(paths))
        svg = paths[0].read_text()
        self.assertIn("发枪：06:00", svg)
        self.assertIn("括号内：区间配速", svg)
        for cp, timing in zip(plan["checkpoints"][1:], plan["schedules"][0]["checkpoints"][1:]):
            expected = timing["moving_seconds"] / (cp["segment_distance_m"] / 1000)
            self.assertIn(f"({pace.format_chart_pace(expected)})", svg)

    def test_output_format_subsets_and_order(self):
        for formats in (["html"], ["csv"], ["json"], ["svg", "json"], ["json", "csv", "html", "svg"]):
            with self.subTest(formats=formats):
                plan = self.plan(output_formats=formats)
                output_dir = Path(self.temp.name) / "-".join(formats)
                paths = pace.write_outputs(plan, output_dir)
                self.assertEqual([path.suffix[1:] for path in paths], formats)
                self.assertEqual(set(output_dir.iterdir()), set(paths))
                for path in paths:
                    if path.suffix == ".json":
                        self.assertEqual(json.loads(path.read_text()), plan)
                    elif path.suffix == ".svg":
                        ET.parse(path)
                    elif path.suffix == ".csv":
                        with path.open(encoding="utf-8-sig", newline="") as stream:
                            self.assertEqual(len(list(csv.DictReader(stream))),
                                             len(plan["checkpoints"]) * len(plan["schedules"]))
                    else:
                        self.assertIn("<!doctype html>", path.read_text())

    def test_invalid_output_formats_fail_before_creating_files(self):
        for value in (None, "svg", [], ["pdf"], ["SVG"], ["svg", "svg"], [True], [{}]):
            with self.subTest(value=value), self.assertRaisesRegex(pace.InputError, "output_formats"):
                self.plan(output_formats=value)

    def test_output_conflicts_only_apply_to_selected_files(self):
        output_dir = Path(self.temp.name) / "selected"
        output_dir.mkdir()
        other = output_dir / "pace-chart.json"
        other.write_text("existing user output")
        plan = self.plan()
        paths = pace.write_outputs(plan, output_dir)
        self.assertEqual(paths, [output_dir / "pace-chart.svg"])
        self.assertEqual(other.read_text(), "existing user output")
        with self.assertRaises(pace.InputError):
            pace.write_outputs(plan, output_dir)
        pace.write_outputs(plan, output_dir, overwrite=True)
        self.assertEqual(other.read_text(), "existing user output")
        svg_before = paths[0].read_bytes()
        with self.assertRaises(pace.InputError):
            pace.write_outputs(self.plan(output_formats=["svg", "json"]), output_dir)
        self.assertEqual(paths[0].read_bytes(), svg_before)
        self.assertEqual(other.read_text(), "existing user output")

    def test_secondary_display_selects_pace_without_changing_schedule(self):
        baseline = self.plan(targets=["04:00"])
        self.assertEqual(baseline["parameters"]["secondary_display"], "pace")
        for mode, field, label in (
            ("pace", "distance_pace_seconds_per_km", "区间配速"),
            ("equivalent_pace", "eq_pace_seconds_per_km", "区间等强配速"),
        ):
            with self.subTest(mode=mode):
                plan = self.plan(targets=["04:00"], secondary_display=mode)
                cp, timing = plan["checkpoints"][1], plan["schedules"][0]["checkpoints"][1]
                expected = f'({pace.format_chart_pace(timing[field])})'
                self.assertEqual(pace.timing_lines(plan, cp, timing)[1], expected)
                self.assertAlmostEqual(timing["pace_seconds_per_km"], timing[field])
                for render in (pace.render_html, pace.render_svg):
                    output = render(plan)
                    self.assertIn(expected, output)
                    self.assertIn("括号内：" + label, output)
                self.assertEqual(pace.timing_lines(plan, plan["checkpoints"][0],
                                                 plan["schedules"][0]["checkpoints"][0]), ["00:00"])
                for original, selected in zip(baseline["schedules"][0]["checkpoints"],
                                              plan["schedules"][0]["checkpoints"]):
                    for key in ("arrival_seconds", "departure_seconds", "moving_seconds"):
                        self.assertEqual(original[key], selected[key])

    def test_secondary_display_overrides_legacy_pace_basis(self):
        legacy = self.plan(pace_basis="equivalent")
        self.assertEqual(legacy["parameters"]["secondary_display"], "equivalent_pace")
        for mode, basis in (("pace", "distance"), ("equivalent_pace", "equivalent")):
            plan = self.plan(pace_basis="equivalent" if basis == "distance" else "distance",
                             secondary_display=mode)
            self.assertEqual(plan["parameters"]["pace_basis"], basis)
            timing = plan["schedules"][0]["checkpoints"][1]
            self.assertEqual(timing["pace_seconds_per_km"],
                             timing["distance_pace_seconds_per_km"] if basis == "distance"
                             else timing["eq_pace_seconds_per_km"])

    def test_arrival_clock_uses_arrival_before_rest_and_previous_rests(self):
        self.write(points=[(0, 0, 0), (0, 0.01, 0), (0, 0.02, 0)])
        plan = self.plan(targets=["04:00"], fatigue_rate=0,
                         secondary_display="arrival_time", start_time="2026-10-31T23:30",
                         checkpoint_overrides={"wpt:1": {"rest_minutes": 20}})
        times = plan["schedules"][0]["checkpoints"]
        for index, expected in enumerate((
            ["00:00", "(23:30)"],
            ["02:10", "(次日 01:20)"],
            ["04:00", "(次日 03:30)"],
        )):
            self.assertEqual(pace.timing_lines(plan, plan["checkpoints"][index], times[index]), expected)
            for output in (pace.render_html(plan), pace.render_svg(plan)):
                self.assertIn(expected[1], output)
                self.assertIn("括号内：到达时间", output)
        baseline = self.plan(targets=["04:00"], fatigue_rate=0,
                             checkpoint_overrides={"wpt:1": {"rest_minutes": 20}})
        self.assertEqual(plan["schedules"], baseline["schedules"])
        # Pace mode still preserves the elapsed arrival detail at resting stations.
        self.assertEqual(pace.timing_lines(baseline, baseline["checkpoints"][1],
                                         baseline["schedules"][0]["checkpoints"][1])[-1], "到 01:50")

    def test_arrival_clock_rollover_and_minute_truncation(self):
        for start, target, expected in (
            ("2026-10-31 06:00", "04:00:59", "(10:00)"),
            ("2026-10-31 23:30", "00:29:59", "(23:59)"),
            ("2026-10-31 23:30", "00:30", "(次日 00:00)"),
            ("2026-12-31 23:30", "25:00", "(+2天 00:30)"),
        ):
            with self.subTest(start=start, target=target):
                plan = self.plan(targets=[target], secondary_display="arrival_time", start_time=start)
                lines = pace.timing_lines(plan, plan["checkpoints"][-1],
                                          plan["schedules"][0]["checkpoints"][-1])
                self.assertEqual(lines[1], expected)

    def test_default_start_is_six_am_in_all_display_modes(self):
        for mode in ("pace", "equivalent_pace", "arrival_time"):
            with self.subTest(mode=mode):
                plan = self.plan(targets=["30:00"], secondary_display=mode, output_formats=["json"])
                self.assertEqual(plan["parameters"]["start_time"], "06:00")
                for render in (pace.render_html, pace.render_svg):
                    output = render(plan)
                    self.assertIn("发枪：06:00", output)
                    if mode == "arrival_time":
                        self.assertIn("(06:00)", output)
                        self.assertIn("(次日 12:00)", output)
                paths = pace.write_outputs(plan, Path(self.temp.name) / mode)
                saved = json.loads(next(p for p in paths if p.suffix == ".json").read_text())
                self.assertEqual(saved["parameters"]["start_time"], "06:00")

    def test_explicit_start_overrides_default_with_or_without_date(self):
        baseline = self.plan(targets=["25:00"])
        for start in ("07:30", "2026-10-31 07:30", "2026-10-31T07:30"):
            with self.subTest(start=start):
                plan = self.plan(targets=["25:00"], secondary_display="arrival_time", start_time=start)
                self.assertEqual(plan["parameters"]["start_time"], start)
                self.assertEqual(plan["schedules"], baseline["schedules"])
                for render in (pace.render_html, pace.render_svg):
                    output = render(plan)
                    self.assertIn("发枪：" + start.replace("T", " "), output)
                    self.assertIn("(07:30)", output)
                    self.assertIn("(次日 08:30)", output)

    def test_invalid_secondary_display_and_start_are_actionable(self):
        for value in ("unknown", "", None, 1, True, []):
            with self.subTest(value=value), self.assertRaisesRegex(pace.InputError, "secondary_display"):
                self.plan(secondary_display=value)
        for value in ("6:00", "24:00", "06:60", "", None, 600, "2026-02-30 06:00"):
            with self.subTest(value=value), self.assertRaisesRegex(pace.InputError, "start_time"):
                self.plan(secondary_display="arrival_time", start_time=value)

    def test_all_formats_share_values_and_svg_is_standalone(self):
        plan = self.plan(output_formats=["svg", "html", "csv", "json"])
        paths = pace.write_outputs(plan, Path(self.temp.name) / "result")
        self.assertEqual({p.suffix for p in paths}, {".svg", ".html", ".csv", ".json"})
        saved = json.loads(next(p for p in paths if p.suffix == ".json").read_text())
        self.assertEqual(saved, plan)
        svg = next(p for p in paths if p.suffix == ".svg").read_text()
        html = next(p for p in paths if p.suffix == ".html").read_text()
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        for element in root.iter():
            self.assertNotEqual(element.tag.rsplit("}", 1)[-1], "foreignObject")
            self.assertNotIn("href", element.attrib)
        self.assertIn("@page", html)
        self.assertIn("table-header-group", html)
        with next(p for p in paths if p.suffix == ".csv").open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), len(plan["checkpoints"]) * len(plan["schedules"]))
        for schedule in plan["schedules"]:
            for cp, timing in zip(plan["checkpoints"], schedule["checkpoints"]):
                record = next(row for row in rows if row["checkpoint_id"] == cp["id"]
                              and float(row["target_seconds"]) == schedule["target_seconds"])
                self.assertAlmostEqual(float(record["departure_seconds"]), timing["departure_seconds"])
                for output in (html, svg):
                    self.assertIn(pace.format_chart_time(timing["departure_seconds"]), output)
                    if timing["pace_seconds_per_km"] is not None:
                        self.assertIn(pace.format_chart_pace(timing["pace_seconds_per_km"]), output)

    def test_escape_text_and_long_names_many_columns(self):
        name = '赛事 & <script>alert("x")</script>'
        long_name = "超长补给站名称" * 8 + " & <tag>"
        plan = self.plan(name=name, targets=["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
                         checkpoint_overrides={"wpt:1": {"name": long_name}})
        svg = pace.render_svg(plan)
        html = pace.render_html(plan)
        root = ET.fromstring(svg)
        self.assertIn(name, "".join(root.itertext()))
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertGreater(float(root.attrib["width"]), 1500)
        self.assertIn("超长补给站名称", "".join(root.itertext()))

    def test_vector_graphics_have_cell_positions(self):
        plan = self.plan()
        root = ET.fromstring(pace.render_svg(plan))
        ns = {"svg": "http://www.w3.org/2000/svg"}
        graphics = [item for item in root.findall("svg:g", ns) if "transform" in item.attrib]
        self.assertEqual(len(graphics), 2 * len(plan["checkpoints"]))
        # Histogram and profile groups must be placed below the header inside their columns.
        for item in graphics:
            transform = item.attrib["transform"].removeprefix("translate(").removesuffix(")")
            x, y = (float(value) for value in transform.split())
            self.assertGreaterEqual(x, 100)
            self.assertLess(x, 360)
            self.assertGreaterEqual(y, 100)

    def test_station_details_show_supplied_cutoffs_only(self):
        for config, details in (
            ({}, ["CP1"]),
            ({"rest_minutes": 5}, ["CP1", "停留 5 min"]),
            ({"cutoff": "02:00"}, ["CP1", "关门 02:00:00"]),
            ({"cutoff": "02:00", "rest_minutes": 5}, ["CP1", "停留 5 min", "关门 02:00:00"]),
        ):
            plan = self.plan(checkpoint_overrides={"wpt:1": config})
            self.assertEqual(pace.cp_details(plan["checkpoints"][1]), details)
            for output in (pace.render_html(plan), pace.render_svg(plan)):
                self.assertIn("CP1", output)
                if "cutoff" in config:
                    self.assertIn("关门 02:00:00", output)
                else:
                    self.assertNotIn("关门", output)

    def test_chart_ends_at_table_and_retains_source_metadata(self):
        plan = self.plan()
        root = ET.fromstring(pace.render_svg(plan))
        ns = {"svg": "http://www.w3.org/2000/svg"}
        cells = [rect for rect in root.findall("svg:rect", ns) if "data-column" in rect.attrib]
        table_bottom = max(float(cell.attrib["y"]) + float(cell.attrib["height"]) for cell in cells)
        self.assertAlmostEqual(float(root.attrib["height"]), table_bottom + 1)
        for text in root.findall("svg:text", ns):
            self.assertLess(float(text.attrib["y"]), table_bottom)
        metadata = json.loads(root.find("svg:metadata", ns).text)
        self.assertEqual(metadata, plan["article"])
        html = pace.render_html(plan)
        self.assertIn("</table></div>\n</main>", html)
        self.assertIn(f'<meta name="author" content="{plan["article"]["author"]}">', html)
        self.assertIn(plan["article"]["url"], html)
        self.assertTrue(plan["warnings"])
        self.assertIsNone(plan["checkpoints"][1]["cutoff_seconds"])

    def test_reference_table_layout_colours_start_time_and_minute_times(self):
        plan = self.plan(start_time="2026-10-31 06:00", targets=["12:00", "13:00", "14:00", "15:00", "16:00"])
        self.assertEqual([label for label, _ in pace.BASE_COLUMNS],
                         ["累积\n距离", "坡度\n分布", "肖像图", "距离", "爬升", "下降", "水", "位置"])
        for output in (pace.render_svg(plan), pace.render_html(plan)):
            self.assertIn("2026-10-31 06:00", output)
            self.assertIn("Target", output)
            self.assertIn("14.0 Hr", output)
        root = ET.fromstring(pace.render_svg(plan))
        ns = {"svg": "http://www.w3.org/2000/svg"}
        by_column = {}
        for cell in root.findall("svg:rect", ns):
            if "data-column" in cell.attrib:
                by_column.setdefault(cell.attrib["data-column"], set()).add(cell.attrib["fill"])
        for column in ("distance", "ascent", "descent", "water"):
            self.assertTrue(by_column[column] - {"#ffffff"})
        histogram = ET.fromstring(pace.histogram_svg([0.1, 0.1, 0.1, 0.4, 0.1, 0.1, 0.1]))
        bars = histogram.findall("svg:rect", ns)
        self.assertEqual([bar.attrib["fill"] for i, bar in enumerate(bars) if i != 3], ["#111111"] * 6)
        self.assertEqual(bars[3].attrib["fill"], "#ffffff")
        self.assertEqual(pace.format_chart_time(25 * 3600 + 59), "25:00")
        self.assertEqual(pace.format_chart_pace(359.6), "06:00")

    def test_csv_formula_names_and_overwrite_protection(self):
        plan = self.plan(checkpoint_overrides={"wpt:1": {"name": "=SUM(1,2)"}}, output_formats=["csv"])
        output = Path(self.temp.name) / "out"
        paths = pace.write_outputs(plan, output)
        csv_path = next(p for p in paths if p.suffix == ".csv")
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertTrue(any(row["checkpoint_name"] == "'=SUM(1,2)" for row in rows))
        with self.assertRaises(pace.InputError):
            pace.write_outputs(plan, output)
        pace.write_outputs(plan, output, overwrite=True)

    def test_cli_inspect_generate_and_actionable_error(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "inspect", str(self.path)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["cp_candidates"][0]["name"], "CP1")
        config = Path(self.temp.name) / "race.json"
        config.write_text(json.dumps({"target": "04:00"}))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.path), "--config", str(config),
             "--output-dir", str(Path(self.temp.name) / "cli")], text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["outputs"],
                         [str(Path(self.temp.name) / "cli/pace-chart.svg")])
        self.write(waypoints=[])
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.path), "--config", str(config),
             "--output-dir", str(Path(self.temp.name) / "error")], text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("checkpoints", json.loads(result.stderr)["error"])
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
