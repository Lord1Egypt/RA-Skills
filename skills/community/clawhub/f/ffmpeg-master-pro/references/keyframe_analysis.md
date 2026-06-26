# 关键帧分析完整指南

## 概述

关键帧分析是 ffmpeg-master 技能的核心功能之一，提供智能的剪辑点评估和质量分析能力。

### 核心功能

- **关键帧检测**：自动检测视频中的所有关键帧位置
- **剪辑点质量评估**：评估任意时间点的剪辑适用性
- **时间轴导出**：导出关键帧时间轴到多种格式
- **智能策略建议**：基于关键帧位置推荐最优剪辑策略

### 为什么需要关键帧分析？

**问题**：视频剪辑时，如果不在关键帧位置剪辑，会导致：
- 快速模式（流拷贝）无法精确剪辑
- 播放器可能从错误位置开始播放
- 音视频可能不同步

**解决**：通过关键帧分析，智能选择剪辑策略，确保精确剪辑。

## 关键帧基础

### 什么是关键帧？

关键帧（I-frame）是视频压缩中的完整帧，包含完整的图像信息。

| 帧类型 | 说明 | 压缩率 | 用途 |
|--------|------|--------|------|
| **I-frame (关键帧)** | 完整帧，可独立解码 | 低 | 随机访问、剪辑点 |
| **P-frame (预测帧)** | 基于前一帧预测 | 中 | 时间冗余压缩 |
| **B-frame (双向预测帧)** | 基于前后帧预测 | 高 | 高压缩率 |

### 关键帧与剪辑

```python
# 示例：关键帧位置
时间轴：0.0s —— 2.5s —— 5.0s —— 7.5s —— 10.0s
关键帧：  ✓      ✓      ✓      ✓      ✓

# 如果在 3.0s 处剪辑
距离前一个关键帧（2.5s）：0.5 秒 ✓ 推荐（快速模式）
距离后一个关键帧（5.0s）：2.0 秒

# 如果在 6.3s 处剪辑
距离前一个关键帧（5.0s）：1.3 秒 ✓ 推荐（快速模式）
距离后一个关键帧（7.5s）：1.2 秒

# 如果在 9.2s 处剪辑
距离前一个关键帧（7.5s）：1.7 秒 ✓ 推荐（快速模式）
距离后一个关键帧（10.0s）：0.8 秒
```

## 核心功能

### 1. 关键帧检测

```python
from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer

analyzer = KeyFrameAnalyzer()

# 检测所有关键帧
keyframes = analyzer.detect_keyframes(
    video_path="input.mp4",
    tolerance=0.1  # 时间容差（秒）
)

# 返回：
# [0.0, 2.5, 5.0, 7.5, 10.0, 12.5, ...]

# 获取关键帧信息
info = analyzer.get_keyframe_info(
    video_path="input.mp4"
)

# 返回：
# {
#     "total_keyframes": 245,
#     "duration": 300.5,
#     "avg_keyframe_interval": 1.23,
#     "min_interval": 0.5,
#     "max_interval": 5.0
# }
```

### 2. 剪辑点质量评估

```python
# 评估单个剪辑点
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

# 返回：CutPointQuality 对象
print(f"位置: {quality.position}")
print(f"质量等级: {quality.quality_level}")
# → "excellent" | "good" | "fair" | "poor"

print(f"推荐模式: {quality.recommended_mode}")
# → "fast" | "precise" | "smart_cut"

print(f"距前一个关键帧: {quality.distance_to_keyframe_before} 秒")
print(f"距后一个关键帧: {quality.distance_to_keyframe_after} 秒")
print(f"最近关键帧时间: {quality.nearest_keyframe_time} 秒")
print(f"精度估计: {quality.precision_estimate}")
print(f"原因: {quality.reason}")
```

#### 质量等级标准

| 等级 | 距离关键帧 | 推荐模式 | 精度估计 |
|------|-----------|----------|----------|
| **excellent** | < 0.5 秒 | fast | ±0-1 帧 |
| **good** | 0.5-1.0 秒 | fast | ±1-2 帧 |
| **fair** | 1.0-2.0 秒 | smart_cut | ±2-3 帧 |
| **poor** | > 2.0 秒 | precise/smart_cut | ±3+ 帧 |

### 3. 批量评估剪辑点

```python
# 批量评估多个剪辑点
points = [30.5, 60.0, 90.5, 120.0]
qualities = analyzer.assess_multiple_cut_points(
    video_path="input.mp4",
    cut_points=points
)

# 返回：List[CutPointQuality]
for q in qualities:
    print(f"{q.position}s: {q.quality_level} ({q.recommended_mode})")
```

### 4. 关键帧时间轴导出

```python
# 导出为 JSON 格式
timeline_json = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="json",
    output_file="keyframe_timeline.json"
)

# JSON 结构：
# {
#   "video_path": "input.mp4",
#   "total_keyframes": 245,
#   "duration": 300.5,
#   "keyframes": [
#     {
#       "index": 0,
#       "time": 0.0,
#       "time_formatted": "00:00:00",
#       "frame_number": 0
#     },
#     {
#       "index": 1,
#       "time": 2.5,
#       "time_formatted": "00:00:02.500",
#       "frame_number": 60
#     },
#     ...
#   ]
# }

# 导出为 CSV 格式（用于 Excel 分析）
timeline_csv = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="csv",
    output_file="keyframe_timeline.csv"
)

# 导出为 Markdown 格式（用于文档）
timeline_md = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="markdown",
    output_file="keyframe_timeline.md"
)

# 导出为 TXT 格式（纯文本）
timeline_txt = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="txt",
    output_file="keyframe_timeline.txt"
)
```

#### 导出格式对比

| 格式 | 用途 | 优点 | 缺点 |
|------|------|------|------|
| **JSON** | 程序处理 | 结构化，易解析 | 文件较大 |
| **CSV** | Excel 分析 | 易导入表格 | 嵌套结构需展平 |
| **Markdown** | 文档 | 可读性好 | 格式限制 |
| **TXT** | 简单查看 | 最简单 | 缺少结构 |

## 使用场景

### 场景1：精确剪辑决策

```python
# 用户要在 30.5 秒处剪辑
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

if quality.recommended_mode == "fast":
    # 使用流拷贝，极快速度
    print("推荐快速模式：", quality.reason)
elif quality.recommended_mode == "smart_cut":
    # 使用 Smart Cut，平衡速度与质量
    print("推荐 Smart Cut：", quality.reason)
else:
    # 使用精确模式，重新编码
    print("推荐精确模式：", quality.reason)
```

### 场景2：批量剪辑点分析

```python
# 分析多个可能的剪辑点
cut_points = [30.0, 45.0, 60.0, 75.0, 90.0]
qualities = analyzer.assess_multiple_cut_points(
    video_path="input.mp4",
    cut_points=cut_points
)

# 选择最佳剪辑点
best_point = max(qualities, key=lambda q: q.quality_level)
print(f"最佳剪辑点: {best_point.position} 秒")
print(f"质量等级: {best_point.quality_level}")
```

### 场景3：导出时间轴用于分析

```python
# 导出关键帧时间轴，用于可视化分析
timeline = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="csv",
    output_file="keyframe_timeline.csv"
)

# 导入 Excel 分析关键帧分布
# - 计算平均关键帧间隔
# - 识别关键帧稀疏区域
# - 优化剪辑点选择
```

### 场景4：智能剪辑策略

```python
# 获取智能剪辑策略
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time=30.0,
    duration=60.0,
    video_path="input.mp4",
    max_encoded_segment=5.0
)

# 分析策略
print(f"模式: {strategy.mode}")
print(f"总重编码时长: {strategy.total_encoded_duration} 秒")
print(f"流拷贝时长: {strategy.copy_duration} 秒")

# 查看分段详情
for segment in strategy.segments:
    print(f"  {segment['type']}: {segment['start']}s - {segment['end']}s")
```

## 高级功能

### 自定义质量标准

```python
# 自定义质量等级阈值
analyzer = KeyFrameAnalyzer(
    excellent_threshold=0.3,  # excellent: < 0.3 秒
    good_threshold=0.8,       # good: 0.3-0.8 秒
    fair_threshold=1.5        # fair: 0.8-1.5 秒
)
```

### 时间轴导出自定义字段

```python
# 自定义导出字段
timeline = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="json",
    output_file="timeline.json",
    include_fields=[
        "index", "time", "time_formatted",
        "frame_number", "frame_type"
    ]
)
```

### 批量分析多个视频

```python
# 批量分析多个视频的关键帧
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    info = analyzer.get_keyframe_info(video_path=video)
    print(f"{video}: {info['total_keyframes']} 个关键帧")
```

## 性能优化

### 缓存关键帧数据

```python
# 缓存关键帧数据，避免重复检测
analyzer = KeyFrameAnalyzer(use_cache=True)

# 首次检测会缓存
keyframes1 = analyzer.detect_keyframes(video_path="input.mp4")

# 第二次从缓存读取
keyframes2 = analyzer.detect_keyframes(video_path="input.mp4")
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor

# 并行检测多个视频的关键帧
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(
            analyzer.detect_keyframes,
            video_path=video
        )
        for video in video_list
    ]
    results = [f.result() for f in futures]
```

## 最佳实践

### 1. 剪辑前先评估

```python
# 推荐流程
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

# 根据评估结果选择策略
if quality.recommended_mode == "fast":
    # 使用流拷贝
    pass
elif quality.recommended_mode == "smart_cut":
    # 使用 Smart Cut
    pass
else:
    # 使用精确模式
    pass
```

### 2. 批量剪辑时导出时间轴

```python
# 批量剪辑前导出所有关键帧
timeline = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="json",
    output_file="keyframe_timeline.json"
)

# 使用时间轴数据优化剪辑点
```

### 3. 长视频分析优化

```python
# 长视频（>1小时）建议分段分析
analyzer = KeyFrameAnalyzer()

# 方案1：只分析前 N 分钟
keyframes = analyzer.detect_keyframes(
    video_path="long_video.mp4",
    duration=300  # 只分析前 5 分钟
)

# 方案2：分析指定时间段
keyframes = analyzer.detect_keyframes(
    video_path="long_video.mp4",
    start_time=0,
    end_time=600  # 分析 0-10 分钟
)
```

## 故障排除

### 问题1：关键帧检测失败

**现象**：detect_keyframes() 返回空列表

**原因**：
- FFmpeg 未安装或不在 PATH
- 视频文件损坏
- 视频编码不支持

**解决**：
```bash
# 检查 FFmpeg 是否安装
ffmpeg -version

# 检查视频文件
ffprobe -v error -show_format -show_streams input.mp4
```

### 问题2：质量评估不准确

**现象**：评估结果与实际不符

**原因**：
- 时间容差设置不当
- 关键帧检测不完整

**解决**：
```python
# 调整时间容差
analyzer = KeyFrameAnalyzer(tolerance=0.05)  # 更精确

# 完整检测关键帧
keyframes = analyzer.detect_keyframes(
    video_path="input.mp4",
    complete=True  # 完整扫描
)
```

### 问题3：时间轴导出失败

**现象**：export_keyframe_timeline() 报错

**原因**：
- 输出文件路径不可写
- 磁盘空间不足
- 格式不支持

**解决**：
```python
# 检查输出路径
import os
os.makedirs("output", exist_ok=True)

# 使用绝对路径
timeline = analyzer.export_keyframe_timeline(
    video_path="input.mp4",
    output_format="json",
    output_file="/absolute/path/timeline.json"
)
```

## 相关文档

- [Smart Cut 指南](smart_cut_guide.md)
- [API 参考](api_reference.md)
- [快速入门](quickstart.md)
- [详细工作流](detailed_workflows.md)

---

**关键帧分析** - 让剪辑更智能、更精确！
