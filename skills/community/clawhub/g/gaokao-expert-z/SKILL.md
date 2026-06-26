---
name: 高考志愿
description: 提供高考志愿相关工具，获取学校和专业以往的录取分数线，提供推荐信息等。注意：往年的数据都是真实数据，当前2026年的数据还未发布，为提前获得完整体验，暂时基于2025年数据虚拟了一份，后面会及时更新。
version: 1.0.0
---

# 全国高考志愿填报助手 MCP

提供高考志愿相关工具，获取学校和专业以往的录取分数线，提供推荐信息等。注意：往年的数据都是真实数据，当前2026年的数据还未发布，为提前获得完整体验，暂时基于2025年数据虚拟了一份，后面会及时更新。

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
| 获取某省某年的高考控制分数线（一本线/二本线）。 | `scripts.tools.get_control_lines` |
| 获取学校前几年的录取分数线。 | `scripts.tools.get_school_scores` |
| 查询某所学校在某省某年的招生计划。 | `scripts.tools.get_plans` |
| 查询某所学校在某省某科类的各专业历年录取分数线。当用户想了解具体专业的录取分数（如"北大的计算机多少分"、"西安交大各专业录取分数"）时使用。返回每个专业的最低分、位次和录取人数。 | `scripts.tools.get_major_scores` |
| 根据考生条件筛选有录取数据的候选学校，返回的学校中筛选录取位次接近考生排名（考生排名±3000名）的学校名称。你需要提取学校名称传给 calculate_probability 计算概率。 | `scripts.tools.search_schools` |
| 批量计算录取概率。传入学校代码列表，返回每所学校的录取概率、档位（冲刺/稳妥/保底/不建议）和说明。 | `scripts.tools.calculate_probability` |
| 查询某所学校在某省某科类的历年录取分数线（最近5年），包含最低分、最低排名 | `scripts.tools.lookup_scores` |
| 模糊搜索学校。按学校名称或代码搜索，支持筛选条件。 | `scripts.tools.search_school_by_keyword` |
| 将高考分数转换为省排名（基于官方一分一段表）。当用户只有分数不知道位次时使用此工具。 | `scripts.tools.score_to_rank` |
| 获取关于指定学校的某方面信息。通过设置参数info_type的值（"基本信息", "学校简介", "学校详情", "大学排名", "学科评估", "特色专业", "院系设置"）获取相应信息。默认返回基本信息。 | `scripts.tools.get_school_info` |
| 获取关于指定专业的某方面信息。通过设置参数info_type的值（"基本信息", "专业介绍", "培养目标", "授予学位", "修业年限", "男女比例", "专业与就业", "专业解析", "报考指南","主要就业行业分布", "主要就业地区分布", "近10年平均薪资", "就业方向", "主要职业分布"）获取相应信息。默认返回基本信息。 | `scripts.tools.get_major_info` |
| 获取开设某专业的学校列表（按该专业的排名顺序）。 | `scripts.tools.get_schools_of_major` |
| 获取某学校开设的专业列表。 | `scripts.tools.get_majors_of_school` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_control_lines
工具描述：获取某省某年的高考控制分数线（一本线/二本线）。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|province|string|true| |招生省份|
|year|integer|false| |年份，默认为今年|

---

## scripts.tools.get_school_scores
工具描述：获取学校前几年的录取分数线。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|province|string|true| |招生省份|
|school|string|true| |学校名称，如"清华大学"|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.get_plans
工具描述：查询某所学校在某省某年的招生计划。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|province|string|true| |招生省份|
|school|string|true| |学校名称，如"清华大学"|
|year|integer|false| |年份，默认为今年|

---

## scripts.tools.get_major_scores
工具描述：查询某所学校在某省某科类的各专业历年录取分数线。当用户想了解具体专业的录取分数（如"北大的计算机多少分"、"西安交大各专业录取分数"）时使用。返回每个专业的最低分、位次和录取人数。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|province|string|true| |招生省份|
|school|string|true| |学校名称，如"清华大学"|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.search_schools
工具描述：根据考生条件筛选有录取数据的候选学校，返回的学校中筛选录取位次接近考生排名（考生排名±3000名）的学校名称。你需要提取学校名称传给 calculate_probability 计算概率。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|is985|boolean|false| |是否只看985（可选）|
|score|string|true| |高考分数|
|province|string|true| |招生省份|
|is211|boolean|false| |是否只看211（可选）|
|level|string|false| |报考等级（本科或者专科）,默认为本科|
|target_provinces|string|false| |指定选择哪些省份的学校，省份名称以逗号分隔。若不输入此参数，则搜索所有省份的学校。|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.calculate_probability
工具描述：批量计算录取概率。传入学校代码列表，返回每所学校的录取概率、档位（冲刺/稳妥/保底/不建议）和说明。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|score|string|true| |高考分数|
|province|string|true| |招生省份|
|level|string|false| |报考等级（本科或者专科）,默认为本科|
|target_schools|string|true| |目标学校名称列表，逗号分隔|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.lookup_scores
工具描述：查询某所学校在某省某科类的历年录取分数线（最近5年），包含最低分、最低排名
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|province|string|true| |招生省份|
|school|string|true| |学校名称，如"清华大学"|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.search_school_by_keyword
工具描述：模糊搜索学校。按学校名称或代码搜索，支持筛选条件。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|is985|boolean|false| |是否只看985（可选）|
|q|string|true| |学校名称的搜索关键词|
|is211|boolean|false| |是否只看211（可选）|
|level|string|false| |报考等级（本科或者专科）,默认为本科|
|target_provinces|string|false| |指定选择哪些省份的学校，省份名称以逗号分隔。若不输入此参数，则搜索所有省份的学校。|

---

## scripts.tools.score_to_rank
工具描述：将高考分数转换为省排名（基于官方一分一段表）。当用户只有分数不知道位次时使用此工具。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|score|string|true| |高考分数|
|province|string|true| |招生省份|
|year|integer|false| |年份，默认为今年|
|level|string|false| |报考等级（本科或者专科）,默认为本科|
|category|string|true| |科类：综合/文科/理科/物理类/历史类|

---

## scripts.tools.get_school_info
工具描述：获取关于指定学校的某方面信息。通过设置参数info_type的值（"基本信息", "学校简介", "学校详情", "大学排名", "学科评估", "特色专业", "院系设置"）获取相应信息。默认返回基本信息。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|info_type|string|false| |信息选项（可选），支持查询的信息选项："基本信息", "学校简介", "学校详情", "大学排名", "学科评估", "特色专业", "院系设置"。|
|school|string|true| |学校名称，如"清华大学"|

---

## scripts.tools.get_major_info
工具描述：获取关于指定专业的某方面信息。通过设置参数info_type的值（"基本信息", "专业介绍", "培养目标", "授予学位", "修业年限", "男女比例", "专业与就业", "专业解析", "报考指南","主要就业行业分布", "主要就业地区分布", "近10年平均薪资", "就业方向", "主要职业分布"）获取相应信息。默认返回基本信息。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|info_type|string|false| |信息选项（可选），支持查询的信息选项："基本信息", "专业介绍", "培养目标", "授予学位", "修业年限", "男女比例", "专业与就业", "专业解析", "报考指南","主要就业行业分布", "主要就业地区分布", "近10年平均薪资", "就业方向", "主要职业分布"。|
|major|string|true| |专业名称|

---

## scripts.tools.get_schools_of_major
工具描述：获取开设某专业的学校列表（按该专业的排名顺序）。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|major|string|true| |专业名称|

---

## scripts.tools.get_majors_of_school
工具描述：获取某学校开设的专业列表。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|school|string|true| |学校名称，如"清华大学"|

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