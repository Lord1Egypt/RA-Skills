import os
import re
import requests
from yt_dlp import YoutubeDL

def extract_url(text):
    """使用正则表达式从混乱的分享文案中精准提取 http/https 链接"""
    match = re.search(r'(https?://[^\s]+)', text)
    return match.group(1) if match else None

def download_video_only(video_url, output_dir):
    """使用 yt-dlp 下载单文件 MP4"""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'b', 
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_path = os.path.join(output_dir, f"{info['id']}.mp4")
        return video_path, info.get('title', '未命名视频')

def transcribe_with_siliconflow(file_path, api_key):
    """调用硅基流动 SenseVoice API 进行极速识别"""
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "video/mp4")}
        data = {"model": "FunAudioLLM/SenseVoiceSmall"}
        response = requests.post(url, headers=headers, files=files, data=data)
        
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return f"API识别报错: {response.status_code} - {response.text}"

def process_douyin_text(raw_input):
    """Agent 调用的主入口函数"""
    SF_API_KEY = os.environ.get("SF_API_KEY")
    if not SF_API_KEY:
        return "执行失败：系统未配置硅基流动 API Key (SF_API_KEY环境变量)。"

    # 1. 自动从文案中提取纯净链接
    clean_url = extract_url(raw_input)
    if not clean_url:
        return "执行失败：未在您的输入中检测到有效的 http/https 链接。"

    output_dir = "./temp_douyin"
    video_path = None
    
    try:
        # 2. 下载视频
        video_path, title = download_video_only(clean_url, output_dir)
        
        # 3. 云端提取文案
        transcript = transcribe_with_siliconflow(video_path, SF_API_KEY)
        
        # 4. 清理临时视频文件
        if os.path.exists(video_path):
            os.remove(video_path)
            
        if not transcript.strip():
            return f"视频《{title}》提取完毕，但未检测到有效语音。"
            
        # 5. 组装返回给 Agent 的纯文本结果
        result = f"【视频标题】: {title}\n【原始转录文案】:\n{transcript}"
        return result
        
    except Exception as e:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        return f"执行过程中发生异常: {str(e)}"

if __name__ == "__main__":
    # 本地测试代码
    import sys
    test_input = sys.argv[1] if len(sys.argv) > 1 else "5.10 复制打开抖音... https://v.douyin.com/LlSh03J3OIY/ QkC:/ f@O.KW"
    print(process_douyin_text(test_input))