# 基本资料数据查询接口文档

## 接口概述

查询全品类标的（股票、指数、基金、期货、期权、转债、债券、理财、保险等）的基础信息、发行主体、机构资料、费率、上市地点、上市日期等静态信息，支持自然语言问句输入，返回相关金融数据结果。

## 基本信息

| 字段 | 值 |
|------|-----|
| 接口地址 | `https://openapi.iwencai.com/v1/query2data` |
| 请求方式 | POST |
| 认证方式 | API Key |
| Content-Type | application/json |

## 认证

请求头中需携带 API Key：

```
Authorization: Bearer {IWENCAI_API_KEY}
```

环境变量：`IWENCAI_API_KEY`

## 请求参数

### Headers

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | STRING | 是 | Bearer {IWENCAI_API_KEY} |
| Content-Type | STRING | 是 | application/json |

### Body

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| query | STRING | 是 | 用户问句，例如："同花顺上市日期？" |
| source | STRING | 否 | 来源，默认值：test |
| page | STRING | 否 | 分页参数，默认值：1 |
| limit | STRING | 否 | 分页参数，默认值：10 |
| is_cache | STRING | 否 | 缓存参数，默认值：1 |

### 请求示例

```json
{
  "query": "同花顺上市日期？",
  "source": "test",
  "page": "1",
  "limit": "10",
  "is_cache": "1"
}
```

## 响应参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| datas | ARRAY | 金融数据列表，接口返回的金融数据数组 |

### 响应示例

**查询：同花顺上市日期？**

```json
{
  "datas": [
    {
      "股票代码": "300033.SZ",
      "股票简称": "同花顺",
      "上市日期": "20091225"
    }
  ]
}
```

## 调用示例

```python
import os
import urllib.request
import json

url = "https://openapi.iwencai.com/v1/query2data"
headers = {
    "Authorization": f"Bearer {os.environ['IWENCAI_API_KEY']}",
    "Content-Type": "application/json"
}
payload = {
    "query": "同花顺上市日期？",
    "source": "test",
    "page": "1",
    "limit": "10",
    "is_cache": "1"
}

data = json.dumps(payload).encode("utf-8")
request = urllib.request.Request(url, data=data, headers=headers, method="POST")
response = urllib.request.urlopen(request, timeout=30)
result = json.loads(response.read().decode("utf-8"))
print(result.get("datas", []))
```

## 使用说明

- 将用户的自然语言问题直接作为 `query` 参数传入。
- 返回的 `datas` 字段为对象数组，根据查询内容不同，返回不同的字段列表。
- `source` `page` `limit` `is_cache` 均为可选参数，使用默认值即可。
- 环境变量 `IWENCAI_API_KEY` 为鉴权密钥，需提前配置。
