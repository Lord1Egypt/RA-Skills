---
name: 法国个人所得税计算服务
description: 一个提供法国个人所得税计算的MCP服务器，支持基于净应税收入和家庭构成的计算，并动态获取最新税档信息。
version: 1.0.0
---

# 法国个人所得税计算服务

一个提供法国个人所得税计算的MCP服务器，支持基于净应税收入和家庭构成的计算，并动态获取最新税档信息。

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
| Get tax information from official French government websites like impots.gouv.fr, service-public.fr, or legifrance.gouv.fr | `scripts.tools.get_tax_info_from_web` |
| Get income tax brackets (tranches d'imposition) for a specific year | `scripts.tools.get_tax_brackets` |
| Get detailed information about a specific tax form including fields and instructions | `scripts.tools.get_form_details` |
| Get cached tax information when web scraping fails | `scripts.tools.get_cached_tax_info` |
| Calculate French income tax based on net taxable income and household composition | `scripts.tools.calculate_income_tax` |
| Get information about a tax procedure from service-public.fr | `scripts.tools.get_tax_procedure` |
| Get tax deadlines from service-public.fr | `scripts.tools.get_tax_deadlines` |
| Simple health check to verify the server is responsive | `scripts.tools.health_check` |
| Get information about a tax law article from legifrance.gouv.fr | `scripts.tools.get_tax_article` |
| Search for tax law articles on legifrance.gouv.fr | `scripts.tools.search_tax_law` |
| Generate a detailed report about a specific tax topic | `scripts.tools.generate_tax_report` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_tax_info_from_web
工具描述：Get tax information from official French government websites like impots.gouv.fr, service-public.fr, or legifrance.gouv.fr
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tax_topic|string|true| |null|
|year|null|false| |null|

---

## scripts.tools.get_tax_brackets
工具描述：Get income tax brackets (tranches d'imposition) for a specific year
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|year|null|false| |null|

---

## scripts.tools.get_form_details
工具描述：Get detailed information about a specific tax form including fields and instructions
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|form_number|string|true| |null|
|year|null|false| |null|

---

## scripts.tools.get_cached_tax_info
工具描述：Get cached tax information when web scraping fails
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tax_topic|string|true| |null|
|year|null|false| |null|

---

## scripts.tools.calculate_income_tax
工具描述：Calculate French income tax based on net taxable income and household composition
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|net_taxable_income|number|true| |null|
|household_parts|number|false|1.0|null|
|year|null|false| |null|

---

## scripts.tools.get_tax_procedure
工具描述：Get information about a tax procedure from service-public.fr
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|procedure_name|string|true| |null|

---

## scripts.tools.get_tax_deadlines
工具描述：Get tax deadlines from service-public.fr
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|year|null|false| |null|

---

## scripts.tools.health_check
工具描述：Simple health check to verify the server is responsive
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_tax_article
工具描述：Get information about a tax law article from legifrance.gouv.fr
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|article_id|string|true| |null|

---

## scripts.tools.search_tax_law
工具描述：Search for tax law articles on legifrance.gouv.fr
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|

---

## scripts.tools.generate_tax_report
工具描述：Generate a detailed report about a specific tax topic
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tax_data|object|true| |null|
|topic_name|string|true| |null|
|output_file|null|false| |null|
|format|string|false|"markdown"|null|

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