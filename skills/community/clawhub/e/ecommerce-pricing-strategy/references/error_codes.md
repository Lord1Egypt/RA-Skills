# 错误码定义 - ecommerce-pricing-strategy

> 来源: SKILL.md(ecommerce-pricing-strategy) + 05文档§七

> 电商定价策略生成器的错误码与处理方案。

## 错误码列表

| 错误码 | 描述 | 触发条件 | 处理方案 |
|:-------|:-----|:---------|:---------|
| INVALID_INPUT | 成本为空或非正数 | cost参数为空或≤0 | 返回错误，提示cost应为正数 |
| INVALID_COMPETITOR | 竞品价格格式错误 | competitor_prices非逗号分隔数字 | 降级为成本加成法，提示竞品格式应为逗号分隔数字 |
| INVALID_PLATFORM | 平台无效 | platform不在支持列表中 | 返回错误，提示可选xianyu/douyin/taobao/pdd/jd/kuaishou |
| INVALID_ACTION | action无效 | action非strategy/promotion/bundle | 返回错误，提示可选strategy/promotion/bundle |

### 输入验证规则

| 字段 | 类型 | 验证规则 | 失败错误码 |
|:-----|:-----|:---------|:-----------|
| cost | number | 必须为正数 | INVALID_INPUT |
| competitor_prices | string | 逗号分隔的数字列表 | INVALID_COMPETITOR |
| platform | string | xianyu/douyin/taobao/pdd/jd/kuaishou之一 | INVALID_PLATFORM |
| action | string | strategy/promotion/bundle之一 | INVALID_ACTION |

### 降级策略

| 场景 | 降级方案 |
|:-----|:---------|
| 竞品价格格式错误 | 降级为成本加成法(售价=成本×(1+加成率)) |
| 竞品价格为空 | 降级为成本加成法 |
| 平台未指定 | 使用默认加成率计算 |
