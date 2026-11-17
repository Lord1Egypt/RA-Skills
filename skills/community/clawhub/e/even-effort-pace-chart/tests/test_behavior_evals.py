import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


EVALS = Path(__file__).resolve().parents[1] / "evals"
sys.path.insert(0, str(EVALS))
import evaluate


def time_water_candidate():
    return {
        "target": "05:00", "water_mode": "time", "water_target": "05:00",
        "water_ml_per_hour": 600, "water_buffer_minutes": 15,
        "water_rate_overrides": {"wpt:1": 700},
        "water_weather": {"source": "manual", "confirmed": True, "description": "晴"},
    }


class BehaviorCheckerTests(unittest.TestCase):
    def test_accepts_valid_candidate_configurations(self):
        candidates = {
            "target_only": {"target": "05:00"},
            "start_does_not_select_arrival": {
                "target": "05:00", "start_time": "06:00", "target_step_minutes": 30,
            },
            "explicit_arrival": {"target": "05:00", "secondary_display": "arrival_time"},
            "replace_target_list": {"target": "05:00", "start_time": "07:30", "fatigue_rate": 0.1},
            "preserve_zero_false": {
                "target": "05:00", "smoothing_m": 0, "ascent_smoothing_m": 0, "fatigue_rate": 0,
                "water_ml_per_10km": 0, "use_kml_altitudes": False,
            },
            "time_water_manual_conditions": time_water_candidate(),
            "explicit_svg_only": {"target": "05:00", "output_formats": ["svg"]},
            "single_target": {"targets": ["05:00"]},
            "exact_target_list": {"targets": ["04:00", "05:00", "06:00"]},
            "distance_water": {"target": "05:00", "water_ml_per_10km": 900},
            "station_rest_and_cutoff": {
                "target": "05:00",
                "checkpoint_overrides": {"wpt:1": {"rest_minutes": 10, "cutoff": "03:00"}},
            },
            "explicit_html_only": {"target": "05:00", "output_formats": ["html"]},
            "preserve_selected_options": {
                "target": "05:00", "start_time": "07:30", "fatigue_rate": 0.1,
                "secondary_display": "arrival_time", "output_formats": ["svg", "html"],
            },
        }
        self.assertEqual(set(candidates), {case["id"] for case in evaluate.SUITE["cases"]})
        for case_id, config in candidates.items():
            with self.subTest(case=case_id):
                result = evaluate.evaluate(case_id, config)
                self.assertTrue(result["passed"], result["errors"])

    def test_rejects_unrequested_display_exports_and_other_parameter_changes(self):
        for override in (
            {"secondary_display": "arrival_time"}, {"output_formats": ["svg", "json"]},
            {"sample_m": 25}, {"fatigue_rate": 0},
            {"ascent_method": "window"}, {"ascent_smoothing_m": 40}, {"ascent_threshold_m": 3},
            {"elevation_spike_m": 0}, {"distance_tolerance_m": 5},
            {"checkpoint_overrides": {"wpt:1": {"rest_minutes": 10}}},
            {"checkpoint_overrides": {"wpt:1": {"cutoff": "04:00"}}},
            {"cp_selection": []},
        ):
            with self.subTest(override=override):
                self.assertFalse(evaluate.evaluate("target_only", {"target": "05:00", **override})["passed"])

    def test_rejects_unconfirmed_weather_and_incorrect_time_water_settings(self):
        for override in (
            {"water_weather": {"source": "manual", "confirmed": False, "description": "晴"}},
            {"water_weather": {"source": "manual", "confirmed": True, "description": ""}},
            {"water_target": "04:30"},
            {"water_ml_per_hour": 700},
            {"water_buffer_minutes": 0},
            {"water_rate_overrides": {"wpt:1": 600}},
        ):
            with self.subTest(override=override):
                result = evaluate.evaluate("time_water_manual_conditions", {
                    **time_water_candidate(), **override,
                })
                self.assertFalse(result["passed"])

    def test_explicit_svg_only_overrides_selected_exports(self):
        for formats in (["svg", "html"], ["json"]):
            with self.subTest(formats=formats):
                result = evaluate.evaluate("explicit_svg_only", {
                    "target": "05:00", "output_formats": formats,
                })
                self.assertFalse(result["passed"])

    def test_exact_target_cases_reject_expansion_or_other_targets(self):
        for case_id, config in (
            ("single_target", {"target": "05:00"}),
            ("single_target", {"targets": ["04:30", "05:00"]}),
            ("exact_target_list", {"target": "05:00"}),
            ("exact_target_list", {"targets": ["04:00", "05:00", "05:30"]}),
        ):
            with self.subTest(case=case_id, config=config):
                self.assertFalse(evaluate.evaluate(case_id, config)["passed"])

    def test_distance_water_accepts_default_mode_and_rejects_time_mode(self):
        self.assertTrue(evaluate.evaluate("distance_water", {
            "target": "05:00", "water_mode": "distance", "water_ml_per_10km": 900,
        })["passed"])
        result = evaluate.evaluate("distance_water", {
            **time_water_candidate(), "water_ml_per_10km": 900,
        })
        self.assertFalse(result["passed"])

    def test_station_case_requires_requested_rest_and_cutoff(self):
        for override in (
            {"wpt:1": {"rest_minutes": 10}},
            {"wpt:1": {"cutoff": "03:00"}},
            {"wpt:1": {"rest_minutes": 5, "cutoff": "03:00"}},
            {"wpt:1": {"rest_minutes": 10, "cutoff": "04:00"}},
        ):
            with self.subTest(override=override):
                result = evaluate.evaluate("station_rest_and_cutoff", {
                    "target": "05:00", "checkpoint_overrides": override,
                })
                self.assertFalse(result["passed"])

    def test_html_only_and_preserved_options_are_checked(self):
        self.assertFalse(evaluate.evaluate("explicit_html_only", {
            "target": "05:00", "output_formats": ["svg", "html"],
        })["passed"])
        self.assertFalse(evaluate.evaluate("preserve_selected_options", {
            "target": "05:00", "start_time": "07:30", "fatigue_rate": 0.1,
            "secondary_display": "arrival_time", "output_formats": ["svg"],
        })["passed"])

    def test_every_case_has_distinct_chinese_and_english_variants(self):
        for group in ("cases", "manual_review_cases"):
            for case in evaluate.SUITE[group]:
                for language in ("zh", "en"):
                    with self.subTest(case=case["id"], language=language):
                        prompts = [case[f"prompt_{language}"], *case[f"variants_{language}"]]
                        self.assertGreaterEqual(len(prompts), 2)
                        self.assertTrue(all(isinstance(prompt, str) and prompt.strip() for prompt in prompts))
                        self.assertEqual(len(prompts), len(set(prompts)))

    def test_rejects_stale_target_list_even_when_new_target_is_present(self):
        result = evaluate.evaluate("replace_target_list", {
            "target": "05:00", "targets": ["12:00", "13:00"],
            "start_time": "07:30", "fatigue_rate": 0.1,
        })
        self.assertFalse(result["passed"])
        self.assertTrue(any("targets_seconds" in error for error in result["errors"]))

    def test_reports_invalid_candidate_as_failure(self):
        for config in ({}, {"target": "05:00", "unknown_option": True}, []):
            self.assertFalse(evaluate.evaluate("target_only", config)["passed"])

    def test_checker_cli_reports_pass_and_fail_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            for target, code in (("05:00", 0), ("06:00", 1)):
                path.write_text(json.dumps({"target": target}))
                result = subprocess.run([
                    sys.executable, str(EVALS / "evaluate.py"), "--case", "target_only",
                    "--config", str(path),
                ], capture_output=True, text=True)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(json.loads(result.stdout)["passed"], code == 0)

    def test_prompt_cli_outputs_a_variant_without_expected_results(self):
        case = next(case for case in evaluate.SUITE["cases"] if case["id"] == "replace_target_list")
        result = subprocess.run([
            sys.executable, str(EVALS / "evaluate.py"), "--case", case["id"],
            "--prompt", "--language", "en", "--variant", "2",
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "case": case["id"], "language": "en", "variant": 2,
            "prompt": case["variants_en"][0], "selected_config": case["selected_config"],
        })

    def test_prompt_cli_supports_manual_review_and_rejects_invalid_variants(self):
        case = next(case for case in evaluate.SUITE["manual_review_cases"]
                    if case["id"] == "custom_water_needs_clarification")
        command = [
            sys.executable, str(EVALS / "evaluate.py"), "--case", case["id"], "--prompt",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["prompt"], case["prompt_zh"])
        for variant in ("0", "999"):
            with self.subTest(variant=variant):
                result = subprocess.run(command + ["--variant", variant], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
