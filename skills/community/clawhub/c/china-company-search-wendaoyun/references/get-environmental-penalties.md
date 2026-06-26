# get-environmental-penalties - 环保处罚

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchKey | string | 是 | 企业全称 |
| pageNum | integer | 否 | 页码，默认 1 |
| pageSize | integer | 否 | 每页条数，默认 10，最大 20 |

## 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| punishBehavior | string | 违法事实 |
| punishAmount | integer | 处罚金额（单位：分） |
| punishInstitution | string | 作出处罚单位名称 |
| publishDate | string | 发布日期 |
| punishDate | string | 处罚日期 |
| punishNumber | string | 环保处罚决定书文号 |

## 特殊说明

- `punishAmount` 单位为分，展示时需 ÷100 换算为元