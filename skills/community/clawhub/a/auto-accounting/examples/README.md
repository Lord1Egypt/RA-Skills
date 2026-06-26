# 示例数据

本目录包含自动记账 Skill 的测试示例数据。

## 示例说明

### 支付平台

| 文件 | 说明 |
|------|------|
| wechat_pay.json | 微信支付截图示例 |
| alipay.json | 支付宝账单示例 |

### 购物平台

| 文件 | 说明 |
|------|------|
| jd_order.json | 京东订单示例 |
| taobao_order.json | 淘宝订单示例 |
| pdd_order.json | 拼多多订单示例 |

### 外卖平台

| 文件 | 说明 |
|------|------|
| meituan_order.json | 美团外卖订单示例 |
| eleme_order.json | 饿了么订单示例 |

## 使用方式

这些示例数据用于测试记账解析器的识别能力。

```python
from scripts.accounting_parser import AccountingParser

parser = AccountingParser()

# 加载示例数据
with open('examples/wechat_pay.json') as f:
    data = json.load(f)
    
result = parser.parse_image_result(data['text'])
print(result)
```
