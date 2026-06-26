import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_plan_accepts_source_file_with_spaces_and_crlf(tmp_path: Path) -> None:
    source = tmp_path / "input with spaces.txt"
    source.write_text("第一行需求\r\n第二行需求\r\n", encoding="utf-8", newline="")
    blueprint = tmp_path / "solution.blueprint.json"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "business_blueprint.cli",
            "--plan",
            str(blueprint),
            "--from",
            str(source),
            "--industry",
            "common",
        ],
        cwd=ROOT,
        check=True,
    )

    payload = json.loads(blueprint.read_text(encoding="utf-8"))
    assert payload["context"]["sourceRefs"][0]["excerpt"] == "第一行需求\r\n第二行需求\r\n"


def test_plan_treats_windows_style_missing_path_as_inline_text(tmp_path: Path) -> None:
    blueprint = tmp_path / "solution.blueprint.json"
    inline_text = r"C:\Users\song\需求说明.txt"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "business_blueprint.cli",
            "--plan",
            str(blueprint),
            "--from",
            inline_text,
            "--industry",
            "common",
        ],
        cwd=ROOT,
        check=True,
    )

    payload = json.loads(blueprint.read_text(encoding="utf-8"))
    assert payload["context"]["sourceRefs"][0]["excerpt"] == inline_text


def test_validate_writes_json_to_stdout_without_stderr(tmp_path: Path) -> None:
    blueprint = tmp_path / "solution.blueprint.json"
    blueprint.write_text(
        json.dumps(
            {
                "version": "1.0",
                "meta": {"title": "Test", "industry": "common"},
                "context": {
                    "goals": [],
                    "scope": [],
                    "assumptions": [],
                    "constraints": [],
                    "sourceRefs": [],
                    "clarifyRequests": [],
                    "clarifications": [],
                },
                "library": {
                    "capabilities": [],
                    "actors": [],
                    "flowSteps": [],
                    "systems": [],
                },
                "relations": [],
                "views": [],
                "editor": {"fieldLocks": {}, "theme": "enterprise-default"},
                "artifacts": {},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "business_blueprint.cli", "--validate", str(blueprint)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert "summary" in payload
    assert result.stderr == ""
