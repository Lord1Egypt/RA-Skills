---
name: "auto-iteration"
version: "1.0.0"
description: "安全的自动任务迭代和优化系统"
author: "AI Skills Team"
tags: ["迭代", "优化", "自动化", "工作流"]
requires: []
---

# AI自动迭代技能

安全的自动任务迭代和优化系统，支持质量评估和自动重试。

## 技能描述

自动执行任务并根据质量评估结果进行迭代优化，直到达到预期质量标准。支持工具白名单、危险操作检测和完整的历史记录。

## 使用场景

- 用户："生成一份报告，如果不满意就改进" → 自动迭代优化
- 用户："分析这段代码并优化" → 评估质量后自动改进
- 用户："创建一个方案，确保质量达标" → 迭代直到满足标准
- 用户："执行任务并记录过程" → 完整日志和历史记录

## 工具和依赖

### 工具列表

- `scripts/iteration_agent.py`：核心迭代引擎

### 内置工具

| 工具 | 功能 | 参数 |
|------|------|------|
| search | 搜索内容 | query, max_results |
| read | 读取文件 | file_path |
| write | 写入文件 | file_path, content |
| calculate | 安全计算 | expression |
| validate | 验证数据 | data, rules |
| analyze | 分析内容 | content |

### API密钥

无

### 外部依赖

- Python 3.7+（仅使用标准库）

## 配置说明

### 配置参数

```python
agent = IterationAgent(
    max_iterations=3,        # 最大迭代次数
    quality_threshold=0.7    # 质量阈值 (0-1)
)
```

### 数据存储位置

任务日志：`~/.ai_iteration_log.db`

## 使用示例

### 基本用法

```python
from iteration_agent import IterationAgent

# 创建Agent
agent = IterationAgent(max_iterations=3, quality_threshold=0.7)

# 定义任务步骤
task_steps = [
    {'tool': 'write', 'params': {'file_path': 'output.txt', 'content': 'Hello AI'}},
    {'tool': 'read', 'params': {'file_path': 'output.txt'}},
    {'tool': 'analyze', 'params': {'content': 'Hello AI'}},
]

# 执行任务（自动迭代直到达标）
result = agent.run_task('文本处理任务', task_steps)
```

### 场景1：自动优化文本

用户："写一段产品介绍，质量要达到8分以上"

AI：
```python
agent = IterationAgent(quality_threshold=0.8)
task_steps = [
    {'tool': 'write', 'params': {'content': '生成产品介绍'}},
    {'tool': 'analyze', 'params': {'evaluate_quality': True}},
]
result = agent.run_task('产品介绍生成', task_steps)
# 自动迭代改进，直到质量达标
```

### 场景2：文件处理任务

用户："读取data.txt，分析内容，保存报告"

AI：
```python
task_steps = [
    {'tool': 'read', 'params': {'file_path': 'data.txt'}},
    {'tool': 'analyze', 'params': {'type': 'content_analysis'}},
    {'tool': 'write', 'params': {'file_path': 'report.txt'}},
]
result = agent.run_task('数据分析任务', task_steps)
```

### 场景3：自定义工具

用户："添加一个自定义工具来发送通知"

AI：
```python
def send_notification(**kwargs):
    # 自定义通知逻辑
    return {'success': True, 'message': '已发送通知'}

agent.tools['notify'] = send_notification
```

## 故障排除

### 问题1：任务未达标但停止迭代

**现象**：质量未达标但已达到最大迭代次数

**解决**：
1. 提高 `max_iterations` 参数
2. 降低 `quality_threshold` 阈值
3. 检查任务步骤是否合理

### 问题2：危险操作被阻止

**现象**：提示"危险操作已阻止"

**解决**：
- 这是安全机制，阻止危险命令
- 使用白名单内的安全工具
- 或明确告知操作是安全的

### 问题3：文件路径错误

**现象**：找不到文件或路径错误

**解决**：
- 使用绝对路径
- 或确保当前工作目录正确
- 只允许写入当前目录的文件

## 注意事项

1. **迭代限制**：默认最多3次迭代，避免无限循环
2. **质量阈值**：默认0.7，可根据需求调整
3. **安全优先**：危险操作会被自动阻止
4. **只写当前**：只允许写入当前目录的文件
5. **定期备份**：建议定期备份任务日志数据库
