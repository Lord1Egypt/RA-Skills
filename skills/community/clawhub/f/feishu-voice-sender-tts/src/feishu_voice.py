#!/usr/bin/env python3
"""
Feishu Voice Advanced - 安全合规版本
飞书语音消息发送，支持语音识别(ASR)、语音合成(TTS)和情绪参数

安全特性：
- 仅处理用户提供的输入
- 不读取任意本地文件
- 不自动运行，仅显式调用
- 使用环境变量管理密钥
"""

import os
import sys
import json
import base64
import tempfile
import subprocess
from typing import Optional, Dict, Any

# 安全限制常量
MAX_TEXT_LENGTH = 300

# Token 缓存
_token_cache = {"token": None, "expires_at": 0}

# 从环境变量读取配置
def get_base_config() -> Dict[str, str]:
    """获取基础配置（TTS + Feishu），从环境变量读取"""
    config = {
        'TTS_APP_ID': os.getenv('TTS_APP_ID'),
        'TTS_ACCESS_KEY': os.getenv('TTS_ACCESS_KEY'),
        'FEISHU_APP_ID': os.getenv('FEISHU_APP_ID'),
        'FEISHU_APP_SECRET': os.getenv('FEISHU_APP_SECRET'),
        'DEFAULT_RECEIVE_ID': os.getenv('DEFAULT_RECEIVE_ID', '')
    }
    
    required = ['TTS_APP_ID', 'TTS_ACCESS_KEY', 'FEISHU_APP_ID', 'FEISHU_APP_SECRET']
    missing = [k for k in required if not config.get(k)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return config


def get_asr_config() -> Dict[str, str]:
    """获取 ASR 配置，仅在调用语音识别时读取"""
    config = {
        'ASR_APP_ID': os.getenv('ASR_APP_ID'),
        'ASR_ACCESS_KEY': os.getenv('ASR_ACCESS_KEY'),
        'ASR_RESOURCE_ID': os.getenv('ASR_RESOURCE_ID', 'volc.bigasr.auc_turbo')
    }

    required = ['ASR_APP_ID', 'ASR_ACCESS_KEY']
    missing = [k for k in required if not config.get(k)]
    if missing:
        raise ValueError(f"ASR requires environment variables: {', '.join(missing)}")

    return config

# 向后兼容
get_config = get_base_config


def detect_emotion(text: str) -> str:
    """
    简单情绪检测
    
    Args:
        text: 输入文本
        
    Returns:
        情绪类型: happy, sad, neutral
    """
    positive_words = ['成功', '完成', '棒', '好', '赞', '恭喜', '胜利', '完美', '优秀', '厉害', '成功', 'good', 'great', 'success']
    negative_words = ['失败', '错误', '遗憾', '抱歉', '对不起', '难过', '伤心', '不好', '糟', 'fail', 'error', 'sorry']
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in positive_words):
        return 'happy'
    elif any(word in text_lower for word in negative_words):
        return 'sad'
    else:
        return 'neutral'


def recognize_voice_file(audio_path: str) -> str:
    """
    识别语音文件（ASR）
    
    安全限制：
    - 仅允许 .ogg 文件
    - 必须检查文件存在
    - 不扫描目录
    
    Args:
        audio_path: 音频文件路径
        
    Returns:
        识别文本
    """
    # 安全检查：文件格式
    if not audio_path.endswith('.ogg'):
        raise ValueError(f"Invalid audio format. Only .ogg files are allowed. Got: {audio_path}")
    
    # 安全检查：文件存在
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # 安全检查：是文件不是目录
    if not os.path.isfile(audio_path):
        raise ValueError(f"Path is not a file: {audio_path}")
    
    config = get_asr_config()
    
    # 读取音频文件
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    # 调用豆包 ASR API（极速版，本地文件直传）
    import requests
    import uuid
    
    url = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash"
    headers = {
        'X-Api-App-Key': config['ASR_APP_ID'],
        'X-Api-Access-Key': config['ASR_ACCESS_KEY'],
        'X-Api-Resource-Id': config['ASR_RESOURCE_ID'],
        'X-Api-Request-Id': str(uuid.uuid4()),
        'X-Api-Sequence': '-1',
        'Content-Type': 'application/json'
    }

    payload = {
        "user": {"uid": "12345"},
        "audio": {
            "data": base64.b64encode(audio_data).decode('utf-8'),
            "format": "ogg",
            "codec": "opus",
            "rate": 48000,
            "bits": 16,
            "channel": 1
        },
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        raise RuntimeError(f"ASR request failed: {response.status_code} | {response.text[:500]}")
    
    try:
        result = response.json()
    except Exception as e:
        raise RuntimeError(f"ASR invalid response: {e} | {response.text[:500]}")

    text = result.get('result', {}).get('text', '')
    if not text:
        raise RuntimeError(f"ASR empty result: {response.text[:500]}")
    
    return text


def generate_voice(text: str, emotion: str = 'neutral', context: str = '') -> str:
    """
    生成语音文件（TTS）
    
    Args:
        text: 要合成的文本
        emotion: 情绪类型
        context: 上下文文本（用于 context_texts）
        
    Returns:
        生成的音频文件路径（opus 格式）
    """
    # 安全检查：文本长度
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Text too long. Maximum {MAX_TEXT_LENGTH} characters. Got: {len(text)}")
    
    config = get_config()
    
    # 调用豆包 TTS API
    import requests
    
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
    headers = {
        'X-Api-App-Key': config['TTS_APP_ID'],
        'X-Api-Access-Key': config['TTS_ACCESS_KEY'],
        'X-Api-Resource-Id': 'seed-tts-2.0',
        'Content-Type': 'application/json'
    }
    
    # 构建请求体
    payload = {
        "user": {"uid": "12345"},
        "event": 100,
        "req_params": {
            "text": text,
            "speaker": "zh_male_m191_uranus_bigtts",
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000
            }
        }
    }
    
    # 添加 context_texts（如果提供）
    if context:
        payload["req_params"]["additions"] = json.dumps({
            "context_texts": [context]
        })
    
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    
    if response.status_code != 200:
        raise RuntimeError(f"TTS request failed: {response.status_code}")
    
    # 解析响应并提取音频
    audio_parts = []
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if data.get('code') == 0 and data.get('data'):
                    audio_parts.append(data['data'])
            except json.JSONDecodeError:
                continue
    
    if not audio_parts:
        raise RuntimeError("TTS returned empty audio")
    
    # 解码音频数据
    audio_data = base64.b64decode(''.join(audio_parts))
    
    # 使用临时文件
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_mp3:
        tmp_mp3.write(audio_data)
        mp3_path = tmp_mp3.name
    
    # 转换为 opus 格式（使用 ffmpeg）
    with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as tmp_opus:
        opus_path = tmp_opus.name
    
    try:
        # SECURITY: This subprocess call is restricted to ffmpeg for audio conversion only.
        # No user input is passed to the command.
        cmd = [
            'ffmpeg',
            '-i', mp3_path,
            '-c:a', 'libopus',
            '-b:a', '24k',
            opus_path,
            '-y'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    finally:
        # 清理临时 mp3 文件
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
    
    return opus_path


def get_feishu_token(config: Dict[str, str]) -> str:
    """获取飞书 access token（带缓存）"""
    import requests
    import time
    
    global _token_cache
    
    # 检查缓存是否有效
    if _token_cache["token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["token"]
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'app_id': config['FEISHU_APP_ID'],
        'app_secret': config['FEISHU_APP_SECRET']
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to get Feishu token: {response.status_code}")
    
    data = response.json()
    if data.get('code') != 0:
        raise RuntimeError(f"Feishu API error: {data.get('msg')}")
    
    token = data['tenant_access_token']
    expire = data.get('expire', 7200)  # 默认2小时
    
    # 缓存 token（提前5分钟过期）
    _token_cache["token"] = token
    _token_cache["expires_at"] = time.time() + expire - 300
    
    return token


def upload_audio_to_feishu(audio_path: str, token: str) -> str:
    """
    上传音频文件到飞书
    
    Args:
        audio_path: 音频文件路径
        token: 飞书 access token
        
    Returns:
        file_key
    """
    import requests
    
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    headers = {'Authorization': f'Bearer {token}'}
    
    with open(audio_path, 'rb') as f:
        files = {'file': ('voice.opus', f, 'audio/opus')}
        data = {'file_type': 'opus', 'file_name': 'voice.opus'}
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code != 200:
        raise RuntimeError(f"Upload failed: {response.status_code}")
    
    result = response.json()
    if result.get('code') != 0:
        raise RuntimeError(f"Upload error: {result.get('msg')}")
    
    return result['data']['file_key']


def send_voice_message(
    text: str,
    user_input: str = '',
    receive_id: str = ''
) -> bool:
    """
    发送语音消息（主函数）
    
    显式流程：
    用户输入 → 情绪参数提取 → TTS 语音合成 → 格式转换 → 飞书发送
    
    此函数仅处理用户提供的输入。
    
    Args:
        text: AI 生成的播报内容（必填，最大 300 字符）
        user_input: 用户的原始输入，用于情绪感知（可选）
        receive_id: 接收者 ID（可选，默认从环境变量读取）
        
    Returns:
        是否发送成功
    """
    try:
        config = get_config()
        
        # 确定接收者
        if not receive_id:
            receive_id = config.get('DEFAULT_RECEIVE_ID')
        if not receive_id:
            raise ValueError("No receive_id provided and no DEFAULT_RECEIVE_ID set")
        
        # 检测情绪
        emotion = detect_emotion(user_input or text)
        
        # 生成语音
        opus_path = generate_voice(text, emotion, user_input)
        
        try:
            # 获取飞书 token
            token = get_feishu_token(config)
            
            # 上传音频
            file_key = upload_audio_to_feishu(opus_path, token)
            
            # 发送消息
            import requests
            
            url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # 获取音频时长（动态计算：每个字符约 200ms，最大 60 秒）
            duration = min(len(text) * 200, 60000)  # 动态计算，最大 60 秒
            
            payload = {
                'receive_id': receive_id,
                'msg_type': 'audio',
                'content': json.dumps({
                    'file_key': file_key,
                    'duration': duration
                })
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise RuntimeError(f"Send failed: {response.status_code}")
            
            result = response.json()
            return result.get('code') == 0
            
        finally:
            # 清理临时文件
            if os.path.exists(opus_path):
                os.remove(opus_path)
                
    except Exception as e:
        print(f"发送语音消息失败: {e}")
        return False


# 便捷函数
def recognize(audio_path: str) -> str:
    """识别语音文件（便捷函数）"""
    return recognize_voice_file(audio_path)


def send(text: str, user_input: str = '', receive_id: str = '') -> bool:
    """发送语音消息（便捷函数）"""
    return send_voice_message(text, user_input, receive_id)


if __name__ == "__main__":
    # 测试
    print("情绪检测测试:")
    print(f"  '任务完成了！' -> {detect_emotion('任务完成了！')}")
    print(f"  '很遗憾，失败了...' -> {detect_emotion('很遗憾，失败了...')}")
    print(f"  '普通汇报工作' -> {detect_emotion('普通汇报工作')}")
