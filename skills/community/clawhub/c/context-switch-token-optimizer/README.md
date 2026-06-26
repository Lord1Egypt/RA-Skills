# Context Switch Token Optimizer - 使用指南

## 🎯 技能概述
智能对话上下文切换和Token优化技能，通过分析对话主题连续性来自动管理上下文，确保相关对话的连续性，同时在不同话题间高效切换以节省Token使用。

## 🚀 核心功能

### 1. 对话主题管理
- **自动总结**: 每次回复后总结对话的一句话主题
- **连续性判断**: 判断当前对话是否与之前对话连续相关
- **智能切换**: 识别明显无关的话题，自动切换上下文
- **历史记忆**: 搜索相关记忆并渐进加载

### 2. Token优化策略
- **实时监控**: 监控当前Token使用情况
- **自动优化**: 使用率超过70%时自动触发优化
- **压缩机制**: 智能压缩上下文内容
- **清理策略**: 清理过期和无用内容

### 3. 上下文搜索与加载
- **关键词提取**: 自动提取对话关键词
- **记忆匹配**: 搜索相关记忆文件
- **渐进加载**: 按需加载记忆内容
- **相关性评分**: 计算记忆与当前主题的相关性

## 📋 使用方法

### 基本命令

```bash
# 处理对话内容
python3 context-switch-token-optimizer.py --process "对话内容"

# 生成状态报告
python3 context-switch-token-optimizer.py --status

# 重置上下文
python3 context-switch-token-optimizer.py --reset

# 运行测试
python3 context-switch-token-optimizer.py --test
```

### 配置管理

```bash
# 使用自定义配置
python3 context-switch-token-optimizer.py --config custom-config.json --status

# 查看当前配置
python3 context_manager.py --show-state
```

### 环境变量（与 SKILL.md / 代码一致）

| 变量 | 作用 |
|------|------|
| `CONTEXT_HISTORY_SIZE` | 覆盖 `context_switch.max_topic_history`（1–100） |
| `MEMORY_SEARCH_DEPTH` | 覆盖 `memory_search.search_depth`（1–3） |
| `TOKEN_OPTIMIZER_ENABLED` | `false`/`0` 关闭自动 Token 优化触发 |
| `CONTEXT_SWITCH_LOG_LEVEL` | `DEBUG`/`INFO`/`WARNING`/`ERROR` |

## 🔧 工具详解

### 1. 上下文管理器 (`context_manager.py`)

```bash
# 处理单个对话
python3 context_manager.py --content "关于记忆管理技能的问题"

# 测试主题切换
python3 context_manager.py --test-switch

# 查看当前状态
python3 context_manager.py --show-state

# 重置状态
python3 context_manager.py --reset
```

**主要功能**:
- 总结对话主题
- 判断主题连续性
- 管理上下文状态
- 搜索和加载相关记忆

### 2. Token优化器 (`token_optimizer.py`)

```bash
# 监控Token使用
python3 token_optimizer.py --monitor

# 触发优化
python3 token_optimizer.py --trigger-optimization

# 生成优化报告
python3 token_optimizer.py --report

# 获取优化建议
python3 token_optimizer.py --suggestions

# 测试特定Token量
python3 token_optimizer.py --test-usage 60000
```

**主要功能**:
- 监控Token使用情况
- 触发优化措施
- 生成优化报告
- 提供优化建议

### 3. 主工具 (`context-switch-token-optimizer.py`)

```bash
# 处理对话（推荐使用）
python3 context-switch-token-optimizer.py --process "你的对话内容"

# 完整测试
python3 context-switch-token-optimizer.py --test

# 状态报告
python3 context-switch-token-optimizer.py --status
```

## 📊 状态报告说明

### 健康评分系统
```
0-20: 严重问题，需要立即优化
21-50: 需要注意，建议优化
51-80: 正常范围，维持现状
81-100: 状态良好，无需优化
```

### Token状态等级
- **Healthy**: < 50% - 状态良好
- **Warning**: 50-70% - 需要注意
- **Critical**: 70-90% - 需要优化
- **Emergency**: > 90% - 紧急处理

### 优化类型
1. **压缩上下文**: 保留重要内容，压缩历史记录
2. **清理记忆**: 清理过期和无用记忆内容
3. **重置上下文**: 完全重置，开始新的对话

## 🎯 实际应用场景

### 1. 多项目管理
```bash
# 项目1: 记忆技能开发
python3 context-switch-token-optimizer.py --process "记忆管理技能的设计方案"

# 切换到项目2: 飞书集成
python3 context-switch-token-optimizer.py --process "飞书API权限问题处理"

# 查看切换状态
python3 context-switch-token-optimizer.py --status
```

### 2. 学习和研究
```bash
# 深入研究一个主题
python3 context-switch-token-optimizer.py --process "机器学习算法原理和应用"

# 切换到其他学习内容
python3 context-switch-token-optimizer.py --process "Python编程最佳实践"

# 获取优化建议
python3 token_optimizer.py --suggestions
```

### 3. 日常对话管理
```bash
# 一般对话
python3 context-switch-token-optimizer.py --process "今天的工作进展如何？"

# 技术问题讨论
python3 context-switch-token-optimizer.py --process "遇到Token优化的问题"

# 查看Token使用情况
python3 token_optimizer.py --monitor
```

## 📈 监控和调试

### 日志查看
```bash
# 查看上下文状态文件
cat memory/context_switch_state.json

# 查看Token使用历史（需在 skill 目录下执行）
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from token_optimizer import TokenOptimizer
optimizer = TokenOptimizer()
for usage in optimizer.usage_log[-5:]:
    print(f'{usage.timestamp}: {usage.tokens_used} tokens')
"
```

### 性能监控
```bash
# 监控Token使用趋势
python3 context-switch-token-optimizer.py --status | grep 'usage_percentage'

# 查看主题切换统计
python3 context-switch-token-optimizer.py --status | grep 'switch_count'

# 检查健康分数
python3 context-switch-token-optimizer.py --status | grep 'health_score'
```

## 🔍 故障排除

### 常见问题

**Q: 主题切换过于频繁**
A: 调整配置文件中的 `similarity_threshold`，提高相似度要求

**Q: Token使用过高**
A: 检查 `compression_threshold` 设置，可以降低到50,000

**Q: 相关记忆加载不准确**
A: 调整 `memory_relevance_threshold`，降低相关性要求

**Q: 优化建议不准确**
A: 检查关键词提取算法，调整 `keyword_limit` 设置

### 配置调优建议

```json
{
  "context_switch": {
    "similarity_threshold": 0.8,  // 提高要求，减少切换
    "time_decay_factor": 0.9,     // 加速时间衰减
    "max_topic_history": 5        // 减少历史记录
  },
  "token_optimization": {
    "compression_threshold": 50000, // 降低压缩阈值
    "context_cleanup_threshold": 0.7
  }
}
```

---

**版本**: v1.0  
**维护**: Hermosa  
**最后更新**: 2026-03-17

## 🎯 快速开始

```bash
# 1. 运行完整测试
python3 context-switch-token-optimizer.py --test

# 2. 处理你的第一个对话
python3 context-switch-token-optimizer.py --process "你好，我想了解这个技能"

# 3. 查看状态
python3 context-switch-token-optimizer.py --status
```