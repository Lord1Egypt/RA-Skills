#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板内容工厂
监控剪贴板 → 自动改写成多平台版本 → 保存到桌面
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
import argparse

# 剪贴板访问（跨平台兼容）
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        def get_clipboard():
            try:
                return root.clipboard_get()
            except Exception:
                return ""
        def set_clipboard(text):
            root.clipboard_clear()
            root.clipboard_append(text)
        HAS_TKINTER = True
    except Exception:
        HAS_TKINTER = False


# ============ 配置 ============

DEFAULT_OUTPUT = Path.home() / "Desktop" / "clipboard_content_factory"

# 平台配置
PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "emoji": "🔥",
        "title_len": 20,
        "body_len": 150,
        "hashtag_count": 6,
        "times": ["12:00", "18:00", "21:00"],
    },
    "xhs": {
        "name": "小红书",
        "emoji": "📕",
        "title_len": 25,
        "body_len": 500,
        "hashtag_count": 10,
        "times": ["08:00", "12:00", "20:00"],
    },
    "bilibili": {
        "name": "B站",
        "emoji": "📺",
        "title_len": 30,
        "body_len": 800,
        "hashtag_count": 8,
        "times": ["18:00", "22:00"],
    },
}

HASHTAG_POOL = [
    "#AI工具", "#AI写作", "#AI变现", "#干货分享", "#效率神器",
    "#自媒体", "#涨粉技巧", "#副业赚钱", "#科技数码", "#实用技巧",
    "#小红书运营", "#抖音运营", "#短视频制作", "#内容创作", "#AI助手",
    "#AI技能", "#自动化工具", "#效率提升", "#数字游民", "#被动收入",
]


# ============ 剪贴板工具 ============

def get_clipboard_text():
    """获取剪贴板文本"""
    if HAS_PYPERCLIP:
        try:
            return pyperclip.paste()
        except Exception:
            return ""
    elif HAS_TKINTER:
        try:
            return get_clipboard()
        except Exception:
            return ""
    else:
        # Fallback: 尝试PowerShell
        import subprocess
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-Clipboard"],
                capture_output=True, text=True, timeout=3
            )
            return result.stdout.strip()
        except Exception:
            return ""


def set_clipboard_text(text):
    """设置剪贴板文本"""
    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    elif HAS_TKINTER:
        try:
            set_clipboard(text)
            return True
        except Exception:
            return False
    else:
        import subprocess
        try:
            subprocess.run(
                ["powershell", "-Command", f"Set-Clipboard -Value '{text}'"],
                capture_output=True, timeout=3
            )
            return True
        except Exception:
            return False


# ============ 内容改写引擎 ============

def rewrite_for_platform(text, platform):
    """为指定平台改写内容"""
    cfg = PLATFORMS[platform]
    emoji = cfg["emoji"]

    # 提取核心信息
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    core_text = text.replace("\n", " ")[:100]

    # 生成平台专属标题
    title_templates = {
        "douyin": [
            f"没想到...{core_text[:8]}竟然这么简单！",
            f"学会这5点，{core_text[:10]}不再难",
            f"曝光！{core_text[:12]}的内幕",
            f"{core_text[:15]}，看完你就懂了",
        ],
        "xhs": [
            f"救命！{core_text[:8]}真的太绝了！",
            f"宝藏{core_text[:10]}分享✨建议收藏",
            f"新手必看！{core_text[:12]}完整攻略",
        ],
        "bilibili": [
            f"【{core_text[:10]}】深度解析",
            f"关于{core_text[:10]}，你可能不知道的事",
            f"{core_text[:10]}全攻略｜零基础到精通",
        ],
    }

    import random
    title = random.choice(title_templates.get(platform, title_templates["douyin"]))

    # 生成正文
    body_templates = {
        "douyin": f"{text[:100]}...\n\n#AI工具 #干货分享 #效率神器",
        "xhs": f"今天来聊聊{core_text[:15]}～\n\n💡 {text[:80]}...\n\n{' '.join(random.sample(HASHTAG_POOL, 6))}",
        "bilibili": f"**{core_text[:20]}**\n\n{text[:200]}...\n\n**总结：**\n{' '.join(random.sample(HASHTAG_POOL, 5))} #知识分享",
    }

    body = body_templates[platform]

    # 生成标签
    import random
    hashtags = random.sample(HASHTAG_POOL, cfg["hashtag_count"])

    return {
        "platform": cfg["name"],
        "emoji": emoji,
        "title": title,
        "body": body,
        "hashtags": hashtags,
        "best_times": cfg["times"],
        "cover_tip": f"封面建议：{emoji} {core_text[:8]}（大字+背景图）",
    }


def process_content(text, output_dir=None):
    """处理内容：改写所有平台版本"""
    if not text or len(text.strip()) < 5:
        return None

    text = text.strip()
    output_dir = output_dir or DEFAULT_OUTPUT

    # 创建日期目录
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_path = Path(output_dir) / date_str
    out_path.mkdir(parents=True, exist_ok=True)

    results = {}
    summary = {
        "original": text[:200],
        "original_hash": hashlib.md5(text.encode()).hexdigest()[:8],
        "platforms": {},
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(f"\n📋 原始内容: {text[:80]}...\n")

    for platform in ["douyin", "xhs", "bilibili"]:
        r = rewrite_for_platform(text, platform)
        results[platform] = r

        # 保存文件
        ext_map = {"douyin": "douyin", "xhs": "xhs", "bilibili": "bilibili"}
        filepath = out_path / f"{ext_map[platform]}_version.md"
        filepath.write_text(
            f"# {r['emoji']} {r['platform']}版本\n\n"
            f"## 标题\n{r['title']}\n\n"
            f"## 正文\n{r['body']}\n\n"
            f"## 话题标签\n{' '.join(r['hashtags'])}\n\n"
            f"## 封面建议\n{r['cover_tip']}\n\n"
            f"## 最佳发布时间\n" + "\n".join(f"- {t}" for t in r["best_times"]),
            encoding="utf-8"
        )

        summary["platforms"][platform] = {
            "title": r["title"],
            "hashtags": r["hashtags"],
        }

        print(f"  {r['emoji']} {r['platform']}: {r['title']}")

    # 保存总览
    (out_path / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return out_path, results


# ============ 核心逻辑 ============

last_hash = None


def check_and_process():
    """检查剪贴板，如有新内容则处理"""
    global last_hash

    text = get_clipboard_text()
    if not text:
        return None

    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]

    if text_hash == last_hash:
        return None  # 内容未变

    last_hash = text_hash
    return process_content(text)


def run_once():
    """单次运行"""
    result = check_and_process()
    if result:
        out_path, _ = result
        print(f"\n✅ 已保存到: {out_path}")
    else:
        print("📋 剪贴板内容无变化或为空")


def run_watch(interval=3):
    """持续监控模式"""
    print(f"👀 开始监控剪贴板（每{interval}秒检查一次）...")
    print("按 Ctrl+C 停止\n")

    try:
        while True:
            check_and_process()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n👋 监控已停止")


# ============ 入口 ============

def main():
    parser = argparse.ArgumentParser(description="剪贴板内容工厂")
    parser.add_argument("--once", action="store_true", help="一次性处理当前剪贴板")
    parser.add_argument("--watch", action="store_true", help="持续监控剪贴板")
    parser.add_argument("--interval", type=int, default=3, help="监控间隔（秒）")
    parser.add_argument("--output", type=str, default=None, help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT

    if args.watch:
        run_watch(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
