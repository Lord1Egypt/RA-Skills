---
name: AnnData数据检索工具
description: AnnData MCP是一个通过MCP协议检索AnnData对象信息的工具，适用于生物医学数据分析场景。
version: 1.0.0
---

# AnnData数据检索工具

AnnData MCP是一个通过MCP协议检索AnnData对象信息的工具，适用于生物医学数据分析场景。

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
| View the raw data of an AnnData object. | `scripts.tools.view_raw_data` |
| Get a summary of an AnnData object from a file or URL. | `scripts.tools.get_summary` |
| Provide basic descriptive statistics (e.g., count, mean, std, min, max, etc. or value counts) for an attribute or attribute value of an optionally filtered AnnData object. | `scripts.tools.get_descriptive_stats` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.view_raw_data
工具描述：View the raw data of an AnnData object.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|path|string|true| |Absolute path or URL to the AnnData file|
|attribute|string|true| |The attribute to view|
|key|null|false| |The key of the attribute value to view. Can be a single string or a list of strings for nested key retrieval (e.g., ['key1', 'key2'] to access attr_obj['key1']['key2']).|
|columns_or_genes|null|false| |Column names or gene names to select. For pandas.DataFrame attributes (e.g., obs, var), these are column names. For 'X' or 'layers' attributes, these are gene names (from var_names) and are used instead of col_start_index/col_stop_index. If None, the entire attribute is considered or col_start_index/col_stop_index is used. Also accepts glob-like patterns as input, e.g. ['RE*', 'CD4*'].|
|row_start_index|integer|false|0.0|The start index for the row slice. Only applied to attributes or attribute values with a suitable type.|
|row_stop_index|integer|false|5.0|The stop index for the row slice. Only applied to attributes or attribute values with a suitable type.|
|col_start_index|integer|false|0.0|The start index for the column slice. Only applied to attributes or attribute values with a suitable type.|
|col_stop_index|integer|false|5.0|The stop index for the column slice. Only applied to attributes or attribute values with a suitable type.|
|filter_column|null|false| |The column name of the dataframe to filter by. Only applicable when the selected attribute (or attribute value) is a dataframe. Must be provided TOGETHER with filter_operator and filter_value.|
|filter_operator|null|false| |The operator to use for the dataframe filter.|
|filter_value|null|false| |The value(s) to filter the dataframe by.|

---

## scripts.tools.get_summary
工具描述：Get a summary of an AnnData object from a file or URL.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|path|string|true| |Absolute path or URL to the AnnData file (.h5ad or .zarr)|

---

## scripts.tools.get_descriptive_stats
工具描述：Provide basic descriptive statistics (e.g., count, mean, std, min, max, etc. or value counts) for an attribute or attribute value of an optionally filtered AnnData object.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|path|string|true| |Absolute path or URL to the AnnData file (.h5ad or .zarr)|
|attribute|string|true| |The attribute to describe|
|key|null|false| |The key of the attribute value to explore. Can be a single string or a list of strings for nested key retrieval (e.g., ['key1', 'key2'] to access attr_obj['key1']['key2']). Should be None for attributes X, obs, and var.|
|columns_or_genes|null|false| |The columns or genes to describe. For pandas.DataFrame attributes (e.g., obs, var), these are column names. For 'X' or 'layers' attributes, these are gene names (from var_names). If None, the entire dataset is considered. Also accepts glob-like patterns as input, e.g. ['RE*', 'CD4*'].|
|return_value_counts_for_categorical|boolean|false|false|Whether to return the value counts for categorical columns.|
|filter_attribute|string|false| |The attribute to filter by. One of 'obs' or 'var' or None for no filtering. Has to be provided TOGETHER with filter_column, filter_operator, and filter_value.|
|filter_column|null|false| |The column name of the obs or var dataframe to filter by.|
|filter_operator|null|false| |The operator to use for the filter.|
|filter_value|null|false| |The value(s) to filter by.|

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