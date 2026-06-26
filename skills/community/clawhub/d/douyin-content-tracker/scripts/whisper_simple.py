#!/usr/bin/env python3
"""
使用 Whisper 进行语音识别 - 单文件版本
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import whisper
from pathlib import Path

audio_dir = Path("/Users/liyong/DouyinContentTracker/audio/周凯谈烘焙")
subtitle_dir = Path("/Users/liyong/DouyinContentTracker/subtitles/周凯谈烘焙")
subtitle_dir.mkdir(parents=True, exist_ok=True)

# 加载 small 模型
print("加载 Whisper small 模型...")
model = whisper.load_model("small", download_root="/Users/liyong/workskills/douyin-content-tracker-skill/models")

# 处理每个音频文件
for audio_file in sorted(audio_dir.glob("*.m4a")):
    print(f"\n处理：{audio_file.name}")
    video_id = audio_file.stem
    
    # 语音识别
    result = model.transcribe(str(audio_file), language="zh")
    text = result["text"].strip()
    
    # 保存字幕
    output_file = subtitle_dir / f"{video_id}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# 视频 {video_id}\n\n")
        f.write(text)
    
    print(f"  → 已保存：{output_file}")
    print(f"  → 转写内容：{text[:200]}...")

print("\n✅ 所有音频处理完成！")
