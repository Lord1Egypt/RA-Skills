# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json
import os
import socket
import time
from typing import Any

from common import (
    OUTPUT_ROOT,
    create_client,
    create_video_task,
    default_output_path,
    download_file,
    extract_video_url,
    get_trace_id,
    log_params,
    query_video_task,
    resolve_image_source,
    setup_logging,
    wait_for_video_task,
)

setup_logging()

DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"
DEFAULT_PROMPT = "小猫对着镜头打哈欠，镜头缓缓拉出"
DEFAULT_RATIO = "16:9"
DEFAULT_DURATION = 5
DEFAULT_CALLBACK_PORT = 8888


def get_local_ip() -> str:
    """Get the local network IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def _read_webhook_token() -> str | None:
    """Read the webhook token from the file written by webhook_server.py."""
    token_path = OUTPUT_ROOT / "outputs" / "doubao" / ".webhook_token"
    if token_path.exists():
        token = token_path.read_text(encoding="utf-8").strip()
        if token:
            return token
    return None


def resolve_callback_url(manual_url: str | None) -> str | None:
    """Resolve callback URL: manual > env var > auto-detect local IP."""
    if manual_url:
        return manual_url
    base = os.getenv("VIDEO_CALLBACK_BASE_URL")
    if base:
        base = base.rstrip("/")
        token = _read_webhook_token()
        if token:
            return f"{base}/webhook/callback/{token}"
        return f"{base}/webhook/callback"
    # Auto-detect: check if webhook server is running on default port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("127.0.0.1", DEFAULT_CALLBACK_PORT))
        s.close()
        ip = get_local_ip()
        token = _read_webhook_token()
        if token:
            return f"http://{ip}:{DEFAULT_CALLBACK_PORT}/webhook/callback/{token}"
        return f"http://{ip}:{DEFAULT_CALLBACK_PORT}/webhook/callback"
    except OSError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包 Seedance 视频生成")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--name", default="", help="文件名描述，不超过 10 个中文字")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument(
        "--image-url",
        action="append",
        dest="image_urls",
        help="图片 URL 或本地路径，可多次传；配合 --role 使用",
    )
    parser.add_argument(
        "--last-frame-url",
        help="尾帧图片 URL 或本地路径（用于首尾帧图生视频场景）",
    )
    parser.add_argument(
        "--role",
        default="first_frame",
        choices=["first_frame", "last_frame"],
        help="图片角色（需配合 --image-url）",
    )
    parser.add_argument("--ratio", default=DEFAULT_RATIO, help="宽高比：16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="视频时长（秒）：2~12，默认 5")
    parser.add_argument("--resolution", default="480p", help="分辨率：480p, 720p, 1080p")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument(
        "--generate-audio",
        action="store_true",
        default=False,
        help="生成有声视频（仅 1.5 pro 支持，API 默认 true）",
    )
    parser.add_argument("--watermark", action="store_true", default=False, help="添加水印")
    parser.add_argument(
        "--camera-fixed",
        action="store_true",
        default=False,
        help="固定摄像头（参考图场景不支持）",
    )
    parser.add_argument(
        "--return-last-frame",
        action="store_true",
        default=False,
        help="返回生成视频的尾帧图像",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        default=False,
        help="生成样片（仅 1.5 pro）",
    )
    parser.add_argument(
        "--execution-expires-after",
        type=int,
        help="任务超时时间（秒），范围 [3600, 259200]，默认 172800（48小时）",
    )
    parser.add_argument(
        "--frames",
        type=int,
        help="生成视频帧数，格式 25+4n，范围 [29, 289]（1.5 pro 暂不支持）",
    )
    parser.add_argument(
        "--service-tier",
        choices=["default", "flex"],
        help="推理模式：default（在线）/ flex（离线，50%% 价格）",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        default=False,
        help="创建后自动轮询并下载",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="轮询间隔秒数，默认 10",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="轮询超时秒数，默认 900",
    )
    parser.add_argument(
        "--callback-url",
        help="Webhook 回调地址；不传时自动检测：先读环境变量 VIDEO_CALLBACK_BASE_URL，再探测本地 8888 端口并获取本机 IP",
    )
    return parser.parse_args()


def build_content(
    prompt: str,
    image_urls: list[str] | None = None,
    last_frame_url: str | None = None,
    role: str = "first_frame",
) -> list[dict[str, Any]]:
    """Build the content array for the API request."""
    content: list[dict[str, Any]] = [
        {"type": "text", "text": prompt}
    ]
    if image_urls:
        for url in image_urls:
            item: dict[str, Any] = {
                "type": "image_url",
                "image_url": {"url": resolve_image_source(url)},
            }
            if role:
                item["role"] = role
            content.append(item)
    if last_frame_url:
        item: dict[str, Any] = {
            "type": "image_url",
            "image_url": {"url": resolve_image_source(last_frame_url)},
            "role": "last_frame",
        }
        content.append(item)
    return content


def determine_scene(
    image_urls: list[str] | None,
    role: str | None = None,
    last_frame_url: str | None = None,
) -> str:
    if not image_urls and not last_frame_url:
        return "text_to_video"
    if last_frame_url or role == "last_frame" or (len(image_urls) > 1):
        return "first_last_frame_to_video"
    return "first_frame_to_video"


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    client = create_client()
    content = build_content(args.prompt, args.image_urls, args.last_frame_url, args.role)
    scene = determine_scene(args.image_urls, args.role, args.last_frame_url)
    image_refs = args.image_urls or []
    if args.last_frame_url:
        image_refs.append(args.last_frame_url)
    log_params(
        "视频任务开始", scene=scene, model=args.model, prompt=args.prompt, name=args.name,
        ratio=args.ratio, duration=args.duration, resolution=args.resolution or "480p",
        generate_audio=args.generate_audio or "(API默认true)",
        service_tier=args.service_tier or "(API默认default/在线)",
        draft=args.draft, return_last_frame=args.return_last_frame,
        images=image_refs or "(无)",
    )
    trace_id = get_trace_id()

    # Build optional kwargs
    kwargs: dict[str, Any] = {
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": args.watermark,
    }
    if args.resolution:
        kwargs["resolution"] = args.resolution
    else:
        kwargs["resolution"] = "480p"
    if args.seed is not None:
        kwargs["seed"] = args.seed
    if args.generate_audio:
        kwargs["generate_audio"] = True
    if args.camera_fixed:
        kwargs["camera_fixed"] = True
    if args.return_last_frame:
        kwargs["return_last_frame"] = True
    if args.draft:
        kwargs["draft"] = True
    if args.execution_expires_after is not None:
        kwargs["execution_expires_after"] = args.execution_expires_after
    if args.frames is not None:
        kwargs["frames"] = args.frames
    if args.service_tier:
        kwargs["service_tier"] = args.service_tier
    if args.callback_url:
        kwargs["callback_url"] = args.callback_url
    else:
        callback_url = resolve_callback_url(None)
        if callback_url:
            kwargs["callback_url"] = callback_url
            print(f"自动检测到回调地址: {callback_url}")

    print(f"创建视频任务: model={args.model}")
    api_start = time.monotonic()
    result = create_video_task(client, model=args.model, content=content, **kwargs)
    api_elapsed = time.monotonic() - api_start

    task_id = result.get("id", "")
    status = result.get("status", "unknown")
    print(f"任务已创建: {task_id}, 状态: {status}")
    log_params("视频任务创建完成", task_id=task_id, status=status, api_elapsed=round(api_elapsed, 3))

    create_output = {
        "type": "video",
        "scene": scene,
        "provider": "doubao",
        "trace_id": trace_id,
        "task_id": task_id,
        "status": status,
        "timing": {
            "total_elapsed": round(time.monotonic() - pipeline_start, 3),
            "api_elapsed": round(api_elapsed, 3),
        },
    }
    print(json.dumps(create_output, ensure_ascii=False, indent=2))

    if not args.poll:
        return

    # Poll until completion
    print(f"\n开始轮询任务: {task_id}")
    log_params("开始轮询视频任务", task_id=task_id, interval=args.poll_interval, timeout=args.timeout)
    poll_start = time.monotonic()
    final = wait_for_video_task(
        client,
        task_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    poll_elapsed = time.monotonic() - poll_start

    video_url = extract_video_url(final)
    print(f"视频生成成功，开始下载...")
    log_params("视频生成成功", task_id=task_id, poll_elapsed=round(poll_elapsed, 3))

    output_path = default_output_path("videos", scene, suffix=".mp4", name=args.name)
    download_file(video_url, output_path)
    log_params("视频下载完成", path=str(output_path.name))

    poll_output = {
        "type": "video",
        "scene": scene,
        "provider": "doubao",
        "trace_id": trace_id,
        "task_id": task_id,
        "used_model": args.model,
        "local_path": str(output_path.relative_to(OUTPUT_ROOT)),
        "source_url": video_url,
        "resolution": final.get("resolution", ""),
        "ratio": final.get("ratio", ""),
        "duration": final.get("duration", ""),
        "timing": {
            "total_elapsed": round(time.monotonic() - pipeline_start, 3),
            "api_elapsed": round(api_elapsed, 3),
            "poll_elapsed": round(poll_elapsed, 3),
        },
    }
    log_params("视频任务完成", task_id=task_id, total_elapsed=round(time.monotonic() - pipeline_start, 3))
    print(json.dumps(poll_output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
