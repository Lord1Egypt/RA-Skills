"""Tests for build123d CAD scripts.

Run: .venv/bin/python -m pytest tests/ -v
"""

import subprocess
import json
import os
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent / "scripts"
PYTHON = Path(__file__).parent.parent / ".venv" / "bin" / "python"
if not PYTHON.exists():
    import sys
    PYTHON = Path(sys.executable)


def run_script(name: str, args: list[str]) -> dict:
    r = subprocess.run(
        [str(PYTHON), str(SCRIPTS / name)] + args,
        capture_output=True, text=True, timeout=60,
        cwd=str(SCRIPTS),
    )
    return json.loads(r.stdout)


def test_generate_step():
    out = run_script("cad_generate.py", [
        "--script", "from build123d import *\nwith BuildPart() as result:\n    Box(10, 20, 30)",
        "--format", "step",
    ])
    assert out["success"]
    assert Path(out["artifact_path"]).exists()
    assert out["bounding_box_mm"]["z"] == pytest.approx(30.0, abs=0.5)


def test_generate_stl():
    out = run_script("cad_generate.py", [
        "--script", "from build123d import *\nwith BuildPart() as result:\n    Cylinder(5, 10)",
        "--format", "stl",
    ])
    assert out["success"]
    assert out["format"] == "stl"


def test_measure_box():
    out = run_script("cad_measure.py", [
        "--script", "from build123d import *\nwith BuildPart() as result:\n    Box(10, 20, 30)",
    ])
    assert out["success"]
    assert out["volume_mm3"] == pytest.approx(6000.0, abs=1.0)
    assert out["face_count"] == 6


def test_section():
    out = run_script("cad_section.py", [
        "--script", "from build123d import *\nwith BuildPart() as result:\n    Box(10, 10, 10)",
        "--plane", "XY", "--offset", "5.0",
    ])
    assert out["success"]
    assert Path(out["artifact_path"]).suffix == ".svg"


def test_api():
    out = run_script("cad_api.py", [])
    assert "primitives_3d" in out
    assert "pattern" in out


def test_bad_script():
    out = run_script("cad_generate.py", [
        "--script", "raise ValueError('boom')",
        "--format", "step",
    ])
    assert not out["success"]
    assert "boom" in out["error"]


# --- cad_validate tests ---

ASSEMBLY_NO_INTERFERENCE = """from build123d import *
with BuildPart() as box_a:
    Box(10, 10, 10)
with BuildPart() as box_b:
    with Locations((50, 0, 0)):
        Box(10, 10, 10)
parts = {"box_a": box_a.part, "box_b": box_b.part}
"""

ASSEMBLY_WITH_INTERFERENCE = """from build123d import *
with BuildPart() as box_a:
    Box(10, 10, 10)
with BuildPart() as box_b:
    with Locations((5, 0, 0)):
        Box(10, 10, 10)
parts = {"box_a": box_a.part, "box_b": box_b.part}
"""

ASSEMBLY_TIGHT_CLEARANCE = """from build123d import *
with BuildPart() as box_a:
    Box(10, 10, 10)
with BuildPart() as box_b:
    with Locations((10.5, 0, 0)):
        Box(10, 10, 10)
parts = {"box_a": box_a.part, "box_b": box_b.part}
"""


def test_validate_pass():
    out = run_script("cad_validate.py", [
        "--script", ASSEMBLY_NO_INTERFERENCE,
        "--mode", "static",
    ])
    assert out["success"]
    assert out["verdict"] == "PASS"
    assert out["static_interference"]["interferences_found"] == 0


def test_validate_fail_interference():
    out = run_script("cad_validate.py", [
        "--script", ASSEMBLY_WITH_INTERFERENCE,
        "--mode", "static",
    ])
    assert out["success"]
    assert out["verdict"] == "FAIL"
    assert out["static_interference"]["interferences_found"] > 0


def test_validate_clearance_warn():
    out = run_script("cad_validate.py", [
        "--script", ASSEMBLY_TIGHT_CLEARANCE,
        "--mode", "clearance",
        "--min-clearance", "2.0",
    ])
    assert out["success"]
    assert out["verdict"] in ("WARN", "PASS")  # 0.5mm gap < 2.0mm threshold


# --- sandbox security tests ---

def test_sandbox_blocks_subprocess():
    out = run_script("cad_generate.py", [
        "--script", "import subprocess\nsubprocess.run(['ls'])",
        "--format", "step",
    ])
    assert not out["success"]
    assert "Blocked" in out["error"]


def test_sandbox_blocks_os_system():
    out = run_script("cad_generate.py", [
        "--script", "import os\nos.system('whoami')",
        "--format", "step",
    ])
    assert not out["success"]
    assert "Blocked" in out["error"]


def test_sandbox_blocks_open():
    out = run_script("cad_generate.py", [
        "--script", "open('/etc/passwd')",
        "--format", "step",
    ])
    assert not out["success"]
    assert "Blocked" in out["error"]


def test_sandbox_blocks_requests():
    out = run_script("cad_generate.py", [
        "--script", "import requests\nrequests.get('http://evil.com')",
        "--format", "step",
    ])
    assert not out["success"]
    assert "Blocked" in out["error"]


def test_sandbox_blocks_disallowed_import():
    out = run_script("cad_generate.py", [
        "--script", "import socket\nsocket.socket()",
        "--format", "step",
    ])
    assert not out["success"]
    assert "Blocked" in out["error"]


def test_sandbox_allows_math():
    out = run_script("cad_generate.py", [
        "--script", "import math\nfrom build123d import *\nwith BuildPart() as result:\n    Cylinder(math.sqrt(25), 10)",
        "--format", "step",
    ])
    assert out["success"]
