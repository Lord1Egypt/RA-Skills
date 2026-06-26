---
name: baidu-youjia-car
description: 查询汽车品牌、车系、车型详情、价格行情、经销商信息、排行榜数据等。当用户问"奥迪A4L多少钱？""宝马最近成交价是多少？""奥迪A4L附近经销商""或类似汽车查询问题时，使用本技能。支持按城市查询经销商报价、降价信息、保险成本等完整车型信息。
metadata: { "openclaw": { "emoji": "🚗",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Baidu Youjia Car (百度有驾汽车查询)

通过百度有驾 API 查询汽车价格、经销商报价、降价信息、购置税、保险费用等完整购车信息。

## Prerequisites

### API Key Configuration
This skill requires a **BAIDU_API_KEY** to be configured in OpenClaw.

If you don't have an API key yet, please visit:
**https://console.bce.baidu.com/qianfan/ais/console/apiKey**

For detailed setup instructions, see:
[references/apikey-fetch.md](references/apikey-fetch.md)

## Usage

```bash
python3 skills/baidu-youjia-car/scripts/askprice.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | 汽车查询内容，必须包含车系名称（如"奥迪A4L多少钱"、"宝马3系报价"） |
| city | str | no | 北京 | 查询城市，用于获取当地经销商报价（如"上海"、"广州"） |

## Examples

```bash
# 基本查询 - 查询奥迪A4L价格
python3 scripts/askprice.py '{"query":"奥迪A4L多少钱"}'

# 指定城市查询
python3 scripts/askprice.py '{"query":"宝马3系报价","city":"上海"}'

# 查询降价信息
python3 scripts/askprice.py '{"query":"奔驰C级优惠多少"}'

# 查询落地价
python3 scripts/askprice.py '{"query":"特斯拉Model 3落地价","city":"深圳"}'
```

## Response Fields

API 返回的主要信息包括：

| Field | Description |
|-------|-------------|
| car_info | 车系基本信息（品牌、车系、车型、图片等） |
| advertise_price_info | 价格汇总（厂商指导价、经销商最低/最高报价、降价幅度） |
| discount | 降价/直降信息 |
| min_reference_price | 最低经销商报价 |
| net_price_info | 裸车价、落地价 |
| price_info | 费用明细（购置税、车船税、交强险等） |
| owner_price_gap_detail | 车主成交价参考（真实用户成交记录） |
| city_name | 查询城市 |

## Output Format

The script outputs formatted results including:
- 车型基本信息（品牌、车系、车型名称）
- 厂商指导价
- 经销商最低报价 / 最高报价
- 降价幅度
- 裸车价 / 落地价
- 购置税、车船税、交强险等费用
- 车主成交价参考记录
- 百度有驾平台介绍

## Important Notes

- **query 必须包含车系名称**，API 通过车系名识别具体车型
- city 参数可选，默认为"北京"，不同城市的经销商报价可能不同
- 返回的价格数据为实时数据，会随市场变化更新
- Authorization header 中只需要 API Key

## Current Status

Fully functional.
