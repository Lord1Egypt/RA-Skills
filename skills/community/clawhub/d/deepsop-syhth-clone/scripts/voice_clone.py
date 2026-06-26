#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice Clone - AI 声音复刻与语音合成工具
调用 AI Artist API 进行音色克隆和语音合成
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path

# API 配置
BASE_URL = "https://ai.deepsop.com/prod-api"
FILE_UPLOAD_URL = f"{BASE_URL}/system/fileUpload/upload"

# 环境配置
API_KEY_ENV = "AI_ARTIST_TOKEN"


def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        # Try loading from .env file (in script directory)
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and line.startswith(f"{API_KEY_ENV}="):
                        api_key = line.split("=", 1)[1].strip('"\'')
                        break
        
        # Also check parent directory (skill root)
        if not api_key:
            env_file = Path(__file__).parent.parent / ".env"
            if env_file.exists():
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and line.startswith(f"{API_KEY_ENV}="):
                            api_key = line.split("=", 1)[1].strip('"\'')
                            break
    
    return api_key


def check_api_key():
    """检查 API Key 是否配置"""
    api_key = get_api_key()
    if not api_key:
        print(f"[ERROR] 未配置 {API_KEY_ENV} 环境变量", file=sys.stderr)
        print(f"\n请设置 API Key:")
        print(f"  Windows PowerShell: $env:{API_KEY_ENV}=\"sk-your_api_key_here\"")
        print(f"  Linux/macOS: export {API_KEY_ENV}=\"sk-your_api_key_here\"")
        return None
    return api_key


def get_headers():
    """获取请求头"""
    api_key = get_api_key()
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }


def upload_file(file_path):
    """上传本地文件到 OSS 获取 URL"""
    if not os.path.exists(file_path):
        print(f"[ERROR] 文件不存在：{file_path}", file=sys.stderr)
        return None
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(
                FILE_UPLOAD_URL,
                headers={"x-api-key": get_api_key()},
                files=files,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 200:
                url = result.get("url")
                print(f"[SUCCESS] 文件已上传：{file_path} -> {url}")
                return url
            else:
                print(f"[ERROR] 文件上传失败：{result.get('msg', '未知错误')}", file=sys.stderr)
                return None
                
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 文件上传错误：{e}", file=sys.stderr)
        return None


def list_voices():
    """查询音色列表"""
    url = f"{BASE_URL}/ai/voice/clone/list"
    params = {"pageNum": 1, "pageSize": 10}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 200:
            print(f"[ERROR] 查询失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None
        
        rows = result.get("rows", [])
        total = result.get("total", 0)
        
        print(f"[INFO] 共有 {total} 个音色")
        print("\n可用音色列表:")
        
        available = []
        for voice in rows:
            vid = voice.get("id")
            name = voice.get("name")
            status = voice.get("status")
            model = voice.get("targetModel", "unknown")
            
            status_mark = "[OK]" if status == "OK" else f"[{status}]"
            print(f"  [{vid}] {name} {status_mark} - {model}")
            
            if status == "OK":
                available.append(voice)
        
        return available
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 查询音色列表出错：{e}", file=sys.stderr)
        return None


def create_voice(name, audio_url=None, audio_path=None, prefix="DeepSop", remark=None):
    """创建新音色"""
    # 如果提供本地文件路径，先上传获取 URL
    if audio_path and not audio_url:
        audio_url = upload_file(audio_path)
        if not audio_url:
            return None
    
    if not audio_url:
        print("[ERROR] 必须提供 audio_url 或 audio_path", file=sys.stderr)
        return None
    
    payload = {
        "name": name,
        "prefix": prefix,
        "audioUrl": audio_url,
        "remark": remark
    }
    
    url = f"{BASE_URL}/ai/voice/clone/sync/create"
    
    try:
        response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 200:
            print(f"[ERROR] 创建失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None
        
        data = result.get("data", {})
        vid = data.get("id")
        voice_id = data.get("voiceId")
        status = data.get("status")
        
        print(f"[SUCCESS] 音色创建成功!")
        print(f"   ID: {vid}")
        print(f"   VoiceID: {voice_id}")
        print(f"   名称：{name}")
        print(f"   状态：{status}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 创建音色出错：{e}", file=sys.stderr)
        return None


def get_balance():
    """查询 K 币余额"""
    url = f"{BASE_URL}/ai/vip/balance"

    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != 200:
            print(f"[ERROR] 查询余额失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None

        balance = result.get("data")
        if balance is None:
            print("[ERROR] 查询余额失败：返回数据缺少余额信息", file=sys.stderr)
            return None

        print(f"[INFO] 当前 K 币余额：{balance}")
        return float(balance)

    except (ValueError, TypeError):
        print("[ERROR] 查询余额失败：余额数据格式异常", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 查询余额出错：{e}", file=sys.stderr)
        return None


def synthesize_voice(text, voice_id=None, voice_name=None):
    """语音合成"""
    # 如果提供名称，先查询获取 ID
    if voice_name and not voice_id:
        voices = list_voices()
        if voices:
            for v in voices:
                if v.get("name") == voice_name:
                    if v.get("status") != "OK":
                        print(f"[ERROR] 音色 '{voice_name}' 状态为 {v.get('status')}，不可用", file=sys.stderr)
                        return None
                    voice_id = v.get("id")
                    break
        
        if not voice_id:
            print(f"[ERROR] 未找到音色：{voice_name}", file=sys.stderr)
            return None
    
    if not voice_id:
        print("[ERROR] 必须提供 voice_id 或 voice_name", file=sys.stderr)
        return None

    balance = get_balance()
    if balance is None:
        return None

    if balance <= 0:
        print("[ERROR] K 币余额不足，无法进行语音合成，请先充值 K 币", file=sys.stderr)
        return None

    payload = {
        "text": text,
        "id": voice_id
    }
    
    url = f"{BASE_URL}/ai/voice/clone/synthesize"
    
    try:
        response = requests.post(url, headers=get_headers(), json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") != 200:
            print(f"[ERROR] 合成失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None
        
        audio_url = result.get("msg")
        
        print(f"[SUCCESS] 语音合成成功!")
        print(f"   音频链接：{audio_url}")
        
        return {
            "status": "SUCCESS",
            "url": audio_url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 语音合成出错：{e}", file=sys.stderr)
        return None


def download_audio(url, output_dir=None):
    """下载音频文件"""
    if not output_dir:
        output_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "audio")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # Generate filename from URL
        filename = url.split("/")[-1].split("?")[0]
        if not filename.endswith(".mp3"):
            filename = f"{int(time.time())}.mp3"
        
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"[SAVE] 音频已保存：{output_path}")
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"[WARNING] 下载音频失败：{e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="AI 声音复刻与语音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 模式选择
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--list", action="store_true", help="列出所有可用音色")
    mode_group.add_argument("--synthesize", action="store_true", help="语音合成模式")
    mode_group.add_argument("--create", action="store_true", help="创建新音色模式")
    
    # 通用参数
    parser.add_argument("--id", type=int, help="音色 ID")
    parser.add_argument("--name", help="音色名称")
    parser.add_argument("--text", help="要合成的文本内容")
    
    # 创建音色参数
    parser.add_argument("--audio", help="本地音频文件路径（创建音色时使用）")
    parser.add_argument("--audio-url", help="在线音频 URL（创建音色时使用）")
    parser.add_argument("--prefix", default="DeepSop", help="音色前缀（默认：DeepSop）")
    
    # 下载参数
    parser.add_argument("--download", action="store_true", help="下载合成的音频到本地")
    parser.add_argument("--output-dir", help="音频保存目录")
    
    args = parser.parse_args()
    
    # 检查 API Key
    if not check_api_key():
        sys.exit(1)
    
    # 列出音色
    if args.list:
        voices = list_voices()
        sys.exit(0 if voices is not None else 1)
    
    # 语音合成
    elif args.synthesize:
        if not args.text:
            print("[ERROR] 合成模式必须提供 --text 参数", file=sys.stderr)
            sys.exit(1)
        
        if not args.id and not args.name:
            print("[ERROR] 合成模式必须提供 --id 或 --name 参数", file=sys.stderr)
            sys.exit(1)
        
        result = synthesize_voice(args.text, voice_id=args.id, voice_name=args.name)
        
        if result and result.get("status") == "SUCCESS":
            if args.download:
                download_audio(result["url"], args.output_dir)
            print(result["url"])
            sys.exit(0)
        else:
            sys.exit(1)
    
    # 创建音色
    elif args.create:
        if not args.name:
            print("[ERROR] 创建模式必须提供 --name 参数", file=sys.stderr)
            sys.exit(1)
        
        if not args.audio and not args.audio_url:
            print("[ERROR] 创建模式必须提供 --audio 或 --audio-url 参数", file=sys.stderr)
            sys.exit(1)
        
        result = create_voice(
            name=args.name,
            audio_url=args.audio_url,
            audio_path=args.audio,
            prefix=args.prefix
        )
        
        if result:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
