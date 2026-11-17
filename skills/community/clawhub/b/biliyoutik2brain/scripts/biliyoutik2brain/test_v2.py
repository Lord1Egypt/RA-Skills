"""biliyoutik2brain v2 测试：运行一个视频并输出各阶段耗时"""
import sys, os, time

# 确保 workspace 版优先
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

# 禁用 skill 版
for p in list(sys.path):
    if ".openclaw/skills" in p:
        sys.path.remove(p)

import asyncio
from core.pipeline import process
from core.config import record_task

async def run_test():
    url = "https://www.bilibili.com/video/BV1nTo4BQEuC"
    print(f"=== biliyoutik2brain v2 测试 ===")
    print(f"视频: {url}")
    print(f"时间: {time.strftime('%H:%M:%S')}")
    print()
    
    start = time.time()
    result = await process(url)
    elapsed = time.time() - start
    
    print(f"\n=== 完成: {elapsed:.1f}s ===")
    
    # 分析状态
    if result and not result.error:
        print(f"文本: {len(result.plain_text)} 字符")
        print(f"分析结果: {result.analysis is not None}")
        print(f"知识库: {result.knowledge_updated}")
        print(f"文件: {result.output_file}")
    else:
        print(f"错误: {result.error if result else 'No result'}")

if __name__ == "__main__":
    result = asyncio.run(run_test())
