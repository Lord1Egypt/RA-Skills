#!/usr/bin/env python3
"""Agnes AI 图片生成 CLI — 仅文生图/图生图。项目级操作在 project-generate。"""

import argparse, json, os, sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from modules.config import _auto_size, _log, _safe_write_json
from modules.image_api import load_api_key, generate_image, API_BASE, DEFAULT_MODEL, VERSION
from modules.prompt import _resolve_single_shot_params


def main():
    parser = argparse.ArgumentParser(description="Agnes AI 图片生成（文生图/图生图）")
    parser.add_argument("prompt", nargs="?", default="", help="图片描述提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"模型名（默认: {DEFAULT_MODEL}）")
    parser.add_argument("--size", default="1024x1024", help="图片尺寸（默认: 1024x1024）")
    parser.add_argument("--n", type=int, default=1, help="生成数量（默认: 1）")
    parser.add_argument("--quality", default="standard", choices=["standard", "hd"], help="质量（默认: standard）")
    parser.add_argument("--output-dir", "-o", default=".", help="输出目录（默认: 当前目录）")
    parser.add_argument("--api-key", help="API Key 文件路径")
    parser.add_argument("--ref-image", help="参考图路径（启用图生图模式）")
    parser.add_argument("--ref-images", nargs="+", help="多张参考图路径（多图图生图模式）")
    parser.add_argument("--output-name", help="输出文件名（默认自动生成带时间戳的文件名）")
    parser.add_argument("--shot-id", type=int, help="从 script.json 读取 shot 配置生成首帧图（需 --project）")
    parser.add_argument("--project", help="项目根目录（--shot-id 模式需要）")
    parser.add_argument("--seed", type=int, default=None, help="固定随机种子（可复现结果）")
    parser.add_argument("--negative-prompt", default="", help="负面提示词（排除不需要的元素）")
    parser.add_argument("--version", action="store_true", help="显示脚本版本信息")
    parser.add_argument("--verbose", action="store_true", help="详细输出模式")
    parser.add_argument("--quiet", action="store_true", help="静默模式（只输出最终结果）")
    args = parser.parse_args()

    if args.quiet:
        import modules.config as _cfg; _cfg.LOG_LEVEL = 0
    elif args.verbose:
        import modules.config as _cfg; _cfg.LOG_LEVEL = 2

    if args.version:
        _log(f"Agnes AI 图片生成工具  v{VERSION}", level=0)
        _log(f"  API Base:  {API_BASE}", level=0)
        _log(f"  默认模型:  {DEFAULT_MODEL}", level=0)
        return

    api_key = load_api_key(args.api_key)

    # --shot-id 模式：从 script.json 读取 shot 配置
    if args.shot_id is not None:
        if not args.project:
            parser.error("--shot-id 需要配合 --project 使用")
        if args.size == "1024x1024":
            auto_sz = _auto_size(args.project)
            if auto_sz != "1024x1024":
                args.size = auto_sz
                _log(f"  -> 尺寸自动设为: {args.size}（来自 script.aspect_ratio）")
        script_path = os.path.join(args.project, "script.json")
        if not os.path.isfile(script_path):
            parser.error(f"未找到 script.json: {script_path}")
        with open(script_path, "r", encoding="utf-8") as f:
            sdata = json.load(f)
        shot = next((s for s in sdata.get("shots", []) if s.get("id") == args.shot_id), None)
        if not shot:
            parser.error(f"shot_{args.shot_id:02d} 未找到")
        params = _resolve_single_shot_params(args.project, shot, args.size)
        if args.model != DEFAULT_MODEL:
            params["model"] = args.model
        preview = params["prompt"][:120].replace("\n", " ").strip()
        _log(f"\n  📋 生成预览")
        _log(f"     ┌─ 模型: {params['model']}")
        _log(f"     ├─ 尺寸: {args.size}")
        _log(f"     ├─ 参考图: {len(params['ref_images'])} 张")
        _log(f"     ├─ 输出: {os.path.join(params['output_dir'], params['output_name'])}")
        _log(f"     └─ 提示词: {preview}...")
        files = generate_image(
            api_key=api_key, prompt=params["prompt"],
            model=params["model"], size=args.size,
            output_dir=params["output_dir"],
            ref_images=params["ref_images"],
            output_name=params["output_name"],
            project=args.project, seed=args.seed,
            negative_prompt=args.negative_prompt or None,
        )
        _log(f"\n== 完成！共生成 {len(files)} 张图片：", level=0)
        for f in files:
            _log(f"  {f}", level=0)
        if files:
            with open(script_path, "r", encoding="utf-8") as f:
                sdata = json.load(f)
            st = next((s for s in sdata.get("shots", []) if s.get("id") == args.shot_id), None)
            if st and st.get("first_frame"):
                if args.seed is not None:
                    st["first_frame"]["seed"] = args.seed
                elif st["first_frame"].get("seed") is None:
                    st["first_frame"]["seed"] = None
                _safe_write_json(script_path, sdata)
        return

    # 普通模式：文生图/图生图
    if not args.prompt:
        parser.error("请提供提示词，或使用 --shot-id 模式")
    files = generate_image(
        api_key=api_key, prompt=args.prompt, model=args.model,
        size=args.size, n=args.n, quality=args.quality,
        output_dir=args.output_dir, ref_image=args.ref_image,
        ref_images=args.ref_images, output_name=args.output_name,
    )
    _log(f"\n== 完成！共生成 {len(files)} 张图片：", level=0)
    for f in files:
        _log(f"  {f}", level=0)


if __name__ == "__main__":
    main()
