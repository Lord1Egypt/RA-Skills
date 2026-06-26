# 快速开始

欢迎使用 FFmpeg Master！本指南将帮助您在 5 分钟内开始使用智能视频处理功能。

---

## 安装

### 1. 系统要求

- Python 3.7 或更高版本
- FFmpeg 4.0 或更高版本
- 足够的磁盘空间（至少是源视频的 2 倍）

### 2. 安装 FFmpeg

**Windows:**
```bash
winget install FFmpeg
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

**验证安装:**
```bash
ffmpeg -version
```

### 3. 安装 Python 依赖

```bash
uv add numpy
```

### 4. 验证安装

```bash
cd scripts
python3 -c "from decision_engine import DecisionEngine; print('安装成功！')"
```

---

## 基础使用

### 示例 1：格式转换

最简单的用法 - 将视频转换为不同格式：

```python
from scripts import DecisionEngine

engine = DecisionEngine()
engine.process("input.mov", "output.mp4")
```

**支持的所有格式**：
- 输入：MP4, MKV, AVI, MOV, WMV, FLV, WebM, 等
- 输出：MP4, MKV, AVI, MOV, WebM, 等

---

### 示例 2：智能压缩

自动识别视频类型并选择最优参数：

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 自动分析并优化
params = engine.get_optimized_encoding_params(
    video_path="video.mp4",
    quality_preference="balanced"  # 可选: high, balanced, fast
)

# 执行转换
engine.process_with_params("video.mp4", "output.mp4", params)
```

**质量偏好选项**：
- `high` - 最高质量（较慢）
- `balanced` - 质量与速度平衡（推荐）
- `fast` - 快速处理（较低质量）

---

### 示例 3：使用预设

为特定平台优化视频：

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 使用 B站 预设
params = engine.apply_preset('bilibili')
engine.process_with_params("video.mp4", "output.mp4", params)
```

**可用的内置预设**：

| 预设名称 | 适用场景 |
|---------|---------|
| `youtube` | YouTube 上传 |
| `bilibili` | B站 上传 |
| `wechat` | 微信聊天/朋友圈 |
| `douyin` | 抖音短视频 |
| `social` | 社交媒体（Instagram/TikTok/Twitter/Facebook） |
| `archive` | 长期存档（高质量） |
| `preview` | 快速预览（低质量） |
| `web` | 网站嵌入（优化） |

**自然语言识别**：
```python
# 以下写法等效：
params = engine.apply_preset('bilibili')
params = engine.apply_preset('B站')
params = engine.apply_preset('BiliBili')
```

---

### 示例 4：精确文件大小

压缩视频到指定大小（偏差 < 5%）：

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 压缩到 50MB
result = engine.compress_to_target_size(
    input_path="large_video.mp4",
    output_path="compressed.mp4",
    target_size_mb=50
)

print(f"实际大小: {result['actual_size_mb']:.2f} MB")
print(f"偏差: {result['deviation_percent']:.2f}%")
```

**适用场景**：
- 邮件附件限制（如 25MB）
- 平台上传限制（如 100MB）
- 存储空间优化

---

### 示例 5：批量处理

批量处理多个视频文件：

```python
from scripts.processors import OptimizedBatchProcessor

processor = OptimizedBatchProcessor(
    max_workers=4,           # 并发数
    enable_retry=True,       # 启用错误重试
    skip_strategy='smart'    # 智能跳过已处理文件
)

# 准备文件列表
file_list = [
    ("video1.mp4", "output1.mp4"),
    ("video2.mp4", "output2.mp4"),
    ("video3.mp4", "output3.mp4")
]

# 批量处理
results = processor.process_batch(file_list)

# 生成报告
report = processor.generate_report()
report.save("batch_report.md")

print(f"成功: {len(results['success'])}")
print(f"失败: {len(results['failed'])}")
```

**批量处理特性**：
- 错误自动重试
- 智能跳过未修改文件
- 详细的处理报告（Markdown/JSON）
- 并发处理加速

---

### 示例 6：带进度显示

实时查看处理进度：

```python
from scripts import DecisionEngine
from scripts.progress import SimpleProgressDisplay

engine = DecisionEngine()
display = SimpleProgressDisplay()

# 启用进度显示
result = engine.process_with_progress(
    input_path="video.mp4",
    output_path="output.mp4",
    progress_callback=display.show_progress
)
```

**进度显示包含**：
- 当前文件名
- 进度百分比
- 剩余时间
- 处理速度
- 预计完成时间

---

## 常见使用场景

### 场景 1：为 B站上传准备视频

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 使用 B站 1080p60 预设
params = engine.apply_preset('bilibili_1080p60')
engine.process_with_params("raw_video.mp4", "bilibili_upload.mp4", params)
```

### 场景 2：压缩视频以通过微信发送

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 使用微信预设（限制 100MB）
params = engine.apply_preset('wechat_chat')
engine.process_with_params("large_video.mp4", "wechat_send.mp4", params)
```

### 场景 3：制作抖音短视频

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 使用抖音竖屏预设
params = engine.apply_preset('douyin')
engine.process_with_params("horizontal.mp4", "douyin_vertical.mp4", params)
```

### 场景 4：批量转换手机拍摄的视频

```python
from scripts.processors import OptimizedBatchProcessor
from pathlib import Path

# 获取所有手机拍摄的视频（MOV 格式）
videos = list(Path("phone_videos").glob("*.mov"))

# 准备输出列表（转换为 MP4）
file_list = [
    (str(v), str(v).replace(".mov", ".mp4").replace("phone_videos", "converted"))
    for v in videos
]

# 批量处理
processor = OptimizedBatchProcessor(max_workers=4)
results = processor.process_batch(file_list)

# 生成报告
report = processor.generate_report()
report.save("conversion_report.md")
```

### 场景 5：创建高质量视频存档

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 使用存档预设（最高质量）
params = engine.apply_preset('archive')
engine.process_with_params("original.mp4", "archive.mp4", params)
```

---

## 实用技巧

### 技巧 1：查看视频类型

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 深度分析视频类型
analysis = engine.analyze_video_type_deep("video.mp4")

print(f"视频类型: {analysis.content_type}")
print(f"运动等级: {analysis.motion_level}/10")
print(f"复杂度等级: {analysis.complexity_level}/10")
print(f"色彩丰富度: {analysis.color_richness}/10")
```

### 技巧 2：自定义预设参数

```python
from scripts import DecisionEngine

engine = DecisionEngine()

# 应用预设并覆盖部分参数
params = engine.apply_preset('youtube')
params.video_bitrate = "8M"           # 覆盖视频码率
params.audio_bitrate = "320k"         # 覆盖音频码率
paramspreset = "slower"               # 覆盖编码速度

engine.process_with_params("input.mp4", "output.mp4", params)
```

### 技巧 3：检查 FFmpeg 命令

```python
from scripts import FFmpegBuilder

builder = FFmpegBuilder()
builder.compress_video("input.mp4", "output.mp4", target_size_mb=100)

# 查看将要执行的 FFmpeg 命令
command = builder.build()
print("FFmpeg 命令:", " ".join(command))
```

### 技巧 4：处理字幕

```python
from scripts import SubtitleProcessor

processor = SubtitleProcessor()

# 嵌入字幕
processor.embed_subtitle("video.mp4", "subtitle.srt", "output.mp4")

# 提取字幕
processor.extract_subtitle("video.mp4", "output.srt")

# 烧录字幕（硬字幕）
processor.burn_subtitle("video.mp4", "subtitle.srt", "output.mp4")
```

---

## 故障排除

### 问题 1：FFmpeg 未找到

**错误信息**：`FFmpeg not found in PATH`

**解决方案**：
1. 确认 FFmpeg 已安装：`ffmpeg -version`
2. 添加 FFmpeg 到系统 PATH
3. 重启终端/编辑器

### 问题 2：NumPy 导入失败

**错误信息**：`ModuleNotFoundError: No module named 'numpy'`

**解决方案**：
```bash
pip install numpy
```

### 问题 3：GPU 加速不工作

**原因**：未安装 GPU 驱动或运行时

**解决方案**：
- NVIDIA：安装 CUDA Toolkit
- AMD：安装 AMF 运行时
- Intel：安装 QSV 运行时

### 问题 4：两遍编码太慢

**原因**：两遍编码需要约 1.5 倍时间

**解决方案**：
- 使用单遍编码（更快）
- 降低质量预设（`fast`/`veryfast`）
- 使用 GPU 加速

### 问题 5：批量处理内存不足

**原因**：并发数过高

**解决方案**：
```python
processor = OptimizedBatchProcessor(
    max_workers=2  # 降低并发数
)
```

---

## 下一步

恭喜！您已经掌握了 FFmpeg Master 的基础用法。

**继续学习**：
- 查看 [API 参考](api_reference.md) - 完整的 API 文档
- 查看 [最佳实践](best_practices.md) - 使用建议
- 查看 [故障排除](troubleshooting.md) - 常见问题解决

**获取帮助**：
- 查看文档中的"故障排除"部分

---

**FFmpeg Master** - 让视频处理变得简单智能！
