import os
import json
import requests
from openai import OpenAI

def format_timestamp(seconds: float) -> str:
    """将秒数转换为 SRT 标准时间戳 (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def split_srt(srt_content: str, batch_size: int = 30):
    """拆分长字幕，防止大模型翻译时上下文超限或截断"""
    lines = srt_content.strip().split('\n\n')
    for i in range(0, len(lines), batch_size):
        yield '\n\n'.join(lines[i:i + batch_size])

def generate_bilingual_subtitles(audio_path: str) -> str:
    """
    提取本地音频文件的原始外文字幕，并将其翻译为带有标准时间轴的中文 SRT 格式字幕文件。
    
    :param audio_path: 必须是本地音频文件（如 .mp3 或 .wav）的绝对路径。
    :return: 成功时返回生成的中文 SRT 字幕文件的绝对路径，失败时返回错误说明字符串。
    """
    
    # 1. 从环境变量动态获取配置 (提高安全性与环境适配性)
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    LLM_API_KEY = os.environ.get("LLM_API_KEY") # 你的 DeepSeek 等翻译大模型 Key
    LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

    # 校验环境与参数
    if not GROQ_API_KEY or not LLM_API_KEY:
        return "执行失败：系统环境变量中未找到 GROQ_API_KEY 或 LLM_API_KEY，请先配置。"
    if not os.path.exists(audio_path):
        return f"执行失败：找不到指定的音频文件路径 {audio_path}。"

    print(f"[Skill 运行中] 开始处理音频: {audio_path}")

    # 2. 调用 Groq (Whisper) 提取时间轴
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    try:
        with open(audio_path, "rb") as f:
            files = {"file": f}
            data = {"model": "whisper-large-v3", "response_format": "verbose_json"}
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
    except Exception as e:
        return f"执行失败：调用 Groq 接口提取音频发生异常 - {str(e)}"
        
    try:
        result_json = response.json()
        segments = result_json.get("segments", [])
        if not segments:
            return "执行失败：Groq 接口返回成功，但未解析出任何有效的时间轴片段。"
            
        raw_srt = ""
        for i, segment in enumerate(segments):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            raw_srt += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
            
    except Exception as e:
        return f"执行失败：解析 Groq 数据为 SRT 格式时发生异常 - {str(e)}"

    # 保存原文备份
    base_name = os.path.splitext(audio_path)[0]
    source_srt_path = f"{base_name}_source.srt"
    try:
        with open(source_srt_path, "w", encoding="utf-8-sig") as f: 
            f.write(raw_srt)
    except IOError:
        pass # 原文备份失败不影响主流程

    # 3. 大模型分批翻译
    print("[Skill 运行中] 时间轴提取成功，开始分批翻译...")
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    translated_segments = []
    
    for i, chunk in enumerate(split_srt(raw_srt)):
        prompt = "你是一个专业的字幕翻译。请将以下英文字幕翻译为中文。严格保留序号和时间轴，只翻译文本。不要输出任何解释和多余的换行。"
        try:
            res = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": chunk}
                ],
                temperature=0.1
            )
            translated_segments.append(res.choices[0].message.content)
        except Exception as e:
            print(f"[Skill 警告] 第 {i+1} 批翻译异常，将回退为原文: {e}")
            translated_segments.append(chunk)

    # 4. 合并并输出最终结果
    final_content = "\n\n".join(translated_segments)
    target_srt_path = f"{base_name}_zh.srt"
    
    try:
        with open(target_srt_path, "w", encoding="utf-8-sig") as f:
            f.write(final_content)
        return f"成功！已提取并翻译字幕，文件保存在：{target_srt_path}"
    except Exception as e:
        return f"执行失败：无法写入最终的字幕文件 - {str(e)}"