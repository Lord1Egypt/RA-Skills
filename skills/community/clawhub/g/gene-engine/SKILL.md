---
name: gene-engine
description: Gene系统自动化引擎 — Agent行为规则的退役检查、冷却期管理、主动探测、健康评分。让Agent的规则系统从「人驱动」变成「代码驱动」。
version: 1.0.0
---

# Gene Engine

Agent的行为规则（Gene）会随着时间退化：该触发的不触发，该退役的不退役，该验证的不验证。Gene Engine 自动化管理整个生命周期。

## 功能

- **退役检查**：从未触发>30天 → 标记候选，连续3次触发未改变判断 → 候选，连续5次 → 自动归档
- **冷却期**：连续失败3次 → cooldown，72h后自动恢复
- **主动探测**：超过阈值未触发 → 输出警告
- **验证间隔**：按规则分类自动检查（data=7d, cognitive=30d, principle=90d）
- **唤醒率**：activationCount / triggeredCount，自动计算
- **健康分数**：0-100分，A/B/C/D等级
- **指标日志**：每次运行记录到 gene-metrics.log
- **JSON摘要**：机器可读输出，供心跳流程解析
- **自动提醒**：有警告时生成提醒文案

## 安装

```bash
clawhub install gene-engine
```

## 使用

### 主引擎（心跳时调用）

```bash
bash ~/.openclaw/workspace/scripts/gene-engine.sh
```

### 记录触发结果

```bash
bash ~/.openclaw/workspace/scripts/gene-trigger.sh <gene_key> <success|fail> <outcome描述>

# 示例
bash scripts/gene-trigger.sh gene24 success "三层验证通过"
bash scripts/gene-trigger.sh gene26 fail "学到但没有行为改变"
```

### 输出示例

```
=== Gene系统状态报告 ===
heartbeat_sampling        verified    3次  1.0   13d
three_layer_verification  active      0次  N/A   0d
learning_application_check verified   1次  1.0   0d

🟢 健康分数: 100/100 (等级: A)
```

## 配置

在 `memory/gene-state.json` 中定义Gene规则。每条Gene需要：

```json
{
  "gene_key": {
    "status": "active|verified|pending_verification|cooldown|disabled|archived|internalized",
    "triggeredCount": 0,
    "lastTriggered": null,
    "consecutiveFailures": 0,
    "totalFailures": 0,
    "category": "data|cognitive|principle",
    "triggerCondition": {
      "signal": "可观察信号",
      "context": "上下文条件",
      "exclusion": "边界排除"
    },
    "creationDate": "ISO时间戳"
  }
}
```

## Gene生命周期

```
active → verified → internalized（最高荣誉：规则变成了行为习惯）
active → cooldown → active（冷却期后恢复）
active → disabled → archived（总失败10次禁用）
active → archived（退役）
```

## 文件结构

```
scripts/
├── gene-engine.sh    # 主引擎（12个模块）
├── gene-trigger.sh   # 触发记录器
memory/
├── gene-state.json   # 状态文件
├── gene-metrics.log  # 指标日志
```

## 来源

基于 InStreet 社区的实战经验改造，包含 @ivan_agent（触发条件三要素）、@Void（激活阈值分层）、@ljj_xiaor（唤醒率追踪）、@summer_golden_706036（退役信号）等社区贡献。

#Gene系统 #Agent进化 #自动化
