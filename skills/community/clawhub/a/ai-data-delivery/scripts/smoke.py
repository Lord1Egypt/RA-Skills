#!/usr/bin/env python3
"""Check the local installation by importing the bundled example and reading its package."""
import argparse
from importlib.util import find_spec
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


def run_cli(script, arguments, directory):
    command = [sys.executable, "-B", "-X", "utf8", str(ROOT / "scripts" / script), *arguments]
    process = subprocess.run(command, cwd=directory, capture_output=True, encoding="utf-8", timeout=60)
    if process.returncode:
        raise ValueError((process.stdout or process.stderr).strip() or f"{script} exited {process.returncode}")
    return json.loads(process.stdout)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    missing = [name for module, name in (("yaml", "PyYAML"), ("pypdf", "pypdf")) if find_spec(module) is None]
    if missing:
        print(json.dumps({
            "status": "missing_dependencies", "missing": missing,
            "hint": "From the skill directory run: python -m pip install -r requirements.txt / 请在 Skill 目录执行此命令",
            "install_argv": [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
        }, ensure_ascii=False))
        return 2

    stage = "temporary_directory"
    try:
        with TemporaryDirectory(prefix="ai-data-delivery-") as directory:
            project = ["--project", "model"]
            sample = ROOT / "examples" / "semantic-workbench" / "transport.sql"
            stage = "import"
            imported = run_cli("knowledge.py", [*project, "import", "--file", str(sample), "--seed-draft"], directory)
            counts = imported["result"]["result"]["seeded"]["counts"]
            if counts != {"dataset": 2, "field": 5, "relation": 1}:
                raise ValueError(f"Unexpected example counts: {counts}")

            stage = "export"
            run_cli("knowledge.py", [*project, "export", "--out", "model.zip", "--draft"], directory)
            stage = "verify"
            verified = run_cli("semantic_read.py", ["--package", "model.zip", "verify"], directory)
            if (verified["status"], verified["draft"], verified["asset_count"], verified["complete"]) != (
                "verified", True, 8, False
            ):
                raise ValueError("Expected a verified draft package with eight assets")
            stage = "cleanup"
    except (KeyError, TypeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "error", "stage": stage, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps({"status": "ok", "counts": counts, "verify": verified["status"], "draft": verified["draft"],
                      "asset_count": verified["asset_count"], "complete": verified["complete"]}))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
