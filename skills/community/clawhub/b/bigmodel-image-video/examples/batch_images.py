#!/usr/bin/env python3
"""批量图片生成示例"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

from image_video import batch_generate_images

# 批量生成多张图片
prompts = [
    "日出时分的山景",
    "蓝色大海的海滩",
    "秋天的森林小路",
    "雪后的村庄"
]

results = batch_generate_images(
    prompts=prompts,
    model="cogview-3-flash",
    max_concurrent=2
)

for i, r in enumerate(results):
    print(f"图片 {i+1}: {r['data'][0]['url']}")
