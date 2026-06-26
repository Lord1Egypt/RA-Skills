#!/usr/bin/env bash
# 从设计框架文件中提取尺寸，转换为标准宽高比字符串
# 用法: ./extract_ratio.sh <framework_file>
# 输出: 标准宽高比如 16:9 / 9:16 / 1:1，无法识别时输出空字符串

FRAMEWORK_FILE="${1:-}"
if [ -z "$FRAMEWORK_FILE" ]; then
  exit 0
fi

python3 << PYEOF
import re, sys

try:
    with open("$FRAMEWORK_FILE") as f:
        text = f.read()
except:
    sys.exit(0)

# 支持的标准宽高比
SUPPORTED = [
    (1, 1), (2, 3), (3, 2), (3, 4), (4, 3),
    (4, 5), (5, 4), (9, 16), (16, 9), (21, 9)
]

def ratio_diff(r1w, r1h, r2w, r2h):
    return abs(r1w / r1h - r2w / r2h)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def best_match(w, h):
    if w <= 0 or h <= 0:
        return None
    g = gcd(w, h)
    rw, rh = w // g, h // g
    best = min(SUPPORTED, key=lambda r: ratio_diff(rw, rh, r[0], r[1]))
    # 超过阈值则视为无法匹配（防止差异过大强行匹配）
    if ratio_diff(rw, rh, best[0], best[1]) > 0.3:
        return None
    return best

sizes = []

# ① 像素尺寸格式：1920×1080 / 1920x1080 / 1920*1080
for m in re.finditer(r'(\d{3,5})\s*[×xX\*]\s*(\d{3,5})', text):
    w, h = int(m.group(1)), int(m.group(2))
    if 100 <= w <= 8000 and 100 <= h <= 8000:
        sizes.append((w, h))

# ② 直接写比例格式：16:9 / 9:16 / 16比9 / 16／9
# 只在尺寸/规格/比例/输出等关键词附近匹配，避免误匹配版本号等
ratio_context = re.findall(
    r'(?:尺寸|规格|比例|输出|size|ratio|aspect)[^\n]{0,30}?(\d{1,2})\s*[:：比\/／]\s*(\d{1,2})',
    text, re.IGNORECASE
)
# 全局也匹配标准比例直接出现（如 "16:9"）
ratio_global = re.findall(r'\b(\d{1,2})\s*:\s*(\d{1,2})\b', text)

for m in ratio_context + ratio_global:
    w, h = int(m[0]), int(m[1])
    # 过滤掉明显不是宽高比的数字（如年份1920:1080会被像素格式捕获，这里只处理小数字）
    if 1 <= w <= 32 and 1 <= h <= 32:
        sizes.append((w * 100, h * 100))  # 等比扩大便于gcd计算

if not sizes:
    print("", end="")
    sys.exit(0)

# 取第一个有效匹配
for w, h in sizes:
    result = best_match(w, h)
    if result:
        print(f"{result[0]}:{result[1]}", end="")
        sys.exit(0)

print("", end="")
PYEOF
