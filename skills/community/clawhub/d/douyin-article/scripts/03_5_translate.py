#!/usr/bin/env python3
"""v4.0 新增：阶段 3.5 翻译编排。

扫描 pack_summary.json，为需要翻译的视频（非中文）准备 subtitle_pipeline manifest。
实际翻译由主对话（AI / active session model）完成，本脚本只负责编排和进度查询。

工作流程：
  1. prepare: 扫描 pack_summary，为 needs_translation=true 的视频生成 manifest
  2. 主对话循环:
     a. next-batch → 取一批未翻译 segment
     b. AI 翻译 → 写 batch-response.json
     c. apply → 合并到 manifest
     d. 重复直到 done:true
     e. render → 输出 translation_N.json
     f. validate → 校验
  3. status: 查询翻译进度

用法：
  python 03_5_translate.py prepare --output-dir work/
  python 03_5_translate.py status --output-dir work/
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import read_json, write_json
from subtitle_pipeline import prepare as pipeline_prepare


def prepare_translations(work_dir: Path, target_language: str = "zh-CN") -> list[dict]:
    """扫描 pack_summary，为需要翻译的视频准备 manifest。

    Returns:
        [{"video_id", "title", "manifest_path", "total_units"}]
    """
    pack_summary_path = work_dir / "pack_summary.json"
    if not pack_summary_path.exists():
        print(f"❌ 未找到 pack_summary.json: {pack_summary_path}", file=sys.stderr)
        sys.exit(1)

    summary = read_json(pack_summary_path)
    items = summary.get("items", [])

    # 筛选需要翻译的
    to_translate = [it for it in items if it.get("needs_translation", False)]
    if not to_translate:
        print("✅ 没有需要翻译的视频（全部为中文内容）", flush=True)
        return []

    print(f"📋 需要翻译: {len(to_translate)}/{len(items)} 个视频", flush=True)

    results = []
    for item in to_translate:
        video_id = item["video_id"]
        title = item["title"]
        transcript_path = work_dir.parent / "transcript" / f"transcript_{video_id}.json"

        if not transcript_path.exists():
            print(f"   ⚠️ 跳过 {video_id}: transcript 文件不存在", flush=True)
            continue

        # 准备 manifest
        manifest_dir = work_dir / f"subtitle-{video_id}"
        manifest_path = pipeline_prepare(
            transcript_path=transcript_path,
            output_dir=manifest_dir,
            target_language=target_language,
        )

        manifest = read_json(manifest_path)
        results.append({
            "video_id": video_id,
            "title": title,
            "manifest_path": str(manifest_path),
            "total_units": manifest.get("total_units", 0),
            "translated_count": 0,
            "completed": False,
        })

        print(
            f"   📝 视频 {video_id}: {title} "
            f"({manifest.get('total_units', 0)} units)",
            flush=True,
        )

    # 写入翻译状态文件
    status_path = work_dir / "translation_status.json"
    write_json(status_path, {
        "items": results,
        "target_language": target_language,
        "total_videos": len(results),
        "completed_videos": 0,
    })

    print(f"\n📊 翻译准备完成: {len(results)} 个视频待翻译", flush=True)
    print(f"   状态文件: {status_path.name}", flush=True)
    print(f"\n💡 主对话（AI）现在可以循环调用 subtitle_pipeline next-batch 翻译", flush=True)
    return results


def check_status(work_dir: Path) -> dict:
    """查询翻译进度。"""
    status_path = work_dir / "translation_status.json"
    if not status_path.exists():
        print("ℹ️ 无翻译任务（可能全部为中文内容，或尚未执行 prepare）", flush=True)
        return {"items": [], "total_videos": 0, "completed_videos": 0}

    status = read_json(status_path)
    items = status.get("items", [])

    print(f"📊 翻译进度: {len(items)} 个视频", flush=True)
    completed = 0
    for item in items:
        manifest_path = Path(item["manifest_path"])
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            translated = manifest.get("translated_count", 0)
            total = manifest.get("total_units", 0)
            is_done = manifest.get("completed", False)
            pct = (translated / total * 100) if total > 0 else 0
            status_icon = "✅" if is_done else "🔄"
            print(
                f"   {status_icon} 视频 {item['video_id']}: {item['title'][:40]}... "
                f"{translated}/{total} ({pct:.0f}%)",
                flush=True,
            )
            item["translated_count"] = translated
            item["completed"] = is_done
            if is_done:
                completed += 1
        else:
            print(f"   ❌ 视频 {item['video_id']}: manifest 不存在", flush=True)

    status["completed_videos"] = completed
    write_json(status_path, status)

    print(f"\n总计: {completed}/{len(items)} 完成", flush=True)
    return status


def main():
    parser = argparse.ArgumentParser(
        description="v4.0: 阶段 3.5 翻译编排（prepare/status）"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare", help="准备翻译 manifest")
    p_prepare.add_argument("--output-dir", required=True, help="work/ 目录")
    p_prepare.add_argument("--target-language", default="zh-CN", help="目标语言")

    p_status = sub.add_parser("status", help="查询翻译进度")
    p_status.add_argument("--output-dir", required=True, help="work/ 目录")

    args = parser.parse_args()

    if args.command == "prepare":
        prepare_translations(Path(args.output_dir), args.target_language)
    elif args.command == "status":
        check_status(Path(args.output_dir))


if __name__ == "__main__":
    main()
