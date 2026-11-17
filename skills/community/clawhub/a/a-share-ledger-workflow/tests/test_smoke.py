import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script: str, data_dir: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["STOCK_DATA_DIR"] = str(data_dir)
    env.pop("HERMES_HOME", None)
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )


def test_sample_ledgers_validate(tmp_path):
    data_dir = tmp_path / "sample"
    shutil.copytree(ROOT / "examples/sample_direction", data_dir)

    result = run("validate_ledgers.py", data_dir)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "全部台账通过" in result.stdout


def test_dictionary_self_check_detects_corruption(tmp_path):
    data_dir = tmp_path / "sample"
    shutil.copytree(ROOT / "examples/sample_direction", data_dir)

    result = run("selftest_dict_check.py", data_dir)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "通过" in result.stdout


def test_init_is_idempotent_and_preserves_user_file(tmp_path):
    data_dir = tmp_path / "stock-data"
    env = os.environ.copy()
    env["STOCK_DATA_DIR"] = str(data_dir)
    script = ROOT / "init.sh"

    for _ in range(2):
        result = subprocess.run(
            ["bash", str(script)], cwd=ROOT, env=env, capture_output=True,
            text=True, encoding="utf-8", timeout=30,
        )
        assert result.returncode == 0, result.stdout + result.stderr

    bench = data_dir / "bench.json"
    bench.write_text("user data", encoding="utf-8")
    result = subprocess.run(
        ["bash", str(script)], cwd=ROOT, env=env, capture_output=True,
        text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert bench.read_text(encoding="utf-8") == "user data"


def test_demo_script_runs():
    result = subprocess.run(
        ["bash", str(ROOT / "demo.sh")], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", timeout=180,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "示例跑通" in result.stdout
