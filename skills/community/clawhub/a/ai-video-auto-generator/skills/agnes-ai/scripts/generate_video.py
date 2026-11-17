#!/usr/bin/env python3
"""Agnes AI 视频生成 CLI — 仅文生视频/图生视频。项目级操作在 project-generate。"""
import argparse, json, os, sys, time
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from modules.video_api import (
    API_BASE_VIDEO, DEFAULT_VIDEO_MODEL, DURATION_PRESETS,
    submit_video, quick_query, poll_task, download_video,
    get_closest_valid_frames, parse_size, _select_mode, _log,
)
from modules.image_api import load_api_key

MODE_HELP = """standard:    标准文生图/图生视频（默认）
multi-image: 多图视频，2+ 张参考图 → extra_body.image 数组
keyframes:   关键帧动画，2+ 张参考图 → extra_body.image + extra_body.mode=keyframes"""


def main():
    parser = argparse.ArgumentParser(description="Agnes AI 视频生成（文生视频/图生视频）")
    parser.add_argument("prompt", nargs="?", default="", help="视频描述提示词")
    parser.add_argument("--mode", default="standard", choices=["standard", "keyframes", "multi-image", "auto"], help=MODE_HELP)
    parser.add_argument("--model", default=DEFAULT_VIDEO_MODEL, help="模型名")
    parser.add_argument("--ref-image", help="参考图路径（标准模式）")
    parser.add_argument("--ref-image-list", nargs="+", help="多张参考图路径（关键帧/多图模式）")
    parser.add_argument("--ref-image-urls", nargs="+", help="已上传的参考图 URL")
    parser.add_argument("--duration", choices=list(DURATION_PRESETS.keys()), help="时长预设")
    parser.add_argument("--num-frames", type=int, default=121)
    parser.add_argument("--frame-rate", type=int, default=24)
    parser.add_argument("--size", default="1152x768", help="分辨率或比例别名（16:9 / 9:16 / 1:1）")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--negative-prompt", help="负向提示词")
    parser.add_argument("-o", "--output-dir", default=".", help="输出目录")
    parser.add_argument("--output-name", help="输出文件名")
    parser.add_argument("--api-key", help="API Key 文件路径")
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--submit-only", action="store_true", help="仅创建任务，打印 task_id 后退出")
    parser.add_argument("--query-task", help="查询已有任务，若完成则下载")
    parser.add_argument("--version", action="store_true", help="显示版本信息")
    parser.add_argument("--verbose", action="store_true", help="详细输出模式")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    args = parser.parse_args()

    if args.quiet:
        import modules.config as _cfg; _cfg.LOG_LEVEL = 0
    elif args.verbose:
        import modules.config as _cfg; _cfg.LOG_LEVEL = 2

    if args.version:
        _log(f"Agnes AI 视频生成工具  v2.1.0", level=0)
        return

    if args.query_task:
        api_key = load_api_key(args.api_key)
        video_url = poll_task(api_key, args.query_task, args.poll_interval, args.timeout)
        if video_url:
            os.makedirs(args.output_dir, exist_ok=True)
            fn = args.output_name or f"{args.query_task}.mp4"
            download_video(video_url, os.path.join(args.output_dir, fn))
            _log(f"\n== 完成！视频已保存")
        return

    if not args.prompt:
        parser.error("必须指定 prompt（或使用 --query-task 查询已有任务）")

    api_key = load_api_key(args.api_key)

    if args.duration:
        args.num_frames = DURATION_PRESETS[args.duration]
        _log(f"  [时长] 预设 {args.duration} → num_frames={args.num_frames}")
    if args.num_frames not in [8 * n + 1 for n in range(1, 56) if 8 * n + 1 <= 441]:
        closest = get_closest_valid_frames(args.num_frames)
        _log(f"  [调整] num_frames={args.num_frames} → {closest}")
        args.num_frames = closest

    ref_paths = []; ref_urls = []
    if args.ref_image_urls:
        ref_urls = args.ref_image_urls
    elif args.ref_image_list:
        ref_paths = args.ref_image_list
    elif args.ref_image:
        ref_paths = [args.ref_image]

    width, height = parse_size(args.size)
    mode = args.mode

    if mode == "standard" and len(ref_paths) == 1:
        task_id = submit_video(
            prompt=args.prompt, ref_img=ref_paths[0], mode=mode,
            num_frames=args.num_frames, frame_rate=args.frame_rate,
            width=width, height=height,
            seed=args.seed, negative_prompt=args.negative_prompt,
        )
    else:
        task_id = submit_video(
            prompt=args.prompt, mode=mode,
            ref_paths=ref_paths if ref_paths else None,
            ref_urls=ref_urls if ref_urls else None,
            num_frames=args.num_frames, frame_rate=args.frame_rate,
            width=width, height=height,
            seed=args.seed, negative_prompt=args.negative_prompt,
        )

    if not task_id:
        sys.exit(1)

    if args.submit_only:
        _log(f"TASK_ID={task_id}")
        return

    video_url = poll_task(api_key, task_id, args.poll_interval, args.timeout)
    os.makedirs(args.output_dir, exist_ok=True)
    if args.output_name:
        fn = args.output_name
    else:
        ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        sp = "".join(c if c.isalnum() or c in " _-" else "_" for c in args.prompt[:30])
        fn = f"{sp}_{ts}.mp4"
    download_video(video_url, os.path.join(args.output_dir, fn))
    _log(f"\n== 完成！视频已保存")


if __name__ == "__main__":
    main()
