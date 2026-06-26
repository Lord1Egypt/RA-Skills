#!/usr/bin/env python3
"""
飞书 TTS 语音消息发送
1. 用 edge-tts 生成 TTS（mp3）
2. 用 ffmpeg 转换为标准 Ogg Opus
3. 调用官方 API 发送语音消息

用法: python3 tts_and_send.py "文字内容" <open_id> [-v voice] [-r rate]
"""
import os
import sys
import json
import subprocess
import tempfile
import shutil
from typing import Tuple, Optional

# 从环境变量或 OpenClaw 配置读取飞书凭证
def load_feishu_credentials():
    """从环境变量或 OpenClaw 配置读取飞书凭证"""
    # 优先使用环境变量
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    if app_id and app_secret:
        return app_id, app_secret
    
    # 回退到 OpenClaw 配置
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        feishu_config = config.get('channels', {}).get('feishu', {})
        accounts = feishu_config.get('accounts', {})
        main_account = accounts.get('main', {})
        return main_account.get('appId'), main_account.get('appSecret')
    except Exception as e:
        print(f"读取 OpenClaw 配置失败: {e}")
        return None, None

APP_ID, APP_SECRET = load_feishu_credentials()


def get_tenant_access_token(app_id: str, app_secret: str) -> Tuple[str, Optional[Exception]]:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    try:
        import requests
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code", 0) != 0:
            return "", Exception(f"获取 token 失败: {result.get('msg', 'unknown')}")
        
        return result["tenant_access_token"], None
    except Exception as e:
        return "", e


def get_audio_duration(file_path: str) -> int:
    """用 ffprobe 获取音频时长（毫秒）"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration_sec = float(result.stdout.strip())
        return int(duration_sec * 1000)
    except Exception as e:
        print(f"获取音频时长失败: {e}")
        return 0


def upload_audio_file(tenant_access_token: str, file_path: str, duration: int) -> Tuple[str, Optional[Exception]]:
    """上传 OPUS 音频文件"""
    import requests
    
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        if len(file_content) == 0:
            return "", Exception("音频文件为空")
        
        if len(file_content) > 30 * 1024 * 1024:
            return "", Exception("音频文件超过 30MB 限制")
        
        files = {
            'file': (os.path.basename(file_path), file_content, 'application/octet-stream')
        }
        data = {
            'file_type': 'opus',
            'file_name': os.path.basename(file_path),
            'duration': str(duration)
        }
        
        response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code", 0) != 0:
            return "", Exception(f"上传文件失败: {result.get('msg', 'unknown')}")
        
        file_key = result["data"]["file_key"]
        print(f"文件上传成功, file_key: {file_key}")
        return file_key, None
        
    except Exception as e:
        return "", e


def send_audio_message(tenant_access_token: str, receive_id: str, file_key: str, duration: int) -> Tuple[str, Optional[Exception]]:
    """发送语音消息"""
    import requests
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    content = {
        "file_key": file_key,
        "duration": duration
    }
    
    payload = {
        "receive_id": receive_id,
        "msg_type": "audio",
        "content": json.dumps(content)
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code", 0) != 0:
            return "", Exception(f"发送消息失败: {result.get('msg', 'unknown')}")
        
        message_id = result["data"].get("message_id", "")
        print(f"语音消息发送成功, message_id: {message_id}")
        return message_id, None
        
    except Exception as e:
        return "", e


def generate_tts(text: str, output_path: str, voice: str = "zh-CN-YunjianNeural", rate: str = "-10%") -> bool:
    """用 edge-tts 生成 TTS"""
    try:
        cmd = [
            "uvx", "edge-tts",
            "-t", text,
            "-v", voice,
            f"--rate={rate}",
            "--write-media", output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"TTS 生成失败: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"TTS 生成异常: {e}")
        return False


def convert_to_opus(input_path: str, output_path: str) -> bool:
    """用 ffmpeg 转换为标准 Ogg Opus"""
    try:
        cmd = [
            "ffmpeg", "-i", input_path,
            "-c:a", "libopus", "-b:a", "32k", "-ar", "24000", "-ac", "1",
            output_path, "-y"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"转换失败: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"转换异常: {e}")
        return False


def main():
    # 解析参数
    if len(sys.argv) < 3:
        print("用法: python3 tts_and_send.py \"文字内容\" <open_id> [-v voice] [-r rate]")
        print("示例: python3 tts_and_send.py \"你好\" ou_xxx -v zh-CN-YunjianNeural -r -10%")
        sys.exit(1)
    
    # 验证凭证
    if not APP_ID or not APP_SECRET:
        print("错误: 无法从 OpenClaw 配置读取飞书凭证")
        sys.exit(1)
    
    text = sys.argv[1]
    receive_id = sys.argv[2]
    
    # 解析可选参数
    voice = "zh-CN-YunjianNeural"
    rate = "-10%"
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "-v" and i + 1 < len(sys.argv):
            voice = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "-r" and i + 1 < len(sys.argv):
            rate = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    print(f"文字内容: {text}")
    print(f"音色: {voice}, 语速: {rate}")
    print(f"接收者: {receive_id}")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    mp3_path = os.path.join(temp_dir, "tts.mp3")
    ogg_path = os.path.join(temp_dir, "voice.ogg")
    
    try:
        # Step 1: 生成 TTS
        print("\n[1/4] 生成 TTS...")
        if not generate_tts(text, mp3_path, voice, rate):
            sys.exit(1)
        print(f"TTS 生成成功: {mp3_path}")
        
        # Step 2: 转换为 Ogg Opus
        print("\n[2/4] 转换为 Ogg Opus...")
        if not convert_to_opus(mp3_path, ogg_path):
            sys.exit(1)
        print(f"转换成功: {ogg_path}")
        
        # Step 3: 获取 duration
        print("\n[3/4] 获取音频时长...")
        duration = get_audio_duration(ogg_path)
        if duration <= 0:
            print("错误: 无法获取音频时长")
            sys.exit(1)
        print(f"音频时长: {duration} 毫秒")
        
        # Step 4: 获取 token
        print("\n[4/4] 发送语音消息...")
        print("获取 tenant_access_token...")
        import requests
        token, err = get_tenant_access_token(APP_ID, APP_SECRET)
        if err:
            print(f"错误: {err}")
            sys.exit(1)
        print("Token 获取成功")
        
        # 上传文件
        print("上传音频文件...")
        file_key, err = upload_audio_file(token, ogg_path, duration)
        if err:
            print(f"错误: {err}")
            sys.exit(1)
        
        # 发送消息
        message_id, err = send_audio_message(token, receive_id, file_key, duration)
        if err:
            print(f"错误: {err}")
            sys.exit(1)
        
        print(f"\n✅ 完成! message_id: {message_id}")
        
    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
