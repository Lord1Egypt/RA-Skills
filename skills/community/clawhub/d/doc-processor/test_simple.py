#!/usr/bin/env python3
"""doc-processor v2.7.3 功能测试 - 简化版"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '/home/fuyabing/.openclaw/workspace/skills/doc-processor')
sys.path.insert(0, '/home/fuyabing/.openclaw/workspace/.venvs/doc-processor/lib/python3.12/site-packages')

from doc_processor import DocumentProcessor

test_dir = Path(tempfile.mkdtemp(prefix='doc_test_'))
print(f"测试目录：{test_dir}\n")
print("="*60)

processor = DocumentProcessor(workspace=str(test_dir))
passed = 0
failed = 0

def test(name, func):
    global passed, failed
    try:
        func()
        passed += 1
        print(f"✅ {name}")
    except Exception as e:
        failed += 1
        print(f"❌ {name}: {e}")

# P0 基础功能
print("【P0 基础功能】")
print("-"*60)

def t1():
    output = str(test_dir / "test.docx")
    processor.write(output, {'title': '测试', 'paragraphs': ['内容']})
    assert Path(output).exists()

def t2():
    content = processor.read(str(test_dir / "test.docx"))
    assert 'paragraphs' in content.data

def t3():
    output = str(test_dir / "test.xlsx")
    processor.write(output, {'sheet_name': 'S1', 'data': [['A', 'B'], [1, 2]]})
    assert Path(output).exists()

def t4():
    content = processor.read(str(test_dir / "test.xlsx"))
    assert content.type == 'excel'

def t5():
    template = str(test_dir / "tpl.docx")
    processor.write(template, {'title': '{{title}}', 'paragraphs': ['{{content}}']})
    output = str(test_dir / "filled.docx")
    result = processor.fill_template(template, {'title': 'T', 'content': 'C'}, output)
    assert Path(result).exists()

test("Word 写入", t1)
test("Word 读取", t2)
test("Excel 写入", t3)
test("Excel 读取", t4)
test("模板填充", t5)

# 总结
print("\n" + "="*60)
print(f"通过：{passed}, 失败：{failed}, 成功率：{passed/(passed+failed)*100:.0f}%")
print("="*60)

sys.exit(0 if failed == 0 else 1)
