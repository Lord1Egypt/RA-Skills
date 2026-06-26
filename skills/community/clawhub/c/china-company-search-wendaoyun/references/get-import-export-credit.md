# get-import-export-credit - 海关进出口信用信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| identifyCode | string | 认证证书编码 |
| creditLevel | string | 信用等级 |
| eCommerceType | string | 跨境贸易电子商务类型 |
| industryType | string | 行业种类 |
| validityDate | string | 报关有效期 |
| annualReport | string | 年报情况 |
| cancelFlag | string | 海关注销标志 |
| specialArea | string | 特殊贸易区域 |
| economicArea | string | 经济地区 |
| area | string | 行政地区 |
| regCode | string | 海关注册编码 |
| regDate | string | 注册日期（如 "2022-01-01"） |
| busType | string | 经营类别 |
| regGov | string | 注册海关 |