# 数据查询示例参考

## 常见查询模式

### 1. 单数值查询

**用户问题**："昨天DAU多少？"

**查询JSON**：
```json
{
  "filters": [
    {"column": "日期", "operator": "==", "value": "昨天"}
  ],
  "aggregations": [
    {"column": "活跃用户", "func": "sum", "alias": "DAU"}
  ]
}
```

### 2. 时间趋势查询

**用户问题**："最近7天新增用户趋势"

**查询JSON**：
```json
{
  "filters": [
    {"column": "日期", "operator": ">=", "value": "7天前"}
  ],
  "groupby": ["日期"],
  "aggregations": [
    {"column": "新增用户", "func": "sum", "alias": "新增用户"}
  ],
  "sort": [{"column": "日期", "asc": true}]
}
```

### 3. 分类对比查询

**用户问题**："各渠道的用户占比"

**查询JSON**：
```json
{
  "groupby": ["渠道"],
  "aggregations": [
    {"column": "用户数", "func": "sum", "alias": "总用户数"}
  ],
  "sort": [{"column": "总用户数", "asc": false}]
}
```

### 4. 平均值查询

**用户问题**："平均客单价是多少？"

**查询JSON**：
```json
{
  "aggregations": [
    {"column": "订单金额", "func": "mean", "alias": "平均客单价"}
  ]
}
```

### 5. 多维度分析

**用户问题**："各城市近30天的销售额"

**查询JSON**：
```json
{
  "filters": [
    {"column": "日期", "operator": ">=", "value": "30天前"}
  ],
  "groupby": ["城市", "日期"],
  "aggregations": [
    {"column": "销售额", "func": "sum", "alias": "总销售额"}
  ],
  "sort": [
    {"column": "城市", "asc": true},
    {"column": "日期", "asc": true}
  ]
}
```

### 6. 最大值查询

**用户问题**："销量最高的产品是哪个？"

**查询JSON**：
```json
{
  "groupby": ["产品名"],
  "aggregations": [
    {"column": "销量", "func": "sum", "alias": "总销量"}
  ],
  "sort": [{"column": "总销量", "asc": false}],
  "limit": 1
}
```

### 7. 本周数据

**用户问题**："本周每天的收入"

**查询JSON**：
```json
{
  "filters": [
    {"column": "日期", "operator": ">=", "value": "本周"}
  ],
  "groupby": ["日期"],
  "aggregations": [
    {"column": "收入", "func": "sum", "alias": "日收入"}
  ],
  "sort": [{"column": "日期", "asc": true}]
}
```

### 8. 文本筛选

**用户问题**："北京地区的订单有多少？"

**查询JSON**：
```json
{
  "filters": [
    {"column": "城市", "operator": "==", "value": "北京"}
  ],
  "aggregations": [
    {"column": "订单ID", "func": "count", "alias": "订单数"}
  ]
}
```

### 9. 范围筛选

**用户问题**："金额大于1000的订单"

**查询JSON**：
```json
{
  "filters": [
    {"column": "订单金额", "operator": ">", "value": 1000}
  ],
  "sort": [{"column": "订单金额", "asc": false}],
  "limit": 50
}
```

### 10. 多条件筛选

**用户问题**："北京最近7天的新增用户"

**查询JSON**：
```json
{
  "filters": [
    {"column": "城市", "operator": "==", "value": "北京"},
    {"column": "日期", "operator": ">=", "value": "7天前"}
  ],
  "groupby": ["日期"],
  "aggregations": [
    {"column": "新增用户", "func": "sum", "alias": "新增用户"}
  ],
  "sort": [{"column": "日期", "asc": true}]
}
```

## 支持的运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `==` | 等于 | `{"column": "城市", "operator": "==", "value": "北京"}` |
| `!=` | 不等于 | `{"column": "状态", "operator": "!=", "value": "已删除"}` |
| `>` | 大于 | `{"column": "金额", "operator": ">", "value": 1000}` |
| `<` | 小于 | `{"column": "年龄", "operator": "<", "value": 18}` |
| `>=` | 大于等于 | `{"column": "日期", "operator": ">=", "value": "2024-01-01"}` |
| `<=` | 小于等于 | `{"column": "日期", "operator": "<=", "value": "昨天"}` |
| `contains` | 包含 | `{"column": "产品名", "operator": "contains", "value": "手机"}` |

## 支持的聚合函数

| 函数 | 说明 | 适用场景 |
|------|------|----------|
| `sum` | 求和 | 销售额、用户数等 |
| `mean` | 平均值 | 客单价、平均年龄等 |
| `count` | 计数 | 订单数、记录数等 |
| `max` | 最大值 | 最高销量、最高金额等 |
| `min` | 最小值 | 最低价格、最早日期等 |

## 时间表达式

查询中可直接使用以下时间表达式，脚本会自动解析：

| 表达式 | 含义 |
|--------|------|
| `今天` | 当前日期 |
| `昨天` | 昨天日期 |
| `N天前` | N天前的日期 |
| `本周` | 本周第一天（周一） |
| `上周` | 上周第一天 |
| `本月` | 本月第一天 |
| `上月` | 上月第一天 |

## 追问模式处理

### 上下文继承

用户首次查询："最近7天新增用户趋势"  
追问："那上周呢？"  
→ 自动将时间范围改为"上周"

用户首次查询："各城市的销售额"  
追问："按渠道看看？"  
→ 将分组维度从"城市"改为"渠道"

用户首次查询："总销售额是多少？"  
追问："平均值呢？"  
→ 将聚合函数从"sum"改为"mean"

### 追问关键词映射

| 追问关键词 | 操作 |
|-----------|------|
| "上周/上月/昨天" | 调整时间范围 |
| "按XX看/按XX分组" | 调整分组维度 |
| "平均值/均值" | 改为mean聚合 |
| "总计/总和" | 改为sum聚合 |
| "有多少/计数" | 改为count聚合 |
| "最高/最大" | 改为max聚合 + 降序排序 |
| "最低/最小" | 改为min聚合 + 升序排序 |
