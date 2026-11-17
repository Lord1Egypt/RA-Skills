---
name: ccpa-audit
description: |
  CCPA Compliance Audit — California Consumer Privacy Act (CCPA, Cal. Civ. Code §1798.100 et seq.) & CPRA amendment.

  Free compliance audit skill covering 20 core CCPA/CPRA items. Scoring runs on the
  CQDev cloud compliance engine at compliancehub.cn (free API Key with 100 calls; an
  anonymous trial gives 5 real cloud-scored runs per 7-day window). Bilingual (中文/English).

  Activated when the user explicitly invokes it by name (e.g. "run ccpa-audit").
  Scored runs transmit the user's answers to compliancehub.cn; the --non-interactive
  preview fetches check items from the cloud but sends no answers.
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 CCPA Compliance Audit (CCPA 合规深度审计) — Free, Cloud-Scored

## Overview
CCPA 合规深度审计 is a **free** 审计 based on 加州消费者隐私法案（CCPA）及 CPRA 修正案.
It covers 20 core items. Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine.** When you run a *scored* 审计, your responses are
> transmitted to the CQDev cloud at `compliancehub.cn` for scoring. The free `--non-interactive` preview
> fetches the latest check items from the cloud rule library but transmits NO answers; it falls back to the
> bundled item set if the network is unavailable.

- The skill is free to install.
- Check items are served from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- A free API Key (100 calls) is required for scoring. Get one in seconds at the web account center.

## What it checks (24 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | 知情权 | CCPA §1798.100 |
| 2 | 删除权 | CCPA §1798.105 |
| 3 | 选择退出权 | CCPA §1798.120 |
| 4 | 非歧视原则 | CCPA §1798.125 |
| 5 | 更正权 | CPRA §1798.106 |
| 6 | 请求验证 | CCPA §1798.145(i) |
| 7 | 授权代理人 | CCPA §1798.130(a)(2) |
| 8 | 收集通知 | CCPA §1798.100(b) |
| 9 | 个人信息类别 | CCPA §1798.140 |
| 10 | 隐私政策 | CCPA §1798.130 |
| 11 | 年度披露 | CCPA §1798.130(a)(5) |
| 12 | 数据最小化 | CPRA §1798.100(b) |
| 13 | 敏感个人信息(CPRA) | CPRA §1798.140(ae) |
| 14 | 限制敏感PI使用 | CPRA §1798.121 |
| 15 | 留存期限 | CPRA §1798.100(a)(3) |
| 16 | 服务提供商义务 | CCPA §1798.140(ag) |
| 17 | 第三方共享 | CCPA §1798.115 |
| 18 | 合同审计权 | CCPA §1798.140(ag)(3) |
| 19 | 自动化决策 | CPRA §1798.185(a)(16) |
| 24 | 未成年人数据 | CCPA §1798.120(c) |
| 21 | 暗模式/选择对称性 | CCPA §1798.140(ad) |
| 22 | 员工/求职者数据 | CCPA §1798.100 (HR context) |
| 23 | 安全义务 | CCPA §1798.150(a)(1) |
| 24 | 高风险评估/网络安全审计（前瞻） | CPPA 2025 Rules (Risk Assessments / Cyber Audits) |

## Usage
> 💡 交互提示：逐项作答时可直接输入中文（是 / 否 / 不适用），输入 `?` 可查看该项的合规建议

### Free preview (no Key)
```bash
python3 scripts/ccpa-audit.py --non-interactive
```
### Get a free API Key (web, then hand it to this skill)
1. Open the account center and register (human check is browser-only):
   https://compliancehub.cn/account.html?skill=ccpa-audit
2. Copy the Key, then give it to this skill (pick one):
```bash
export COMPLIANCEHUB_API_KEY=<网页显示的 Key>
```
或用编辑器手动创建密钥文件 `~/.config/compliancehub/ccpa-audit.key`（权限 600）并粘贴 Key。

### Full 审计 + report
```bash
python3 scripts/ccpa-audit.py --format html -o ccpa-audit-report.html
```

## Agent guide
When a user asks for a CCPA 合规深度审计:
1. Run `--non-interactive` to preview the 24 items (no Key needed).
2. If the user wants a scored report, point them to the web account center to get a free Key, then run the full 审计 (the Key is read from COMPLIANCEHUB_API_KEY or ~/.config/compliancehub/ccpa-audit.key).

## Security & data handling
- **No account creation / no credentials collected:** This skill never prompts for or transmits your email/password,
  and it never registers accounts. In preview mode (`--non-interactive`) it only reads the public rule library and
  sends NO answers; nothing about your compliance status persists across sessions.
- **Where data goes:** Check items are fetched from, and your answers are scored by, the CQDev cloud at
  `https://compliancehub.cn` (the operator's official endpoint). Scoring transmits only your item answers and the free API Key (as a Bearer token).
- **API Key (you provide it):** obtained from the web account center and supplied via the
  `COMPLIANCEHUB_API_KEY` environment variable or `~/.config/compliancehub/ccpa-audit.key` (0600, outside the skill
  folder). The skill reads the Key; it does not write accounts or collect credentials.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Not a rogue/autonomous agent:** The stored files are an ordinary API key file (0600) and a random
  anonymous-trial anon_id (`~/.config/compliancehub/ccpa-audit.anon_id`, 0600, no personal data) — not
  auto-start, session, or background processes. No compliance answers are stored locally.
- **Preview mode:** `--non-interactive` fetches the public check items from the cloud rule library but
  sends NO answers; it falls back to the bundled item set if the network is unavailable.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.

## License
MIT.
