#!/usr/bin/env python3
"""
ccy-ocr-local 图表识别回归测试脚本
验证当前版本在示例图上的基本功能是否可用。
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/chen/disk0/disk_ntfs/openclaw/main/workspace')
SCRIPT = ROOT / 'skills/ccy-ocr-local/scripts/chart_ocr.py'
IMAGE = ROOT / '饼图示例.jpg'


def run(chart_type: str):
    cmd = ['python3', str(SCRIPT), str(IMAGE), '--chart-type', chart_type, '--json']
    try:
        out = subprocess.check_output(cmd, text=True, timeout=120)
        return json.loads(out)
    except subprocess.TimeoutExpired:
        print(f"❌ {chart_type}: 超时")
        return None
    except Exception as e:
        print(f"❌ {chart_type}: {e}")
        return None


def test_dashboard():
    print("🧪 测试 dashboard 模式...")
    dashboard = run('dashboard')
    if not dashboard:
        return False
    if dashboard['chart_type'] != 'dashboard':
        print("❌ dashboard 模式未返回 dashboard")
        return False
    region_types = [c['chart_type'] for c in dashboard['charts']]
    if 'pie' not in region_types:
        print("❌ dashboard 未识别出 pie")
        return False
    if 'bar' not in region_types:
        print("❌ dashboard 未识别出 bar")
        return False
    if 'line' not in region_types:
        print("❌ dashboard 未识别出 line")
        return False
    print("✅ dashboard 模式通过")
    return True


def test_auto():
    print("🧪 测试 auto 模式...")
    auto = run('auto')
    if not auto:
        return False
    if auto['chart_type'] not in {'pie', 'bar', 'line', 'table', 'unknown'}:
        print("❌ auto 模式返回未知类型")
        return False
    print("✅ auto 模式通过")
    return True


def test_line():
    print("🧪 测试 line 模式...")
    line = run('line')
    if not line:
        return False
    if line['chart_type'] != 'line':
        print("❌ line 模式未返回 line")
        return False
    if not isinstance(line.get('data_points', []), list):
        print("❌ data_points 不是列表")
        return False
    if len(line.get('data_points', [])) < 1:
        print("❌ data_points 数量不足")
        return False
    print("✅ line 模式通过")
    return True


def test_pie():
    print("🧪 测试 pie 模式...")
    pie = run('pie')
    if not pie:
        return False
    if pie['chart_type'] != 'pie':
        print("❌ pie 模式未返回 pie")
        return False
    if not isinstance(pie.get('segments', []), list):
        print("❌ segments 不是列表")
        return False
    print("✅ pie 模式通过")
    return True


def test_bar():
    print("🧪 测试 bar 模式...")
    bar = run('bar')
    if not bar:
        return False
    if bar['chart_type'] != 'bar':
        print("❌ bar 模式未返回 bar")
        return False
    if not isinstance(bar.get('categories', []), list):
        print("❌ categories 不是列表")
        return False
    print("✅ bar 模式通过")
    return True


def main():
    print("📊 ccy-ocr-local 图表识别回归测试")
    print("=" * 50)
    results = []
    results.append(('dashboard', test_dashboard()))
    results.append(('auto', test_auto()))
    results.append(('line', test_line()))
    results.append(('pie', test_pie()))
    results.append(('bar', test_bar()))
    print("=" * 50)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"结果: {passed}/{total} 通过")
    if passed == total:
        print("🎉 所有测试通过")
        return 0
    else:
        print("❌ 部分测试失败")
        for name, ok in results:
            if not ok:
                print(f"  - {name} 失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())
