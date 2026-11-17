# FFmpeg 常用命令速查

> 所有脚本的基础引擎。快速参考常用命令和参数。

## 基本信息

```bash
# 查看视频信息
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4

# 仅时长
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# 仅分辨率
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 video.mp4
```

## 视频剪切

```bash
# 精确剪切 (无重编码，速度快)
ffmpeg -ss 00:01:30 -i input.mp4 -t 00:00:30 -c copy output.mp4

# 剪切 + 重编码 (帧精确，带音频)
ffmpeg -ss 30 -i input.mp4 -t 60 -c:v libx264 -preset fast -c:a aac output.mp4

# 多段剪切并拼接
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]trim=0:30,setpts=PTS-STARTPTS[v1]; \
                   [0:v]trim=60:90,setpts=PTS-STARTPTS[v2]; \
                   [v1][v2]concat=n=2:v=1:a=0[out]" \
  -map "[out]" output.mp4
```

## 字幕操作

```bash
# 烧录 SRT 字幕
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4

# 烧录 + 自定义样式
ffmpeg -i input.mp4 \
  -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=20,PrimaryColour=&HFFFFFF&,Outline=1'" \
  output.mp4

# ASS 高级字幕
ffmpeg -i input.mp4 -vf "ass=subs.ass" output.mp4
```

## 格式转换

```bash
# 横转竖 (9:16 抖音)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  output.mp4

# 横转方 (1:1 Instagram)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black" \
  output.mp4

# 裁剪中心区域 (不缩放)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih" output.mp4
```

## 音频处理

```bash
# 提取音频
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# 音频淡入淡出 (30ms)
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=0.03,afade=t=out:st=59.97:d=0.03" output.mp4

# 音量检测
ffmpeg -i input.mp4 -af "volumedetect" -vn -f null -
```

## 场景检测

```bash
# 检测场景切换点
ffmpeg -i input.mp4 -vf "select='gt(scene,0.03)',showinfo" -f null -

# 在场景切换处提取关键帧
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)',scale=320:-1" -vsync vfr keyframes_%03d.png
```

## 色彩校正

```bash
# 暖色调
ffmpeg -i input.mp4 -vf "eq=brightness=0.02:saturation=1.15:contrast=1.05" output.mp4

# 冷色调
ffmpeg -i input.mp4 -vf "eq=brightness=-0.02:saturation=0.9:contrast=1.05:gamma_r=0.95:gamma_b=1.05" output.mp4

# 电影感
ffmpeg -i input.mp4 -vf "eq=contrast=1.15:saturation=0.85:brightness=-0.05" output.mp4
```

## GPU 加速 (macOS)

```bash
# 使用 VideoToolbox 编码器 (Apple Silicon)
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# 快速缩放 (VideoToolbox)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v h264_videotoolbox -b:v 5M output.mp4
```

## 拼接

```bash
# Concat demuxer (推荐，无需重编码)
# 1. 创建文件列表
echo "file 'clip1.mp4'\nfile 'clip2.mp4'\nfile 'clip3.mp4'" > list.txt
# 2. 拼接
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concat filter (重编码，支持不同格式)
ffmpeg -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

## 快速预览 / 测试

```bash
# 生成缩略图网格
ffmpeg -i input.mp4 -vf "fps=1/10,scale=320:-1,tile=8x8" thumbnails.png

# 提取指定时间帧
ffmpeg -ss 60 -i input.mp4 -vframes 1 -q:v 2 frame.jpg

# 裁剪前 10 秒快速预览
ffmpeg -i input.mp4 -t 10 -c copy preview.mp4
```
