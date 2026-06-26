#!/usr/bin/env python3
"""
动漫短剧生成系统 - Anime Drama Pipeline v2
小说原文 → 分镜脚本 → 文生图 → 图生视频 → 配音合成 → 最终成片

API配置:
  - RH API Key: 从环境变量 RUNNINGHUB_API_KEY 读取（请勿硬编码）
  - 文生图 App ID: 从环境变量 RH_IMAGE_APP_ID 读取，默认为 YOUR_IMAGE_APP_ID 占位符
  - 图生视频 App ID: 从环境变量 RH_VIDEO_APP_ID 读取，默认为 YOUR_VIDEO_APP_ID 占位符

使用方法:
  python3 anime_drama_pipeline.py <小说原文文件> [输出目录]
"""

import json
import subprocess
import sys
import time
import os
import re
import tempfile
from pathlib import Path

# ============ 配置 ============
# RH API Key: 从环境变量 RUNNINGHUB_API_KEY 读取，请勿硬编码
API_KEY = os.environ.get("RUNNINGHUB_API_KEY", "")
if not API_KEY:
    print("Error: 请设置环境变量 RUNNINGHUB_API_KEY")
    sys.exit(1)

# RH AI 应用 AppID（请替换为你的）
IMG_APP_ID = os.environ.get("RH_IMAGE_APP_ID", "YOUR_IMAGE_APP_ID")   # 文生图
VID_APP_ID = os.environ.get("RH_VIDEO_APP_ID", "YOUR_VIDEO_APP_ID")   # 图生视频
RH_SCRIPT_APP = "~/.openclaw/workspace/skills/runninghub/scripts/runninghub_app.py"
WORKSPACE = Path.home() / "anime-drama-workspace"
VIDEO_DURATION = "5"  # 秒

# ============ 工具函数 ============

def run(cmd, timeout=300, check=True):
    """执行shell命令"""
    print(f"[CMD] {cmd}", file=sys.stderr)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0 and check:
        print(f"[ERROR] stdout: {result.stdout}", file=sys.stderr)
        print(f"[ERROR] stderr: {result.stderr}", file=sys.stderr)
        return result
    return result

def rh_check():
    """检查API状态"""
    result = run(f"python3 {RH_SCRIPT_APP} --check --api-key {API_KEY}", timeout=20, check=False)
    try:
        data = json.loads(result.stdout)
        print(f"[RunningHub] 余额: ¥{data.get('balance','?')} | 状态: {data.get('status','?')}", file=sys.stderr)
        return data.get("status") == "ready"
    except:
        print(f"[ERROR] API检查失败", file=sys.stderr)
        return False

def upload_to_runninghub(file_path):
    """上传文件到RunningHub，返回fileName"""
    url = "https://www.runninghub.cn/task/openapi/upload"
    cmd = [
        "curl", "-s", "-S", "--fail-with-body", "-X", "POST", url,
        "--max-time", "120",
        "-H", "Host: www.runninghub.cn",
        "-F", f"apiKey={API_KEY}",
        "-F", "fileType=input",
        "-F", f"file=@{file_path}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] 上传失败: {result.stderr}", file=sys.stderr)
        return None
    try:
        resp = json.loads(result.stdout)
        if resp.get("code") == 0:
            return resp["data"]["fileName"]
        print(f"[ERROR] 上传失败: {resp}", file=sys.stderr)
    except:
        print(f"[ERROR] 上传解析失败: {result.stdout}", file=sys.stderr)
    return None

def rh_image(prompt, output_path, aspect="9:16"):
    """文生图 - 调用AI应用"""
    # 增强prompt，加入风格和质量要求
    enhanced_prompt = (
        f"Anime cinematic scene: {prompt}, "
        f"high quality anime art style, dramatic lighting, "
        f"vibrant colors, detailed background, anime key visual, 4K"
    )
    
    cmd = (
        f"python3 {RH_SCRIPT_APP} "
        f"--run {IMG_APP_ID} "
        f'--node "12:value={enhanced_prompt}" '
        f'-o {output_path} '
        f"--api-key {API_KEY}"
    )
    result = run(cmd, timeout=300, check=False)
    
    # 解析输出找文件路径
    for line in (result.stdout + result.stderr).split("\n"):
        if line.startswith("OUTPUT_FILE:"):
            return line.split("OUTPUT_FILE:")[1].strip()
    
    # 检查是否有错误
    for line in (result.stdout + result.stderr).split("\n"):
        if "error" in line.lower() or "failed" in line.lower():
            print(f"[WARN] {line}", file=sys.stderr)
    return None

def rh_video(image_path, prompt, output_path, duration="5"):
    """图生视频 - 调用AI应用"""
    # 先上传图片
    print(f"[UPLOAD] 上传图片: {image_path}", file=sys.stderr)
    file_name = upload_to_runninghub(image_path)
    if not file_name:
        print(f"[ERROR] 图片上传失败", file=sys.stderr)
        return None
    
    # 增强视频prompt
    enhanced_prompt = (
        f"{prompt}, subtle camera movement, cinematic anime style, "
        f"smooth motion, dramatic lighting, 4K"
    )
    
    cmd = (
        f"python3 {RH_SCRIPT_APP} "
        f"--run {VID_APP_ID} "
        f'--node "325:value={enhanced_prompt}" '
        f'--node "269:image={file_name}" '
        f'-o {output_path} '
        f"--api-key {API_KEY}"
    )
    result = run(cmd, timeout=600, check=False)
    
    # 解析输出找文件路径
    for line in (result.stdout + result.stderr).split("\n"):
        if line.startswith("OUTPUT_FILE:"):
            return line.split("OUTPUT_FILE:")[1].strip()
    
    # 检查是否有错误
    for line in (result.stdout + result.stderr).split("\n"):
        if "error" in line.lower() or "failed" in line.lower():
            print(f"[WARN] {line}", file=sys.stderr)
    return None

def parse_story(story_text):
    """将小说原文解析为分镜列表"""
    shots = []
    paragraphs = [p.strip() for p in story_text.split("\n") if p.strip()]
    for i, para in enumerate(paragraphs):
        shots.append({
            "id": i + 1,
            "description": para,
            "duration": VIDEO_DURATION,
            "image_prompt": para,
            "video_prompt": para
        })
    return shots

def assemble_video(shot_videos, output_path):
    """使用ffmpeg合并所有镜头"""
    print(f"[INFO] 合并 {len(shot_videos)} 个镜头为最终视频...", file=sys.stderr)
    
    list_file = WORKSPACE / "video_list.txt"
    with open(list_file, "w") as f:
        for video in shot_videos:
            f.write(f"file '{video}'\n")
    
    cmd = (
        f"ffmpeg -y -f concat -safe 0 -i {list_file} "
        f"-c:v libx264 -pix_fmt yuv420p -vf \"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black\" "
        f"{output_path}"
    )
    
    result = run(cmd, timeout=120, check=False)
    if result.returncode != 0:
        print(f"[ERROR] 合并失败: {result.stderr}", file=sys.stderr)
        return False
    return True

# ============ 主流程 ============

def main(story_text, output_dir=None):
    if not output_dir:
        output_dir = WORKSPACE / f"project_{int(time.time())}"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[START] 动漫短剧生成 pipeline", file=sys.stderr)
    print(f"[INFO] 工作目录: {output_dir}", file=sys.stderr)
    
    # Step 1: 检查API状态
    if not rh_check():
        print("[ERROR] RunningHub API 不可用", file=sys.stderr)
        sys.exit(1)
    
    # Step 2: 生成分镜脚本
    shots = parse_story(story_text)
    print(f"[INFO] 生成了 {len(shots)} 个镜头", file=sys.stderr)
    
    # 保存分镜脚本
    script_path = output_dir / "shot_script.json"
    with open(script_path, "w") as f:
        json.dump(shots, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 分镜脚本已保存: {script_path}", file=sys.stderr)
    
    # Step 3: 逐个生成图片和视频
    images = {}
    videos = {}
    
    for shot in shots:
        shot_id = shot["id"]
        print(f"\n[{shot_id}/{len(shots)}] 处理镜头: {shot['description'][:40]}...", file=sys.stderr)
        
        # 文生图
        img_path = output_dir / f"shot_{shot_id:03d}_img.png"
        print(f"[IMG] 生成图片中...", file=sys.stderr)
        img_result = rh_image(shot["image_prompt"], str(img_path))
        
        if img_result and Path(img_result).exists():
            images[shot_id] = img_result
            print(f"[OK] 图片完成: {img_result}", file=sys.stderr)
        else:
            print(f"[WARN] 图片生成失败，跳过", file=sys.stderr)
            continue
        
        # 图生视频
        vid_path = output_dir / f"shot_{shot_id:03d}_vid.mp4"
        print(f"[VID] 生成视频中... (约需2-5分钟)", file=sys.stderr)
        vid_result = rh_video(images[shot_id], shot["video_prompt"], str(vid_path))
        
        if vid_result and Path(vid_result).exists():
            videos[shot_id] = vid_result
            print(f"[OK] 视频完成: {vid_result}", file=sys.stderr)
        else:
            print(f"[WARN] 视频生成失败，跳过", file=sys.stderr)
        
        # 避免API过载
        time.sleep(3)
    
    # Step 4: 合并最终视频
    if videos:
        ordered_videos = [videos[shots[i]["id"]] for i in range(len(shots)) if shots[i]["id"] in videos]
        final_output = output_dir / "final_drama.mp4"
        
        if assemble_video(ordered_videos, str(final_output)):
            print(f"\n[DONE] 动漫短剧生成完成！", file=sys.stderr)
            print(f"[FILE] {final_output}", file=sys.stderr)
            
            # 输出摘要
            total_duration = len(ordered_videos) * int(VIDEO_DURATION)
            print(f"[STATS] 镜头数: {len(ordered_videos)} | 总时长: {total_duration}秒", file=sys.stderr)
            return str(final_output)
    else:
        print("[ERROR] 没有生成任何视频", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 anime_drama_pipeline.py <小说原文文件> [输出目录]")
        sys.exit(1)
    
    story_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    with open(story_file, "r") as f:
        story_text = f.read()
    
    main(story_text, output_dir)
