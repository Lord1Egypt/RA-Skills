---
name: ax-publish-goods
description: 翱象（淘宝闪购）发品接口，支持批量创建商品。Use when: (1) 需要调用翱象发品接口创建商品, (2) 需要生成翱象API签名, (3) 需要批量发布商品到淘宝闪购。
---

# 翱象发品接口

对接翱象（淘宝闪购）零售开放平台，实现商品批量创建功能。

## 快速开始

### Python 版本

```python
from scripts.aoxiang_publish import AoxiangPublishClient

# 创建客户端
client = AoxiangPublishClient(
    app_key="???",
    secret="???"
)

# 构建商品列表
sku_list = [
    {
        "sku_name": "可口可乐 330ml",
        "inventory_unit": "瓶",
        "sku_code": "COLA330001",
        "barcodes": ["6901234567890"],
        "specification": "330ml",
        "sale_price": "350"  # 单位：分
    }
]

# 调用接口
result = client.create_goods(
    merchant_code="ERP_ACCESS_TEST",
    erp_store_code="ERP_NORMAL",
    sku_list=sku_list
)

# 处理结果
if result["body"]["errno"] == 0:
    print("发品成功!")
else:
    print(f"失败: {result['body']['error']}")
```

### 命令行使用

```bash
# 使用默认示例数据
python3 scripts/aoxiang_publish.py

# 自定义参数
python3 scripts/aoxiang_publish.py "MERCHANT_CODE" "STORE_CODE" '[{"sku_name":"商品","inventory_unit":"个","sku_code":"SKU001","barcodes":["123"],"specification":"规格","sale_price":"100"}]'
```

## API 参数说明

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cmd | string | 是 | 固定值: `saas.sku.create.goods.batch` |
| source | string | 是 | AppKey |
| secret | string | 是 | 用于签名，不传参只用于签名计算 |
| ticket | string | 是 | 随机生成的UUID格式字符串 |
| timestamp | string | 是 | 10位时间戳 |
| version | string | 是 | 固定值: `3` |
| encrypt | string | 是 | 固定值: 空字符串 `""` |
| body | string | 是 | JSON格式的业务参数 |
| sign | string | 是 | MD5签名（大写） |

### Body 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| merchant_code | string | 是 | 商家编码 |
| erp_store_code | string | 是 | 门店编码 |
| sku_list | array | 是 | 商品列表 |

### SKU 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sku_name | string | 是 | 商品名称 |
| inventory_unit | string | 是 | 库存单位（个/瓶/盒等） |
| sku_code | string | 是 | 商品编码（唯一） |
| barcodes | array | 是 | 条码列表 |
| specification | string | 是 | 规格 |
| sale_price | string | 是 | 售价（单位：**分**） |

## 签名算法

1. 构建签名参数（按 key 字母顺序排序）：
   - body, cmd, encrypt, secret, source, ticket, timestamp, version

2. 拼接成字符串：
   ```
   key1=value1&key2=value2&...
   ```

3. MD5 加密，转大写32位

## 响应格式

```json
{
    "body": {
        "errno": 0,
        "data": null,
        "error": "success"
    },
    "cmd": "resp.saas.sku.create.goods.batch",
    "encrypt": "",
    "sign": "...",
    "source": "41389872",
    "ticket": "...",
    "timestamp": 1234567890,
    "traceid": "...",
    "version": "3"
}
```

- `errno: 0` 表示成功
- `errno != 0` 表示失败，错误信息在 `error` 字段

## 注意事项

1. **价格单位是"分"**，不是元（3.5元 = 350分）
2. **sku_code 必须唯一**
3. **ticket** 是随机生成的UUID格式（带减号）
4. **timestamp** 是10位时间戳（秒级）
5. **body** 需要转为JSON字符串参与签名

## 文件列表

- `scripts/aoxiang_publish.py` - Python 客户端
- `REFERENCE.md` - Java 参考实现
