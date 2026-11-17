# Adaptive ETA — Give Your AI a Sense of Time

**[English]**

AI agents can't feel time passing between tool calls, so they go silent during long tasks. `adaptive-eta` gives them a real clock: promise an ETA, correct it honestly when it slips, ask before running far over — and learn from past estimates so the next one is closer.

# 自适应预估时间 — 让你的 AI 拥有「时间感」

**[中文]**

AI 在两次工具调用之间感知不到时间流逝，所以长任务时常常一声不吭。`adaptive-eta` 给它一只真正的表：先许下预估时间，超时诚实更新，严重超时先征求你的意见——并且从历史偏差中学习，下一次预估更准。

## What it does / 功能

| | EN | 中文 |
|---|---|---|
| Tiered | Only tasks > ~2 min get the full protocol; quick tasks stay quiet | 只有 >2 分钟的任务走完整流程，短任务不打扰 |
| Honest updates | Re-estimates at 80% and at expiry, naming the cause | 用到 80% 和到期时重新预估，并说明原因 |
| Circuit breaker | Past 3× the original estimate → asks before continuing | 超过最初预估 3 倍 → 先问你是否继续 |
| Learns | Logs estimate vs. actual; suggests a correction factor | 记录预估与实际，自动给出校准系数 |
| Low overhead | Checks at step boundaries, not around every tool call | 只在步骤切换时检查，不在每次工具调用前后打卡 |

## Example / 效果

> **You:** Refactor the auth module and update the tests.
>
> **AI:** About 6 minutes: read 9 files (~1 min), refactor (~3 min), fix and run tests (~2 min).
>
> **AI:** Slower than planned — two tests depend on the old token format. About 4 more minutes.
>
> **AI:** Done. … *Estimated 6m · actual 9m40s · 1 revision*

## Installation / 安装

```bash
clawhub install Yanghe1941/adaptive-eta
```

Requires Python 3.8+ (stdlib only). Timer state and history live in `~/.adaptive-eta/` (override with `ADAPTIVE_ETA_HOME`).
需要 Python 3.8+（仅标准库）。计时状态和历史存放在 `~/.adaptive-eta/`。

## Changelog / 更新记录

**0.3.0**
- Fix: the 3× rule now works — `revise` keeps the original estimate (before, re-running `start` erased it). / 修复：3 倍熔断此前因 `start` 覆盖初始预估而失效，新增 `revise`。
- New: history + `calibrate`; `start` suggests a corrected ETA once there are 3+ past tasks. / 新增历史记录与自动校准。
- Changed: threshold from 15s to ~2 min; checks only at step boundaries. / 触发阈值从 15 秒调到约 2 分钟；只在步骤切换时检查。
- Changed: state moved out of the skill directory; stale timers auto-expire; `--task` for parallel timers. / 状态移出技能目录，残留计时器自动过期，支持并行计时。
- Removed: personal names and the nonexistent "cron reminder" from the description. / 移除私人称呼和不存在的「cron 提醒」描述。
