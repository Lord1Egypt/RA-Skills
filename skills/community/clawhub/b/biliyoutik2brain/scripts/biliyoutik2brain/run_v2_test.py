#!/usr/bin/env python3
"""v2 Task Graph 管线测试"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.getcwd()))
sys.path.insert(0, os.getcwd())

from biliyoutik2brain.core.pipeline import process, process_linear, build_pipeline_graph
from biliyoutik2brain.core.pipeline_graph import Graph

URL = "https://www.bilibili.com/video/BV1JFz3B8Ehn"
# "黄金创历史新高！华尔街量化系统抓突破！" 7分42秒

print("=" * 60)
print("P1 Task Graph v2 测试")
print(f"视频: {URL}")
print("=" * 60)

# 运行新版（完整执行）
start = time.time()
result = process(URL)
total = time.time() - start

print()
print("=" * 60)
print("测试结果")
print("=" * 60)
print(f"管线耗时: {total:.1f}s")
print(f"状态: {'成功' if not result.error else f'失败: {result.error}'}")
if result.file_path:
    print(f"保存: {result.file_path}")
if result.corrected_text:
    print(f"修复文本: {len(result.corrected_text)} 字符")
if result.analysis:
    summary = result.analysis.get('summary', '')
    kw = result.analysis.get('keywords', [])
    print(f"摘要: {summary[:80]}")
    print(f"关键词: {kw[:6]}")
