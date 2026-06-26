# Smart Cut 智能剪辑完整指南

## 概述

Smart Cut 是 ffmpeg-master 技能的核心创新功能，通过混合剪辑策略实现速度与质量的完美平衡。

### 核心优势

- **精确到帧**：重编码片段实现精确剪辑
- **速度极快**：大部分内容使用流拷贝（通常 90%+）
- **智能分段**：自动分析关键帧位置，生成最优分段策略
- **重编码少**：通常只需重编码 5-10% 的内容

### 适用场景

- 从视频中间/非关键帧位置精确剪辑
- 需要平衡速度和质量的大多数场景
- 不想牺牲精确度但追求快速处理

## 工作原理

### 1. 分析阶段

检测视频的关键帧位置，计算剪辑点与最近关键帧的距离：

```python
from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer

analyzer = KeyFrameAnalyzer()

# 检测关键帧
keyframes = analyzer.detect_keyframes(video_path="input.mp4")

# 返回：
# [0.0, 2.5, 5.0, 7.5, 10.0, ...]
```

### 2. 分段策略

Smart Cut 将剪辑任务分为三个片段：

| 片段 | 类型 | 时长 | 编码方式 | 说明 |
|------|------|------|----------|------|
| **起始段** | encode | 2-3 秒 | 重新编码 | 从剪辑点到下一个关键帧 |
| **中间段** | copy | 占 90%+ | 流拷贝 | 主体内容，无需重编码 |
| **结束段** | encode | 2-3 秒 | 重新编码 | 从最后一个关键帧到结束点 |

### 3. 执行阶段

分段执行 FFmpeg 命令，最后合并：

```bash
# 第1段：重编码起始片段
ffmpeg -ss 30.0 -i input.mp4 -t 2.5 -c:v libx264 -c:a aac segment1.mp4

# 第2段：流拷贝中间片段
ffmpeg -ss 32.5 -i input.mp4 -t 55.0 -c copy segment2.mp4

# 第3段：重编码结束片段
ffmpeg -ss 87.5 -i input.mp4 -t 2.5 -c:v libx264 -c:a aac segment3.mp4

# 合并所有片段
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

## 使用方法

### 基本用法

```python
from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer

analyzer = KeyFrameAnalyzer()

# 获取 Smart Cut 策略
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time=30.0,        # 起始时间（秒）
    duration=60.0,          # 剪辑时长（秒）
    video_path="input.mp4",
    max_encoded_segment=5.0 # 最大重编码片段时长（秒）
)

print(f"模式: {strategy.mode}")
print(f"总重编码时长: {strategy.total_encoded_duration} 秒")
print(f"流拷贝时长: {strategy.copy_duration} 秒")
print(f"重编码占比: {strategy.encoded_ratio*100:.1f}%")
```

### 返回结构

```python
# TrimStrategy 对象
{
    "mode": "smart_cut",
    "segments": [
        {"type": "encode", "start": 30.0, "end": 32.5, "duration": 2.5},
        {"type": "copy", "start": 32.5, "end": 87.5, "duration": 55.0},
        {"type": "encode", "start": 87.5, "end": 90.0, "duration": 2.5}
    ],
    "total_encoded_duration": 5.0,
    "copy_duration": 55.0,
    "encoded_ratio": 0.083  # 8.3%
}
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `start_time` | float | 必填 | 剪辑起始时间（秒） |
| `duration` | float | 必填 | 剪辑时长（秒） |
| `video_path` | str | 必填 | 视频文件路径 |
| `max_encoded_segment` | float | 5.0 | 单个重编码片段最大时长（秒） |

## 性能对比

### 三种剪辑模式对比

| 模式 | 速度 | 精度 | 重编码比例 | 适用场景 |
|------|------|------|-----------|----------|
| **快速模式** | 极快 | 低（关键帧对齐） | 0% | 预览、粗剪 |
| **精确模式** | 慢 | 高（精确到帧） | 100% | 精确剪辑 |
| **Smart Cut** | 快 | 高（精确到帧） | 通常 < 10% | 平衡速度与质量 |

### 实际案例

**场景**：剪辑 60 秒视频片段

| 模式 | 耗时 | 文件大小 | 质量 | 适用性 |
|------|------|----------|------|--------|
| 快速模式 | 5 秒 | 与源相同 | 可能有伪影 | 预览 |
| 精确模式 | 60 秒 | 与源相同 | 高 | 精确需求 |
| Smart Cut | 12 秒 | 与源相同 | 高 | 推荐 ✓ |

## 智能决策

### 自动推荐

技能会根据剪辑点与关键帧的距离自动推荐模式：

```python
from scripts.analyzers.keyframe_analyzer import KeyFrameAnalyzer

analyzer = KeyFrameAnalyzer()

# 评估剪辑点质量
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

print(f"质量等级: {quality.quality_level}")
print(f"推荐模式: {quality.recommended_mode}")
print(f"原因: {quality.reason}")
```

### 决策树

```
检测剪辑点与关键帧距离
    ↓
    ├─ 距离 < 2秒 → 推荐快速模式（流拷贝）
    ├─ 距离 > 5秒 → 推荐精确模式或 Smart Cut
    └─ 2-5秒 → 推荐 Smart Cut（最优）
```

## 高级用法

### 自定义分段策略

```python
# 调整最大重编码片段时长
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time=30.0,
    duration=60.0,
    video_path="input.mp4",
    max_encoded_segment=3.0  # 更精确，但重编码更多
)
```

### 与剪辑点质量评估结合

```python
# 先评估剪辑点质量
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

# 根据质量等级选择策略
if quality.recommended_mode == "smart_cut":
    strategy = analyzer.suggest_trim_strategy_smart_cut(
        start_time=30.5,
        duration=60.0,
        video_path="input.mp4"
    )
```

## 最佳实践

### 1. 优先使用 Smart Cut

- 对于大多数剪辑任务，Smart Cut 是最优选择
- 比快速模式更精确，比精确模式更快
- 重编码比例通常 < 10%

### 2. 合理设置 max_encoded_segment

- 默认值 5.0 秒适合大多数场景
- 追求速度可以设置为 3.0 秒
- 追求质量可以设置为 8.0 秒

### 3. 先评估再剪辑

```python
# 推荐流程
quality = analyzer.assess_cut_point_quality(
    video_path="input.mp4",
    cut_point=30.5
)

if quality.recommended_mode == "smart_cut":
    strategy = analyzer.suggest_trim_strategy_smart_cut(...)
    # 执行 Smart Cut
```

### 4. 批量处理优化

```python
# 批量处理时使用 Smart Cut
for video in video_list:
    strategy = analyzer.suggest_trim_strategy_smart_cut(
        start_time=30.0,
        duration=60.0,
        video_path=video
    )
    # 执行分段处理
```

## 故障排除

### 问题1：重编码比例过高

**现象**：重编码占比 > 20%

**原因**：
- 剪辑点附近关键帧稀疏
- max_encoded_segment 设置过大

**解决**：
```python
# 降低 max_encoded_segment
strategy = analyzer.suggest_trim_strategy_smart_cut(
    start_time=30.0,
    duration=60.0,
    video_path="input.mp4",
    max_encoded_segment=3.0  # 从 5.0 降到 3.0
)
```

### 问题2：剪辑不精确

**现象**：剪辑点有偏差

**原因**：
- 关键帧检测不准确
- 时间戳问题

**解决**：
```python
# 添加音视频同步参数
ffmpeg -i input.mp4 -ss 30.0 -t 60.0 \
  -avoid_negative_ts make_zero \
  -fflags +genpts \
  -c:v libx264 -c:a aac output.mp4
```

### 问题3：合并后视频质量下降

**现象**：合并后视频有质量损失

**原因**：
- 重编码参数不一致
- 编码器配置不当

**解决**：
```python
# 使用统一的编码参数
ffmpeg -i segment1.mp4 -c:v libx264 -preset medium -crf 23 segment1_re.mp4
ffmpeg -i segment2.mp4 -c:v libx264 -preset medium -crf 23 segment2_re.mp4
ffmpeg -i segment3.mp4 -c:v libx264 -preset medium -crf 23 segment3_re.mp4

# 合并
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

## 相关文档

- [关键帧分析指南](keyframe_analysis.md)
- [API 参考](api_reference.md)
- [快速入门](quickstart.md)
- [详细工作流](detailed_workflows.md)

---

**Smart Cut** - 让剪辑既快又精确！
