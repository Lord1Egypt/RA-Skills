# Report Templates

## A. Daily Report Structure

```markdown
# 《{game_name} 舆情监测日报｜{date} {time}》

## 摘要看板
- 📊 整体情绪：正面 X% / 中性 X% / 负面 X%
- 🔴 问题分布：P1 × N / P2 × N / P3 × N
- 🏪 商店评分变化：{if applicable}
- 📋 本期最重要结论：
  1. {conclusion 1}
  2. {conclusion 2}
  3. {conclusion 3}
- 覆盖渠道：{N} 个 | 有效样本：{N} 条
- ⚠️ 未成功采集渠道：{list if any}

## 时间维度

| 渠道 | 目标窗口 | 实际可得窗口 | 时间可信度 |
|------|---------|------------|-----------|
| {channel} | {e.g. 最近24h} | {e.g. 4/4 当天} | {高/中/低} |

说明：
- 高：有精确时间戳，窗口可控
- 中：有相对时间或近似范围
- 低：无法限制时间，可能包含过期内容

## 采样策略
- **报告类型**：{定向风险扫描 / 全局舆情扫描 / 渠道专项扫描 / 事件专项扫描}
- **搜索关键词**：{list}
- **偏差说明**：{sampling bias description}

## 核心问题责任看板

### [{P级}] {问题标题}
- **issue_type**：{账号安全 / 封禁争议 / 新手体验 / 外挂生态 / 版本预期 / 平衡性 / 付费争议 / 技术故障 / 运营沟通 / ...}
- **cause_category**：{安全 / 客服 / 匹配机制 / 反作弊 / 宣发运营 / 设计 / 技术 / ...}
- **严重度**：{P1/P2/P3} | **置信度**：{高/中/低}
- **传播程度**：{isolated/single-platform-hot/multi-platform/mainstream}
- **证据统计**：
  - 玩家 L1 样本：{N} 条（去重后）
  - 媒体 L1 支撑：{N} 条
  - 官方响应状态：{无 / 有回应 / 有明确措施}
  - L2 辅助证据：{N} 条
- **渠道覆盖**：{platforms} ({N} 个渠道)
- **建议人工复核**：{是/否}（{原因}）
- **玩家原帖证据（L1）**：
  > "{quote 1}" — {source, time, engagement}
  > "{quote 2}" — {source, time, engagement}
- **媒体报道证据（L1）**：
  > "{summary}" — {source, date}
- **官方公告/回应**：
  > "{summary}" — {source, date}
- **影响判断**：{impact assessment}
- **建议 Owner**：{team}
- **建议动作**：{action}
- **是否需即时响应**：{yes/no}
- **来源链接**：{urls}

{repeat for each issue, P1 first, then P2, then P3}

## 各渠道详情

### {channel_name}
- **情绪倾向**：{sentiment}
- **热门议题**：{topics}
- **本期主要问题**：{issues}
- **代表性评论**：
  > "{quote}" — {source}
- **评分变化**：{if applicable}

{repeat for each channel}

## 本期观察
- ⚠️ 本期新增高风险议题：{list}
- 📡 本期重点扩散平台：{platforms}
- ✅ 本期正面亮点：{list}
- 👀 本期待观察议题：{list}
- 📰 KOL/媒体动向：{list}
- 🆚 竞品提及：{if configured}

## 行动建议清单

### 🔴 需要立即响应
- {action items}

### 🟡 需要持续观察
- {action items}

### ⚪ 暂不处理
- {action items}
```

## B. Low-Sample Observation Report

When valid samples are insufficient for confident analysis:

```markdown
# 《{game_name} 舆情观察报告（低样本）｜{date} {time}》

> ⚠️ 本期有效样本不足，以下为观察性摘要，不作为高置信度判断依据。

## 采集概况
- 成功采集渠道：{list}
- 未成功采集渠道：{list with reasons}
- 有效样本总量：{N} 条

## 已采集反馈摘要
{brief summary of what was found, organized by channel}

## 代表性评论
> "{quote}" — {source}
{3-5 representative quotes if available}

## 建议
- {e.g., broaden keywords, adjust channels, retry failed channels, switch to manual scan}
```

## C. P1 Instant Alert

Sent immediately via Feishu when P1 is detected. Keep short — this is for speed, not completeness.

```markdown
🚨 **P1 舆情告警 | {game_name}**

**风险**：{issue title}
**严重度**：P1
**涉及平台**：{platforms}
**主要议题**：{brief description}

**代表样本**：
> "{quote}" — {source}

**建议动作**：{action}
**详细报告**：{path to full report}
```

## D. Feishu Summary (Daily)

Condensed version for Feishu message delivery. Keep under 500 chars if possible.

```markdown
📊 **{game_name} 舆情日报 | {date}**

情绪：正面{X}% 中性{X}% 负面{X}%
问题：🔴P1×{N} 🟡P2×{N} ⚪P3×{N}

**Top 问题：**
1. [{P级}] {issue title} → {suggested action}
2. [{P级}] {issue title} → {suggested action}
3. [{P级}] {issue title} → {suggested action}

完整报告：{path}
```
