# get-judicial-sale - 司法拍卖信息

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| auctionName | string | 拍卖名称 |
| caseNo | string | 案号 |
| dealOrgName | string | 处置单位名称 |
| dataJudicialAuctionId | string | 司法拍卖ID |
| startPrice | integer | 起拍价（单位：分，换算需÷100才是元）|
| evaluationPrice | integer | 评估价（单位：分，换算需÷100才是元）|
| auctionTime | string | 拍卖时间段 |

## 特殊说明

- 金额字段单位为分，展示时需 ÷100 换算为元