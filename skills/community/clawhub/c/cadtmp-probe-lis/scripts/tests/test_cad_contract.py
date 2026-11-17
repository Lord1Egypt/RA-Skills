#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from cad_contract import contractize_payload, validate_contract_payload  # noqa: E402


class CadContractTest(unittest.TestCase):
    def test_direct_evidence_is_confirmed_and_mainline(self):
        payload = {
            "schema": "cad-descriptive-geometry/v7",
            "source_file": "sample.dwg",
            "views": [{"id": "v1", "title": "一层平面图", "layer": "TITLE", "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"}],
        }
        result = contractize_payload(payload)
        contract = result["contract"]
        self.assertEqual(contract["summary"]["confirmed_evidence"], 1)
        self.assertEqual(contract["summary"]["review_required"], 0)
        self.assertEqual(len(contract["candidates"]), 1)
        self.assertEqual(contract["candidates"][0]["confidence_tier"], "confirmed_evidence")
        self.assertFalse(contract["candidates"][0]["final_quantity"])
        self.assertEqual(validate_contract_payload(result), [])

    def test_inferred_low_confidence_and_duplicate_split(self):
        payload = {
            "schema": "cad-mep-geometry/v2",
            "source_file": "sample.dwg",
            "route_segments": [
                {"id": "r1", "layer": "PIPE", "geometry": [0, 0, 10, 0], "confidence": 0.78, "status": "candidate"},
                {"id": "r2", "layer": "PIPE", "geometry": [0, 0, 10, 0], "confidence": 0.78, "status": "candidate"},
                {"id": "r3", "layer": "PIPE", "geometry": [20, 0, 30, 0], "confidence": 0.40, "status": "review", "review_reason": "低置信"},
            ],
        }
        result = contractize_payload(payload)
        contract = result["contract"]
        self.assertEqual(contract["summary"]["inferred_candidate"], 1)
        self.assertEqual(contract["summary"]["review_required"], 2)
        self.assertEqual(len(contract["candidates"]), 1)
        self.assertEqual(len(contract["review_candidates"]), 2)
        self.assertIn("duplicate_candidate", contract["review_candidates"][0]["review_reasons"])
        ids = [row["id"] for row in contract["candidates"] + contract["review_candidates"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(validate_contract_payload(result), [])

    def test_validator_rejects_final_quantity_and_bad_reason(self):
        payload = {
            "schema": "cad-measurement-candidates/v1",
            "source_file": "sample.json",
            "measurements": [{"id": "m1", "kind": "length", "value": 1.0, "unit": "m", "confidence": 0.42, "status": "review"}],
        }
        result = contractize_payload(payload)
        result["contract"]["review_candidates"][0]["final_quantity"] = True
        errors = validate_contract_payload(result)
        self.assertTrue(any("final_quantity" in error for error in errors))

    def test_measure_cli_emits_valid_contract(self):
        payload = {
            "schema": "cad-descriptive-geometry/v7",
            "source_file": "source.dwg",
            "scale_unit_audit": [{"scales": ["1:100"], "units": ["mm"], "spaces": ["paper"], "status": "candidate"}],
            "wall_segments": [{"id": "wall-1", "segment": [0, 0, 100, 0], "status": "candidate"}],
        }
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "source.json"
            out = Path(temp) / "out"
            src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SKILL_DIR / "scripts" / "cad_measure.py"), str(src), "--out-dir", str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads((out / "cad-measurement-candidates.json").read_text(encoding="utf-8"))
            self.assertEqual(validate_contract_payload(result), [])
            self.assertGreaterEqual(result["contract"]["summary"]["total"], 1)
            validate = subprocess.run(
                [sys.executable, str(SKILL_DIR / "scripts" / "cad_validate.py"), str(out / "cad-measurement-candidates.json")],
                capture_output=True, text=True,
            )
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)



    def test_missing_key_field_must_be_review_not_mainline(self):
        # 外部拼好的 contract 把 missing_layer 的候选放进主线 candidates，应被强校验拦下
        payload = {
            "schema": "cad-descriptive-geometry/v7",
            "source_file": "sample.dwg",
            "views": [
                {"id": "v1", "title": "一层平面图", "layer": "TITLE", "bbox": [0, 0, 10, 10], "confidence": 0.95, "status": "candidate"},
                {"id": "v2", "title": "某构件", "layer": "", "bbox": [20, 20, 30, 30], "confidence": 0.95, "status": "candidate", "review_reasons": ["missing_layer"]},
            ],
        }
        result = contractize_payload(payload)
        # 正确路径：missing_layer 自动进 review_candidates
        self.assertEqual(validate_contract_payload(result), [])
        # 人为把该候选挪回主线 candidates，应报错
        review = result["contract"]["review_candidates"]
        target = next(r for r in review if "missing_layer" in r["review_reasons"])
        result["contract"]["candidates"].append(target)
        result["contract"]["review_candidates"] = [r for r in review if r is not target]
        result["contract"]["summary"]["candidate_count"] += 1
        result["contract"]["summary"]["review_required"] -= 1
        errors = validate_contract_payload(result)
        self.assertTrue(any("缺关键字段" in e and "missing_layer" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
