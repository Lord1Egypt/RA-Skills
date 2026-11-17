---
name: ecosystem-auditor
version: 1.0.0
description: |
  技能生态健康度审计：扫描技能生态（默认 ~/.workbuddy/skills），对每枚技能做体检——
  frontmatter 合法性、脚本可编译性、陈旧度、近重复（shingle Jaccard）、孤儿 meta
  （meta-X 但教师 X 不存在），输出结构化健康报告，供元进化引擎定位"该修/该并/该弃"的技能。
  这是让全栈超级智能体"能治理自身生态"的元能力，一线大模型不具备。
agent_created: true
visibility: public
---

# ecosystem-auditor（技能生态健康度审计）

> 「自主能力治理与生态(下一阶梯)」域 Top1（权重 1.50）：让已具备全栈能力的超级智能体
> 能审计、能自审自己的技能生态，而非只管"造新技能"。

## 何时使用
- 定期体检技能生态，找出坏 frontmatter / 语法错误 / 长期未更新 / 近重复 / 孤儿 meta。
- 元进化引擎在批量构建/蒸馏后，定位需要 repair 或合并的技能。
- 发布前健康门禁：阻断损坏或重复的技能进入发布清单。

## 核心 API（scripts/ecosystem_auditor.py）
- `audit(skills_root, stale_days=120, dup_threshold=0.9)` → 报告 dict：
  - `broken`：frontmatter 非法或脚本语法错误
  - `stale`：最后修改超 stale_days
  - `duplicates`：SKILL.md 正文 shingle Jaccard ≥ dup_threshold 的近重复对
  - `orphans`：以 `meta-` 开头但对应教师技能不存在的蒸馏学生
  - `summary`：各项计数
- `python ecosystem_auditor.py --selftest`：内置自检（自建临时沙箱，零副作用）。

## 设计要点
- **零文件副作用**：脚本检查用内存 `compile()`，不写 `__pycache__`；陈旧度扫描排除
  `__pycache__/*.pyc`，避免编译产物干扰 mtime。
- **近重复检测**：正文去空白小写后取 4-gram 集合，Jaccard 度量相似度，可配置阈值。
- **孤儿 meta**：蒸馏学生 `meta-<教师>` 若找不到教师技能即标记，防止蒸馏链断裂。

## 与元进化闭环的关系
作为 meta-evolver 的"生态体检仪"：sense 阶段可调用本技能生成 `summary`，把
`broken`/`orphans` 自动转为 `repair`/`evolve` 缺口，形成"构建→审计→修复"治理闭环。

## 自进化学习系统
本技能接入 meta-evolver 自进化闭环：每次审计经 learner 记录生态规模/问题分布，
跨会话沉淀"哪些命名易冲突""哪些域易重复"等经验。

## 已知限制
- 近重复阈值需按生态规模调参；过小误报、过大漏报。
- 陈旧度基于文件 mtime，不反映"逻辑是否仍正确"（需结合运行时成功率）。
