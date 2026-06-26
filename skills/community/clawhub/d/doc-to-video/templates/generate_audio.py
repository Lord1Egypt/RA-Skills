#!/usr/bin/env python3
"""
Doc to Video: 配音生成脚本模板
=================================
用法：复制此文件，修改 SCENES 列表中的旁白文本，然后运行：

    python3 generate_audio.py

生成的文件保存在 audio/ 目录下（.m4a 格式）。

模板版本：v1.0.1（已修 file_list.txt 路径 bug）
"""

import asyncio, edge_tts, os

# ============================================================
# 在这里修改配音内容
# ============================================================
# 格式：(文件前缀, "旁白文本")
# 文件前缀不要有空格，用于生成 00_title.m4a, 01_chapter1.m4a 等文件
# 每段建议 100-200 字，对应 15-30 秒配音

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
# 在这里修改语音参数
# ============================================================
# 推荐中文 voices：
#   zh-CN-XiaoxiaoNeural  - 女声，自然流畅（默认推荐）
#   zh-CN-YunjianNeural   - 男声
#   zh-CN-YunxiNeural     - 男声，有故事感
#   zh-CN-XiaoyiNeural    - 女声，柔和
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
    print(f"  -> {scene_id}...")
    try:
        cm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
        await cm.save(m4a)
        size = os.path.getsize(m4a)
        print(f"    OK ({scene_id}, {size//1024}KB)")
    except Exception as e:
        print(f"    FAILED ({scene_id}): {e}")


async def main() -> None:
    print(f"AI  配音生成工具")
    print(f"   Voice : {VOICE} ({RATE} / {PITCH})")
    print(f"   场景数: {len(SCENES)}")
    print(f"   输出  : {OUT_DIR}/\n")

    await asyncio.gather(*[gen(sid, txt) for sid, txt in SCENES])

    # 关键：file_list.txt 里的路径必须相对 list 自身所在目录（audio/），
    # 所以直接用裸文件名，不要加 "audio/" 前缀
    files = sorted([f for f in os.listdir(OUT_DIR) if f.endswith(".m4a")])
    list_path = os.path.join(OUT_DIR, "file_list.txt")
    with open(list_path, "w") as f:
        for fname in files:
            f.write(f"file '{fname}'\n")  # 注意：不要写 audio/{fname}

    print(f"\nFile list: {list_path} ({len(files)} files)")
    print("\nNext steps:")
    print("   1. Measure total: python3 -c \"import subprocess,os; t=sum(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',f'audio/{f}']).decode()) for f in os.listdir('audio') if f.endswith('.m4a')); print(f'{t:.2f}s')\"")
    print("   2. Concat (must re-encode): ffmpeg -y -f concat -safe 0 -i audio/file_list.txt -c:a aac -b:a 128k audio/combined.m4a")
    print("   3. If total < 180s, accelerate: ffmpeg -y -i audio/combined.m4a -filter:a \"atempo=1.2,atempo=1.2\" -c:a aac -b:a 128k audio/combined.m4a")


if __name__ == "__main__":
    asyncio.run(main())
