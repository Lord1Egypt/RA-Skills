# CPN JSON Schema 参考

## 完整结构

```json
{
  "project_id": "REST-ORDER-001",
  "color_sets": [
    { "name": "OrderType",   "values": ["堂食", "外卖"] },
    { "name": "DishType",    "values": ["热菜", "冷菜", "饮品"] },
    { "name": "StockStatus", "values": ["充足", "不足"] }
  ],
  "places": [
    {
      "id": "P1",
      "name": "顾客_待点餐",
      "color": "OrderType",
      "initial_marking": ["1`堂食"],
      "subproject": "点餐阶段",
      "chain": "点餐链"
    },
    {
      "id": "P8",
      "name": "库存_充足",
      "color": "StockStatus",
      "initial_marking": ["1`充足"],
      "subproject": "点餐阶段",
      "chain": "库存链"
    }
  ],
  "transitions": [
    {
      "id": "T1",
      "name": "接单",
      "guard": "true",
      "subproject": "点餐阶段",
      "chain": "点餐链"
    },
    {
      "id": "T2",
      "name": "开始备餐",
      "guard": "true",
      "subproject": "备餐阶段",
      "chain": "厨房链"
    }
  ],
  "arcs": [
    { "id": "A1", "from": "P1", "to": "T1", "type": "input",  "annotation": "1`堂食" },
    { "id": "A2", "from": "T1", "to": "P2", "type": "output", "annotation": "1`堂食" }
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
      "mechanism": "guard_condition",
      "predecessor": "厨房链.出餐",
      "successor": "收银链.结账",
      "description": "出餐完成后才能结账（跨链守卫条件）"
    },
    {
      "id": "DEP3",
      "mechanism": "fusion_place",
      "predecessor": "库存链.库存_充足",
      "successor": "厨房链.开始备餐",
      "description": "库存充足才能备餐（融合库所共享状态）"
    }
  ]
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | string | 项目唯一标识 |
| color_sets | array | 着色集合定义，token 的类型枚举 |
| places | array | 库所列表，`initial_marking` 非空表示有初始 token |
| transitions | array | 变迁列表，`guard` 为触发守卫条件 |
| arcs | array | 弧列表，`type` 为 input 或 output |
| dependency_rules | array | 依赖规则，`mechanism` 为 arc_sequence / guard_condition / fusion_place |

## 关键约束

- **多输入变迁**：所有输入库所在流程某时刻必须都有 token，否则死锁
- **资源库所**：库存、人员等资源库所需设 `initial_marking`
- **chain 字段**：用于 HTML 可视化的颜色分组，同一业务链用同一 chain 名

## 完整示例

见 `references/example-restaurant.md`（餐厅点餐流程，含建模要点说明）
