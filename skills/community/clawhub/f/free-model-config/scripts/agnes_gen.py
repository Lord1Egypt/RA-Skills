#!/usr/bin/env python3
"""
Agnes AI 多模态生成工具（图像/视频）。

架构：基本命令组合复杂命令
- 基本命令：image、video、concat
- 复杂命令：long-video、images-video、story-video（由基本命令组合而成）

用法:
  # 基本命令
  python agnes_gen.py image --prompt "描述" [--size 2K] [--ratio 16:9] [--output result.png]
  python agnes_gen.py video --prompt "描述" [--seconds 5] [--size 720P] [--aspect-ratio 16:9]
  python agnes_gen.py concat --inputs a.mp4 b.mp4 c.mp4 --output long.mp4

  # 复杂命令（由基本命令组合）
  python agnes_gen.py long-video --prompt "描述" --segments 3 --segment-seconds 10 --output long.mp4
  python agnes_gen.py images-video --images img1.png img2.png --prompt "描述" --output result.mp4
  python agnes_gen.py story-video --storyboard storyboard.json --output story.mp4

环境变量:
  AGNES_API_KEY      - API 密钥（优先）
  FREE_MODEL_CONFIG  - 通用台账路径（默认 ~/.free-model-config/models.json）

说明:
  Video 2.5 接口以「秒 + 分辨率档位」表达时长与画质；
  旧的 --width/--height/--frames/--fps 仍可传入，但会自动换算并告警。
"""

import argparse
import base64
import json
import os
import sys
import time
import struct
import urllib.request
import urllib.error
import urllib.parse
import io
import subprocess
import tempfile
import shutil

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_BASE = "https://apihub.agnes-ai.com"

# 当前现役模型 ID（基线以 SKILL.md 平台表为准；平台升级后只需改这里）
MODEL_TEXT = "agnes-3.0-flash"
MODEL_IMAGE = "agnes-image-2.5-flash"
MODEL_VIDEO = "agnes-video-2.5"
MODEL_VIDEO_FAST = "agnes-video-2.5-flash"

# Video 2.5 只接受档位名与秒数，不再接受 width/height/fps/num_frames
VIDEO_SIZES = ("720P", "1080P", "1K", "2K")
VIDEO_ASPECTS = ("16:9", "9:16", "1:1", "4:3", "3:4", "2:3", "3:2", "21:9")
VIDEO_SECONDS_MIN = 4
VIDEO_SECONDS_MAX = 12


def normalize_seconds(value, default="5"):
    """把任意输入规整为 4–12 的字符串秒数"""
    try:
        n = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default
    n = max(VIDEO_SECONDS_MIN, min(VIDEO_SECONDS_MAX, n))
    return str(n)


def normalize_size(value, default="720P"):
    """把旧式像素值/小写档位规整为合法档位"""
    if not value:
        return default
    text = str(value).strip()
    if text.upper() in VIDEO_SIZES:
        return text.upper()
    return default


def legacy_geometry_to_size(width=None, height=None, default="720P"):
    """把旧的 width/height 近似映射到分辨率档位"""
    if not width or not height:
        return default
    short_edge = min(int(width), int(height))
    if short_edge >= 1000:
        return "1080P"
    return "720P"


def api_request(method, path, body=None, api_key=None, timeout=300, exit_on_error=True):
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
        err_body = ""
        if isinstance(e, urllib.error.HTTPError) and e.fp:
            err_body = e.read().decode()
        print(f"API Error: {e} {err_body}", file=sys.stderr)
        if exit_on_error:
            sys.exit(1)
        return None


def upload_image_to_url(local_path):
    """将本地图片上传到临时文件托管服务，返回可访问的 URL"""
    with open(local_path, "rb") as f:
        img_data = f.read()

    # 尝试 catbox.moe
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    parts = []
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(b'Content-Disposition: form-data; name="reqtype"\r\n\r\n')
    parts.append(b"fileupload\r\n")
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(f'Content-Disposition: form-data; name="fileToUpload"; filename="image.png"\r\n'.encode())
    parts.append(b"Content-Type: image/png\r\n\r\n")
    parts.append(img_data)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)

    req = urllib.request.Request("https://catbox.moe/user/api.php", data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            url = resp.read().decode().strip()
        if url.startswith("http"):
            print(f"图片已上传: {url}", file=sys.stderr)
            return url
    except Exception as e:
        print(f"catbox.moe 上传失败: {e}", file=sys.stderr)

    # 备选: litterbox
    boundary2 = "----FormBoundary7MA4YWxkTrZu0gW"
    parts2 = []
    parts2.append(f"--{boundary2}\r\n".encode())
    parts2.append(b'Content-Disposition: form-data; name="reqtype"\r\n\r\n')
    parts2.append(b"fileupload\r\n")
    parts2.append(f"--{boundary2}\r\n".encode())
    parts2.append(b'Content-Disposition: form-data; name="time"\r\n\r\n')
    parts2.append(b"24h\r\n")
    parts2.append(f"--{boundary2}\r\n".encode())
    parts2.append(f'Content-Disposition: form-data; name="fileToUpload"; filename="image.png"\r\n'.encode())
    parts2.append(b"Content-Type: image/png\r\n\r\n")
    parts2.append(img_data)
    parts2.append(f"\r\n--{boundary2}--\r\n".encode())
    body2 = b"".join(parts2)

    req2 = urllib.request.Request("https://litterbox.catbox.moe/resources/internals/api.php", data=body2)
    req2.add_header("Content-Type", f"multipart/form-data; boundary={boundary2}")
    try:
        with urllib.request.urlopen(req2, timeout=120) as resp2:
            url = resp2.read().decode().strip()
        if url.startswith("http"):
            print(f"图片已上传: {url}", file=sys.stderr)
            return url
    except Exception as e:
        print(f"litterbox 上传失败: {e}", file=sys.stderr)

    print("错误: 无法上传图片到任何托管服务", file=sys.stderr)
    sys.exit(1)


def _poll_video(video_id, model_name, api_key, output_path=None):
    """轮询视频任务（video_id + model_name），返回视频 URL"""
    print("等待视频生成（轮询间隔 2 秒）...", file=sys.stderr)
    query = urllib.parse.urlencode({"video_id": video_id, "model_name": model_name})
    path = f"/agnesapi?{query}"
    while True:
        time.sleep(2)
        status_result = api_request("GET", path, api_key=api_key, timeout=30, exit_on_error=False)
        if not status_result:
            print("轮询请求失败，重试...", file=sys.stderr)
            continue
        status = status_result.get("status", "unknown")
        progress = status_result.get("progress", 0)
        print(f"状态: {status} ({progress}%)", file=sys.stderr)

        if status == "completed":
            video_url = status_result.get("url") or ""
            if output_path and video_url:
                urllib.request.urlretrieve(video_url, output_path)
                print(f"视频已下载: {output_path}", file=sys.stderr)
            return video_url
        if status == "failed":
            error = status_result.get("error") or "未知错误"
            print(f"视频生成失败: {error}", file=sys.stderr)
            return None


def _create_video_task(body, api_key):
    """创建视频生成任务，返回 (video_id, model_name)"""
    print("正在创建视频任务...", file=sys.stderr)
    result = api_request("POST", "/v1/videos", body, api_key, timeout=600)
    video_id = result.get("video_id")
    model_name = result.get("model") or body.get("model")
    seconds = result.get("seconds", "unknown")
    size = result.get("size", "unknown")
    if not video_id:
        print(f"错误: 创建响应中没有 video_id: {result}", file=sys.stderr)
        sys.exit(1)
    print(f"任务已创建: video_id={video_id}, 时长={seconds}秒, 分辨率={size}", file=sys.stderr)
    return video_id, model_name


# ============================================================
# 基本命令（原子操作）
# ============================================================

def generate_image_core(prompt, image=None, size="1K", ratio="1:1", seed=None, output=None, api_key=None):
    """核心图像生成函数（Image 2.5），返回图像路径或URL"""
    body = {
        "model": MODEL_IMAGE,
        "prompt": prompt,
        "size": size,
        "ratio": ratio,
    }
    extra = {}
    if image:
        images = [image] if isinstance(image, str) else image
        extra["image"] = images
    if extra:
        body["extra_body"] = extra
    # 注意：Image 2.5 官方参数表不含 seed，传入可能被拒，这里保留参数但不下发

    print("正在生成图像...", file=sys.stderr)
    result = api_request("POST", "/v1/images/generations", body, api_key)

    item = result["data"][0]
    if output and item.get("b64_json"):
        img_bytes = base64.b64decode(item["b64_json"])
        with open(output, "wb") as f:
            f.write(img_bytes)
        print(f"图像已保存: {output}", file=sys.stderr)
        return output
    elif item.get("url"):
        url = item["url"]
        if output:
            try:
                urllib.request.urlretrieve(url, output)
                print(f"图像已下载: {output}", file=sys.stderr)
                return output
            except Exception as e:
                print(f"警告: 下载图像失败: {e}", file=sys.stderr)
        return url
    return None


def generate_video_core(prompt, image=None, seconds="5", size="720P", aspect_ratio="16:9",
                        mode=None, first_frame=None, last_frame=None, images=None,
                        audios=None, videos=None, model=MODEL_VIDEO, seed=None,
                        output=None, api_key=None):
    """核心视频生成函数（Video 2.5），返回视频路径或URL"""
    seconds = normalize_seconds(seconds)
    size = normalize_size(size)
    if aspect_ratio not in VIDEO_ASPECTS:
        print(f"警告: aspect_ratio {aspect_ratio} 不受支持，回退 16:9", file=sys.stderr)
        aspect_ratio = "16:9"

    # 单图入口视为首帧（keyframe）
    if image:
        img_input = image[0] if isinstance(image, list) else image
        if img_input.startswith(("http://", "https://")):
            first_frame = first_frame or img_input
        else:
            print("检测到本地图片，正在上传...", file=sys.stderr)
            first_frame = first_frame or upload_image_to_url(img_input)

    if not mode:
        if images or audios or videos:
            mode = "reference"
        elif first_frame or last_frame:
            mode = "keyframe"
        else:
            mode = "text"

    body = {
        "model": model,
        "prompt": prompt,
        "mode": mode,
        "seconds": seconds,
        "size": size,
        "aspect_ratio": aspect_ratio,
    }

    if mode == "keyframe":
        if not (first_frame or last_frame):
            print("错误: keyframe 模式需要 first_frame 或 last_frame", file=sys.stderr)
            sys.exit(1)
        if first_frame:
            body["first_frame"] = first_frame
        if last_frame:
            body["last_frame"] = last_frame
    elif mode == "reference":
        if not any([images, audios, videos]):
            print("错误: reference 模式需要 images / audios / videos", file=sys.stderr)
            sys.exit(1)
        if images:
            body["images"] = images
        if audios:
            body["audios"] = audios
        if videos:
            body["videos"] = [v if isinstance(v, dict) else {"url": v} for v in videos]

    if seed is not None:
        body["seed"] = seed

    video_id, model_name = _create_video_task(body, api_key)
    return _poll_video(video_id, model_name, api_key, output)


def concat_videos_core(inputs, output):
    """核心拼接函数"""
    if len(inputs) < 2:
        print("错误: 至少需要 2 个视频文件", file=sys.stderr)
        sys.exit(1)

    # 检查所有输入文件存在
    for f in inputs:
        if not os.path.exists(f):
            print(f"错误: 文件不存在: {f}", file=sys.stderr)
            sys.exit(1)

    # 方案 A: 尝试使用 ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"使用 ffmpeg 拼接 {len(inputs)} 个视频...", file=sys.stderr)
        # 创建文件列表
        list_file = os.path.join(tempfile.gettempdir(), "concat_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for v in inputs:
                safe_path = v.replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{safe_path}'\n")

        cmd = [
            ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
            "-i", list_file, "-c", "copy", output
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            print(f"拼接完成: {output}", file=sys.stderr)
            os.remove(list_file)
            return
        except subprocess.CalledProcessError:
            print(f"ffmpeg concat copy 失败，尝试重编码...", file=sys.stderr)
            cmd2 = [ffmpeg_path, "-y"]
            for v in inputs:
                cmd2.extend(["-i", v])
            cmd2.extend([
                "-filter_complex", f"concat=n={len(inputs)}:v=1:a=0[outv]",
                "-map", "[outv]", output
            ])
            try:
                subprocess.run(cmd2, check=True, capture_output=True, timeout=600)
                print(f"拼接完成（重编码）: {output}", file=sys.stderr)
                os.remove(list_file)
                return
            except subprocess.CalledProcessError as e2:
                print(f"ffmpeg 重编码也失败: {e2}", file=sys.stderr)
        except Exception as e:
            print(f"ffmpeg 执行失败: {e}", file=sys.stderr)

    # 方案 B: 纯 Python MP4 二进制拼接
    print(f"ffmpeg 不可用，使用纯 Python 拼接...", file=sys.stderr)
    _concat_mp4_pure_python(inputs, output)


def _concat_mp4_pure_python(inputs, output):
    """纯 Python MP4 拼接：将多个 MP4 文件的 mdat 数据合并到一个容器中"""
    with open(inputs[0], "rb") as f:
        data = f.read()

    # 找到 ftyp box
    ftyp_size = struct.unpack(">I", data[0:4])[0]
    ftyp_box = data[:ftyp_size]

    # 找到 moov box
    moov_offset = ftyp_size
    while moov_offset < len(data):
        box_size = struct.unpack(">I", data[moov_offset:moov_offset+4])[0]
        box_type = data[moov_offset+4:moov_offset+8]
        if box_type == b"moov":
            moov_box = data[moov_offset:moov_offset+box_size]
            break
        moov_offset += box_size
    else:
        print("错误: 第一个文件中未找到 moov box", file=sys.stderr)
        sys.exit(1)

    # 收集所有文件的 mdat 数据
    mdat_parts = []
    for vfile in inputs:
        with open(vfile, "rb") as f:
            vdata = f.read()
        offset = 0
        while offset < len(vdata):
            box_size = struct.unpack(">I", vdata[offset:offset+4])[0]
            box_type = vdata[offset+4:offset+8]
            if box_type == b"mdat":
                mdat_parts.append(vdata[offset:offset+box_size])
                break
            offset += box_size
        else:
            print(f"警告: 文件 {vfile} 中未找到 mdat box，跳过", file=sys.stderr)

    if not mdat_parts:
        print("错误: 没有有效的 mdat 数据", file=sys.stderr)
        sys.exit(1)

    with open(output, "wb") as f:
        f.write(ftyp_box)
        f.write(moov_box)
        for part in mdat_parts:
            f.write(part)

    print(f"纯 Python 拼接完成: {output} ({len(mdat_parts)} 个片段)", file=sys.stderr)


# ============================================================
# 基本命令的CLI接口
# ============================================================

def cmd_image(args):
    """图像生成命令"""
    result = generate_image_core(
        prompt=args.prompt,
        image=args.image,
        size=args.size,
        ratio=args.ratio,
        output=args.output,
        api_key=args.api_key
    )
    if result and not args.output:
        print(result)


def cmd_video(args):
    """视频生成命令"""
    size = args.size
    seconds = args.seconds

    # 兼容旧参数：width/height → 档位；frames/fps → 秒数
    if getattr(args, "width", None) or getattr(args, "height", None):
        size = legacy_geometry_to_size(args.width, args.height, default=size)
        print(f"提示: --width/--height 已废弃，按 {size} 档处理", file=sys.stderr)
    if getattr(args, "frames", None):
        fps = getattr(args, "fps", None) or 24
        seconds = normalize_seconds(int(round(args.frames / fps)), default=seconds)
        print(f"提示: --frames/--fps 已废弃，按 {seconds} 秒处理", file=sys.stderr)

    result = generate_video_core(
        prompt=args.prompt,
        image=args.image,
        seconds=seconds,
        size=size,
        aspect_ratio=args.aspect_ratio,
        mode=args.mode,
        first_frame=args.first_frame,
        last_frame=args.last_frame,
        model=args.model,
        seed=args.seed,
        output=args.output,
        api_key=args.api_key
    )
    if result:
        print(f"视频 URL: {result}")
    else:
        print("视频生成失败", file=sys.stderr)
        sys.exit(1)


def cmd_concat(args):
    """拼接命令"""
    concat_videos_core(args.inputs, args.output)


# ============================================================
# 复杂命令（由基本命令组合而成）
# ============================================================

def cmd_long_video(args):
    """长视频命令：多次video + concat"""
    segments = args.segments
    seconds = normalize_seconds(args.segment_seconds, default="10")
    size = normalize_size(args.size)
    aspect_ratio = args.aspect_ratio

    print(f"=== 长视频生成 ===", file=sys.stderr)
    print(f"分辨率档位: {size}, 画幅: {aspect_ratio}", file=sys.stderr)
    print(f"分段数: {segments}, 每段 {seconds} 秒 (合计 {int(seconds) * segments} 秒)", file=sys.stderr)

    temp_dir = tempfile.mkdtemp(prefix="agnes_video_")
    segment_files = []

    # 组合：多次调用video核心函数
    for i in range(segments):
        print(f"\n--- 生成第 {i+1}/{segments} 段 ---", file=sys.stderr)
        seg_path = os.path.join(temp_dir, f"segment_{i:03d}.mp4")
        
        video_url = generate_video_core(
            prompt=args.prompt,
            image=args.image,
            seconds=seconds,
            size=size,
            aspect_ratio=aspect_ratio,
            model=args.model,
            seed=args.seed,
            output=seg_path,
            api_key=args.api_key
        )
        
        if video_url and os.path.exists(seg_path):
            segment_files.append(seg_path)
            print(f"第 {i+1} 段完成", file=sys.stderr)
        else:
            print(f"第 {i+1} 段失败，停止生成", file=sys.stderr)
            break

    if len(segment_files) < 2:
        print(f"错误: 只成功生成了 {len(segment_files)} 段，无法拼接", file=sys.stderr)
        sys.exit(1)

    # 组合：调用concat核心函数
    print(f"\n=== 拼接 {len(segment_files)} 个片段 ===", file=sys.stderr)
    concat_videos_core(segment_files, args.output)

    # 清理
    for f in segment_files:
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

    print(f"\n长视频生成完成: {args.output}", file=sys.stderr)


def cmd_images_video(args):
    """批量图片视频命令：多次video + concat"""
    images = args.images
    shared_prompt = args.prompt
    per_prompts = args.prompts
    seconds = normalize_seconds(args.seconds)
    size = normalize_size(args.size)
    aspect_ratio = args.aspect_ratio
    seed = args.seed

    print(f"=== 锚点图片 → 视频 ===", file=sys.stderr)
    print(f"图片数: {len(images)}, 每段 {seconds} 秒, 档位: {size}, 画幅: {aspect_ratio}", file=sys.stderr)

    if per_prompts and len(per_prompts) != len(images):
        print(f"错误: --prompts 数量 ({len(per_prompts)}) 必须与 --images 数量 ({len(images)}) 一致", file=sys.stderr)
        sys.exit(1)

    temp_dir = tempfile.mkdtemp(prefix="agnes_iv_")
    segment_files = []

    # 组合：多次调用video核心函数
    for i, img_path in enumerate(images):
        scene_prompt = per_prompts[i] if per_prompts else shared_prompt

        print(f"\n--- 图片 {i+1}/{len(images)}: {os.path.basename(img_path)} ---", file=sys.stderr)
        print(f"Prompt: {scene_prompt[:60]}...", file=sys.stderr)

        # 处理图片路径
        image_input = None
        if img_path.startswith(("http://", "https://")):
            image_input = img_path
        elif os.path.exists(img_path):
            image_input = img_path
        else:
            print(f"错误: 图片不存在: {img_path}", file=sys.stderr)
            continue

        seg_path = os.path.join(temp_dir, f"seg_{i:03d}.mp4")
        video_url = generate_video_core(
            prompt=scene_prompt,
            image=[image_input] if image_input else None,
            seconds=seconds,
            size=size,
            aspect_ratio=aspect_ratio,
            model=args.model,
            seed=seed,
            output=seg_path,
            api_key=args.api_key
        )

        if video_url and os.path.exists(seg_path):
            segment_files.append(seg_path)
            print(f"图片 {i+1} 视频完成", file=sys.stderr)
        else:
            print(f"图片 {i+1} 视频失败，跳过", file=sys.stderr)

    if not segment_files:
        print("错误: 所有视频都失败了", file=sys.stderr)
        sys.exit(1)

    # 组合：调用concat核心函数
    print(f"\n=== 拼接 {len(segment_files)} 个视频 ===", file=sys.stderr)
    concat_videos_core(segment_files, args.output)

    # 清理
    for f in segment_files:
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

    print(f"\n视频生成完成: {args.output}", file=sys.stderr)


def cmd_story_video(args):
    """故事板视频命令：多次image + 多次video + concat"""
    with open(args.storyboard, "r", encoding="utf-8") as f:
        storyboard = json.load(f)

    scenes = storyboard.get("scenes", [])
    if not scenes:
        print("错误: 故事板中没有 scenes", file=sys.stderr)
        sys.exit(1)

    base_prompt = storyboard.get("base_prompt", "")
    style = storyboard.get("style", "")
    seed = args.seed or storyboard.get("seed")
    anchor_size = storyboard.get("image_size", "2K")
    aspect_ratio = args.aspect_ratio or storyboard.get("aspect_ratio", "16:9")
    size = normalize_size(args.size)

    prefix_parts = []
    if base_prompt:
        prefix_parts.append(base_prompt)
    if style:
        prefix_parts.append(style)
    shared_prefix = ", ".join(prefix_parts) + ", " if prefix_parts else ""

    print(f"=== 故事板视频生成 ===", file=sys.stderr)
    print(f"场景数: {len(scenes)}, 档位: {size}, 画幅: {aspect_ratio}", file=sys.stderr)

    temp_dir = tempfile.mkdtemp(prefix="agnes_story_")

    # === 阶段 1: 批量生成锚点图片（组合：多次image） ===
    print(f"\n=== 阶段 1: 生成锚点图片 ===", file=sys.stderr)
    anchor_images = []

    for i, scene in enumerate(scenes):
        scene_image = scene.get("image")

        # 如果已有图片，直接使用
        if scene_image:
            if scene_image.startswith(("http://", "https://")):
                anchor_images.append(scene_image)
                print(f"场景 {i+1}: 使用已有图片 URL", file=sys.stderr)
            elif os.path.exists(scene_image):
                anchor_images.append(scene_image)
                print(f"场景 {i+1}: 使用本地图片 {scene_image}", file=sys.stderr)
            else:
                print(f"警告: 图片不存在: {scene_image}，将生成新图片", file=sys.stderr)
                scene_image = None

        # 没有图片，调用image核心函数生成
        if not scene_image:
            scene_prompt = scene.get("prompt", "")
            full_prompt = f"{shared_prefix}{scene_prompt}" if shared_prefix else scene_prompt

            print(f"场景 {i+1}: 生成锚点图片...", file=sys.stderr)
            img_path = os.path.join(temp_dir, f"anchor_{i:03d}.png")
            
            result = generate_image_core(
                prompt=full_prompt,
                size=anchor_size,
                ratio=aspect_ratio,
                seed=seed,
                output=img_path,
                api_key=args.api_key
            )
            
            if result and os.path.exists(result):
                anchor_images.append(result)
                print(f"锚点图片已保存: {result}", file=sys.stderr)
            else:
                print(f"警告: 锚点图片生成失败", file=sys.stderr)
                anchor_images.append(None)

    print(f"\n锚点图片准备完成: {len([a for a in anchor_images if a])}/{len(scenes)} 成功", file=sys.stderr)

    # === 阶段 2: 从锚点图片生成视频（组合：多次video） ===
    print(f"\n=== 阶段 2: 生成分段视频 ===", file=sys.stderr)
    segment_files = []

    for i, scene in enumerate(scenes):
        scene_prompt = scene.get("prompt", "")
        scene_seconds = scene.get("seconds")
        if scene_seconds is None and scene.get("frames"):
            # 兼容旧故事板：按 24fps 折算成秒
            scene_seconds = int(round(scene["frames"] / 24))
        scene_seconds = normalize_seconds(scene_seconds, default="5")
        full_prompt = f"{shared_prefix}{scene_prompt}" if shared_prefix else scene_prompt

        print(f"\n场景 {i+1}/{len(scenes)}: {scene_prompt[:40]}...", file=sys.stderr)

        # 准备图片输入
        image_input = None
        anchor = anchor_images[i] if i < len(anchor_images) else None
        if anchor:
            if anchor.startswith(("http://", "https://")):
                image_input = anchor
            elif os.path.exists(anchor):
                image_input = anchor

        seg_path = os.path.join(temp_dir, f"scene_{i:03d}.mp4")
        video_url = generate_video_core(
            prompt=full_prompt,
            image=[image_input] if image_input else None,
            seconds=scene_seconds,
            size=size,
            aspect_ratio=aspect_ratio,
            model=args.model,
            seed=seed,
            output=seg_path,
            api_key=args.api_key
        )

        if video_url and os.path.exists(seg_path):
            segment_files.append(seg_path)
            print(f"场景 {i+1} 完成", file=sys.stderr)
        else:
            print(f"场景 {i+1} 失败，跳过", file=sys.stderr)

    if not segment_files:
        print("错误: 所有场景都失败了", file=sys.stderr)
        sys.exit(1)

    # === 阶段 3: 拼接（组合：concat） ===
    print(f"\n=== 阶段 3: 拼接 {len(segment_files)} 个场景 ===", file=sys.stderr)
    concat_videos_core(segment_files, args.output)

    # 清理
    for f in segment_files + [a for a in anchor_images if a and os.path.exists(a) and temp_dir in a]:
        try:
            os.remove(f)
        except OSError:
            pass
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

    print(f"\n故事板视频生成完成: {args.output}", file=sys.stderr)


def _read_models(path):
    """读取配置台账，兼容 list 与 {"models": [...]} 两种结构"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"警告: 读取 {path} 失败: {e}", file=sys.stderr)
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("models") or data.get("providers") or []
    return []


def load_api_key(model_name):
    """从通用台账读取 API Key（FREE_MODEL_CONFIG 可覆盖默认路径）"""
    env_path = os.environ.get("FREE_MODEL_CONFIG")
    candidates = []
    if env_path:
        candidates.append(env_path)
    candidates.append(os.path.expanduser("~/.free-model-config/models.json"))

    for path in candidates:
        if not os.path.exists(path):
            continue
        for model in _read_models(path):
            mid = model.get("id") or model.get("model") or model.get("name") or ""
            url = model.get("url") or model.get("base_url") or ""
            key = model.get("apiKey") or model.get("api_key")
            if not key:
                continue
            if mid == model_name or (mid and (model_name in mid or mid in model_name)) or "agnes" in url:
                print(f"从 {path} 读取到 API Key", file=sys.stderr)
                return key
    return None


def main():
    parser = argparse.ArgumentParser(description="Agnes AI 多模态生成工具")
    parser.add_argument("--api-key", default=os.environ.get("AGNES_API_KEY"), help="API Key")
    sub = parser.add_subparsers(dest="command", required=True)

    # 基本命令：图像生成
    img = sub.add_parser("image", help="图像生成（基本命令）")
    img.add_argument("--prompt", required=True, help="图像描述")
    img.add_argument("--image", nargs="+", help="输入图片 URL（图生图/多图合成）")
    img.add_argument("--size", default="1K", help="分辨率档位：1K/2K/3K/4K（默认 1K）")
    img.add_argument("--ratio", default="1:1", help="画幅比例，如 16:9（默认 1:1）")
    img.add_argument("--output", "-o", help="输出文件路径")

    # 基本命令：视频生成
    vid = sub.add_parser("video", help="视频生成（基本命令）")
    vid.add_argument("--prompt", required=True, help="视频描述")
    vid.add_argument("--image", nargs="+", help="首帧图片 URL 或本地路径")
    vid.add_argument("--seconds", default="5", help="时长 4-12 秒（默认 5）")
    vid.add_argument("--size", default="720P", help="档位：720P/1080P/1K/2K（默认 720P）")
    vid.add_argument("--aspect-ratio", dest="aspect_ratio", default="16:9", help="画幅（默认 16:9）")
    vid.add_argument("--mode", choices=["text", "keyframe", "reference"], help="生成模式（默认自动判断）")
    vid.add_argument("--first-frame", dest="first_frame", help="keyframe 模式首帧 URL")
    vid.add_argument("--last-frame", dest="last_frame", help="keyframe 模式尾帧 URL")
    vid.add_argument("--model", default=MODEL_VIDEO, help=f"视频模型（默认 {MODEL_VIDEO}）")
    vid.add_argument("--seed", type=int, help="随机种子")
    vid.add_argument("--output", "-o", help="输出视频文件路径")
    # 已废弃参数：仅用于兼容旧脚本
    vid.add_argument("--width", type=int, default=None, help=argparse.SUPPRESS)
    vid.add_argument("--height", type=int, default=None, help=argparse.SUPPRESS)
    vid.add_argument("--frames", type=int, default=None, help=argparse.SUPPRESS)
    vid.add_argument("--fps", type=int, default=None, help=argparse.SUPPRESS)

    # 基本命令：拼接
    cat = sub.add_parser("concat", help="拼接多个视频文件（基本命令）")
    cat.add_argument("--inputs", "-i", nargs="+", required=True, help="输入视频文件列表")
    cat.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：长视频（由video + concat组合）
    long = sub.add_parser("long-video", help="同 prompt 自动分段长视频（= video × N + concat）")
    long.add_argument("--prompt", required=True, help="视频描述")
    long.add_argument("--image", nargs="+", help="首帧图片 URL 或本地路径")
    long.add_argument("--segments", type=int, required=True, help="分段数量")
    long.add_argument("--segment-seconds", dest="segment_seconds", default="10", help="每段时长 4-12 秒（默认 10）")
    long.add_argument("--size", default="720P", help="档位（默认 720P）")
    long.add_argument("--aspect-ratio", dest="aspect_ratio", default="16:9", help="画幅（默认 16:9）")
    long.add_argument("--model", default=MODEL_VIDEO, help=f"视频模型（默认 {MODEL_VIDEO}）")
    long.add_argument("--seed", type=int, help="随机种子")
    long.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：批量图片视频（由video + concat组合）
    iv = sub.add_parser("images-video", help="批量图 → 批量视频 → 拼接（= video × N + concat）")
    iv.add_argument("--images", "-i", nargs="+", required=True, help="锚点图片列表（逐张作为首帧）")
    iv.add_argument("--prompt", required=True, help="视频描述（所有图片共享）")
    iv.add_argument("--prompts", nargs="+", help="每张图片的独立描述（可选）")
    iv.add_argument("--seconds", default="5", help="每段时长 4-12 秒（默认 5）")
    iv.add_argument("--size", default="720P", help="档位（默认 720P）")
    iv.add_argument("--aspect-ratio", dest="aspect_ratio", default="16:9", help="画幅（默认 16:9）")
    iv.add_argument("--model", default=MODEL_VIDEO, help=f"视频模型（默认 {MODEL_VIDEO}）")
    iv.add_argument("--seed", type=int, help="随机种子")
    iv.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：故事板视频（由image + video + concat组合）
    story = sub.add_parser("story-video", help="故事板全流程（= image × N + video × N + concat）")
    story.add_argument("--storyboard", "-s", required=True, help="故事板 JSON 文件路径")
    story.add_argument("--size", default="720P", help="视频档位（默认 720P）")
    story.add_argument("--aspect-ratio", dest="aspect_ratio", default="16:9", help="画幅（默认 16:9）")
    story.add_argument("--model", default=MODEL_VIDEO, help=f"视频模型（默认 {MODEL_VIDEO}）")
    story.add_argument("--seed", type=int, help="随机种子")
    story.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    args = parser.parse_args()

    # concat 不需要 API Key
    if args.command == "concat":
        cmd_concat(args)
        return

    # 其他命令需要 API Key
    if not args.api_key:
        api_key = load_api_key(MODEL_TEXT)
        if api_key:
            args.api_key = api_key
        else:
            print("错误: 未提供 AGNES_API_KEY。以下任一方式均可：", file=sys.stderr)
            print("  1. 命令行参数: --api-key YOUR_KEY", file=sys.stderr)
            print("  2. 环境变量: export AGNES_API_KEY=YOUR_KEY", file=sys.stderr)
            print("  3. 通用台账: ~/.free-model-config/models.json（FREE_MODEL_CONFIG 可覆盖）", file=sys.stderr)
            sys.exit(1)

    # 分发到对应命令
    if args.command == "image":
        cmd_image(args)
    elif args.command == "video":
        cmd_video(args)
    elif args.command == "long-video":
        cmd_long_video(args)
    elif args.command == "images-video":
        cmd_images_video(args)
    elif args.command == "story-video":
        cmd_story_video(args)


if __name__ == "__main__":
    main()
