# 1688 API 接口文档

## 商品榜单接口

### 请求地址
```
POST https://gw.open.1688.com/openapi/param2/1/com.alibaba.fenxiao.crossborder/product.topList.query/${APPKEY}
```

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| rankId | string | 是 | 榜单ID/类目ID |
| type | string | 否 | 榜单类型：complex(综合榜)/hot(热卖榜)/goodPrice(好价榜) |
| limit | string | 否 | 返回商品数量，1-20，默认10 |
| language | string | 否 | 语言代码，默认en |
| access_token | string | 是 | 访问令牌 |
| sign | string | 是 | 签名 |

### 响应示例
```json
{
  "result": {
    "rankProductModels": [
      {
        "itemId": "1022110124099",
        "title": "商品标题",
        "translateTitle": "Product Title",
        "imgUrl": "https://example.com/image.jpg",
        "sort": 1,
        "buyerNum": 100,
        "soldOut": 1000,
        "goodsScore": "5.0"
      }
    ]
  }
}
```

### 商品榜单字段说明
| 字段 | 说明 |
|------|------|
| `itemId` | **商品ID**（1688商品唯一标识）|
| `title` | 商品中文标题 |
| `translateTitle` | 商品英文翻译标题 |
| `imgUrl` | 商品主图URL |
| `sort` | 排名序号 |
| `buyerNum` | 买家数量 |
| `soldOut` | 销量 |
| `goodsScore` | 商品评分 |

## 热搜词接口

### 请求地址
```
POST https://gw.open.1688.com/openapi/param2/1/com.alibaba.fenxiao.crossborder/product.search.topKeyword/${APPKEY}
```

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sourceId | string | 是 | 类目ID |
| country | string | 否 | 国家/语言代码 |
| type | string | 否 | 热搜类型，固定为cate |
| access_token | string | 是 | 访问令牌 |
| sign | string | 是 | 签名 |

### 响应示例
```json
{
  "result": {
    "keywords": [
      {
        "keyword": "hot keyword",
        "searchCount": 10000
      }
    ]
  }
}
```

## 签名规则

1. 将所有请求参数（除sign外）按key的字母顺序排序
2. 将排序后的参数拼接成字符串：`key1value1key2value2...`
3. 在拼接字符串末尾追加AppSecret
4. 对结果进行MD5加密，并转换为大写

## 错误码

| 错误码 | 说明 |
|--------|------|
| 25 | 签名错误 |
| 401 | 未授权/Token无效 |
| 400 | 参数错误 |
| 403 | 无权限调用 |