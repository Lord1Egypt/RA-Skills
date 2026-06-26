import os
import re
import sys
import json
import requests
import argparse
import tempfile

# ==========================================
# OpenClaw Skill: Bilibili Transcript Extractor
# 核心逻辑: 字幕优先 -> 回退音频流下载 -> 硅基流动 ASR 转录 -> 返回纯文本
# ==========================================

# 1. 检查环境变量中的 API Key
SILICONFLOW_API_KEY = os.environ.get("SILICONFLOW_API_KEY")

# B站通用请求头，必须带上 Referer 防止防盗链 (WAF/403错误)
BILI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com"
}

def extract_bvid(url):
    """从URL中提取BVID"""
    match = re.search(r'(BV[1-9A-HJ-NP-Za-km-z]{10})', url)
    return match.group(1) if match else None

def get_video_info_and_cid(bvid):
    """获取视频基础信息和 CID"""
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    response = requests.get(api_url, headers=BILI_HEADERS)
    data = response.json()
    if data['code'] == 0:
        return data['data']['cid']
    return None

def fetch_subtitles(bvid, cid):
    """途径一：尝试获取官方/AI生成的CC字幕"""
    api_url = f"https://api.bilibili.com/x/player/v2?cid={cid}&bvid={bvid}"
    try:
        response = requests.get(api_url, headers=BILI_HEADERS)
        data = response.json()
        subtitles = data.get('data', {}).get('subtitle', {}).get('subtitles', [])
        
        if subtitles:
            sub_url = subtitles[0]['subtitle_url']
            if not sub_url.startswith('http'):
                sub_url = 'https:' + sub_url
            
            sub_response = requests.get(sub_url, headers=BILI_HEADERS)
            sub_data = sub_response.json()
            
            full_text = " ".join([item['content'] for item in sub_data['body']])
            return full_text
    except Exception:
        pass # 静默失败，转入音频提取
    return None

def fetch_audio_stream_url(bvid, cid):
    """途径二：获取DASH音频流URL"""
    api_url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16"
    response = requests.get(api_url, headers=BILI_HEADERS)
    data = response.json()
    
    if data['code'] == 0:
        dash_data = data['data'].get('dash', {})
        audio_streams = dash_data.get('audio', [])
        if audio_streams:
            return audio_streams[0]['base_url']
    return None

def download_audio_to_temp(audio_url):
    """将带防盗链的音频流下载到本地临时文件"""
    # 必须携带 B站 Header 才能成功下载
    response = requests.get(audio_url, headers=BILI_HEADERS, stream=True)
    response.raise_for_status()
    
    # 创建临时文件 (后缀m4a适配B站音频格式)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".m4a")
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            temp_audio.write(chunk)
    temp_audio.close()
    return temp_audio.name

def convert_audio_to_text(audio_filepath):
    """调用硅基流动 (SiliconFlow) ASR 接口将音频转录为文本"""
    # 硅基流动标准的音频转写 API 端点
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}"
    }
    
    # 默认使用 SenseVoiceSmall 模型，速度快且支持多语种
    data = {
        "model": "FunAudioLLM/SenseVoiceSmall"
    }
    
    with open(audio_filepath, "rb") as audio_file:
        files = {
            "file": (os.path.basename(audio_filepath), audio_file, "audio/mp4")
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            result_json = response.json()
            return result_json.get("text", "")
        except Exception as e:
            return f"[ASR API 调用失败]: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Bilibili Transcript Extractor for OpenClaw")
    parser.add_argument("url", help="Bilibili 视频链接")
    args = parser.parse_args()

    # 运行时检查 API Key
    if not SILICONFLOW_API_KEY:
        print("\n[错误] 缺失硅基流动 API Key！", file=sys.stderr)
        print("请在系统或 OpenClaw 环境变量中设置 'SILICONFLOW_API_KEY'。", file=sys.stderr)
        print("Linux/macOS 示例: export SILICONFLOW_API_KEY='sk-你的真实密钥'", file=sys.stderr)
        print("Windows CMD 示例: set SILICONFLOW_API_KEY=sk-你的真实密钥", file=sys.stderr)
        sys.exit(1)

    bvid = extract_bvid(args.url)
    if not bvid:
        print("无法识别 BVID，请检查 URL格式。")
        return

    cid = get_video_info_and_cid(bvid)
    if not cid:
        print(f"无法获取视频 CID (BVID: {bvid})，视频可能失效或需登录。")
        return

    # 1. 优先尝试提取现成字幕
    transcript = fetch_subtitles(bvid, cid)
    
    # 2. 如果没有字幕，启动音频提取与ASR流程
    if not transcript:
        audio_url = fetch_audio_stream_url(bvid, cid)
        if audio_url:
            # 下载到临时文件
            temp_file_path = download_audio_to_temp(audio_url)
            try:
                # 调用 ASR
                transcript = convert_audio_to_text(temp_file_path)
            finally:
                # 清理临时文件，防止塞满硬盘
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        else:
            transcript = "提取失败：该视频既无自带字幕，也无法获取音频流。"

    # 3. 输出纯净文本给 OpenClaw LLM 进行总结
    print("\n--- B站视频提取内容开始 ---\n")
    print(transcript)
    print("\n--- B站视频提取内容结束 ---\n")

if __name__ == "__main__":
    main()