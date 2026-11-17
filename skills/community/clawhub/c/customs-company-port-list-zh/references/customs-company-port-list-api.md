# 公司贸易港口列表 API 参考

> 根据公司ID获取公司贸易的港口列表数据（支持游标分页）。
> 接口路径：`POST /agent/customs/company/port/list`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| companyId | integer | 是 | 公司ID |
| companyType | integer | 是 | 公司类型（1：供应商，2：采购商） |
| cursor | string | 否 | 分页游标 |
| dateStart | integer | 否 | 开始时间（毫秒级时间戳） |
| dateEnd | integer | 否 | 结束时间（毫秒级时间戳） |
| products | array[string] | 否 | 产品名称列表 |
| hscodes | array[string] | 否 | HS编码列表 |
| countryCodes | array[string] | 否 | 国家代码列表 |
| port | string | 否 | 港口名称 |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：港口列表数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（无更多数据时不返回） |
| list | array | 港口列表 |

### list 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| port | string | 港口名称 |
| tradeCount | integer | 交易次数 |
| percentTrade | number | 贸易占比（%） |
| amount | integer | 金额 |
| quantity | integer | 数量 |
| weight | integer | 重量 |
