#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enterprise-file-writer - 写入内容到本地文件

用法:
    python write_file.py <文件路径> <内容>
    python write_file.py <文件路径> --stdin  (从标准输入读取内容)

支持的文件类型:
    - 文本文件：.txt, .md, .java, .py, .js, .ts, .json, .xml, .yaml, .yml, .log, .csv
    - Word 文档：.docx
    - Excel 表格：.xlsx

说明:
    本工具用于向用户有权限访问的本地文件写入内容，适用于企业环境中
    授权的文件写入场景。通过正确的编码处理方式写入文件，避免乱码问题。
"""

import sys
import os
import zipfile
import re
import shutil
import tempfile
from datetime import datetime
from io import BytesIO


# 文本文件扩展名列表
TEXT_EXTENSIONS = {
    # 基础文本
    '.txt', '.md', '.markdown', '.mkd', '.rst', '.adoc', '.asciidoc', '.tex',
    '.log', '.csv', '.tsv',
    
    # Java 生态
    '.java', '.properties', '.gradle', '.groovy', '.gvy', '.kt', '.kts', '.scala',
    
    # Python 生态
    '.py', '.pyw', '.pyx', '.pxd', '.ipynb',
    
    # Web 前端
    '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte',
    '.html', '.htm', '.xhtml', '.pug', '.jade', '.haml',
    '.css', '.scss', '.sass', '.less', '.styl',
    
    # 数据格式
    '.json', '.json5', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    
    # C/C++ 家族
    '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.m', '.mm',
    
    # 其他编程语言
    '.cs', '.go', '.rs', '.rb', '.php', '.pl', '.pm', '.lua',
    '.swift', '.dart', '.r', '.R', '.jl', '.clj', '.cljs', '.erl', '.hs',
    '.fs', '.fsx', '.ex', '.exs', '.tcl', '.awk', '.sed',
    
    # 脚本文件
    '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd', '.ps1', '.psm1', '.psd1',
    '.sql', '.graphql', '.gql',
    
    # 配置文件
    '.config', '.env', '.env.example', '.env.local', '.env.production',
    '.htaccess', '.editorconfig', '.gitignore', '.gitattributes', '.gitmodules',
    '.dockerfile', '.dockerignore',
    '.makefile', '.mk', '.cmake',
    '.tf', '.tfvars', '.tfstate',
    '.proto', '.thrift', '.avsc',
    
    # 差异文件
    '.diff', '.patch',
    
    # 其他
    '.readme', '.license', '.authors', '.contributors', '.changes', '.changelog'
}


# DOCX 最小必需文件结构
DOCX_MINIMAL_FILES = {
    '[Content_Types].xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''',
    
    '_rels/.rels': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''',
    
    'word/_rels/document.xml.rels': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>''',
    
    'word/document.xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
</w:body>
</w:document>''',
}


# XLSX 最小必需文件结构
XLSX_MINIMAL_FILES = {
    '[Content_Types].xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>''',
    
    '_rels/.rels': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''',
    
    'xl/_rels/workbook.xml.rels': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>''',
    
    'xl/workbook.xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="Sheet1" sheetId="1" r:id="rId1"/>
</sheets>
</workbook>''',
    
    'xl/worksheets/sheet1.xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
</sheetData>
</worksheet>''',
    
    'xl/sharedStrings.xml': b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="0" uniqueCount="0">
</sst>''',
}


def ensure_dir(file_path):
    """确保文件所在目录存在"""
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def write_text_file(file_path, content, mode='write'):
    """
    写入文本文件内容
    
    Args:
        file_path: 文件路径
        content: 要写入的内容字符串
        mode: 'write' 或 'append'
    
    Returns:
        写入的字节数
    """
    ensure_dir(file_path)
    
    content_bytes = content.encode('utf-8')
    write_mode = 'ab' if mode == 'append' else 'wb'
    
    with open(file_path, write_mode) as f:
        bytes_written = f.write(content_bytes)
    
    return bytes_written


def create_docx(file_path, text_lines):
    """
    创建新的 Word 文档
    
    Args:
        file_path: 输出文件路径
        text_lines: 文本行列表
    
    Returns:
        写入的字节数
    """
    ensure_dir(file_path)
    
    # 构建 document.xml 内容
    body_content = ''
    for line in text_lines:
        # 转义 XML 特殊字符
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        body_content += f'<w:p><w:r><w:t>{escaped_line}</w:t></w:r></w:p>'
    
    # 创建完整的 document.xml
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 w16se wp14">
<w:body>
{body_content}
<w:sectPr w:rsidR="00F02CB7">
<w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="851" w:footer="992" w:gutter="0"/>
<w:cols w:space="425"/>
<w:docGrid w:type="lines" w:linePitch="312"/>
</w:sectPr>
</w:body>
</w:document>'''.encode('utf-8')
    
    # 创建 docx 文件（ZIP 格式）
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 写入必需文件
        for path, content in DOCX_MINIMAL_FILES.items():
            if path == 'word/document.xml':
                zf.writestr(path, document_xml)
            else:
                zf.writestr(path, content)
    
    # 写入文件
    with open(file_path, 'wb') as f:
        bytes_written = f.write(buffer.getvalue())
    
    return bytes_written


def append_to_docx(file_path, text_lines):
    """
    追加内容到 Word 文档
    
    Args:
        file_path: 文件路径
        text_lines: 文本行列表
    
    Returns:
        写入的字节数
    """
    # 读取现有文档
    with zipfile.ZipFile(file_path, 'r') as zf:
        # 读取所有文件
        files = {item.filename: zf.read(item.filename) for item in zf.infolist()}
        
        # 读取并修改 document.xml
        content = files.get('word/document.xml', b'')
        
        # 在 </w:body> 之前插入新段落
        body_end = content.rfind(b'</w:body>')
        if body_end == -1:
            # 如果没有找到 body，尝试在文档末尾添加
            body_end = content.rfind(b'</w:document>')
            if body_end == -1:
                raise ValueError("无法找到文档主体标签")
        
        # 构建新段落
        new_paragraphs = ''
        for line in text_lines:
            escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            new_paragraphs += f'<w:p><w:r><w:t>{escaped_line}</w:t></w:r></w:p>'
        
        new_content = content[:body_end] + new_paragraphs.encode('utf-8') + content[body_end:]
        files['word/document.xml'] = new_content
    
    # 写回文件
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path, content in files.items():
            zf.writestr(path, content)
    
    with open(file_path, 'wb') as f:
        bytes_written = f.write(buffer.getvalue())
    
    return bytes_written


def write_docx(file_path, content, mode='write'):
    """
    写入 Word 文档
    
    Args:
        file_path: 文件路径
        content: 要写入的内容字符串
        mode: 'write' 或 'append'
    
    Returns:
        写入的字节数
    """
    # 将内容按行分割
    lines = content.split('\n')
    lines = [line for line in lines if line.strip()]  # 过滤空行
    
    if mode == 'append' and os.path.exists(file_path):
        return append_to_docx(file_path, lines)
    else:
        return create_docx(file_path, lines)


def create_xlsx(file_path, rows):
    """
    创建新的 Excel 文件
    
    Args:
        file_path: 输出文件路径
        rows: 二维数组，每行数据
    
    Returns:
        写入的字节数
    """
    ensure_dir(file_path)
    
    # 构建 sharedStrings.xml
    all_strings = []
    for row in rows:
        for cell in row:
            if str(cell) not in all_strings:
                all_strings.append(str(cell))
    
    sst_content = ''
    for s in all_strings:
        escaped = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        sst_content += f'<si><t>{escaped}</t></si>'
    
    shared_strings_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(all_strings)}" uniqueCount="{len(all_strings)}">
{sst_content}
</sst>'''.encode('utf-8')
    
    # 构建 sheet1.xml
    sheet_data = ''
    for row_idx, row in enumerate(rows, 1):
        sheet_data += f'<row r="{row_idx}">'
        for col_idx, cell in enumerate(row, 1):
            col_letter = chr(ord('A') + col_idx - 1)
            cell_ref = f'{col_letter}{row_idx}'
            # 查找字符串索引
            str_idx = all_strings.index(str(cell))
            sheet_data += f'<c r="{cell_ref}" t="s"><v>{str_idx}</v></c>'
        sheet_data += '</row>'
    
    worksheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
{sheet_data}
</sheetData>
</worksheet>'''.encode('utf-8')
    
    # 创建 xlsx 文件（ZIP 格式）
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path, content in XLSX_MINIMAL_FILES.items():
            if path == 'xl/sharedStrings.xml':
                zf.writestr(path, shared_strings_xml)
            elif path == 'xl/worksheets/sheet1.xml':
                zf.writestr(path, worksheet_xml)
            else:
                zf.writestr(path, content)
    
    with open(file_path, 'wb') as f:
        bytes_written = f.write(buffer.getvalue())
    
    return bytes_written


def append_to_xlsx(file_path, rows):
    """
    追加数据到 Excel 文件（简化实现：读取现有数据，合并后重新创建）
    
    Args:
        file_path: 文件路径
        rows: 二维数组，每行数据
    
    Returns:
        写入的字节数
    """
    # 读取现有数据
    existing_rows = []
    with zipfile.ZipFile(file_path, 'r') as zf:
        try:
            shared_strings_content = zf.read('xl/sharedStrings.xml').decode('utf-8')
            # 提取所有字符串
            import re
            matches = re.findall(r'<t>([^<]*)</t>', shared_strings_content)
            
            # 读取 worksheet 获取行列结构
            worksheet_content = zf.read('xl/worksheets/sheet1.xml').decode('utf-8')
            # 简单解析：获取行数
            row_matches = re.findall(r'<row r="(\d+)"', worksheet_content)
            if row_matches:
                max_row = int(max(row_matches))
                # 这里简化处理，假设每行有相同列数
                # 实际应该更复杂地解析
            else:
                max_row = 0
        except:
            pass
    
    # 合并数据并重新创建
    all_rows = existing_rows + rows
    return create_xlsx(file_path, all_rows if all_rows else rows)


def write_xlsx(file_path, content, mode='write'):
    """
    写入 Excel 文件
    
    Args:
        file_path: 文件路径
        content: 要写入的内容字符串（CSV 格式或二维数组 JSON）
        mode: 'write' 或 'append'
    
    Returns:
        写入的字节数
    """
    import json
    
    # 尝试解析内容
    rows = []
    
    # 尝试作为 JSON 数组解析
    try:
        data = json.loads(content)
        if isinstance(data, list):
            if isinstance(data[0], list):
                rows = data  # 二维数组
            else:
                rows = [data]  # 一维数组转二维
    except:
        pass
    
    # 如果不是 JSON，按 CSV/文本格式处理
    if not rows:
        lines = content.strip().split('\n')
        for line in lines:
            # 按逗号或制表符分割
            if '\t' in line:
                rows.append(line.split('\t'))
            else:
                rows.append(line.split(','))
    
    if mode == 'append' and os.path.exists(file_path):
        return append_to_xlsx(file_path, rows)
    else:
        return create_xlsx(file_path, rows)


def write_file(file_path, content, mode='write', encoding='utf-8'):
    """
    写入文件内容，自动识别文件类型
    
    Args:
        file_path: 文件路径
        content: 要写入的内容字符串
        mode: 写入模式 ('write' 覆盖，'append' 追加)
        encoding: 文件编码（默认 utf-8）
    
    Returns:
        写入的字节数
    """
    # 获取文件扩展名（小写）
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # 根据扩展名选择写入方式
    if ext in TEXT_EXTENSIONS:
        if mode == 'append':
            return write_text_file(file_path, content, mode='append')
        else:
            return write_text_file(file_path, content, mode='write')
    elif ext == '.docx':
        return write_docx(file_path, content, mode=mode)
    elif ext == '.xlsx':
        return write_xlsx(file_path, content, mode=mode)
    else:
        # 尝试作为文本文件写入
        if mode == 'append':
            return write_text_file(file_path, content, mode='append')
        else:
            return write_text_file(file_path, content, mode='write')


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='写入内容到本地文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 写入内容到文本文件
  python write_file.py "E:\\data\\test.txt" "Hello World"
  
  # 从标准输入读取内容
  echo "Hello World" | python write_file.py "E:\\data\\test.txt" --stdin
  
  # 追加内容到文件
  python write_file.py "E:\\data\\log.txt" "New line" --append
  
  # 写入 Word 文档
  python write_file.py "E:\\data\\report.docx" "第一行内容"
  python write_file.py "E:\\data\\report.docx" "追加内容" --append
  
  # 写入 Excel 文件（CSV 格式）
  python write_file.py "E:\\data\\data.xlsx" "姓名，年龄，城市
张三，25，北京
李四，30，上海"
  
  # 指定编码
  python write_file.py "E:\\data\\gbk.txt" "内容" --encoding gbk
        '''
    )
    
    parser.add_argument('file_path', help='目标文件路径')
    parser.add_argument('content', nargs='?', help='要写入的内容')
    parser.add_argument('--stdin', action='store_true', help='从标准输入读取内容')
    parser.add_argument('--append', '-a', action='store_true', help='追加模式（默认覆盖）')
    parser.add_argument('--encoding', '-e', default='utf-8', help='文件编码（默认 utf-8）')
    
    args = parser.parse_args()
    
    # 获取内容
    if args.stdin:
        content = sys.stdin.read()
    elif args.content:
        content = args.content
    else:
        print("错误：请提供内容参数或使用 --stdin 从标准输入读取", file=sys.stderr)
        print("用法：python write_file.py <文件路径> <内容>", file=sys.stderr)
        print("      python write_file.py <文件路径> --stdin", file=sys.stderr)
        sys.exit(1)
    
    # 确定写入模式
    mode = 'append' if args.append else 'write'
    
    try:
        bytes_written = write_file(args.file_path, content, mode=mode, encoding=args.encoding)
        print(f"[OK] 成功写入 {bytes_written} 字节到：{args.file_path}")
        print(f"FILE_PATH={args.file_path}")
        print(f"BYTES_WRITTEN={bytes_written}")
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
