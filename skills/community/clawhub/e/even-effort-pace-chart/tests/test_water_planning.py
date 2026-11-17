from contextlib import redirect_stderr, redirect_stdout
import csv
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import unittest
from unittest import mock
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET

from test_pace_chart import Fixture, pace
import compare_activity as compare


class TableCells(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.in_body = True
        elif self.in_body and tag == "tr":
            self.row = []
        elif self.in_body and tag == "td":
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.in_body and tag == "td":
            self.row.append(" ".join(self.cell))
            self.cell = None
        elif self.in_body and tag == "tr":
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_body = False


class DistanceWaterTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write(points=[(0, 0, 0), (0, 0.01, 0), (0, 0.02, 0)])

    def test_distance_water_metadata_identifies_comparison_and_actual_rate(self):
        for rate, displayed in ((700, "700"), (900.25, "900.25"), (900.234567, "900.234567"), (0, "0")):
            with self.subTest(rate=rate):
                plan = self.plan(water_ml_per_10km=rate)
                svg = ET.fromstring(pace.render_svg(plan))
                visible_svg = " ".join("".join(text.itertext()) for text in svg.findall("{*}text"))
                html = pace.render_html(plan)
                visible_html = html.split("<header>", 1)[1].split("</header>", 1)[0]
                for name, content in (("SVG", visible_svg), ("HTML", visible_html)):
                    for expected in (f"{displayed} ml/10 等效公里", "仅供赛段比较", "非个人饮水建议"):
                        self.assertTrue(expected in content, f"{name}: missing {expected}")

    def test_distance_water_matches_next_leg_and_exports(self):
        plan = self.plan(water_mode="distance", water_ml_per_10km=900)
        checkpoints = plan["checkpoints"]
        self.assertGreater(checkpoints[0]["water_ml"], 0)
        self.assertEqual(checkpoints[0]["water_ml"], checkpoints[1]["segment_water_ml"])
        self.assertEqual(checkpoints[1]["water_ml"], checkpoints[2]["segment_water_ml"])
        self.assertEqual(checkpoints[2]["water_ml"], 0)

        rows = list(csv.DictReader(io.StringIO(pace.csv_text(plan))))
        self.assertEqual([float(row["water_ml"]) for row in rows[:3]],
                         [cp["water_ml"] for cp in checkpoints])

        svg = list(ET.fromstring(pace.render_svg(plan)))
        svg_cells = []
        for index, element in enumerate(svg):
            if element.get("data-column") != "water":
                continue
            texts = []
            for sibling in svg[index + 1:]:
                if sibling.tag.endswith("}rect"):
                    break
                texts.extend(sibling.itertext())
            svg_cells.append(" ".join(texts))
        html = TableCells()
        html.feed(pace.render_html(plan))
        expected = [f'{cp["water_ml"]:.0f}' for cp in checkpoints]
        self.assertEqual([cell.strip() for cell in svg_cells], expected)
        self.assertEqual([row[6].strip() for row in html.rows], expected)


class TimeWaterTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write(points=[(0, 0, 0), (0, 0.01, 0), (0, 0.02, 0)])
        self.manual_weather = {
            "source": "manual",
            "confirmed": True,
            "description": "预计晴天，按个人训练经验确认",
        }

    def time_config(self, **overrides):
        return {
            "targets": ["04:00"],
            "fatigue_rate": 0,
            "checkpoint_overrides": {"wpt:1": {"rest_minutes": 20}},
            "water_mode": "time",
            "water_ml_per_hour": 600,
            "water_buffer_minutes": 15,
            "water_rate_overrides": {"wpt:1": 900},
            "water_weather": self.manual_weather,
            **overrides,
        }

    def test_time_water_uses_next_leg_target_and_excludes_station_rest(self):
        plan = self.plan(**self.time_config())
        checkpoints = plan["checkpoints"]
        timings = plan["schedules"][0]["checkpoints"]
        self.assertEqual(timings[1]["moving_seconds"], 6600)
        self.assertEqual(timings[2]["moving_seconds"], 6600)
        self.assertAlmostEqual(checkpoints[0]["water_ml"], 1250)
        self.assertAlmostEqual(checkpoints[1]["segment_water_ml"], 1250)
        self.assertAlmostEqual(checkpoints[1]["water_ml"], 1875)
        self.assertAlmostEqual(checkpoints[2]["segment_water_ml"], 1875)
        self.assertEqual(checkpoints[2]["water_ml"], 0)
        self.assertEqual(plan["parameters"]["water_target_seconds"], 14400)
        self.assertEqual(plan["parameters"]["water_weather_source"], "manual")

    def test_reference_target_is_explicit_and_shared_across_exports(self):
        plan = self.plan(**self.time_config(
            targets=["03:00", "04:00"], water_target="03:00",
        ))
        self.assertEqual(plan["parameters"]["water_target_seconds"], 10800)
        self.assertIn("水量目标：03:00", pace.render_svg(plan))
        self.assertIn("水量目标：03:00", pace.render_html(plan))
        rows = list(csv.DictReader(io.StringIO(pace.csv_text(plan))))
        self.assertEqual({row["water_reference_target_seconds"] for row in rows}, {"10800.0"})
        self.assertEqual({row["water_weather_source"] for row in rows}, {"manual"})
        self.assertEqual(float(rows[0]["water_ml"]), plan["checkpoints"][0]["water_ml"])
        self.assertEqual(plan["water_weather"]["description"], self.manual_weather["description"])

    def test_reference_target_seconds_and_water_assumptions_are_visible(self):
        plan = self.plan(**self.time_config(
            targets=["03:00:30", "04:00"], water_target="03:00:30",
        ))
        for document in (pace.render_svg(plan), pace.render_html(plan)):
            self.assertIn("水量目标：03:00:30", document)
            self.assertIn("600", document)
            self.assertIn("15", document)
            self.assertIn("分段", document)
            self.assertNotIn("仅供赛段比较", document)

    def test_chart_water_cells_show_each_departure_rate(self):
        plan = self.plan(**self.time_config())
        svg = list(ET.fromstring(pace.render_svg(plan)))
        svg_cells = []
        for index, element in enumerate(svg):
            if element.get("data-column") != "water":
                continue
            texts = []
            for sibling in svg[index + 1:]:
                if sibling.tag.endswith("}rect"):
                    break
                texts.extend(sibling.itertext())
            svg_cells.append(" ".join(texts))

        html = TableCells()
        html.feed(pace.render_html(plan))
        html_cells = [row[6] for row in html.rows]
        for cells in (svg_cells, html_cells):
            self.assertEqual(len(cells), 3)
            self.assertIn("1250", cells[0])
            self.assertIn("600 ml/h", cells[0])
            self.assertIn("1875", cells[1])
            self.assertIn("900 ml/h", cells[1])
            self.assertEqual(cells[2].strip(), "0")

    def test_distance_mode_water_cells_do_not_show_hourly_rates(self):
        plan = self.plan(targets=["04:00"])
        for document in (pace.render_svg(plan), pace.render_html(plan)):
            self.assertNotIn("ml/h", document)

    def test_time_options_are_not_silently_ignored_in_distance_mode(self):
        with self.assertRaisesRegex(pace.InputError, "water_mode"):
            self.plan(water_ml_per_hour=600)

    def test_invalid_time_water_configuration_is_rejected(self):
        cases = [
            ({"water_mode": "other"}, "water_mode"),
            ({"water_ml_per_hour": 0}, "water_ml_per_hour"),
            ({"water_ml_per_hour": float("nan")}, "water_ml_per_hour"),
            ({"water_buffer_minutes": -1}, "water_buffer_minutes"),
            ({"water_rate_overrides": {"missing": 500}}, "water_rate_overrides"),
            ({"water_rate_overrides": {"wpt:1": -1}}, "water_rate_overrides"),
            ({"targets": ["03:00", "04:00"]}, "water_target"),
            ({"water_target": "05:00"}, "water_target"),
            ({"water_weather": {"source": "manual", "confirmed": False, "description": "晴"}}, "confirmed"),
            ({"water_weather": {"source": "manual", "confirmed": True, "description": ""}}, "description"),
        ]
        for changes, message in cases:
            with self.subTest(changes=changes), self.assertRaisesRegex(pace.InputError, message):
                self.plan(**self.time_config(**changes))

    def test_comparison_target_override_does_not_require_water_target(self):
        original = {"target": "04:00", **self.time_config(
            targets=["03:00", "04:00"], water_target="04:00",
        )}
        plan, _ = compare.load_plan(self.path, original, ["01:30", "02:30"])
        self.assertEqual(plan["targets_seconds"], [5400, 9000])
        self.assertEqual(original["targets"], ["03:00", "04:00"])
        self.assertEqual(original["water_target"], "04:00")


class WeatherPreviewTests(Fixture):
    def setUp(self):
        super().setUp()
        self.write(points=[(0, 0, 0), (0, 0.01, 0), (0, 0.02, 0)])
        self.day = (datetime.now(timezone.utc) + timedelta(days=1)).date()
        self.config = {
            "targets": ["04:00"],
            "fatigue_rate": 0,
            "start_time": f"{self.day} 06:00",
            "water_timezone": "UTC",
            "water_mode": "time",
        }
        self.config_path = Path(self.temp.name) / "race.json"
        self.output = Path(self.temp.name) / "output"

    def response(self, *, missing=None):
        start = datetime.combine(self.day, datetime.min.time(), tzinfo=timezone.utc) - timedelta(days=1)
        hourly = {
            "time": [int((start + timedelta(hours=hour)).timestamp()) for hour in range(72)],
            "temperature_2m": [20.0] * 72,
            "relative_humidity_2m": [60] * 72,
            "wind_speed_10m": [10.0] * 72,
            "precipitation_probability": [20] * 72,
        }
        if missing:
            hourly.pop(missing)
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"hourly": hourly}).encode()
        return response

    def run_generate(self):
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            status = pace.main([
                "generate", str(self.path), "--config", str(self.config_path),
                "--output-dir", str(self.output),
            ])
        return status, json.loads(output.getvalue() or errors.getvalue())

    def test_preview_then_confirm_generates_without_requery(self):
        with mock.patch.object(pace, "urlopen", create=True, return_value=self.response()) as request:
            status, preview = self.run_generate()
        self.assertEqual(status, 0)
        self.assertEqual(preview["status"], "needs_water_confirmation")
        self.assertEqual(preview["outputs"], [])
        self.assertFalse(self.output.exists())
        snapshot = preview["water_weather"]
        self.assertEqual(snapshot["source"], "open-meteo")
        self.assertFalse(snapshot["confirmed"])
        self.assertEqual(len(snapshot["segments"]), 2)
        self.assertTrue(snapshot["segments"][0]["hourly"])
        query = parse_qs(urlsplit(request.call_args.args[0].full_url).query)
        self.assertIn("latitude", query)
        self.assertIn("longitude", query)
        self.assertIn("temperature_2m", query["hourly"][0])
        locations = [
            parse_qs(urlsplit(call.args[0].full_url).query)
            for call in request.call_args_list
        ]
        self.assertEqual(
            [(float(item["latitude"][0]), float(item["longitude"][0])) for item in locations],
            [(0.0, 0.005), (0.0, 0.015)],
        )

        snapshot["confirmed"] = True
        self.config.update(water_ml_per_hour=600, water_weather=snapshot)
        with mock.patch.object(pace, "urlopen", create=True, side_effect=AssertionError("unexpected network")):
            status, result = self.run_generate()
        self.assertEqual(status, 0)
        self.assertEqual(len(result["outputs"]), 1)
        self.assertTrue((self.output / "pace-chart.svg").is_file())
        self.assertEqual(result["summary"]["parameters"]["water_weather_source"], "open-meteo")

    def test_local_time_is_converted_to_utc_across_midnight(self):
        self.config.update(start_time=f"{self.day} 23:00", water_timezone="Asia/Shanghai")
        with mock.patch.object(pace, "urlopen", create=True, return_value=self.response()):
            status, preview = self.run_generate()
        self.assertEqual(status, 0)
        segments = preview["water_weather"]["segments"]
        self.assertEqual(segments[0]["start_time"], f"{self.day}T15:00:00+00:00")
        self.assertEqual(segments[1]["end_time"], f"{self.day}T19:00:00+00:00")
        self.assertEqual(segments[0]["hourly"][0]["time"], f"{self.day}T15:00:00+00:00")

    def test_corrupt_confirmed_forecast_is_not_used(self):
        with mock.patch.object(pace, "urlopen", create=True, return_value=self.response()):
            status, preview = self.run_generate()
        self.assertEqual(status, 0)
        snapshot = preview["water_weather"]
        snapshot["confirmed"] = True
        snapshot["segments"][0]["hourly"] = ["invalid"]
        self.config.update(water_ml_per_hour=600, water_weather=snapshot)
        with mock.patch.object(pace, "urlopen", create=True, side_effect=AssertionError("unexpected network")):
            status, error = self.run_generate()
        self.assertEqual(status, 2)
        self.assertIn("water_weather", error["error"])
        self.assertFalse(self.output.exists())

    def test_default_mode_stays_offline(self):
        self.config = {"targets": ["04:00"]}
        with mock.patch.object(pace, "urlopen", create=True, side_effect=AssertionError("unexpected network")):
            status, result = self.run_generate()
        self.assertEqual(status, 0)
        self.assertTrue(result["outputs"])

    def test_non_object_configuration_reports_input_error(self):
        self.config = []
        status, error = self.run_generate()
        self.assertEqual(status, 2)
        self.assertIn("configuration", error["error"])

    def test_changed_start_time_requires_fresh_confirmation(self):
        with mock.patch.object(pace, "urlopen", create=True, return_value=self.response()):
            status, preview = self.run_generate()
        self.assertEqual(status, 0)
        preview["water_weather"]["confirmed"] = True
        self.config.update(
            water_ml_per_hour=600,
            water_weather=preview["water_weather"],
            start_time=f"{self.day} 07:00",
        )
        with mock.patch.object(pace, "urlopen", create=True, return_value=self.response()) as request:
            status, changed = self.run_generate()
        self.assertEqual(status, 0)
        self.assertEqual(changed["status"], "needs_water_confirmation")
        self.assertFalse(changed["water_weather"]["confirmed"])
        self.assertGreater(request.call_count, 0)
        self.assertFalse(self.output.exists())

    def test_failed_or_incomplete_forecast_has_explicit_manual_fallback(self):
        failures = [
            URLError("offline"),
            self.response(missing="relative_humidity_2m"),
        ]
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                patcher = (mock.patch.object(pace, "urlopen", create=True, side_effect=failure)
                           if isinstance(failure, Exception) else
                           mock.patch.object(pace, "urlopen", create=True, return_value=failure))
                with patcher:
                    status, error = self.run_generate()
                self.assertEqual(status, 2)
                self.assertIn("manual", error["error"].lower())
                self.assertFalse(self.output.exists())
        self.config.update(
            water_ml_per_hour=600,
            water_weather={"source": "manual", "confirmed": True, "description": "预报不可用，按个人经验"},
        )
        with mock.patch.object(pace, "urlopen", create=True, side_effect=AssertionError("unexpected network")):
            status, result = self.run_generate()
        self.assertEqual(status, 0)
        self.assertEqual(result["summary"]["parameters"]["water_weather_source"], "manual")

    def test_date_and_timezone_are_required_before_network(self):
        for changes, expected in (
            ({"start_time": "06:00"}, "start_time"),
            ({"water_timezone": "not/a-zone"}, "water_timezone"),
        ):
            original = dict(self.config)
            self.config.update(changes)
            with mock.patch.object(pace, "urlopen", create=True) as request:
                status, error = self.run_generate()
            self.assertEqual(status, 2)
            self.assertIn(expected, error["error"])
            request.assert_not_called()
            self.config = original

    def test_ambiguous_and_nonexistent_dst_start_times_fail_before_network(self):
        self.config["water_timezone"] = "America/New_York"
        for start_time in ("2026-03-08 02:30", "2026-11-01 01:30"):
            with self.subTest(start_time=start_time):
                self.config["start_time"] = start_time
                with mock.patch.object(pace, "urlopen", create=True) as request:
                    status, error = self.run_generate()
                self.assertEqual(status, 2)
                self.assertIn("ambiguous or nonexistent", error["error"])
                request.assert_not_called()
