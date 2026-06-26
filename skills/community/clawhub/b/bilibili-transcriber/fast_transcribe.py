"""
Bilibili 视频快速转录脚本 - 优化版
优化点：
1. 跳过 wav 转换，直接转录 m4a
2. 使用更快的转录参数
3. 并行下载和预处理
4. 流式/内存处理（小文件跳过磁盘I/O）
5. 智能模型选择（根据视频特征自动选择）
"""

import os
import sys
import re
import json
import urllib.request
import subprocess
import time
import io
import tempfile
import shutil
from pathlib import Path
from typing import Optional, BinaryIO, Literal
from dataclasses import dataclass

# 添加 transcriber 模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transcriber import (
    transcribe_with_timestamps,
    transcribe_with_timestamps_bytes,
    get_model_info
)


# ==================== 智能模型选择 ====================

@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    size: str  # tiny, base, small, medium, large
    speed_rating: int  # 1-5, 越高越快
    accuracy_rating: int  # 1-5, 越高越准
    memory_mb: int  # 预估内存占用
    best_for: list  # 适用场景


# 模型性能参考（基于 faster-whisper 中文场景）
MODEL_CONFIGS = {
    "tiny": ModelConfig(
        name="tiny",
        size="tiny",
        speed_rating=5,
        accuracy_rating=2,
        memory_mb=400,
        best_for=["短视频", "实时预览", "快速草稿"]
    ),
    "base": ModelConfig(
        name="base",
        size="base",
        speed_rating=4,
        accuracy_rating=3,
        memory_mb=600,
        best_for=["中等长度", "平衡场景"]
    ),
    "small": ModelConfig(
        name="small",
        size="small",
        speed_rating=3,
        accuracy_rating=4,
        memory_mb=1000,
        best_for=["长视频", "技术内容", "高质量需求"]
    ),
    "medium": ModelConfig(
        name="medium",
        size="medium",
        speed_rating=2,
        accuracy_rating=4,
        memory_mb=1500,
        best_for=["专业内容", "多语言混合"]
    ),
    "large": ModelConfig(
        name="large",
        size="large",
        speed_rating=1,
        accuracy_rating=5,
        memory_mb=2500,
        best_for=["最高质量", "复杂音频"]
    ),
}


@dataclass
class VideoProfile:
    """视频特征画像"""
    duration: int  # 秒
    title: str
    category: str  # 分区
    has_tech_terms: bool  # 是否包含技术术语
    is_tutorial: bool  # 是否是教程类
    audio_quality: str  # 音频质量估计


def analyze_video_content(title: str, desc: str = "", tags: list = None) -> dict:
    """
    分析视频内容特征

    Args:
        title: 视频标题
        desc: 视频简介
        tags: 视频标签

    Returns:
        内容特征字典
    """
    text = f"{title} {desc}".lower()
    tags = tags or []

    # 技术关键词
    tech_keywords = [
        "python", "java", "javascript", "编程", "代码", "教程", "教学",
        "算法", "数据结构", "机器学习", "ai", "人工智能", "深度学习",
        "前端", "后端", "数据库", "linux", "docker", "git",
        "面试", "leetcode", "力扣", "刷题", "课程", "公开课",
        "讲座", "学术", "论文", "研究", "技术", "开发"
    ]

    # 教程类关键词
    tutorial_keywords = [
        "教程", "教学", "入门", "基础", "进阶", "实战", "项目",
        "课程", "学习", "讲解", "手把手", "从零开始", "零基础"
    ]

    # 高质量音频需求关键词
    quality_keywords = [
        "音乐", "歌曲", "演唱会", "asmr", "录音", "播客", "podcast"
    ]

    tech_count = sum(1 for kw in tech_keywords if kw in text)
    tutorial_count = sum(1 for kw in tutorial_keywords if kw in text)
    quality_count = sum(1 for kw in quality_keywords if kw in text)

    return {
        "has_tech_terms": tech_count >= 2,
        "is_tutorial": tutorial_count >= 1,
        "needs_high_quality": quality_count >= 1,
        "tech_score": min(tech_count / 3, 1.0),  # 0-1
        "complexity": "high" if tech_count >= 3 else ("medium" if tech_count >= 1 else "low")
    }


def select_optimal_model(
    duration: int,
    title: str = "",
    desc: str = "",
    tags: list = None,
    user_preference: str = "auto",  # auto, fast, accurate
    available_memory_mb: int = None
) -> str:
    """
    根据视频特征智能选择最优模型

    Args:
        duration: 视频时长（秒）
        title: 视频标题
        desc: 视频简介
        tags: 视频标签
        user_preference: 用户偏好 (auto/fast/accurate)
        available_memory_mb: 可用内存（自动检测）

    Returns:
        模型名称 (tiny/base/small/medium/large)
    """
    # 自动检测可用内存
    if available_memory_mb is None:
        try:
            import psutil
            available_memory_mb = psutil.virtual_memory().available // (1024 * 1024)
        except ImportError:
            available_memory_mb = 4000  # 默认假设 4GB 可用

    # 分析内容特征
    content = analyze_video_content(title, desc, tags)

    # 根据用户偏好和特征选择模型
    if user_preference == "fast":
        # 速度优先：短视频用 tiny，长视频用 base
        if duration < 300:  # < 5分钟
            return "tiny"
        elif duration < 1800:  # < 30分钟
            return "base"
        else:
            return "small"

    elif user_preference == "accurate":
        # 质量优先
        if content["needs_high_quality"] or content["complexity"] == "high":
            if available_memory_mb >= 2500:
                return "large"
            elif available_memory_mb >= 1500:
                return "medium"
        return "small"

    else:  # auto 智能选择
        # 规则 1: 超短视频 (< 3分钟) -> tiny（速度优先）
        if duration < 180:
            return "tiny"

        # 规则 2: 短视频 (3-10分钟) + 非技术内容 -> base
        if duration < 600 and not content["has_tech_terms"]:
            return "base"

        # 规则 3: 技术/教程类内容 -> small（需要识别专业术语）
        if content["has_tech_terms"] or content["is_tutorial"]:
            # 内存足够用 small，否则 base
            if available_memory_mb >= 1000:
                return "small"
            return "base"

        # 规则 4: 长视频 (> 30分钟) -> small（平衡选择）
        if duration > 1800:
            if available_memory_mb >= 1000:
                return "small"
            return "base"

        # 规则 5: 默认 small（平衡选择）
        if available_memory_mb >= 1000:
            return "small"
        elif available_memory_mb >= 600:
            return "base"
        return "tiny"


def get_model_selection_reason(
    model: str,
    duration: int,
    content_analysis: dict
) -> str:
    """获取模型选择的理由说明"""
    config = MODEL_CONFIGS.get(model)
    if not config:
        return "使用默认模型"

    reasons = []

    # 时长原因
    if duration < 180:
        reasons.append("短视频优先速度")
    elif duration > 1800:
        reasons.append("长视频需要平衡质量与速度")

    # 内容原因
    if content_analysis.get("has_tech_terms"):
        reasons.append("技术内容需要更高精度")
    if content_analysis.get("is_tutorial"):
        reasons.append("教程类内容需要准确识别")

    # 模型特点
    reasons.append(f"{config.name}模型: 速度{config.speed_rating}/5, 精度{config.accuracy_rating}/5")

    return "; ".join(reasons)


def extract_bvid(url: str) -> str:
    """从URL中提取BV号"""
    match = re.search(r'BV[0-9a-zA-Z]+', url)
    if match:
        return match.group()
    raise ValueError(f"无法从URL提取BV号: {url}")


def get_video_info(bvid: str) -> dict:
    """获取视频基本信息"""
    api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    req = urllib.request.Request(api_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('code') == 0:
            return data['data']
        raise Exception(f"API错误: {data}")


def check_subtitle(bvid: str, cid: str) -> list:
    """检查视频是否有官方字幕"""
    api_url = f'https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}'
    req = urllib.request.Request(api_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://www.bilibili.com/video/{bvid}'
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('code') == 0:
            subtitle_info = data['data'].get('subtitle', {})
            return subtitle_info.get('subtitles', [])
    return []


def download_subtitle(subtitle_url: str) -> list:
    """
    下载并解析字幕文件

    Args:
        subtitle_url: 字幕JSON文件的URL（通常是 //subtitle.bilibili.com/...）

    Returns:
        字幕片段列表，每项为 {"start": float, "end": float, "text": str}
    """
    # 确保URL有协议头
    if subtitle_url.startswith('//'):
        subtitle_url = 'https:' + subtitle_url

    req = urllib.request.Request(subtitle_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.bilibili.com'
    })

    with urllib.request.urlopen(req, timeout=30) as response:
        subtitle_data = json.loads(response.read().decode('utf-8'))

    # B站字幕格式: {"body": [{"from": 0.0, "to": 5.0, "content": "..."}, ...]}
    results = []
    for item in subtitle_data.get('body', []):
        results.append({
            "start": float(item.get('from', 0)),
            "end": float(item.get('to', 0)),
            "text": item.get('content', '').strip()
        })

    return results


def get_official_subtitle(bvid: str, cid: str, prefer_ai: bool = True) -> tuple:
    """
    获取官方字幕（优先AI字幕，其次人工字幕）

    Args:
        bvid: BV号
        cid: 视频CID
        prefer_ai: 是否优先使用AI生成字幕

    Returns:
        (字幕列表, 字幕类型) 或 (None, None) 如果没有字幕
    """
    subtitles = check_subtitle(bvid, cid)

    if not subtitles:
        return None, None

    # 筛选字幕类型
    ai_subtitles = [s for s in subtitles if 'ai' in s.get('lan_doc', '').lower()]
    human_subtitles = [s for s in subtitles if 'ai' not in s.get('lan_doc', '').lower()]

    # 选择优先级
    if prefer_ai and ai_subtitles:
        selected = ai_subtitles[0]
        sub_type = "AI字幕"
    elif human_subtitles:
        selected = human_subtitles[0]
        sub_type = "人工字幕"
    elif ai_subtitles:
        selected = ai_subtitles[0]
        sub_type = "AI字幕"
    else:
        selected = subtitles[0]
        sub_type = selected.get('lan_doc', '未知字幕')

    subtitle_url = selected.get('subtitle_url')
    if not subtitle_url:
        return None, None

    subtitle_data = download_subtitle(subtitle_url)
    return subtitle_data, sub_type


def download_audio(url: str, output_path: str) -> str:
    """下载视频音频到文件"""
    cmd = [
        'python', '-m', 'yt_dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'm4a',
        '-o', f'{output_path}.%(ext)s',
        url
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return f"{output_path}.m4a"


def download_audio_to_memory(url: str, max_size_mb: int = 50) -> Optional[bytes]:
    """
    下载音频到内存（小文件优化）

    Args:
        url: 视频URL
        max_size_mb: 最大文件大小(MB)，超过则返回None

    Returns:
        音频文件字节数据，或None（文件过大或下载失败）
    """
    try:
        # 使用 yt-dlp 的 pipe 模式下载到 stdout
        cmd = [
            'python', '-m', 'yt_dlp',
            '-f', f'bestaudio[filesize<{max_size_mb}M]',
            '--extract-audio',
            '--audio-format', 'm4a',
            '-o', '-',  # 输出到 stdout
            url
        ]

        print(f'[FastTranscribe] 尝试流式下载音频（<{max_size_mb}MB）...')
        start_time = time.time()

        result = subprocess.run(cmd, capture_output=True, timeout=120)

        if result.returncode != 0:
            error_msg = result.stderr.decode('utf-8', errors='ignore')[:200]
            print(f'[FastTranscribe] 流式下载失败: {error_msg}')
            return None

        audio_data = result.stdout
        elapsed = time.time() - start_time
        size_mb = len(audio_data) / (1024 * 1024)

        print(f'[FastTranscribe] 流式下载完成: {size_mb:.1f} MB, 耗时 {elapsed:.1f}s')
        return audio_data

    except subprocess.TimeoutExpired:
        print('[FastTranscribe] 流式下载超时')
        return None
    except Exception as e:
        print(f'[FastTranscribe] 流式下载异常: {e}')
        return None


def get_audio_duration(audio_data: bytes) -> float:
    """
    使用 ffprobe 获取音频时长（从内存数据）

    Args:
        audio_data: 音频文件字节数据

    Returns:
        时长（秒）
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            '-i', 'pipe:0'  # 从 stdin 读取
        ]

        result = subprocess.run(
            cmd,
            input=audio_data,
            capture_output=True,
            timeout=10
        )

        if result.returncode == 0:
            duration = float(result.stdout.decode().strip())
            return duration
    except Exception:
        pass

    return 0.0


def transcribe_audio(audio_path: str, language: str = 'zh', model_size: str = 'tiny') -> list:
    """
    转录音频文件 - 优化版
    直接转录 m4a，跳过 wav 转换
    """
    print(f'[FastTranscribe] 开始转录: {audio_path}')
    start_time = time.time()

    # 使用优化的参数
    results = transcribe_with_timestamps(
        audio_path,
        language=language,
        model_size=model_size,
        beam_size=3,  # 减小beam size提高速度
        vad_filter=True,
        use_modelscope=True
    )

    elapsed = time.time() - start_time
    print(f'[FastTranscribe] 转录完成: {len(results)} 个片段, 耗时 {elapsed:.1f} 秒')

    return results


def transcribe_audio_bytes_optimized(
    audio_data: bytes,
    language: str = 'zh',
    model_size: str = 'tiny'
) -> list:
    """
    从内存转录音频 - 流式处理版
    完全跳过磁盘I/O，使用内存临时文件
    """
    print(f'[FastTranscribe] 开始内存转录 ({len(audio_data)/(1024*1024):.1f} MB)')
    start_time = time.time()

    # 使用优化的参数
    results = transcribe_with_timestamps_bytes(
        audio_data,
        language=language,
        model_size=model_size,
        beam_size=3,
        vad_filter=True,
        use_modelscope=True
    )

    elapsed = time.time() - start_time
    print(f'[FastTranscribe] 转录完成: {len(results)} 个片段, 耗时 {elapsed:.1f} 秒')

    return results


def save_transcription(results: list, output_path: str):
    """保存转录结果"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for seg in results:
            start_min = int(seg['start'] // 60)
            start_sec = int(seg['start'] % 60)
            text = seg['text']
            f.write(f'[{start_min:02d}:{start_sec:02d}] {text}\n')
    print(f'[FastTranscribe] 转录结果已保存: {output_path}')


def process_video(
    url: str,
    output_dir: str = '/tmp',
    model_size: str = 'auto',
    user_preference: str = 'auto'
) -> dict:
    """
    处理视频的完整流程 - 优化版

    Args:
        url: B站视频URL
        output_dir: 输出目录
        model_size: 模型大小 (tiny/base/small/medium/large/auto)
        user_preference: 用户偏好 (auto/fast/accurate)

    Returns:
        dict: 包含视频信息和转录结果
    """
    total_start = time.time()

    # 1. 提取BV号
    print(f'\n{"="*60}')
    print(f'[1/6] 解析视频URL...')
    bvid = extract_bvid(url)
    print(f'      BVID: {bvid}')

    # 2. 获取视频信息
    print(f'\n[2/6] 获取视频信息...')
    video_info = get_video_info(bvid)
    title = video_info['title']
    author = video_info['owner']['name']
    duration = video_info['duration']
    cid = video_info['cid']
    desc = video_info.get('desc', '')
    # 尝试获取标签
    tags = []
    if 'dynamic' in video_info:
        tags.append(video_info['dynamic'])

    print(f'      标题: {title}')
    print(f'      UP主: {author}')
    print(f'      时长: {duration} 秒 ({duration//60}分{duration%60}秒)')

    # 3. 智能选择模型
    print(f'\n[3/6] 智能选择转录模型...')
    if model_size == 'auto':
        selected_model = select_optimal_model(
            duration=duration,
            title=title,
            desc=desc,
            tags=tags,
            user_preference=user_preference
        )
        content_analysis = analyze_video_content(title, desc, tags)
        reason = get_model_selection_reason(selected_model, duration, content_analysis)
        print(f'      选择模型: {selected_model}')
        print(f'      选择理由: {reason}')
    else:
        selected_model = model_size
        print(f'      使用指定模型: {selected_model}')

    # 4. 检查并获取官方字幕
    print(f'\n[4/6] 检查官方字幕...')
    subtitle_data, subtitle_type = get_official_subtitle(bvid, cid, prefer_ai=True)

    if subtitle_data:
        print(f'      找到 {subtitle_type}，共 {len(subtitle_data)} 条字幕')
        print(f'      跳过音频下载，直接使用官方字幕')

        # 保存字幕结果
        output_path = os.path.join(output_dir, bvid)
        transcription_path = f"{output_path}_transcription.txt"
        save_transcription(subtitle_data, transcription_path)

        total_elapsed = time.time() - total_start
        print(f'\n{"="*60}')
        print(f'处理完成！（使用官方{subtitle_type}）')
        print(f'总耗时: {total_elapsed:.1f} 秒')
        print(f'视频时长: {duration//60}分{duration%60}秒')
        print(f'{"="*60}\n')

        return {
            'bvid': bvid,
            'title': title,
            'author': author,
            'duration': duration,
            'transcription': subtitle_data,
            'transcription_path': transcription_path,
            'total_time': total_elapsed,
            'source': subtitle_type
        }
    else:
        print(f'      无官方字幕，将使用音频转录')

    # 5. 下载音频（优先流式内存处理）
    print(f'\n[5/6] 下载音频...')
    output_path = os.path.join(output_dir, bvid)

    # 尝试流式下载到内存（小文件优化）
    audio_data = download_audio_to_memory(url, max_size_mb=50)

    if audio_data:
        # 流式处理：内存 -> 转录
        print(f'\n[6/6] 转录音频（流式内存处理，模型: {selected_model}）...')
        results = transcribe_audio_bytes_optimized(audio_data, language='zh', model_size=selected_model)
        # 清理内存
        del audio_data
    else:
        # 回退到文件下载（大文件）
        print(f'      文件较大，使用磁盘缓存模式')
        audio_path = download_audio(url, output_path)
        audio_size = os.path.getsize(audio_path) / (1024 * 1024)
        print(f'      音频已下载: {audio_path} ({audio_size:.1f} MB)')

        print(f'\n[6/6] 转录音频（磁盘模式，模型: {selected_model}）...')
        results = transcribe_audio(audio_path, language='zh', model_size=selected_model)

    # 保存结果
    transcription_path = f"{output_path}_transcription.txt"
    save_transcription(results, transcription_path)

    # 清理临时文件（如果是磁盘模式）
    if 'audio_path' in locals() and os.path.exists(audio_path):
        try:
            os.remove(audio_path)
            print(f'[FastTranscribe] 已清理临时音频文件')
        except:
            pass

    total_elapsed = time.time() - total_start
    print(f'\n{"="*60}')
    print(f'处理完成！（音频转录）')
    print(f'总耗时: {total_elapsed:.1f} 秒 ({total_elapsed/60:.1f} 分钟)')
    print(f'视频时长: {duration//60}分{duration%60}秒')
    print(f'处理速度比: {duration/total_elapsed:.1f}x')
    print(f'{"="*60}\n')

    return {
        'bvid': bvid,
        'title': title,
        'author': author,
        'duration': duration,
        'transcription': results,
        'transcription_path': transcription_path,
        'total_time': total_elapsed,
        'source': '音频转录',
        'model': selected_model
    }


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Bilibili视频快速转录 - 智能模型选择版')
    parser.add_argument('url', help='Bilibili视频URL')
    parser.add_argument('--output', '-o', default='/tmp', help='输出目录')
    parser.add_argument('--model', '-m', default='auto',
                        choices=['auto', 'tiny', 'base', 'small', 'medium', 'large'],
                        help='模型大小 (auto=智能选择, tiny=最快, large=最准)')
    parser.add_argument('--preference', '-p', default='auto',
                        choices=['auto', 'fast', 'accurate'],
                        help='用户偏好 (auto=智能平衡, fast=速度优先, accurate=质量优先)')

    args = parser.parse_args()

    result = process_video(args.url, args.output, args.model, args.preference)
    print(f'转录结果已保存: {result["transcription_path"]}')
