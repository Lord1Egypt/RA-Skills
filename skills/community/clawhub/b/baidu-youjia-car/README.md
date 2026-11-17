# baidu-youjia-car

百度有驾出品。一句话查询汽车品牌、车系、车型详情、价格行情、经销商信息。提供手机号验证码获取 Key + 手动配置双重方式，开箱即用。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/baidu/baidu-youjia-car)

---

## ✨ 能力一览

| 能力 | 说明 | 方法 |
|:-----|:-----|:-----|
| 🚗 汽车价格查询 | 查询车型价格、经销商报价、降价信息、落地价、车主成交价 | `ask_price` |

## 🚀 快速开始

### 安装依赖

```bash
pip install -e .
```

> 仅依赖 `requests`，多数环境已自带。

### 基本用法

```python
from youjia_client import YoujiaClient

client = YoujiaClient()

# 查询汽车价格
data = client.ask_price("奥迪A4L多少钱")

# 指定城市查询
data = client.ask_price("宝马3系报价", city="上海")

# 格式化为 Markdown 输出
print(YoujiaClient.format_for_reply(data))
```

### 配置 Key

未配置 Key 时可通过手机号验证码流程获取 Key。如已有百度有驾 Key：

```python
from youjia_client import save_key_to_dotenv

save_key_to_dotenv("sk-xxxxxxxxxxxxx")  # 持久化到 .env，之后自动生效
```

或手动编辑 `.env` 文件：

```bash
cp .env.example .env
# 编辑 .env，填入你的 Key
```

## 📖 API 参考

### `ask_price(query, city="北京")`

查询汽车价格、经销商报价、降价信息、落地价、车主成交价等。

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `query` | str | ✅ | 查询内容，必须包含车系名称（如"奥迪A4L多少钱"） |
| `city` | str | | 查询城市，默认"北京" |

**返回**：`{ResultCode, Result: {car_info, advertise_price_info, ...}, ResultMsg, QueryID}`

**辅助方法**：`YoujiaClient.format_for_reply(result)` 将返回结果渲染为可直接发送给用户的 Markdown。

## 📁 项目结构

```
baidu-youjia-car/
├── SKILL.md                          # Skill 定义与使用说明
├── scripts/
│   ├── send_code.py / create_key.py / save_config.py  # Key 配置工具
│   ├── youjia_client.py              # 核心客户端（API 封装）
│   └── test_all.py                   # 测试套件
├── references/
│   ├── agent-notes.md                # AI 调用指引
│   └── apikey-fetch.md               # Key 配置指南
├── setup.py                           # pip install -e . 安装入口
├── .env.example                      # 环境变量模板
├── tempkey-guide.md                  # Key 申请指南
└── README.md                         # 本文件
```

## 🔑 Key 策略

| 场景 | 行为 |
|:-----|:-----|
| 未配置 Key | 可通过手机号验证码获取 Key，或手动配置 `YOUJIA_API_KEY` |
| 已配置 Key | 使用配置的 Key（`X-Youjia-OpenAPI-Key` 请求头） |
| Key 优先级 | 传入参数 → 环境变量 `YOUJIA_API_KEY` → `.env` 文件 → `~/.youjia/key.json` |
