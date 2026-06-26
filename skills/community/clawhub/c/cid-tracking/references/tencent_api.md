# 腾讯广点通 API 参考

## 认证方式

### 签名算法

腾讯广告 API 使用 HMAC-SHA256 签名：

```python
import hashlib
import hmac
import time

def generate_signature(params, secret_key):
    sorted_params = sorted(params.items())
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
    signature = hmac.new(
        secret_key.encode(),
        query_string.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature.upper()
```

## API 端点

### 获取广告计划数据

```
POST https://e.qq.com/v1.0/report
```

**请求头:**
```json
{
  "Content-Type": "application/json",
  "Access-Token": "YOUR_ACCESS_TOKEN"
}
```

**请求体:**
```json
{
  "account_id": "123456",
  "report_type": "CAMPAIGN",
  "date_range": {
    "start_date": "2026-03-20",
    "end_date": "2026-03-20"
  },
  "metrics": ["impression", "click", "cost", "conversion"],
  "group_by": ["campaign_id", "campaign_name"]
}
```

## 转化回传

⚠️ **待实现** - 需要实现完整的签名算法

参考文档：https://e.qq.com/dev/

## 注意事项

1. 腾讯广告 API 需要完整的签名流程
2. 建议先申请 API 测试权限
3. 签名时效性：5 分钟

## 文档链接

https://e.qq.com/dev/
