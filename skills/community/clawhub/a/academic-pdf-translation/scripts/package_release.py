"""按允许名单打包发布用的干净 ZIP。

不要压缩整个工作目录。``zip -r`` 会把 `.git`、`.venv`、缓存、本地设置、
审查证据和用户作业一起装进去——用户拿到的包里会有别人的东西。

这里反过来：**只有允许名单里的东西才进包**。以后新增目录默认在包外，
需要它进包时明确加进名单——排除法每加一个目录就得记得改一次，
总有一次会忘。

用法::

    python3 scripts/package_release.py \\
      --version 1.2.0-rc.1 \\
      --output dist/academic-pdf-translation-1.2.0-rc.1.zip
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import json  # noqa: E402
import zipfile  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent

#: 用户运行 Skill 真正需要的文件。目录按整目录收，但仍逐文件过滤后缀。
ALLOWED_FILES = (
    "SKILL.md",
    "README.md",
    "README_EN.md",
    "CHANGELOG.md",
    "LICENSE",
    "TERMS.md",
    "PRIVACY.md",
    "requirements.txt",
    "pyproject.toml",
    ".claude-plugin/plugin.json",
    "Workspace/README.md",
    # check_bundle 要求这两个存在：用户装完后作业目录不会被误提交。
    ".gitignore",
    "Workspace/.gitignore",
)

ALLOWED_DIRS = (
    "scripts",
    "academic_pdf_translation",
    "references",
    "assets",
    "agents",
)

#: 即便在允许目录里，这些也不进包。
SKIP_SUFFIXES = (".pyc", ".pyo", ".log", ".tmp", ".bak")
SKIP_DIR_NAMES = (
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".git",
    ".venv",
    "venv",
    "__MACOSX",
)


def _skip(path: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in path.parts):
        return True
    if path.suffix.casefold() in SKIP_SUFFIXES:
        return True
    return path.name in (".DS_Store", "Thumbs.db", "settings.local.json")


def collect_files(root: Path = REPO_ROOT) -> list[Path]:
    """按允许名单收集要打包的文件，返回仓库相对路径，已排序。"""

    selected: list[Path] = []
    for relative in ALLOWED_FILES:
        path = root / relative
        if path.is_file() and not _skip(path):
            selected.append(Path(relative))
    for directory in ALLOWED_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and not _skip(path):
                selected.append(path.relative_to(root))
    return sorted(set(selected))


def declared_versions(root: Path = REPO_ROOT) -> dict[str, str]:
    """包里各处声明的版本号，用来核对一致性。"""

    versions: dict[str, str] = {}
    manifest = root / ".claude-plugin" / "plugin.json"
    if manifest.is_file():
        versions["plugin.json"] = str(
            json.loads(manifest.read_text(encoding="utf-8")).get("version")
            or ""
        )
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("version"):
                versions["pyproject.toml"] = stripped.split("=", 1)[1].strip(
                    " \"'"
                )
                break
    return versions


def build_archive(
    version: str, output: Path, root: Path = REPO_ROOT
) -> tuple[Path, list[Path]]:
    """写出 ZIP。包内统一放在 ``<name>-<version>/`` 目录下。"""

    files = collect_files(root)
    if not files:
        raise SystemExit("允许名单没有收集到任何文件，拒绝打一个空包")
    prefix = f"academic-pdf-translation-{version}"
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative in files:
            archive.write(root / relative, f"{prefix}/{relative.as_posix()}")
    return output, files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    versions = declared_versions()
    base_version = args.version.split("-", 1)[0]
    mismatched = {
        name: value
        for name, value in versions.items()
        if value != base_version
    }
    if mismatched:
        print(
            "错误: 版本号与包内声明不一致 "
            f"（--version {args.version} 的基线是 {base_version}）: "
            + "、".join(f"{k}={v}" for k, v in mismatched.items())
        )
        return 1

    output, files = build_archive(args.version, args.output)
    print(f"发布包已写入: {output}")
    print(f"文件 {len(files)} 个，压缩后 {output.stat().st_size // 1024} KB")
    print("下一步: python3 scripts/check_release_archive.py " + str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
