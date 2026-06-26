#!/usr/bin/env python3
"""
抖音视频去重工具 v3
功能：下载 → 去水印 → 深度混剪去重 → 去声音 → 输出
"""

import subprocess
import random
import uuid
import os
import sys
import re
import json
import shutil
from pathlib import Path

# ============ 配置 ============
WORKSPACE = Path("~/video-dedup/workspace").expanduser()
OUTPUT = Path("~/video-dedup/output").expanduser()
WORKSPACE.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

# 去重参数（全部可配置）
MIN_SEGMENTS = 2       # 最少片段数
MAX_SEGMENTS = 3       # 最多片段数
TARGET_DURATION = 12.0  # 目标时长（秒）
MAX_DURATION = 15.0    # 绝对上限
SPEED_RANGE = (0.9, 1.1)
SCALE_RANGE = (0.95, 0.99)
MIRROR_PROB = 0.3
GAMMA_RANGE = (0.95, 1.05)
NOISE_PROB = 0.2
SATURATION_RANGE = (0.85, 1.15)
CONTRAST_RANGE = (0.90, 1.10)
HUE_SHIFT_RANGE = (-5, 5)
FILTER_PROB = 0.4
FRAME_DROP_PROB = 0.25
MIN_FILE_SIZE_KB = 100  # 下载质量校验：最小文件大小


def get_next_output_path() -> Path:
    """获取下一个可用的输出文件路径，按日期+序号命名"""
    import time
    today = time.strftime("%Y-%m-%d")
    existing = list(OUTPUT.glob(f"dedup_{today}_*.mp4"))
    seqs = []
    for f in existing:
        try:
            seq = int(f.stem.split('_')[-1])
            seqs.append(seq)
        except ValueError:
            pass
    next_seq = max(seqs) + 1 if seqs else 1
    return OUTPUT / f"dedup_{today}_{next_seq:02d}.mp4"


def run_cmd(cmd: list, desc: str = "") -> str:
    """执行命令"""
    print(f"[RUN] {desc or ' '.join(cmd[:3])}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {desc} failed:\n{result.stderr[-800:]}")
        raise RuntimeError(f"{desc} failed")
    return result.stdout


def get_video_info(video_path: str) -> dict:
    """获取视频信息（时长、分辨率等），一次 ffprobe 搞定"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=width,height,codec_name",
        "-of", "json", str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    fmt = data.get("format", {})
    streams = data.get("streams", [{}])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    return {
        "duration": float(fmt.get("duration", 0)),
        "width": int(video_stream.get("width", 0)),
        "height": int(video_stream.get("height", 0)),
        "size": int(fmt.get("size", 0)),
    }


def extract_video_id(url: str) -> str:
    """从抖音链接提取视频ID"""
    if "v.douyin.com" in url:
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                "Method": "HEAD"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                real_url = resp.url
                if real_url:
                    match = re.search(r'/video/(\d+)', real_url)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"[WARN] 重定向解析失败: {e}")
    
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    return None


def fetch_no_watermark_url(video_id: str) -> str:
    """从抖音页面获取无水印视频URL（iesdouyin.com 方式，不需要登录）"""
    import urllib.request
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    }
    req = urllib.request.Request(share_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode()
    
    # 提取视频 URI
    video_uri_match = re.search(r'"uri":"(v[0-9a-zA-Z]+)"', content)
    if not video_uri_match:
        raise RuntimeError("无法解析视频URI")
    video_uri = video_uri_match.group(1)
    
    # 优先无水印，无水印失败则用有水印
    no_wm = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={video_uri}&ratio=720p&line=0"
    wm = f"https://aweme.snssdk.com/aweme/v1/playwm/?video_id={video_uri}&ratio=720p&line=0"
    
    for candidate in [no_wm, wm]:
        try:
            req = urllib.request.Request(candidate, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200 and r.headers.get("content-type", "").startswith("video/"):
                    return candidate
        except Exception:
            continue
    return wm


def download_with_ytdlp(url: str, output_path: Path) -> bool:
    """用 yt-dlp 下载视频（备用，需要 cookie）"""
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"无法从URL提取视频ID: {url}")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]/best[ext=mp4]/best",
        "--no-playlist", "--quiet", "--no-warnings",
        "-o", str(output_path),
        url,
    ]
    run_cmd(cmd, f"yt-dlp 下载 {video_id}")
    return True


def download_video(url: str, output_path: Path) -> bool:
    """下载视频：优先直接抓取（免登录），备用 yt-dlp"""
    import urllib.request
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"无法从URL提取视频ID")
    
    try:
        video_url = fetch_no_watermark_url(video_id)
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        }
        req = urllib.request.Request(video_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
        print(f"[OK] 直接下载成功")
        return True
    except Exception as e:
        print(f"[WARN] 直接下载失败: {e}")
        print(f"[INFO] 尝试 yt-dlp...")
        try:
            download_with_ytdlp(url, output_path)
            return True
        except RuntimeError:
            raise RuntimeError("下载失败，请检查网络或提供登录cookie")


def validate_download(file_path: Path) -> bool:
    """检查下载文件是否完整有效"""
    if not file_path.exists():
        return False
    size_kb = file_path.stat().st_size // 1024
    if size_kb < MIN_FILE_SIZE_KB:
        print(f"[WARN] 文件过小 ({size_kb}KB)，可能下载不完整")
        return False
    try:
        info = get_video_info(str(file_path))
        if info["duration"] <= 0:
            print(f"[WARN] 视频时长异常")
            return False
        print(f"[OK] 文件完整 ({info['size']//1024}KB, {info['duration']:.1f}s, {info['width']}x{info['height']})")
        return True
    except Exception as e:
        print(f"[WARN] 视频校验失败: {e}")
        return False


def create_and_shuffle_segments(video_path: str, output_dir: Path) -> list:
    """
    核心去重逻辑：
    1. 视频 <= MAX_DURATION：直接切成 3-6 个片段打乱顺序
    2. 视频 > MAX_DURATION：从随机位置截取 MAX_DURATION，再切成 3-6 个片段打乱
    所有片段都会应用基础画面处理（缩放裁剪）
    """
    info = get_video_info(video_path)
    duration = info["duration"]
    
    # 确定要处理的视频区间
    if duration > MAX_DURATION:
        start = random.uniform(0, duration - MAX_DURATION)
        trimmed = output_dir / f"trimmed_{uuid.uuid4().hex[:8]}.mp4"
        cmd = [
            "ffmpeg", "-y", "-ss", str(start), "-i", str(video_path),
            "-t", str(MAX_DURATION),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            str(trimmed)
        ]
        run_cmd(cmd, f"截取前{MAX_DURATION}秒 (从{start:.1f}s起)")
        video_to_split = trimmed
        actual_duration = MAX_DURATION
    else:
        trimmed = None
        video_to_split = video_path
        actual_duration = duration
    
    # 决定片段数量（所有片段均分视频，长度统一）
    num_segments = random.randint(MIN_SEGMENTS, MAX_SEGMENTS)
    segment_length = actual_duration / num_segments
    
    # 生成片段（打乱前先给个基础缩放统一分辨率）
    trim_start = 0.08
    trim_end = 0.08
    segments = []
    for i in range(num_segments):
        seg_file = output_dir / f"seg_{i}_{uuid.uuid4().hex[:8]}.mp4"
        seg_start = i * segment_length
        
        # 确保裁完首尾后至少剩0.5秒
        seg_len_raw = segment_length - trim_start - trim_end
        if seg_len_raw < 0.5:
            # 太短了，减少裁剪量
            trim_start = 0.02
            trim_end = 0.02
            seg_len_raw = segment_length - trim_start - trim_end
        
        # 基础处理：统一分辨率
        vf_filters = ["scale=1080:1920"]
        
        vf_string = ",".join(vf_filters)
        cmd = [
            "ffmpeg", "-y", "-ss", str(seg_start + trim_start), "-i", str(video_to_split),
            "-t", str(seg_len_raw),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-vf", vf_string,
            str(seg_file)
        ]
        run_cmd(cmd, f"截取片段 {i+1}/{num_segments} ({seg_start:.1f}s, 裁首尾{trim_start}s)")
        
        # 检查实际输出时长，太短则跳过
        info = get_video_info(str(seg_file))
        if info["duration"] < 0.3:
            print(f"[WARN] 片段 {i+1} 太短({info['duration']:.1f}s)，跳过")
            seg_file.unlink()
            continue
        
        segments.append(seg_file)
    
    # 如果片段太少（<2个），重新从原始视频截取
    if len(segments) < 2:
        print(f"[WARN] 片段不足，重新生成...")
        segments = []
        for i in range(max(2, num_segments)):
            seg_file = output_dir / f"seg_{i}_{uuid.uuid4().hex[:8]}.mp4"
            seg_start = i * (actual_duration / max(2, num_segments))
            seg_len = (actual_duration / max(2, num_segments)) - trim_start - trim_end
            if seg_start + trim_start + seg_len > actual_duration:
                seg_len = actual_duration - seg_start - trim_start
            if seg_len < 0.5:
                continue
            cmd = [
                "ffmpeg", "-y", "-ss", str(seg_start + trim_start), "-i", str(video_to_split),
                "-t", str(seg_len),
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-vf", "scale=1080:1920",
                str(seg_file)
            ]
            run_cmd(cmd, f"重新截取片段 {i+1} ({seg_start:.1f}s, {seg_len:.1f}s)")
            segments.append(seg_file)
    
    # 保持原始顺序，不打乱
    print(f"[OK] 生成 {len(segments)} 个片段，保持原始顺序")
    
    # 清理截取后的临时视频
    if trimmed and trimmed.exists():
        trimmed.unlink()
    
    return segments


def apply_dedup_effects(segment_path: Path, output_dir: Path) -> Path:
    """应用去重效果（缩放+镜像+调色+噪点+变速），同时完成音频处理"""
    output_file = output_dir / f"eff_{uuid.uuid4().hex[:8]}.mp4"
    filters = []
    
    # 随机缩放裁剪（留黑边再放大回原尺寸）
    scale_ratio = random.uniform(*SCALE_RANGE)
    new_w = int(1080 * scale_ratio)
    new_h = int(1920 * scale_ratio)
    x_offset = random.randint(0, max(0, 1080 - new_w))
    y_offset = random.randint(0, max(0, 1920 - new_h))
    filters.append(f"crop={new_w}:{new_h}:{x_offset}:{y_offset}")
    filters.append("scale=1080:1920")
    
    # 镜像翻转
    if random.random() < MIRROR_PROB:
        filters.append("hflip")
    
    # Gamma校正（亮度）
    gamma = random.uniform(*GAMMA_RANGE)
    filters.append(f"eq=gamma={gamma}")
    
    # 噪点
    if random.random() < NOISE_PROB:
        filters.append("noise=alls=2:allf=u")
    
    # 调色（饱和度/对比度/色调）
    if random.random() < FILTER_PROB:
        saturation = random.uniform(*SATURATION_RANGE)
        contrast = random.uniform(*CONTRAST_RANGE)
        filters.append(f"eq=saturation={saturation}:contrast={contrast}")
        hue = random.uniform(*HUE_SHIFT_RANGE)
        if abs(hue) > 0.5:
            filters.append(f"hue=h={hue}")
    
    vf_string = ",".join(filters)
    
    # 随机播放速度
    speed = random.uniform(*SPEED_RANGE)
    
    cmd = [
        "ffmpeg", "-y", "-i", str(segment_path),
        "-filter:v", f"{vf_string},setpts={1/speed}*PTS",
        "-af", f"atempo={speed}",
        # 去除音频在最终合并时统一处理，这里保留原始音频以保证片段质量
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(output_file)
    ]
    run_cmd(cmd, "应用去重效果")
    return output_file


def concat_and_strip_audio(segments: list, output_path: Path):
    """
    合并片段 + 去除音频，一步完成（避免二次重编码）
    """
    list_file = output_path.parent / f"concat_{uuid.uuid4().hex}.txt"
    with open(list_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg.absolute()}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-an",  # 去除音频，一步到位
        str(output_path)
    ]
    run_cmd(cmd, "合并片段并去除音频")
    list_file.unlink()


def cleanup(*files):
    """清理临时文件"""
    for f in files:
        if f and isinstance(f, Path) and f.exists():
            f.unlink()


def process(url: str) -> Path:
    """主流程"""
    session_id = uuid.uuid4().hex[:8]
    session_dir = WORKSPACE / session_id
    session_dir.mkdir(exist_ok=True)
    
    raw_video = None
    segments = []
    processed_segments = []
    final_output = None
    
    try:
        # Step 1: 下载
        print("\n" + "="*50)
        print("Step 1/4: 解析视频...")
        video_id = extract_video_id(url)
        print(f"[OK] 视频ID: {video_id}")
        
        print("下载视频...")
        raw_video = session_dir / "raw.mp4"
        download_video(url, raw_video)
        
        if not validate_download(raw_video):
            raise RuntimeError("视频下载校验失败，请重试")
        print(f"[OK] 下载完成: {raw_video}")
        
        # Step 2: 截取并打乱片段
        print("\n" + "="*50)
        print("Step 2/4: 截取并打乱片段...")
        segments = create_and_shuffle_segments(str(raw_video), session_dir)
        
        # Step 3: 应用去重效果
        print("\n" + "="*50)
        print("Step 3/4: 应用去重效果...")
        processed_segments = []
        for seg in segments:
            eff_seg = apply_dedup_effects(seg, session_dir)
            processed_segments.append(eff_seg)
        print(f"[OK] 效果应用完成")
        
        # Step 4: 合并并去音频（一步）
        print("\n" + "="*50)
        print("Step 4/4: 合并片段并去除音频...")
        final_output = get_next_output_path()
        concat_and_strip_audio(processed_segments, final_output)
        
        # 最终校验
        final_info = get_video_info(str(final_output))
        print(f"\n" + "="*50)
        print(f"✅ 完成！输出: {final_output}")
        print(f"   时长: {final_info['duration']:.1f}s | 大小: {final_info['size']//1024}KB")
        return final_output
        
    finally:
        # 清理所有临时文件
        cleanup(raw_video, *segments, *processed_segments)
        if session_dir.exists():
            shutil.rmtree(session_dir)


def process_batch(urls: list) -> list:
    """批量处理"""
    results = []
    total = len(urls)
    for i, url in enumerate(urls, 1):
        separator = "#" * 60
        print(f"\n{separator}")
        print(f"# [{i}/{total}] {url}")
        print(separator)
        try:
            result = process(url)
            results.append({"url": url, "status": "success", "output": str(result)})
        except Exception as e:
            print(f"❌ 失败: {e}")
            results.append({"url": url, "status": "failed", "error": str(e)})
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  单个: python3 dedup.py <抖音URL>")
        print("  批量: python3 dedup.py <URL1> <URL2> ...")
        sys.exit(1)
    
    urls = sys.argv[1:]
    
    if len(urls) == 1:
        result = process(urls[0])
        print(f"\n输出路径: {result}")
    else:
        print(f"\n开始批量处理 {len(urls)} 个视频...")
        results = process_batch(urls)
        
        print(f"\n{'='*60}")
        print("批量处理完成!")
        print(f"{'='*60}")
        success = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]
        print(f"✅ 成功: {len(success)}")
        if failed:
            print(f"❌ 失败: {len(failed)}")
            for r in failed:
                print(f"   - {r['url']}: {r['error']}")
        print(f"\n输出目录: {OUTPUT}")
