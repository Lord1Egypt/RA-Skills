#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline test for parameter sweep batch simulation.

Runs run_parameter_sweep.py with a **mock COMSOL backend** to validate:
  - Parameter combination generation (Cartesian product)
  - Case directory structure
  - Resume / checkpoint logic (.done skip)
  - Summary CSV + JSON aggregation
  - Error handling and retry reporting

No COMSOL installation required. All "simulations" are instant mock outputs.

Usage:
    python test_sweep_offline.py

Exit code: 0 = all tests passed, 1 = any test failed.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).resolve().parents[1]  # scripts/ -> comsol-opto-simulation/
SWEEP_SCRIPT = SKILL_DIR / "scripts" / "run_parameter_sweep.py"
TEST_DIR = SKILL_DIR / "tmp_test_sweep"


def parse_last_json_object(text: str) -> dict:
    """Parse the final JSON object from stdout that may contain progress logs first."""
    decoder = json.JSONDecoder()
    stripped = text.strip()
    for idx, char in enumerate(stripped):
        if char != "{":
            continue
        try:
            obj, end = decoder.raw_decode(stripped[idx:])
        except json.JSONDecodeError:
            continue
        if stripped[idx + end:].strip() == "":
            return obj
    return {}


def write_mock_sim_script(mock_script_path: Path) -> None:
    """Create a fake COMSOL simulation script that instantly produces output."""
    mock_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock COMSOL simulation for offline testing."""

import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    output_dir = Path(config.get("output_dir", "output/mock"))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Simulate model save
    model_path = output_dir / "mock_result.mph"
    model_path.write_text("FAKE_MPH", encoding="utf-8")

    # Simulate metrics extraction
    metrics_dir = output_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metrics = {
        "mock_eqe": 0.85,
        "mock_responsivity": 0.42,
        "mock_open_circuit_voltage": 0.0,
        "mock_jsc": 15.3,
    }
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f)

    result = {
        "status": "ok",
        "output_dir": str(output_dir),
        "model_saved": str(model_path),
        "mock": True,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
'''
    mock_script_path.write_text(mock_code, encoding="utf-8")


def write_mock_sim_script_fail(mock_script_path: Path, fail_case_id: int) -> None:
    """Create a mock script that fails only for a specific case index."""
    mock_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock COMSOL simulation with selective failure."""

import argparse
import json
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    output_dir = Path(config.get("output_dir", "output/mock"))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine case id from output_dir name (case_NNNN)
    case_name = output_dir.name
    fail = (case_name == "case_{fail_case_id:04d}")

    if fail:
        print(json.dumps({{"status": "error", "message": "Mock failure for testing"}}, indent=2))
        sys.exit(1)

    model_path = output_dir / "mock_result.mph"
    model_path.write_text("FAKE_MPH", encoding="utf-8")
    metrics = {{"mock_eqe": 0.85, "mock_responsivity": 0.42}}
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f)

    print(json.dumps({{
        "status": "ok",
        "output_dir": str(output_dir),
        "model_saved": str(model_path),
        "mock": True,
    }}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
'''
    mock_script_path.write_text(mock_code, encoding="utf-8")


def build_sweep_config(base_config: dict, sweep_params: list[dict], output_dir: str, mock_script: str) -> dict:
    """Build a sweep config that uses the mock simulation script."""
    return {
        "simulation_type": "mock",
        "base_config": base_config,
        "sweep_parameters": sweep_params,
        "parallel": False,
        "max_workers": 1,
        "output_dir": output_dir,
        "resume": True,
        "extract_metrics": True,
        "generate_summary_plots": False,
        "verbose": False,
        "_mock_script": str(mock_script),  # internal hint for test harness
    }


def run_sweep_test(sweep_config: dict, env_overrides: dict | None = None) -> tuple[int, dict, Path]:
    """Run parameter sweep with given config. Returns (exit_code, parsed_stdout, output_dir)."""
    # Write sweep config to temp file
    cfg_path = TEST_DIR / "test_sweep_config.json"
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(sweep_config, f, indent=2, ensure_ascii=False)

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    env.setdefault("PYTHONIOENCODING", "utf-8")

    cmd = [sys.executable, str(SWEEP_SCRIPT), "--config", str(cfg_path)]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(SKILL_DIR),
        env=env,
    )

    result = parse_last_json_object(proc.stdout)
    if not result:
        result = {
            "raw": proc.stdout.strip()[-500:],
            "stderr": proc.stderr.strip()[-500:],
            "returncode": proc.returncode,
        }

    output_dir = Path(sweep_config["output_dir"])
    return proc.returncode, result, output_dir


def test_combination_generation() -> bool:
    """Test A: Verify Cartesian product generates correct number of cases."""
    print("\n[Test A] Parameter combination generation")

    mock_script = TEST_DIR / "mock_sim.py"
    write_mock_sim_script(mock_script)

    sweep_cfg = build_sweep_config(
        base_config={"dummy": "value"},
        sweep_params=[
            {"name": "param1", "mode": "lin", "start": 1, "stop": 3, "points": 3},
            {"name": "param2", "mode": "lin", "start": 10, "stop": 20, "points": 3},
        ],
        output_dir=str(TEST_DIR / "test_a_output"),
        mock_script=str(mock_script),
    )

    # Override: make run_parameter_sweep.py use our mock script instead of real COMSOL scripts
    # We do this by monkey-patching the script path via env var
    rc, result, out_dir = run_sweep_test(sweep_cfg, {"MOCK_SIM_SCRIPT": str(mock_script)})

    expected_cases = 3 * 3  # 9
    actual_cases = len(list(out_dir.glob("case_*")))

    ok = actual_cases == expected_cases
    print(f"  Expected cases: {expected_cases}, Actual: {actual_cases} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(f"  Stderr: {result.get('raw', '')}")
    return ok


def test_checkpoint_resume() -> bool:
    """Test B: Verify .done marker causes skip on re-run."""
    print("\n[Test B] Checkpoint / resume logic")

    mock_script = TEST_DIR / "mock_sim.py"
    write_mock_sim_script(mock_script)

    out_dir = TEST_DIR / "test_b_output"
    sweep_cfg = build_sweep_config(
        base_config={"dummy": "value"},
        sweep_params=[
            {"name": "x", "mode": "lin", "start": 0, "stop": 2, "points": 3},
        ],
        output_dir=str(out_dir),
        mock_script=str(mock_script),
    )

    # First run
    rc1, res1, _ = run_sweep_test(sweep_cfg, {"MOCK_SIM_SCRIPT": str(mock_script)})

    # Create .done in all case dirs to simulate completed state
    for case_dir in out_dir.glob("case_*"):
        (case_dir / ".done").write_text("mock", encoding="utf-8")

    # Second run (should skip all)
    rc2, res2, _ = run_sweep_test(sweep_cfg, {"MOCK_SIM_SCRIPT": str(mock_script)})

    skipped = res2.get("skipped", 0)
    expected_skipped = 3
    ok = skipped == expected_skipped
    print(f"  Expected skipped: {expected_skipped}, Actual: {skipped} -> {'PASS' if ok else 'FAIL'}")
    return ok


def test_summary_aggregation() -> bool:
    """Test C: Verify summary.csv and summary.json contain all cases."""
    print("\n[Test C] Summary aggregation (CSV + JSON)")

    mock_script = TEST_DIR / "mock_sim.py"
    write_mock_sim_script(mock_script)

    out_dir = TEST_DIR / "test_c_output"
    sweep_cfg = build_sweep_config(
        base_config={"dummy": "value"},
        sweep_params=[
            {"name": "thickness", "mode": "lin", "start": 50, "stop": 150, "points": 3},
        ],
        output_dir=str(out_dir),
        mock_script=str(mock_script),
    )

    rc, res, _ = run_sweep_test(sweep_cfg, {"MOCK_SIM_SCRIPT": str(mock_script)})

    csv_path = out_dir / "summary.csv"
    json_path = out_dir / "summary.json"

    csv_ok = csv_path.exists()
    json_ok = json_path.exists()

    row_count = 0
    if csv_ok:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            row_count = len(rows) - 1  # minus header

    json_count = 0
    if json_ok:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            json_count = len(data)

    expected = 3
    ok = csv_ok and json_ok and row_count == expected and json_count == expected
    print(f"  CSV rows: {row_count}, JSON entries: {json_count}, Expected: {expected} -> {'PASS' if ok else 'FAIL'}")
    return ok


def test_error_handling() -> bool:
    """Test D: Verify failed cases are recorded correctly in summary."""
    print("\n[Test D] Error handling and reporting")

    mock_script = TEST_DIR / "mock_sim_fail.py"
    write_mock_sim_script_fail(mock_script, fail_case_id=1)

    out_dir = TEST_DIR / "test_d_output"
    sweep_cfg = build_sweep_config(
        base_config={"dummy": "value"},
        sweep_params=[
            {"name": "x", "mode": "lin", "start": 0, "stop": 2, "points": 3},
        ],
        output_dir=str(out_dir),
        mock_script=str(mock_script),
    )

    rc, res, _ = run_sweep_test(sweep_cfg, {"MOCK_SIM_SCRIPT": str(mock_script)})

    expected_ok = 2
    expected_err = 1
    actual_ok = res.get("ok", 0)
    actual_err = res.get("error", 0)

    ok = actual_ok == expected_ok and actual_err == expected_err
    print(f"  Expected OK={expected_ok}, Error={expected_err} | Actual OK={actual_ok}, Error={actual_err} -> {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    print("=" * 60)
    print("Offline Parameter Sweep Test Suite")
    print("=" * 60)

    # Clean test workspace
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    results = {
        "A_combination": test_combination_generation(),
        "B_checkpoint": test_checkpoint_resume(),
        "C_summary": test_summary_aggregation(),
        "D_errors": test_error_handling(),
    }

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    all_pass = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {name:20s} -> {status}")
        if not passed:
            all_pass = False

    print("=" * 60)
    print(f"Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    # Cleanup on success
    if all_pass and TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
        print("(test artifacts cleaned up)")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())

