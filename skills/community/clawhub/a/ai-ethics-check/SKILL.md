---
name: ai-ethics-check
description: |
  AI 科技伦理审查合规检查 — 基于《人工智能科技伦理审查与服务办法(试行)》（工信部等十部门，工信部联科〔2026〕75号，2026-03-20 施行），覆盖 10 项核心检查，快速评估合规状态并生成专业报告。

  本 skill 免费安装、免费使用。检查评分由「complianceHub 引擎」完成：
  首次使用前需在 compliancehub.cn 免费注册获取 API Key（网页注册后复制 Key，
  设置环境变量 COMPLIANCEHUB_API_KEY，或保存为 ~/.config/compliancehub/ai-ethics-check.key，权限 0600），
  每个 Key 含 100 次免费额度，无需付费。
  预览模式（--non-interactive / --non-interactive-json）完全离线，不读取 Key、不发起任何网络请求。

  评分时检查项实时从合规 Hub 云端规则库 API 拉取（单一数据源，后端更新即生效）；离线预览使用内置检查项，不发起任何网络请求。

  ⚠️ 本检查结果基于你提交的自报信息生成，非监管/审计结论，仅供参考，不构成法律意见。

  Use when: 用户显式要求运行 ai-ethics-check（如"运行 ai-ethics-check"、"做AI 科技伦理审查合规检查"）。
  普通对话中提及相关合规词不自动触发——本 skill 会向第三方云端发送答题内容，必须由用户按名显式调用。

  Trigger (explicit opt-in only)：ai-ethics-check, run ai-ethics-check, use ai-ethics-check skill, AI 科技伦理审查合规检查
  Pricing: Free skill; cloud scoring is free (anonymous trial 5 runs, then register for a free API Key with 100 calls)
  ⚠️ Cloud scoring sends your answers to compliancehub.cn; use --non-interactive for a fully offline preview. Without a Key the skill runs an anonymous trial (up to 5 scored runs) using a local random anon_id; registering gives a free Key with 100 calls.
  🔐 Account & free API Key are created on the website (compliancehub.cn) — not in the terminal.
  Open https://compliancehub.cn/account.html?skill=ai-ethics-check to register and get a Key instantly, then
  provide it via env `COMPLIANCEHUB_API_KEY` or save to ~/.config/compliancehub/ai-ethics-check.key (mode 0600).
  💡 Free preview: --non-interactive lists the 10 items without a Key
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔍 AI 科技伦理审查合规检查 — Free 检查 (Cloud-Scored)

## Overview
AI 科技伦理审查合规检查 is a **free** 检查 based on 《人工智能科技伦理审查与服务办法(试行)》（工信部等十部门，工信部联科〔2026〕75号，2026-03-20 施行）. It covers 10 core items. Scoring runs on the complianceHub engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* 检查, your responses are
> transmitted to the complianceHub cloud at `compliancehub.cn` for scoring. Run `--non-interactive` for a fully
> **offline** preview that never contacts the cloud.

- The skill is free to install.
- During a scored run, check items are served from the cloud rule library (always current); the offline preview uses the built-in items and never contacts the cloud.
- Scoring + quota are computed in the cloud; you get a professional report locally.
- Scoring: no Key? The anonymous trial (5 real cloud-scored runs) runs automatically. Register for a free API Key (100 calls) to keep going.

## What it checks (10 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | 设立科技伦理委员会 | 办法§9 |
| 2 | 委员会独立履职 | 办法§9 |
| 3 | 活动前申请伦理审查 | 办法§12 |
| 4 | 审查决定时限合规 | 办法§16 |
| 5 | 审查重点：公平公正 | 办法§15 |
| 6 | 审查重点：可控可信可解释 | 办法§15 |
| 7 | 人机融合系统专家复核 | 办法§21-25+附件 |
| 8 | 舆论动员算法专家复核 | 办法附件 |
| 9 | 高风险自动化决策专家复核 | 办法附件 |
| 10 | 登记与跟踪审查 | 办法§19/§30 |

## Usage
### Free preview (no Key)
```bash
python3 scripts/ai-ethics-check.py --non-interactive
```
### Anonymous trial (no Key)
Just run the full 检查 — without a Key the skill issues a local random anon_id and scores in the cloud
(5 free runs / 7-day window). When the trial runs out it prints the one-click registration page,
carrying your anon_id so the trial progress carries over after registering.

### Get a free API Key
Open https://compliancehub.cn/account.html?skill=ai-ethics-check in your browser to register and get a free Key instantly.
Then provide it to the skill via env or key file:
```bash
export COMPLIANCEHUB_API_KEY=<your-key>
# or save to ~/.config/compliancehub/ai-ethics-check.key (mode 0600)
```

### Full 检查 + report
```bash
python3 scripts/ai-ethics-check.py --format html -o ai-ethics-check-report.html
```

## Agent guide
When a user asks for a AI 科技伦理审查合规检查:
1. Run `--non-interactive` to preview the 10 items (no Key needed).
2. Run the full 检查. Without a Key it automatically uses the anonymous trial (5 real cloud-scored runs) — the user gets the complete report immediately.

## Security & data handling
- **No account in the terminal:** Account creation and free API Key issuance happen on the website (compliancehub.cn).
- **Where data goes:** Check items are fetched from, and your answers are scored by, the complianceHub cloud at `https://compliancehub.cn`.
- **API Key storage:** provided via env `COMPLIANCEHUB_API_KEY`, or saved to `~/.config/compliancehub/ai-ethics-check.key` (0600), outside the skill folder.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Preview without cloud:** `--non-interactive` never contacts the cloud.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.
（本工具仅供一般合规参考，不构成法律意见；涉及具体案件请咨询有资质的律师。）

## License
MIT.
