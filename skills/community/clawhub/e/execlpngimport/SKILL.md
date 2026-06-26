---
name: excel-import-helper
description: Excel/截图字段智能导入工具。将 Excel 数据源或截图（PDU截图）中的字段，按照固定模板格式自动导入，生成标准化的导入模板。支持中英文字段名映射、字段类型智能识别、截图 OCR 识别。适用于资产负债表、现金流量表、利润表、银行账号等财务报表批量导入场景。
author: QClaw Assistant
version: "1.0.0"
tags: [excel, ocr, template, 报表, 财务]
---

# Excel 导入模板智能生成器

## 功能说明

将 Excel 数据源或截图中的字段，按照固定模板格式自动导入，生成标准化的导入模板。

**支持的数据源类型**：
- Excel/CSV 文件
- 截图/图片（PNG、JPG 等）

**支持的报表类型**：
- 资产负债表
- 现金流量表
- 利润表
- 银行账号配置
- 任意自定义表单

## 使用方法

### 方式一：处理 Excel 文件

用户提供：
1. 模板文件路径
2. 数据源 Excel 文件路径
3. 表中文名

### 方式二：处理截图/图片

用户提供：
1. 截图文件路径（支持多张截图）

系统自动完成：
- OCR 识别截图文字
- 提取字段名
- 生成中英文映射
- 识别字段类型
- 输出模板文件

## 工作流程

### Step 1: OCR 识别（截图场景）

```python
from cnocr import CnOcr

ocr = CnOcr()
result = ocr.ocr('截图路径.png')

# 打印全部识别结果检查完整性
for i, item in enumerate(result, 1):
    print(f'{i}. {item["text"].strip()}')
```

### Step 2: 字段提取与过滤

```python
# 排除占位符
keywords_to_exclude = ['请输入', '年/月/日']

fields = []
for item in result:
    text = item['text'].strip()
    if text and not any(kw in text for kw in keywords_to_exclude):
        fields.append(text)
```

### Step 3: 中英文字段映射

```python
# 预定义映射库
name_mapping = {
    # 财务报表通用
    '营业收入': 'operatingRevenue',
    '营业成本': 'operatingCosts',
    '净利润': 'netProfit',
    '利润总额': 'totalProfit',
    
    # 银行账号
    '账号名称': 'accountName',
    '银行名称': 'bankName',
    '开户行': 'openingBank',
    '银行账户': 'bankAccount',
    
    # ... 更多见 scripts/field_mapping.py
}

# 自动映射，未知字段使用 field{N} 格式
eng_name = name_mapping.get(name, f'field{index+1}')
```

### Step 4: 字段类型智能识别

```python
def detect_field_type(name):
    amount_keywords = ['资金', '借款', '资产', '负债', '权益', '资本', 
                       '账款', '票据', '投资', '应收', '应付', '利润',
                       '费用', '收益', '收入', '成本', '税额']
    if any(kw in name for kw in amount_keywords):
        return '金额'
    
    if any(kw in name for kw in ['日期']):
        return '日期时间'
    
    if any(kw in name for kw in ['类型', '状态']):
        return '单选'
    
    return '单行文本'
```

### Step 5: 生成模板

```python
import openpyxl

# 读取模板
tpl_wb = openpyxl.load_workbook('Excel导入模板.xlsx')
tpl_ws = tpl_wb.active

# ⚠️ 表名放在 B1，不是 A1！
tpl_ws['B1'] = '表中文名'

# 清除旧数据
for row in range(5, tpl_ws.max_row + 1):
    for col in range(1, 6):
        tpl_ws.cell(row=row, column=col).value = None

# 写入字段
for i, name in enumerate(fields):
    row_num = i + 5
    eng_name = name_mapping.get(name, f'field{i+1}')
    field_type = detect_field_type(name)
    
    tpl_ws.cell(row=row_num, column=1, value=name)
    tpl_ws.cell(row=row_num, column=2, value=eng_name)
    tpl_ws.cell(row=row_num, column=3, value=field_type)
    tpl_ws.cell(row=row_num, column=4, value='否')

# 保存
tpl_wb.save('输出模板.xlsx')
```

## 标准模板结构

```
行1: A1='表中文名' | B1=实际表名
行2: A2='表英文名' | B2=entityName
行3: A3='说明'
行4: 字段中文名 | 字段英文名 | 字段类型 | 是否必填 | 字段说明
行5+: 字段数据行
```

## 字段类型说明

| 类型 | 识别关键词 | 说明 |
|-----|----------|------|
| 金额 | 资金、资产、负债、收入、成本、利润等 | 财务数值 |
| 日期时间 | 日期、时间 | 日期格式 |
| 单选 | 类型、状态 | 下拉选项 |
| 状态标签 | 状态 | 状态显示 |
| 单行文本 | 其他 | 普通文本 |

## 环境依赖

```
pip install openpyxl cnocr
```

## 注意事项

1. **表名位置**：表名必须填在 B1，A1 保持"表中文名"
2. **OCR 完整性**：识别后检查全部结果，不能遗漏任何区域
3. **残留清除**：每次生成前清除第5行及之后所有旧数据
4. **结果验证**：生成后检查前25行确认无误

## 故障排除

### cnocr 首次运行慢
首次运行会自动下载模型，后续会快很多。

### OCR 识别不准确
- 确保截图清晰
- 避免文字与背景颜色相近
- 文字方向保持正向
