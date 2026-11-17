# 国家贸易概览-美国进口交易 API 参考

> 按州或城市维度返回美国进口交易统计，包含进口记录数、集装箱数及近90天数据，支持游标分页。
> 接口路径：`POST /agent/customs/overview/us-import`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | 查询类型：state=按州，city=按城市 |
| cursor | string | 否 | 游标（base64 编码的 {"start":N}） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：美国进口交易数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（base64 编码） |
| list | array | 美国进口交易列表 |

### list 条目字段

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 州名或城市名 |
| records | integer | 进口记录数 |
| recordsLast90Days | integer | 近90天进口记录数 |
| containers | integer | 集装箱数 |
| containersLast90Days | integer | 近90天集装箱数 |
