#!/usr/bin/env python3
"""
Agnes AI 多模态生成工具（图像/视频）。

架构：基本命令组合复杂命令
- 基本命令：image、video、concat
- 复杂命令：long-video、images-video、story-video（由基本命令组合而成）

用法:
  # 基本命令
  python agnes_gen.py image --prompt "描述" [--size 1024x768] [--output result.png]
  python agnes_gen.py video --prompt "描述" [--width 1152] [--height 768] [--frames 121] [--fps 24]
  python agnes_gen.py concat --inputs a.mp4 b.mp4 c.mp4 --output long.mp4

  # 复杂命令（由基本命令组合）
  python agnes_gen.py long-video --prompt "描述" --segments 3 --output long.mp4
  python agnes_gen.py images-video --images img1.png img2.png --prompt "描述" --output result.mp4
  python agnes_gen.py story-video --storyboard storyboard.json --output story.mp4

环境变量:
  AGNES_API_KEY  - API 密钥（可选，优先从 ~/.workbuddy/models.json 读取）
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

# 帧数限制表：(分辨率描述, 宽, 高, 最大帧数)
FRAME_LIMITS = [
    ("1080p", 1920, 1080, 169),
    ("1080p", 1920, 1200, 169),
    ("720p",  1088, 832,  409),
    ("720p",  1280, 720,  409),
    ("480p",  854,  480,  961),
    ("480p",  640,  480,  961),
]


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


def _poll_video(task_id, api_key, output_path=None):
    """轮询视频任务状态，返回视频 URL"""
    print(f"等待视频生成（轮询间隔 10 秒）...", file=sys.stderr)
    while True:
        time.sleep(10)
        status_result = api_request("GET", f"/v1/videos/{task_id}", api_key=api_key, timeout=30, exit_on_error=False)
        if not status_result:
            print("轮询请求失败，重试...", file=sys.stderr)
            continue
        status = status_result.get("status", "unknown")
        progress = status_result.get("progress", 0)
        print(f"状态: {status} ({progress}%)", file=sys.stderr)

        if status == "completed":
            video_url = ""
            for k in ["url", "video_url", "result", "output", "video", "remixed_from_video_id"]:
                val = status_result.get(k)
                if val and isinstance(val, str) and val.startswith("http"):
                    video_url = val
                    break
            if not video_url:
                result_data = status_result.get("result", {})
                if isinstance(result_data, dict):
                    for k in ["url", "video_url", "output", "video"]:
                        val = result_data.get(k)
                        if val and isinstance(val, str) and val.startswith("http"):
                            video_url = val
                            break
            if not video_url:
                result_data = status_result.get("result", {})
                if isinstance(result_data, str) and result_data.startswith("http"):
                    video_url = result_data
            if output_path and video_url:
                urllib.request.urlretrieve(video_url, output_path)
                print(f"视频已下载: {output_path}", file=sys.stderr)
            return video_url
        elif status == "failed":
            error = status_result.get("error", "未知错误")
            print(f"视频生成失败: {error}", file=sys.stderr)
            return None


def _create_video_task(args_dict, api_key):
    """创建视频生成任务，返回 task_id"""
    print("正在创建视频任务...", file=sys.stderr)
    result = api_request("POST", "/v1/videos", args_dict, api_key, timeout=600)
    task_id = result.get("task_id") or result.get("id")
    seconds = result.get("seconds", "unknown")
    size = result.get("size", "unknown")
    print(f"任务已创建: task_id={task_id}, 时长={seconds}秒, 分辨率={size}", file=sys.stderr)
    return task_id


def get_max_frames(width, height):
    """根据分辨率确定最大帧数"""
    for _, w, h, mf in FRAME_LIMITS:
        if width <= w and height <= h:
            return mf
    return 121  # 默认


# ============================================================
# 基本命令（原子操作）
# ============================================================

def generate_image_core(prompt, image=None, size="1024x768", seed=None, output=None, api_key=None):
    """核心图像生成函数，返回图像路径或URL"""
    body = {
        "model": "agnes-image-2.0-flash",
        "prompt": prompt,
        "size": size,
    }
    extra = {}
    if image:
        images = [image] if isinstance(image, str) else image
        extra["image"] = images
    if extra:
        body["extra_body"] = extra
    if seed is not None:
        body["seed"] = seed

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


def generate_video_core(prompt, image=None, width=1152, height=768, frames=121, fps=24, 
                       seed=None, negative_prompt=None, output=None, api_key=None):
    """核心视频生成函数，返回视频路径或URL"""
    # 处理本地图片
    image_url = None
    if image:
        img_input = image[0] if isinstance(image, list) else image
        if img_input.startswith(("http://", "https://")):
            image_url = img_input
        else:
            print(f"检测到本地图片，正在上传...", file=sys.stderr)
            image_url = upload_image_to_url(img_input)

    body = {
        "model": "agnes-video-v2.0",
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_frames": frames,
        "frame_rate": fps,
    }
    if image_url:
        body["image"] = image_url
    if seed is not None:
        body["seed"] = seed
    if negative_prompt:
        body["negative_prompt"] = negative_prompt

    task_id = _create_video_task(body, api_key)
    video_url = _poll_video(task_id, api_key, output)
    return video_url


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
        output=args.output,
        api_key=args.api_key
    )
    if result and not args.output:
        print(result)


def cmd_video(args):
    """视频生成命令"""
    result = generate_video_core(
        prompt=args.prompt,
        image=args.image,
        width=args.width,
        height=args.height,
        frames=args.frames,
        fps=args.fps,
        seed=args.seed,
        negative_prompt=args.negative_prompt,
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
    width = args.width
    height = args.height
    fps = args.fps
    segments = args.segments
    max_frames = get_max_frames(width, height)

    print(f"=== 长视频生成 ===", file=sys.stderr)
    print(f"分辨率: {width}x{height}, 帧率: {fps}fps", file=sys.stderr)
    print(f"分段数: {segments}, 每段 {max_frames} 帧 ({max_frames/fps:.1f}秒)", file=sys.stderr)

    temp_dir = tempfile.mkdtemp(prefix="agnes_video_")
    segment_files = []

    # 组合：多次调用video核心函数
    for i in range(segments):
        print(f"\n--- 生成第 {i+1}/{segments} 段 ---", file=sys.stderr)
        seg_path = os.path.join(temp_dir, f"segment_{i:03d}.mp4")
        
        video_url = generate_video_core(
            prompt=args.prompt,
            image=args.image,
            width=width,
            height=height,
            frames=max_frames,
            fps=fps,
            seed=args.seed,
            negative_prompt=args.negative_prompt,
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
    width = args.width
    height = args.height
    fps = args.fps
    seed = args.seed

    max_frames = get_max_frames(width, height)
    frames = args.frames if args.frames > 0 else max_frames

    print(f"=== 锚点图片 → 视频 ===", file=sys.stderr)
    print(f"图片数: {len(images)}, 每段 {frames} 帧, 分辨率: {width}x{height}", file=sys.stderr)

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
            width=width,
            height=height,
            frames=frames,
            fps=fps,
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
    anchor_size = storyboard.get("image_size", "1024x768")
    width = args.width
    height = args.height
    fps = args.fps

    prefix_parts = []
    if base_prompt:
        prefix_parts.append(base_prompt)
    if style:
        prefix_parts.append(style)
    shared_prefix = ", ".join(prefix_parts) + ", " if prefix_parts else ""

    max_frames = get_max_frames(width, height)

    print(f"=== 故事板视频生成 ===", file=sys.stderr)
    print(f"场景数: {len(scenes)}, 分辨率: {width}x{height}", file=sys.stderr)

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
        scene_frames = scene.get("frames", max_frames)
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
            width=width,
            height=height,
            frames=min(scene_frames, max_frames),
            fps=fps,
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


def load_api_key_from_models(model_name):
    """从 ~/.workbuddy/models.json 文件中读取 API Key"""
    try:
        models_path = os.path.expanduser("~/.workbuddy/models.json")
        if not os.path.exists(models_path):
            return None
        
        with open(models_path, "r", encoding="utf-8") as f:
            models = json.load(f)
        
        for model in models:
            if model.get("id") == model_name or model.get("name") == model_name:
                return model.get("apiKey")
        
        for model in models:
            model_id = model.get("id", "")
            if model_name in model_id or model_id in model_name:
                return model.get("apiKey")
        
        return None
    except Exception as e:
        print(f"警告: 读取 models.json 失败: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Agnes AI 多模态生成工具")
    parser.add_argument("--api-key", default=os.environ.get("AGNES_API_KEY"), help="API Key")
    sub = parser.add_subparsers(dest="command", required=True)

    # 基本命令：图像生成
    img = sub.add_parser("image", help="图像生成（基本命令）")
    img.add_argument("--prompt", required=True, help="图像描述")
    img.add_argument("--image", nargs="+", help="输入图片 URL（图生图）")
    img.add_argument("--size", default="1024x768", help="分辨率，如 1024x768")
    img.add_argument("--output", "-o", help="输出文件路径")

    # 基本命令：视频生成
    vid = sub.add_parser("video", help="视频生成（基本命令）")
    vid.add_argument("--prompt", required=True, help="视频描述")
    vid.add_argument("--image", nargs="+", help="输入图片 URL 或本地路径（图生视频）")
    vid.add_argument("--width", type=int, default=1152, help="视频宽度")
    vid.add_argument("--height", type=int, default=768, help="视频高度")
    vid.add_argument("--frames", type=int, default=121, help="总帧数（8n+1）")
    vid.add_argument("--fps", type=int, default=24, help="帧率 1-60")
    vid.add_argument("--seed", type=int, help="随机种子")
    vid.add_argument("--negative-prompt", dest="negative_prompt", help="负面提示词")
    vid.add_argument("--output", "-o", help="输出视频文件路径")

    # 基本命令：拼接
    cat = sub.add_parser("concat", help="拼接多个视频文件（基本命令）")
    cat.add_argument("--inputs", "-i", nargs="+", required=True, help="输入视频文件列表")
    cat.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：长视频（由video + concat组合）
    long = sub.add_parser("long-video", help="同 prompt 自动分段长视频（= video × N + concat）")
    long.add_argument("--prompt", required=True, help="视频描述")
    long.add_argument("--image", nargs="+", help="输入图片 URL 或本地路径")
    long.add_argument("--width", type=int, default=1088, help="视频宽度")
    long.add_argument("--height", type=int, default=832, help="视频高度")
    long.add_argument("--fps", type=int, default=24, help="帧率 1-60")
    long.add_argument("--segments", type=int, required=True, help="分段数量")
    long.add_argument("--seed", type=int, help="随机种子")
    long.add_argument("--negative-prompt", dest="negative_prompt", help="负面提示词")
    long.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：批量图片视频（由video + concat组合）
    iv = sub.add_parser("images-video", help="批量图 → 批量视频 → 拼接（= video × N + concat）")
    iv.add_argument("--images", "-i", nargs="+", required=True, help="锚点图片列表")
    iv.add_argument("--prompt", required=True, help="视频描述（所有图片共享）")
    iv.add_argument("--prompts", nargs="+", help="每张图片的独立描述（可选）")
    iv.add_argument("--width", type=int, default=1088, help="视频宽度")
    iv.add_argument("--height", type=int, default=832, help="视频高度")
    iv.add_argument("--fps", type=int, default=24, help="帧率 1-60")
    iv.add_argument("--frames", type=int, default=0, help="每段帧数（0=自动使用最大值）")
    iv.add_argument("--seed", type=int, help="随机种子")
    iv.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    # 复杂命令：故事板视频（由image + video + concat组合）
    story = sub.add_parser("story-video", help="故事板全流程（= image × N + video × N + concat）")
    story.add_argument("--storyboard", "-s", required=True, help="故事板 JSON 文件路径")
    story.add_argument("--width", type=int, default=1088, help="视频宽度")
    story.add_argument("--height", type=int, default=832, help="视频高度")
    story.add_argument("--fps", type=int, default=24, help="帧率 1-60")
    story.add_argument("--seed", type=int, help="随机种子")
    story.add_argument("--output", "-o", required=True, help="输出视频文件路径")

    args = parser.parse_args()

    # concat 不需要 API Key
    if args.command == "concat":
        cmd_concat(args)
        return

    # 其他命令需要 API Key
    if not args.api_key:
        model_name = "agnes-2.0-flash"
        api_key = load_api_key_from_models(model_name)
        if api_key:
            args.api_key = api_key
            print(f"从 ~/.workbuddy/models.json 读取到 API Key", file=sys.stderr)
        else:
            print("错误: 未设置 AGNES_API_KEY。请通过以下方式之一提供：", file=sys.stderr)
            print("  1. 命令行参数: --api-key YOUR_KEY", file=sys.stderr)
            print("  2. 环境变量: export AGNES_API_KEY=YOUR_KEY", file=sys.stderr)
            print("  3. 配置文件: ~/.workbuddy/models.json 中对应模型的 apiKey 字段", file=sys.stderr)
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
