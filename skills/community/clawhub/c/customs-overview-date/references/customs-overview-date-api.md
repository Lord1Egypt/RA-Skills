# 国家贸易概览-日期相关 API 参考

> 返回去年年份、上月月份、去年当月月份等日期参考信息（无业务请求参数）。
> 接口路径：`POST /agent/customs/overview/date`

## python脚本参数

- `--params`：JSON格式的查询参数（必填，可传空对象 {}）

## API请求参数

该接口无业务请求参数，传空对象 `{}` 即可。

## 响应数据

### 外层结构

- code（integer）：响应码，0 表示成功
- msg（string）：响应消息
- data：日期参考数据（见下）
- fee：计费信息（apiCost 本次扣费、accountBalance 账户余额、uuid 调用标识）

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| yesteryear | integer | 去年年份，如 2025 |
| lastMonth | integer | 上月月份，如 202604 |
| yesteryearMonth | integer | 去年当月月份，如 202504 |
