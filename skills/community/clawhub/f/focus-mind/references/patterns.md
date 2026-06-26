# FocusMind 设计模式参考

本文档提供 FocusMind 技能的设计模式和最佳实践参考。

## 1. 上下文分析模式

### 1.1 滑动窗口模式

适用于需要保留最近和最早期上下文，但压缩中间部分的场景：

```
[早期重要信息] → [压缩中间] → [最近N条]
```

实现参考 (`summarize.py`):

```python
def compress_messages(messages, preserve_recent=5):
    recent = messages[-preserve_recent:]
    middle = messages[len(messages)//4 : len(messages)-preserve_recent]
    # 对 middle 进行语义压缩
    return compress(middle) + recent
```

### 1.2 分层存储模式

将信息分为不同层次：

- **短期上下文**: 当前任务直接相关的信息
- **中期记忆**: 最近项目的关键信息
- **长期记忆**: 重要决策、用户偏好等

### 1.3 关键点提取模式

从长上下文中提取关键点：

```python
def extract_key_points(text):
    # 1. 提取包含数字的句子
    # 2. 提取包含决策关键词的句子
    # 3. 提取包含TODO/待办的句子
    return key_points
```

## 2. 目标追踪模式

### 2.1 主目标 + 子目标结构

```
主目标: 构建一个博客系统
├── 子目标1: 用户系统 [完成]
├── 子目标2: 文章CRUD [进行中]
├── 子目标3: 评论功能 [待处理]
└── 子目标4: 标签系统 [待处理]
```

### 2.2 阶段检测

基于对话内容检测当前阶段：

| 阶段 | 关键词 | 特征 |
|------|--------|------|
| 规划 | 计划、设计、方案 | 需求讨论 |
| 实现 | 开发、编码、实现 | 具体执行 |
| 测试 | 测试、验证、debug | 验证功能 |
| 收尾 | 完成、整理、优化 | 收尾工作 |

### 2.3 进度追踪

```python
def track_progress(goals):
    completed = sum(1 for g in goals if g.completed)
    total = len(goals)
    return f"{completed}/{total} 完成 ({completed/total*100:.0f}%)"
```

## 3. 摘要生成模式

### 3.1 结构化摘要模板

```markdown
## 上下文摘要

### 核心任务
[一句话描述]

### 关键信息
- 信息点1
- 信息点2

### 待办事项
- [ ] 待办1
- [ ] 待办2

### 历史决策
- 决策1: 原因
- 决策2: 原因
```

### 3.2 压缩策略

| 场景 | 策略 | 压缩比 |
|------|------|--------|
| 短上下文 | 不压缩 | 1:1 |
| 中等上下文 | 选择性保留 | 2:1 |
| 长上下文 | 关键点提取 | 5:1 |

### 3.3 语义压缩

对中间对话进行语义压缩：

```python
def semantic_compress(messages):
    compressed = []
    for msg in messages:
        content = msg.content
        # 只保留关键句子
        key_sentences = extract_key_sentences(content)
        compressed.append(key_sentences)
    return compressed
```

## 4. 触发机制模式

### 4.1 阈值触发

```python
def should_trigger(token_count, threshold=10000):
    return token_count > threshold
```

### 4.2 周期性触发

```python
import time

class PeriodicTrigger:
    def __init__(self, interval_minutes=30):
        self.interval = interval_minutes * 60
        self.last_check = time.time()
    
    def should_check(self):
        now = time.time()
        if now - self.last_check > self.interval:
            self.last_check = now
            return True
        return False
```

### 4.3 组合触发

```python
def should_clear_fog(context):
    # 阈值触发 OR 周期性触发 OR 手动触发
    return (
        context.tokens > THRESHOLD or
        periodic_trigger.should_check() or
        context.manual_trigger
    )
```

## 5. 集成模式

### 5.1 Heartbeat 集成

在每次 heartbeat 时轻量检查：

```python
def on_heartbeat(context):
    health = analyze_context_health(context)
    if health.level in ["yellow", "red"]:
        # 输出提示，但不打断
        print(f"🧠 {health.emoji} {health.label}: {health.recommendations[0]}")
```

### 5.2 主动介入模式

当上下文非常长时，主动建议：

```python
def proactive_cleanup(context):
    health = analyze_context_health(context)
    if health.level == "red":
        # 主动生成摘要
        summary = generate_summary(context)
        goals = extract_goals(context)
        # 输出完整建议
        return format_cleanup_suggestion(health, summary, goals)
```

### 5.3 用户请求模式

响应用户的明确请求：

```python
def handle_user_request(context, request):
    if "整理" in request or "清除脑雾" in request:
        return full_cleanup(context)
    elif "状态" in request or "health" in request.lower():
        return analyze_context_health(context)
    elif "目标" in request:
        return extract_goals(context)
```

## 6. 最佳实践

### 6.1 不修改原始上下文

FocusMind 技能应该：
- ✅ 只提供分析和建议
- ✅ 生成摘要供 Agent 参考
- ❌ 不自动修改或删除原始上下文

### 6.2 渐进式介入

根据上下文健康度采取不同行动：

| 等级 | 行动 | 干扰程度 |
|------|------|----------|
| 绿色 | 忽略 | 无 |
| 黄色 | 提示建议 | 低 |
| 红色 | 主动建议 | 中 |
| 危险 | 强烈建议清理 | 高 |

### 6.3 保留关键信息

清理时必须保留：
- 原始任务/目标
- 已完成的关键步骤
- 重要决策和原因
- 未完成的待办
- 必要的上下文背景

### 6.4 定期优化

根据使用反馈持续改进：
1. 收集触发频率数据
2. 分析摘要质量
3. 调整阈值参数
4. 优化压缩算法

## 7. 常见问题

### Q: 上下文多长应该触发清理？

A: 默认 10000 tokens，可根据实际情况调整。短任务 5000，长任务可到 20000。

### Q: 摘要会丢失重要信息吗？

A: 可能会有损失，建议：
1. 使用关键点提取而非全文压缩
2. 保留开头（目标）和结尾（最近状态）
3. 重要决策单独标记

### Q: 如何平衡压缩和保真？

A: 采用分层策略：
- 核心目标 → 必须保留
- 关键决策 → 必须保留
- 详细实现 → 可压缩
- 重复内容 → 去除

---

本文档应与 SKILL.md 配合使用，提供实现在设计层面的参考。
