"""字体准备：在生成 PDF 之前把目标语言字体解析成具体文件。

字体解析原来住在 `build_candidate` 里，只有真正开始排版时才会执行。
但输入就绪检查跑在排版之前，全新作业的 `selected_fonts` 是空的，于是
每一次都被 `SELECTED_FONTS_MISSING` 拦下，自动解析永远没机会运行。

现在解析是独立一步：初始化时做一次，统一入口在检查之前再确认一次。
真正的发现、探测与角色选择在 `academic_pdf_translation.contracts.fonts`，
这里只负责和作业数据打交道。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from academic_pdf_translation.contracts.fonts import (
    ROLE_BOLD,
    ROLE_REFERENCE,
    ROLE_REGULAR,
    FontResolution,
    reference_weight_ok,
    resolve_fonts,
)

from _common import (  # noqa: E402
    SkillError,
    load_json,
    resolve_language_profile,
    sha256_file,
    write_json,
)

#: 目标语言字体候选之外的兜底家族，按偏好顺序。
FALLBACK_FONT_NAMES = (
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "PingFang SC",
    "Hiragino Sans GB",
    "Microsoft YaHei",
    "STHeiti",
    "Arial Unicode",
    "DejaVu Sans",
)


def _job_sample_characters(job_dir: Path) -> str:
    """从作业里取一小撮真实字符，用来验证字体真的画得出来。

    只读已经在磁盘上的 source_units.json，不重新扫描原文。
    """

    path = Path(job_dir) / "source_units.json"
    if not path.is_file():
        return ""
    try:
        data = load_json(path)
    except SkillError:
        return ""
    seen: set[str] = set()
    for unit in data.get("units", [])[:400]:
        for character in str(unit.get("source") or ""):
            if not character.isspace():
                seen.add(character)
        if len(seen) > 600:
            break
    return "".join(sorted(seen))


def _job_math_characters(job_dir: Path) -> str:
    """译文里既非 ASCII 也非 CJK 的字符——∈、Ω、私用区这类符号。

    核心中文与数学符号分开检查：正文字体只需覆盖核心中文，符号字符
    由数学后备角色兜底，谁也不必假装一把字体什么都能画。
    """

    path = Path(job_dir) / "translation.json"
    if not path.is_file():
        return ""
    try:
        data = load_json(path)
    except SkillError:
        return ""
    seen: set[str] = set()
    for unit in data.get("units", []):
        if not isinstance(unit, dict):
            continue
        text = str(unit.get("translation") or "") or str(
            unit.get("source") or ""
        )
        for character in text:
            code = ord(character)
            if code < 0x2000 or character.isspace():
                continue
            if 0x3400 <= code <= 0x9FFF or 0x3000 <= code <= 0x303F:
                continue
            if 0xFF00 <= code <= 0xFFEF:
                continue
            seen.add(character)
        if len(seen) > 120:
            break
    return "".join(sorted(seen))


def _language_sample(job: dict[str, Any]) -> str:
    """目标语言的代表字符；字体必须画得出来才算可用。"""

    target = str(job.get("translation", {}).get("target_language") or "")
    _, profile = resolve_language_profile(target) if target else ("", {})
    writing_system = str(profile.get("writing_system") or "latin")
    if writing_system == "han":
        return "中文样本一二三时间方法结果"
    if writing_system == "japanese":
        return "日本語見本一二三方法結果ひらがなカタカナ"
    if writing_system == "hangul":
        return "한국어 표본 방법 결과"
    return "Latin sample ABCabc123"


def resolve_job_fonts(job: dict[str, Any], job_dir: Path | None = None) -> FontResolution:
    """按作业的字体候选解析正文、粗体和题录三个角色。"""

    quality = job.get("quality", {})
    requested = [
        str(value)
        for value in quality.get("font_candidates", [])
        if isinstance(value, str) and value.strip()
    ]
    explicit = [
        str(value)
        for value in quality.get("selected_fonts", [])
        if isinstance(value, str) and value.strip()
    ]
    reference_characters = (
        _job_sample_characters(job_dir) if job_dir is not None else ""
    )
    resolution = resolve_fonts(
        requested,
        required_characters=_language_sample(job),
        fallback_names=[*FALLBACK_FONT_NAMES, *explicit],
        reference_characters=reference_characters,
        math_characters=(
            _job_math_characters(job_dir) if job_dir is not None else ""
        ),
    )
    if ROLE_REGULAR not in resolution.selections:
        raise SkillError(
            "无法解析目标语言字体。请在 job.json.quality.font_candidates 中"
            "写入本机可用的字体家族名，或安装一种可嵌入的目标语言字体。"
            + (
                "\n被拒绝的候选: "
                + "; ".join(
                    f"{Path(probe.path).name}: {probe.reason}"
                    for probe in resolution.rejected[:5]
                )
                if resolution.rejected
                else ""
            )
        )
    return resolution


def _resolve_fonts(job: dict[str, Any]) -> tuple[Path, Path]:
    """兼容入口：返回 (正文字体, 粗体)。"""

    resolution = resolve_job_fonts(job)
    return (
        Path(resolution.selections[ROLE_REGULAR].path),
        Path(resolution.selections[ROLE_BOLD].path),
    )


def _resolve_reference_font(regular_font: Path) -> Path:
    """兼容入口：题录体。找不到合适的拉丁字体时回落到正文字体。"""

    resolution = resolve_fonts(
        [],
        fallback_names=[str(regular_font)],
        reference_characters="",
    )
    selection = resolution.selections.get(ROLE_REFERENCE)
    return Path(selection.path) if selection else regular_font


def font_evidence(paths: list[Path]) -> list[dict[str, str]]:
    return [
        {"path": str(path), "sha256": sha256_file(path, use_cache=False)}
        for path in paths
    ]


def fonts_are_current(job: dict[str, Any]) -> bool:
    """已冻结的字体是否仍然可用：文件在，且内容哈希没变。"""

    quality = job.get("quality", {})
    selected = quality.get("selected_fonts")
    evidence = quality.get("selected_font_evidence")
    if not isinstance(selected, list) or not selected:
        return False
    if not isinstance(evidence, list) or len(evidence) != len(selected):
        return False
    for value, record in zip(selected, evidence, strict=True):
        if not isinstance(value, str) or not isinstance(record, dict):
            return False
        path = Path(value).expanduser()
        if not path.is_file():
            return False
        if str(record.get("path") or "") != str(value):
            return False
        if record.get("sha256") != sha256_file(path, use_cache=False):
            return False
    return True


def prepare_job_fonts(
    job_dir: Path,
    *,
    force: bool = False,
) -> dict[str, Any]:
    """解析并冻结字体，把绝对路径、角色和文件哈希写回 job.json。

    已经冻结且仍然有效时不重复解析；文件变了就重新选。
    """

    job_dir = Path(job_dir).resolve()
    job_path = job_dir / "job.json"
    job = load_json(job_path)
    # 冻结的题录体若违反字重闸门（例如旧作业冻住了 Arial Black），
    # 冻结作废，强制重选。旧证据在返回里标记失效原因。
    stale_reference = None
    stale_missing: list[str] = []
    frozen = (job.get("quality") or {}).get("selected_fonts")
    if isinstance(frozen, list) and frozen:
        # 换机器后旧的绝对字体路径可能不存在（Mac 冻结、Linux 运行）。
        # 找不到就作废重选，先把失效记下来再动手。
        stale_missing = [
            str(value)
            for value in frozen
            if isinstance(value, str) and not Path(value).expanduser().is_file()
        ]
        if stale_missing:
            force = True
    if isinstance(frozen, list) and len(frozen) >= 3:
        reference_path = Path(str(frozen[2]))
        if not reference_weight_ok(reference_path):
            stale_reference = str(reference_path)
            force = True
    if not force and fonts_are_current(job):
        quality = job["quality"]
        return {
            "status": "unchanged",
            "selected_fonts": list(quality["selected_fonts"]),
            "selected_font_evidence": list(quality["selected_font_evidence"]),
            "warnings": list(quality.get("font_warnings", [])),
        }

    resolution = resolve_job_fonts(job, job_dir)
    quality = job.setdefault("quality", {})
    previous = quality.get("selected_fonts")
    quality["selected_fonts"] = resolution.paths
    quality["selected_font_evidence"] = resolution.evidence()
    quality["font_warnings"] = list(resolution.warnings)
    quality["font_rejected_candidates"] = [
        probe.as_dict() for probe in resolution.rejected[:20]
    ]
    write_json(job_path, job)
    report = {
        "status": "reselected" if previous else "selected",
        "selected_fonts": resolution.paths,
        "selected_font_evidence": resolution.evidence(),
        "warnings": list(resolution.warnings),
    }
    if stale_reference:
        report["stale_evidence"] = (
            f"冻结题录体 {stale_reference} 是粗体家族，违反题录字重闸门，"
            "旧冻结作废并已重选"
        )
    elif stale_missing:
        report["stale_evidence"] = (
            "冻结字体在当前系统不存在，旧冻结作废并已重新解析: "
            + "、".join(stale_missing[:3])
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="解析并冻结作业使用的实际字体文件"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="忽略现有冻结结果，重新解析",
    )
    args = parser.parse_args()
    try:
        report = prepare_job_fonts(args.job_dir, force=args.force)
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
