import easyocr
import sys
import re

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Initialize reader (only once, models are cached)
print("Initializing EasyOCR...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

# Read image
image_path = sys.argv[1] if len(sys.argv) > 1 else "C:\\Users\\Administrator\\.openclaw\\media\\inbound\\98f5109c-8990-4516-bf83-6f2e754c2640.webp"
print(f"Reading: {image_path}")

results = reader.readtext(image_path)

print("\n=== OCR Results ===")
for (bbox, text, prob) in results:
    # Print in ASCII-safe way
    text_ascii = text.encode('utf-8', errors='ignore').decode('utf-8')
    print(f"Text: {text_ascii} (confidence: {prob:.2f})")

# Look for 6-digit numbers (fund codes)
import re
print("\n=== Potential Fund Codes ===")
for (bbox, text, prob) in results:
    codes = re.findall(r'\d{6}', text)
    for code in codes:
        print(f"Found code: {code}")
