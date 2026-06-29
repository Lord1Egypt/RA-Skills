---
name: 星座服务
description: 一个功能完整的星座 MCP (Model Context Protocol) 服务，提供星座信息查询、运势分析、配对测试等功能。
version: 1.0.0
---

# 星座服务

一个功能完整的星座 MCP (Model Context Protocol) 服务，提供星座信息查询、运势分析、配对测试等功能。

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
| 获取指定星座的详细信息，包括性格特征、守护星、元素等 | `scripts.tools.get_zodiac_info` |
| 获取指定星座的今日运势 | `scripts.tools.get_daily_horoscope` |
| 获取两个星座的配对指数和关系分析 | `scripts.tools.get_compatibility` |
| 获取所有星座的基本信息列表 | `scripts.tools.get_all_zodiacs` |
| 根据出生日期确定星座 | `scripts.tools.get_zodiac_by_date` |
| 计算上升星座，需要出生时间、地点和日期 | `scripts.tools.get_rising_sign` |
| 获取指定上升星座的详细信息 | `scripts.tools.get_rising_sign_info` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_zodiac_info
工具描述：获取指定星座的详细信息，包括性格特征、守护星、元素等
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|zodiac|string|true| |星座名称（中文或英文）|

---

## scripts.tools.get_daily_horoscope
工具描述：获取指定星座的今日运势
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|zodiac|string|true| |星座名称（中文或英文）|
|category|string|false|"luck"|运势类别|

---

## scripts.tools.get_compatibility
工具描述：获取两个星座的配对指数和关系分析
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|zodiac1|string|true| |第一个星座名称（中文或英文）|
|zodiac2|string|true| |第二个星座名称（中文或英文）|

---

## scripts.tools.get_all_zodiacs
工具描述：获取所有星座的基本信息列表
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_zodiac_by_date
工具描述：根据出生日期确定星座
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|month|integer|true| |出生月份（1-12）|
|day|integer|true| |出生日期（1-31）|

---

## scripts.tools.get_rising_sign
工具描述：计算上升星座，需要出生时间、地点和日期
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|birthHour|integer|true| |出生小时（0-23）|
|birthMinute|integer|true| |出生分钟（0-59）|
|latitude|number|true| |出生地纬度（-90到90）|
|longitude|number|true| |出生地经度（-180到180）|
|birthMonth|integer|true| |出生月份（1-12）|
|birthDay|integer|true| |出生日期（1-31）|
|birthYear|integer|true| |出生年份（1900-2100）|

---

## scripts.tools.get_rising_sign_info
工具描述：获取指定上升星座的详细信息
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|risingSign|string|true| |上升星座名称（中文或英文）|

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