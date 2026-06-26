#!/usr/bin/env python3
"""
briefing-visualizer 核心脚本：
将 HTML 简报转化为手机长图

用法：
    python3 process_briefing.py <html文件> <底部通栏图> <输出文件>

示例：
    python3 process_briefing.py briefing.html banner.png final.jpg
"""
import os
import sys
import subprocess
from PIL import Image

# ============ 配置区（可按需修改） ============
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCREENSHOT_W, SCREENSHOT_H = 390, 10000   # 截图窗口宽高
VIRTUAL_TIME = 3000                        # 等待渲染时间(ms)
BOTTOM_BLANK_MARGIN = 30                    # 裁剪底部时额外保留的行数
BG_DIFF_THRESHOLD = 10                      # 内容判定阈值
PURE_BG_THRESHOLD = 5                       # 纯背景色判定阈值

# ============================================

def get_chrome_path():
    """查找 Chrome"""
    if os.path.exists(CHROME):
        return CHROME
    for path in [
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    ]:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("未找到 Chrome，请安装 Google Chrome 或配置 CHROME 路径")

def screenshot(html_path, output_path):
    """Chrome headless 全页面截图"""
    chrome = get_chrome_path()
    cmd = [
        chrome,
        "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars",
        "--screenshot=" + output_path,
        f"--window-size={SCREENSHOT_W},{SCREENSHOT_H}",
        f"--virtual-time-budget={VIRTUAL_TIME}",
        "file://" + os.path.abspath(html_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    ok = os.path.exists(output_path)
    print(f"  Chrome exit={result.returncode}, file_exists={ok}")
    return ok

def crop_bottom_blank(img):
    """
    裁剪掉底部的纯背景色空白区域。
    策略：先按行扫描底部区域，识别连续纯色行，然后裁剪。
    """
    w, h = img.size
    pixels = img.load()

    # 取 body 背景色：取图片中间某行左侧的代表性颜色
    # 若左上角偏深色（被渐变头部占用），则取 body 区域
    body_bg_candidates = [pixels[5, h//3], pixels[5, h//2]]
    # 选 RGB 和最接近 (255,248,240) 的候选
    TARGET_BODY_BG = (255, 248, 240)
    bg = min(body_bg_candidates,
             key=lambda p: sum(abs(a-b) for a,b in zip(p, TARGET_BODY_BG)))

    print(f"  Body BG ref: {bg}")

    # 从底部向上扫描，连续纯背景色行数
    bottom_blank = 0
    for y in range(h - 1, max(h - 300, 0), -1):
        is_pure_bg = True
        for x in range(0, w, 5):
            p = pixels[x, y]
            diff = sum(abs(a-b) for a,b in zip(p, bg))
            if diff > PURE_BG_THRESHOLD:
                is_pure_bg = False
                break
        if is_pure_bg:
            bottom_blank += 1
        else:
            break

    print(f"  Bottom pure-bg rows: {bottom_blank}")

    # 再从剩余底部向上找最后一个内容行
    last_content = h - bottom_blank - 1
    for y in range(last_content, -1, -1):
        has_content = False
        for x in range(0, w, 10):
            p = pixels[x, y]
            diff = sum(abs(a-b) for a,b in zip(p, bg))
            if diff > BG_DIFF_THRESHOLD:
                has_content = True
                break
        if has_content:
            last_content = y
            break

    if last_content < 10:
        last_content = h - bottom_blank - 1

    crop_h = last_content + BOTTOM_BLANK_MARGIN
    cropped = img.crop((0, 0, w, crop_h))
    print(f"  Cropped: {cropped.size} (from {w}x{h})")
    return cropped

def crop_top(img):
    """裁剪顶部纯色（header渐变区以下的内容开始点）"""
    w, h = img.size
    pixels = img.load()
    bg = pixels[0, 0]
    first_content = 0
    for y in range(0, h):
        has_content = False
        for x in range(0, w, 10):
            p = pixels[x, y]
            diff = sum(abs(a-b) for a,b in zip(p, bg))
            if diff > BG_DIFF_THRESHOLD:
                has_content = True
                break
        if has_content:
            first_content = y
            break
    if first_content > 5:
        cropped = img.crop((0, first_content, w, h))
        print(f"  Top cropped: {cropped.size}")
        return cropped
    return img

def stitch_bottom(report_img, bottom_path):
    """将底部通栏图拼接至报告底部"""
    if not os.path.exists(bottom_path):
        print(f"  Warning: bottom image not found: {bottom_path}")
        return report_img

    bottom = Image.open(bottom_path).convert("RGB")
    w = report_img.width
    h = int(bottom.height * w / bottom.width)
    bottom = bottom.resize((w, h), Image.LANCZOS)
    print(f"  Bottom resized to: {bottom.size}")

    total = Image.new("RGB", (w, report_img.height + bottom.height), (0, 0, 0))
    total.paste(report_img, (0, 0))
    total.paste(bottom, (0, report_img.height))
    return total

def main():
    if len(sys.argv) < 4:
        print("用法: python3 process_briefing.py <html文件> <底部通栏图> <输出文件>")
        sys.exit(1)

    html_file = sys.argv[1]
    bottom_img = sys.argv[2]
    output_file = sys.argv[3]

    if not os.path.exists(html_file):
        print(f"错误: HTML文件不存在: {html_file}")
        sys.exit(1)

    raw_path = os.path.join(os.path.dirname(output_file) or ".", "raw_briefing.png")

    # Step 1: 截图
    print(f"=== Screenshot ===")
    ok = screenshot(html_file, raw_path)
    if not ok:
        print("截图失败！")
        sys.exit(1)

    # Step 2: 裁剪
    print(f"=== Crop ===")
    img = Image.open(raw_path).convert("RGB")
    cropped = crop_bottom_blank(img)
    cropped.save(raw_path.replace("raw_", "cropped_"))

    # Step 3: 拼接底部
    print(f"=== Stitch ===")
    final = stitch_bottom(cropped, bottom_img)
    final.save(output_file, quality=95)

    size_kb = os.path.getsize(output_file) / 1024
    print(f"\n✅ Done: {final.size} -> {output_file} ({size_kb:.0f}KB)")

if __name__ == "__main__":
    main()
