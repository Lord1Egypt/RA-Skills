import base64
import os
import pathlib
import sys
from openai import OpenAI

# 配置百炼参数
API_KEY = 'sk-76735bc919a549a7a643f6b401815840'
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def extract_audio(video_path, audio_path):
    print(f"正在从视频提取音频并极致压缩: {video_path}")
    # 压缩为 16k mono mp3, 32k 码率以确保 Base64 编码后不超过 10MB (约支持 10-15 分钟视频)
    cmd = f'ffmpeg -y -i "{video_path}" -vn -ar 16000 -ac 1 -ab 32k "{audio_path}" -loglevel error'
    os.system(cmd)
    return os.path.exists(audio_path)

def transcribe_with_data_uri(audio_path):
    print(f"正在将音频转换为 Data URI 格式...")
    file_path_obj = pathlib.Path(audio_path)
    if not file_path_obj.exists():
        return f"音频文件不存在: {audio_path}"
    
    # 转换为 Data URI 格式: data:audio/mpeg;base64,<data>
    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    
    print(f"正在调用 qwen3-asr-flash 模型 (Data URI 模式)...")
    try:
        completion = client.chat.completions.create(
            model="qwen3-asr-flash",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": data_uri
                            }
                        },
                        {
                            "type": "text",
                            "text": "请将这段音频转录为文字，并分段总结核心观点。"
                        }
                    ]
                }
            ],
            extra_body={
                "asr_options": {
                    "enable_itn": False
                }
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"转录失败: {str(e)}"

def run_skill(video_input):
    if not os.path.exists(video_input):
        print(f"错误: 找不到输入文件 {video_input}")
        return

    # 如果输入是视频，提取音频；如果是音频，直接处理
    if video_input.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
        audio_tmp = "temp_audio_uri_skill.mp3"
        if not extract_audio(video_input, audio_tmp):
            print("音频提取失败。")
            return
    else:
        audio_tmp = video_input

    result = transcribe_with_data_uri(audio_tmp)
    print("\n=== 处理结果 ===\n")
    print(result)
    
    # 保存结果
    output_txt = video_input.rsplit('.', 1)[0] + "_summary_v3.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\n✅ 结果已保存至: {output_txt}")
    
    # 清理临时文件
    if audio_tmp == "temp_audio_uri_skill.mp3" and os.path.exists(audio_tmp):
        os.remove(audio_tmp)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_skill(sys.argv[1])
    else:
        print("用法: python audio_summary_v3.py <文件路径>")
