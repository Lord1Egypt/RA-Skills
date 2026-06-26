import os
import sys
from http import HTTPStatus

import dashscope
from dashscope.audio.asr import Recognition


if __name__ == "__main__":
    # Get audio file path from user
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = input("请输入音频文件路径: ").strip()

    if not os.path.exists(audio_file):
        print(f"Error: 文件不存在: {audio_file}")
        sys.exit(1)

    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
    dashscope.base_websocket_api_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"

    # 使用非流式调用方式（适合本地文件）
    recognition = Recognition(
        model="fun-asr-realtime",
        format="wav",
        sample_rate=16000,
        callback=None,
    )

    result = recognition.call(audio_file)
    if result.status_code == HTTPStatus.OK:
        sentence = result.get_sentence()
        if sentence:
            # 返回的是列表，提取所有文本
            if isinstance(sentence, list):
                texts = [s.get("text", "") for s in sentence if s.get("text")]
                full_text = "".join(texts)
                if full_text:
                    print(full_text)
            elif isinstance(sentence, dict) and "text" in sentence:
                print(sentence["text"])
    else:
        print(f"Error: {result.message}", file=sys.stderr)
        sys.exit(1)
