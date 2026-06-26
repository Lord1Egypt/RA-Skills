---
name: docx-tool
description: 使用 python-docx 库创建、读取和修改 Word 文档 (.docx)。支持文本、段落、表格、样式、图片等操作。
---

# DOCX 文档操作工具

使用 python-docx 库进行 Word 文档的创建、读取和修改。

## 前置要求

已安装 python-docx：
```bash
pip install python-docx
```

## 常用操作

### 创建新文档

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 创建新文档
doc = Document()

# 添加标题
doc.add_heading('文档标题', level=1)

# 添加段落
p = doc.add_paragraph('这是一个普通段落。')
p.add_run('这是加粗文字').bold = True
p.add_run('，这是普通文字。')

# 保存文档
doc.save('output.docx')
```

### 读取现有文档

```python
from docx import Document

doc = Document('input.docx')

# 读取所有段落文本
for para in doc.paragraphs:
    print(para.text)

# 读取表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
```

### 添加表格

```python
from docx import Document

doc = Document()

# 创建 3x3 表格
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

# 填充表头
hdr_cells = table.rows[0].cells
hdr_cells[0].text = '姓名'
hdr_cells[1].text = '年龄'
hdr_cells[2].text = '城市'

# 填充数据
row_cells = table.rows[1].cells
row_cells[0].text = '张三'
row_cells[1].text = '25'
row_cells[2].text = '北京'

doc.save('table.docx')
```

### 设置样式

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# 添加标题并设置样式
heading = doc.add_heading('标题', level=1)
heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 添加段落并设置格式
p = doc.add_paragraph()
run = p.add_run('自定义格式文字')
run.font.size = Pt(14)
run.font.bold = True
run.font.color.rgb = RGBColor(255, 0, 0)

# 设置段落间距
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(12)

doc.save('styled.docx')
```

### 添加图片

```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_heading('带图片的文档', level=1)

# 添加图片
doc.add_picture('image.png', width=Inches(5.0))

# 添加图片说明
doc.add_paragraph('图 1: 示例图片', style='Caption')

doc.save('with_image.docx')
```

### 修改现有文档

```python
from docx import Document

doc = Document('existing.docx')

# 在开头插入段落
doc.paragraphs[0].insert_paragraph_before('新插入的段落')

# 修改现有段落
if doc.paragraphs:
    doc.paragraphs[0].text = '修改后的文字'

# 添加新内容到末尾
doc.add_paragraph('添加到末尾的段落')

doc.save('modified.docx')
```

## 可用表格样式

- `Table Grid` - 基础网格
- `Light Grid Accent 1` - 浅色网格
- `Medium Grid 1` - 中等网格
- `Medium Grid 2` - 中等网格 2
- `Medium Grid 3` - 中等网格 3

## 段落对齐方式

- `WD_ALIGN_PARAGRAPH.LEFT` - 左对齐
- `WD_ALIGN_PARAGRAPH.CENTER` - 居中
- `WD_ALIGN_PARAGRAPH.RIGHT` - 右对齐
- `WD_ALIGN_PARAGRAPH.JUSTIFY` - 两端对齐

## 注意事项

1. **文件格式**: 仅支持 .docx 格式，不支持 .doc 格式
2. **兼容性**: 复杂格式在不同 Word 版本间可能有差异
3. **图片**: 支持的格式包括 PNG, JPEG, GIF, BMP
4. **字体**: 使用系统已安装的字体
