# Excel 模板规格

> 适用场景：1 网页采集 / 2 文档字段提取 / 4 数据核对
> 配套方法论：M1（黄金五要素）+ M2（防幻觉三招）+ M7（验真闭环）

## 触发场景

| 场景 | 用途 | 与 Prompt 的关系 |
|------|------|----------------|
| 1 采集 | 抓取结果的字段清单 + 列宽建议 | Prompt 输出格式 = 此模板 |
| 2 提取 | 提取字段的列定义 + 取值规则 | Prompt 输出格式 = 此模板 |
| 4 核对 | 两表对比的状态矩阵 + 异常标记 | Prompt 输出格式 = 此模板 |

## 模板结构（YAML 描述）

```yaml
template_type: excel
template_name: "{场景名}-{日期}-template"
sheet_name: "Data"
freeze_pane: "A2"
header_row: 1
columns:
  - name: "{字段名}"
    type: "text|number|date|datetime|formula"
    width: 12-30
    required: true|false
    default: "{默认值}"
    validation:
      type: "list|number_range|date_range|regex"
      rule: "{校验规则}"
    multi_value_strategy: "first|last|join_with_separator|all_rows"
    note: "{字段说明}"
  # ... 更多字段
summary_sheet:
  enabled: true
  sheet_name: "Summary"
  metrics:
    - name: "{统计指标名}"
      formula: "{Excel 公式}"
      description: "{说明}"
```

## 生成规则

### Step 1: 从访谈快照提取字段

读取 SKILL.md Step A2 的 5 要素完备快照，提取：
- 字段清单（来自 M1）
- 取值规则（异常处理策略）
- 多值取舍策略（来自访谈第 3 轮）
- 输出格式偏好（Excel）

### Step 2: 按场景调整结构

#### 场景 1 网页采集

```yaml
columns:
  - name: 序号
    type: number
    width: 6
    required: true
  - name: 标题
    type: text
    width: 40
    required: true
  - name: 发布日期
    type: date
    width: 12
    validation:
      type: date_range
      rule: ">=2024-01-01"
  - name: 来源 URL
    type: text
    width: 50
    required: true
  - name: 正文摘要
    type: text
    width: 60
    default: ""
    note: "留空表示未抓取到"
  - name: 抓取时间
    type: datetime
    width: 18
    required: true
    default: "=NOW()"
```

#### 场景 2 文档字段提取

```yaml
columns:
  - name: 文档序号
    type: number
    required: true
  - name: 文档名
    type: text
    required: true
  - name: 姓名
    type: text
    required: true
    multi_value_strategy: "first"
  - name: 电话
    type: text
    validation:
      type: regex
      rule: "^1[3-9]\\d{9}$"
    default: "未填写"
  - name: 学历
    type: text
    validation:
      type: list
      rule: "大专,本科,硕士,博士,其他"
  - name: 期望薪资
    type: text
    note: "保留原始字符串，不强制数值化"
  - name: 异常标记
    type: text
    default: ""
    note: "字段缺失/格式异常时填'待人工核查'"
```

#### 场景 4 数据核对

```yaml
sheets:
  - name: "核对明细"
    columns:
      - name: 匹配键
        type: text
        required: true
      - name: A 表字段值
        type: text
      - name: B 表字段值
        type: text
      - name: 核对状态
        type: text
        validation:
          type: list
          rule: "一致,不一致,仅A有,仅B有,待确认"
      - name: 差异说明
        type: text
        default: ""
      - name: 处理建议
        type: text
  - name: "汇总统计"
    metrics:
      - name: 总行数
        formula: "=COUNTA(核对明细!A:A)-1"
      - name: 一致数
        formula: '=COUNTIF(核对明细!D:D,"一致")'
      - name: 不一致数
        formula: '=COUNTIF(核对明细!D:D,"不一致")'
      - name: 仅 A 有
        formula: '=COUNTIF(核对明细!D:D,"仅A有")'
      - name: 仅 B 有
        formula: '=COUNTIF(核对明细!D:D,"仅B有")'
      - name: 待确认
        formula: '=COUNTIF(核对明细!D:D,"待确认")'
```

### Step 3: 注入防幻觉元素

每个模板必须包含：
1. **序号列**（确保可追溯）
2. **来源列**（数据出处，URL 或文档名）
3. **异常标记列**（默认空，遇异常填"待人工核查"）
4. **抓取/处理时间列**（带 =NOW() 公式）

### Step 4: 与验真脚本联动

Excel 模板生成后，必须同时生成对应的验真脚本（见 [verify-template-spec.md](verify-template-spec.md)），用于：
- 检查必填字段是否为空
- 检查格式是否符合 validation 规则
- 检查异常标记列是否有未处理项

## 示例输出（场景 2 简历提取）

```yaml
template_type: excel
template_name: "简历提取-20260722-template"
sheet_name: "ResumeData"
freeze_pane: "A2"
header_row: 1
columns:
  - {name: 序号, type: number, width: 6, required: true}
  - {name: 文档名, type: text, width: 30, required: true}
  - {name: 姓名, type: text, width: 12, required: true, multi_value_strategy: "first"}
  - {name: 电话, type: text, width: 14, validation: {type: regex, rule: "^1[3-9]\\d{9}$"}, default: "未填写"}
  - {name: 学历, type: text, width: 8, validation: {type: list, rule: "大专,本科,硕士,博士,其他"}}
  - {name: 期望薪资, type: text, width: 14, note: "保留原始字符串"}
  - {name: 异常标记, type: text, width: 20, default: "", note: "待人工核查"}
  - {name: 抓取时间, type: datetime, width: 18, default: "=NOW()"}
summary_sheet:
  enabled: true
  sheet_name: "Summary"
  metrics:
    - {name: 总数, formula: "=COUNTA(A:A)-1"}
    - {name: 异常数, formula: '=COUNTIF(G:G,"待人工核查")'}
```

## 与其他模块的接口

| 接口 | 调用方 | 依赖 |
|------|--------|------|
| 上游 | SKILL.md Step A4 | 5 要素完备快照 + 方法论组合 |
| 下游 | verify-template-spec.md | 验真脚本读取此模板的字段定义 |
| 关联方法论 | M1 黄金五要素 | 字段清单 + 取值规则 |
| 关联方法论 | M2 防幻觉三招 | 异常标记列 + 默认值 |
| 关联方法论 | M7 验真闭环 | 与验真脚本联动 |
