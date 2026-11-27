#!/usr/bin/env python3
"""把 Skill 打包为可导入 ZIP，确保 SKILL.md 位于压缩包根目录。"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {"__pycache__", ".git", ".DS_Store"}
SLIM_EXCLUDED_PREFIXES = {
    ("scripts", "tests"),
}
SLIM_EXCLUDED_FILES = {
    ("references", "同类技能工程参考.md"),
    ("scripts", "package_desktop_agents.py"),
    ("scripts", "package_skill.py"),
    ("scripts", "test_skill.py"),
}
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory", type=Path)
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("--force", action="store_true", help="覆盖已存在的目标ZIP")
    parser.add_argument("--enforce-versioned-name", action="store_true", help="要求ZIP文件名包含清单中的vX.Y.Z")
    parser.add_argument(
        "--profile",
        choices=("full", "slim-production"),
        default="full",
        help="full 保留研发资料；slim-production 排除打包工具、工程参考、全量自测试与夹具",
    )
    return parser.parse_args()


def should_include(path: Path, root: Path, profile: str = "full") -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.suffix.lower() == ".pyc":
        return False
    if profile == "slim-production":
        parts = relative.parts
        if parts in SLIM_EXCLUDED_FILES:
            return False
        if any(parts[: len(prefix)] == prefix for prefix in SLIM_EXCLUDED_PREFIXES):
            return False
    return True


def load_version(root: Path) -> str:
    version_path = root / "assets" / "skill-version.json"
    if not version_path.is_file():
        raise FileNotFoundError(f"version manifest not found: {version_path}")
    value = json.loads(version_path.read_text(encoding="utf-8-sig"))
    version = str(value.get("version", "")) if isinstance(value, dict) else ""
    if not SEMVER_PATTERN.fullmatch(version):
        raise ValueError(f"invalid semantic version: {version!r}")
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8-sig")
    agent_text = (root / "agents" / "openai.yaml").read_text(encoding="utf-8-sig")
    release_example = json.loads((root / "assets" / "发布清单示例.json").read_text(encoding="utf-8-sig"))
    if f"当前版本 {version}" not in skill_text or f"v{version}" not in skill_text:
        raise ValueError("SKILL.md version is inconsistent with skill-version.json")
    if f"v{version}" not in agent_text:
        raise ValueError("agents/openai.yaml version is inconsistent with skill-version.json")
    if str(release_example.get("skill_version")) != version:
        raise ValueError("release manifest example version is inconsistent with skill-version.json")
    return version


def package(skill_directory: Path, output_zip: Path, force: bool = False,
            enforce_versioned_name: bool = False,
            profile: str = "full") -> tuple[int, int, str]:
    root = skill_directory.resolve()
    output = output_zip.resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    if not (root / "SKILL.md").is_file():
        raise FileNotFoundError(f"SKILL.md not found: {root}")
    version = load_version(root)
    if enforce_versioned_name and f"v{version}" not in output.name:
        raise ValueError(f"output ZIP name must contain v{version}: {output.name}")
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing package: {output}")
    if root == output.parent or root in output.parents:
        raise ValueError("output ZIP must be outside the skill directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and should_include(path, root, profile)
    )
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())

    with zipfile.ZipFile(output, "r") as archive:
        names = archive.namelist()
        if "SKILL.md" not in names:
            raise RuntimeError("package validation failed: SKILL.md is not at ZIP root")
        if "assets/skill-version.json" not in names:
            raise RuntimeError("package validation failed: version manifest missing")
        if "scripts/smoke_test_skill.py" not in names:
            raise RuntimeError("package validation failed: smoke test missing")
        if profile == "slim-production":
            forbidden = {
                "references/同类技能工程参考.md",
                "scripts/package_desktop_agents.py",
                "scripts/package_skill.py",
                "scripts/test_skill.py",
            }
            if forbidden.intersection(names) or any(name.startswith("scripts/tests/") for name in names):
                raise RuntimeError("package validation failed: development tests leaked into slim package")
        if any(name.startswith(root.name + "/") for name in names):
            raise RuntimeError("package validation failed: unexpected outer skill directory")
        archive.testzip()
    return len(files), output.stat().st_size, version


def main() -> int:
    args = parse_args()
    try:
        count, size, version = package(
            args.skill_directory,
            args.output_zip,
            force=args.force,
            enforce_versioned_name=args.enforce_versioned_name,
            profile=args.profile,
        )
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    print(f"OK: {args.output_zip.resolve()}")
    print(f"FILES: {count}")
    print(f"SIZE: {size}")
    print(f"VERSION: {version}")
    print(f"PROFILE: {args.profile}")
    print("ROOT_ENTRY: SKILL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
