# FFmpeg Master API 参考文档

**版本**: v2.0.0
**更新日期**: 2026-01-11

---

## 目录

1. [核心引擎](#核心引擎)
2. [分析器](#分析器)
3. [编码器](#编码器)
4. [构建器](#构建器)
5. [处理器](#处理器)
6. [进度模块](#进度模块)
7. [工具模块](#工具模块)
8. [数据类](#数据类)

---

## 核心引擎

### DecisionEngine

智能决策引擎，整合所有高级功能。

#### 初始化

```python
from scripts import DecisionEngine

engine = DecisionEngine(
    enable_smart_analysis=True,  # 启用智能分析
    gpu_detector=None,  # 可选：自定义GPU检测器
    preset_manager=None  # 可选：自定义预设管理器
)
```

#### 主要方法

##### analyze_video_type_deep()

深度分析视频类型。

```python
analysis = engine.analyze_video_type_deep(video_path: str) -> VideoAnalysisResult
```

**参数：**
- `video_path` (str): 视频文件路径

**返回：** `VideoAnalysisResult` 对象

**示例：**
```python
analysis = engine.analyze_video_type_deep("video.mp4")
print(f"类型: {analysis.content_type}")
print(f"置信度: {analysis.confidence}")
print(f"运动分数: {analysis.motion_score}")
```

##### get_optimized_encoding_params()

获取优化的编码参数。

```python
params = engine.get_optimized_encoding_params(
    video_path: str,
    quality_preference: str = "balanced",
    manual_content_type: VideoContentType = None,
    target_size_mb: float = None
) -> EncodingParams
```

**参数：**
- `video_path` (str): 视频文件路径
- `quality_preference` (str): 质量偏好 ("high" | "balanced" | "fast")
- `manual_content_type` (VideoContentType): 手动指定视频类型
- `target_size_mb` (float): 目标文件大小（MB）

**返回：** `EncodingParams` 对象

**示例：**
```python
params = engine.get_optimized_encoding_params(
    video_path="video.mp4",
    quality_preference="high"
)
```

##### apply_preset()

应用预设模板。

```python
params = engine.apply_preset(
    preset_name: str,
    user_params: dict = None
) -> EncodingParams
```

**参数：**
- `preset_name` (str): 预设名称
- `user_params` (dict): 用户覆盖的参数

**返回：** `EncodingParams` 对象

**示例：**
```python
params = engine.apply_preset('bilibili')
# 或覆盖部分参数
params = engine.apply_preset('youtube', user_params={'crf': 20})
```

##### list_available_presets()

列出所有可用预设。

```python
presets = engine.list_available_presets() -> dict
```

**返回：** 预设信息字典

**示例：**
```python
presets = engine.list_available_presets()
for name, info in presets.items():
    print(f"{name}: {info['metadata']['description']}")
```

##### compress_to_target_size()

压缩到目标文件大小。

```python
engine.compress_to_target_size(
    input_path: str,
    output_path: str,
    target_size_mb: float,
    tolerance: float = 0.05,
    audio_bitrate: str = "128k"
)
```

**参数：**
- `input_path` (str): 输入文件路径
- `output_path` (str): 输出文件路径
- `target_size_mb` (float): 目标文件大小（MB）
- `tolerance` (float): 容差（默认0.05，即5%）
- `audio_bitrate` (str): 音频码率

---

## 分析器

### VideoTypeAnalyzer

视频类型分析器。

#### 初始化

```python
from scripts.analyzers import VideoTypeAnalyzer

analyzer = VideoTypeAnalyzer()
```

#### 主要方法

##### analyze()

分析视频类型。

```python
result = analyzer.analyze(video_path: str) -> VideoAnalysisResult
```

**返回：** `VideoAnalysisResult` 对象

**属性：**
- `content_type` (VideoContentType): 视频类型
- `confidence` (float): 置信度 (0-1)
- `motion_score` (float): 运动分数 (0-1)
- `complexity_score` (float): 复杂度分数 (0-1)
- `color_score` (float): 色彩分数 (0-1)
- `analysis_notes` (str): 分析备注

---

### ParamOptimizer

参数优化器。

#### 初始化

```python
from scripts.encoders import ParamOptimizer

optimizer = ParamOptimizer()
```

#### 主要方法

##### optimize()

优化编码参数。

```python
params = optimizer.optimize(
    content_type: VideoContentType,
    has_gpu: bool = False,
    gpu_type: str = None,
    quality_preference: str = "balanced",
    target_size_mb: float = None
) -> EncodingParams
```

---

### KeyFrameAnalyzer

关键帧分析器，提供智能剪辑策略建议和剪辑点质量评估。

#### 初始化

```python
from scripts.analyzers import KeyFrameAnalyzer

analyzer = KeyFrameAnalyzer()
```

#### 主要方法

##### suggest_trim_strategy_smart_cut()

Smart Cut 混合剪辑模式策略，只重编码剪辑点附近的小片段。

```python
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time: float,
    duration: float,
    video_path: str,
    max_encoded_segment: float = 5.0
) -> TrimStrategy
```

**参数：**
- `start_time` (float): 起始时间（秒）
- `duration` (float): 持续时间（秒）
- `video_path` (str): 视频文件路径
- `max_encoded_segment` (float): 最大重编码片段时长（秒），默认5秒

**返回：** `TrimStrategy` 对象

**示例：**
```python
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time=30.0,
    duration=60.0,
    video_path="input.mp4"
)

print(f"模式: {strategy.mode}")
print(f"原因: {strategy.reason}")

if "segments" in strategy.recommended_params:
    for segment in strategy.recommended_params["segments"]:
        print(f"片段: {segment['type']} - {segment['duration']:.2f}秒")
```

##### export_keyframe_timeline()

导出关键帧时间轴为多种格式。

```python
result = analyzer.export_keyframe_timeline(
    video_path: str,
    output_format: str = "json",
    output_file: Optional[str] = None,
    max_frames: Optional[int] = None
) -> Optional[Union[str, Dict]]
```

**参数：**
- `video_path` (str): 视频文件路径
- `output_format` (str): 输出格式 ("json", "csv", "markdown", "txt")
- `output_file` (str): 输出文件路径（可选）
- `max_frames` (int): 最大检测帧数（可选）

**返回：**
- 如果 `output_file` 为 None，返回格式化的字符串或字典
- 如果 `output_file` 指定，返回 None，结果写入文件

**示例：**
```python
# 导出为 JSON
json_data = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="json"
)

# 导出到 CSV 文件
analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="csv",
    output_file="keyframes.csv"
)

# 导出为 Markdown
md_content = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="markdown"
)
```

##### assess_cut_point_quality()

评估剪辑点的质量并提供建议。

```python
quality = analyzer.assess_cut_point_quality(
    video_path: str,
    cut_point: float,
    max_frames: Optional[int] = None
) -> Optional[CutPointQuality]
```

**参数：**
- `video_path` (str): 视频文件路径
- `cut_point` (float): 剪辑点位置（秒）
- `max_frames` (int): 最大检测帧数（可选）

**返回：** `CutPointQuality` 对象，检测失败返回 None

**示例：**
```python
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

if quality:
    print(f"质量等级: {quality.quality_level}")
    print(f"推荐模式: {quality.recommended_mode}")
    print(f"精度估算: {quality.precision_estimate}")
    print(f"建议: {quality.reason}")
```

**质量等级说明：**
- `excellent`: 剪辑点非常接近关键帧（< 0.5秒），推荐快速模式
- `good`: 剪辑点接近关键帧（< 2秒），推荐快速模式
- `fair`: 剪辑点距离关键帧中等（< 5秒），推荐 Smart Cut 模式
- `poor`: 剪辑点距离关键帧较远（> 5秒），推荐精确模式

---

## 编码器

### TwoPassEncoder

两遍编码器。

#### 初始化

```python
from scripts.encoders import TwoPassEncoder

encoder = TwoPassEncoder()
```

#### 主要方法

##### build_commands()

构建两遍编码命令。

```python
commands = encoder.build_commands(
    input_path: str,
    output_path: str,
    target_bitrate: int,
    audio_bitrate: str = "128k"
) -> tuple
```

**返回：** (第一遍命令, 第二遍命令)

---

### AdaptiveBitrateController

自适应码率控制器。

#### 主要方法

##### refine_bitrate()

根据实际大小调整码率。

```python
new_bitrate = controller.refine_bitrate(
    target_bitrate: int,
    actual_size_mb: float,
    target_size_mb: float
) -> int
```

---

### QualityAwareCompressor

质量感知压缩器。

#### 主要方法

##### should_use_two_pass()

判断是否应该使用两遍编码。

```python
should_use = compressor.should_use_two_pass(
    file_size_mb: float,
    target_size_mb: float,
    current_bitrate: int
) -> bool
```

---

## 构建器

### FFmpegBuilder

FFmpeg命令构建器。

#### 初始化

```python
from scripts import FFmpegBuilder

builder = FFmpegBuilder()
```

#### 主要方法

##### compress_video()

压缩视频。

```python
builder.compress_video(
    input_path: str,
    output_path: str,
    target_size_mb: float = None,
    crf: int = 23
)
```

##### convert_format()

转换格式。

```python
builder.convert_format(
    input_path: str,
    output_path: str
)
```

##### resize_video()

调整分辨率。

```python
builder.resize_video(
    input_path: str,
    output_path: str,
    width: int,
    height: int
)
```

##### set_encoding_params()

设置编码参数。

```python
builder.set_encoding_params(params: EncodingParams)
```

##### build_and_run()

构建并执行命令。

```python
result = builder.build_and_run(
    input_path: str,
    output_path: str
) -> dict
```

---

## 处理器

### OptimizedBatchProcessor

优化的批量处理器。

#### 初始化

```python
from scripts.processors import OptimizedBatchProcessor

processor = OptimizedBatchProcessor(
    max_workers: int = 4,
    retry_strategy: str = 'exponential_backoff',
    skip_strategy: SkipStrategy = SkipStrategy.SMART,
    enable_progress: bool = True
)
```

**参数：**
- `max_workers` (int): 最大并发数
- `retry_strategy` (str): 重试策略
- `skip_strategy` (SkipStrategy): 跳过策略
- `enable_progress` (bool): 是否显示进度

#### 主要方法

##### process_batch()

批量处理视频。

```python
results = processor.process_batch(
    file_list: list,
    encoding_params: EncodingParams = None
) -> list
```

**参数：**
- `file_list` (list): 文件列表 [(input, output), ...]
- `encoding_params` (EncodingParams): 编码参数

**返回：** `ProcessResult` 对象列表

##### generate_report()

生成处理报告。

```python
report = processor.generate_report() -> BatchReportGenerator
```

---

### RetryHandler

重试处理器。

#### 初始化

```python
from scripts.processors import RetryHandler, RetryStrategy

handler = RetryHandler(
    max_retries: int = 3,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
)
```

#### 主要方法

##### execute_with_retry()

带重试的执行。

```python
result = handler.execute_with_retry(
    func: Callable,
    *args,
    **kwargs
) -> RetryResult
```

---

### SmartSkipper

智能跳过器。

#### 主要方法

##### should_skip()

判断是否应该跳过。

```python
should_skip = skipper.should_skip(
    input_path: str,
    output_path: str
) -> SkipDecision
```

---

## 进度模块

### ProgressTracker

进度跟踪器。

#### 初始化

```python
from scripts.progress import ProgressTracker

tracker = ProgressTracker(duration: float)
```

#### 主要方法

##### update()

更新进度。

```python
tracker.update(ffmpeg_output: str)
```

##### get_progress()

获取当前进度。

```python
progress = tracker.get_progress() -> float
```

##### get_remaining_time()

获取剩余时间。

```python
remaining = tracker.get_remaining_time() -> str
```

---

### SimpleProgressDisplay

简洁进度显示。

#### 主要方法

##### show_progress()

显示进度。

```python
display.show_progress(
    current: str,
    progress: float,
    total_files: int = 1,
    current_file_index: int = 0,
    remaining_time: str = "",
    speed: str = "",
    eta: str = ""
)
```

##### clear()

清除显示。

```python
display.clear()
```

---

### BatchProgressDisplay

批量进度显示。

#### 主要方法

##### start_batch()

开始批量处理。

```python
display.start_batch(title: str, total_files: int)
```

##### finish_file()

完成文件。

```python
display.finish_file(filename: str, success: bool, duration: float)
```

##### show_summary()

显示摘要。

```python
display.show_summary(
    total: int,
    success: int,
    failed: int,
    skipped: int,
    total_time: float
)
```

---

## 工具模块

### PresetManager

预设管理器。

#### 主要方法

##### load_preset()

加载预设。

```python
preset = manager.load_preset(preset_name: str) -> dict
```

##### list_presets()

列出所有预设。

```python
presets = manager.list_presets() -> dict
```

##### validate_preset()

验证预设。

```python
is_valid = manager.validate_preset(preset: dict) -> bool
```

---

### BatchReportGenerator

批量报告生成器。

#### 主要方法

##### add_result()

添加结果。

```python
reporter.add_result(result: ProcessResult)
```

##### generate_markdown_report()

生成Markdown报告。

```python
md_content = reporter.generate_markdown_report(
    stats: BatchStatistics
) -> str
```

##### generate_json_report()

生成JSON报告。

```python
json_content = reporter.generate_json_report(
    stats: BatchStatistics
) -> str
```

##### save_report()

保存报告。

```python
reporter.save_report(filepath: str, format: str = "markdown")
```

---

## 数据类

### VideoAnalysisResult

视频分析结果。

```python
@dataclass
class VideoAnalysisResult:
    content_type: VideoContentType
    confidence: float
    motion_score: float
    complexity_score: float
    color_score: float
    analysis_notes: str
```

---

### EncodingParams

编码参数。

```python
@dataclass
class EncodingParams:
    codec: str
    preset: str
    crf: int
    tune: str = None
    bitrate: int = None
    maxrate: int = None
    bufsize: int = None
    audio_codec: str = "aac"
    audio_bitrate: str = "128k"
```

---

### ProcessResult

处理结果。

```python
@dataclass
class ProcessResult:
    input_file: str
    output_file: str
    success: bool
    status: str
    duration: float = 0.0
    file_size_mb: float = 0.0
    retries: int = 0
    error: str = None
    timestamp: datetime = None
```

---

### BatchStatistics

批量统计。

```python
@dataclass
class BatchStatistics:
    total: int
    success: int
    failed: int
    skipped: int
    total_duration: float
    total_size_mb: float
    avg_duration: float
    avg_size_mb: float
    total_retries: int
    throughput_mb_per_sec: float
    files_per_sec: float
```

---

### VideoContentType

视频内容类型枚举。

```python
class VideoContentType(Enum):
    SCREEN_RECORDING = "screen_recording"
    ANIME = "anime"
    SPORTS = "sports"
    MUSIC_VIDEO = "music_video"
    MOVIE = "movie"
    OLD_VIDEO = "old_video"
```

---

### SkipStrategy

跳过策略枚举。

```python
class SkipStrategy(Enum):
    NONE = "none"
    SMART = "smart"
    FORCE = "force"
```

---

### RetryStrategy

重试策略枚举。

```python
class RetryStrategy(Enum):
    IMMEDIATE = "immediate"
    FIXED_DELAY = "fixed_delay"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
```

---

## 使用示例

### 完整工作流示例

```python
from scripts import DecisionEngine, FFmpegBuilder
from scripts.progress import SimpleProgressDisplay

# 1. 创建决策引擎
engine = DecisionEngine(enable_smart_analysis=True)

# 2. 分析视频
analysis = engine.analyze_video_type_deep("input.mp4")
print(f"检测到视频类型: {analysis.content_type}")

# 3. 获取优化参数
params = engine.get_optimized_encoding_params(
    video_path="input.mp4",
    quality_preference="balanced"
)

# 4. 构建并执行
builder = FFmpegBuilder()
builder.set_encoding_params(params)
result = builder.build_and_run("input.mp4", "output.mp4")

print(f"处理完成: {result}")
```

### 批量处理示例

```python
from scripts.processors import OptimizedBatchProcessor

processor = OptimizedBatchProcessor(
    max_workers=4,
    skip_strategy=SkipStrategy.SMART
)

file_list = [
    ("video1.mp4", "output1.mp4"),
    ("video2.mp4", "output2.mp4"),
    ("video3.mp4", "output3.mp4")
]

results = processor.process_batch(file_list)

# 生成报告
report = processor.generate_report()
report.save("batch_report.md")
```

---

## 异常处理

### 常见异常

- `FileNotFoundError`: 文件不存在
- `RuntimeError`: FFmpeg执行失败
- `ValueError`: 参数无效
- `MemoryError`: 内存不足

### 异常处理示例

```python
from scripts import DecisionEngine

try:
    engine = DecisionEngine()
    params = engine.get_optimized_encoding_params("video.mp4")
except FileNotFoundError as e:
    print(f"文件未找到: {e}")
except RuntimeError as e:
    print(f"处理失败: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 更多资源

- **使用指南**: [快速入门](quickstart.md)
- **版本信息**: 参考 [detailed_workflows.md](detailed_workflows.md) 获取最新工作流信息

---

*FFmpeg Master v2.0.0 - API参考文档*
