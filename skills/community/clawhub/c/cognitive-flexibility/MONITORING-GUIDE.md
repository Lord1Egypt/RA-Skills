# Cognitive Flexibility Skill 监控指南

**版本:** v2.1  
**创建时间:** 2026-04-05  
**功能:** 使用情况追踪和效果评估

---

## 📊 监控功能概述

Cognitive Flexibility Skill 内置完整的使用监控功能，用于：

1. **追踪使用情况** - 记录每次使用的时间、模式、任务
2. **评估效果** - 统计成功率、置信度、评分
3. **模式对比** - 对比 4 种认知模式的效果
4. **优化建议** - 基于数据提供优化建议

---

## 🔧 监控模块

### UsageMonitor 类

**位置:** `scripts/usage_monitor.py`

**核心功能:**

```python
from scripts.usage_monitor import UsageMonitor

# 创建监控器
monitor = UsageMonitor()

# 记录使用（自动在 CognitiveController 中调用）
monitor.log_usage(task, mode, result, context)

# 获取统计数据
stats = monitor.get_stats(days=7)  # 最近 7 天

# 生成报告
report = monitor.generate_report(days=7)

# 导出日志
export_file = monitor.export_logs()
```

---

## 📈 监控指标

### 1. 使用统计

| 指标 | 说明 |
|------|------|
| **总使用次数** | Skill 被使用的总次数 |
| **首次/最后使用** | 使用时间范围 |
| **平均置信度** | 所有使用的平均置信度 |
| **成功/失败次数** | 评分>=0.7 为成功 |

### 2. 模式分布

| 模式 | 指标 |
|------|------|
| **OOA** | 使用次数、占比 |
| **OODA** | 使用次数、占比 |
| **OOCA** | 使用次数、占比 |
| **OOHA** | 使用次数、占比 |

### 3. 模式效果对比

| 模式 | 指标 |
|------|------|
| **OOA** | 使用次数、平均评分 |
| **OODA** | 使用次数、平均评分 |
| **OOCA** | 使用次数、平均评分 |
| **OOHA** | 使用次数、平均评分 |

### 4. 任务类型分布

| 类型 | 说明 |
|------|------|
| **analysis** | 分析类任务 |
| **creative** | 创意类任务 |
| **research** | 研究类任务 |
| **simple** | 简单任务 |
| **other** | 其他 |

---

## 📋 使用方式

### 方式 1: 查看监控报告

```bash
cd skills/cognitive-flexibility
python monitor-usage.py
```

**输出示例:**
```
============================================================
Cognitive Flexibility Skill 使用监控
============================================================

1. 总体统计
----------------------------------------
总使用次数：100
首次使用：2026-04-05T13:30:00
最后使用：2026-04-05T13:50:00
平均置信度：0.75
成功次数：85
失败次数：15

2. 模式分布
----------------------------------------
OOA: 30 次 (30.0%) ██████
OODA: 50 次 (50.0%) ██████████
OOCA: 10 次 (10.0%) ██
OOHA: 10 次 (10.0%) ██

3. 模式效果对比
----------------------------------------
OOA: 使用 30 次，平均评分 0.82
OODA: 使用 50 次，平均评分 0.78
OOCA: 使用 10 次，平均评分 0.85
OOHA: 使用 10 次，平均评分 0.76

...
```

### 方式 2: 在代码中查看

```python
from scripts.usage_monitor import UsageMonitor

monitor = UsageMonitor()

# 获取总体统计
stats = monitor.get_stats()
print(f"总使用次数：{stats['total_uses']}")

# 获取最近 7 天统计
weekly_stats = monitor.get_stats(days=7)
print(f"本周使用：{weekly_stats['count']}次")

# 生成报告
report = monitor.generate_report(days=7)
print(report)

# 模式效果对比
mode_comp = monitor.get_mode_comparison()
for mode, data in mode_comp.items():
    print(f"{mode}: {data['count']}次，评分{data['avg_score']:.2f}")
```

### 方式 3: 导出日志分析

```python
# 导出详细日志
export_file = monitor.export_logs()
# 输出：logs/usage-export.json

# 分析导出的 JSON 文件
import json
with open(export_file, 'r') as f:
    logs = json.load(f)
    
# 自定义分析
for log in logs:
    print(f"{log['timestamp']}: {log['mode']} - {log['task']}")
```

---

## 📁 日志文件位置

```
skills/cognitive-flexibility/logs/
├── usage-log.jsonl      # 使用日志（每行一个 JSON）
├── usage-stats.json     # 聚合统计数据
└── usage-export.json    # 导出的完整日志（可选）
```

---

## 📊 报告示例

### 7 天使用报告

```
============================================================
Cognitive Flexibility Skill 使用报告（最近 7 天）
============================================================

总使用次数：100
成功率：85.0%
平均置信度：0.75
平均评分：0.80

模式分布:
  OOA: 30 次 (30.0%)
  OODA: 50 次 (50.0%)
  OOCA: 10 次 (10.0%)
  OOHA: 10 次 (10.0%)

模式效果对比:
  OOA: 使用 30 次，平均评分 0.82
  OODA: 使用 50 次，平均评分 0.78
  OOCA: 使用 10 次，平均评分 0.85
  OOHA: 使用 10 次，平均评分 0.76

============================================================
```

---

## 🔍 效果评估

### 评估指标

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| **成功率** | >90% | 70-90% | <70% |
| **平均置信度** | >0.8 | 0.6-0.8 | <0.6 |
| **平均评分** | >0.8 | 0.7-0.8 | <0.7 |

### 模式效果分析

**如果某模式评分持续偏低:**
1. 检查该模式的实现
2. 调整模式选择算法
3. 考虑是否需要该模式

**如果某模式使用频率过高:**
1. 检查模式选择是否合理
2. 考虑是否需要优化其他模式
3. 分析任务类型分布

---

## 📋 最佳实践

### 1. 定期检查

**建议频率:**
- 每日：查看使用次数
- 每周：生成使用报告
- 每月：深度分析效果

### 2. 数据驱动优化

**基于监控数据优化:**
- 调整 `confidence_threshold`
- 优化模式选择算法
- 改进低效模式

### 3. 导出备份

**定期导出日志:**
```python
monitor.export_logs('backup-20260405.json')
```

---

## 🎯 监控价值

**回答关键问题:**

1. **有没有用？** - 总使用次数、使用频率
2. **好不好用？** - 成功率、平均评分
3. **哪种模式好用？** - 模式效果对比
4. **用在什么场景？** - 任务类型分布
5. **如何改进？** - 基于数据优化

---

_道师出品 · Cognitive Flexibility Skill 监控指南 v2.1_

**创建时间:** 2026-04-05  
**下次更新:** 根据使用反馈持续优化
