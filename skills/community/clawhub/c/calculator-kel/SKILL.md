---
name: 数值计算器
description: 基于Model Context Protocol (MCP)的数值计算器，提供加减乘除、幂运算、平方根和整数阶乘运算功能。
version: 1.0.0
---

# 数值计算器

基于Model Context Protocol (MCP)的数值计算器，提供加减乘除、幂运算、平方根和整数阶乘运算功能。

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
| 执行浮点数加法运算 | `scripts.tools.add` |
| 执行浮点数减法运算 | `scripts.tools.subtract` |
| 执行浮点数乘法运算 | `scripts.tools.multiply` |
| 执行浮点数除法运算
Args:
    b: 除数（必须非零）
 | `scripts.tools.divide` |
| 计算幂运算 | `scripts.tools.power` |
| 计算平方根 | `scripts.tools.sqrt` |
| 计算整数阶乘 | `scripts.tools.factorial` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.add
工具描述：执行浮点数加法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.subtract
工具描述：执行浮点数减法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.multiply
工具描述：执行浮点数乘法运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.divide
工具描述：执行浮点数除法运算
Args:
    b: 除数（必须非零）

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.power
工具描述：计算幂运算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|base|number|true| |null|
|exponent|number|true| |null|

---

## scripts.tools.sqrt
工具描述：计算平方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|number|number|true| |null|

---

## scripts.tools.factorial
工具描述：计算整数阶乘
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |null|

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