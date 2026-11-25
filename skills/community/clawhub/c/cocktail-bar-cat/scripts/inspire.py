#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""家庭调酒 · 微创新灵感引擎

用法：
  python3 scripts/inspire.py                  随机来一个灵感
  python3 scripts/inspire.py 金菲士           给这款经典的 3 档微创新
  python3 scripts/inspire.py --lever 分基酒    看这个旋钮怎么玩
  python3 scripts/inspire.py --list           列出全部旋钮与阶梯
  python3 scripts/inspire.py --home           家庭器具/换算/常备清单

原则：骨架不动、一次只动一个变量、扰动 10~30%、先做半杯。
"""
import json, os, random, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'inspiration.json'), encoding='utf-8'))
R = json.load(open(os.path.join(ROOT, 'recipes.json'), encoding='utf-8'))['recipes']
BY_NAME = {r['name']: r for r in R}
LEVERS = {l['id']: l for l in D['levers']}
# 别名表直接从 recipes.json 的 aliases 字段构建（v2.4.1 起单一数据源）：
# 旧中文名、行业异译、英文名都能查到，不需要在这里手工维护第二份清单。
ALIAS = {}
for _r in R:
    for _a in _r.get('aliases', []):
        ALIAS[_a] = _r['name']


def lookup(name):
    # 标准名优先，其次别名，最后才做模糊匹配（避免「金菲士」误命中「拉莫斯金菲士」）
    return BY_NAME.get(name) or BY_NAME.get(ALIAS.get(name))


def recipe_line(name):
    r = lookup(name)
    if not r:
        return '基准：按你手上的经典配方'
    parts = [f"{i['name']}{i['amount'] if i['amount'] is not None else ''}{i['unit']}"
             for i in r['ingredients']]
    return f"基准：{' + '.join(parts)}｜{r.get('method') or ''}/{r.get('glass') or ''}"


def show_ladder(lad):
    print(f"\n🍸 {lad['base']} · 微创新 3 档")
    print('   ' + recipe_line(lad['base']))
    print('   ' + '─' * 58)
    for s in lad['steps']:
        print(f"   {s['level']}｜{s['lever']}")
        print(f"        改动：{s['change']}")
        print(f"        预期：{s['expect']}")
        print(f"        风险：{s['risk']}")
    print('   💡 只动一个变量，先做半杯；试完记一句「改了什么 / 像不像 / 下次怎么调」')


def show_split(sp=None):
    sp = sp or random.choice(D['split_base_recipes'])
    print(f"\n🥃 分基酒拼配 · {sp['name']}（{sp['family']}）")
    print('   ' + '─' * 58)
    print(f"   切分：{sp['split']}")
    print(f"   适配：{' / '.join(sp['applies_to'])}")
    print(f"   口感：{sp['effect']}")
    print(f"   熟悉感：{sp['familiarity']}")
    print(f"   花销：{sp['budget']}")
    print('   💡 总量保持不变，主基酒别低于 70% —— 第一口要还是那杯酒')


def show_lever(key):
    l = next((x for x in D['levers']
              if key == x['id'] or key in x['name'] or x['name'] in key), None)
    if not l:
        print(f'没找到旋钮「{key}」，可用：' + '、'.join(x['name'] for x in D['levers']))
        return
    print(f"\n🎛 {l['name']} · {l['en']}（难度 {'★' * l['difficulty']}）")
    print('   ' + '─' * 58)
    print(f"   思路：{l['idea']}")
    print(f"   用量：{l['ratio']}")
    print(f"   为什么还是那杯酒：{l['why_familiar']}")
    print(f"   家庭提示：{l['home_tip']}")
    print(f"   适配：{' / '.join(l['applies_to'])}")
    rel = [s for s in D['split_base_recipes'] if l['id'] == 'split_base']
    for s in rel[:2]:
        print(f"   · {s['name']}：{s['split']}")


def show_list():
    print('\n🎛 八个旋钮（按难度）')
    for l in sorted(D['levers'], key=lambda x: x['difficulty']):
        print(f"   {'★' * l['difficulty']:<2} {l['name']:<10} {l['en']}")
    print('\n🪜 现成三档阶梯')
    for lad in D['ladders']:
        print(f"   {lad['base']} → " + ' / '.join(s['lever'] for s in lad['steps']))
    print(f"\n🥃 分基酒方案 {len(D['split_base_recipes'])} 组：")
    for s in D['split_base_recipes']:
        print(f"   · {s['family']}｜{s['name']}")
    print('\n💬 可以直接说的话：')
    for t in D['triggers']:
        print(f"   「{t}」")


def show_home():
    k = D['home_kit']
    print('\n🏠 家庭调酒备忘')
    print('\n  器具替代')
    for x in k['tool_swaps']:
        print(f"   {x['tool']:<8} → {x['swap']}")
    print('\n  换算')
    for x in k['conversions']:
        print(f"   · {x}")
    print('\n  起步酒柜（不用一次买齐）')
    for x in k['starter_bottles']:
        print(f"   · {x}")
    print('\n  习惯')
    for x in k['habits']:
        print(f"   · {x}")


def main():
    ap = argparse.ArgumentParser(description='家庭调酒微创新灵感')
    ap.add_argument('drink', nargs='?', help='经典酒名，如 金菲士')
    ap.add_argument('--lever', help='旋钮名，如 分基酒拼配')
    ap.add_argument('--list', action='store_true', help='列出全部旋钮与阶梯')
    ap.add_argument('--home', action='store_true', help='家庭器具/换算/常备清单')
    a = ap.parse_args()

    print('═' * 62)
    print(' 🐱 调酒师喵 · 微创新灵感 ｜ 骨架不动，只动一个零件')
    print('═' * 62)

    if a.list:
        show_list()
    elif a.home:
        show_home()
    elif a.lever:
        show_lever(a.lever)
    elif a.drink:
        # 旧名 / 英文名 / 行业异译先解析成标准中文名，再参与阶梯与拼配匹配
        r = lookup(a.drink)
        drink = r['name'] if r else a.drink
        if drink != a.drink:
            print(f'\n   🔎 「{a.drink}」已按标准名「{drink}」查询')
        lad = next((x for x in D['ladders'] if drink in x['base'] or x['base'] in drink), None)
        if lad:
            show_ladder(lad)
        else:
            rel = [s for s in D['split_base_recipes'] if drink in s['applies_to']]
            print(f'\n   「{drink}」暂无现成阶梯，先从这些通用旋钮里挑一个：')
            for l in D['levers'][:4]:
                print(f"   · {l['name']}：{l['ratio']}")
            if rel:
                print('\n   也可以试这组拼配：')
                show_split(rel[0])
            print('\n   💡 或运行 --list 看全部阶梯')
    else:
        show_ladder(random.choice(D['ladders']))
        show_split()
    print()


if __name__ == '__main__':
    main()
