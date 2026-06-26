#!/usr/bin/env python3
"""简单图片生成示例"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

from image_video import generate_image

# 生成一张简单的图片
result = generate_image(
    prompt="一只可爱的橘猫",
    model="cogview-3-flash",
)

print(f"图片 URL: {result['data'][0]['url']}")
