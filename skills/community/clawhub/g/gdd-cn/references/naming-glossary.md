# 术语对照与文风约束

写任何一段前先读这份。目标只有一个：别让文档冒出英文直译腔，读起来像国内策划写的。

## 一、术语对照（左为原词，右为国内常用说法）

| 原词 | 国内常用 | 说明 |
|---|---|---|
| Player Fantasy | 设计目的 / 体验目标 | 别直译成「玩家幻想」 |
| Core Loop | 核心循环 | |
| Progression | 成长线 / 养成线 | |
| Tuning Knobs | 可调项 / 可调数值 | |
| Edge Cases | 边界情况 / 异常处理 | 必须 IF-THEN，别写「妥善处理」 |
| Acceptance Criteria | 验收标准 | QA 口径：前置 / 操作 / 预期 |
| Entities | 实体 | |
| Affix | 词条 | |
| Drop Table / Loot | 掉落表 / 掉落 | |
| Weight | 权重 | |
| Pity | 保底 | |
| Gacha | 抽卡 / 卡池 | |
| Power / CP | 战力 | |
| Stamina / Energy | 体力 / 精力 | |
| Sink / Faucet | 消耗口 / 产出 | 经济系统 |
| Retention | 留存（次留 / 7留 / 30留） | |
| DAU / MAU | 日活 / 月活 | |
| ARPPU / ARPU | 付费用户平均收入 / 用户平均收入 | |
| Whale / Dolphin / Minnow | 大R / 中R / 小R | |
| F2P | 免费玩家 | 文档里写「免费玩家」，别写「白嫖」 |
| Vertical Slice | 纵切片 / 垂直切片 | |
| Polish | 打磨 | |
| Pivot | 转向 | |
| Scope Creep | 需求蔓延 / 范围膨胀 | |
| Soft Lock | 卡死（软锁） | |
| Degenerate Strategy | 退化玩法 / 无脑最优解 | |
| Min-max | 极限配装 | |
| Skill Ceiling / Floor | 上限 / 下限 | |
| Onboarding | 新手引导 | |
| Telemetry / Event | 埋点 | |
| Live Ops | 长线运营 / 版本运营 | |
| Build | 版本包 | |
| Hotfix | 热修 | |
| Churn | 流失 | |
| A/B Test | 分组实验 / AB 实验 | |
| Milestone | 里程碑 / 阶段目标 | |

## 二、角色体系对照

| 原角色 | 国内叫法 |
|---|---|
| systems-designer | 数值策划 / 系统策划 |
| game-designer | 系统策划 / 玩法策划 |
| level-designer | 关卡策划 |
| narrative-director | 主文案 / 剧情策划 |
| economy-designer | 数值策划（经济向） |
| creative-director | 主策 / 制作人 |
| art-director | 主美 |
| technical-artist | TA / 技术美术 |
| audio-director | 音频负责人 |
| qa-lead | 测试组长 / QA 负责人 |
| gameplay-programmer | 客户端 / 玩法程序 |
| engine-programmer | 引擎程序 |
| ui-programmer | UI 程序 |
| ai-programmer | AI 程序 |

## 三、研发流程用语

需求评审 → 技术评审 → 排期 → 开发 → 提测 → 测试 → 验收 → 上线 → 复盘

对应文档状态：未开始 → 设计中 → 待评审 → 已评审 → 开发中 → 已提测 → 已验收 → 已上线

## 四、文风约束（去 AI 味）

- 一句话能说清的别拆三句。
- 不要「首先 / 其次 / 最后」三段式排比堆砌。
- 不要用「值得注意的是」「需要指出的是」「总而言之」「不可忽视」。
- 不要给每个条目加 emoji。
- 用祈使句和陈述句，别用「我们可以……」「让我们一起……」。
- 表格优先于长段落；同一层级超过 4 条就列表。
- 术语第一次出现给中文，后面直接用。
- 数值必须有单位或量纲（秒 / 米 / 百分比 / 万分比 / 级）。
- 每个「建议 / 应该」都要带理由，不要空降结论。
- 写规则时用动词开头：进入、触发、扣除、结算、解除、锁定。
- 玩家的约束和能做的事分开写，约束和 capability 同等重要。
