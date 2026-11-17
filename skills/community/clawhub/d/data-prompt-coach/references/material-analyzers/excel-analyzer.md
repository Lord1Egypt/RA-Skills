# Excel Analyzer — Excel/CSV 样表分析器

> 适用于：data-prompt-coach 引导入口 L2+ 资料感知
> 角色：用户提交 Excel/CSV 样表后，分析字段元数据并回填 5 要素

## 触发条件

用户在引导入口提交 .xlsx / .xls / .csv 文件，且场景属于：
- 场景 1（采集）— 用户提供目标数据样例
- 场景 2（提取）— 用户提供源文件样例
- 场景 4（核对）— 用户提供待核对表样例
- 场景 5（标注）— 用户提供待标注数据样例

## 分析流程

### Step 1: 读取文件元数据

```
├─ 文件类型：.xlsx / .xls / .csv
├─ 工作表数（仅 Excel）：N 个 sheet
├─ 行数：M 行（含表头）
└─ 列数：K 列
```

### Step 2: 字段清单分析（每列）

对每一列提取以下信息：

```yaml
column_index: 1
column_name: "姓名"
data_type: "string"  # string / number / date / boolean / mixed
sample_values: ["张三", "李四", "王五"]
missing_rate: 0.05  # 缺失率 0-1
unique_count: 95  # 唯一值数（仅前 100 行采样）
format_pattern: "纯中文姓名"  # 如有规律
potential_issues:
  - "格式不统一：部分带分隔符 138-0000-0001"
  - "存在空值：5% 缺失"
```

### Step 3: 字段类型推断

对每列做类型推断：

| 数据特征 | 推断类型 |
|---------|---------|
| 全是数字 | number |
| 全是日期格式 | date |
| 全是 true/false/是/否 | boolean |
| 数字+文本混合 | mixed（需用户确认） |
| 长文本 | text |
| 短文本（<20 字） | string |

### Step 4: 数据质量扫描

```yaml
quality_issues:
  - type: "missing_values"
    column: "联系方式"
    rate: 0.05
    suggestion: "考虑回退到邮箱"
  - type: "format_inconsistent"
    column: "期望薪资"
    samples: ["30-40k", "10000/月", "未填写"]
    suggestion: "建议原样保留或统一为月薪数字"
  - type: "duplicate_values"
    column: "姓名"
    duplicate_count: 3
    suggestion: "建议加唯一标识列"
  - type: "outliers"
    column: "工作年限"
    outlier_values: [99, -1]
    suggestion: "可能是异常值，需确认"
```

### Step 5: 回填 5 要素

基于分析结果，回填访谈要素：

```yaml
scope: "✅ 已知数据规模：M 行 K 列"
fields:
  - "✅ 字段清单已识别：{K 个字段}"
  - "❓ 取值规则待确认（如多值取舍）"
processing_rules:
  - "⚠️ 检测到格式不一致：{字段名}，需处理规则"
  - "⚠️ 检测到缺失：{字段名} {rate}%，需异常处理"
output_format: "❓ 待确认（建议 Excel 或 CSV）"
exception_handling:
  - "⚠️ 检测到 {N} 个潜在异常值，需处理规则"
  - "❓ 缺失值处理规则待确认"
```

## 回填后访谈策略

资料分析后，5 要素状态变化：

| 要素 | 资料分析前 | 资料分析后 | 第 1 轮访谈重点 |
|------|----------|----------|---------------|
| 范围 | ❓ | ✅ 已知规模 | 跳过 |
| 字段 | ❓ | ✅ 清单已识别，❓取值规则 | 问取值规则 |
| 处理规则 | ❓ | ⚠️ 检测到问题 | 问处理规则 |
| 输出格式 | ❓ | ❓ | 问输出格式 |
| 异常处理 | ❓ | ⚠️ 检测到异常 | 问异常处理 |

**3 轮访谈维度划分**（基于资料分析调整）：
- 第 1 轮：取值规则（基于已识别字段问多值取舍）
- 第 2 轮：处理规则 + 输出格式（基于检测到的问题）
- 第 3 轮：异常处理 + 边界（基于检测到的异常）

## 与 SKILL.md 的接口

**入口点**：本文件"分析流程"段落
**出口点**：本文件"回填后访谈策略"末尾（5 要素回填结果）
**调用方**：SKILL.md Step A2 资料感知访谈
**依赖**：用户提交的 Excel/CSV 文件
