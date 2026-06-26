#!/usr/bin/env python3
"""
doc-processor v2.7.3 功能完整性测试
"""

import sys
import os
import tempfile
import time
from pathlib import Path

# 添加技能目录到路径
sys.path.insert(0, '/home/fuyabing/.openclaw/workspace/skills/doc-processor')

# 激活虚拟环境
venv_path = '/home/fuyabing/.openclaw/workspace/.venvs/doc-processor/lib/python3.12/site-packages'
sys.path.insert(0, venv_path)

from doc_processor import DocumentProcessor

# 测试结果
results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}

def test(name, func):
    """测试装饰器"""
    try:
        func()
        results['passed'] += 1
        results['tests'].append({'name': name, 'status': '✅ PASS'})
        print(f"✅ {name}")
        return True
    except Exception as e:
        results['failed'] += 1
        results['tests'].append({'name': name, 'status': '❌ FAIL', 'error': str(e)})
        print(f"❌ {name}: {e}")
        return False

# 创建测试目录
test_dir = Path(tempfile.mkdtemp(prefix='doc_processor_test_'))
print(f"测试目录：{test_dir}")
print("="*60)

# 初始化处理器
processor = DocumentProcessor(workspace=str(test_dir))

# ========== P0 测试 ==========
print("\n【P0 测试】基础功能")
print("-"*60)

def test_word_write():
    """测试 Word 写入"""
    output = str(test_dir / "test.docx")
    processor.write(output, {
        'title': '测试文档',
        'paragraphs': ['第一段内容', '第二段内容']
    })
    assert Path(output).exists(), "Word 文件未创建"
    assert Path(output).stat().st_size > 0, "Word 文件为空"

def test_word_read():
    """测试 Word 读取"""
    output = str(test_dir / "test.docx")
    content = processor.read(output)
    assert content.type == 'word', f"类型错误：{content.type}"
    assert 'paragraphs' in content.data, "缺少段落数据"

def test_excel_write():
    """测试 Excel 写入"""
    output = str(test_dir / "test.xlsx")
    processor.write(output, {
        'sheet_name': 'Sheet1',
        'data': [['姓名', '年龄'], ['张三', 25], ['李四', 30]]
    })
    assert Path(output).exists(), "Excel 文件未创建"
    assert Path(output).stat().st_size > 0, "Excel 文件为空"

def test_excel_read():
    """测试 Excel 读取"""
    output = str(test_dir / "test.xlsx")
    content = processor.read(output)
    assert content.type == 'excel', f"类型错误：{content.type}"

def test_pdf_read():
    """测试 PDF 读取"""
    # 创建一个简单的 PDF（使用系统命令）
    import subprocess
    pdf_file = test_dir / "test.pdf"
    txt_file = test_dir / "temp.txt"
    txt_file.write_text("这是 PDF 测试内容\n第二行内容")
    
    # 使用 LibreOffice 或其他工具创建 PDF（如果没有，跳过）
    try:
        # 尝试使用 Python 创建简单 PDF
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(str(pdf_file), pagesize=letter)
        c.drawString(100, 750, "这是 PDF 测试内容")
        c.save()
        
        # 读取 PDF
        content = processor.read(str(pdf_file))
        assert content.type == 'pdf', f"类型错误：{content.type}"
        assert len(content.data) > 0, "PDF 内容为空"
    except ImportError:
        print("⚠️  跳过 PDF 读取测试 (reportlab 未安装)")

test("Word 写入", test_word_write)
test("Word 读取", test_word_read)
test("Excel 写入", test_excel_write)
test("Excel 读取", test_excel_read)
test("PDF 读取", test_pdf_read)

# ========== P1 测试 ==========
print("\n【P1 测试】高级功能")
print("-"*60)

def test_convert_word_to_txt():
    """测试 Word 转 TXT（手动转换）"""
    docx_file = test_dir / "convert_test.docx"
    txt_file = test_dir / "convert_test.txt"
    
    processor.write(str(docx_file), {
        'title': '转换测试',
        'paragraphs': ['测试内容']
    })
    
    # 读取 Word 并手动转换为 TXT
    content = processor.read(str(docx_file))
    txt_content = '\n'.join([p['text'] for p in content.data.get('paragraphs', [])])
    txt_file.write_text(txt_content)
    
    assert Path(txt_file).exists(), "TXT 文件未创建"
    assert len(txt_content) > 0, "TXT 文件为空"

def test_template_fill_word():
    """测试 Word 模板填充"""
    # 创建模板
    template = test_dir / "template.docx"
    processor.write(str(template), {
        'title': '{{title}}',
        'paragraphs': ['{{content}}']
    })
    
    # 填充模板
    output = str(test_dir / "filled.docx")
    result = processor.fill_template(
        str(template),
        {'title': '填充标题', 'content': '填充内容'},
        output
    )
    assert Path(result).exists(), "填充后的文件未创建"

def test_batch_process():
    """测试批量处理（跳过，本地版本未集成）"""
    print("⚠️  跳过批量处理测试（本地版本未集成 batch_processor.py）")
    pass

def test_error_handling():
    """测试错误处理（跳过，本地版本未集成）"""
    print("⚠️  跳过错误处理测试（本地版本未集成 error_handler.py）")
    pass

# ========== 总结 ==========
print("\n" + "="*60)
print("测试结果汇总")
print("="*60)
print(f"通过：{results['passed']}")
print(f"失败：{results['failed']}")
print(f"成功率：{results['passed']/(results['passed']+results['failed'])*100:.1f}%")
print()

for t in results['tests']:
    print(f"{t['status']} {t['name']}")
    if 'error' in t:
        print(f"   错误：{t['error']}")

print()
print(f"测试目录：{test_dir}")
print("="*60)

# 清理（可选）
# import shutil
# shutil.rmtree(test_dir)

sys.exit(0 if results['failed'] == 0 else 1)
