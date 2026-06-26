# best-skill-recommendations (ClawHub 版)

## 中文介绍

`best-skill-recommendations` 是一个技能综合评估与推荐技能，通过 **ClawHub** 获取候选技能，进行冲突检测、替换/共存决策，并在用户确认后安全安装。

它优先消费其他技能（如 `find-skills`）已搜索到的结果做评估；当没有上游结果时，自行去 ClawHub 搜索并推荐。

**ClawHub 常用命令：**

| 操作 | 命令 |
|---|---|
| 搜索技能 | `clawhub search <关键词>` |
| 安装技能 | `clawhub install <技能>` |
| 更新技能 | `clawhub update <技能>` |
| 查看已安装 | `clawhub list` |
| 卸载技能 | `clawhub uninstall <技能>` |

核心能力：

- 通过 ClawHub 搜索并获取候选技能
- 评估已安装技能与新候选的冲突/重叠关系
- 给出"卸载替换"或"并存共用"的建议
- 安装前强制披露来源、版本和风险信号
- 在用户确认后再执行安装

适用场景：

- "这个需求装哪个技能最合适？"
- "我现在的技能会不会和新技能冲突？"
- "应该替换旧技能还是共存？"

---

## English Overview

`best-skill-recommendations` is a skill evaluation and recommendation engine — it sources candidates from **ClawHub**, detects install conflicts, recommends replace-or-coexist strategies, and executes safe installs with explicit user confirmation.

It prefers to evaluate results already discovered by upstream skills (e.g. `find-skills`). Only when no upstream results exist does it independently search ClawHub.

**ClawHub CLI commands:**

| Action | Command |
|---|---|
| Search skills | `clawhub search <keywords>` |
| Install a skill | `clawhub install <skill>` |
| Update a skill | `clawhub update <skill>` |
| List installed | `clawhub list` |
| Uninstall | `clawhub uninstall <skill>` |

Key capabilities:

- ClawHub-powered skill discovery
- Installed-skill compatibility and conflict analysis
- Replace-vs-coexist decision support
- Mandatory pre-install disclosure (source, version, risk signals)
- Explicit user confirmation before install actions

Typical use cases:

- "What is the best skill for this task?"
- "Will this new skill conflict with what I already installed?"
- "Should I replace an existing skill or keep both?"

---

## Author

VinceZ.辉 (<https://x.com/zhaowh3613>)
