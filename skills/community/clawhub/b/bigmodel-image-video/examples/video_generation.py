#!/usr/bin/env python3
"""视频生成示例"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

from image_video import generate_video, wait_for_video

# 步骤 1: 启动视频生成
video = generate_video(
    prompt="一朵花在阳光下缓缓开放",
    model="cogvideox-flash",
    duration=5,
)
task_id = video["id"]
print(f"任务 ID: {task_id}")
print("等待视频生成完成...")

# 步骤 2: 等待生成完成
final = wait_for_video(task_id, max_wait_time=180000)
video_url = final["video_result"][0]["url"]
print(f"视频 URL: {video_url}")

if final["video_result"][0].get("cover_image_url"):
    print(f"封面 URL: {final["video_result"][0]['cover_image_url']}")
