# 维护者 / 联调配置（勿展示给用户）

本文档仅供安装、排障的 Agent 或开发者阅读。**禁止**将下列环境变量名、deve 域名片段写入用户聊天、下载附件或 `userView`。

## 网关（config.py）

在 `config.py` 中修改：

```python
EXPORT_BASE_URL = "https://flight-deve.flightroutes24.com"
GRAY_HEADER = "ww"
```

## 采购密钥（系统环境变量）

```powershell
$env:FR_NEWAPI_APPKEY='你的APPKEY'
$env:FR_NEWAPI_SIGN_SECRET='你的SHA512签名密钥'
$env:FR_NEWAPI_AES_SECRET='你的16字节AES密钥'
```

## deve 联调可选（仅测试环境）

```powershell
$env:FR_NEWAPI_SKIP_IP_WHITELIST='1'
$env:FR_NEWAPI_SKIP_AUTH='1'
```

## 全流程自动化测试

```bash
pip install -r requirements.txt
set FR_BOOKING_TEST_ORDER=1
python scripts/booking_flow_test.py
```

可选：`FR_BOOKING_TEST_QUERY`、`FR_BOOKING_TEST_PAX` 覆盖默认查询与乘客文本。
