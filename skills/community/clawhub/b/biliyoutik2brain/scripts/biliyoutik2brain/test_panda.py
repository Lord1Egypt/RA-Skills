"""测试 P1 知识注入: 熊猫技术分析社区"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

import asyncio
from core.pipeline import process

async def run():
    url = "https://www.bilibili.com/video/BV1529aBSETF"
    print(f"=== 熊猫测试: {url} ===")
    
    # P1检测
    know_file = os.path.expanduser("~/openclaw/workspace/storage/knowledge/熊猫技术分析社区.md")
    if os.path.exists(know_file):
        ksize = os.path.getsize(know_file)
        print(f"[P1] 知识库存在: {ksize}字节")
    else:
        print("[P1] ⚠️ 未找到知识库")
    
    start = time.time()
    result = await process(url)
    elapsed = time.time() - start
    
    if result and not result.error:
        print(f"\n=== 完成: {elapsed:.1f}s ===")
        print(f"文本: {len(result.plain_text)}字")
        print(f"分析: {json.dumps(result.analysis, ensure_ascii=False)[:200] if result.analysis else 'None'}")
    else:
        print(f"\n=== 完成: {elapsed:.1f}s (失败) ===")
        print(f"错误: {result.error if result else 'None'}")

if __name__ == "__main__":
    asyncio.run(run())
