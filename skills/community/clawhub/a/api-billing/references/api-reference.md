# API 账单查询接口参考

## 火山引擎

### 余额查询
- **API**: QueryBalanceAcct
- **版本**: 2022-01-01
- **服务**: billing
- **地址**: https://open.volcengineapi.com
- **签名**: V4 HMAC-SHA256

### 历史账单
- **API**: ListBillOverviewByCategory
- **参数**: BillPeriod=YYYY-MM
- **返回**: 折后价、原价、优惠券、应付金额

## 阿里云

### 余额查询
- **API**: QueryAccountBalance
- **服务**: bssopenapi
- **地址**: business.aliyuncs.com
- **SDK**: aliyun-python-sdk-bssopenapi

### 历史账单
- **API**: QueryBillOverview
- **参数**: BillingCycle=YYYY-MM
- **返回**: 各产品消费明细

### 账单明细
- **API**: QueryInstanceBill
- **参数**: BillingCycle=YYYY-MM

## DeepSeek

- **API**: GET https://api.deepseek.com/user/balance
- **认证**: Bearer Token

## MiniMax

- **API**: GET https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains
- **认证**: Bearer Token (Coding Plan Key)

## OpenRouter

- **API**: GET https://openrouter.ai/api/v1/credits
- **认证**: Bearer Token

## 凭证格式

### 火山引擎
```
VOLC_ACCESS_KEY_ID=AKLTMmFkNTM5MmNlY2ZlNDFhNzhhNGQyNDg5ODhmOTA4OGY
VOLC_SECRET_KEY=WldRMFpEUTBPV0ppT0RVd05HVmxZbUptWW1VNFlXRmxNV0U0WlRjek1UZw==
```
注意: SecretKey 无需 Base64 解码，直接使用

### 阿里云
```
ALIYUN_ACCESS_KEY_ID_B64=TFRBSTV0U2NuaHdMelk2YWgycEt1RWdY
ALIYUN_ACCESS_KEY_SECRET_B64=dlF4RjVqRUVqcE1zMDNWWUV2c0xIRG5VZDByWXps
```
