#!/usr/bin/env python3
"""v4.0 新增：字幕翻译管线（纯 Python 标准库）。

4 个 CLI 子命令，编排 active session model 翻译流程：
  1. prepare:    transcript_N.json → manifest.json（含 segment、hash、翻译状态）
  2. next-batch: 取下一批未翻译 segment（80条/批，前后2条只读 context）
  3. render:     合并所有翻译结果 → translation_N.json
  4. validate:   校验翻译完整性

设计原则：
  - 翻译由 AI 完成（active session model），pipeline 只编排
  - segment 是不可变翻译单元（1 cue 1 segment，不做 smart 合并）
  - 批次间通过 context 保持连贯性
  - manifest 是唯一状态源，可从任意批次恢复

用法：
  # 1. 准备
  python subtitle_pipeline.py prepare \\
    --transcript transcript/transcript_1.json \\
    --output-dir work/subtitle-1/ \\
    --target-language zh-CN

  # 2. 取批次（循环调用直到 done:true）
  python subtitle_pipeline.py next-batch \\
    --manifest work/subtitle-1/manifest.json \\
    --output work/subtitle-1/batch-1.json

  # 3. AI 翻译 batch-1.json，写入 batch-1-response.json:
  #    {"translations":[{"id":"seg-...","translation":"中文译文"}]}

  # 4. 渲染（合并所有 batch response）
  python subtitle_pipeline.py render \\
    --manifest work/subtitle-1/manifest.json \\
    --output work/translation_1.json

  # 5. 校验
  python subtitle_pipeline.py validate \\
    --manifest work/subtitle-1/manifest.json \\
    --translation work/translation_1.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import read_json, write_json

# 翻译批次大小（条/批）
BATCH_SIZE = 80
# 前后 context 大小（条）
CONTEXT_SIZE = 2
# manifest 版本
MANIFEST_VERSION = "1.0"


def _segment_id(index: int, source_hash: str) -> str:
    """生成 segment ID: seg-000001-<hash前8位>"""
    return f"seg-{index + 1:06d}-{source_hash[:8]}"


def _hash_text(text: str) -> str:
    """SHA256 哈希文本（用于完整性校验）"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prepare(transcript_path: Path, output_dir: Path, target_language: str = "zh-CN") -> Path:
    """准备 manifest：把 transcript segments 转为翻译单元。

    Args:
        transcript_path: transcript_N.json 路径
        output_dir: 输出目录（manifest.json 存放处）
        target_language: 目标语言

    Returns:
        manifest.json 路径
    """
    transcript = read_json(transcript_path)
    segments = transcript.get("segments", [])
    source_language = transcript.get("language", "unknown")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"

    manifest_units = []
    for i, seg in enumerate(segments):
        text = seg.get("text", "").strip()
        if not text:
            continue
        source_hash = _hash_text(text)
        manifest_units.append({
            "id": _segment_id(i, source_hash),
            "index": i,
            "source": text,
            "source_hash": source_hash,
            "start": seg.get("start", 0),
            "end": seg.get("end", 0),
            "translation": None,
            "translated": False,
        })

    manifest = {
        "version": MANIFEST_VERSION,
        "source_language": source_language,
        "target_language": target_language,
        "source_transcript": str(transcript_path),
        "units": manifest_units,
        "batch_size": BATCH_SIZE,
        "context_size": CONTEXT_SIZE,
        "total_units": len(manifest_units),
        "translated_count": 0,
        "completed": False,
    }

    write_json(manifest_path, manifest)
    print(
        f"✅ manifest 准备完成: {manifest_path.name} "
        f"({len(manifest_units)} units, src={source_language}, tgt={target_language})",
        flush=True,
    )
    return manifest_path


def next_batch(manifest_path: Path, output_path: Path) -> dict:
    """取下一批未翻译的 segment。

    Returns:
        {
            "items": [{"id", "source"}],
            "context": {"before": [...], "after": [...]},
            "output_path": str,       # AI 翻译结果写入此路径
            "batch_number": int,
            "total_batches": int,
            "done": bool,
        }
    """
    manifest = read_json(manifest_path)
    units = manifest.get("units", [])
    batch_size = manifest.get("batch_size", BATCH_SIZE)
    context_size = manifest.get("context_size", CONTEXT_SIZE)

    # 找到第一个未翻译的 unit
    next_index = None
    for i, unit in enumerate(units):
        if not unit.get("translated", False):
            next_index = i
            break

    if next_index is None:
        return {
            "items": [],
            "context": {"before": [], "after": []},
            "output_path": str(output_path),
            "batch_number": 0,
            "total_batches": _estimate_total_batches(manifest),
            "done": True,
        }

    # 取一批
    batch_end = min(next_index + batch_size, len(units))
    batch_units = units[next_index:batch_end]

    items = [{"id": u["id"], "source": u["source"]} for u in batch_units]

    # context：前 2 条 + 后 2 条（只读，不在翻译范围内）
    before_ctx = [
        {"id": u["id"], "source": u["source"]}
        for u in units[max(0, next_index - context_size):next_index]
    ]
    after_ctx = [
        {"id": u["id"], "source": u["source"]}
        for u in units[batch_end:batch_end + context_size]
    ]

    batch_number = (next_index // batch_size) + 1
    total_batches = _estimate_total_batches(manifest)

    result = {
        "items": items,
        "context": {"before": before_ctx, "after": after_ctx},
        "output_path": str(output_path),
        "batch_number": batch_number,
        "total_batches": total_batches,
        "done": False,
    }

    write_json(output_path, result)
    print(
        f"   📦 批次 {batch_number}/{total_batches}: {len(items)} units "
        f"(index {next_index}-{batch_end - 1})",
        flush=True,
    )
    return result


def _estimate_total_batches(manifest: dict) -> int:
    """估算总批次数"""
    total = manifest.get("total_units", 0)
    batch_size = manifest.get("batch_size", BATCH_SIZE)
    return (total + batch_size - 1) // batch_size if batch_size > 0 else 0


def apply_batch_translation(
    manifest_path: Path, batch_response_path: Path
) -> int:
    """把 AI 翻译结果合并到 manifest。

    batch_response_path 文件格式：
        {"translations": [{"id": "seg-...", "translation": "中文译文"}]}

    Returns:
        本次合并的翻译数量
    """
    manifest = read_json(manifest_path)
    response = read_json(batch_response_path)

    translations = response.get("translations", [])
    if not translations:
        return 0

    # 建立 id → translation 映射
    trans_map = {t["id"]: t["translation"] for t in translations}

    # 合并到 manifest units
    applied = 0
    for unit in manifest.get("units", []):
        if unit["id"] in trans_map and not unit.get("translated", False):
            unit["translation"] = trans_map[unit["id"]]
            unit["translated"] = True
            applied += 1

    # 更新计数
    manifest["translated_count"] = sum(
        1 for u in manifest.get("units", []) if u.get("translated", False)
    )
    manifest["completed"] = manifest["translated_count"] == manifest["total_units"]

    write_json(manifest_path, manifest)
    print(
        f"   ✅ 合并 {applied} 条翻译 "
        f"({manifest['translated_count']}/{manifest['total_units']})",
        flush=True,
    )
    return applied


def render(manifest_path: Path, output_path: Path) -> Path:
    """渲染 manifest 为 translation_N.json。

    输出格式：
        {
            "translations": [{"id", "source", "translation"}],
            "source_language": "en",
            "target_language": "zh-CN",
            "total_units": 100,
            "translated_count": 100
        }
    """
    manifest = read_json(manifest_path)
    units = manifest.get("units", [])

    translations = []
    for unit in units:
        translations.append({
            "id": unit["id"],
            "source": unit["source"],
            "translation": unit.get("translation") or "",
            "start": unit.get("start", 0),
            "end": unit.get("end", 0),
        })

    output = {
        "translations": translations,
        "source_language": manifest.get("source_language", "unknown"),
        "target_language": manifest.get("target_language", "zh-CN"),
        "total_units": manifest.get("total_units", 0),
        "translated_count": manifest.get("translated_count", 0),
        "completed": manifest.get("completed", False),
    }

    write_json(output_path, output)
    print(
        f"✅ 渲染完成: {output_path.name} "
        f"({output['translated_count']}/{output['total_units']} 已翻译)",
        flush=True,
    )
    return output_path


def validate(manifest_path: Path, translation_path: Path) -> bool:
    """校验翻译完整性。

    Returns:
        True = 全部翻译且 hash 匹配，False = 有缺失或不匹配
    """
    manifest = read_json(manifest_path)
    translation = read_json(translation_path)

    manifest_units = manifest.get("units", [])
    translations = translation.get("translations", [])

    # 建立 id → translation 映射
    trans_map = {t["id"]: t for t in translations}

    errors = []
    for unit in manifest_units:
        uid = unit["id"]
        if uid not in trans_map:
            errors.append(f"缺失翻译: {uid}")
            continue
        t = trans_map[uid]
        # 校验 hash
        if t.get("source", "") != unit["source"]:
            errors.append(f"源文本不匹配: {uid}")
        if not t.get("translation"):
            errors.append(f"翻译为空: {uid}")

    if errors:
        print(f"❌ 校验失败（{len(errors)} 个错误）:", file=sys.stderr)
        for e in errors[:5]:
            print(f"   - {e}", file=sys.stderr)
        if len(errors) > 5:
            print(f"   ... 还有 {len(errors) - 5} 个", file=sys.stderr)
        return False

    print(
        f"✅ 校验通过: {len(translations)}/{len(manifest_units)} "
        f"(src={manifest.get('source_language')}, tgt={manifest.get('target_language')})",
        flush=True,
    )
    return True


def main():
    parser = argparse.ArgumentParser(
        description="v4.0: 字幕翻译管线（prepare/next-batch/render/validate）"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # prepare
    p_prepare = sub.add_parser("prepare", help="准备 manifest")
    p_prepare.add_argument("--transcript", required=True, help="transcript_N.json 路径")
    p_prepare.add_argument("--output-dir", required=True, help="输出目录")
    p_prepare.add_argument("--target-language", default="zh-CN", help="目标语言")

    # next-batch
    p_batch = sub.add_parser("next-batch", help="取下一批")
    p_batch.add_argument("--manifest", required=True, help="manifest.json 路径")
    p_batch.add_argument("--output", required=True, help="批次输出路径")

    # apply（合并翻译结果到 manifest）
    p_apply = sub.add_parser("apply", help="合并翻译结果")
    p_apply.add_argument("--manifest", required=True, help="manifest.json 路径")
    p_apply.add_argument("--response", required=True, help="batch response 路径")

    # render
    p_render = sub.add_parser("render", help="渲染最终翻译")
    p_render.add_argument("--manifest", required=True, help="manifest.json 路径")
    p_render.add_argument("--output", required=True, help="输出 translation_N.json 路径")

    # validate
    p_validate = sub.add_parser("validate", help="校验翻译")
    p_validate.add_argument("--manifest", required=True, help="manifest.json 路径")
    p_validate.add_argument("--translation", required=True, help="translation_N.json 路径")

    args = parser.parse_args()

    if args.command == "prepare":
        prepare(
            Path(args.transcript),
            Path(args.output_dir),
            args.target_language,
        )
    elif args.command == "next-batch":
        next_batch(Path(args.manifest), Path(args.output))
    elif args.command == "apply":
        apply_batch_translation(Path(args.manifest), Path(args.response))
    elif args.command == "render":
        render(Path(args.manifest), Path(args.output))
    elif args.command == "validate":
        success = validate(Path(args.manifest), Path(args.translation))
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
