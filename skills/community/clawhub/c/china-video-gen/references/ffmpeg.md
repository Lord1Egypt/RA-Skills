# ffmpeg 合成参数说明

## 基础：图片序列 + 音频合成

```bash
# 最简单的合成方式（所有图片等时长）
ffmpeg -y \
  -framerate 1/5 \           # 每张图显示5秒
  -i frames/frame_%02d.jpg \ # 图片序列
  -i audio/voiceover.mp3 \   # 音频
  -c:v libx264 \             # 视频编码
  -pix_fmt yuv420p \         # 像素格式（兼容性最好）
  -c:a aac \                 # 音频编码
  -shortest \                # 以短的轨道为准
  output.mp4
```

## 精确控制每张图片时长（concat demuxer）

```bash
# concat.txt 格式：
file 'frames/frame_01.jpg'
duration 3
file 'frames/frame_02.jpg'
duration 5
file 'frames/frame_03.jpg'
duration 5
# ...
# 最后一帧重复（必须）
file 'frames/frame_06.jpg'

# 合成命令
ffmpeg -y \
  -f concat -safe 0 \
  -i concat.txt \
  -i audio/voiceover.mp3 \
  -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -shortest \
  output.mp4
```

## Ken Burns 效果（缓慢放大）

```bash
# 单张图片 Ken Burns 效果（持续5秒，25fps）
ffmpeg -y -loop 1 -i input.jpg \
  -vf "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.3)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720,fps=25" \
  -t 5 -c:v libx264 -pix_fmt yuv420p \
  clip.mp4

# 参数说明：
# zoom+0.0015  每帧放大速度（越大越快）
# 1.3          最大缩放倍数
# d=125        总帧数（5秒×25fps）
# s=1280x720   输出分辨率
```

## Ken Burns 平移效果（从左到右）

```bash
ffmpeg -y -loop 1 -i input.jpg \
  -vf "scale=2560:1440,crop=1280:720:x='t/5*1280':y=0,fps=25" \
  -t 5 -c:v libx264 -pix_fmt yuv420p \
  clip_pan.mp4
```

## 淡入淡出转场（xfade）

```bash
# 两个片段之间0.5秒淡入淡出
ffmpeg -y \
  -i clip_01.mp4 \
  -i clip_02.mp4 \
  -filter_complex \
    "[0][1]xfade=transition=fade:duration=0.5:offset=4.5[out]" \
  -map "[out]" \
  -c:v libx264 -pix_fmt yuv420p \
  merged.mp4

# offset = 第一个片段时长 - 转场时长
# 如第一个片段5秒，转场0.5秒：offset=4.5
```

## 多片段合并（所有 Ken Burns 片段拼接）

```bash
# 生成片段列表
for i in 01 02 03 04 05 06; do
  echo "file 'frames/clip_${i}.mp4'" >> concat_clips.txt
done

# 合并
ffmpeg -y \
  -f concat -safe 0 \
  -i concat_clips.txt \
  -i audio/voiceover.mp3 \
  -c:v libx264 -c:a aac -shortest \
  output.mp4
```

## 添加背景音乐（可选）

```bash
# 混合解说词和背景音乐（背景音乐音量降低到30%）
ffmpeg -y \
  -i video_without_audio.mp4 \
  -i audio/voiceover.mp3 \
  -i audio/bgm.mp3 \
  -filter_complex \
    "[1:a]volume=1.0[voice];
     [2:a]volume=0.3[bgm];
     [voice][bgm]amix=inputs=2:duration=first[aout]" \
  -map "0:v" -map "[aout]" \
  -c:v copy -c:a aac -shortest \
  output_with_bgm.mp4
```

## 分辨率与比例设置

```bash
# 16:9 横版（B站/YouTube/抖音投放）
-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"

# 9:16 竖版（抖音/小红书竖版）
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"

# 1:1 方形（小红书）
-vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"

# 3:4 小红书竖版
-vf "scale=1080:1440:force_original_aspect_ratio=decrease,pad=1080:1440:(ow-iw)/2:(oh-ih)/2,setsar=1"
```

## 输出质量设置

```bash
# 高质量（文件较大，适合保存）
-c:v libx264 -crf 18 -preset slow

# 平衡质量（推荐默认）
-c:v libx264 -crf 23 -preset medium

# 小文件（适合上传分享）
-c:v libx264 -crf 28 -preset fast

# CRF说明：值越小质量越高，18接近无损，28肉眼可见损失
```
