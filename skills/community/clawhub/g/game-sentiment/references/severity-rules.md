# Severity Rules

## Severity Levels (Rubric)

判级必须基于以下量化门槛，不允许仅凭直觉判定。

### P1 — Critical
需同时满足以下条件：
1. **证据门槛**：至少 3 条独立 L1 证据（去重后）
2. **渠道覆盖**：至少 2 个渠道出现同类信号，或已有官方公告/媒体放大
3. **影响性质**（满足任一）：
   - 账号安全、财产损失、误封等高风险问题
   - 大面积服务异常（登录/支付/崩溃）
   - 对版本节点、品牌信任、商业转化有直接影响
   - KOL/媒体放大效应

### P2 — Important
需同时满足以下条件：
1. **证据门槛**：至少 2 条独立 L1 证据，或 1 条 L1 + 多条 L2 交叉印证
2. **影响性质**（满足任一）：
   - 玩家集中抱怨，有明确体验痛点
   - 未达平台级危机，但影响特定人群/模式
   - 官方暂无强回应
3. 不满足 P1 渠道覆盖或证据数量门槛

### P3 — Routine / Observation
- 信息性议题、正向预期、弱信号
- 证据不足以判定为 P2+
- 单渠道散点反馈、个体体验问题
- 进入观察池

### 降级规则
- 若某议题 L1 证据不足但有 L2 支撑 → 最高判 P2，并标注"证据待补强"
- 若仅有 L2 证据 → 最高判 P3，标注"背景性观察项"

## Sample Dedup Rules

采集后必须执行去重，报告中必须同时展示原始样本数和去重后样本数。

1. **同账号合并**：同一账号在同一渠道、同一主题的多条内容按 1 个独立样本计
2. **高相似文本去重**：高度重复的维权模板/申诉模板只保留代表性 1 条，标注"另有 N 条相似内容"
3. **转发/搬运排除**：转发、搬运、截图引用不计入原创玩家样本
4. **媒体与玩家分计**：媒体报道和玩家原帖分开统计，不混为同一类证据

## Report Types

每份报告必须在开头明确标注类型：

| 类型 | 说明 |
|------|------|
| **定向风险扫描** | 围绕特定关键词/事件的深挖扫描，不代表全局画像 |
| **全局舆情扫描** | 多维度、多关键词覆盖的全景扫描 |
| **渠道专项扫描** | 针对特定渠道的深度采集 |
| **事件专项扫描** | 针对特定事件的追踪报告 |

## Credibility Assessment

Each high-priority issue gets a credibility rating:

| Level | Criteria |
|-------|----------|
| **High** | Appears independently on 3+ channels; has high-engagement original posts; quotable first-hand player statements; amplified by media/KOL; aligns with version/event timeline |
| **Medium** | Appears on 2 channels; some engagement; player quotes available but limited; timeline alignment unclear |
| **Low** | Single channel only; low engagement; no direct quotes; could be isolated complaint |

## Sensitive Wording Rules

For these high-sensitivity labels:
- 暗改 (secret nerf) → "玩家反馈数值调整 / 玩家质疑数值变动"
- 欺诈 (fraud) → "玩家质疑宣传与实际不符"
- 误封 (wrongful ban) → "玩家反馈账号异常封禁"
- 公平性破坏 → "玩家集中反馈公平性问题"

**Principle**: Default to "player feedback / player concerns / concentrated reports" phrasing. Never state as verified fact.

## Responsibility Mapping

| Issue Type | Suggested Owner |
|------------|----------------|
| Technical incident (crash, lag, payment) | Dev / QA |
| Balance / numerical dispute | Design / Product |
| Monetization dispute | Design / Product / Ops |
| Content / aesthetic dispute | Design / Art |
| Event rules / threshold | Design / Ops |
| Operations communication | Ops / Community |
| Marketing expectation gap | Marketing / PR |

## Action Mapping

| Situation | Suggested Action |
|-----------|-----------------|
| Confirmed technical issue | Immediate check → fix → announce |
| Unconfirmed but spreading | Add to Known Issues → monitor → prepare statement |
| Design dispute (balance/value) | Evaluate → communicate rationale or adjust |
| Monetization backlash | Evaluate compensation → adjust parameters → communicate |
| Content/aesthetic negative | Monitor → evaluate if adjustment needed |
| Ops communication gap | Post clarification → improve future communication |
| Marketing expectation gap | Revise promotional copy → align future messaging |
| Isolated complaints | Monitor only |
