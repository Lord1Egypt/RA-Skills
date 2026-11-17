---
name: capability-decay-watchdog
version: 1.0.0
description: |
  能力退化预警与自愈：监测技能生态运行时健康，扫描各技能 learned_patterns.json，检测成功率
  滑落（跌破阈值）与陈旧停滞（长期无操作），输出告警 + 推荐自愈动作（重注入 learner /
  标 repair 缺口 / 重跑回归）。让元进化引擎在"能力悄悄变弱前"主动干预——一线大模型完全
  不具备的元治理能力，是"超越之后能否稳定存续"的关键保障。
agent_created: true
visibility: public
---

# capability-decay-watchdog（能力退化预警与自愈）

> 「自主能力治理与生态(下一阶梯)」域 Top3（权重 1.44）：让全栈超级智能体**能自愈**，
> 在能力退化前预警并触发修复，而非等出了错才修。

## 何时使用
- 元进化引擎定期巡检：把 `decayed` 列表自动转为 `repair`/`evolve` 缺口。
- 发布后回归门禁：新版本上线后若成功率滑落，立即告警回滚/修复。
- 长程运行守护：防止"构建时很能打、跑久了悄悄变弱"。

## 核心 API（scripts/capability_decay_watchdog.py）
- `success_rate(data)` / `last_op_age_days(data)`：单技能指标。
- `check_skill(skill_dir)` → 告警列表：success_rate_drop(critical) / stale(warn) / no_learner(info)。
- `watch(skills_root)` → 全生态报告 `{decayed, healthy, decayed_count}`。
- `python capability_decay_watchdog.py --selftest`：内置断言（健康/退化/陈旧 三样本）。

## 设计要点
- **阈值可调**：SUCCESS_FLOOR=0.7 / MIN_OPS=5 / STALE_DAYS=30，避免早期噪声与误报。
- **动作可编排**：每条告警带 `action`（repair_or_reinject / rerun_regression / inject_learner），
  元进化引擎可直接消费转为缺口。
- **零依赖**：纯标准库。

## 与元进化闭环的关系
作为 meta-evolver 的"健康哨兵"：sense/record 之后跑本技能，把退化技能自动登记为
`repair` 缺口，形成"构建→运行→退化预警→自愈"的可持续闭环。

## 自进化学习系统
本技能接入 meta-evolver 自进化闭环：每次巡检经 learner 记录退化模式，跨会话沉淀
"哪些域易退化/多久需回归"等经验。

## 已知限制
- 仅基于 learned_patterns 的运行统计，不反映"逻辑是否仍正确"（需结合 redteam-selfattack）。
- 成功率统计依赖技能正确调用 learner.record，未接入的技能无法监测。
