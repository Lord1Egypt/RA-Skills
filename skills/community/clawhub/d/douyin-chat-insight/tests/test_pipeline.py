#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fixture_sample() -> Path:
    fx = ROOT / "tests" / "fixtures"
    for name in ("sample_group.jsonl", "sample_group.chatlab.txt", "sample_simple.json"):
        cand = fx / name
        if cand.is_file():
            return cand
    return fx / "sample_group.jsonl"

SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from analyze import analyze_conversation  # noqa: E402
from core import load_config, redact_path, save_config  # noqa: E402
from inventory import inventory_conversations, resolve_target  # noqa: E402
from load_export import load_input  # noqa: E402
from quality_gate import assert_no_default_max_group, gate_deep, gate_inventory  # noqa: E402


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx = ROOT / "tests" / "fixtures"
        cls.cfg = load_config()
        cls.cfg["owner_aliases"] = ["主理人小A"]

    def test_load_chatlab(self):
        fx = fixture_sample()
        convs = load_input(fx)
        self.assertEqual(len(convs), 1)
        # sample_simple fallback has >=4; full chatlab sample has >=5
        min_n = 4 if fx.suffix == ".json" else 5
        self.assertGreaterEqual(len(convs[0].messages), min_n)

    def test_load_simple_json(self):
        self.assertGreaterEqual(len(load_input(self.fx / "sample_simple.json")[0].messages), 4)

    def test_load_plaintext_with_ts(self):
        conv = load_input(self.fx / "sample_plain.txt")[0]
        self.assertGreaterEqual(len(conv.messages), 2)
        self.assertTrue(any(m.ts for m in conv.messages), "plaintext [time] should parse into ts")

    def test_inventory_gate(self):
        convs = load_input(fixture_sample())
        inv = inventory_conversations(convs, self.cfg)
        ok, errs = gate_inventory(inv)
        self.assertTrue(ok, errs)
        sp = inv["conversations"][0]["source_path"]
        self.assertFalse(sp.startswith("/" + "Users/"), sp)
        self.assertFalse(sp.startswith("/" + "home/"), sp)

    def test_no_deep_without_conv(self):
        with self.assertRaises(ValueError):
            assert_no_default_max_group(True, False)

    def test_optional_enhancements_port(self):
        from analyze import analyze_conversation
        from load_export import load_input
        convs = load_input(fixture_sample())
        r = analyze_conversation(convs[0], {"owner_aliases": ["主理人"], "filters": {}, "limits": {}})
        opt = r.get("optional_enhancements") or {}
        self.assertIn("cloud_asr_required_for_core", opt)
        self.assertFalse(opt.get("cloud_asr_required_for_core"))
        self.assertIn("optional-douyin-link-asr.md", opt.get("guide_path", ""))
        self.assertIn("user_guidance_zh", opt)

    def test_deep_analyze(self):
        convs = load_input(fixture_sample())
        target = resolve_target(convs, conv="1")
        result = analyze_conversation(target, self.cfg)
        ok, errs = gate_deep(result)
        self.assertTrue(ok, errs)
        self.assertGreater(len(result["blocks"]["demand_quotes"]), 0)
        self.assertFalse(
            ("/" + "Users/") in json.dumps(result),
        )
        blob = json.dumps(result, ensure_ascii=False)
        self.assertNotRegex(blob, r"/" + r"Users/[\w.-]+")
        self.assertNotRegex(blob, r"/" + r"home/[\w.-]+")

    def test_person_filter(self):
        convs = load_input(fixture_sample())
        target = resolve_target(convs, conv="1")
        result = analyze_conversation(target, self.cfg, person="学员小B")
        for d in result["blocks"]["demand_quotes"]:
            self.assertIn("学员小B", d["sender"])

    def test_owner_aliases_yaml_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "config.yaml"
            cfg = {
                "default_locale": "zh",
                "output_dir": str(Path(td) / "out"),
                "owner_aliases": ["于先生", "群主A"],
                "report": {"formats": ["html", "md", "json"]},
                "filters": {"drop_system": True, "drop_join_leave": True, "min_demand_chars": 15},
                "limits": {
                    "inventory_top_senders": 12,
                    "demand_wall": 24,
                    "hard_fact_candidates": 12,
                    "contradiction_pairs": 8,
                },
            }
            save_config(cfg, path)
            raw = path.read_text(encoding="utf-8")
            self.assertIn("于先生", raw)
            loaded = load_config(path)
            self.assertEqual(loaded["owner_aliases"], ["于先生", "群主A"])

    def test_redact_path(self):
        self.assertEqual(redact_path("/" + "/".join(["Users","someone","secret","a.jsonl"])), "a.jsonl")
        self.assertEqual(redact_path("/" + "/".join(["home","u","x.json"])), "x.json")

    def test_cli_json_report_paths_redacted(self):
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run.py"),
                    "-i",
                    str(fixture_sample()),
                    "--conv",
                    "1",
                    "--json",
                    "-o",
                    td,
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            data = json.loads(r.stdout)
            blob = json.dumps(data, ensure_ascii=False)
            self.assertNotRegex(blob, r"/" + r"Users/|/" + r"home/|/" + r"Volumes/")
            for path in (data.get("report_paths") or {}).values():
                self.assertNotRegex(str(path), r"^/" + r"Users/|^/" + r"home/|^/" + r"Volumes/")

    def test_cli_inventory_exit0(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "run.py"), "-i", str(fixture_sample()), "--inventory-only"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue("会话概况" in r.stdout or "Inventory" in r.stdout, r.stdout)

    def test_cli_person_without_conv_fails(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "run.py"), "-i", str(fixture_sample()), "--person", "甲"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 2)
        self.assertIn("ERROR", r.stderr)

    def test_cli_missing_path_friendly(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "run.py"), "-i", "/no/such/export.jsonl"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 2)
        self.assertIn("找不到", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_cli_bad_format(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "run.py"), "-i", str(fixture_sample()),
             "--conv", "1", "--formats", "pdf"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 2)

    def test_empty_export_fails_gate(self):
        with tempfile.TemporaryDirectory() as td:
            empty = Path(td) / "empty.jsonl"
            empty.write_text(
                json.dumps({"type": "header", "conversation_id": "x", "name": "空", "members": []}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            convs = load_input(empty)
            inv = inventory_conversations(convs, self.cfg)
            ok, errs = gate_inventory(inv)
            self.assertFalse(ok)
            self.assertTrue(any("0" in e for e in errs))


    def test_load_multi_dir(self):
        d = self.fx / "multi_dir"
        if not d.is_dir():
            self.skipTest("multi_dir fixture missing")
        convs = load_input(d)
        self.assertGreaterEqual(len(convs), 1)

    def test_redact_volumes_and_tmp(self):
        self.assertEqual(redact_path("/" + "/".join(["Volumes","Cache","secret","a.jsonl"])), "a.jsonl")
        self.assertNotIn("/" + "tmp/", redact_path("/tmp/cvi/out/report.html"))

    def test_cli_version(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "run.py"), "--version"],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("douyin-chat-insight", (r.stdout + r.stderr))

    def test_doctor_ready(self):
        if os.environ.get("CVI_DOCTOR") == "1":
            self.skipTest("nested doctor")
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "doctor.py")],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("READY", r.stdout)


if __name__ == "__main__":
    unittest.main()
