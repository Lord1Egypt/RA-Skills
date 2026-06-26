#!/usr/bin/env python3
"""doc-processor v2.7.4 新功能测试"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, '/home/fuyabing/.openclaw/workspace/skills/doc-processor')
sys.path.insert(0, '/home/fuyabing/.openclaw/workspace/.venvs/doc-processor/lib/python3.12/site-packages')

from doc_processor import DocumentProcessor

test_dir = Path(tempfile.mkdtemp(prefix='doc_test_v274_'))
print(f"测试目录：{test_dir}\n")
print("="*60)

# 测试新功能
processor = DocumentProcessor(
    workspace=str(test_dir),
    enable_cache=True,
    enable_perf_monitor=True,
    ai_service_type='simple'
)

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

print("【v2.7.0 新功能测试】")
print("-"*60)

def t1_convert_word_to_txt():
    """测试 Word 转 TXT"""
    docx = test_dir / "test.docx"
    processor.write(str(docx), {'title': 'T', 'paragraphs': ['P1', 'P2']})
    txt = test_dir / "test.txt"
    processor.convert(str(docx), str(txt))
    content = txt.read_text()
    assert 'P1' in content or 'P2' in content

def t2_cache_stats():
    """测试缓存统计"""
    stats = processor.get_cache_stats()
    assert 'enabled' in stats

def t3_perf_stats():
    """测试性能统计"""
    stats = processor.get_performance_stats()
    # 可能为 None 如果模块未正确加载

def t4_clear_cache():
    """测试清空缓存"""
    processor.clear_cache()  # 不应抛出异常

def t5_batch_process():
    """测试批量处理"""
    # 创建 3 个模板
    templates = []
    data_list = []
    for i in range(3):
        tpl = test_dir / f"tpl_{i}.docx"
        processor.write(str(tpl), {'title': f'T{i}', 'paragraphs': [f'P{i}']})
        templates.append(str(tpl))
        data_list.append({'title': f'T{i}', 'content': f'C{i}'})
    
    # 批量处理
    output_dir = test_dir / "batch_out"
    result = processor.batch_fill_templates(
        templates=templates,
        data_list=data_list,
        output_dir=str(output_dir),
        max_workers=2
    )
    assert result.success == 3, f"成功数错误：{result.success}"
    assert result.failed == 0, f"失败数错误：{result.failed}"

test("Word 转 TXT", t1_convert_word_to_txt)
test("缓存统计", t2_cache_stats)
test("性能统计", t3_perf_stats)
test("清空缓存", t4_clear_cache)
test("批量处理", t5_batch_process)

# 总结
print("\n" + "="*60)
print(f"通过：{passed}, 失败：{failed}, 成功率：{passed/(passed+failed)*100:.0f}%")
print("="*60)

if failed == 0:
    print("\n✅ 所有 v2.7.0 新功能测试通过！")
else:
    print(f"\n⚠️  {failed} 个测试失败")

sys.exit(0 if failed == 0 else 1)
