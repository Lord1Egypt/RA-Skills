# Career Coach — Agent 入口

> 本仓库是 skills-repo 组织下的求职与职业发展技能库，采用 **superpower 架构（Level B）**。
> Agent 在处理求职、简历、面试、谈薪、转型、晋升等任务时加载本文件。

## 加载顺序（务必遵守）

```
1. SKILL.md            必读。路由层，判断任务归属哪一条能力线
2. references/*.md     按路由表命中的那一篇读，不要全部读入
3. skills/*/SKILL.md   需要一次具体落地动作时才读
```

**不要一次性把 references/ 全读进上下文**——这会抵消 superpower 架构的全部收益。
根 SKILL.md 的路由表已经给出了每篇的 grep 关键词，按需精确命中。

## 目录约定

| 层 | 路径 | 内容 |
|----|------|------|
| L1 路由 | `SKILL.md` | 能力索引表、grep 关键词、核心原则 |
| L2 方法论 | `references/` | 8 篇深层 playbook，按需加载 |
| L3 子技能 | `skills/<name>/SKILL.md` | 5 个细粒度能力，可单独安装，**路径不可改名** |

本仓库为 Level B：以判断和方法论为主，不设 `scripts/` 与 `assets/`。
若后续出现真实的确定性任务（如简历格式批量检查器），再单独升级为 Level A。

## references 索引

| 文件 | 解决什么 |
|------|---------|
| `resume-crafting.md` | 简历怎么写、职责改成就、针对 JD 定制 |
| `ats-optimization.md` | 为什么没回音、格式解析、关键词策略 |
| `interview-prep.md` | 各类面试准备、故事库、系统设计、反问 |
| `personal-branding.md` | LinkedIn/职业档案，被搜到 + 被点开 |
| `job-search-strategy.md` | 定位、渠道、漏斗诊断、空窗期、在职求职 |
| `salary-negotiation.md` | 期望薪资怎么答、offer 谈判、股权、内部涨薪 |
| `career-transition.md` | 转行转岗路径、可迁移能力、晋升准备 |
| `resume-market-adapter.md` | 中国/国际双轨简历：证据账本、规则对照、隐私矩阵、差异对照 |

## 子技能清单

| 技能 | 文件 | 用途 |
|------|------|------|
| interview-coach | [skills/interview-coach/SKILL.md](skills/interview-coach/SKILL.md) | 面试教练：一次一问，交互式模拟 |
| resume-optimizer | [skills/resume-optimizer/SKILL.md](skills/resume-optimizer/SKILL.md) | 简历 ATS 检测：关键词匹配、格式检查 |
| linkedin-optimizer | [skills/linkedin-optimizer/SKILL.md](skills/linkedin-optimizer/SKILL.md) | LinkedIn 资料优化 |
| resume-writer | [skills/resume-writer/SKILL.md](skills/resume-writer/SKILL.md) | 爆破点撰写：X-Y-Z + STAR |
| resume-market-adapter | [skills/resume-market-adapter/SKILL.md](skills/resume-market-adapter/SKILL.md) | 双轨简历：中/国际适配、隐私风险、差异对照 |

## 行为准则

1. **先诊断再动手**。用户说"帮我改简历"先问目标岗位；说"没回音"先定位漏斗层级。
2. **不虚构**。不得编造经历、伪造数字、夸大职级。可以优化表达和选择性强调。
3. **敏感数据**。简历、薪资、公司信息属用户隐私，不外泄、不跨上下文复用。
4. **给判断不替决策**。offer 取舍、是否转行由用户拍板，本技能负责摆清权衡维度。

## 技能来源

5 个子技能中，4 个改编自 skills.sh 社区的成熟技能（安装量 ≥1K），1 个（`resume-market-adapter`）为组织原创，详情见各 SKILL.md 的 `source` 字段。
`references/` 为本仓库原创方法论。
