# 亲子场景 · fliggy-fast-search 查询写法

使用 **`flyai fliggy-fast-search --query "<自然语言>"`**（须已安装 `@fly-ai/flyai-cli`）。该子命令**只有 `--query`**，没有日期/床型等结构化 flag —— 凡 **`search-hotels` / `search-flight` / `search-poi` 表达不了的约束**，都应写进 query。

## 建议写入 query 的要素

| 维度 | 中文示例片段 | English examples |
|------|----------------|------------------|
| 儿童年龄与人数 | `5岁` `两大一小` `两大两小` `婴儿` | `toddler` `one child age 5` |
| 陪护与体力 | `单人带娃` `每天最多一个主景点` `少走台阶` | `single parent` `one main activity per day` |
| 节奏 | `半天行程` `中午回酒店午休` | `half-day` `nap time` |
| 交通承受 | `车程不超过1小时` `少换乘` | `max 1h drive` |
| 偏好 | `沙滩` `室内为主` `主题乐园` | `beach` `indoor` `theme park` |
| 酒店设施（无结构化 flag 时） | `带儿童乐园` `泳池` `洗衣` `亲子酒店` | `kids club` `pool` `laundry` |
| 特殊需求（结果需人工核实） | `饮食清淡` `过敏需注意` | `food allergies` |
| 时间与目的地 | `2026年7月` `三亚` `周边自驾` | `July 2026` `Sanya` |

## 与结构化命令的分工（从实际出发）

| 用户诉求 | 优先手段 |
|----------|----------|
| 比机票时段、直飞、大致价格 | `search-flight`（`--journey-type`、`--dep-hour-*`、`--sort-type`） |
| 比酒店日期、星级、双床/多床、离景点近 | `search-hotels`（`--hotel-bed-types` 仅 大床/双床/多床） |
| 按类型扒景点列表 | `search-poi`（`--category` 严格枚举） |
| 家庭房连通房、套餐、玩乐组合、模糊一句话 | **`fliggy-fast-search`** |

## 可直接改写的模板

```bash
flyai fliggy-fast-search --query "<城市或区域> <天数> 亲子 <孩子年龄> <节奏要求> <偏好>"
```

示例：

```bash
flyai fliggy-fast-search --query "杭州 三天两晚 亲子 4岁 推车友好 每天一个主景点"
flyai fliggy-fast-search --query "普吉岛 5天 亲子 海水沙滩 酒店带儿童乐园"
flyai fliggy-fast-search --query "北京 周末 两大一小 室内为主 下雨备选"
flyai fliggy-fast-search --query "珠海 亲子 长隆附近 双床 预算中等 带娃省心"
```

## 与结构化命令的配合

1. 先用 **`fliggy-fast-search`** 定方向或找套餐/组合商品。
2. 需要对齐 **真实日期、床型、直飞、POI 类目** 时，再用 `search-hotels` / `search-flight` / `search-poi` 细化。
3. 具体 flag 与枚举以 **`references/cli-capabilities.md`** 与 **`flyai <子命令> --help`** 为准。
