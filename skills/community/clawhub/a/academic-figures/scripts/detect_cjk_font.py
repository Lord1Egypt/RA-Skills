#!/usr/bin/env python3
"""Auto-detect CJK fonts on the system for matplotlib. Returns font path or None."""
import subprocess, os, json

CJK_FONT_PRIORITY = [
    # Noto CJK (most Linux distros)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansSC-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    # Windows
    "C:/Windows/Fonts/msyh.ttc",       # Microsoft YaHei
    "C:/Windows/Fonts/simhei.ttf",      # SimHei
    "C:/Windows/Fonts/simsun.ttc",      # SimSun
    # Common Linux
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

if os.environ.get("AF_SKETCH") == "1":
    # v7.6.1 sketch 手绘模式：中文走清晰手写字形（霞鹜文楷=清晰楷体；清松潦草备选）
    # （环境变量仅在 --style sketch 进程树内置位，全局默认不受影响）
    CJK_FONT_PRIORITY = [
        os.path.expanduser("~/.local/share/fonts/LXGWWenKai-Regular.ttf"),
        os.path.expanduser("~/.local/share/fonts/ChienShongHandwriting7-Piaoyi.ttf"),
    ] + CJK_FONT_PRIORITY

def detect_cjk_font():
    """Return path to first available CJK font, or None."""
    for p in CJK_FONT_PRIORITY:
        if os.path.exists(p):
            return p
    # Fallback: fc-list
    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh", "file"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            # Return first font path
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    return line.split(':')[0].strip()
    except Exception:
        pass
    return None

if __name__ == "__main__":
    font = detect_cjk_font()
    if font:
        print(json.dumps({"found": True, "path": font, "name": os.path.basename(font)}))
    else:
        print(json.dumps({"found": False, "path": None}))
