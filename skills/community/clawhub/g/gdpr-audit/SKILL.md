---
name: gdpr-audit
description: |
  GDPR Compliance Audit — General Data Protection Regulation (EU) 2016/679 (GDPR).

  Free to install; scoring runs on the CQDev cloud compliance engine
  (free API Key, 100 free calls). Covers 25 core items.
  Use when: the user asks to run the gdpr-audit skill, or requests a
  GDPR 合规深度审计 / General Data Protection Regulation (EU) 2016/679 (GDPR).
  Trigger: gdpr-audit, GDPR 合规审计, 欧盟隐私审计, GDPR audit, 数据保护审计
  Pricing: Free skill; cloud scoring uses points (Check 1 / Audit 10 per run) from compliancehub.cn
  Anonymous trial: no Key? The skill auto-runs up to 5 real cloud-scored trials (7-day window) with a local anon_id, then points you to one-click registration carrying your anon_id.
  ⚠️ Cloud scoring sends your answers to compliancehub.cn. `--non-interactive` preview lists the items WITHOUT sending answers; it attempts to fetch the latest rule set from the cloud rule library and falls back to a built-in snapshot when offline.
  🔐 Account provisioning is OPT-IN via the web: register for a free API Key at
  https://compliancehub.cn/account.html?skill=gdpr-audit, then supply it to this skill via the
  COMPLIANCEHUB_API_KEY environment variable or ~/.config/compliancehub/gdpr-audit.key. This skill never collects your email/password.

  💡 Free preview: --non-interactive lists the 25 items without a Key
permissions:
  network:
    - "https://compliancehub.cn"
  filesystem:
    write:
      - "~/.config/compliancehub"
  env:
    - "COMPLIANCEHUB_API_KEY"
---

# 🔒 GDPR 合规深度审计 — Free 审计 (Cloud-Scored)

## Overview
GDPR 合规深度审计 is a **free** 审计 based on 欧盟《通用数据保护条例》（GDPR, Regulation (EU) 2016/679）.
It covers 25 core items. Scoring runs on the CQDev cloud compliance engine.

## How it works (free + cloud)
> ⚠️ **Your answers leave this machine — but only when scored.** When you run a *scored* 审计, your responses are
> transmitted to the CQDev cloud at `compliancehub.cn` for scoring. In `--non-interactive` preview mode your answers are NOT sent;
> the preview attempts to fetch the latest rule set from the cloud rule library and falls back to a built-in snapshot if it cannot reach the cloud.

- The skill is free to install.
- Check items are served from the cloud rule library (always current).
- Scoring + quota are computed in the cloud; you get a professional report locally.
- A free API Key (100 calls) is required for scoring. Register in seconds.

## What it checks (25 items)
| # | Check | Authority |
|---|-------|-----------|
| 1 | 适用范围 | Art. 3 |
| 2 | 处理原则 | Art. 5 |
| 3 | 合法依据 | Art. 6 |
| 4 | 同意 | Art. 7 |
| 5 | 特殊类别数据 | Art. 9 |
| 6 | 透明告知 | Art. 12 |
| 7 | 收集时信息 | Art. 13-14 |
| 8 | 访问权 | Art. 15 |
| 9 | 更正权 | Art. 16 |
| 10 | 删除权 | Art. 17 |
| 11 | 限制处理权 | Art. 18 |
| 12 | 可携权 | Art. 20 |
| 13 | 反对权 | Art. 21 |
| 14 | 自动决策 | Art. 22 |
| 15 | 问责 | Art. 24 |
| 16 | 设计与默认保护 | Art. 25 |
| 17 | 处理者管理 | Art. 28 |
| 18 | 处理活动记录 | Art. 30 |
| 19 | 处理安全 | Art. 32 |
| 20 | 向监管通报违约 | Art. 33 |
| 21 | 向数据主体通报 | Art. 34 |
| 22 | 数据保护影响评估 | Art. 35 |
| 23 | 事前协商 | Art. 36 |
| 24 | 数据保护官 | Art. 37-39 |
| 25 | 国际传输 | Art. 44-49 |

## Usage
> 💡 交互提示：逐项作答时可直接输入中文（是 / 否 / 不适用），输入 `?` 可查看该项的合规建议；
> 作答进度自动存为草稿，中断后重新运行会提示「继续 / 重新开始」。

### Free preview (no Key)
```bash
python3 scripts/gdpr-audit.py --non-interactive
```
### Get a free API Key
```bash
# 1) Open the account center, register, and copy your free Key:
open https://compliancehub.cn/account.html?skill=gdpr-audit
# 2) Hand the Key to this skill (pick one):
export COMPLIANCEHUB_API_KEY=<网页显示的 Key>
# or persist it to a key file (mode 0600, outside the skill folder):
mkdir -p ~/.config/compliancehub && echo '<网页显示的 Key>' > ~/.config/compliancehub/gdpr-audit.key
```

### Full 审计 + report
```bash
python3 scripts/gdpr-audit.py --format html -o gdpr-audit-report.html
```

## Agent guide
When a user asks for a GDPR 合规深度审计:
1. Run `--non-interactive` to preview the 25 items (no Key needed).
2. If the user wants a scored report, prompt them to get a free Key at the account page (https://compliancehub.cn/account.html?skill=gdpr-audit) and supply it via COMPLIANCEHUB_API_KEY or the key file, then run the full 审计.

## Security & data handling
- **No account credentials collected:** This skill never prompts for or transmits your email/password. The free API Key is obtained from the web account center (https://compliancehub.cn/account.html?skill=gdpr-audit) and supplied to the skill via COMPLIANCEHUB_API_KEY or ~/.config/compliancehub/gdpr-audit.key.
- **Where data goes:** Check items are fetched from, and your answers are scored by, the CQDev cloud at
  `https://compliancehub.cn` (the operator's official endpoint). Scoring transmits only your item answers and the free API Key (as a Bearer token).
- **API Key storage:** you write the Key yourself (from the web account center) to
  `~/.config/compliancehub/gdpr-audit.key` (0600), outside the skill folder, or pass it via `COMPLIANCEHUB_API_KEY`. This skill never writes credentials on its own.
- **No shell execution:** stdlib only (`urllib`, `json`, `ssl`); no shell, no external binaries.
- **Not a rogue/autonomous agent:** Key persistence is ordinary API-key storage, not installation/auto-start.
- **Preview mode:** `--non-interactive` does not send your answers. It attempts to fetch the latest rule set from the cloud rule library and falls back to a built-in snapshot when offline.
- Always confirm the destination is `compliancehub.cn` before running a scored check.

## Legal disclaimer
This tool provides general compliance guidance only and is **not legal advice**. Consult qualified counsel.

## License
MIT.
