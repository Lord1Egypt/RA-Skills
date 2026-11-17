# 环境变量审计器 / Environment Variable Auditor

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `env-var-audit` v1.0.1 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

## English

**Can't run a fresh clone? Secrets leaked into source? One command reconciles the environment-variable books.**

Audit env vars: undocumented keys, unused examples, hardcoded secrets.

**Keywords**: env var, .env.example, hardcoded secret, secret scanning, config audit, leak prevention.

### Install & try
```bash
mkdir -p ~/.claude/skills/env-var-audit/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/env-var-audit/scripts/env_var_audit.py -o ~/.claude/skills/env-var-audit/scripts/env_var_audit.py
python ~/.claude/skills/env-var-audit/scripts/env_var_audit.py --help
```
Other agents: place under `~/.config/opencode/skills/`, `~/.agents/skills/`, etc. with the same structure.

### Usage
```bash
# audit the current project
python scripts/env_var_audit.py .

# JSON output
python scripts/env_var_audit.py . --json
```

### Sample output
```
$ env_var_audit.py .
env vars read by code: 5 · declared in .env.example: 4
  undocumented MEDIUM: AWS_REGION (used in code, missing from example)
  hardcoded-secret HIGH: DB_PASSWORD = "hunter2secret123" (app/db.py:12)
high findings, rc=1
```

### Exit codes & error receipts
rc=0 ok / rc=1 findings / rc=2 usage.
| Code | Meaning | Suggested fix |
|---|---|---|
| EVA_E_NO_DIR | directory does not exist | pass the correct project root |
| EVA_E_NO_FILES | no scannable source files found | ensure the dir holds .py/.js/.ts/.sh files |

### FAQ
**How is HIGH decided?**
Two classes: the value matches a known secret prefix (ghp_ / sk- / AKIA / xoxb etc.), or a likely-secret field name is assigned a 12+ char literal that is not an example.

**Any false positives?**
A few (e.g. fake keys in sample code). The tool does static heuristics with file:line evidence; the call to act is human.

### Links
- Repo: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/env-var-audit
- Family hub: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

### Disclaimer
env-var-audit outputs deterministic format/structure verdicts and rule-based suggestions; it is not legal advice, a security guarantee or professional consultation. Have a human review key decisions against the latest official requirements.

License MIT © env-var-audit authors. LGD-Powered badge: https://synomos.ai/badge/powered/svg/lgd-powered-en.svg

## 中文

**克隆即跑不起来？密钥进了源码？一条命令把环境变量账目对清。**

审计环境变量：未文档化的键、未使用的示例、硬编码密钥。

**关键词**：环境变量 .env.example 硬编码密钥 secret scanning env audit 配置审计 泄漏防护

### 安装即试
```bash
mkdir -p ~/.claude/skills/env-var-audit/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/env-var-audit/scripts/env_var_audit.py -o ~/.claude/skills/env-var-audit/scripts/env_var_audit.py
python ~/.claude/skills/env-var-audit/scripts/env_var_audit.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置。

### 用法
```bash
# 审计当前项目
python scripts/env_var_audit.py .

# JSON 输出
python scripts/env_var_audit.py . --json
```

### 真机输出
```
$ env_var_audit.py .
代码读取的环境变量：5 · .env.example 声明：4
  未文档化 MEDIUM：AWS_REGION（代码使用，example 未列）
  硬编码疑密 HIGH：DB_PASSWORD = "hunter2secret123" (app/db.py:12)
发现高危项，rc=1
```

### 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| EVA_E_NO_DIR | 目录不存在 | 传入正确的项目根目录 |
| EVA_E_NO_FILES | 未发现可扫描的源码文件 | 确认目录含 .py/.js/.ts/.sh 文件 |

### FAQ
**HIGH 是怎么判定的？**
两类：值匹配已知密钥前缀（ghp_/sk-/AKIA/xoxb 等），或疑似密钥字段名被赋以 12 位以上字面量且不是示例。

**会误报吗？**
会有少量误报（如示例代码里的假密钥）。工具只做静态启发式并给出文件行号证据，处置由人决定。

### 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/env-var-audit
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

### 免责
env-var-audit 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © env-var-audit authors. LGD-Powered 徽章：https://synomos.ai/badge/powered/svg/lgd-powered-en.svg

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
