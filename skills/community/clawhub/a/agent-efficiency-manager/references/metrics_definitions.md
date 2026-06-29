# 效率指标定义

本文档定义 Agent 效率分析中的各项指标及其计算方法。

---

## 核心指标

### 1. skill_count（技能数量）

**定义：** Agent 配置的技能总数。

**影响：** 每个技能都会注入 system prompt，直接影响 token 消耗。

**基准：**
- ✅ 优秀：≤ 10 个
- ⚠️ 一般：11-20 个
- ❌ 较差：> 20 个

---

### 2. estimated_tokens（预估 token 消耗）

**定义：** 单次对话的预估 token 消耗量（仅计算 skills 注入部分）。

**计算方法：**
```
estimated_tokens = Σ (skill 的 SKILL.md token 数)
```

**经验值：**
- 简单 skill（如 `qclaw-text-file`）：~500 tokens
- 中等 skill（如 `docx`、`pdf`）：~800 tokens
- 复杂 skill（如 `online-search`、`xbrowser`）：~1000+ tokens

**基准：**
- ✅ 优秀：≤ 5,000 tokens
- ⚠️ 一般：5,000-10,000 tokens
- ❌ 较差：> 10,000 tokens

---

### 3. efficiency_score（效率评分）

**定义：** 综合评分（0-100），衡量 Agent 配置的效率。

**计算公式：**
```
efficiency_score = base_score - redundancy_penalty
```

**基准分（base_score）：**
- skill_count ≤ 10：50 分
- 11 ≤ skill_count ≤ 20：30 分
- skill_count > 20：10 分

**冗余扣分（redundancy_penalty）：**
- 存在重复技能：`-20 分`
- `another_them` 和 `another-them` 同时存在：`-15 分`
- 包含 `qclaw-migration`（一次性工具）：`-10 分`

**基准：**
- ✅ 优秀：≥ 70 分
- ⚠️ 一般：40-69 分
- ❌ 较差：< 40 分

---

### 4. redundancy_count（冗余技能数量）

**定义：** Agent 配置中冗余、重复或无关的技能数量。

**冗余类型：**
1. **完全重复**：同一技能出现多次（如 `another_them` 出现 2 次）
2. **命名重复**：功能相同的不同命名（如 `another_them` vs `another-them`）
3. **跨领域无关**：股票 Agent 配置了房产技能
4. **一次性工具**：非常驻工具（如 `qclaw-migration`）

**计算方法：**
```python
redundancy_count = (
    len(skills) - len(set(skills)) +  # 完全重复
    check_naming_conflicts(skills) +    # 命名重复
    check_cross_domain(skills, agent_role) +  # 跨领域
    check_one_time_tools(skills)         # 一次性工具
)
```

---

## 衍生指标

### 5. token_savings（Token 节省量）

**定义：** 优化后预计节省的 token 数量。

**计算方法：**
```
token_savings = estimated_tokens_before - estimated_tokens_after
```

---

### 6. optimization_priority（优化优先级）

**定义：** 推荐优先优化的 Agent 排序。

**计算方法：**
```python
priority_score = (
    (100 - efficiency_score) * 0.5 +  # 效率评分越低越优先
    skill_count * 10 +                  # 技能越多越优先
    redundancy_count * 20                # 冗余越多越优先
)
```

**排序：** 按 `priority_score` 降序排列。

---

## 趋势指标

### 7. efficiency_trend（效率趋势）

**定义：** 一段时间内效率评分的变化趋势。

**计算方法：**
```python
efficiency_trend = (
    "improving"   if score_change > +5 else
    "declining"    if score_change < -5 else
    "stable"
)
```

---

### 8. token_trend（Token 消耗趋势）

**定义：** 一段时间内 token 消耗的变化趋势。

**计算方法：**
```python
token_change_percent = (latest_tokens - previous_tokens) / previous_tokens * 100

token_trend = (
    "increasing"  if token_change_percent > +5% else
    "decreasing"  if token_change_percent < -5% else
    "stable"
)
```

---

## 使用示例

### 查询某个 Agent 的指标

```python
from analyze_agent_efficiency import analyze_agent_efficiency

result = analyze_agent_efficiency(config_path, output_path)

# 找到特定 Agent
agent_metrics = [r for r in result["agents"] if r["agent_id"] == "stock"][0]

print(f"效率评分：{agent_metrics['efficiency_score']}/100")
print(f"预估 Token 消耗：{agent_metrics['estimated_tokens']}")
```

---

### 批量对比 Agent 效率

```python
import json

with open("efficiency_report.json", "r") as f:
    report = json.load(f)

# 按效率评分排序
sorted_agents = sorted(report["agents"], key=lambda x: x["efficiency_score"])

print("Agent 效率排名（从低到高）：")
for agent in sorted_agents:
    print(f"  {agent['agent_name']}：{agent['efficiency_score']}/100")
```

---

## 注意事项

1. **预估偏差**：`estimated_tokens` 是经验估值，实际消耗取决于模型和处理内容
2. **动态更新**：指标应定期重新计算（建议每周一次）
3. **角色相关**：跨领域判断需要准确的 Agent 角色识别
4. **趋势需要历史数据**：首次运行无法计算趋势，需要积累至少 2 次历史记录

---

**最后更新：** 2026-05-29
