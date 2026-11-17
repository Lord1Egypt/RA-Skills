---
name: baidu-youjia-car
description: "百度有驾·汽车查询 Skill，一句话查询汽车品牌、车系、车型详情、价格行情、经销商信息。提供手机号验证码获取 Key + 手动配置双重方式，开箱即用。涉及汽车价格、降价信息、落地价计算、车主成交价参考等购车场景时使用。"
license: MIT
version: 1.1.0
git_url: https://github.com/baidu/baidu-youjia-car
display_name: "百度有驾汽车查询"
display_name_en: "Baidu Youjia Car Query"
description_zh: "一句话查询汽车品牌、车系、车型详情、价格行情、经销商信息、降价幅度、落地价计算、车主成交价参考。支持按城市查询当地经销商报价。"
description_en: "Query car brands, series, model details, price trends, dealer info, and transaction price references with natural language."
visibility: "public"
---

# 百度有驾汽车查询 Skill

百度有驾出品。用一句自然语言即可查询汽车价格、车型详情、经销商报价、降价信息、落地价计算和车主成交价参考。

## 能力

| 能力 | 说明 | 方法 |
|------|------|------|
| 汽车价格查询 | 查询车型价格、经销商报价、降价信息、落地价、车主成交价 | `ask_price` |

## 安装

首次使用前安装：

```
pip install -e .
```

## 用法

```python
from youjia_client import YoujiaClient

client = YoujiaClient()

result = client.ask_price("奥迪A4L多少钱", city="北京")
```

配置自己的百度有驾 Key（持久化到 `.env`，之后自动启用）：

```python
from youjia_client import save_key_to_dotenv

save_key_to_dotenv("sk-xxxxxxxxxxxxx")
```

## Key 检查

1. 已有 Key（用户传入 `YoujiaClient(key=...)`、环境变量 `YOUJIA_API_KEY`、skill 包内 `.env` 文件或 `~/.youjia/key.json`）→ 直接使用

2. 未检测到 Key 时向用户输出以下选项：

   > - **申请 Key（推荐）**：手机号验证即可获取
   > - **手动配置 Key**：通过环境变量 `YOUJIA_API_KEY` 或 `.env` 文件配置

3. 用户选择"申请 Key" → 读取 `tempkey-guide.md` 按其中步骤执行；验证码校验通过后，新 Key 会覆盖本地 `YOUJIA_API_KEY` 环境变量与 skill 包内 `.env`

## 参数与返回

### 汽车价格查询 — ask_price

`ask_price(query, city="北京")`：查询汽车品牌、车系、车型详情、经销商报价、降价信息、落地价、车主成交价等。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | str | 是 | 查询内容，必须包含车系名称（如"奥迪A4L多少钱"、"宝马3系报价"） |
| `city` | str | 否 | 查询城市，用于获取当地经销商报价，默认"北京" |

**返回**：API 原生响应 dict，包含 `car_info`（车型信息）、`advertise_price_info`（价格汇总）、`discount`（降价信息）、`net_price_info`（裸车价/落地价）、`price_info`（费用明细）、`owner_price_gap_detail`（车主成交价参考）等字段。

**辅助方法**：`YoujiaClient.format_for_reply(result)` 将返回结果渲染为可直接发送给用户的 Markdown 格式。

## 使用要点

1. **Key**：未配置 Key 时按"Key 检查"流程处理；如已有 Key，用 `save_key_to_dotenv` 配置后稳定性更佳
2. **query 必须包含车系名称**，API 通过车系名识别具体车型
3. **city 参数可选**，不同城市的经销商报价可能不同
4. **返回的价格数据为实时数据**，会随市场变化更新

## 示例

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

> 调用细节、Key 流程等见 `references/`。
