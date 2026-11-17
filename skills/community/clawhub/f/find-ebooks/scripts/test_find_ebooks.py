#!/usr/bin/env python3
"""
find-ebooks 测试脚本 v1.1.0
测试：安娜档案搜索 + 中文平台搜索 + 微信读书
"""

import subprocess
import sys
import json
import os

PASS = 0
FAIL = 0

def test(name, cmd, check_func=None):
    global PASS, FAIL
    print(f'\n━━━ 测试: {name} ━━━')
    print(f'命令: {cmd}')
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        output = r.stdout + r.stderr
        if r.returncode != 0:
            print(f'❌ 失败 (返回码 {r.returncode})')
            print(f'错误: {r.stderr[:300]}')
            FAIL += 1
            return None
        if check_func:
            if check_func(output):
                print(f'✅ 通过')
                PASS += 1
            else:
                print(f'❌ 断言失败')
                print(f'输出: {output[:500]}')
                FAIL += 1
                return None
        else:
            print(f'✅ 通过 (无断言)')
            PASS += 1
        return output
    except subprocess.TimeoutExpired:
        print(f'❌ 超时')
        FAIL += 1
        return None
    except Exception as e:
        print(f'❌ 异常: {e}')
        FAIL += 1
        return None


if __name__ == '__main__':
    script = os.path.join(os.path.dirname(__file__), 'find_ebooks.py')

    os.environ['PYTHONPATH'] = '/tmp/pylibs:' + os.environ.get('PYTHONPATH', '')

    # 测试1: 基本搜索 - 安娜档案
    test('基本搜索 - OpenAI Codex',
         f'python3 {script} "OpenAI Codex" --max 3 --no-weread --no-cn',
         lambda o: '慢速下载' in o and '安娜档案详情' in o)

    # 测试2: 搜索结果非空
    test('搜索结果非空',
         f'python3 {script} "OpenAI Codex" --max 2 --no-weread --no-cn',
         lambda o: '共找到' in o and '1.' in o)

    # 测试3: JSON 输出
    test('JSON 格式输出',
         f'python3 {script} "OpenAI Codex" --max 2 --json --no-weread --no-cn',
         lambda o: json.loads(o) is not None)

    # 测试4: 中文平台搜索启用
    test('中文平台搜索启用',
         f'python3 {script} "Python编程" --max 1 --no-weread',
         lambda o: '豆瓣读书' in o and '京东图书' in o and '当当网' in o)

    # 测试5: 中文平台搜索禁用
    test('中文平台搜索禁用 (--no-cn)',
         f'python3 {script} "Python编程" --max 1 --no-weread --no-cn',
         lambda o: '豆瓣读书' not in o and '京东图书' not in o)

    # 测试6: 中文平台图标 (✅ 或 🔍)
    test('中文平台图标显示',
         f'python3 {script} "Python编程" --max 1 --no-weread',
         lambda o: ('✅' in o or '🔍' in o) and '豆瓣读书' in o)

    # 测试7: 完整模式（所有平台）
    test('完整模式（安娜+中文+微信读书）',
         f'python3 {script} "Docker" --max 1',
         lambda o: '安娜档案详情' in o and ('豆瓣读书' in o or '京东图书' in o))

    # 测试8: ISBN 字段
    test('ISBN 字段',
         f'python3 {script} "OpenAI Codex" --max 2 --json --no-weread --no-cn',
         lambda o: 'isbn' in o)

    print(f'\n━━━ 测试汇总 ━━━')
    print(f'通过: {PASS}  |  失败: {FAIL}')
    if FAIL > 0:
        print('❌ 部分测试失败')
        sys.exit(1)
    else:
        print('✅ 全部测试通过')
