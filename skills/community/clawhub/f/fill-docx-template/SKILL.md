---
name: fill-docx-template
description: 当用户需要基于模板填充 Word 文档（.docx）、从模板生成报告、创建包含动态数据的合同，或自动化文档生成时使用此技能。包括替换普通占位符 {name} 替换文本、使用 {name|r:x,c:y} 格式标记的智能表格填充（支持从标记行开始向下填充，保留上方内容）、插入图片、批量生成文档等。如果用户提及 .docx 模板、邮件合并功能或以编程方式填写 Word 表单，请使用此技能。
---

# Word 文档模板填充指南

## ⚠️ 0. 最重要的规则：`\n` 在 docx 中不会产生换行！

**这是最高优先级的注意事项，在此之前已多次出错。**

python-docx 中 `paragraph.text = "含有\n的文本"` 不会在 Word 中产生渲染换行。`\n` 只是 XML 文本节点中的普通字符，Word 不识别为排版指令。

- **行内软换行（Shift+Enter）**：必须在 run 中插入 `<w:br/>` XML 元素
- **段落分隔（Enter）**：必须创建独立的 `<w:p>` 段落元素

**正确做法：**

```python
from lxml import etree
from docx.oxml.ns import qn

def set_paragraph_with_breaks(paragraph, text):
    """将含 \n 的文本正确写入段落，\n 转换为 <w:br/>"""
    lines = text.split('\n')
    # 清空原有 runs
    for run in list(paragraph.runs):
        run._element.getparent().remove(run._element)
    for i, line in enumerate(lines):
        if i > 0:
            # 在前一个 run 中插入换行符
            if paragraph.runs:
                etree.SubElement(paragraph.runs[-1]._element, qn('w:br'))
        if line:  # 非空行
            run = paragraph.add_run(line)

def split_into_paragraphs(doc_or_body, text, base_paragraph, style=None):
    """将含 \n\n 的文本拆分为多个独立段落，插入 base_paragraph 之前"""
    from copy import deepcopy
    blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
    if len(blocks) <= 1:
        set_paragraph_with_breaks(base_paragraph, text)
        return
    parent = base_paragraph._element.getparent()
    pos = list(parent).index(base_paragraph._element)
    for i, block in enumerate(blocks):
        new_p = deepcopy(base_paragraph._element)
        for child in list(new_p):
            if child.tag == qn('w:r'):
                new_p.remove(child)
        # 处理单 \n 为 br
        lines = block.split('\n')
        run = etree.SubElement(new_p, qn('w:r'))
        for j, line in enumerate(lines):
            if j > 0:
                etree.SubElement(run, qn('w:br'))
            t_elem = etree.SubElement(run, qn('w:t'))
            t_elem.text = line
            t_elem.set(qn('xml:space'), 'preserve')
        if style and hasattr(new_p, 'style'):
            pass  # XML 级别设置样式较复杂，可后续补充
        parent.insert(pos + i, new_p)
    parent.remove(base_paragraph._element)
```

**判断用哪种方式：**
- 文本中包含 `\n\n`（段落间距）→ 拆分为独立段落
- 文本中只有单个 `\n`（连续行）→ 用 `<w:br/>` 软换行
- 绝对不要直接把含 `\n` 的字符串赋给 `paragraph.text`

---

## 概述

本指南介绍如何使用 Python 向 Word（.docx）模板填充动态数据。支持：

- **普通占位符**：`{variable_name}` 替换文本
- **智能表格填充**：使用 `{name|r:x,c:y}` 标记在表格左侧任意位置，自动从标记行向下填充，保留上方内容，并自动调整表格行列数

### ⚠️ 1. 表格自动调整的时机与条件

**表格并非总是"提前自动扩展"** - 这取决于占位符是否被正确识别：

- ✅ **会被自动调整的情况**：当且仅当 `{name|r:x,c:y}` 格式**完全正确**且位于**该行的最左侧单元格（第一列）**时，表格会在 `DocxTemplateFiller` 初始化时立即调整为声明的行列数
- ❌ **不会被调整的情况**：如果占位符格式错误、包含空格（如 `{name | r:5, c:4}`）、或不在第一列，表格将**保持原样**，不会自动扩展或收缩

### ⚠️ 2. 普通占位符一般情况下需要被覆盖！

- 除非未提供值时保留原样

### ❌3. 任何情况下不能修改、覆盖模板文件！

### ⚠️4. 尽量使用DocxTemplateFiller类的方法实现所有功能！

## 快速开始

```python
from docx import Document
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from lxml import etree
from copy import deepcopy
import re
import os

def set_paragraph_text_with_breaks(paragraph, text):
    """将含 \n 的文本正确写入段落（辅助函数，见第0条规则）"""
    lines = text.split('\n')
    for run in list(paragraph.runs):
        run._element.getparent().remove(run._element)
    for i, line in enumerate(lines):
        if i > 0 and paragraph.runs:
            etree.SubElement(paragraph.runs[-1]._element, qn('w:br'))
        if line:
            run = paragraph.add_run(line)

class DocxTemplateFiller:
    def __init__(self, template_path):
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")
        self.doc = Document(template_path)
        self.template_path = template_path
        self.named_tables = {}

        # 初始化时扫描表格占位符
        self._process_table_placeholders()

    def _process_table_placeholders(self):
        """
        扫描所有表格的每一行第一个单元格，查找 {name|r:x,c:y} 格式
        例如：{products|r:5,c:4} 表示从当前行开始，共5行，4列
        """
        pattern = re.compile(r'\{(\w+)\|r:(\d+),c:(\d+)\}')

        for table_idx, table in enumerate(self.doc.tables):
            for row_idx, row in enumerate(table.rows):
                if len(row.cells) == 0:
                    continue

                first_cell = row.cells[0]
                text = first_cell.text.strip()
                match = pattern.search(text)

                if match:
                    name = match.group(1)
                    target_rows = int(match.group(2))
                    target_cols = int(match.group(3))

                    self.named_tables[name] = {
                        'table': table,
                        'start_row': row_idx,
                        'target_rows': target_rows,
                        'target_cols': target_cols
                    }

                    self._resize_table(table, row_idx, target_rows, target_cols)

                    new_text = pattern.sub('', first_cell.text).strip()
                    if new_text:
                        set_paragraph_text_with_breaks(first_cell.paragraphs[0], new_text)
                    else:
                        first_cell.text = ""

    def _resize_table(self, table, start_row, target_rows, target_cols):
        """调整表格大小：确保从 start_row 开始有 target_rows 行，总列数为 target_cols"""
        total_needed_rows = start_row + target_rows
        current_rows = len(table.rows)
        current_cols = len(table.columns) if table.columns else 0

        if total_needed_rows > current_rows:
            for _ in range(total_needed_rows - current_rows):
                table.add_row()
        elif total_needed_rows < current_rows:
            self._delete_rows_from_end(table, current_rows - total_needed_rows)

        if target_cols != current_cols:
            self._resize_columns(table, target_cols)

    def _delete_rows_from_end(self, table, num_rows):
        """从表格末尾删除指定行数"""
        tbl = table._tbl
        for _ in range(num_rows):
            if len(table.rows) > 0:
                tr = table.rows[-1]._tr
                tbl.remove(tr)

    def _resize_columns(self, table, target_cols):
        """调整表格列数"""
        current_cols = len(table.columns)
        tbl = table._tbl
        tblGrid = tbl.find(qn('w:tblGrid'))

        if target_cols > current_cols:
            for _ in range(target_cols - current_cols):
                gridCol = OxmlElement('w:gridCol')
                tblGrid.append(gridCol)
            for row in table.rows:
                for _ in range(target_cols - current_cols):
                    tc = OxmlElement('w:tc')
                    tcPr = OxmlElement('w:tcPr')
                    tc.append(tcPr)
                    p = OxmlElement('w:p')
                    tc.append(p)
                    row._tr.append(tc)
        elif target_cols < current_cols:
            for _ in range(current_cols - target_cols):
                if len(tblGrid) > 0:
                    tblGrid.remove(tblGrid[-1])
            for row in table.rows:
                for _ in range(current_cols - target_cols):
                    tcs = row._tr.findall(qn('w:tc'))
                    if len(tcs) > target_cols:
                        row._tr.remove(tcs[-1])

    def fill_placeholders(self, data_dict):
        """
        替换普通占位符 {key}（不包括表格定义格式）。
        ⚠️ 如果替换值包含 \n，会自动按规则0转换为真换行。
        """
        pattern = re.compile(r'\{(\w+)\}(?!\|r:\d+,c:\d+)')

        for para in self.doc.paragraphs:
            self._replace_in_paragraph(para, pattern, data_dict)

        for table in self.doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        self._replace_in_paragraph(para, pattern, data_dict)

    def _replace_in_paragraph(self, paragraph, pattern, data_dict):
        """在段落中执行替换，含 \n 的值用 set_paragraph_text_with_breaks 处理"""
        text = paragraph.text
        matches = pattern.findall(text)
        if not matches:
            return

        new_text = text
        for key in matches:
            if key in data_dict:
                placeholder = f'{{{key}}}'
                value = str(data_dict[key])
                new_text = new_text.replace(placeholder, value)

        if new_text != text:
            set_paragraph_text_with_breaks(paragraph, new_text)

    def fill_named_table(self, table_name, data):
        """
        填充指定名称的表格。
        ⚠️ 如果单元格数据包含 \n，会自动转换为 <w:br/> 软换行。
        """
        if table_name not in self.named_tables:
            raise KeyError(f"未找到名为 '{table_name}' 的表格")

        table_info = self.named_tables[table_name]
        table = table_info['table']
        start_row = table_info['start_row']
        target_rows = table_info['target_rows']
        target_cols = table_info['target_cols']

        if len(data) > target_rows:
            data = data[:target_rows]

        for row_offset, row_data in enumerate(data):
            actual_row_idx = start_row + row_offset
            if actual_row_idx >= len(table.rows):
                break
            if len(row_data) > target_cols:
                row_data = row_data[:target_cols]
            for col_idx, value in enumerate(row_data):
                if col_idx >= len(table.columns):
                    break
                cell = table.cell(actual_row_idx, col_idx)
                text = str(value)
                if '\n' in text:
                    set_paragraph_text_with_breaks(cell.paragraphs[0], text)
                else:
                    cell.text = text

    def fill_all(self, text_data=None, table_data=None):
        """一键填充所有内容"""
        if text_data:
            self.fill_placeholders(text_data)
        if table_data:
            for name, data in table_data.items():
                self.fill_named_table(name, data)

    def set_paragraph(self, paragraph, text):
        """
        设置段落文本，正确处理 \n 换行。
        短文本用 <w:br/>，含 \n\n 的长文本建议调用 split_and_insert_paragraphs。
        """
        set_paragraph_text_with_breaks(paragraph, text)

    def split_and_insert_paragraphs(self, base_paragraph, text, style=None):
        """
        将含 \n\n 的长文本拆分为多个独立段落，替换当前段落。
        每个 \n\n 分割处成为新的 docx 段落边界。
        """
        blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
        if len(blocks) <= 1:
            set_paragraph_text_with_breaks(base_paragraph, text)
            return

        parent = base_paragraph._element.getparent()
        pos = list(parent).index(base_paragraph._element)

        for i, block in enumerate(blocks):
            new_p = deepcopy(base_paragraph._element)
            for child in list(new_p):
                if child.tag == qn('w:r'):
                    new_p.remove(child)
            lines = block.split('\n')
            run = etree.SubElement(new_p, qn('w:r'))
            for j, line in enumerate(lines):
                if j > 0:
                    etree.SubElement(run, qn('w:br'))
                t_elem = etree.SubElement(run, qn('w:t'))
                t_elem.text = line
                t_elem.set(qn('xml:space'), 'preserve')
            parent.insert(pos + i, new_p)

        parent.remove(base_paragraph._element)

    def insert_paragraph_at(self, index, text, style=None):
        """在指定位置插入段落。⚠️ 如果 text 含 \n\n，自动拆分为多个段落。"""
        if '\n\n' in text:
            # 先在 index 处插入一个空段落作为锚点
            if index == -1 or index >= len(self.doc.paragraphs):
                anchor = self.doc.add_paragraph('')
            else:
                anchor = self.doc.paragraphs[index].insert_paragraph_before('')
            self.split_and_insert_paragraphs(anchor, text, style)
        else:
            if index == -1 or index >= len(self.doc.paragraphs):
                p = self.doc.add_paragraph('')
            else:
                p = self.doc.paragraphs[index].insert_paragraph_before('')
            set_paragraph_text_with_breaks(p, text)
            if style:
                p.style = style

    def insert_image(self, paragraph_index, image_path, width=None):
        """在指定段落后插入图片"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        para = self.doc.paragraphs[paragraph_index]
        run = para.add_run()
        if width:
            run.add_picture(image_path, width=Inches(width))
        else:
            run.add_picture(image_path)

    def save(self, output_path):
        self.doc.save(output_path)
        print(f"✅ 文档已生成: {os.path.abspath(output_path)}")

```
## 模板创建规范

### 1. 普通占位符

使用 `{variable_name}` 格式：
```

甲方（购方）：{company}
签署日期：{date}
合同编号：{contract_no}

```
### 2. 表格占位符（新逻辑）

**格式**：`{name|r:x,c:y}`
**位置**：表格最左侧的任意单元格（通常是某一行的第一列）
**行为**：

- 从占位符所在行开始，向下填充 x 行
- 占位符所在行会被第一个数据行覆盖
- 占位符上方的行内容完全保留
- 表格会被调整为 y 列

**示例**：
```

| 序号     | 产品名称     | 规格  | 数量  | 单价  | 金额   |
| ------ | -------- | --- | --- | --- | ---- |
| 1      | 产品A      | 规格1 | 10  | 100 | 1000 |
| {items|r:3,c:6} |			|     |     |     |      |
|        |          |     |     |     |      |

```
**说明**：

- `{items|r:3,c:6}` 放在第3行第1列（索引从0开始则为第2行）
- 程序会保留第0-2行（表头+第一行数据）
- 从第3行开始填充3行数据，覆盖占位符
- 表格自动调整为6列

### 3. 复杂模板示例

**场景**：合同中有两个表格，第一个表格上方有静态说明行
```

采购合同

甲方：{company}
乙方：{seller}

产品列表（常规采购）：
| 产品名称 | 型号 | 数量 | 单价 |
|----------|------|------|------|
| {regular|r:4,c:4} |      |      |      |
|          |      |      |      |
|          |      |      |      |
|          |      |      |      |

紧急采购项（如有）：
| 产品名称 | 型号 | 数量 | 要求 |
|----------|------|------|------|
| 说明：紧急采购需24小时内到货 |      |      |      |
| {urgent|r:2,c:4} |      |      |      |
|          |      |      |      |

总计金额：{total_amount}

```
**填充代码**：

```python
filler = DocxTemplateFiller("template.docx")

filler.fill_all(
    text_data={
        'company': '北京科技',
        'seller': '上海贸易',
        'total_amount': '¥50,000'
    },
    table_data={
        'regular': [
            ['办公椅', '人体工学', '10', '¥800'],
            ['办公桌', '1.2米', '5', '¥1500'],
            ['文件柜', '铁皮', '3', '¥600']
        ],
        'urgent': [
            ['投影仪', '4K激光', '1', '急需'],
            ['幕布', '100寸', '1', '配套']
        ]
    }
)

filler.save("contract.docx")
```

## 关键特性说明

### 0. 多行文本正确换行（重要！）

```python
filler = DocxTemplateFiller("template.docx")

# ✅ 正确：fill_placeholders 自动处理 \n
filler.fill_placeholders({
    'description': '第一段内容\n\n第二段内容\n包含两行',
})
# \n\n → 拆分为两个独立段落
# \n   → 段落内 <w:br/> 软换行

# ✅ 正确：单段落设置
filler.set_paragraph(doc.paragraphs[5], '标题\n副标题\n正文')

# ✅ 正确：多段落拆分
filler.split_and_insert_paragraphs(
    doc.paragraphs[10],
    '第一节标题\n\n第一节正文第一段\n\n第一节正文第二段'
)
```

### 1. 上方内容保护

占位符所在行上方的所有行（包括表头、说明文字、静态数据）**完全不会**被修改。

```python
# 模板：
# 第0行：表头 | 名称 | 价格 |
# 第1行：说明 | 这是说明文字 |
# 第2行：占位符 {data|r:2,c:2} | |
# 第3行：空行 | |

# 填充 data = [['A', '100'], ['B', '200']]
# 结果：
# 第0行：表头 | 名称 | 价格 |  （不变）
# 第1行：说明 | 这是说明文字 |  （不变）
# 第2行：A | 100 |  （覆盖占位符）
# 第3行：B | 200 |  （填充）
```

### 2. 自动行数调整

如果模板中占位符下方没有足够的行，程序会自动添加；过多则删除（从末尾）。

### 3. 列数自动调整

无论原表格有多少列，程序会调整为占位符声明的列数。

## 常见操作示例

### 基础填充（保留表头）

```python
filler = DocxTemplateFiller("contract.docx")
filler.fill_named_table('products', [
    ['笔记本电脑', 'ThinkPad X1', '10', '¥5000'],
    ['显示器', 'Dell 27寸', '20', '¥1500'],
])
filler.save("output.docx")
```

### 多行文本填充占位符

```python
filler = DocxTemplateFiller("report.docx")

# 含换行的文本会自动正确处理
filler.fill_placeholders({
    'summary': '第一部分：概述\n\n第二部分：详细分析\n包含（1）数据（2）结论',
    'conclusion': '综上所述，\n本项目具有重要价值。'
})
```

### 动态写入长段落

```python
# 写入一个含多段的长内容，自动拆分为独立段落
filler.split_and_insert_paragraphs(
    doc.paragraphs[3],
    '一、背景介绍\n\n这是背景的第一段...\n\n这是背景的第二段...\n\n三、小结\n这是小结内容。'
)
```

## 注意事项

### 1. 占位符位置必须正确

- 必须位于某一行的**第一个单元格**（最左侧）
- 格式必须严格为 `{name|r:数字,c:数字}`，不能有空格

### 2. 数据行数限制

提供的数据行数超过声明的 `r:x` 时，多余数据会被截断。

### 3. 单元格合并

如果占位符所在行存在合并单元格，填充行为可能不符合预期。建议占位符所在行及下方行为标准行列结构。

### 4. 样式保留

填充时会替换单元格的 `.text` 属性，这可能清除单元格内的特殊格式（如加粗、颜色）。如果需要保留格式，建议使用 `python-docx` 的低级 API 直接操作 `run` 对象。

## 快速参考

| 功能 | 方法/说明 |
|------|----------|
| **加载模板** | `filler = DocxTemplateFiller("template.docx")` |
| **普通占位符** | `{company}` → `filler.fill_placeholders({'company': '名称'})` |
| **填充表格** | `filler.fill_named_table('products', [...])` |
| **一键填充** | `filler.fill_all(text_dict, table_dict)` |
| **设置段落（自动换行）** | `filler.set_paragraph(p, text)` |
| **拆分长段落** | `filler.split_and_insert_paragraphs(p, text)` |
| **插入段落** | `filler.insert_paragraph_at(idx, text)` |
| **上方内容** | 占位符所在行上方的内容自动保留 |
| **覆盖范围** | 从占位符行开始，向下填充 `r:x` 行 |

## 后续步骤

- 如需将生成的 DOCX 转换为 PDF，请参阅 PDF 处理技能
