#!/usr/bin/env python3
"""
最终版Markdown转Word转换器
"""

import re

def read_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_markdown(md_content):
    """解析Markdown内容"""
    lines = md_content.split('\n')
    parsed = []
    in_table = False
    table_rows = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 表格处理
        if '|' in line_stripped and not line_stripped.startswith('#'):
            if not in_table:
                in_table = True
                table_rows = []
            # 跳过分隔行 (|---|---|)
            if not re.match(r'^\|[-\s|]+\|$', line_stripped):
                cells = [cell.strip() for cell in line_stripped.split('|')[1:-1]]
                table_rows.append(cells)
            continue
        else:
            if in_table:
                # 结束表格
                parsed.append({'type': 'table', 'rows': table_rows})
                in_table = False
                table_rows = []
        
        if not line_stripped:
            parsed.append({'type': 'empty', 'content': ''})
        elif line_stripped.startswith('# '):
            parsed.append({'type': 'h1', 'content': line_stripped[2:]})
        elif line_stripped.startswith('## '):
            parsed.append({'type': 'h2', 'content': line_stripped[3:]})
        elif line_stripped.startswith('### '):
            parsed.append({'type': 'h3', 'content': line_stripped[4:]})
        elif line_stripped.startswith('#### '):
            parsed.append({'type': 'h4', 'content': line_stripped[5:]})
        elif line_stripped.startswith('- ') or line_stripped.startswith('• '):
            parsed.append({'type': 'bullet', 'content': line_stripped[2:]})
        else:
            parsed.append({'type': 'paragraph', 'content': line_stripped})
    
    # 处理最后一个表格
    if in_table and table_rows:
        parsed.append({'type': 'table', 'rows': table_rows})
    
    return parsed

def generate_docx_js(parsed_content, output_path):
    """生成docx-js脚本"""
    
    script = '''const { Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber, 
        HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType, BorderStyle } = require('docx');
const fs = require('fs');

const doc = new Document({
    styles: {
        default: {
            document: {
                run: { font: "宋体", size: 24 }
            }
        },
        paragraphStyles: [
            {
                id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 36, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 }
            },
            {
                id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 32, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 200, after: 200 }, outlineLevel: 1 }
            },
            {
                id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 28, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 160, after: 160 }, outlineLevel: 2 }
            },
            {
                id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 26, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 3 }
            }
        ]
    },
    sections: [{
        properties: {
            page: {
                size: { width: 11906, height: 16838 },
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        headers: {
            default: new Header({
                children: [
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        children: [new TextRun({ text: "武汉大学硕士学位论文", size: 18, font: "宋体" })]
                    })
                ]
            })
        },
        footers: {
            default: new Footer({
                children: [
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        children: [
                            new TextRun({ text: "第 ", size: 20 }),
                            new TextRun({ children: [PageNumber.CURRENT], size: 20 }),
                            new TextRun({ text: " 页", size: 20 })
                        ]
                    })
                ]
            })
        },
        children: [
'''
    
    for item in parsed_content:
        if item['type'] == 'h1':
            content = item['content'].replace('"', '\\"')
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h2':
            content = item['content'].replace('"', '\\"')
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h3':
            content = item['content'].replace('"', '\\"')
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_3,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h4':
            content = item['content'].replace('"', '\\"')
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_4,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'bullet':
            content = item['content'].replace('"', '\\"')
            script += f'''            new Paragraph({{
                bullet: {{ level: 0 }},
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'table':
            # 生成表格
            rows = item['rows']
            if len(rows) >= 2:
                col_count = len(rows[0])
                script += f'''            new Table({{
                width: {{ size: 9000, type: WidthType.DXA }},
                columnWidths: [{', '.join(['3000'] * col_count)}],
                rows: [
'''
                for row in rows:
                    cells_str = ', '.join([f'new TableCell({{ children: [new Paragraph({{ children: [new TextRun("{cell.replace("\"", "\\\"")}")] }})] }})' for cell in row])
                    script += f'''                    new TableRow({{ children: [{cells_str}] }}),
'''
                script += '''                ]
            }),
'''
        elif item['type'] == 'empty':
            script += '''            new Paragraph({ children: [] }),
'''
        else:  # paragraph
            content = item['content'].replace('"', '\\"')
            # 处理引用标记
            parts = re.split(r'(\[\d+\])', content)
            children = []
            for part in parts:
                if re.match(r'\[\d+\]', part):
                    children.append(f'new TextRun({{ text: "{part}", superScript: true, size: 20 }})')
                elif part:
                    children.append(f'new TextRun("{part}")')
            
            if children:
                children_str = ', '.join(children)
                script += f'''            new Paragraph({{
                children: [{children_str}]
            }}),
'''
    
    script += '''        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync('OUTPUT_PATH', buffer);
    console.log('Word文档已生成: OUTPUT_PATH');
});
'''
    return script.replace('OUTPUT_PATH', output_path)

def main():
    md_path = '/Users/openclaw2026/.qclaw/workspace/output/论文初稿v5.0_final.md'
    output_docx = '/Users/openclaw2026/.qclaw/workspace/output/论文初稿v5.0.docx'
    
    print(f"读取最终版Markdown: {md_path}")
    md_content = read_markdown(md_path)
    
    print("解析Markdown内容...")
    parsed = parse_markdown(md_content)
    print(f"解析完成，共 {len(parsed)} 个元素")
    
    print("生成docx-js脚本...")
    script = generate_docx_js(parsed, output_docx)
    
    script_path = '/Users/openclaw2026/.qclaw/workspace/temp/generate_final.js'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"脚本已保存: {script_path}")
    print("正在生成Word文档...")
    
    import subprocess
    result = subprocess.run(['node', script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("错误:", result.stderr)
    
    print(f"\n最终Word文档: {output_docx}")

if __name__ == "__main__":
    main()
