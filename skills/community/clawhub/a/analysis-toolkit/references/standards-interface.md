# 标准接口与模板管理

## 概述

analysis-toolkit 从 v1.3.0 引入了**标准注册表 + 模板管理 + 搜索链**机制，让计算函数不再硬编码公式，而是通过查标准注册表获取参数。未指定标准时通过搜索链自动降级查找。

## 架构

```
用户需求（行业 + 数据描述）
  ↓ 未指定标准 → 走搜索链
       ┌─────────────────────────────┐
       │  StandardSearchChain         │
       │  [1] national   (ISO/GB)    │ ← 一级
       │  [2] industry   (行标)      │ ← 回退
       │  [3] association(团标)      │ ← 回退
       │  [4] literature (文献)      │ ← 回退
       │  [5] tech_doc   (技术文档)  │ ← 末级
       └──────────┬──────────────────┘
                  ↓ 找到 → 自动注册
         ┌─────────────────┐
         │   标准注册表     │ ← JSON 持久化
         │ (StandardRegistry)│
         └────────┬────────┘
                  │ get_lod_loq_params(standard)
                  ▼
         ┌─────────────────┐
         │  计算函数        │
         │ (calc_lod_loq)  │
         └─────────────────┘

         ┌─────────────────┐
         │   模板管理器     │ ← JSON 持久化
         │ (TemplateManager)│
         └────────┬────────┘
                  │ apply(template_id)
                  ▼
         ┌─────────────────┐
         │  默认配置 + 标准列表│
         └─────────────────┘
```

## 标准注册表

### 标准数据模型

| 字段 | 类型 | 必需 | 说明 |
|------|------|:----:|------|
| `standard_id` | str | ✅ | 唯一标识，如 `gbt27417` |
| `name` | str | ✅ | 标准简称，如 `GB/T 27417-2017` |
| `full_name` | str | ✅ | 标准全称 |
| `industry` | list[str] | ✅ | 适用行业 |
| `applicable_functions` | list[str] | ✅ | 适用函数列表 |
| `parameters` | dict | ✅ | 公式参数键值对 |
| `formulas` | dict | ✅ | 公式描述 |
| `sigma_sources_supported` | list[str] | | 支持的 sigma 来源 |
| `notes` | str | | 补充说明 |

### LLM 注册接口

智能体/LLM 需要从标准文档中提取以下信息用于注册：

1. **standard_id** — 标准号去符号，如 `GB/T 27417-2017` → `gbt27417`
2. **name** — 标准号原样
3. **full_name** — 标准封面标题
4. **industry** — 从"适用范围"章节提取
5. **applicable_functions** — 根据公式类型判断（如 LOD 公式 → `calc_lod_loq`）
6. **parameters** — 公式中的系数
7. **formulas** — 标准原文公式
8. **sigma_sources_supported** — 标准中规定的 sigma 测定方法

**Python 注册代码：**
```python
from scripts.standards.registry import get_registry
reg = get_registry()
reg.register({
    "standard_id": "gbt5009_295",
    "name": "GB 5009.295-2023",
    "full_name": "食品安全国家标准 化学分析方法验证通则",
    "industry": ["食品检测", "理化检验"],
    "applicable_functions": ["calc_lod_loq"],
    "parameters": {"lod_factor": 3, "loq_factor": 10},
    "formulas": {"lod": "LOD = 3σ/b", "loq": "LOQ = 10σ/b"},
})
```

**CLI 注册（从 JSON 文件）：**
```bash
python scripts/standards/registry.py register my_standard.json
```

### 查询

```bash
# 列出所有标准
python scripts/standards/registry.py list

# 按行业查询
python scripts/standards/registry.py list-by-industry 食品检测

# 按函数查询
python scripts/standards/registry.py list-by-function calc_lod_loq

# 查看标准详情
python scripts/standards/registry.py get gbt27417
```

## 模板管理

### 模板数据模型

| 字段 | 类型 | 必需 | 说明 |
|------|------|:----:|------|
| `template_id` | str | ✅ | 唯一标识，如 `food-testing` |
| `name` | str | ✅ | 模板名称 |
| `industry` | str | ✅ | 所属行业 |
| `description` | str | ✅ | 模板用途说明 |
| `standards` | list[str] | ✅ | 引用的标准 ID 列表 |
| `default_config` | dict | | 默认计算参数 |
| `applicable_scenarios` | list[str] | | 适用分析场景 |
| `notes` | str | | 补充说明 |

### LLM 创建模板接口

创建模板需从用户需求提取：
1. **template_id** — 行业英文简写
2. **name** — 中文模板名称
3. **industry** — 所属行业
4. **description** — 模板覆盖的业务范围
5. **standards** — 该行业常用的标准 ID 列表
6. **default_config** — 最常用的参数默认值
7. **applicable_scenarios** — 该行业做哪些分析

**示例：**
```python
from scripts.standards.template_manager import get_manager
tm = get_manager()
tm.create({
    "template_id": "food-testing",
    "name": "食品检验检测标准体系",
    "industry": "食品检测",
    "description": "适用于食品理化检验的常用国家标准体系",
    "standards": ["gbt27417"],
    "default_config": {"lod_loq_standard": "gbt27417"},
    "applicable_scenarios": ["方法验证", "标准曲线"],
})
```

### 模板操作

```bash
# 列出所有模板
python scripts/standards/template_manager.py list

# 查看模板详情
python scripts/standards/template_manager.py get food-testing

# 搜索模板
python scripts/standards/template_manager.py search 食品

# 应用模板（获取配置）
python scripts/standards/template_manager.py apply food-testing

# 删除模板
python scripts/standards/template_manager.py delete food-testing
```

## 内置数据

### 已注册标准

| standard_id | 名称 | 适用行业 |
|:-----------:|------|----------|
| `gbt27417` | GB/T 27417-2017 | 化学分析、食品检测、环境监测、药品检测 |
| `ich` | ICH Q2(R1) / 中国药典 2020版 | 药品检测、生物制品、化学药品 |

### 内置模板

| template_id | 名称 | 行业 | 引用标准 | 适用场景 |
|:-----------:|------|:----:|:--------:|:--------:|
| `food-testing` | 食品检验检测标准体系 | 食品检测 | gbt27417 | 室内质控、方法验证、标准曲线、回收率 |
| `pharmaceutical-testing` | 药品检验检测标准体系 | 药品检测 | ich | 方法验证、标准曲线、LOD/LOQ |

---

## 数据流水线

完整数据流：**用户原始数据 → LLM 指令 → Python 执行 → 格式校验 → 计算**

### 数据准备引擎（data_prep.py）

LLM 分析用户数据后，输出结构化指令，Python 自动执行转换。

```python
from scripts.core.data_prep import execute_prep, validate

# 用户原始数据（Excel/CSV/字典列表/数组）
raw_data = [
    {"浓度ppm": 0, "响应值": 101, "备注": "空白"},
    {"浓度ppm": 5, "响应值": 32500},
]

# LLM 根据接口指南生成指令
instructions = {
    "rename": {"浓度ppm": "x", "响应值": "y"},
    "drop_columns": ["备注"],
    "type_cast": {"x": "float", "y": "float"},
    "dropna": True,
}

# Python 自动执行
prepped = execute_prep(raw_data, instructions)

# 格式校验（计算前兜底）
result = validate(prepped["data"],
                  required_columns=["x", "y"],
                  min_rows=2)
if not result["valid"]:
    print("数据问题:", result["errors"])

# 通过 → 传入计算函数
```

**支持的指令：**

| 指令 | 说明 | 示例 |
|------|------|------|
| `rename` | 列名映射（用户列名 → 函数期望列名） | `{"浓度ppm": "x"}` |
| `drop_columns` | 删除无关列 | `["备注", "编号"]` |
| `type_cast` | 类型转换 | `{"日期": "datetime", "结果": "float"}` |
| `dropna` | 删除空值行 | `true` |
| `filter` | 行过滤（范围/异常值剔除） | `{"column": "结果", "min": 0, "remove_outliers": true}` |
| `aggregate` | 分组聚合 | `{"group_by": "实验室", "agg_column": "结果", "agg_func": "mean"}` |

### 格式校验（validate()）

在数据传入计算函数前执行，仅检查：
- 数据是否为空
- 必需列是否存在
- 数据量是否达到最低要求
- NaN 数量提示

校验不阻断执行，仅通过 errors/warnings 告知 LLM。LLM 收到后修正指令重新准备即可。

当用户未指定具体标准号时，按以下优先级自动降级搜索：

| 优先级 | 级别 | 说明 | 覆盖方式 |
|:------:|:----:|------|:--------:|
| 1 | `national` | 国家标准(GB) / 国际标准(ISO) | 指定 `explicit="GB/T XXXX"` 跳过链 |
| 2 | `industry` | 行业标准 | 指定 `start_level="industry"` 从本级开始 |
| 3 | `association` | 团体标准 | 指定 `start_level="association"` |
| 4 | `literature` | 行业惯例/学术文献 | 指定 `start_level="literature"` |
| 5 | `tech_doc` | 技术文档/博客/非文献资料 | 末级，不可跳过 |

### 搜索链配置

每级的搜索钩子（hook）可独立替换，默认实现为从注册表搜索和空占位。

```python
from scripts.standards.searcher import get_search_chain

chain = get_search_chain()

# 替换第二级(行业标准)的搜索钩子
def my_industry_search(industry, data_description, context):
    # 联网搜索行业标准
    return [{"standard_id": "qc/t-xxx", "name": "...", ...}]

chain.set_hook("industry", my_industry_search)

# 执行搜索
result = chain.search(industry="汽车", data_description="涂装线质控")
# result.chain_trace → ["national → 无匹配", "industry → QC/T-XXX"]

# 明确标准号 → 跳过链直接查
result = chain.search(explicit="GB/T 27417")

# 从第二级开始
result = chain.search(industry="汽车", start_level="industry")

# 自动注册模式
result = chain.auto_register_and_search(industry="汽车")
```

### 搜索链命中后的自动注册

`auto_register_and_search()` 在搜索链找到匹配标准时，自动将其注册到 `StandardRegistry`，
后续计算函数调用时可以直接通过 standard_id 引用。

### 降级钩子替换原则

1. **默认降级顺序不可变**（ISO/GB → 行标 → 团标 → 文献 → 技术文档）
2. **指定标准号**（`explicit="GB/T XXXX"`）：完全跳过链
3. **指定起始级**（`start_level="industry"`）：从指定级往下搜
4. **指定标准等级**（`start_level` 配合 `stop_level`）：限定搜索范围
5. **自定义钩子**（`set_hook()`）：仅替换某一级的搜索逻辑，不影响降级顺序
