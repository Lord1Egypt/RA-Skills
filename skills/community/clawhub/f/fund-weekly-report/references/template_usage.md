# Word模板格式保留说明

本文档说明如何使用模板文件生成格式一致的周报。

---

## 方案说明

### 方案：基于模板的文字替换

**原理：**
1. 读取用户提供的Word模板
2. 定位需要替换的文字（通过占位符或段落位置）
3. 替换文字但保留原有格式
4. 保留模板中的图片、表格样式

**优点：**
- ✅ 格式完全一致
- ✅ 图片保留
- ✅ 表格样式保留

---

## 实现方式

### 1. 模板占位符

**在模板中使用占位符：**

```
{start_date} → 开始日期
{end_date} → 结束日期
{median1} → 收益率中位数1
...
```

**替换逻辑：**
```python
from docx import Document

doc = Document("模板.docx")

# 遍历所有段落
for para in doc.paragraphs:
    for run in para.runs:
        if '{start_date}' in run.text:
            # 替换文字但保留格式
            run.text = run.text.replace('{start_date}', '0112')
```

---

### 2. 表格数据替换

**定位表格：**
```python
# 通过表格标题定位
for table in doc.tables:
    if len(table.rows) > 0:
        first_cell = table.rows[0].cells[0]
        if '头部绩优产品' in first_cell.text:
            # 找到目标表格，填充数据
            for i, fund in enumerate(funds):
                row = table.add_row()
                row.cells[0].text = fund['基金代码']
                row.cells[1].text = fund['证券简称']
                # ...
```

---

### 3. 图片保留

**Word文档中的图片会自动保留，无需特殊处理。**

---

## 模板文件

**用户需要提供：**
- 周报模板文件（.docx）

**模板要求：**
- 使用占位符标记需要替换的文字
- 表格保留表头行
- 图片位置固定

---

## 占位符列表

### 日期相关
- `{start_date}` → 开始日期（MMDD）
- `{end_date}` → 结束日期（MMDD）

### 主动权益基金
- `{median1}` → 普通股票型基金周收益率中位数
- `{median2}` → 偏股混合型基金周收益率中位数
- `{median3}` → 灵活配置型基金周收益率中位数
- `{median4}` → 平衡混合型基金周收益率中位数
- `{max_return}` → 头部绩优产品周收益
- `{min_return}` → 尾部产品周跌幅
- `{ytd_median1}` → 年初以来收益率中位数1
- ...

### 行业主题基金
- `{top_industry}` → 领涨行业
- `{top_industry_return}` → 领涨行业收益
- `{bottom_industry}` → 领跌行业
- `{bottom_industry_return}` → 领跌行业收益

### ETF资金流动
- `{sector1}` → 板块1名称
- `{sector1_flow}` → 板块1资金流动
- `{top_inflow_fund}` → 净申购TOP基金
- `{top_inflow_amount}` → 净申购金额
- `{top_outflow_fund}` → 净赎回TOP基金
- `{top_outflow_amount}` → 净赎回金额

---

## 使用示例

```python
from generate_report import generate_report_from_template

# 使用模板生成周报
output_path = generate_report_from_template(
    template_path="周报模板.docx",
    excel_path="基金细分类型周度收益.xlsx",
    etf_path="ETF资金流动跟踪.xlsx",
    output_path="基金周报.docx"
)
```

---

## 注意事项

1. **模板文件必需** - 没有模板时使用默认格式
2. **占位符区分大小写** - `{Start_Date}` 和 `{start_date}` 不同
3. **表格行数** - 模板表格只需保留表头，数据行会自动添加
4. **图片位置** - 图片会保留在原位置，不会自动更新
