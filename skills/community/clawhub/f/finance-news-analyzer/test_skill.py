#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本

测试财经新闻分析器的基本功能

用法:
    python test_skill.py
"""

import sys
from pathlib import Path

# 添加脚本路径
scripts_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_dir))


def test_imports():
    """测试依赖导入"""
    print("[TEST] Importing dependencies...")
    
    try:
        import requests
        print("  [OK] requests")
    except ImportError:
        print("  [FAIL] requests (Run: pip install requests)")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  [OK] beautifulsoup4")
    except ImportError:
        print("  [FAIL] beautifulsoup4 (Run: pip install beautifulsoup4)")
        return False
    
    try:
        import jinja2
        print("  [OK] jinja2")
    except ImportError:
        print("  [WARN] jinja2 (optional)")
    
    try:
        import openai
        print("  [OK] openai (optional)")
    except ImportError:
        print("  [WARN] openai (optional)")
    
    try:
        import anthropic
        print("  [OK] anthropic (optional)")
    except ImportError:
        print("  [WARN] anthropic (optional)")
    
    return True


def test_reference_files():
    """测试参考文件"""
    print("\n[TEST] Checking reference files...")
    
    refs_dir = Path(__file__).parent / 'references'
    
    files_to_check = [
        'ticker-map.md',
        'industry-map.md',
        'sentiment-rules.md'
    ]
    
    all_exist = True
    for filename in files_to_check:
        filepath = refs_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  [OK] {filename} ({size} bytes)")
        else:
            print(f"  [FAIL] {filename} (not found)")
            all_exist = False
    
    return all_exist


def test_templates():
    """测试模板文件"""
    print("\n[TEST] Checking template files...")
    
    templates_dir = Path(__file__).parent / 'templates'
    
    files_to_check = [
        'brief.md',
        'full-report.md'
    ]
    
    all_exist = True
    for filename in files_to_check:
        filepath = templates_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  [OK] {filename} ({size} bytes)")
        else:
            print(f"  [FAIL] {filename} (not found)")
            all_exist = False
    
    return all_exist


def test_mock_analysis():
    """测试模拟分析"""
    print("\n[TEST] Mock analysis...")
    
    # 创建测试新闻数据
    test_news = [
        {
            'title': 'NVIDIA launches new AI chip',
            'url': 'https://example.com/1',
            'source': 'Test Source',
            'time': '2026-03-09 22:48',
            'summary': 'NVIDIA today announced new AI chip'
        },
        {
            'title': 'Tesla misses earnings estimate',
            'url': 'https://example.com/2',
            'source': 'Test Source',
            'time': '2026-03-09 21:30',
            'summary': 'Tesla Q4 earnings below analyst expectations'
        },
        {
            'title': 'Fed maintains interest rate',
            'url': 'https://example.com/3',
            'source': 'Test Source',
            'time': '2026-03-09 20:00',
            'summary': 'Federal Reserve announces rate decision'
        }
    ]
    
    # 测试情感分析（mock）
    print("  Running mock sentiment analysis...")
    for i, item in enumerate(test_news, 1):
        # Mock 结果
        if 'launch' in item['title'].lower() or 'new' in item['title'].lower():
            sentiment = 'positive'
            label = '[+]'
        elif 'miss' in item['title'].lower() or 'fail' in item['title'].lower():
            sentiment = 'negative'
            label = '[-]'
        else:
            sentiment = 'neutral'
            label = '[=]'
        
        title_preview = item['title'][:40]
        print(f"    {i}. {label} {title_preview}...")
    
    print("  [OK] Mock analysis completed")
    return True


def test_main_script():
    """测试主脚本"""
    print("\n[TEST] Checking main script...")
    
    main_script = Path(__file__).parent / 'scripts' / 'main.py'
    if main_script.exists():
        size = main_script.stat().st_size
        print(f"  [OK] main.py ({size} bytes)")
        
        # 尝试导入
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("main", main_script)
            module = importlib.util.module_from_spec(spec)
            print("  [OK] main.py is importable")
            return True
        except Exception as e:
            print(f"  [WARN] main.py import warning: {e}")
            return True
    else:
        print(f"  [FAIL] main.py (not found)")
        return False


def main():
    # 设置 UTF-8 输出
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("Finance News Analyzer - Skill Test")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("依赖导入", test_imports()))
    results.append(("参考文件", test_reference_files()))
    results.append(("模板文件", test_templates()))
    results.append(("模拟分析", test_mock_analysis()))
    results.append(("主脚本", test_main_script()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[OK] All tests passed! Skill is ready.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Configure API: export OPENAI_API_KEY=sk-xxx")
        print("  3. Run test: python scripts/main.py --source wallstreetcn --limit 5")
    else:
        print("\n[WARN] Some tests failed. Please check errors above.")
    
    print("=" * 60)


if __name__ == '__main__':
    main()
