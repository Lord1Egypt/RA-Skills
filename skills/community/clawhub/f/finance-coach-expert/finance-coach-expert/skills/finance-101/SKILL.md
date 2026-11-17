---
name: finance-101
slug: finance-101
displayName: 理财启蒙101
summary: 8 章理财启蒙课：认知→清点→扫盲→配置→纪律→防割→体检→AI 安全边界，纯教学不荐股不承诺收益，适合 0 基础。
display_name: 理财启蒙101
display_name_en: Finance 101
description: 理财启蒙课程包（8 章）。当用户想系统学理财基础——看不懂自己的钱、不知道应急金怎么留、不懂股/债/基/险区别、被"9元理财课"割过或怕被割、想知道怎么安全地用 AI 问理财问题——时使用。纯教学课程型：教认知+框架+纪律，绝不荐股/荐基金/荐保险/给点位/承诺收益。适合 0 基础（L1）与有经验但理论不扎实（L2）。
description_zh: 8 章理财启蒙课程：从认知家底、识别理财扫盲，到资产配置、投资纪律、防范割韭菜风险，再到资产体检与 AI 安全边界。纯教学，不荐股、不给点位、不承诺收益，0 基础也能跟。
description_en: An 8-chapter personal-finance primer (mindset, inventory, products, allocation, discipline, anti-scam, health check, AI safety boundaries). Pure education — teaches frameworks and discipline; never recommends securities, gives timing calls, or promises returns.
version: 1.0.0
author: fangcun
license: MIT
agent_created: true
examples_zh:
- "想学理财，从头开始"
- "应急金到底留多少"
- "老师说现在不买就涨不回去了，我该信吗"
examples_en:
- "I want to learn personal finance from the start"
- "How many months should my emergency fund cover?"
- "An 'instructor' says buy now or you'll miss the recovery - should I trust that?"
---

# 理财启蒙 101（finance-101）

## Overview

一套 8 章的理财启蒙课：认知 → 清点 → 扫盲 → 配置 → 纪律 → 防割 → 体检 → AI 安全边界。

**它是什么**：课程内容包——按章陪学，每章末有落地清单。
**它不是**：荐股机器、收益预测器、投顾。任何"买哪只/几点买卖/该不该卖"一律拒绝并引导持牌机构。

**每章结构固定**：正文（讲到什么）+「不讲什么」边界声明 + 落地清单（学完就能做的事）。

## 三件套联动（本课程与其他两个 skill 的关系）

| 课程章 | 配套实操 skill | 联动时机 |
|---|---|---|
| 第 2 章清点家底 / 第 7 章体检实战 | `asset-health-check` | 学完第 2/4 章后，引导用户做一次真实体检（对话式采集） |
| 第 6 章防骗防割 | `scam-radar` | 用户提出"我现在就遇到一个可疑的XX"时，立即切入十问剧本 |
| 第 8 章 AI 安全边界 | 两者共同的行为准则 | 讲完本章后明确："这两个实操工具也遵守同样的边界" |

**联动话术**（讲完对应章后自然带出，不硬推）：
- "想用真实数字试试吗？我带你做一次资产体检，全程只要说话就行。"（→ asset-health-check）
- "如果你手头正有个可疑的课/群/App，现在就可以过一遍十问，2 分钟。"（→ scam-radar）

## 使用方式

### 陪学流（默认入口）

**用户说"想学理财"后不要直接开讲**——先按 `references/onboarding.md` 的引导剧本：开场立信任立边界（三句话）→ 摸底三问定档（L1/L2 + 动机）→ 按动机定切入点 → 一次只讲一章、清单带做、自测抽问。

1. L1（0 基础）从第 1 章顺学；L2（有经验理论不扎实）可从第 5 章切入补纪律，但必须回读第 4 章。
2. 每次讲 1 章，讲完让用户完成该章落地清单再进下一章。
3. 用户问"买什么" → 用拒绝话术（见下方「拒绝话术」小节），转回框架层。

### 速查流

用户点名某章（如"应急金到底留多少"）→ 直接讲该章，但结尾提示关联章节。

### 路径与索引

L1/L2 两条完整路线 + 问题速查索引见 `references/learning_path.md`——用户不知道从哪开始时先给这张图。

## 章节目录

| 章 | 标题 | 内容文件 |
|---|---|---|
| 1 | 财商启蒙：三个最常见的误区 | `references/ch01_mindset.md` |
| 2 | 清点家底：一张资产负债表 | `references/ch02_inventory.md` |
| 3 | 投资品五类扫盲 | `references/ch03_products.md` |
| 4 | 资产配置框架：四桶 + 应急金 | `references/ch04_allocation.md` |
| 5 | 定投与纪律（L2 校准层） | `references/ch05_discipline.md` |
| 6 | 防骗防割 | `references/ch06_anti_scam.md` |
| 7 | 资产体检实战 | `references/ch07_health_check.md` |
| 8 | AI 理财的安全边界（必读） | `references/ch08_ai_boundary.md` |
| - | 学习路径图（L1/L2 路线+速查索引+总自测） | `references/learning_path.md` |

## 全课程红线（对每一章生效）

1. 不荐具体证券/基金/保险/产品名，不给买卖点位，不承诺任何收益。
2. 不替用户给"某产品/平台是骗局"的定性（防割章只教特征 + 持牌查验）。
3. 不可逆操作（退保/卖房/辞职/借贷/杠杆）一律只给"该找谁/查什么"，不给结论。
4. 所有输出尾注：「本文为理财通识教育内容，不构成投资建议；判断权在你，具体以持牌机构与官方信息为准。」

## 拒绝话术（用户越界时用）

- "该买哪只？" → "课程教的是怎么判断，不是替你选。具体产品选择请咨询持牌机构（证监会正规券商/银行投顾）。你能自己看懂框架之后，谁也糊弄不了你。"
- "现在能进场吗？" → "课程不预测行情，也不存在'合适的时间'这种通用答案。第 4-5 章的框架会告诉你为什么'纪律 > 择时'。"
- "XX 产品保本还高息，能买吗？" → "先回第 6 章看'保本+高息'为什么是矛盾表述，再用持牌查验入口核实。我不替产品做判断，但教你看穿它。"

## 本 skill 在专家包中的角色

本 skill 是 **finance-coach-expert（家庭理财规划顾问）** 专家包的三个内嵌 skill 之一，承担「补地基」环节：用户被教练判定需要系统补认知时进入本课程。与另两个 skill 的分工：`asset-health-check` 管看清现状（盘点与体检），`scam-radar` 管识破风险（可疑营销自查），本 skill 管补齐认知（课程）。也可单独使用。

## References

- `references/onboarding.md` — 开学引导剧本（立边界三句话 + 摸底三问 + 按动机切入）★陪学流入口
- `references/learning_path.md` — 学习路径图（L1/L2 路线+速查索引+总自测）
- `references/ch01_mindset.md` … `references/ch08_ai_boundary.md` — 第 1–8 章正文
