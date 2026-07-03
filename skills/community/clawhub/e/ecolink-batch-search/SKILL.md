---
name: ecolink-batch-search
description: EcoLink碳足迹数据库批量搜索（本地模式）。内置ecoinvent/CPCD/GHG因子库CSV数据，本地模糊匹配搜索，利用Agent自身LLM能力做翻译/分解/替代品推荐，生成HTML预览页面让用户勾选后导出CSV。当用户需要"批量搜索碳足迹"、"批量查因子"、"批量查CPCD"、"批量查碳足迹数据"时触发。
---
# EcoLink 批量搜索（本地数据库模式）

内置三个碳足迹数据库 CSV，本地模糊匹配搜索，利用 Agent 自身 LLM 能力做智能分析，零额外费用。

## 架构

```
用户输入产品名称列表
  → Agent 用自身 LLM 做翻译/别名/复合材料判断
  → 脚本本地 CSV 模糊匹配（ecoinvent + CPCD + GHG因子库）
  → 无结果时 Agent 用 LLM 做化学品分解 → 重新搜索各组分
  → 仍无结果时 Agent 用 LLM 推荐替代品 → 搜索替代品
  → 生成 HTML 预览页面 → 用户在浏览器勾选 → 导出 CSV
```

## 内置数据库

| 数据库          | 文件路径（相对 skill/） | 行数    | 说明                                                                                                                               |
| --------------- | ----------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| ecoinvent v3.12 | `data/ecoinvent.csv`  | ~26,500 | Cut-Off AO，列: activity_name, product_name, geography, time_period, sector, unit, cas_number |
| CPCD 产品碳足迹 | `data/cpcd.csv`       | ~4,875  | 列: product_name, product_name_en, model, cf_value, cf_unit, quality_score, data_year, functional_unit |
| GHG 排放因子库  | `data/ghg_factor.csv` | ~3,025  | 列: category_path, emission_type, fuel_type, factor_value, unit_cn, source |

## 执行流程

### Step 1: 获取用户输入

支持三种方式：

1. **文本列表**: 用户直接列出产品名称（逗号分隔）
2. **Excel文件**: 用户上传 Excel，读取指定列（默认列名"产品名称"）
3. **CSV文件**: 用户上传 CSV，读取指定列

如用户提供文件，先读取确认列名。

### Step 2: 对每个产品执行搜索管道

对每个产品名称，按以下顺序执行：

#### 2a. LLM 材料分析（Agent 自身执行）

Agent 用自身 LLM 能力分析产品名称，输出 JSON：

**Prompt：**

```
你是一个碳足迹LCA数据库匹配专家。请对以下原材料/产品名称进行分析：
1. 翻译成准确的英文名称（多个常用英文名全部列出）
2. 判断是否为复合材料/组合产品
3. 如果是复合产品，拆解出各组分材料的英文名称和百分比

严格按以下JSON格式返回：
{"translation": "主要英文名", "alt_names": ["别名1"], "is_composite": false, "components": [], "reason": "分析说明（中文）"}

复合材料示例：
{"translation": "concrete", "alt_names": [], "is_composite": true, "components": [{"name": "cement", "percentage": 30}, {"name": "sand", "percentage": 40}, {"name": "gravel", "percentage": 30}], "reason": "混凝土是由水泥、砂和石子按比例混合的复合材料"}
```

用户输入: `{产品名称}`

#### 2b. 本地数据库匹配（脚本执行）

用中文名 + 英文翻译 + 别名分别搜索三个数据库，结果合并去重。

**ecoinvent 匹配逻辑：**

- 对 Product Name 和 Activity Name 建分词索引
- 精确匹配 → 分词 Jaccard 相似度×0.5 + 序列相似度×0.5 → 长度惩罚
- 废弃处理类（waste/treatment/landfill/incineration）降权 50%
- 阈值 > 0.2

**CPCD 匹配逻辑：**

- 精确匹配（中文名/英文名/型号）→ 包含匹配（长度比 ≤1.5 过滤）→ 反向包含（仅中文）→ 模糊 SequenceMatcher（>0.7 且中文>0.6）
- 阈值 > 0.2

**GHG 因子库匹配逻辑：**

- 精确匹配燃料类型/排放物 → 包含匹配 → 分类路径匹配（低分）→ 模糊匹配（总>0.7 且直接>0.6）
- 阈值 > 0.2

#### 2c. 如有结果 → 直接返回

如果匹配到结果，且 LLM 判断为复合材料，则拆解各组分分别搜索。

#### 2d. 无结果 → LLM 化学品分解（Agent 自身执行）

**Prompt：**

```
你是一个化学专家。以下化学品在碳足迹LCA数据库中没有直接数据。
请将其分解为可以通过化学反应方程式组合得到的基础组分，并计算质量比例。

分解规则：
1. 优先分解为数据库中最可能存在的简单化学品/元素
2. 无机化合物分解为氧化物或单质（如 CaCO3 → CaO + CO2）
3. 有机化合物分解为常见有机原料
4. 合金/混合物分解为各组分金属
5. 组分必须是具体的化学品，不能是宽泛类别

严格按以下JSON格式返回：
{"molecular_formula": "分子式", "molar_mass": 分子量, "is_chemical": true,
 "components": [{"name": "组分英文名", "formula": "分子式", "molar_mass": 分子量,
   "mass_fraction": 0.5, "search_terms": ["搜索词1"]}],
 "reaction": "化学反应方程式", "reason": "分解说明（中文）"}

如果不是化学品，设 is_chemical 为 false 并返回空 components
```

化学品名称: `{产品名称} ({英文翻译})`

对每个组分用 search_terms 搜索，找到结果后标记为 `decomposition` 类型。

#### 2e. 仍无结果 → LLM 替代品推荐（Agent 自身执行）

**Prompt：**

```
你是一个碳足迹LCA数据库匹配专家。以下原材料/产品在数据库中找不到精确匹配。
请推荐在LCA数据库中可能存在的**具体**替代品或相近产品。

严格按以下JSON格式返回：
{"alternatives": [{"name": "替代品英文名", "reason": "推荐理由（中文）"}]}

推荐规则：
1. 替代品必须是**具体的产品/化学品**，不能是宽泛的类别
   禁止：chemical, inorganic / metal / plastic / polymer / material 等
2. 化学品推荐同族/同类具体化学品
3. 工业产品推荐功能/用途最接近的具体产品
4. 金属/合金推荐成分最接近的具体合金
5. 最多推荐3个替代品
6. 如果确实找不到任何具体的替代品，返回空数组
```

用户在碳足迹数据库中找不到: `{产品名称}`

对每个替代品搜索数据库，找到结果后标记为 `alternative` 类型。

### Step 3: 汇总结果并询问用户导出方式

所有产品搜索完成后，Agent 先汇总全部匹配结果，然后**询问用户**选择导出方式：

> 搜索完成！共 X 个产品，Y 个有匹配结果。
> 请选择导出方式：
> 1. **快速导出**：每个产品自动取前 3 条最匹配结果，直接生成 CSV
>    - 优点：速度快，一步到位，适合产品数量多或对精度要求不高的场景
>    - 缺点：无法查看和筛选每条结果，可能包含不太相关的条目
> 2. **手动筛选**：生成交互式 HTML 预览页面，在浏览器中逐条勾选后导出 CSV
>    - 优点：可逐条查看所有匹配结果，人工把关质量，导出结果更精准
>    - 缺点：需要打开浏览器操作，产品数量多时较耗时

### Step 4: 按用户选择执行

**方式一：快速导出**
- Agent 对每个产品的所有匹配结果按相关度排序，取前 3 条
- 直接写入 CSV 文件
- 展示摘要统计 + 文件路径

**方式二：手动筛选**
- 执行脚本生成 HTML 预览页面：
```bash
python skill/scripts/batch_search.py \
  --input "产品1,产品2,产品3" \
  --output results.csv --no-llm --preview
```
- 打开 HTML 预览页面让用户在浏览器中勾选
- 展示摘要统计
- 用户勾选后从浏览器导出 CSV

注意：脚本使用 `--no-llm` 模式（不调远程LLM API），LLM 分析由 Agent 自身完成。
Agent 将 LLM 分析结果（翻译、别名、分解组分、替代品）通过脚本参数或直接在脚本输出后补充到结果中。

## HTML 预览页面规格

Agent 生成 HTML 预览页面时，应包含：

- 按搜索词分组展示所有匹配结果
- 每条结果带勾选框，默认全选
- 每组有全选/取消按钮
- 顶部工具栏：导出选中为 CSV、全选、全不选
- 实时显示已选条数统计
- 结果类型用不同颜色标签区分（direct=绿, composite=紫, decomposition=橙, alternative=蓝）
- 数据来源用不同颜色区分（ecoinvent=蓝, CPCD=绿, GHG因子库=橙）
- 用户点击"导出选中为 CSV"即可下载筛选后的结果文件

## 输出 CSV 列定义

| 列名          | 说明                                             |
| ------------- | ------------------------------------------------ |
| 搜索词        | 用户输入的原始产品名称                           |
| 结果类型      | direct / composite / decomposition / alternative |
| AI翻译        | 翻译的英文名                                     |
| 数据来源      | ecoinvent / CPCD / GHG因子库                     |
| 产品名称      | 匹配到的产品名                                   |
| Activity名称  | ecoinvent 专属                                   |
| 型号          | CPCD 专属                                        |
| 地理区域      | ecoinvent 专属                                   |
| 碳足迹/因子值 | 核心数值                                         |
| 单位          | 因子单位                                         |
| 质量评分      | 数据质量评分                                     |
| 功能单元      | CPCD 专属                                        |
| 数据年份      | CPCD / ecoinvent                                 |
| 匹配原因      | 匹配/推荐原因                                    |
| 说明          | 分类路径 / 数据说明                              |

## 结果类型说明

| 类型              | 含义       | 触发条件                             |
| ----------------- | ---------- | ------------------------------------ |
| `direct`        | 直接匹配   | 中文名/英文名/别名在数据库中找到匹配 |
| `composite`     | 复合材料   | 判断为复合材料，拆解各组分分别搜索   |
| `decomposition` | 化学分解   | 直接匹配无结果，分解为化学组分并搜索 |
| `alternative`   | 替代品推荐 | 分解也无结果，推荐同类具体产品       |

## 数据更新

如需更新数据库 CSV 文件，运行：

```bash
python skill/convert_db.py
```

该脚本从原始 Excel 文件重新生成 `skill/data/` 下的三个 CSV。

## 注意事项

- 数据库文件在 `skill/data/` 目录下，CSV 格式，UTF-8 编码
- ecoinvent 仅包含 Cut-Off AO 工作表（~26,500 行）
- 本地搜索使用模糊匹配，结果质量与网页端接近但可能有细微差异
- 替代品推荐有黑名单过滤（禁止 chemical, inorganic 等宽泛类别）
- 脚本的 `--no-llm` 模式表示脚本本身不调 LLM，LLM 分析由 Agent 完成
