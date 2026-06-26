# FFmpeg 最佳实践完整指南

## 概述

本指南汇总了 FFmpeg 视频处理的最佳实践，涵盖转码、剪辑、字幕、批量处理等各个方面。

### 核心原则

1. **质量优先**：在满足需求的前提下追求最高质量
2. **效率兼顾**：合理平衡处理速度和输出质量
3. **兼容性保证**：确保输出文件能在目标平台播放
4. **可维护性**：使用清晰的参数和可读的命令

## 转码最佳实践

### 1. 选择合适的编码格式

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **H.264** | 兼容性最好，支持广泛 | 压缩率一般 | 通用场景、兼容性要求高 |
| **H.265 (HEVC)** | 压缩率高，文件小 | 兼容性一般，编码慢 | 4K 视频、存储空间有限 |
| **AV1** | 压缩率极高，未来标准 | 编码极慢，兼容性差 | 技术尝鲜、长期存储 |
| **VP9** | Web 优化，开源 | 兼容性一般 | Web 视频、开源项目 |

**推荐**：
- 通用场景：H.264 (libx264)
- 4K 视频：H.265 (libx265)
- Web 视频：VP9 (libvpx-vp9)

### 2. 使用 CRF 模式而非固定码率

**CRF (Constant Rate Factor)** 是恒定质量模式，比固定码率更智能。

```bash
# ❌ 不推荐：固定码率
ffmpeg -i input.mp4 -b:v 2M -maxrate 2.5M -bufsize 5M output.mp4

# ✅ 推荐：CRF 模式
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4
```

**CRF 值参考**：

| CRF | 质量 | 文件大小 | 适用场景 |
|-----|------|----------|----------|
| 18-20 | 极高 | 很大 | 专业制作、存档 |
| 20-23 | 高 | 大 | 高质量发布 |
| 23-26 | 中等 | 中等 | 通用场景（推荐） |
| 26-30 | 低 | 小 | 快速预览、网络传输 |

### 3. 选择合适的预设

预设（preset）影响编码速度和压缩效率。

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 output.mp4
```

**预设对比**：

| 预设 | 速度 | 压缩率 | 适用场景 |
|------|------|--------|----------|
| **ultrafast** | 极快 | 最低 | 实时编码、测试 |
| **superfast** | 很快 | 很低 | 快速预览 |
| **veryfast** | 快 | 低 | 快速处理 |
| **faster** | 较快 | 较低 | 日常使用 |
| **fast** | 中等 | 中等 | 推荐 ✓ |
| **medium** | 中等 | 中等 | 推荐 ✓ |
| **slow** | 慢 | 高 | 高质量发布 |
| **slower** | 很慢 | 很高 | 专业制作 |
| **veryslow** | 极慢 | 最高 | 最终存档 |

**推荐**：
- 日常使用：`medium` 或 `fast`
- 高质量发布：`slow`
- 快速预览：`veryfast`

### 4. 使用两遍编码精确控制大小

当需要精确控制文件大小时，使用两遍编码。

```bash
# 第一遍：分析视频
ffmpeg -i input.mp4 -c:v libx264 -preset medium -b:v 2M \
  -pass 1 -an -f mp4 /dev/null

# 第二遍：实际编码
ffmpeg -i input.mp4 -c:v libx264 -preset medium -b:v 2M \
  -pass 2 -c:a aac -b:a 128k output.mp4
```

**优点**：
- 精确控制文件大小（偏差 < 5%）
- 更好的码率分配
- 更稳定的视频质量

**缺点**：
- 编码时间加倍
- 需要更多磁盘空间（临时文件）

### 5. GPU 加速优化

自动检测并使用 GPU 加速。

```bash
# NVIDIA GPU (NVENC)
ffmpeg -i input.mp4 -c:v h264_nvenc -b:v 5M output.mp4

# AMD GPU (AMF)
ffmpeg -i input.mp4 -c:v h264_amf -b:v 5M output.mp4

# Intel QSV
ffmpeg -i input.mp4 -c:v h264_qsv -b:v 5M output.mp4
```

**GPU 加速对比**：

| GPU | 速度 | 质量 | 兼容性 | 推荐度 |
|-----|------|------|--------|--------|
| **NVIDIA NVENC** | 极快 | 高 | 好 | ⭐⭐⭐⭐⭐ |
| **AMD AMF** | 快 | 中等 | 中等 | ⭐⭐⭐⭐ |
| **Intel QSV** | 快 | 中等 | 中等 | ⭐⭐⭐⭐ |

**最佳实践**：
- 优先使用 GPU 加速
- 回退到 CPU 编码（libx264）
- 测试 GPU 编码质量

## 剪辑最佳实践

### 1. 时间戳问题警告

**⚠️ 视频剪切时需要注意时间戳问题，否则可能导致播放器无法正确播放！**

### 2. 剪辑位置与编码方式

| 剪切位置 | 编码方式 | 原因 | 推荐度 |
|---------|---------|------|--------|
| **开头剪切** | ✅ 可用 `-c copy` | 时间戳从0开始，无时间戳问题 | ⭐⭐⭐⭐⭐ |
| **中间剪切** | ❌ 必须重新编码 | 起始时间戳不为0，会导致时间戳错乱 | ⭐⭐⭐⭐⭐ |
| **结尾剪切** | ❌ 必须重新编码 | 可能产生负时间戳 | ⭐⭐⭐⭐⭐ |

### 3. 正确的剪辑命令

**开头剪切（可以使用 -c copy）**
```bash
# 从开头剪切前10分钟
ffmpeg -i input.mp4 -t 00:10:00 -c copy output.mp4

# 或者使用 -ss（在 -i 之前，更精确）
ffmpeg -ss 00:00:00 -i input.mp4 -t 00:10:00 -c copy output.mp4
```

**中间/结尾剪切（必须重新编码）**
```bash
# 剪切第10分钟到第20分钟（必须重新编码）
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
  -c:v libx264 -c:a aac output.mp4

# 剪切最后10分钟（必须重新编码）
ffmpeg -i input.mp4 -ss 00:50:00 \
  -c:v libx264 -c:a aac output.mp4
```

**修复时间戳问题（如果出现播放问题）**
```bash
# 方法1：使用 -avoid_negative_ts make_zero
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
  -avoid_negative_ts make_zero \
  -c:v libx264 -c:a aac output.mp4

# 方法2：使用 -fflags +genpts 重新生成时间戳
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
  -fflags +genpts \
  -c:v libx264 -c:a aac output.mp4

# 方法3：组合使用（推荐）
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
  -avoid_negative_ts make_zero \
  -fflags +genpts \
  -c:v libx264 -c:a aac output.mp4
```

### 4. 错误用法示例

```bash
# ❌ 错误：中间剪切使用 -c copy（会导致时间戳错乱）
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 -c copy output.mp4

# ❌ 错误：结尾剪切使用 -c copy（可能产生负时间戳）
ffmpeg -i input.mp4 -ss 00:50:00 -c copy output.mp4

# ❌ 错误：-ss 在 -i 之后使用 -c copy（时间戳问题更严重）
ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 -c copy output.mp4
```

### 5. 剪辑最佳实践

1. **优先使用 Smart Cut**：平衡速度与质量
   ```python
   from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer
   analyzer = KeyFrameAnalyzer()

   strategy = analyzer.suggest_trim_strategy_smart_cut(
       start_time=30.0,
       duration=60.0,
       video_path="input.mp4"
   )
   ```

2. **使用两遍编码提高质量**
   ```bash
   ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
     -c:v libx264 -preset medium -crf 23 \
     -pass 1 -an -f mp4 /dev/null

   ffmpeg -i input.mp4 -ss 00:10:00 -t 00:10:00 \
     -c:v libx264 -preset medium -crf 23 \
     -pass 2 -c:a aac output.mp4
   ```

3. **验证输出视频**
   ```bash
   # 使用播放器验证视频能否正常播放
   ffplay output.mp4

   # 检查视频信息
   ffprobe -v error -show_format -show_streams output.mp4
   ```

4. **精确时间点使用关键帧对齐**
   ```bash
   # 在 -i 之前使用 -ss 以关键帧对齐
   ffmpeg -ss 00:10:00 -i input.mp4 -t 00:10:00 \
     -c:v libx264 -c:a aac output.mp4
   ```

5. **批量处理前测试**
   ```bash
   # 先测试单个视频
   ffmpeg -i test.mp4 -ss 00:10:00 -t 00:10:00 \
     -c:v libx264 -c:a aac test_output.mp4

   # 确认结果正确后再批量处理
   ```

## 字幕处理最佳实践

### 1. 字幕格式选择

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **SRT** | 兼容性最好 | 功能简单 | 通用场景 |
| **ASS/SSA** | 功能强大，样式丰富 | 兼容性一般 | 复杂字幕、特效 |
| **VTT** | Web 标准 | 功能简单 | Web 视频 |

### 2. 字幕处理方式

| 方式 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **嵌入（软字幕）** | 可开关，不影响画质 | 需播放器支持 | ⭐⭐⭐⭐⭐ |
| **烧录（硬字幕）** | 兼容性好 | 不可修改，影响画质 | ⭐⭐⭐ |
| **外挂** | 灵活性最高 | 需管理多个文件 | ⭐⭐⭐⭐ |

### 3. 字幕嵌入示例

```bash
# 嵌入 SRT 字幕（软字幕）
ffmpeg -i input.mp4 -i subtitle.srt \
  -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=chi \
  output.mp4

# 烧录字幕（硬字幕）
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" \
  -c:a copy output.mp4
```

### 4. 字幕处理最佳实践

1. **优先使用嵌入而非烧录**
   - 嵌入字幕可开关，不影响画质
   - 烧录字幕不可修改，影响画质

2. **保留原始字幕流**
   ```bash
   # 提取字幕
   ffmpeg -i input.mp4 -map 0:s:0 subtitle.srt

   # 嵌入新字幕时保留原字幕
   ffmpeg -i input.mp4 -i new_subtitle.srt \
     -map 0:v -map 0:a -map 0:s -map 1:s \
     -c:v copy -c:a copy -c:s mov_text output.mp4
   ```

3. **使用 UTF-8 编码避免乱码**
   ```bash
   # 确保字幕文件使用 UTF-8 编码
   iconv -f GBK -t UTF-8 subtitle_gbk.srt > subtitle_utf8.srt

   # 嵌入字幕
   ffmpeg -i input.mp4 -i subtitle_utf8.srt \
     -c:v copy -c:a copy -c:s mov_text output.mp4
   ```

4. **验证字幕时间轴准确性**
   ```bash
   # 使用播放器验证字幕时间轴
   ffplay -vf "subtitles=subtitle.srt" input.mp4
   ```

## 批量处理最佳实践

### 1. 批量处理策略

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **串行处理** | 稳定，资源占用低 | 速度慢 | 少量文件 |
| **并行处理** | 速度快 | 资源占用高 | 大量文件 |
| **混合模式** | 平衡速度与稳定 | 实现复杂 | 推荐方案 |

### 2. 批量处理示例

```python
# 串行处理
for video in video_list:
    process_video(video)

# 并行处理（使用多进程）
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    executor.map(process_video, video_list)
```

### 3. 批量处理最佳实践

1. **先测试单个文件再批量**
   ```python
   # 测试单个文件
   test_result = process_video("test.mp4")
   assert test_result["success"], "测试失败"

   # 批量处理
   for video in video_list:
       process_video(video)
   ```

2. **使用合理的并行度**
   ```python
   import os

   # 根据 CPU 核心数设置并行度
   max_workers = max(1, os.cpu_count() - 1)

   with ProcessPoolExecutor(max_workers=max_workers) as executor:
       executor.map(process_video, video_list)
   ```

3. **保留原始文件（不覆盖）**
   ```python
   # 生成新文件名
   output_file = f"processed_{input_file}"

   # 处理视频
   process_video(input_file, output_file)
   ```

4. **生成详细处理日志**
   ```python
   import logging

   logging.basicConfig(
       filename="batch_process.log",
       level=logging.INFO,
       format="%(asctime)s - %(levelname)s - %(message)s"
   )

   for video in video_list:
       try:
           logging.info(f"处理 {video}")
           process_video(video)
           logging.info(f"完成 {video}")
       except Exception as e:
           logging.error(f"失败 {video}: {e}")
   ```

5. **错误自动重试**
   ```python
   from tenacity import retry, stop_after_attempt, wait_fixed

   @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
   def process_video_with_retry(video):
       return process_video(video)
   ```

## 性能优化最佳实践

### 1. 使用 GPU 加速

```bash
# 检测可用的 GPU
ffmpeg -hwaccels

# 使用 GPU 加速
ffmpeg -i input.mp4 -c:v h264_nvenc -b:v 5M output.mp4
```

### 2. 调整预设

```bash
# 快速处理（牺牲质量）
ffmpeg -i input.mp4 -c:v libx264 -preset veryfast -crf 28 output.mp4

# 高质量（牺牲速度）
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 20 output.mp4
```

### 3. 降低分辨率或帧率

```bash
# 降低分辨率
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4

# 降低帧率
ffmpeg -i input.mp4 -r 24 output.mp4
```

### 4. 使用流拷贝（无需重新编码）

```bash
# 格式转换（流拷贝）
ffmpeg -i input.mp4 -c copy output.mkv

# 剪辑（流拷贝，仅限开头剪切）
ffmpeg -i input.mp4 -t 00:10:00 -c copy output.mp4
```

## 质量保证最佳实践

### 1. 验证输出质量

```bash
# 检查视频信息
ffprobe -v error -show_format -show_streams output.mp4

# 对比文件大小
ls -lh input.mp4 output.mp4

# 播放验证
ffplay output.mp4
```

### 2. 使用质量评估指标

```bash
# VMAF 评分（需要 vmaf 库）
ffmpeg -i input.mp4 -i output.mp4 \
  -lavfi "libvmaf=model_path=vmaf_v0.6.1.pkl" \
  -f null -

# SSIM 指标
ffmpeg -i input.mp4 -i output.mp4 \
  -lavfi "ssim" -f null -

# PSNR 值
ffmpeg -i input.mp4 -i output.mp4 \
  -lavfi "psnr" -f null -
```

### 3. 对比源文件和输出文件

```bash
# 对比分辨率
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 input.mp4

ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0 output.mp4

# 对比码率
ffprobe -v error -select_streams v:0 \
  -show_entries stream=bit_rate -of csv=p=0 input.mp4

ffprobe -v error -select_streams v:0 \
  -show_entries stream=bit_rate -of csv=p=0 output.mp4
```

## 故障排除最佳实践

### 1. 使用详细模式

```bash
# 显示详细信息
ffmpeg -v debug -i input.mp4 -c:v libx264 output.mp4

# 显示警告和错误
ffmpeg -v warning -i input.mp4 -c:v libx264 output.mp4
```

### 2. 检查 FFmpeg 版本

```bash
# 查看 FFmpeg 版本
ffmpeg -version

# 查看支持的编码器
ffmpeg -encoders

# 查看支持的解码器
ffmpeg -decoders

# 查看支持的格式
ffmpeg -formats
```

### 3. 测试命令

```bash
# 测试编码（不输出文件）
ffmpeg -i input.mp4 -c:v libx264 -f null -

# 测试前 10 秒
ffmpeg -i input.mp4 -t 10 -c:v libx264 test_output.mp4
```

## 相关文档

- [Smart Cut 指南](smart_cut_guide.md)
- [关键帧分析指南](keyframe_analysis.md)
- [API 参考](api_reference.md)
- [快速入门](quickstart.md)
- [详细工作流](detailed_workflows.md)

---

**FFmpeg 最佳实践** - 让视频处理更高效、更可靠！
