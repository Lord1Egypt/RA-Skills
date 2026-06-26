---
name: coffee-prices
description: Fetch and compare mainstream coffee prices (latte, americano, etc.) from major chains like Starbucks, Luckin, and Cotti for a given Chinese city and output them as a table. Use when the user wants current city coffee pricing benchmarks or brand comparisons.
---

# Coffee Prices by City

获取当前城市主流连锁品牌咖啡（如星巴克、瑞幸、库迪等）的代表性品类（拿铁、美式等）价格，并以表格形式输出，方便横向对比。

> ⚠️ 说明：本技能内置的是按城市分级的「参考价」，适合作为对比和定价参考，不保证与每家门店实时售价完全一致。需要严谨财务/报销场景时，请以官方 App 或点单小程序为准。

## 能力概览

- **按城市查看咖啡价格**：输入城市名（如「上海」「北京」「成都」），获取该城市的主流品牌咖啡参考价。
- **多品牌对比**：支持星巴克、瑞幸、库迪，可扩展更多品牌。
- **多品类对比**：默认包含拿铁、美式、卡布奇诺、摩卡等常见品类。
- **多种输出格式**：支持 Markdown 表格（适合在对话中直接查看）、JSON、CSV。
- **自动推断城市（可选）**：未显式传入城市时，尝试通过 IP 定位推断当前城市。

## 快速开始

### 1. 在本地安装依赖

```bash
pip install -r requirements.txt
```

### 2. 指定城市查询（推荐）

```bash
python3 scripts/coffee_prices.py \
  --city "上海" \
  --brands starbucks,luckin,cotti \
  --drinks latte,americano,cappuccino,mocha \
  --output markdown
```

### 3. 使用当前城市（IP 自动推断）

```bash
python3 scripts/coffee_prices.py --output markdown
```

### 4. 以 JSON / CSV 形式输出（便于后续加工）

```bash
# JSON
python3 scripts/coffee_prices.py --city "北京" --output json

# CSV
python3 scripts/coffee_prices.py --city "深圳" --output csv > coffee_prices_sz.csv
```

## 参数说明

脚本入口：`scripts/coffee_prices.py`

- `--city`：城市名称（中文），如 `上海`、`北京`、`成都`。  
  - 省略时，脚本会尝试：
    1. 读取环境变量 `OPENCLAW_CITY`
    2. 通过 IP 定位接口自动推断当前城市
- `--brands`：要查询的品牌，逗号分隔。支持值：
  - `starbucks`（星巴克）
  - `luckin`（瑞幸）
  - `cotti`（库迪）
  - 默认：`starbucks,luckin,cotti`
- `--drinks`：要查询的咖啡品类，逗号分隔。支持值：
  - `latte`（拿铁）
  - `americano`（美式）
  - `cappuccino`（卡布奇诺）
  - `mocha`（摩卡）
  - 默认：`latte,americano,cappuccino,mocha`
- `--output`：输出格式：
  - `markdown`（默认）：Markdown 表格
  - `json`：结构化 JSON
  - `csv`：逗号分隔表格数据

## 输出示例（Markdown 表格）

示例命令：

```bash
python3 scripts/coffee_prices.py --city "上海" --output markdown
```

示例输出：

```markdown
| 品牌 | 品牌英文 | 城市 | 品类 | 参考价格(元) |
| ---- | -------- | ---- | ---- | ------------ |
| 星巴克 | starbucks | 上海 | 拿铁 | 38.0 |
| 星巴克 | starbucks | 上海 | 美式 | 32.0 |
| 瑞幸 | luckin | 上海 | 拿铁 | 24.0 |
| 瑞幸 | luckin | 上海 | 美式 | 20.0 |
| 库迪 | cotti | 上海 | 拿铁 | 22.0 |
| 库迪 | cotti | 上海 | 美式 | 18.0 |
```

> 真实输出会根据城市「分级系数」做轻微上/下浮动，反映一线/二线/三线城市的价格差异。

## 城市分级与价格逻辑

脚本内置一个简单的 **城市分级 + 价格系数模型**：

- **一线城市（tier1）**：如北京、上海、深圳、广州、杭州等，价格系数略高
- **二线城市（tier2）**：默认档位
- **三线及以下（tier3）**：价格系数略低

每个品牌有一套「全国基础价」，根据城市档位乘以不同系数后，得到该城市的参考价。  
如果城市未出现在内置城市列表中，会按照二线城市处理。

> 你可以直接修改 `scripts/coffee_prices.py` 中的 `CITY_TIERS` 和 `BASE_PRICES`，替换为你自己调研的更精确价格，或者接入官方 API / 爬虫逻辑。

## 在 OpenClaw 中使用

- **技能名称**：`coffee-prices`
- **推荐触发描述**：
  - 「帮我看下上海星巴克/瑞幸/库迪一杯拿铁和美式大概多少钱，并做成表格」
  - 「对比一下北京和成都的星巴克咖啡价格」
  - 「给我一份当前城市主流连锁咖啡价格表，方便做定价参考」

推荐由 Agent 调用脚本时：

1. 优先从对话中抽取城市信息（如「上海」「北京」）；如果没有，则调用脚本让其自动推断城市。
2. 默认查询 `starbucks,luckin,cotti` 三个品牌，`latte,americano,cappuccino,mocha` 四个品类。
3. 选择 `markdown` 输出，并直接将表格返回给用户。

## 限制与注意事项

- **价格为参考价**：并非实时抓取官方价格，仅按城市分级对基础价做调整。
- **品牌/品类可扩展**：可以在脚本中补充更多品牌（Manner、Seesaw 等）和更多品类。
- **网络依赖（自动定位）**：自动通过 IP 推断城市时，需要可以访问外网（`https://ipinfo.io/json`）；在离线或受限网络环境下，请显式传入 `--city`。

---

如果你需要我进一步根据你调研的真实价格数据，把 `BASE_PRICES` 改成真实价格表，或者增加新的品牌/品类，可以直接在对话中提供数据（可以是表格或 JSON），我会帮你改好脚本和文档。

