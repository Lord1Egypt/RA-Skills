#!/usr/bin/env python3
"""
voice_test.py — 生成 6 个候选 voice 的对比样本（v1.0.4 新增）
========================================================

配套 SKILL.md Step 0：选 voice 之前先试听，避免事后改 voice 触发完整迭代 loop。

用法：
    python3 templates/voice_test.py
    open /tmp  # Finder 打开，逐个点 voice_*.m4a 用 QuickTime 试听

输出：
    /tmp/voice_xiaoxiao.m4a
    /tmp/voice_yunxi.m4a
    /tmp/voice_yunjian.m4a
    /tmp/voice_xiaoyi.m4a
    /tmp/voice_yunyang.m4a
    /tmp/voice_yunxia.m4a

每段 9.5 秒，内容是 "智能合约运行在区块链上，是不可逆的执行环境。
一旦执行失败，状态必须完全回滚。" —— 覆盖技术教程类典型句式。

也可以自己改 SAMPLE 变量。
"""
import asyncio
import edge_tts

SAMPLE = "智能合约运行在区块链上，是不可逆的执行环境。一旦执行失败，状态必须完全回滚。"

# 推荐试听的中文 voices（按 macos-gotchas.md §8 推荐排序）
VOICES = [
    ("xiaoxiao",  "zh-CN-XiaoxiaoNeural"),
    ("yunxi",     "zh-CN-YunxiNeural"),
    ("yunjian",   "zh-CN-YunjianNeural"),
    ("xiaoyi",    "zh-CN-XiaoyiNeural"),
    ("yunyang",   "zh-CN-YunyangNeural"),
    ("yunxia",    "zh-CN-YunxiaNeural"),
]


async def gen(name: str, voice: str) -> None:
    cm = edge_tts.Communicate(SAMPLE, voice)
    out = f"/tmp/voice_{name}.m4a"
    try:
        await cm.save(out)
        print(f"  ✓ {out}")
    except Exception as e:
        print(f"  ✗ {name} ({voice}): {type(e).__name__}: {e}")


async def main() -> None:
    print(f"🎙  生成 {len(VOICES)} 个 voice 对比样本到 /tmp/")
    print(f"   内容: {SAMPLE[:30]}...")
    print()
    await asyncio.gather(*[gen(n, v) for n, v in VOICES])
    print()
    print("👂 试听：open /tmp  # Finder 打开，逐个点 .m4a")


if __name__ == "__main__":
    asyncio.run(main())
