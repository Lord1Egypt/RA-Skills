# 精彩集锦 — Highlight Reel

> 适用：多段视频拼接、精彩片段合集、开放麦切片合并。

## 拼接多个片段

**Step 1**：创建片段列表文件 `concat.txt`：

```
file 'part1.mp4'
file 'part2.mp4'
file 'part3.mp4'
```

**Step 2**：拼接：

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy "$out"
```

## 渐变过渡拼接

两个片段之间加淡入淡出：

```bash
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=X[outv];[0:a][1:a]afade=transition=fade:duration=0.5:offset=X[outa]" \
  -map "[outv]" -map "[outa]" -c:v libx264 -c:a aac "$out"
```

- `transition=fade`：淡入淡出过渡（其他选项：wiperight、slideleft、rectcrop…）
- `duration=0.5`：过渡时长（秒）
- `offset=X`：过渡开始的绝对时间点

## 统一音量

拼接前各片段音量不一致时，先统一：

```bash
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary" -f null -
```

目标值：`I=-16`（Integrated LUFS），`TP=-1.5`（True Peak），`LRA=11`（Loudness Range）

## 统一帧率/分辨率

```bash
ffmpeg -i input -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" -r 30 -c:v libx264 -c:a aac "$out"
```

## 完整 highlight reel 工作流

```bash
# 1. 提取各段
ffmpeg -i "$in" -ss 0 -to 5 -c copy p1.mp4
ffmpeg -i "$in" -ss 10 -to 18 -c copy p2.mp4
ffmpeg -i "$in" -ss 42 -to 48 -c copy p3.mp4

# 2. 写 concat.txt

# 3. 拼接
ffmpeg -f concat -safe 0 -i concat.txt -c copy concat_raw.mp4

# 4. 音量统一
ffmpeg -i concat_raw.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v libx264 -c:a aac "$out"
```