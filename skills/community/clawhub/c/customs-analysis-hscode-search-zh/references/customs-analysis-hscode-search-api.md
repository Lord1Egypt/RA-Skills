# 分析报告-HS编码搜索 API 参考

> 根据产品名称和HS编码关键字搜索匹配的HS编码列表。
> 接口路径：`POST /agent/customs/analysis/hscode/search`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product | string | 是 | 产品名称，如"milk powder" |
| hscode | string | 是 | HS编码关键字，如"0402" |
| cursor | string | 否 | 分页游标（base64 编码） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：HS编码搜索结果（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| cursor | string | 下一页游标（base64 编码） |
| list | array[string] | HS编码列表，如["04021000","04022100"] |
