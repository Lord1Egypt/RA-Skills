# AGENTS.md — 文档编写技能库

> 本仓库为 **skills-repo/docs-writer**，面向个人开发者和小团队，提供项目文档自动化生成技能。采用 superpower 架构。

## 目录约定（superpower）

| 层 | 目录 | 职责 | Agent 何时读 |
|----|------|------|--------------|
| L1 | `SKILL.md` | 路由层，能力索引 | 始终先读 |
| L2 | `references/` | 深层 playbook（流水线/API/图表） | 按路由表按需加载 |
| L3 | `skills/` | 四个细粒度子技能 | 落地具体动作时调用 |
| L4 | `scripts/` | 确定性文档检查脚本 | 需核查死链/标注时运行 |
| L5 | `assets/` | 检查规则、README 模板 | 被 scripts 读取执行 |

## 加载顺序

1. 读 `SKILL.md` 路由表，判断任务属于哪一类。
2. 做方法论决策（文档顺序、API 策略、图表选型）→ 读对应 `references/`。
3. 要落地具体动作（生成 README/Changelog/API/图）→ 调 `skills/` 子技能。
4. 需确定性检查（死链、代码块标注）→ 跑 `scripts/`，规则来自 `assets/`。

## 技能清单

| # | 技能 | 用途 |
|---|------|------|
| 1 | readme-generator | 从代码库自动生成专业 README |
| 2 | changelog-writer | 从 Git 历史生成结构化 Changelog |
| 3 | api-doc-generator | API 文档自动生成（OpenAPI/Swagger） |
| 4 | diagram-architect | 架构图/流程图/时序图/ER 图生成 |

## 定位

- 面向个人开发者和小团队（1-5 人）
- 聚焦"项目文档写什么、怎么写"
- 不替代专业技术写作工具（MadCap Flare 等）
