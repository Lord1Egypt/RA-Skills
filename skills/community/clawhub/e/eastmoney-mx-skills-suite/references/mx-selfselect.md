# mx_self_select - 妙想自选股管理

通过自然语言查询或操作东方财富通行证账户下的自选股数据，接口返回 JSON 格式内容。

## 功能列表

- 查询自选股列表
- 添加指定股票到自选股列表
- 从自选股列表中删除指定股票

## API 接口

### 查询接口

- **URL**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get`
- **Header**: `apikey: {MX_APIKEY}`, `Content-Type: application/json`
- **Body**: `{}`

### 管理接口（添加/删除）

- **URL**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage`
- **Header**: `apikey: {MX_APIKEY}`, `Content-Type: application/json`
- **Body**: `{"query": "自然语言指令"}`

## 使用方式

### Python 调用

```python
import requests, os

headers = {
    "Content-Type": "application/json",
    "apikey": os.getenv("MX_APIKEY")
}

# 查询自选股
response = requests.post(
    "https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get",
    headers=headers, json={}, timeout=30
)

# 添加自选股
response = requests.post(
    "https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage",
    headers=headers, json={"query": "把贵州茅台添加到我的自选股列表"}, timeout=30
)

# 删除自选股
response = requests.post(
    "https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage",
    headers=headers, json={"query": "把贵州茅台从我的自选股列表删除"}, timeout=30
)
```

也可直接使用本套件提供的脚本 `scripts/mx_self_select.py`：

```bash
# 查询自选股
python scripts/mx_self_select.py query

# 添加自选股
python scripts/mx_self_select.py add "贵州茅台"

# 删除自选股
python scripts/mx_self_select.py delete "贵州茅台"

# 自然语言
python scripts/mx_self_select.py "把贵州茅台加入自选"
python scripts/mx_self_select.py "查询我的自选股列表"
```

## 查询结果字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `SECURITY_CODE` | 字符串 | 股票代码 |
| `SECURITY_SHORT_NAME` | 字符串 | 股票名称 |
| `NEWEST_PRICE` | 数字 | 最新价(元) |
| `CHG` | 数字 | 涨跌幅(%) |
| `PCHG` | 数字 | 涨跌额(元) |
| `010000_TURNOVER_RATE` | 数字 | 换手率(%) |
| `010000_LIANGBI` | 数字 | 量比 |

## 输出示例

### 查询自选股成功

```
我的自选股列表
================================================================================
股票代码 | 股票名称 | 最新价(元) | 涨跌幅(%) | 涨跌额(元) | 换手率(%) | 量比
--------------------------------------------------------------------------------
600519   | 贵州茅台 | 1850.00    | +2.78%    | +50.00     | 0.35%     | 1.2
300750   | 宁德时代 | 380.00     | -1.25%    | -4.80      | 0.89%     | 0.9
================================================================================
共 2 只自选股
```

### 添加/删除成功

```
操作成功：贵州茅台已添加到自选股列表
```

## 错误处理

- 未配置 API Key：提示设置环境变量 `MX_APIKEY`
- 接口调用失败：显示错误信息
- 数据为空：提示用户到东方财富 App 查询
