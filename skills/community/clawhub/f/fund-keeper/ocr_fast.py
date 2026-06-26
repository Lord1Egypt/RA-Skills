import easyocr
import sys
import os
import re

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Set console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Check if models are already downloaded
model_dir = os.path.expanduser("~/.EasyOCR/model")
if os.path.exists(model_dir):
    print(f"Models found at: {model_dir}")
else:
    print(f"Models not found, will download to: {model_dir}")

# Initialize reader
print("Initializing EasyOCR (this may take a moment)...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

# Read image
image_path = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\Administrator\\.openclaw\\media\\inbound\\89255283-ae03-4d8c-8014-a2bd4130251c.webp"
print(f"Processing: {os.path.basename(image_path)}")

results = reader.readtext(image_path, paragraph=False)

print("\n=== 识别结果 ===")
for (bbox, text, prob) in results:
    print(f"[{prob:.2f}] {text}")

# Look for 6-digit numbers (fund codes)
import re
print("\n=== 基金代码 (6 位数字) ===")
found_codes = []
for (bbox, text, prob) in results:
    codes = re.findall(r'\b\d{6}\b', text)
    for code in codes:
        if code not in found_codes:
            found_codes.append(code)
            print(f"找到：{code}")

if not found_codes:
    print("未找到 6 位基金代码")
    print("\n=== 识别到的基金名称关键词 ===")
    keywords = ['华泰', '广发', '易方达', '芯片', 'ETF', '联接', '纳斯达克', '沪深']
    for (bbox, text, prob) in results:
        for kw in keywords:
            if kw in text:
                print(f"  {text}")
