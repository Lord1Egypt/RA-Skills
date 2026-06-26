import base64
import requests
from openai import OpenAI
import os
import sys
from pathlib import Path

# ===================== 配置 =====================
def load_api_key():
    # Try to read from secrets file first
    secrets_path = r"C:\Users\Administrator\.openclaw\secrets\openrouter.env"
    try:
        with open(secrets_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.split("=", 1)[1].strip(' "\'')
    except FileNotFoundError:
        pass
    # Fallback to environment variable
    return os.getenv("OPENROUTER_API_KEY")

API_KEY = load_api_key()
MODEL = os.getenv("OCR_MODEL", "baidu/qianfan-ocr-fast:free")
BASE_URL = os.getenv("OCR_BASE_URL", "https://openrouter.ai/api/v1")

def encode_image(image_path):
    """Encode local image to base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr.py <image_input> [prompt]")
        print("  image_input: URL or local file path to image")
        print("  prompt: Optional text prompt (default: 'OCR提取图片所有文字')")
        sys.exit(1)
    
    image_input = sys.argv[1]
    prompt_text = sys.argv[2] if len(sys.argv) > 2 else "OCR提取图片所有文字"
    
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    print("=" * 60)
    print("Starting OCR recognition with model: {}".format(MODEL))
    print("=" * 60)
    
    try:
        # 官方正确写法
        client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
        
        # Prepare message content
        content = [
            {"type": "text", "text": prompt_text}
        ]
        
        # Handle image input (URL or local file)
        if image_input.startswith(('http://', 'https://')):
            # URL case
            content.append({"type": "image_url", "image_url": {"url": image_input}})
        else:
            # Local file case
            base64_image = encode_image(image_input)
            if base64_image is None:
                sys.exit(1)
            content.append({
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        
        # 输出结果
        print("\n✅ OCR 识别结果：")
        print("-" * 60)
        print(completion.choices[0].message.content)
        print("-" * 60)

    except Exception as e:
        print(f"\n❌ 出错：{type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# 不闪退 - 只有在直接运行时才等待输入
if len(sys.argv) > 0 and __name__ == "__main__":
    print("\n" + "=" * 60)
    try:
        input("按回车键退出...")
    except:
        pass  # 在某些环境中input可能不可用