# 分析报告-HS编码详情 API 参考

> 根据HS编码查询其详细描述信息（中英文）。
> 接口路径：`POST /agent/customs/analysis/hscode/detail`

## python脚本参数

- `--params`：JSON格式的查询参数（必填）

## API请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hscode | string | 是 | HS编码，如"04021000" |
| cursor | string | 否 | 分页游标（base64 编码） |

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：HS编码详情（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| hscode | string | HS编码 |
| descZh | string | 中文描述，如"脂肪含量<=1.5%的固状乳及奶油" |
| descEn | string | 英文描述，如"Milk and cream in solid forms, fat content <= 1.5%" |
