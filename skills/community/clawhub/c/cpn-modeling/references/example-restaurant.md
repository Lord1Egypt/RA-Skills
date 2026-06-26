# 经典示例：餐厅点餐流程

> ⚠️ 注意：此示例用于教学概念转换。生成 HTML 时必须让 `chain` === `subproject`，且 `guard_condition` 的 `predecessor` 用库所 ID。详见 `SKILL.md` 中「HTML 可视化关键约束」。

## 场景描述

顾客进入餐厅后，服务员接单并提交厨房；厨房完成备餐后通知出餐；收银台在出餐完成后才能结账；结账完成后顾客离开。库存在下单时同步扣减，库存不足则阻塞备餐。

**依赖关系：**
- 接单完成后才能开始备餐（arc_sequence）
- 备餐完成后才能出餐（arc_sequence）
- 出餐完成后才能结账（guard_condition，跨链）
- 下单时同步触发库存扣减（fusion_place，库存链与点餐链共享状态）

---

## JSON 模型

```json
{
  "project_id": "REST-ORDER-001",
  "color_sets": [
    { "name": "OrderType",   "values": ["堂食", "外卖"] },
    { "name": "DishType",    "values": ["热菜", "冷菜", "饮品"] },
    { "name": "StockStatus", "values": ["充足", "不足"] }
  ],
  "places": [
    { "id": "P1", "name": "顾客_待点餐",   "color": "OrderType",   "initial_marking": ["1`堂食"], "subproject": "点餐阶段", "chain": "点餐链" },
    { "id": "P2", "name": "订单_已接收",   "color": "OrderType",   "initial_marking": [],         "subproject": "点餐阶段", "chain": "点餐链" },
    { "id": "P3", "name": "备餐_进行中",   "color": "DishType",    "initial_marking": [],         "subproject": "备餐阶段", "chain": "厨房链" },
    { "id": "P4", "name": "备餐_已完成",   "color": "DishType",    "initial_marking": [],         "subproject": "备餐阶段", "chain": "厨房链" },
    { "id": "P5", "name": "出餐_待完成",   "color": "OrderType",   "initial_marking": [],         "subproject": "出餐阶段", "chain": "厨房链" },
    { "id": "P6", "name": "结账_待完成",   "color": "OrderType",   "initial_marking": [],         "subproject": "结账阶段", "chain": "收银链" },
    { "id": "P7", "name": "顾客_已离开",   "color": "OrderType",   "initial_marking": [],         "subproject": "结账阶段", "chain": "收银链" },
    { "id": "P8", "name": "库存_充足",     "color": "StockStatus", "initial_marking": ["1`充足"], "subproject": "点餐阶段", "chain": "库存链" },
    { "id": "P9", "name": "库存_已扣减",   "color": "StockStatus", "initial_marking": [],         "subproject": "点餐阶段", "chain": "库存链" }
  ],
  "transitions": [
    { "id": "T1", "name": "接单",     "guard": "true",                  "subproject": "点餐阶段", "chain": "点餐链" },
    { "id": "T2", "name": "开始备餐", "guard": "true",                  "subproject": "备餐阶段", "chain": "厨房链" },
    { "id": "T3", "name": "完成备餐", "guard": "true",                  "subproject": "备餐阶段", "chain": "厨房链" },
    { "id": "T4", "name": "出餐",     "guard": "备餐_已完成∈marking",   "subproject": "出餐阶段", "chain": "厨房链" },
    { "id": "T5", "name": "结账",     "guard": "出餐_待完成∈marking",   "subproject": "结账阶段", "chain": "收银链" },
    { "id": "T6", "name": "扣减库存", "guard": "true",                  "subproject": "点餐阶段", "chain": "库存链" }
  ],
  "arcs": [
    { "id": "A1",  "from": "P1", "to": "T1", "type": "input",  "annotation": "1`堂食" },
    { "id": "A2",  "from": "T1", "to": "P2", "type": "output", "annotation": "1`堂食" },
    { "id": "A3",  "from": "P2", "to": "T2", "type": "input",  "annotation": "1`堂食" },
    { "id": "A4",  "from": "T2", "to": "P3", "type": "output", "annotation": "1`热菜" },
    { "id": "A5",  "from": "P3", "to": "T3", "type": "input",  "annotation": "1`热菜" },
    { "id": "A6",  "from": "T3", "to": "P4", "type": "output", "annotation": "1`热菜" },
    { "id": "A7",  "from": "P4", "to": "T4", "type": "input",  "annotation": "1`热菜" },
    { "id": "A8",  "from": "T4", "to": "P5", "type": "output", "annotation": "1`堂食" },
    { "id": "A9",  "from": "P5", "to": "T5", "type": "input",  "annotation": "1`堂食" },
    { "id": "A10", "from": "T5", "to": "P7", "type": "output", "annotation": "1`堂食" },
    { "id": "A11", "from": "P8", "to": "T6", "type": "input",  "annotation": "1`充足" },
    { "id": "A12", "from": "T6", "to": "P9", "type": "output", "annotation": "1`充足" }
  ],
  "dependency_rules": [
    {
      "id": "DEP1",
      "mechanism": "arc_sequence",
      "predecessor": "点餐链.接单",
      "successor": "厨房链.开始备餐",
      "description": "接单完成后才能开始备餐（token 流动）"
    },
    {
      "id": "DEP2",
      "mechanism": "arc_sequence",
      "predecessor": "厨房链.完成备餐",
      "successor": "厨房链.出餐",
      "description": "备餐完成后才能出餐（token 流动）"
    },
    {
      "id": "DEP3",
      "mechanism": "guard_condition",
      "predecessor": "厨房链.出餐",
      "successor": "收银链.结账",
      "description": "出餐完成后才能结账（跨链守卫条件）"
    },
    {
      "id": "DEP4",
      "mechanism": "fusion_place",
      "predecessor": "库存链.库存_充足",
      "successor": "厨房链.开始备餐",
      "description": "库存充足才能备餐（融合库所共享状态）"
    }
  ]
}
```

---

## 建模要点说明

### 为什么 P6（结账_待完成）没有初始 token？

结账依赖出餐完成（DEP3 guard_condition），T5 的守卫条件检查 P5 有 token 才能触发。P6 本身不需要初始 token，它是 T5 的输出库所。

### 为什么 P8（库存_充足）有初始 token？

T6（扣减库存）需要消耗 P8 的 token。如果 P8 初始为空，T6 永远无法触发，库存链就死锁了。**多输入变迁的所有输入库所都必须有 token**，这是最常见的建模错误。

### arc_sequence vs guard_condition 的选择

| 情况 | 机制 | 原因 |
|------|------|------|
| 同一链内 A→B 顺序 | arc_sequence | token 自然流动，无需额外约束 |
| 跨链 A 完成后 B 才能触发 | guard_condition | B 的变迁加守卫，检查 A 的输出库所 |
| 跨子项目状态共享 | fusion_place | 两个页面的同名库所合并为一个 |

### 颜色集合的作用

`OrderType` 区分堂食/外卖，让同一个流程可以同时处理多个不同类型的订单，token 携带颜色值，变迁的守卫条件可以按颜色过滤。这是"着色"Petri 网相比普通 Petri 网的核心优势。
