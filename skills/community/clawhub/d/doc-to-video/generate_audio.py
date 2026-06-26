#!/usr/bin/env python3
"""
Doc to Video: 配音生成脚本模板
=================================
用法：复制此文件，修改 SCENES 列表中的旁白文本，然后运行：

    python3 generate_audio.py

生成的文件保存在 audio/ 目录下（.m4a 格式）。
"""

import asyncio, edge_tts, os

# ============================================================
# ⚙️ 在这里修改配音内容
# ============================================================
# 格式：(文件前缀, "旁白文本")
# 文件前缀不要有空格，用于生成 00_title.m4a, 01_chapter1.m4a 等文件

SCENES = [
    ("00_title",    "欢迎观看本教程。本节介绍主要内容..."),
    ("01_chapter1", "第一章，首先介绍背景知识..."),
    ("02_chapter2", "第二章，讲解核心概念..."),
    ("03_chapter3", "第三章，实战操作演示..."),
    ("04_chapter4", "第四章，总结与建议..."),
    ("05_end",      "感谢观看！"),
    # 继续添加更多场景...
]

# ============================================================
# ⚙️ 在这里修改语音参数
# ============================================================
# 推荐中文 voices：
#   zh-CN-XiaoxiaoNeural  — 女声，自然流畅（默认推荐）
#   zh-CN-YunjianNeural   — 男声
#   zh-CN-YunxiNeural     — 男声，有故事感
#   zh-CN-XiaoyiNeural    — 女声，柔和
#
# rate: 语速，"+0%" 为正常，"+10%" 略快，"-10%" 略慢
# pitch: 音调，"+0Hz" 为正常

VOICE  = "zh-CN-XiaoxiaoNeural"
RATE   = "+0%"
PITCH  = "+0Hz"

# 输出目录（相对当前目录）
OUT_DIR = "audio"

# ============================================================
# 以下代码一般不需要修改
# ============================================================

os.makedirs(OUT_DIR, exist_ok=True)


async def gen(scene_id: str, text: str) -> None:
    """生成单个场景的配音文件。"""
    m4a = os.path.join(OUT_DIR, f"{scene_id}.m4a")
    if os.path.exists(m4a):
        print(f"  [skip] {scene_id} (文件已存在)")
        return
    print(f"  → 生成中: {scene_id}...")
    try:
        cm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await cm.save(m4a)
        size = os.path.getsize(m4a)
        print(f"    ✅ 完成 ({scene_id}, {size//1024}KB)")
    except Exception as e:
        print(f"    ❌ 失败 ({scene_id}): {e}")


async def list_available_voices() -> None:
    """列出所有可用的中文 voices（调试用）。"""
    voices = await edge_tts.list_voices()
    zh = [v for v in voices if v["Locale"].startswith("zh")]
    print("\n可用中文 voices：")
    for v in zh:
        print(f"  {v['ShortName']:30s} — {v['FriendlyName']}")
    print()


async def main() -> None:
    print(f"🎙️  配音生成工具")
    print(f"   Voice : {VOICE} ({RATE} / {PITCH})")
    print(f"   场景数: {len(SCENES)}")
    print(f"   输出  : {OUT_DIR}/\n")

    await asyncio.gather(*[gen(sid, txt) for sid, txt in SCENES])

    # 生成文件列表（用于 FFmpeg concat）
    files = sorted([f for f in os.listdir(OUT_DIR) if f.endswith(".m4a")])
    list_path = os.path.join(OUT_DIR, "file_list.txt")
    with open(list_path, "w") as f:
        for fname in files:
            f.write(f"file '{OUT_DIR}/{fname}'\n")

    print(f"\n📋 文件列表已生成: {list_path}")
    print(f"   共 {len(files)} 个音频文件")
    print("\n✨ 全部完成！下一步：")
    print("   1. 测量时长：for f in audio/*.m4a; do dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"$f\"); echo \"$f: ${dur}s\"; done")
    print("   2. 拼接音频：ffmpeg -y -f concat -safe 0 -i audio/file_list.txt -codec:a libmp3lame -qscale:a 2 audio/combined_raw.mp3")
    print("   3. 加速音频：ffmpeg -y -i audio/combined_raw.mp3 -filter:a \"atempo=1.31,atempo=1.31\" -codec:a aac -b:a 128k audio/combined_final.m4a")


if __name__ == "__main__":
    asyncio.run(main())
