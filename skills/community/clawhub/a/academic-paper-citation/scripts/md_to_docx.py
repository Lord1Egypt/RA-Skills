#!/usr/bin/env python3
"""
Markdown转Word转换器
将带引用标记的Markdown转换为Word文档
"""

import re
from pathlib import Path

def read_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_markdown(md_content):
    """
    解析Markdown内容，提取结构化数据
    """
    lines = md_content.split('\n')
    parsed = []
    
    for line in lines:
        line = line.strip()
        if not line:
            parsed.append({'type': 'empty', 'content': ''})
            continue
        
        # 标题
        if line.startswith('# '):
            parsed.append({'type': 'h1', 'content': line[2:]})
        elif line.startswith('## '):
            parsed.append({'type': 'h2', 'content': line[3:]})
        elif line.startswith('### '):
            parsed.append({'type': 'h3', 'content': line[4:]})
        elif line.startswith('#### '):
            parsed.append({'type': 'h4', 'content': line[5:]})
        # 列表项
        elif line.startswith('- ') or line.startswith('• '):
            parsed.append({'type': 'bullet', 'content': line[2:]})
        # 普通段落
        else:
            parsed.append({'type': 'paragraph', 'content': line})
    
    return parsed

def generate_docx_js_script(parsed_content, output_path):
    """
    生成docx-js脚本
    """
    
    script = '''
const { Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber, 
        HeadingLevel, AlignmentType, LevelFormat, BorderStyle } = require('docx');
const fs = require('fs');

// 创建文档
const doc = new Document({
    styles: {
        default: {
            document: {
                run: {
                    font: "宋体",
                    size: 24  // 12pt = 24 half-points
                }
            }
        },
        paragraphStyles: [
            {
                id: "Heading1",
                name: "Heading 1",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 36, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 }
            },
            {
                id: "Heading2",
                name: "Heading 2",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 32, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 200, after: 200 }, outlineLevel: 1 }
            },
            {
                id: "Heading3",
                name: "Heading 3",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 28, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 160, after: 160 }, outlineLevel: 2 }
            },
            {
                id: "Heading4",
                name: "Heading 4",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 26, bold: true, font: "黑体" },
                paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 3 }
            }
        ]
    },
    sections: [{
        properties: {
            page: {
                size: {
                    width: 11906,  // A4 width in twips
                    height: 16838  // A4 height in twips
                },
                margin: {
                    top: 1440,     // 1 inch
                    right: 1440,
                    bottom: 1440,
                    left: 1440
                }
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
    
    # 处理解析后的内容
    for item in parsed_content:
        content = item['content'].replace('"', '\\"').replace('\n', ' ')
        
        if item['type'] == 'h1':
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h2':
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_2,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h3':
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_3,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'h4':
            script += f'''            new Paragraph({{
                heading: HeadingLevel.HEADING_4,
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'bullet':
            script += f'''            new Paragraph({{
                bullet: {{ level: 0 }},
                children: [new TextRun("{content}")]
            }}),
'''
        elif item['type'] == 'empty':
            script += '''            new Paragraph({ children: [] }),
'''
        else:  # paragraph
            # 处理引用标记 [数字] -> 转换为上标
            # 先分割文本和引用
            parts = re.split(r'(\[\d+\])', content)
            children = []
            for part in parts:
                if re.match(r'\[\d+\]', part):
                    # 引用标记 - 上标
                    children.append(f'new TextRun({{ text: "{part}", superScript: true, size: 20 }})')
                else:
                    if part:
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

// 保存文档
Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync('OUTPUT_PATH', buffer);
    console.log('Word文档已生成: OUTPUT_PATH');
});
'''
    
    return script

def main():
    md_path = '/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0_citations_enhanced.md'
    output_docx = '/Users/openclaw2026/.qclaw/workspace/output/论文初稿v5.0.docx'
    
    print(f"读取Markdown文件: {md_path}")
    md_content = read_markdown(md_path)
    
    print("解析Markdown内容...")
    parsed = parse_markdown(md_content)
    
    print(f"解析完成，共 {len(parsed)} 个元素")
    
    print("生成docx-js脚本...")
    script = generate_docx_js_script(parsed, output_docx)
    
    # 替换输出路径
    script = script.replace('OUTPUT_PATH', output_docx)
    
    # 保存脚本
    script_path = '/Users/openclaw2026/.qclaw/workspace/temp/generate_paper.js'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"脚本已保存: {script_path}")
    print(f"请运行: node {script_path}")

if __name__ == "__main__":
    main()
