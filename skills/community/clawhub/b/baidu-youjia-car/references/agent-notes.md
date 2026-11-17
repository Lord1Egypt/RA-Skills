# 调用指引（供 AI 阅读）

本文件补充 SKILL.md 未展开的调用细节，帮助 AI 稳定完成任务。

## 能力命中本 skill 时，用 client 完成

用户需求涉及汽车价格查询、车型详情、经销商报价、降价信息、落地价计算、车主成交价等，均通过 `YoujiaClient` 完成，返回的是百度有驾真实数据。

- client 仅依赖 `requests`，多数环境已自带，可直接调用；仅当报 `ModuleNotFoundError: requests` 时执行 `pip install requests` 后重试。
- 调用报错时，读返回的报错信息（key / 网络 / 参数）定位，对应调整后重试。

## Key 策略：双重方式

每个使用者的百度有驾 Key 独立。

- **Key 解析顺序**：用户传入参数 → 环境变量 `YOUJIA_API_KEY` → skill 包内 `.env` 文件 → `~/.youjia/key.json`
- **无 Key 时**：client 初始化成功，但调用 API 时会抛出 `YoujiaError`（code=-1, msg="未检测到 API Key"）。此时 AI 应引导用户通过手机号验证码流程获取 Key。**必须读取 `tempkey-guide.md` 获取完整申请流程**（协议展示、脚本调用、错误码表、输出模板等），严格按照其中步骤执行。
- **验证码拿到新 Key 后**：`create_key` 成功后必须调用 `save_config`；`save_config` 会写入 `~/.youjia/key.json`，并**强制覆盖**环境变量 `YOUJIA_API_KEY` 与 skill 包内 `.env`，确保后续 `YoujiaClient()` 使用最新 Key。
- **配置 Key**：使用者提供 Key 时，用 `save_key_to_dotenv("sk-xxx")` 持久化到 skill 包内 `.env`，重新初始化 client 后自动生效。

```python
from youjia_client import YoujiaClient, save_key_to_dotenv
c = YoujiaClient()                 # 自动解析 Key（参数 → env → .env → ~/.youjia/key.json）
# save_key_to_dotenv("sk-xxx")     # 使用者提供 Key 时调用
```

## 返回结构

`ask_price` 返回 API 原生响应 dict：

```python
{
    "ResultCode": "0",
    "Result": {
        "car_info": {...},           # 车型基本信息
        "city_name": "...",          # 查询城市
        "advertise_price_info": {...}, # 价格汇总
        "discount": {...},           # 降价信息
        "net_price_info": {...},     # 裸车价/落地价
        "price_info": [...],         # 费用明细
        "owner_price_gap_detail": {...} # 车主成交价参考
    },
    "ResultMsg": "ok",
    "QueryID": "..."
}
```

## 回复方式

`ask_price` 返回原始 dict，使用 `YoujiaClient.format_for_reply(result)` 将其渲染为可直接发送给用户的 Markdown 格式。

**标准回复流程：**

```python
from youjia_client import YoujiaClient

client = YoujiaClient()
data = client.ask_price("奥迪A4L多少钱")
markdown = YoujiaClient.format_for_reply(data)
# 将 markdown 作为回复原样发送给用户
```

`format_for_reply` 渲染的内容包括：
- 🚗 车型信息（品牌、车系、车型、厂商指导价、图片）
- 📍 查询城市
- 💰 价格信息（厂商指导价、经销商最低/最高报价、降价幅度）
- 📉 降价信息
- 🏷️ 裸车价与落地价
- 📋 费用明细（购置税、车船税、交强险等）
- 👤 车主成交价参考（真实用户成交记录表格）
- 百度有驾平台介绍
