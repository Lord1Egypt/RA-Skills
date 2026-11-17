# Current State

## 进度 Progress
- Current chapter: 2

## 地点与时间 Location And Time

青云门，外门，早春。

## 主角 Protagonist
- status: 炼气三层，刚突破
- goal: 在外门大比中脱颖而出
- constraints: 资源有限，仅有 300 下品灵石

## 人物关系 Relationships

| 角色 | 与主角关系 | 状态 |
| --- | --- | --- |
| 林逸 | 室友，好友 | 第 1 章结伴 |
| 苏霜 | 内门弟子，初遇 | 第 2 章藏经阁初见 |

## 已知事实 Known Truths（章节感知事实）

> 以本表为"某角色在第 N 章时知道什么、不知道什么"的硬边界。
> `evidence` 为 introduced_chapter 对应章节的原文短引，validate_book 会校验引文必须在该章正文命中。

| fact_id | statement | subject | truth_status | introduced_chapter | invalidated_chapter | source_chapter | knower | known_from_chapter | confidence | evidence | notes |
| --- | --- | --- | --- | ---: | ---: | --- | --- | ---: | --- | --- | --- | --- |
| fact-001 | 陆恒入门首日入住外门甲字七号舍 | 主角 | 当前为真 | 1 | — | 1 | 主角 | 1 | 确证 | 陆恒站在甲字七号舍前 | 第1章正文 |
| fact-002 | 林逸是甲字八号的外门弟子，与陆恒结伴 | 林逸 | 当前为真 | 1 | — | 1 | 主角 | 1 | 确证 | 在下林逸，住甲字八号 | 第1章正文 |
| fact-003 | 陆恒在藏经阁三层初遇内门弟子苏霜 | 苏霜 | 当前为真 | 2 | — | 2 | 主角 | 2 | 确证 | 苏霜，内门 | 第2章正文 |

## 资源 / 伤势 / 库存 Resources / Injuries / Inventory

- 下品灵石：300 枚
- 回春丹：3 枚

## 道具账本 Prop Ledger

> 审计维 39 的判定基础。origin（来历）为道具获得过程的权威记录；origin 变化 = canon 变更，须同步失效旧事实。

| prop_id | 名称 | 类别 | 数量 | 容量单位 | 归属角色 | 存放位置 | 状态 | acquired_chapter | disposed_chapter | previous_owner | origin | event_id | 最近变化章 | 最近变化事件 | 备注 |
| --- | --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- | ---: | ---: | --- |
| prop-001 | 回春丹 | 丹药 | 3 | 枚 | 主角 | 储物袋乙格 | active | 1 | — | — | 入门发放 | evt-001 | 1 | 入门发放 | 疗伤用 |
| prop-002 | 青锋剑 | 法器 | 1 | 柄 | 主角 | 背上剑鞘 | active | 2 | — | — | 藏经阁获赠 | evt-002 | 2 | 藏经阁获赠 | 下品法器 |
| prop-003 | 下品灵石 | 货币 | 300 | 枚 | 主角 | 储物袋甲格 | active | 1 | — | — | 入门发放 | evt-001 | 1 | 入门发放 | — |

## 空间锚点 Spatial Anchors

> 审计维 38 的判定基础。正文被交互的固定物件必须能在锚点中找到（登记完备性）。

| scene_id | canonical_name | aliases | coordinate_reference | 方位 / 格局 | 出入口 | 关键物件位置 | valid_from_chapter | valid_until_chapter | last_change_event | 建立章 | 最近更新章 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| scene-001 | 青云门外门弟子舍（甲字七号） | 甲字七号 | — | 坐北朝南，一明一暗；明间起居、暗间卧榻 | 南向双扇门 | 东墙木案、西墙兵器架、暗间单人床 | 1 | — | — | 1 | — | — |
| scene-002 | 藏经阁三层 | — | — | 八角形中厅，八面经橱按八卦方位排列 | 仅西南角木梯 | 中厅八角石台（阵眼）、离位经橱 | 2 | — | — | 2 | — | — |

## 当前冲突 Current Conflict

外门大比即将开始，陆恒需要快速提升实力。
