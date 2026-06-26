# 文档处理使用示例

## 快速开始

### 1. 激活环境
```bash
source ~/.openclaw/workspace/skills/doc-processor/activate.sh
```

### 2. 读取文档
```bash
./scripts/doc-read.sh report.docx
```

### 3. 转换格式
```bash
./scripts/doc-convert.sh data.xlsx report.csv
```

## 使用场景

### 场景 1: 会议纪要处理

```bash
# 1. 读取 Word 会议纪要
./scripts/doc-read.sh meeting.docx

# 2. 提取表格（参会人员名单）
python3 doc_processor.py --action extract \
  --input meeting.docx \
  --options '{"include_tables": true}'

# 3. 转换为 CSV 便于分析
./scripts/doc-convert.sh meeting.docx attendees.csv
```

### 场景 2: 销售数据合并

```bash
# 合并多个 Excel 报表
./scripts/doc-merge.sh \
  q1.xlsx q2.xlsx q3.xlsx q4.xlsx \
  -o yearly_sales.xlsx
```

### 场景 3: 批量文档转换

```bash
# 批量 Word 转 PDF（需手动）
for doc in *.docx; do
    ./scripts/doc-convert.sh "$doc" "${doc%.docx}.csv"
done
```

### 场景 4: 数据提取与分析

```bash
# 提取 Excel 数据
python3 << 'EOF'
from doc_processor import DocumentProcessor

p = DocumentProcessor()
data = p.extract('sales.xlsx')

# 处理数据
for sheet, content in data['data'].items():
    print(f"Sheet: {sheet}")
    print(f"行数：{content['count']}")
    print(f"列：{content['columns']}")
EOF
```

## Python API 示例

### 基础使用
```python
from doc_processor import DocumentProcessor

processor = DocumentProcessor()

# 读取
content = processor.read('report.docx')
print(content.data['paragraphs'])

# 写入
processor.write('output.docx', {
    'title': '新文档',
    'paragraphs': ['内容']
})

# 转换
processor.convert('input.docx', 'output.csv')
```

### 高级使用
```python
# 批量处理
files = ['a.docx', 'b.docx', 'c.docx']
merged = processor.merge(files, 'merged.docx')

# 获取信息
info = processor.get_info('large.xlsx')
print(f"大小：{info.size_human}")
print(f"Sheet 数：{len(info.sheets)}")

# 条件读取
content = processor.read('data.xlsx', sheet_names=['Sheet1', 'Sheet3'])
```

## 故障排查

### 问题：依赖缺失
```bash
# 检查依赖
python3 check_deps.py

# 重新安装
./setup.sh
```

### 问题：文件无法读取
```bash
# 检查文件格式
file report.doc

# 检查文件权限
ls -la report.docx
```

### 问题：转换失败
```bash
# 检查目标格式是否支持
python3 doc_processor.py --action capabilities
```
