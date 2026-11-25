#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""家庭买酒决策引擎 —— 从 177 款配方实时算「下一瓶买什么最值」

用法：
  python3 scripts/shop.py                          性价比总榜 + 起步建议
  python3 scripts/shop.py --have 金酒,干味美思      我已有这些，下一瓶买什么
  python3 scripts/shop.py --budget 300             预算内最优组合（贪心）
  python3 scripts/shop.py --want 马提尼,古典        想喝这几杯，反推购物清单
  python3 scripts/shop.py --split                  只为拼配买点睛酒的小酒版清单
  python3 scripts/shop.py --rank                   单瓶性价比排行

与门店补货（SKILL.md 3.1/3.4）无关：这里按风味覆盖与预算，不按销量消耗。
"""
import json, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = lambda f: json.load(open(os.path.join(ROOT, f), encoding='utf-8'))
S = L('shopping.json')
R = L('recipes.json')['recipes']

PANTRY = set(S['pantry'])
BOTTLES = {b['key']: b for b in S['bottles']}
BY_NAME = {r['name']: r for r in R}
# 别名表直接从 recipes.json 的 aliases 字段构建（v2.4.1 起单一数据源）
ALIAS = {}
for _r in R:
    for _a in _r.get('aliases', []):
        ALIAS[_a] = _r['name']


def find_recipe(name):
    # 标准名优先 → 别名（旧名/英文名/异译）→ 模糊匹配，避免误命中派生款
    if name in BY_NAME:
        return name
    if name in ALIAS and ALIAS[name] in BY_NAME:
        return ALIAS[name]
    return next((x for x in BY_NAME if name in x or x in name), None)


def needs(recipe):
    """这款酒需要『买』的材料（厨房常备不算）"""
    return {i['name'] for i in recipe['ingredients']} - PANTRY


def makeable(have):
    """用已有酒能完整做出多少款"""
    return [r['name'] for r in R if needs(r) <= have]


PARTICIPATION = {}
def participation(key):
    """这瓶出现在多少款配方里 —— 衡量用途广度，与「完整可做」互补"""
    if key not in PARTICIPATION:
        PARTICIPATION[key] = sum(1 for r in R if key in needs(r))
    return PARTICIPATION[key]


def price_of(b, small=False):
    if small and b.get('small_size'):
        return b['small_size']['price']
    return b['price']


def show_rank(have=None, limit=12):
    have = set(have or [])
    cur = len(makeable(have))
    print('\n📈 单瓶价值（基于 177 款配方实时统计）')
    print('   ' + '─' * 66)
    if have:
        print(f"   当前已有：{'、'.join(sorted(have))} → 可完整做出 {cur} 款")
        print(f"   {'下一瓶':<16}{'价格':>7}{'新增可做':>10}{'参与款数':>10}")
    else:
        print(f"   {'单瓶':<16}{'价格':>7}{'参与款数':>10}{'每百元':>10}")
    print('   ' + '─' * 66)

    rows = []
    for k, b in BOTTLES.items():
        if k in have:
            continue
        p = price_of(b)
        part = participation(k)
        gain = len(makeable(have | {k})) - cur
        rows.append((gain, part, part / max(p, 1) * 100, k, b, p))
    rows.sort(key=lambda x: (-x[0], -x[2]) if have else (-x[2], -x[1]))

    for i, (gain, part, per100, k, b, p) in enumerate(rows[:limit], 1):
        flag = ' ⭐' if i == 1 else ''
        label = b['name'][:13]
        if have:
            print(f"   {i:>2}. {label:<14}¥{p:>5}{gain:>8} 款{part:>9} 款{flag}")
        else:
            print(f"   {i:>2}. {label:<14}¥{p:>5}{part:>8} 款{per100:>9.1f} 款{flag}")
    print('   ' + '─' * 66)
    if rows:
        top = rows[0]
        if have:
            print(f"   💡 下一瓶建议：{top[4]['name']}（¥{top[5]}），能多做出 {top[0]} 款。")
        else:
            print(f"   💡 每百元效率最高：{top[4]['name']}（¥{top[5]}，参与 {top[1]} 款）。")
            print('      修饰类（味美思/苦精）单价低、用途广，比先囤基酒划算；')
            print('      但它们要配基酒才做得成东西，所以第一瓶仍建议从 --budget 起步。')
    print('   📖 参与款数＝这瓶出现在多少配方里；新增可做＝买它后能完整多做出几款。')


def show_budget(budget, have=None):
    have = set(have or [])
    spent, picked = 0, []
    print(f"\n💰 ¥{budget} 起步方案（逐瓶选边际收益最高的）")
    print('   ' + '─' * 62)
    while True:
        cur = len(makeable(have))
        best = None
        for k, b in BOTTLES.items():
            if k in have:
                continue
            p = price_of(b)
            if spent + p > budget:
                continue
            gain = len(makeable(have | {k})) - cur
            if gain <= 0:
                continue
            score = gain / max(p, 1)
            if best is None or score > best[0]:
                best = (score, gain, k, b, p)
        if not best:
            break
        _, gain, k, b, p = best
        have.add(k); spent = round(spent + p, 2)
        picked.append((b, p, gain, len(makeable(have))))
        if len(picked) >= 8:
            break
    if not picked:
        print('   当前演示价格与已有材料下没有可解锁组合；请调整预算或材料。')
        return
    for i, (b, p, gain, total) in enumerate(picked, 1):
        print(f"   {i}. {b['name']:<16} ¥{p:<5} +{gain:>2} 款 → 累计 {total:>2} 款")
        print(f"      {b['price_note']}｜{b['shelf_life']}")
    print('   ' + '─' * 62)
    print(f"   合计 ¥{spent:.2f} / 预算 ¥{budget}｜可做 {len(makeable(have))} 款"
          f"｜余 ¥{budget - spent:.2f}")
    warn = [b['name'] for b, *_ in picked if '⚠️' in b['shelf_life']]
    if warn:
        print(f"   ⏳ 短保鲜：{'、'.join(warn)} —— 这几瓶开封后尽快用完，优先买小瓶。")
    cur = len(makeable(have))
    nxt = []
    for k, b in BOTTLES.items():
        if k in have:
            continue
        g = len(makeable(have | {k})) - cur
        if g > 0:
            nxt.append((g, b['price'], b))
    if nxt:
        nxt.sort(key=lambda x: (-x[0], x[1]))
        g, p, b = nxt[0]
        print(f"   🔜 下一阶段：{b['name']} ¥{p} → 再解锁 {g} 款（累计约 ¥{spent + p:.2f}）")
    else:
        print('   🔜 下一阶段需要成套补（如波本 + 苦精），单买一瓶解锁不了新配方。')
    print('   💡 别一次买齐：先喝两周，再按 --have 问下一瓶。')


def show_want(names):
    # 旧名 / 英文名 / 行业异译先解析成标准中文名，界面也显示标准名
    canon = [find_recipe(n) or n for n in names]
    label = '、'.join(canon)
    if canon != names:
        label += '（旧名/英文名已自动匹配）'
    print(f"\n🎯 想喝：{label}")
    print('   ' + '─' * 62)
    found, missing = [], []
    for n in canon:
        k = find_recipe(n)
        (found if k else missing).append(k or n)
    if missing:
        print(f"   库里没找到：{'、'.join(missing)}（可运行 --have 或直接查配方）")
    need = set()
    for k in found:
        need |= needs(BY_NAME[k])
    buy = [BOTTLES[x] for x in sorted(need) if x in BOTTLES]
    rare = sorted(need - set(BOTTLES))
    total = sum(b['price'] for b in buy)
    for b in buy:
        alt = f"｜可买 {b['small_size']['spec']} ¥{b['small_size']['price']}" if b.get('small_size') else ''
        print(f"   · {b['name']:<16} ¥{b['price']:<5} {b['shelf_life']}{alt}")
    if rare:
        print(f"   · 罕见材料（可用近似替代或先跳过）：{'、'.join(rare[:8])}")
    cheap = sum(b['small_size']['price'] if b.get('small_size') else b['price'] for b in buy)
    print('   ' + '─' * 62)
    print(f"   合计演示金额 ¥{total:.2f}｜全选小酒版/分装 ¥{cheap:.2f}（差 ¥{total - cheap:.2f}）")
    print('   ⏳ 带 ⚠️ 的开封后尽快用完；小酒版尤其适合第一次试这类风味。')
    print('   💡 先只买能做出第一杯的最小集合，别为凑齐全库一次囤货。')


def show_split():
    print('\n🥃 只为拼配买点睛酒（不必买正装）')
    print('   ' + '─' * 62)
    total = 0
    for x in S['split_buys']:
        total += x['price']
        print(f"   · {x['purpose']:<14} → {x['buy']}  ¥{x['price']}")
        print(f"     {x['reason']}")
    print('   ' + '─' * 62)
    print(f"   全部小酒版合计演示金额 ¥{total:.2f}；能玩四种拼配，实际价格需另核。")
    print('   💡 每杯点睛只用 5~15ml，正装会喝到天荒地老。')


def main():
    ap = argparse.ArgumentParser(description='家庭买酒决策引擎')
    ap.add_argument('--have', help='已有材料，逗号分隔，如 金酒,干味美思')
    ap.add_argument('--budget', type=int, help='预算（元）')
    ap.add_argument('--want', help='想喝的酒，逗号分隔')
    ap.add_argument('--split', action='store_true', help='拼配点睛小酒版清单')
    ap.add_argument('--rank', action='store_true', help='性价比总榜')
    a = ap.parse_args()

    print('═' * 64)
    print(' 调酒师喵 · 家庭买酒决策 ｜ 从 177 款配方实时计算')
    print(' 价格为合成演示数据，不是市场报价；替换为实际价格后再采购。')
    print('═' * 64)

    have = set(x.strip() for x in a.have.split(',') if x.strip()) if a.have else set()
    unknown = have - set(BOTTLES)
    if unknown:
        print(f'\n   ⚠️ 采购库里没有：{"、".join(sorted(unknown))}（已忽略）')
        have -= unknown

    if a.split:
        show_split()
    elif a.want:
        show_want([x.strip() for x in a.want.split(',') if x.strip()])
    elif a.budget:
        show_budget(a.budget, have)
    elif a.have or a.rank:
        show_rank(have)
    else:
        show_rank()
        print('\n   📌 常用：')
        print('      --budget 300          预算内最优组合')
        print('      --have 金酒,干味美思   下一瓶买什么')
        print('      --want 马提尼,古典     反推购物清单')
        print('      --split               拼配点睛小酒版')
    print()


if __name__ == '__main__':
    main()
