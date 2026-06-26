# Excel Parser - Excel 操作工具箱

<p align="center">
  <img src="https://img.shields.io/pypi/v/excel-parser-toolkit?style=flat-square" alt="PyPI">
  <img src="https://img.shields.io/pypi/l/excel-parser-toolkit?style=flat-square" alt="License">
</p>

## 📖 简介

**Excel Parser** 是专业的 Microsoft Excel 工作簿操作工具，帮助你轻松创建、读取、编辑 Excel 文件。

### 🎯 适用场景

- 📊 数据分析报告生成
- 📋 批量数据导入导出
- 📑 多Sheet管理工作簿
- 🎨 格式化报表
- 📝 模板文件创建

## 🚀 功能特性

| 功能 | 说明 |
|------|------|
| 📖 **完整读写** | 读取/写入单元格、区域、整个工作簿 |
| 📑 **Sheet管理** | 创建、删除、选择Sheet |
| 🎨 **样式设置** | 字体、颜色、对齐、边框 |
| 📐 **公式支持** | 读取和写入公式 |
| 🔄 **格式转换** | XLSX↔CSV、XLSX→JSON |
| 📦 **批量操作** | 合并文件、拆分文件 |
| 🎯 **模板创建** | 快速生成标准模板 |

## 📦 安装

```bash
pip install openpyxl pandas
```

## 🎬 快速开始

### 读取Excel

```python
from excel_parser import ExcelParser, read_excel

# 方法1: 使用类
parser = ExcelParser('data.xlsx')
df = parser.to_dataframe()
print(f"读取 {len(df)} 行")
parser.close()

# 方法2: 便捷函数
df = read_excel('data.xlsx')
```

### 写入Excel

```python
from excel_parser import ExcelParser

parser = ExcelParser('output.xlsx')

# 创建Sheet
parser.create_sheet('销售数据')

# 写入表头
parser.write_row(1, ['日期', '销售额', '利润', '备注'])

# 追加数据
parser.append_row(['2026-01', 10000, 2000, '开门红'])
parser.append_row(['2026-02', 15000, 3500, '增长'])
parser.append_row(['2026-03', 12000, 1800, '平稳'])

# 保存
parser.save()
parser.close()

print("写入完成!")
```

### XLSX 转 CSV

```python
from excel_parser import excel_to_csv

excel_to_csv('中文数据.xlsx', '中文数据.csv')
```

## 📚 详细示例

### 创建带样式的报表

```python
from excel_parser import ExcelParser
from openpyxl.styles import Font, PatternFill, Alignment

parser = ExcelParser('report.xlsx')
parser.create_sheet('月度报告')

# 写入标题
parser.write_cell('A1', '2026年销售报告')
parser.set_style('A1', font=Font(size=16, bold=True))

# 写入表头
headers = ['日期', '产品', '销量', '销售额']
parser.write_row(3, headers)
parser.set_style('A3:D3', 
    font=Font(bold=True),
    fill=PatternFill(start_color='CCE5FF', fill_type='solid')
)

# 写入数据
data = [
    ['2026-01-01', '产品A', 100, 5000],
    ['2026-01-02', '产品B', 80, 4000],
]
parser.write_range('A4', data)

# 自动筛选
parser.autofilter('A3:D100')

parser.save()
parser.close()
```

### 批量合并Excel文件

```python
from excel_parser import ExcelParser

# 合并多个Excel文件
ExcelParser.merge_files(
    file_paths=['a.xlsx', 'b.xlsx', 'c.xlsx'],
    output_path='merged.xlsx'
)

print("合并完成!")
```

### 按列拆分Excel

```python
# 按"部门"列拆分
ExcelParser.split_by_column(
    input_path='员工列表.xlsx',
    output_dir='部门拆分',
    column='部门'
)

# 生成: 财务部.xlsx, 技术部.xlsx, 销售部.xlsx ...
```

### 创建模板

```python
from excel_parser import ExcelParser

ExcelParser.create_template(
    path='报销单模板.xlsx',
    sheets={
        '费用报销': ['日期', '部门', '姓名', '金额', '事项'],
        '差旅报销': ['出发日期', '返回日期', '地点', '交通费', '住宿费']
    }
)
```

## 📋 API 参考

### 文件操作

```python
parser = ExcelParser('file.xlsx')
parser.load('another.xlsx')     # 加载
parser.save()                   # 保存
parser.save('new.xlsx')         # 另存为
parser.close()                  # 关闭
```

### Sheet操作

```python
sheets = parser.get_sheets()    # 获取所有Sheet
parser.select_sheet('Sheet1')   # 选择Sheet
parser.create_sheet('NewSheet') # 创建Sheet
parser.delete_sheet('Sheet2')   # 删除Sheet
```

### 数据读写

```python
# 读取
value = parser.read_cell('A1')
data = parser.read_range('A1:C10')
all_data = parser.read_all()
df = parser.to_dataframe()

# 写入
parser.write_cell('A1', '值')
parser.write_row(1, [1,2,3])
parser.write_range('A1', [[1,2],[3,4]])
parser.append_row([1,2,3])
```

### 样式

```python
parser.set_style('A1', font=Font(bold=True))
parser.set_column_width(1, 20)  # 列宽
parser.autofilter('A1:D10')     # 筛选
```

## 🔧 常见问题

### Q: 如何设置列宽?
```python
parser.set_column_width(1, 20)  # A列宽20
parser.set_column_width(2, 15) # B列宽15
```

### Q: 如何设置日期格式?
```python
# 使用pandas写入时自动处理
df['date'] = pd.to_datetime(df['date'])
df.to_excel('output.xlsx')
```

### Q: 如何读取公式而非值?
```python
parser = ExcelParser('file.xlsx')
formula = parser.get_formula('A1')  # 获取公式
```

## 📊 性能

| 操作 | 10行 | 1万行 | 10万行 |
|------|------|-------|--------|
| 读取 | 0.1s | 0.5s | 3s |
| 写入 | 0.1s | 0.8s | 8s |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License