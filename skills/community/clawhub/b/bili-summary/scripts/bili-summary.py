#!/usr/bin/env python3
"""
B站视频工具 - 被 Skill 调用
支持：
- 视频信息获取
- 字幕下载（B站CC字幕）
- 视频下载
- 音频提取 + Whisper转录
- AI总结
"""

import subprocess
import json
import sys
import argparse
import shutil
import os
from pathlib import Path
import urllib.request
import urllib.parse
import re

# 查找 yt-dlp 路径
YT_DLP = shutil.which("yt-dlp") or str(Path.home() / "miniconda3/bin/yt-dlp")

# LLM 配置 (Gemini) - 从环境变量读取
LLM_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 默认输出目录 - workspace 下的 temp/bili-summary
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace" / "coding-agent"
DEFAULT_OUTPUT = WORKSPACE_ROOT / "temp" / "bili-summary"
DEFAULT_OUTPUT.mkdir(parents=True, exist_ok=True)

# Whisper 配置 - 使用 tiny 模型加快速度
USE_FASTER_WHISPER = True
WHISPER_MODEL = "tiny"  # tiny, small, medium, large


def get_aid_cid(url: str) -> tuple:
    """从视频URL获取aid和cid"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # 提取 __INITIAL_STATE__
        match = re.search(r'window\.__INITIAL_STATE__=(.*?);\(function', html)
        if match:
            data = json.loads(match.group(1))
            video_data = data.get("videoData", {})
            return video_data.get("aid"), video_data.get("cid")
        
        # 备用方法：使用 yt-dlp
        cmd = [YT_DLP, "--dump-json", "--no-download", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return info.get("aid"), info.get("cid")
        
        return None, None
    except Exception as e:
        return None, None


def get_subtitle_url(aid: int, cid: int) -> str:
    """获取字幕URL"""
    try:
        url = f"https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            subtitles = data.get("data", {}).get("subtitle", {}).get("subtitles", [])
            if subtitles:
                subtitle_url = subtitles[0].get("subtitle_url", "")
                if subtitle_url:
                    return "https:" + subtitle_url if subtitle_url.startswith("//") else subtitle_url
        return ""
    except Exception as e:
        return ""


def parse_subtitle(subtitle_url: str) -> str:
    """解析字幕内容"""
    try:
        req = urllib.request.Request(subtitle_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            body = data.get("body", [])
            
            result = []
            for item in body:
                content = item.get("content", "").strip()
                if content:
                    result.append(content)
            
            return "\n".join(result)
    except Exception as e:
        return ""


def get_video_info(url: str) -> dict:
    """获取视频信息"""
    cmd = [YT_DLP, "--dump-json", "--no-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    
    data = json.loads(result.stdout)
    return {
        "title": data.get("title", ""),
        "bvid": data.get("id", ""),
        "duration": data.get("duration", 0),
        "uploader": data.get("uploader", ""),
        "description": data.get("description", "")[:500],
    }


def download_subtitle(url: str, output_dir: str = ".") -> str:
    """下载字幕（使用B站API）"""
    aid, cid = get_aid_cid(url)
    if not aid or not cid:
        return "Error: 无法获取视频信息"
    
    subtitle_url = get_subtitle_url(aid, cid)
    if not subtitle_url:
        return "Error: 该视频无字幕"
    
    subtitle_text = parse_subtitle(subtitle_url)
    if not subtitle_text:
        return "Error: 无法解析字幕内容"
    
    # 保存到文件
    output_path = Path(output_dir) / "subtitle.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(subtitle_text)
    
    return f"字幕已保存到: {output_path}"


def download_audio(url: str, output_dir: str = ".") -> str:
    """下载视频音频"""
    output_path = Path(output_dir) / "audio.m4a"
    cmd = [
        YT_DLP,
        "-f", "bestaudio[ext=m4a]/bestaudio",
        "-o", str(output_path),
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return str(output_path)


def transcribe_with_whisper(audio_path: str) -> str:
    """使用 Whisper 转录音频"""
    try:
        from faster_whisper import WhisperModel
        
        print(f"🎤 加载 Whisper 模型: {WHISPER_MODEL}")
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        
        print(f"🔄 转录音频: {audio_path}")
        # 自动检测语言，如果检测不准则默认英文
        segments, info = model.transcribe(audio_path, language=None)
        
        detected_lang = info.language if info.language else "en"
        lang_prob = info.language_probability
        
        # 如果检测置信度低，使用英文
        if lang_prob < 0.5:
            detected_lang = "en"
        
        print(f"🗣️ 检测到语言: {detected_lang} (概率: {lang_prob:.2f})")
        
        result = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                result.append(text)
        
        return "\n".join(result)
    except Exception as e:
        return f"转录失败: {str(e)}"


def summarize_with_llm(video_info: dict, subtitle: str) -> str:
    """用 Gemini 总结内容 - 详细版"""
    if not subtitle:
        return "无字幕内容可供总结"
    
    if not GEMINI_API_KEY:
        lines = subtitle.split("\n")
        preview = "\n".join(lines[:30])
        return f"""【视频总结】

标题: {video_info.get('title', '')}
UP主: {video_info.get('uploader', '')}

字幕片段:
{preview}
...

(共 {len(lines)} 条字幕)
设置 GEMINI_API_KEY 环境变量启用 AI 总结)
"""

    prompt = f"""请详细总结以下视频的内容，模仿视频作者的说话风格和语气：

视频标题: {video_info.get('title', '')}
UP主: {video_info.get('uploader', '')}

视频字幕/转录内容:
{subtitle[:8000]}

请按照以下格式详细总结：

## 📖 章节概要
按视频的时间顺序列出主要章节和内容

## 🎯 核心内容
用流畅的段落详细总结视频的主要内容和观点，不要使用列表或bullet points

## 💡 关键思考
挑选最重要的3-5个观点，用详细段落解释

## 📝 总结
用作者的语气给出最终结论

请用中文回复，语气要自然流畅，像在写一篇博客文章而不是列要点。"""

    try:
        url = f"{LLM_API_URL}?key={GEMINI_API_KEY}"
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "总结失败")
    except Exception as e:
        return f"总结失败: {str(e)}"


def download_video(url: str, output_dir: str = ".") -> str:
    """下载视频"""
    cmd = [
        YT_DLP,
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "-o", f"{output_dir}/%(title)s.%(ext)s",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return "Video downloaded"


def main():
    parser = argparse.ArgumentParser(description="B站视频工具")
    parser.add_argument("url", help="B站视频URL")
    parser.add_argument("--action", choices=["info", "subtitle", "video", "transcribe", "summary"], default="info")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="输出目录")
    
    args = parser.parse_args()
    
    if args.action == "info":
        info = get_video_info(args.url)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    elif args.action == "subtitle":
        result = download_subtitle(args.url, args.output)
        print(result)
    elif args.action == "video":
        print(download_video(args.url, args.output))
    elif args.action == "transcribe":
        # 下载音频
        print("📥 下载音频...")
        audio_path = download_audio(args.url, args.output)
        if audio_path.startswith("Error"):
            print(audio_path)
            return
        
        # 转录
        print("🎤 转录音频...")
        transcript = transcribe_with_whisper(audio_path)
        
        # 保存转录
        output_path = Path(args.output) / "transcript.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        print(f"📝 转录已保存到: {output_path}")
        print(f"\n--- 转录内容 (前1000字) ---\n{transcript[:1000]}")
    elif args.action == "summary":
        # 获取视频信息
        info = get_video_info(args.url)
        
        # 尝试获取B站字幕
        aid, cid = get_aid_cid(args.url)
        subtitle_text = ""
        
        if aid and cid:
            subtitle_url = get_subtitle_url(aid, cid)
            if subtitle_url:
                subtitle_text = parse_subtitle(subtitle_url)
        
        # 如果没有字幕，下载音频转录
        if not subtitle_text:
            print("⚠️ 无B站字幕，正在下载音频并转录...")
            
            # 下载音频
            audio_path = download_audio(args.url, args.output)
            if not audio_path.startswith("Error"):
                print("🎤 转录音频...")
                subtitle_text = transcribe_with_whisper(audio_path)
        
        if not subtitle_text:
            print("无法获取字幕内容")
            return
        
        # 保存字幕/转录
        output_path = Path(args.output) / "subtitle.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(subtitle_text)
        
        # 总结
        print("🤖 AI 总结...")
        result = summarize_with_llm(info, subtitle_text)
        
        # 保存总结到文件
        summary_path = Path(args.output) / "summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"\n✅ 总结已保存到: {summary_path}")
        print(f"\n{'='*50}\n{result}")


if __name__ == "__main__":
    main()
