# FFmpeg Master - 故障排除指南

本文档提供常见问题的解决方案和故障排除步骤。

## 目录

- [安装和配置问题](#安装和配置问题)
- [转码问题](#转码问题)
- [剪辑问题](#剪辑问题)
- [字幕问题](#字幕问题)
- [性能问题](#性能问题)
- [文件大小问题](#文件大小问题)
- [质量保证问题](#质量保证问题)
- [批量处理问题](#批量处理问题)

---

## 安装和配置问题

### 问题：FFmpeg 未找到

**症状：**
```
ffmpeg: command not found
```

**解决方案：**

1. **检查 FFmpeg 是否安装**
   ```bash
   ffmpeg -version
   ```

2. **安装 FFmpeg**

   **Windows:**
   ```bash
   winget install FFmpeg
   # 或
   choco install ffmpeg
   ```

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   **Linux (CentOS/RHEL):**
   ```bash
   sudo yum install ffmpeg
   ```

3. **验证安装**
   ```bash
   ffmpeg -version
   ffprobe -version
   ```

### 问题：Python 模块导入失败

**症状：**
```
ModuleNotFoundError: No module named 'ffmpeg'
```

**解决方案：**

1. **检查 Python 环境**
   ```bash
   python --version
   pip --version
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证安装**
   ```bash
   python -c "import ffmpeg; print(ffmpeg.__version__)"
   ```

### 问题：GPU 加速不可用

**症状：**
```
Encoder 'h264_nvenc' not found
```

**解决方案：**

1. **检查 GPU 驱动**

   **NVIDIA:**
   ```bash
   nvidia-smi
   ```

   **AMD:**
   ```bash
   amdgpu-info --show-gpu-info
   ```

   **Intel:**
   ```bash
   vainfo
   ```

2. **检查 FFmpeg 编译的编码器**
   ```bash
   ffmpeg -encoders | grep -E "(nvenc|amf|qsv)"
   ```

3. **重新编译 FFmpeg（如果需要）**

   **NVIDIA NVENC:**
   ```bash
   # 下载支持 NVENC 的 FFmpeg 预编译版本
   # 或从源码编译
   ```

4. **回退到 CPU 编码**
   ```python
   # 技能会自动回退到 libx264
   ```

---

## 转码问题

### 问题：转码后音视频不同步

**症状：**
播放时音频和视频不匹配。

**解决方案：**

1. **使用智能同步修复**
   ```bash
   ffmpeg -i input.mp4 -async 1 output.mp4
   ```

2. **重新编码音视频**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -c:a aac -strict experimental output.mp4
   ```

3. **使用帧率同步**
   ```bash
   ffmpeg -i input.mp4 -r 30 -c:v libx264 -c:a aac output.mp4
   ```

### 问题：转码后画质下降

**症状：**
画面模糊、有马赛克或伪影。

**解决方案：**

1. **提高 CRF 值质量**
   ```bash
   # CRF 值越小，质量越高（范围 0-51）
   ffmpeg -i input.mp4 -c:v libx264 -crf 18 output.mp4
   ```

2. **使用两遍编码**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 1 -f mp4 /dev/null
   ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -pass 2 output.mp4
   ```

3. **调整预设**
   ```bash
   # 使用较慢的预设以提高质量
   ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 20 output.mp4
   ```

4. **调整分辨率**
   ```bash
   # 保持原始分辨率
   ffmpeg -i input.mp4 -c:v libx264 -crf 20 -vf scale=-1:original output.mp4
   ```

### 问题：转码失败，错误信息不明

**解决方案：**

1. **启用详细日志**
   ```bash
   ffmpeg -v debug -i input.mp4 output.mp4
   ```

2. **检查输入文件**
   ```bash
   ffprobe -v error -show_format -show_streams input.mp4
   ```

3. **尝试简化命令**
   ```bash
   # 先使用最简单的命令测试
   ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
   ```

4. **检查文件完整性**
   ```bash
   ffmpeg -v error -i input.mp4 -f null -
   ```

---

## 剪辑问题

### 问题：剪辑位置不准确

**症状：**
剪辑的开始或结束位置与预期不符。

**解决方案：**

1. **使用 Smart Cut 混合剪辑**
   ```python
   from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer

   analyzer = KeyFrameAnalyzer()
   strategy = analyzer.suggest_trim_strategy_smart_cut(
       start_time=30.0,
       duration=60.0,
       video_path="input.mp4"
   )
   ```

2. **使用精确重编码模式**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 60 -c:v libx264 -c:a aac output.mp4
   ```

3. **检查关键帧位置**
   ```bash
   ffprobe -select_streams v -show_frames input.mp4 | grep "key_frame=1"
   ```

### 问题：剪辑后音视频不同步

**解决方案：**

1. **使用同步参数**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 60 -async 1 -c:v libx264 -c:a aac output.mp4
   ```

2. **重新编码音视频**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 60 -c:v libx264 -c:a aac -strict experimental output.mp4
   ```

3. **使用 copyts 参数**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 60 -copyts -c:v libx264 -c:a aac output.mp4
   ```

### 问题：Smart Cut 速度慢

**症状：**
Smart Cut 模式比预期慢。

**解决方案：**

1. **减少最大重编码片段时长**
   ```python
   strategy = analyzer.suggest_trim_strategy_smart_cut(
       start_time=30.0,
       duration=60.0,
       video_path="input.mp4",
       max_encoded_segment=3.0  # 从 5 秒减少到 3 秒
   )
   ```

2. **使用更快的编码预设**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 2.5 -c:v libx264 -preset veryfast -c:a aac segment1.mp4
   ```

3. **使用 GPU 加速**
   ```bash
   ffmpeg -i input.mp4 -ss 30 -t 2.5 -c:v h264_nvenc -c:a aac segment1.mp4
   ```

---

## 字幕问题

### 问题：字幕嵌入失败

**症状：**
```
Could not find tag for codec srt in stream #1, codec not currently supported in container 'mp4'
```

**解决方案：**

1. **转换字幕格式**
   ```bash
   ffmpeg -i input.srt input.ass
   ```

2. **使用正确的封装格式**
   ```bash
   # MP4 只支持 mov_text
   ffmpeg -i input.mp4 -i subs.srt -c:s mov_text output.mp4

   # MKV 支持所有格式
   ffmpeg -i input.mp4 -i subs.srt -c:s srt output.mkv
   ```

3. **烧录字幕**
   ```bash
   ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4
   ```

### 问题：字幕烧录后乱码

**解决方案：**

1. **指定字体**
   ```bash
   ffmpeg -i input.mp4 -vf "subtitles=subs.srt:force_style='FontName=Arial'" output.mp4
   ```

2. **使用 UTF-8 编码**
   ```bash
   ffmpeg -i input.mp4 -vf "subtitles=subs.srt:charenc=UTF-8" output.mp4
   ```

3. **转换字幕编码**
   ```bash
   iconv -f GBK -t UTF-8 input.srt > output.srt
   ```

### 问题：字幕提取失败

**解决方案：**

1. **识别字幕流**
   ```bash
   ffprobe -i input.mp4 -show_streams -select_streams s
   ```

2. **提取指定字幕流**
   ```bash
   ffmpeg -i input.mp4 -map 0:s:0 subs.srt
   ```

3. **使用正确的封装格式**
   ```bash
   ffmpeg -i input.mp4 -map 0:s:0 subs.ass
   ```

---

## 性能问题

### 问题：处理速度慢

**症状：**
转码或剪辑时间过长。

**解决方案：**

1. **使用 GPU 加速**
   ```bash
   ffmpeg -i input.mp4 -c:v h264_nvenc -c:a aac output.mp4
   ```

2. **调整编码预设**
   ```bash
   # 使用更快的预设
   ffmpeg -i input.mp4 -c:v libx264 -preset veryfast -crf 23 output.mp4
   ```

3. **降低分辨率**
   ```bash
   ffmpeg -i input.mp4 -vf scale=1280:720 -c:v libx264 output.mp4
   ```

4. **使用流拷贝（如果可能）**
   ```bash
   ffmpeg -i input.mp4 -c copy output.mp4
   ```

5. **调整线程数**
   ```bash
   ffmpeg -i input.mp4 -threads 4 -c:v libx264 output.mp4
   ```

### 问题：内存占用过高

**症状：**
处理过程中系统变慢或崩溃。

**解决方案：**

1. **限制内存使用**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -threads 2 output.mp4
   ```

2. **使用分段处理**
   ```bash
   # 将大文件分成小段处理
   ffmpeg -i input.mp4 -t 300 -c copy part1.mp4
   ffmpeg -i input.mp4 -ss 300 -t 300 -c copy part2.mp4
   ```

3. **降低缓冲区大小**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -bufsize 1M output.mp4
   ```

---

## 文件大小问题

### 问题：文件大小不符合预期

**症状：**
输出文件大小与目标大小相差较大。

**解决方案：**

1. **使用两遍编码**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f mp4 /dev/null
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
   ```

2. **调整码率**
   ```bash
   # 计算目标码率
   # 目标码率 (Kbps) = (目标大小 MB * 8 * 1024) / 时长 (秒)
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -maxrate 2.5M -bufsize 5M output.mp4
   ```

3. **调整音频码率**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -c:a aac -b:a 128k output.mp4
   ```

4. **降低分辨率**
   ```bash
   ffmpeg -i input.mp4 -vf scale=1280:720 -c:v libx264 output.mp4
   ```

---

## 质量保证问题

### 问题：输出文件无法播放

**症状：**
播放器无法打开输出文件。

**解决方案：**

1. **检查文件完整性**
   ```bash
   ffmpeg -v error -i output.mp4 -f null -
   ```

2. **使用标准参数**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -profile:v high -level 4.1 -c:a aac output.mp4
   ```

3. **添加 faststart 标志**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -movflags +faststart output.mp4
   ```

4. **尝试不同的封装格式**
   ```bash
   ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mkv
   ```

---

## 批量处理问题

### 问题：批量处理部分失败

**症状：**
部分文件处理成功，部分失败。

**解决方案：**

1. **检查失败文件**
   ```bash
   # 使用详细模式查看错误信息
   ffmpeg -v debug -i failed_input.mp4 output.mp4
   ```

2. **使用错误重试机制**
   ```python
   from scripts import BatchProcessor

   processor = BatchProcessor(max_retries=3)
   processor.process_files(file_list)
   ```

3. **跳过已处理的文件**
   ```python
   processor = BatchProcessor(skip_existing=True)
   processor.process_files(file_list)
   ```

4. **降低并行度**
   ```python
   processor = BatchProcessor(max_workers=1)  # 串行处理
   processor.process_files(file_list)
   ```

### 问题：批量处理速度慢

**解决方案：**

1. **调整并行度**
   ```python
   processor = BatchProcessor(max_workers=4)  # 增加并行数
   processor.process_files(file_list)
   ```

2. **使用 GPU 加速**
   ```python
   processor = BatchProcessor(use_gpu=True)
   processor.process_files(file_list)
   ```

3. **跳过质量验证**
   ```python
   processor = BatchProcessor(validate_output=False)
   processor.process_files(file_list)
   ```

---

## 其他常见问题

### Q：如何选择视频编码格式？

**推荐方案：**
- **H.264**：最兼容，适合大多数场景
- **H.265 (HEVC)**：高压缩率，适合 4K 视频
- **AV1**：未来标准，极高压缩率，编码慢
- **VP9**：Web 优化，适合在线视频

### Q：如何平衡质量和文件大小？

**技巧：**
1. 使用 CRF 模式（恒定质量）而非固定码率
2. CRF 值：18-28（越小质量越好，文件越大）
3. 预设：slow/medium（速度与质量平衡）
4. 两遍编码：精确控制码率

### Q：字幕嵌入还是烧录？

**选择建议：**
- **嵌入（软字幕）**：推荐，可开关，不影响画质
- **烧录（硬字幕）**：不可修改，兼容性好，适合永久字幕
- **外挂**：灵活性最高，支持多语言切换

---

## 获取帮助

如果以上解决方案无法解决您的问题：

1. **查看详细文档**
   - [快速入门](quickstart.md)
   - [API 参考](api_reference.md)
   - [最佳实践](best_practices.md)

2. **启用详细日志**
   ```bash
   ffmpeg -v debug -i input.mp4 output.mp4
   ```

3. **检查 FFmpeg 版本**
   ```bash
   ffmpeg -version
   ```

4. **更新 FFmpeg**
   ```bash
   # 下载最新版本
   # 或使用包管理器更新
   ```

5. **报告问题**
   - 提供详细的错误信息
   - 提供输入文件信息（ffprobe 输出）
   - 提供使用的 FFmpeg 命令
   - 描述期望行为和实际行为
