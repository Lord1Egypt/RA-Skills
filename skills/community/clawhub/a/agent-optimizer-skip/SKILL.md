---
name: agent-optimizer
description: V6.1 Agent 性能优化器 - 基于轨迹分析和奖励反馈的轻量级优化框架
homepage: https://github.com/openclaw/openclaw
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["python3"],"env":[]},"primaryEnv":""}}
---

# Agent Optimizer ⚡

**V6.1 联邦智能专用 - 轻量级 Agent 性能优化框架**

无需外部依赖，基于 OpenClaw 原生能力实现 Agent 性能持续优化。

## 🔥 核心功能

### 1. 轨迹记录
- 自动记录 Agent 执行轨迹
- 保存输入、输出、工具调用、耗时
- 结构化存储便于分析

### 2. 奖励反馈
- 支持多种奖励信号（用户评分、任务完成度、ROI 等）
- 累积奖励统计
- 奖励趋势分析

### 3. 提示词优化
- 基于奖励反馈自动优化提示词
- A/B 测试不同提示词版本
- 保留历史版本可回滚

### 4. 性能分析
- 执行耗时分析
- 成功率统计
- ROI 计算与追踪

## 📦 安装

无需安装，已集成到 OpenClaw V6.1 工作区。

## 🚀 快速开始

### 1. 初始化优化器

```python
# 在子 Agent 工作区创建 optimizer 目录
mkdir -p /workspace/subagents/{agent_id}/optimizer

# 创建配置文件
cat > /workspace/subagents/{agent_id}/optimizer/config.json << 'EOF'
{
  "agent_id": "techbot",
  "optimization_target": "tutorial_quality",
  "metrics": ["user_rating", "completion_rate", "roi"],
  "ab_test": true
}
EOF
```

### 2. 记录执行轨迹

```python
import json
from datetime import datetime

def record_trajectory(agent_id, task, output, metrics):
    """记录 Agent 执行轨迹"""
    timestamp = datetime.now().isoformat()
    
    trajectory = {
        "agent_id": agent_id,
        "timestamp": timestamp,
        "task": task,
        "output": output,
        "metrics": metrics,
        "prompt_version": get_current_prompt_version()
    }
    
    # 保存到轨迹文件
    with open(f'/workspace/subagents/{agent_id}/optimizer/trajectories.jsonl', 'a') as f:
        f.write(json.dumps(trajectory) + '\n')
    
    return trajectory
```

### 3. 发射奖励信号

```python
def emit_reward(agent_id, trajectory_id, reward_value, reward_type="user_rating"):
    """发射奖励信号"""
    timestamp = datetime.now().isoformat()
    
    reward = {
        "agent_id": agent_id,
        "trajectory_id": trajectory_id,
        "timestamp": timestamp,
        "reward_value": reward_value,
        "reward_type": reward_type
    }
    
    # 保存到奖励文件
    with open(f'/workspace/subagents/{agent_id}/optimizer/rewards.jsonl', 'a') as f:
        f.write(json.dumps(reward) + '\n')
    
    return reward
```

### 4. 分析性能并优化

```python
def analyze_and_optimize(agent_id):
    """分析性能并生成优化建议"""
    import json
    
    # 加载轨迹数据
    trajectories = []
    with open(f'/workspace/subagents/{agent_id}/optimizer/trajectories.jsonl', 'r') as f:
        for line in f:
            trajectories.append(json.loads(line))
    
    # 加载奖励数据
    rewards = []
    with open(f'/workspace/subagents/{agent_id}/optimizer/rewards.jsonl', 'r') as f:
        for line in f:
            rewards.append(json.loads(line))
    
    # 计算平均奖励
    avg_reward = sum(r['reward_value'] for r in rewards) / len(rewards) if rewards else 0
    
    # 分析高奖励和低奖励轨迹
    high_reward_trajectories = [t for t in trajectories if get_reward(t['task'], rewards) > avg_reward]
    low_reward_trajectories = [t for t in trajectories if get_reward(t['task'], rewards) < avg_reward]
    
    # 生成优化建议
    optimization_report = {
        "agent_id": agent_id,
        "total_trajectories": len(trajectories),
        "total_rewards": len(rewards),
        "average_reward": avg_reward,
        "high_reward_patterns": analyze_patterns(high_reward_trajectories),
        "low_reward_patterns": analyze_patterns(low_reward_trajectories),
        "suggestions": generate_suggestions(high_reward_trajectories, low_reward_trajectories)
    }
    
    # 保存报告
    with open(f'/workspace/subagents/{agent_id}/optimizer/optimization_report.json', 'w') as f:
        json.dump(optimization_report, f, indent=2)
    
    return optimization_report
```

## 📊 使用场景

### TechBot - 教程质量优化
```python
# 记录教程生成轨迹
trajectory = record_trajectory(
    agent_id="techbot",
    task="编写 AI Agent 教程",
    output=tutorial_content,
    metrics={
        "word_count": len(tutorial_content),
        "code_blocks": count_code_blocks(tutorial_content),
        "execution_time": execution_time
    }
)

# 用户评分后发射奖励
emit_reward(
    agent_id="techbot",
    trajectory_id=trajectory['task'],
    reward_value=user_rating,  # 1-5 分
    reward_type="user_rating"
)

# 定期分析优化
report = analyze_and_optimize("techbot")
print(f"平均评分：{report['average_reward']:.2f}")
print(f"优化建议：{report['suggestions']}")
```

### FinanceBot - ROI 预测优化
```python
# 记录 ROI 预测轨迹
trajectory = record_trajectory(
    agent_id="financebot",
    task="预测任务 ROI",
    output={"predicted_roi": 2.5, "confidence": 0.85},
    metrics={
        "prediction_accuracy": 0.0,  # 待实际结果出来后更新
        "confidence_score": 0.85
    }
)

# 实际结果出来后发射奖励
actual_roi = 2.3
prediction_error = abs(2.5 - actual_roi)
reward = 1.0 / (1.0 + prediction_error)  # 误差越小奖励越高

emit_reward(
    agent_id="financebot",
    trajectory_id=trajectory['task'],
    reward_value=reward,
    reward_type="prediction_accuracy"
)
```

### AutoBot - 抓取成功率优化
```python
# 记录数据抓取轨迹
trajectory = record_trajectory(
    agent_id="autobot",
    task="抓取网站数据",
    output={"status": "success", "data_points": 150},
    metrics={
        "success": True,
        "data_points": 150,
        "retry_count": 0
    }
)

# 根据成功率发射奖励
reward = 1.0 if trajectory['output']['status'] == 'success' else 0.0
emit_reward(
    agent_id="autobot",
    trajectory_id=trajectory['task'],
    reward_value=reward,
    reward_type="success_rate"
)
```

## 📈 性能分析工具

### 1. 奖励趋势分析
```bash
# 生成奖励趋势图数据
python3 /workspace/skills/agent-optimizer/scripts/analyze_trends.py --agent techbot
```

### 2. A/B 测试
```python
# 测试两个提示词版本
def ab_test_prompt(agent_id, task, version_a, version_b):
    # 随机选择版本
    import random
    version = random.choice(['a', 'b'])
    
    if version == 'a':
        output = execute_with_prompt(task, version_a)
    else:
        output = execute_with_prompt(task, version_b)
    
    # 记录并比较结果
    return output, version
```

### 3. 提示词版本管理
```python
# 保存提示词版本
def save_prompt_version(agent_id, version, prompt_template):
    with open(f'/workspace/subagents/{agent_id}/optimizer/prompts/v{version}.txt', 'w') as f:
        f.write(prompt_template)

# 加载提示词版本
def load_prompt_version(agent_id, version):
    with open(f'/workspace/subagents/{agent_id}/optimizer/prompts/v{version}.txt', 'r') as f:
        return f.read()
```

## 🔧 配置文件示例

### optimizer/config.json
```json
{
  "agent_id": "techbot",
  "optimization_target": "tutorial_quality",
  "metrics": ["user_rating", "completion_rate", "roi"],
  "ab_test": true,
  "prompt_versions": ["v1.0", "v1.1", "v2.0"],
  "current_version": "v2.0",
  "optimization_interval": 100
}
```

### optimizer/prompts/v2.0.txt
```
你是一个专业的技术教程作家。
请编写一个关于 {topic} 的教程。

要求：
1. 结构清晰，包含简介、步骤、示例代码
2. 代码可运行，有详细注释
3. 语言简洁，避免冗长
4. 包含实际应用场景

教程长度：{word_count} 字左右
```

## 📁 目录结构

```
/workspace/subagents/{agent_id}/optimizer/
├── config.json              # 优化配置
├── trajectories.jsonl       # 执行轨迹记录
├── rewards.jsonl            # 奖励信号记录
├── optimization_report.json # 优化分析报告
├── prompts/                 # 提示词版本目录
│   ├── v1.0.txt
│   ├── v1.1.txt
│   └── v2.0.txt
└── scripts/                 # 分析脚本
    ├── analyze_trends.py
    ├── ab_test.py
    └── generate_report.py
```

## ⚠️ 注意事项

1. **隐私保护**: 轨迹数据可能包含敏感信息，注意脱敏
2. **存储管理**: 定期清理旧轨迹数据，避免文件过大
3. **奖励设计**: 奖励函数要合理，避免优化错方向
4. **版本控制**: 提示词版本要记录清晰，方便回滚

## 🎯 与 Agent Lightning 对比

| 功能 | Agent Lightning | Agent Optimizer |
|------|----------------|-----------------|
| 安装复杂度 | 需要 pip 安装 | ✅ 零安装 |
| 依赖 | Python 包依赖 | ✅ 无依赖 |
| RL 训练 | ✅ 完整 RL 支持 | 基础奖励反馈 |
| 提示词优化 | ✅ 自动优化 | ✅ 手动+A/B 测试 |
| 集成难度 | 中等 | ✅ 简单 |
| 适用场景 | 大规模训练 | ✅ 轻量级持续优化 |

## 🚀 未来扩展

- [ ] 自动化提示词优化算法
- [ ] 集成简单 RL 算法（如 Bandit）
- [ ] Web Dashboard 可视化
- [ ] 多 Agent 协同优化
- [ ] 奖励函数模板库

---

*Agent Optimizer - V6.1 原生性能优化框架*
