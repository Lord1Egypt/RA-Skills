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

def analyze_image(client, image_input, prompt):
    """Analyze image with given prompt"""
    # Prepare message content
    content = [
        {"type": "text", "text": prompt}
    ]
    
    # Handle image input (URL or local file)
    if image_input.startswith(('http://', 'https://')):
        # URL case
        content.append({"type": "image_url", "image_url": {"url": image_input}})
    else:
        # Local file case
        base64_image = encode_image(image_input)
        if base64_image is None:
            return None
        content.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr.py <image_input> [ocr_prompt]")
        print("  image_input: URL or local file path to image")
        print("  ocr_prompt: Optional text prompt for OCR (default: 'OCR提取图片所有文字')")
        sys.exit(1)
    
    image_input = sys.argv[1]
    ocr_prompt = sys.argv[2] if len(sys.argv) > 2 else "OCR提取图片所有文字"
    
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    print("=" * 60)
    print("Starting image analysis with model: {}".format(MODEL))
    print("=" * 60)
    
    try:
        # 官方正确写法
        client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
        
        # Step 1: Describe the image
        print("\nStep 1: Describing image...")
        description_prompt = "请详细描述这张图片的内容，包括物体、场景、颜色等细节。"
        description = analyze_image(client, image_input, description_prompt)
        
        # Step 2: Extract text (OCR)
        print("\nStep 2: Extracting text from image...")
        ocr_result = analyze_image(client, image_input, ocr_prompt)
        
        # 输出结果
        print("\n" + "=" * 60)
        print("IMAGE DESCRIPTION:")
        print("-" * 60)
        print(description if description else "Failed to get description")
        print("-" * 60)
        
        print("\n" + "=" * 60)
        print("OCR RECOGNITION RESULT:")
        print("-" * 60)
        print(ocr_result if ocr_result else "No text found or failed to extract")
        print("-" * 60)

    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# 不闪退 - 只有在直接运行时才等待输入
if len(sys.argv) > 0 and __name__ == "__main__":
    print("\n" + "=" * 60)
    try:
        input("Press Enter to exit...")
    except:
        pass  # 在某些环境中input可能不可用