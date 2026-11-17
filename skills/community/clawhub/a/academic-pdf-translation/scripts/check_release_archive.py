"""检查发布包：里面该有的都有，不该有的一个都没有。

打包脚本用允许名单，这里做独立复核——两边都错才会漏，
比"打包时顺手看一眼"可靠。

检查项：
- 禁止文件与目录（.git/.venv/缓存/本地设置/审查证据/用户作业）；
- 本机绝对路径（家目录形状的路径，含 Windows 盘符写法）；
- 真实论文与作业语料（受版权保护，不得分发）；
- 版本号一致性；
- 入口文件齐全；
- ZIP 能正常解压；
- 解压后能跑通打包完整性检查。

用法::

    python3 scripts/check_release_archive.py dist/xxx.zip
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import tempfile  # noqa: E402
import zipfile  # noqa: E402

from check_bundle import BundleCheckError, check_bundle  # noqa: E402

#: 包里出现任何一条即失败。
FORBIDDEN_PATTERNS = (
    ".git/",
    ".venv/",
    "venv/",
    "__MACOSX/",
    "__pycache__/",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    "local-dev/",
    "audit/",
    "benchmarks/",
    "tests/",
    "settings.local.json",
    ".DS_Store",
)
FORBIDDEN_SUFFIXES = (".pyc", ".pyo", ".log", ".bak", ".tmp")

#: 用户装完必须能找到的入口。
REQUIRED_ENTRIES = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "requirements.txt",
    ".claude-plugin/plugin.json",
    "scripts/deliver_first_candidate.py",
    "scripts/check_bundle.py",
    "academic_pdf_translation/__init__.py",
)

#: 本机家目录路径的形状。模式按片段拼装，避免脚本自身出现字面路径——
#: check_bundle 会把生产脚本里的字面绝对路径判为硬编码。
_HOME_DIR_NAMES = ("Users", "home")
LOCAL_PATH_RE = re.compile(
    "|".join(
        [
            *(
                f"/{name}/[A-Za-z0-9._-]+/"
                for name in _HOME_DIR_NAMES
            ),
            r"[A-Za-z]:\\Users\\",
        ]
    )
)
#: 受版权保护的语料线索：真实论文文件名与作业目录。
CORPUS_HINTS = ("papers-real", "jobs-real", "arxiv-", "source.pdf")

#: 文本文件才扫路径泄漏；二进制（字体、图片）跳过。
TEXT_SUFFIXES = (
    ".py",
    ".md",
    ".json",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
    ".cfg",
)


#: 缓存目录名与字节码后缀。刚解压的目录里出现它们，就是打包漏了。
CACHE_DIR_NAMES = (
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
)
CACHE_FILE_SUFFIXES = (".pyc", ".pyo")


def _extracted_cache_problems(root: Path) -> list[str]:
    """刚解压的目录里的缓存与字节码。"""

    offenders = sorted(
        str(path.relative_to(root))
        for path in root.rglob("*")
        if (path.is_dir() and path.name in CACHE_DIR_NAMES)
        or (path.is_file() and path.suffix in CACHE_FILE_SUFFIXES)
    )
    return [f"解压后含缓存或字节码文件: {name}" for name in offenders[:20]]


def check_archive(archive_path: Path) -> list[str]:
    problems: list[str] = []
    if not archive_path.is_file():
        return [f"发布包不存在: {archive_path}"]
    if not zipfile.is_zipfile(archive_path):
        return [f"不是有效的 ZIP: {archive_path}"]

    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        if bad is not None:
            problems.append(f"ZIP 损坏，无法解压: {bad}")
        names = archive.namelist()
        roots = {name.split("/", 1)[0] for name in names}
        if len(roots) != 1:
            problems.append(
                f"包内应当只有一个顶层目录，实际有 {sorted(roots)}"
            )
        prefix = f"{sorted(roots)[0]}/" if roots else ""
        inner = [
            name[len(prefix):]
            for name in names
            if name.startswith(prefix) and name != prefix
        ]

        for name in inner:
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in name or name.endswith(pattern.rstrip("/")):
                    problems.append(f"禁止内容进入发布包: {name}")
            if name.casefold().endswith(FORBIDDEN_SUFFIXES):
                problems.append(f"禁止后缀进入发布包: {name}")
            if any(hint in name for hint in CORPUS_HINTS):
                problems.append(f"受版权保护的语料进入发布包: {name}")

        for entry in REQUIRED_ENTRIES:
            if entry not in inner:
                problems.append(f"缺少入口文件: {entry}")

        for name in inner:
            if not name.casefold().endswith(TEXT_SUFFIXES):
                continue
            try:
                text = archive.read(prefix + name).decode("utf-8")
            except (KeyError, UnicodeDecodeError):
                continue
            match = LOCAL_PATH_RE.search(text)
            if match:
                problems.append(
                    f"{name} 里有本机绝对路径: {match.group(0)}"
                )

        # 版本一致性：清单、pyproject 与包名三者必须对齐。
        try:
            manifest = json.loads(
                archive.read(prefix + ".claude-plugin/plugin.json").decode(
                    "utf-8"
                )
            )
        except (KeyError, ValueError):
            manifest = {}
        declared = str(manifest.get("version") or "")
        # 目录名形如 academic-pdf-translation-1.2.0-rc.1：
        # 版本本身含连字符，只能按已知前缀剥，不能按最后一个连字符切。
        archive_version = prefix.rstrip("/").removeprefix(
            "academic-pdf-translation-"
        )
        base = archive_version.split("-", 1)[0]
        if declared and not archive_version.startswith(declared):
            problems.append(
                f"包名版本 {archive_version} 与清单版本 {declared} 不一致"
            )
        try:
            pyproject = archive.read(prefix + "pyproject.toml").decode("utf-8")
            for line in pyproject.splitlines():
                if line.strip().startswith("version"):
                    value = line.split("=", 1)[1].strip(" \"'")
                    if value != base:
                        problems.append(
                            f"pyproject 版本 {value} 与包版本基线 {base} 不一致"
                        )
                    break
        except (KeyError, UnicodeDecodeError):
            problems.append("包里缺少 pyproject.toml")

    # 解压后用当前仓库里的可信检查器读取发布包，不执行发布包中的代码。
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(target)
        roots = [path for path in target.iterdir() if path.is_dir()]
        if not roots:
            problems.append("解压后没有内容")
        else:
            # 刚解压、还没人跑过任何脚本：此时出现的缓存只可能来自打包。
            problems.extend(_extracted_cache_problems(roots[0]))
            try:
                check_bundle(roots[0])
            except (BundleCheckError, OSError, ValueError) as exc:
                problems.append(f"解压后 check_bundle 失败: {str(exc)[-400:]}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    problems = check_archive(args.archive)
    if problems:
        print(f"发布包检查未通过，{len(problems)} 条问题:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"发布包检查通过: {args.archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
