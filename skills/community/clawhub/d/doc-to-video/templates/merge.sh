#!/bin/bash
# 合并 Remotion 渲染的视频和 edge-tts 配音
# 用法：cd <project> && ./merge.sh
set -e
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "Step 1: 第一次渲染（确认实际帧数）"
npx remotion render src/index.tsx MyVideo out/temp.mp4 \
  --browser-executable="$CHROME" --concurrency=2

ACTUAL_FRAMES=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=nb_frames -of csv=p=0 out/temp.mp4)
echo "  -> 实际帧数: $ACTUAL_FRAMES"
echo "  -> 请用此值修正 src/index.tsx 的 durationInFrames 和 src/Scene.tsx 的 F[]"

echo ""
echo "Step 2: 第二遍渲染（用修正后的 F[]）"
npx remotion render src/index.tsx MyVideo out/final_video.mp4 \
  --browser-executable="$CHROME" --concurrency=2

echo ""
echo "Step 3: 合并音视频（-an 去原音，-shortest 留最短）"
ffmpeg -y -i out/final_video.mp4 -an -c:v copy /tmp/noaudio.mp4
ffmpeg -y -i /tmp/noaudio.mp4 -i audio/combined.m4a \
  -c:v copy -c:a aac -b:a 128k -shortest out/final_with_audio.mp4

echo ""
echo "完成: out/final_with_audio.mp4"
ls -lh out/final_with_audio.mp4
