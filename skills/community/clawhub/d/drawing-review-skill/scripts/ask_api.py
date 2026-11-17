#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
审图 Skill · 云端判定引擎客户端（壳版 v1.2）

⚠️ 本脚本不含任何判定规则与方法细则——它们全部在服务端，需 API Key。

用法：
  python ask_api.py --health
  python ask_api.py --rules --ids R14,R1
  python ask_api.py --rules --keyword 同号
  python ask_api.py --checklist --keyword 防水 --limit 20
  python ask_api.py --checklist --profession 装修
  python ask_api.py --review --text "同一编号在不同册指不同材料"
  python ask_api.py --review --file items.json     # [{"问题描述": "..."}, ...]

  # 方法库（怎么审）
  python ask_api.py --method list                   # 有哪些主题
  python ask_api.py --method five-steps --outline   # 该主题分几段
  python ask_api.py --method five-steps 3           # 取第 3 段正文

配置（环境变量）：
  DRAWING_REVIEW_KEY   API Key（向作者申请）
  DRAWING_REVIEW_API   服务地址（已内置，一般不用配）
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

API = os.environ.get(
    'DRAWING_REVIEW_API',
    'https://drawing-review-d1g4mjq96a0f1cdcc-1510749119.ap-shanghai.app.tcloudbase.com'
).rstrip('/')
KEY = os.environ.get('DRAWING_REVIEW_KEY', '')


def call(path, payload=None):
    url = API + path
    data = json.dumps(payload or {}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST',
                                 headers={'Content-Type': 'application/json',
                                          'X-API-Key': KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'ignore')
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': body[:300]}
    except Exception as e:
        return 0, {'error': f'连接失败：{e}（检查网络或 DRAWING_REVIEW_API）'}


def main():
    ap = argparse.ArgumentParser(description='审图 Skill 云端判定引擎客户端')
    ap.add_argument('--health', action='store_true')
    ap.add_argument('--rules', action='store_true', help='查判定规则（只给规则名与动作）')
    ap.add_argument('--ids', help='规则编号，逗号分隔，如 R14,R1')
    ap.add_argument('--keyword', help='关键词')
    ap.add_argument('--profession', help='专业，如 装修 / 给排水 / 电气')
    ap.add_argument('--limit', type=int, default=20)
    ap.add_argument('--checklist', action='store_true', help='查审图条目')
    ap.add_argument('--review', action='store_true', help='报告条目五问预检')
    ap.add_argument('--text', help='单条问题描述')
    ap.add_argument('--file', help='条目 JSON 文件（[{"问题描述":"..."}]）')
    ap.add_argument('--method', nargs='*', metavar='TOPIC [PART]',
                    help='方法库：--method list / --method 主题 / --method 主题 段号')
    ap.add_argument('--outline', action='store_true', help='配合 --method 使用：只看该主题分段')
    a = ap.parse_args()

    if a.health:
        code, d = call('/v1/health')

    elif a.rules:
        code, d = call('/v1/rules', {'ids': a.ids, 'keyword': a.keyword})

    elif a.checklist:
        code, d = call('/v1/checklist', {'keyword': a.keyword,
                                         'profession': a.profession,
                                         'limit': a.limit})

    elif a.review:
        items = []
        if a.file:
            items = json.load(open(a.file, encoding='utf-8'))
        elif a.text:
            items = [{'问题描述': a.text}]
        code, d = call('/v1/review', {'items': items})

    elif a.method is not None:
        m = a.method
        if not m or m[0].lower() == 'list':
            code, d = call('/v1/method', {})
        elif a.outline or len(m) == 1:
            code, d = call('/v1/method', {'topic': m[0], 'outline': True})
        else:
            try:
                part = int(m[1])
            except ValueError:
                print('⚠️ 段号必须是整数，例如：--method five-steps 3')
                return 1
            code, d = call('/v1/method', {'topic': m[0], 'part': part})

    else:
        print(__doc__)
        return 1

    if code == 402:
        print('⚠️ Key 缺失或无效：')
        print(json.dumps(d, ensure_ascii=False, indent=2))
        print('\n→ 向作者申请 API Key 后设置环境变量 DRAWING_REVIEW_KEY')
        return 2
    if code == 0:
        print('⚠️ 连不上服务：')
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 3

    # 方法库取正文时，直接输出正文，方便 Agent 直接读
    if a.method is not None and isinstance(d, dict) and 'content' in d:
        print(d['content'])
        return 0

    print(json.dumps(d, ensure_ascii=False, indent=2))
    return 0 if code == 200 else 1


if __name__ == '__main__':
    sys.exit(main())
