# 求职与职业发展技能库

> AI Agent Skills for Career Development —— 简历、ATS、面试、求职策略、谈薪、转型与晋升

## 定位

一套覆盖**求职全链路**的 AI 技能库：从职业定位、简历撰写、档案打造、投递策略、
面试准备，到薪酬谈判和入职后的转型与晋升规划。

采用 **superpower 架构**（Level B）：根 `SKILL.md` 只做路由，
8 篇深层 playbook 放在 `references/` 中按需加载，5 个细粒度子技能可单独安装。

## 核心理念

> 求职的说服力来自证据，不是措辞。工具能帮你表达，不能替你创造成果。

- **先诊断再开方** — "投了没回音"要先定位卡在漏斗哪一层，而不是直接改简历
- **简历是证据材料** — 不是履历流水账，每段经历要能预测未来表现
- **ATS 不会自动拒你** — 它只是解析和检索，真正的淘汰仍由人完成
- **谈判靠信息和 BATNA** — 不是胆量测试
- **先做后要** — 转型和晋升都遵循同一条逻辑：证据先于身份

## 架构

```
career-coach/
├── SKILL.md              路由层：能力索引 + grep 关键词
├── references/           深层 playbook（按需加载）
│   ├── resume-crafting.md        简历撰写：读者模型、四级阶梯、JD 反向工程
│   ├── ats-optimization.md       ATS：解析层 + 检索层、关键词策略
│   ├── interview-prep.md         面试：题型地图、故事库法、系统设计五步
│   ├── personal-branding.md      个人档案：被搜到 + 被点开
│   ├── job-search-strategy.md    求职策略：渠道转化率、漏斗诊断
│   ├── salary-negotiation.md     谈薪：BATNA、时机、整包思维
│   ├── career-transition.md      转型与晋升：可迁移能力、提前 6 个月
│   └── resume-market-adapter.md 双轨简历：中英文差异、地区化隐私、证据账本
└── skills/               细粒度子技能（可单独安装）
    ├── interview-coach/
    ├── linkedin-optimizer/
    ├── resume-market-adapter/
    ├── resume-optimizer/
    └── resume-writer/
```

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 面试 | `interview-coach` | 面试教练：逐题深挖、意图识别、STAR 练习 | [衍生](https://skills.sh/addyosmani/agent-skills/interview-me) |
| ATS | `resume-optimizer` | 简历 ATS 优化：关键词匹配、格式兼容、匹配分 | [衍生](https://skills.sh/paramchoudhary/resumeskills/resume-ats-optimizer) |
| LinkedIn | `linkedin-optimizer` | LinkedIn 优化：Headline、About、搜索可见性 | [衍生](https://skills.sh/paramchoudhary/resumeskills/linkedin-profile-optimizer) |
| 爆破点 | `resume-writer` | 爆破点撰写：X-Y-Z 公式、STAR 方法、量化成就 | [衍生](https://skills.sh/paramchoudhary/resumeskills/resume-bullet-writer) |
| 双轨 | `resume-market-adapter` | 中国/国际市场双轨精修：证据账本、地区化隐私、差异对照 | [原创](https://github.com/skills-repo/career-coach) |

## 快速开始

**安装整个技能库**（推荐，含全部 playbook）：

```bash
npx skills add skills-repo/career-coach -g -y
```

**只装单个子技能**（轻量，仅该能力）：

```bash
npx skills add skills-repo/career-coach@interview-coach -g -y
npx skills add skills-repo/career-coach@resume-optimizer -g -y
npx skills add skills-repo/career-coach@linkedin-optimizer -g -y
npx skills add skills-repo/career-coach@resume-writer -g -y
npx skills add skills-repo/career-coach@resume-market-adapter -g -y
```

## 推荐工作流

```
定位          简历            档案             投递           面试          谈薪
job-search → resume-      → personal-     → job-search  → interview- → salary-
strategy     crafting        branding        strategy      prep         negotiation
             + ats-opt
```

卡住时按漏斗层定位：投递无回音 → ATS + 简历；初面被挂 → 面试准备；
到终面被拒 → 公司研究 + 反问；拿到 offer → 谈薪。

## 诚信边界

本技能库帮你**优化表达、突出相关性、挖掘并量化真实成果**。
不提供虚构经历、伪造数字、夸大职级的建议——这些在背调和深度追问中会暴露，
代价远大于收益。

## 许可

MIT
