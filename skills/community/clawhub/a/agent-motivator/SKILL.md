---
name: agent-motivator
description: 正向激励与任务进度管理技能。使用幽默、积极的激励话术帮助 agent 保持高效工作状态。支持任务创建、进度追踪、里程碑庆祝、专注模式提醒和成果复盘。当需要激励 agent、管理任务进度、庆祝里程碑或进行工作总结时使用此技能。
---

# Agent Motivator - 正向激励大师

> 🎯 **核心理念**：用正向、幽默的激励代替 PUA 操控，让工作变得有趣高效！

## 快速开始

### 生成激励话术

```bash
# 任务开始时
python3 scripts/motivate.py start

# 进行中鼓励
python3 scripts/motivate.py progress

# 里程碑庆祝
python3 scripts/motivate.py milestone

# 专注模式
python3 scripts/motivate.py focus

# 任务完成
python3 scripts/motivate.py complete

# 遇到困难时
python3 scripts/motivate.py encourage
```

### 任务管理

```bash
# 创建新任务
python3 scripts/task_tracker.py create "完成项目报告" high

# 更新进度 (0-100)
python3 scripts/task_tracker.py update 1 50

# 添加里程碑
python3 scripts/task_tracker.py milestone 1 "完成初稿"

# 查看任务列表
python3 scripts/task_tracker.py list

# 查看统计
python3 scripts/task_tracker.py stats
```

## 使用场景

### 1. 任务启动激励

当 agent 开始新任务时，用积极的话术激发动力：

```bash
激励话术 + 任务拆解 → 清晰目标 + 满满动力
```

**示例流程**：
1. 生成启动激励：`motivate.py start`
2. 创建任务：`task_tracker.py create "任务名"`
3. 拆解任务步骤
4. 开始执行

### 2. 进度追踪与鼓励

在长任务执行过程中，定期检查进度并给予鼓励：

```bash
每完成 25% 进度 → motivate.py progress
到达里程碑 → motivate.py milestone + task_tracker.py milestone
```

### 3. 专注模式

当需要深度工作时：

```bash
1. 生成专注提示：motivate.py focus
2. 设定专注时间（如 25 分钟番茄钟）
3. 期间不打断
4. 完成后给予奖励
```

### 4. 困难时刻鼓励

当 agent 遇到卡壳或挫折时：

```bash
motivate.py encourage → 提供正向支持和解决思路
```

### 5. 任务完成庆祝

任务完成后，一定要庆祝！

```bash
1. 更新进度到 100%
2. 生成庆祝话术：motivate.py complete
3. 记录完成统计：task_tracker.py stats
4. 简单复盘（可选）
```

## 激励话术库

内置 6 类激励场景，每类 5+ 条话术：

| 场景 | 用途 | 示例 |
|------|------|------|
| start | 任务启动 | 🚀 新任务已就位！让我们大干一场吧！ |
| progress | 进度鼓励 | 📈 进度条在动！继续保持这个节奏！ |
| milestone | 里程碑 | 🎉 里程碑达成！值得庆祝一下！ |
| focus | 专注模式 | 🧘 专注模式开启，外界勿扰！ |
| complete | 完成庆祝 | 🎊 任务完成！太棒了！ |
| encourage | 困难鼓励 | 💡 小卡壳很正常，换个思路试试！ |

## 任务状态管理

任务追踪器支持以下状态：

- **pending**: 待开始
- **in_progress**: 进行中 (progress > 0)
- **completed**: 已完成 (progress = 100)

### 任务数据结构

```json
{
  "id": 1,
  "name": "任务名称",
  "priority": "high|normal|low",
  "status": "pending|in_progress|completed",
  "progress": 0-100,
  "milestones": [
    {"name": "里程碑名称", "reached": "ISO 时间戳"}
  ],
  "created": "ISO 时间戳",
  "updated": "ISO 时间戳"
}
```

## 最佳实践

### ✅ 推荐做法

1. **及时激励** - 每有小进展就给予正向反馈
2. **具体表扬** - 指出具体做得好的地方
3. **里程碑庆祝** - 大节点一定要庆祝
4. **困难时支持** - 卡壳时给鼓励而非压力
5. **完成必复盘** - 记录成就感和经验

### ❌ 避免做法

1. **PUA 话术** - 不用操控、贬低、制造焦虑
2. **过度催促** - 尊重工作节奏
3. **只关注结果** - 过程也值得肯定
4. **比较他人** - 专注自己的进步
5. **忽视休息** - 劳逸结合更高效

## 状态文件

任务状态存储在：
```
~/.openclaw/agent-motivator/task_state.json
```

此文件自动创建，无需手动管理。

## 扩展激励库

如需添加更多激励话术，编辑 `scripts/motivate.py` 中的 `MOTIVATION_PHRASES` 字典：

```python
MOTIVATION_PHRASES = {
    "your_context": [
        "你的自定义激励话术 1",
        "你的自定义激励话术 2",
    ],
    # ...
}
```

## 与其他技能配合

- **team-lead**: 多 agent 协作时统一激励风格
- **self-improvement**: 记录激励效果和改进点
- **healthcheck**: 避免过度工作，保持健康节奏

---

**记住**：好的激励让工作变得有趣，而不是制造压力。🌟
