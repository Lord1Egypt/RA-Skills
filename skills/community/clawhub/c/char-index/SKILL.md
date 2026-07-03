---
name: 字符索引字符串处理工具
description: 一个基于字符索引的字符串操作协议服务器，适用于需要精确字符定位的测试代码生成和数据处理场景。
version: 1.0.0
---

# 字符索引字符串处理工具

一个基于字符索引的字符串操作协议服务器，适用于需要精确字符定位的测试代码生成和数据处理场景。

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
| Find index of nth occurrence of a character. Returns -1 if not found. | `scripts.tools.find_nth_char` |
| Find all indices where a character appears. Returns empty list if not found. | `scripts.tools.find_all_char_indices` |
| Find starting index of nth occurrence of a substring. Returns -1 if not found. | `scripts.tools.find_nth_substring` |
| Find all starting indices where a substring appears (includes overlaps). | `scripts.tools.find_all_substring_indices` |
| Split text at exact index positions. Indices auto-sorted and deduplicated. | `scripts.tools.split_at_indices` |
| Insert text at index position without replacing. Supports negative indices. | `scripts.tools.insert_at_index` |
| Delete characters in range [start, end). | `scripts.tools.delete_range` |
| Replace characters in range [start, end) with new text. | `scripts.tools.replace_range` |
| Find all regex matches with positions. Returns list of {start, end, match} dicts. | `scripts.tools.find_regex_matches` |
| Extract content between markers with positions. Returns dict with content and position info. | `scripts.tools.extract_between_markers` |
| Count character statistics. Returns dict with total, without_spaces, letters, digits, spaces, special. | `scripts.tools.count_chars` |
| Extract substrings by index ranges. Supports negative indices and omitting end. Returns list of {start, end, substring, length} dicts. | `scripts.tools.extract_substrings` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.find_nth_char
工具描述：Find index of nth occurrence of a character. Returns -1 if not found.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|char|string|true| |null|
|n|integer|false|1.0|null|

---

## scripts.tools.find_all_char_indices
工具描述：Find all indices where a character appears. Returns empty list if not found.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|char|string|true| |null|

---

## scripts.tools.find_nth_substring
工具描述：Find starting index of nth occurrence of a substring. Returns -1 if not found.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|substring|string|true| |null|
|n|integer|false|1.0|null|

---

## scripts.tools.find_all_substring_indices
工具描述：Find all starting indices where a substring appears (includes overlaps).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|substring|string|true| |null|

---

## scripts.tools.split_at_indices
工具描述：Split text at exact index positions. Indices auto-sorted and deduplicated.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|indices|array|true| |null|

---

## scripts.tools.insert_at_index
工具描述：Insert text at index position without replacing. Supports negative indices.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|index|integer|true| |null|
|insertion|string|true| |null|

---

## scripts.tools.delete_range
工具描述：Delete characters in range [start, end).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|start|integer|true| |null|
|end|integer|true| |null|

---

## scripts.tools.replace_range
工具描述：Replace characters in range [start, end) with new text.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|start|integer|true| |null|
|end|integer|true| |null|
|replacement|string|true| |null|

---

## scripts.tools.find_regex_matches
工具描述：Find all regex matches with positions. Returns list of {start, end, match} dicts.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|pattern|string|true| |null|

---

## scripts.tools.extract_between_markers
工具描述：Extract content between markers with positions. Returns dict with content and position info.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|start_marker|string|true| |null|
|end_marker|string|true| |null|
|occurrence|integer|false|1.0|null|

---

## scripts.tools.count_chars
工具描述：Count character statistics. Returns dict with total, without_spaces, letters, digits, spaces, special.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|

---

## scripts.tools.extract_substrings
工具描述：Extract substrings by index ranges. Supports negative indices and omitting end. Returns list of {start, end, substring, length} dicts.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |null|
|ranges|array|true| |null|

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