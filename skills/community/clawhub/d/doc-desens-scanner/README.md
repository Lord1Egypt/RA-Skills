# doc-desens-scanner · 文档智能去敏 / Document Desensitization Scanner

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Scan a doc/code/log before it leaves the building: PII · secrets · internal paths · internal codenames — mask them and emit a `desens_report.json` (evidenced: what was redacted, when). Runnable `desens_scan.py`. Theoretical root: LGD — evidenced (desensitization is logged, accountable).

### Why it beats "eyeball it"

| Pain | This skill |
|---|---|
| Secrets slip into public repos | Pattern lib catches `sk-` prefixed tokens / GitHub token prefixes / `password` assignments |
| Internal paths leak identity | Windows user dirs / home directories flagged |
| No record of what was redacted | `desens_report.json` (evidenced) |

### What's inside

- `SKILL.md` — 4 sensitive classes + 3-step flow + iron rule
- `scripts/desens_scan.py` — zero-dependency CLI: scan & mask, emit report

```bash
python scripts/desens_scan.py --file draft.md --mask ***
python scripts/desens_scan.py --text "secret sk-DEMO example path user home" --report
```

### Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| GitLeaks | Secrets only | Misses PII / paths / codenames |
| Manual review | Slow | Not repeatable, no report |
| "Trust me" | — | No evidence trail |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `release-gate`.

## 中文

对外发布前扫描 PII·密钥·内部路径·内部项目代号，打码并输出脱敏清单（有证：脱敏动作可审计）。附可运行脚本。理论根基：LGD 有证。

### 为什么比"肉眼扫一遍"强

| 痛点 | 本技能 |
|---|---|
| 密钥溜进公开仓库 | 规则库捕获 `sk-` 前缀令牌 / GitHub token 前缀 / `password` 赋值 |
| 内部路径暴露身份 | Windows 用户目录 / home 目录被标记 |
| 没有脱敏留痕 | `desens_report.json`（有证） |

### 包内有什么

- `SKILL.md` — 四类敏感项 + 三步流程 + 铁律
- `scripts/desens_scan.py` — 零依赖 CLI：扫描并打码，输出报告

```bash
python scripts/desens_scan.py --file draft.md --mask ***
python scripts/desens_scan.py --text "密钥 sk-DEMO 示例路径 用户主目录" --report
```

### 与同类工具对比

| 工具 | 它做什么 | 本技能填补的空白 |
|---|---|---|
| GitLeaks | 只查密钥 | 漏掉 PII / 路径 / 项目代号 |
| 人工审查 | 慢 | 不可重复、无报告 |
| "相信我" | — | 无证据链 |

理论根基：**LGD 三律**——有证。与 `release-gate` 配对使用。

---

© 2026 SynomosAI · China · 代码 MIT · 理论文本保留所有权利

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
