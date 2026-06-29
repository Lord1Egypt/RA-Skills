---
name: 万智牌卡牌查询服务
description: 一个基于Model Context Protocol (MCP)的服务端，提供万智牌中文卡牌信息的查询和搜索功能。
version: 1.0.0
---

# 万智牌卡牌查询服务

一个基于Model Context Protocol (MCP)的服务端，提供万智牌中文卡牌信息的查询和搜索功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| 通过系列代码和收集编号获取单张卡牌。 | `scripts.tools.get_card_by_set_and_number` |
| 通过查询字符串搜索卡牌，支持分页和排序。

**查询语法示例:**
- `t:creature c:r` (红色生物)
- `pow>=5 or mv<2` (力量大于等于5或法术力值小于2)
- `o:"draw a card" -c:u` (包含"抓一张牌"的非蓝色牌)
- `(t:instant or t:sorcery) mv<=3` (3费或以下的瞬间或法术)

**分页参数:**
- `page`: 页码 (整数, 默认 1)
- `page_size`: 每页数量 (整数, 默认 20, 最大 100)

**排序参数:**
- `order`: 按字段排序，逗号分隔。前缀 `-` 表示降序
  (例如: `name`, `-mv`, `name,-rarity`)
  默认排序: `name`

**其他参数:**
- `unique`: 去重方式 (id, oracle_id, illustration_id)
- `priority_chinese`: 是否优先显示中文卡牌 | `scripts.tools.search_cards` |
| 返回所有MTG卡牌系列的完整数据，按发布日期降序排列 | `scripts.tools.get_sets` |
| 根据系列代码获取单个系列的详细信息 | `scripts.tools.get_set` |
| 获取特定系列的所有卡牌，支持分页和排序。 | `scripts.tools.get_set_cards` |
| 活字乱刷（使用卡牌图像拼接句子），将输入的文本使用魔法卡牌图像拼接成图片 | `scripts.tools.hzls` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_card_by_set_and_number
工具描述：通过系列代码和收集编号获取单张卡牌。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|set|string|true| |系列代码，例如 'NEO'、'MOM'|
|collector_number|string|true| |收集编号，例如 '1'、'112'、'1a'|

---

## scripts.tools.search_cards
工具描述：通过查询字符串搜索卡牌，支持分页和排序。

**查询语法示例:**
- `t:creature c:r` (红色生物)
- `pow>=5 or mv<2` (力量大于等于5或法术力值小于2)
- `o:"draw a card" -c:u` (包含"抓一张牌"的非蓝色牌)
- `(t:instant or t:sorcery) mv<=3` (3费或以下的瞬间或法术)

**分页参数:**
- `page`: 页码 (整数, 默认 1)
- `page_size`: 每页数量 (整数, 默认 20, 最大 100)

**排序参数:**
- `order`: 按字段排序，逗号分隔。前缀 `-` 表示降序
  (例如: `name`, `-mv`, `name,-rarity`)
  默认排序: `name`

**其他参数:**
- `unique`: 去重方式 (id, oracle_id, illustration_id)
- `priority_chinese`: 是否优先显示中文卡牌
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|q|string|true| |查询字符串，例如 't:creature c:r'、'pow>=5 or mv<2'、's:TDM -t:creature'|
|page|integer|false| |页码 (默认 1)|
|page_size|integer|false| |每页数量 (默认 20，最大 100)|
|order|string|false| |排序字段 (例如: name, -mv, rarity)|
|unique|string|false| |去重方式: id(不去重), oracle_id(按卡牌名去重), illustration_id(按插图去重)|
|priority_chinese|boolean|false| |是否优先显示中文卡牌 (默认 true)|

---

## scripts.tools.get_sets
工具描述：返回所有MTG卡牌系列的完整数据，按发布日期降序排列
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_set
工具描述：根据系列代码获取单个系列的详细信息
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|set_code|string|true| |系列代码，例如 'NEO'、'MOM'|

---

## scripts.tools.get_set_cards
工具描述：获取特定系列的所有卡牌，支持分页和排序。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|set_code|string|true| |系列代码，例如 'NEO'、'MOM'|
|page|integer|false| |页码 (默认 1)|
|page_size|integer|false| |每页数量 (默认 20，最大 100)|
|order|string|false| |排序字段 (例如: collector_number, name, -mv)|
|priority_chinese|boolean|false| |是否优先显示中文卡牌 (默认 true)|

---

## scripts.tools.hzls
工具描述：活字乱刷（使用卡牌图像拼接句子），将输入的文本使用魔法卡牌图像拼接成图片
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|target_sentence|string|true| |要拼接的目标句子/文本|
|cut_full_image|boolean|false| |是否使用卡牌完整图像 (默认 true)|
|with_link|boolean|false| |是否包含链接水印 (默认 true)|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据