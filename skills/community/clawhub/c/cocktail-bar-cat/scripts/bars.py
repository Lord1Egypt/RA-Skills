#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""有意思的酒单 · 公开可查的吧台地图 查询器（v2.6.2）

收录看的是「酒单有没有想法」，不是店有没有上榜。
酒单是连续出版物，不是静态清单：每杯都带快照日期，
时效按运行当天实时计算（不再依赖建档时写死的标签），默认不推历史酒款；
用 --as-of 指定日期可复现任意时点的判断；只有酒单概念的店绝不编配方。

用法：
  python3 scripts/bars.py --map                   城市地图（全部店，按城市分组）
  python3 scripts/bars.py --stats                覆盖统计 + 时效分布 + 诚实边界
  python3 scripts/bars.py --bars                 逐店完整档案（酒单想法/为什么有意思）
  python3 scripts/bars.py --city 西安             按城市
  python3 scripts/bars.py --idea 在地食材         按酒单思路
  python3 scripts/bars.py --tier 独立小店         按店型
  python3 scripts/bars.py --independent          只看独立/社区/主题概念店
  python3 scripts/bars.py --concept-only         只看「只有概念、没有配方」的店
  python3 scripts/bars.py --rotating             只看持续换季 / 无酒单的吧台
  python3 scripts/bars.py --taste                查看公开口味争议
  python3 scripts/bars.py --bar "MIXY BAR"       查单店（含多期酒单快照对照）
  python3 scripts/bars.py --snapshots            所有多期快照对照
  python3 scripts/bars.py --snapshots "MIXY BAR" 单店的多期快照对照
  python3 scripts/bars.py --freshness recent    按时效筛（recent/aging/historical/unknown）
  python3 scripts/bars.py --archive              只看历史酒单快照
  python3 scripts/bars.py --stale                列出所有已过期/存疑的酒款
  python3 scripts/bars.py --anchor 得其利         按经典锚点找同源改编
  python3 scripts/bars.py --flavor 咸鲜           按风味（含口语同义词）
  python3 scripts/bars.py --mood 失落             按情绪（自动过甜度闸门）
  python3 scripts/bars.py --concepts             可照搬的整套酒单骨架
  python3 scripts/bars.py --levers               微调手法
  python3 scripts/bars.py --list                 当前/近期快照中的可复刻招牌
  python3 scripts/bars.py --as-of 2028-01-01 --stats   预览未来某天的时效（回归测试）
  python3 scripts/bars.py 南山 South Mountain     查单杯完整档案（历史款会明确标注）
  python3 scripts/bars.py --json 周至得其利       输出原始 JSON
"""
import argparse, collections, datetime as _dt, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'bar_signatures.json'), encoding='utf-8'))
BARS = {b['name']: b for b in D['bars']}
SIGS = D['signatures']
BY_NAME = {s['name']: s for s in SIGS}
BY_ID = {s['id']: s for s in SIGS}
SOURCES = {s['id']: s for s in D['sources']}

# ── v2.6.1 时效 ────────────────────────────────────────────────
FRESH_LABEL = {
    'recent': '近期快照（仍需核对当日酒单）',
    'aging': '资料偏旧（大概率已换季）',
    'historical': '历史酒单（已下架 / 换季，不作在售承诺）',
    'unknown': '快照日期不详',
}
FRESH_MARK = {'recent': '🟢', 'aging': '🟡', 'historical': '⚪', 'unknown': '⚪'}
MENU_STATUS_LABEL = {
    'rotating': '持续换季型（每期酒单可能完全不同）',
    'no_menu': '无酒单 / 按客人口味现调',
    'seasonal': '按季节换酒单',
    'stable': '相对稳定的固定酒单',
    'unknown': '未确认是否换季',
}
# ── 运行时时效（v2.6.2）────────────────────────────────────────
# 静态 freshness 字段保留为「建档基线」，实际判断一律走下面这套。
# 阈值与 freshness_policy.freshness_computation 保持一致。
FRESH_RECENT_MONTHS = 18
FRESH_AGING_MONTHS = 48
AS_OF = _dt.date.today()


def snapshot_date(text):
    """'2026' / '2019-2021' / '2026-05-01' → 快照日期。
    只有年份时按该年 1 月 1 日保守估计（宁可把资料算旧，不把它算新）。"""
    if not text:
        return None
    s = str(text)
    m = re.search(r'(20\d{2})-(\d{1,2})-(\d{1,2})', s)
    if m:
        try:
            return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    ys = [int(y) for y in re.findall(r'20\d{2}', s)]
    return _dt.date(max(ys), 1, 1) if ys else None


def age_months(text):
    d = snapshot_date(text)
    return None if d is None else max(0, int((AS_OF - d).days / 30.44))


def classify(text):
    m = age_months(text)
    if m is None:
        return 'unknown'
    if m <= FRESH_RECENT_MONTHS:
        return 'recent'
    if m <= FRESH_AGING_MONTHS:
        return 'aging'
    return 'historical'


def eff_freshness(s):
    return classify(s.get('menu_snapshot'))


def eff_bar_freshness(b):
    return classify(b.get('source_date') or b.get('last_verified'))


def eff_status(s):
    f = eff_freshness(s)
    if f == 'historical':
        return 'past_menu'
    if BARS.get(s['bar'], {}).get('menu_status') in ('rotating', 'no_menu'):
        return 'rotating'
    return {'recent': 'current_snapshot', 'aging': 'aging_snapshot',
            'unknown': 'unknown'}[f]


def active_sigs():
    return [s for s in SIGS if eff_freshness(s) != 'historical']


def age_text(text):
    m = age_months(text)
    return f'距今 {m} 个月' if m is not None else '日期不详'


def fresh_line(s, prefix=''):
    fr = eff_freshness(s)
    snap = s.get('menu_snapshot') or '未标注'
    return (f"{prefix}{FRESH_MARK.get(fr, '⚪')} 酒单快照 {snap} · {age_text(s.get('menu_snapshot'))} "
            f"· {FRESH_LABEL.get(fr, fr)}")


def stale_warning(fr, prefix='  '):
    if fr in ('aging', 'historical', 'unknown'):
        print(f"{prefix}⚠️ 不作「当前在售」承诺；到店请看当日酒单或直接问调酒师")


# 情绪 → 偏好风味 / 需避开的信号（与 mood-mapping.json 的甜度规则对齐）
MOOD = {
    '失落': {'want': ['清爽', '茶香', '草本', '醇厚', '复古', '干冽', '威士忌', '经典', '咸鲜'],
            'avoid_words': ['甜品', '小甜酒', '绵密', '椰子'], 'note': '低甜闸门：甜味材料 ≤15%，偏甜招牌一律先给减糖版'},
    '疲惫': {'want': ['清爽', '茶香', '长饮', '气泡', '草本', '轻盈', '极简'],
            'avoid_words': ['甜品', '小甜酒', '绵密'], 'note': '低甜闸门 + 优先长饮 / 慢饮'},
    '治愈': {'want': ['清爽', '茶香', '草本', '醇厚', '干冽'],
            'avoid_words': ['甜品', '小甜酒'], 'note': '同「失落」规则'},
    '庆祝': {'want': ['气泡', '花香', '果香', '热带', '轻盈', '辛香'],
            'avoid_words': [], 'note': '可以放开甜度与仪式感'},
    '好奇': {'want': ['鲜味', '咸甜', '复杂', '实验性', '创意', '多质地', '澄清', '咸鲜'],
            'avoid_words': [], 'note': '优先给「喝得懂层次」的技术流招牌'},
    '想喝懂': {'want': ['鲜味', '复杂', '咸甜', '多质地', '澄清', '复古', '咸鲜'],
             'avoid_words': [], 'note': '优先给能作对照实验的招牌'},
}
# 明确偏甜 / 甜品感：失落与疲惫场景要先减糖
SWEET_IDS = {'hns_air', 'cmyk_avocado', 'coa_coconut', 'longfong_apple',
             'sanyou_maotai', 'clan_dongning', 'kinsman_milk', 'pop_liangzong',
             'mixy_salute', 'vibes_jiulong', 'shifter_bamboo'}
SWEET_WORDS = ('奶洗', '巧克力', '蜂蜜', '焦糖', '利宾纳', '黑糖', '炼奶', '奶盖')

# 用户口语 → 库里实际用词
FLAVOR_SYNONYMS = {
    '咸鲜': ['咸鲜', '鲜味', 'umami', '咸甜', '叉烧', '香菇', '腐乳', '生蚝', '菌子', '酱油', '芝麻酱'],
    '茶香': ['茶香', '茶', '茶糖', '伯爵', '单丛', '抹茶', '玄米', '普洱', '乌龙', '焙茶'],
    '在地': ['在地', '本地', '岭南', '湖南', '江南', '粤式', '胡同', '中式', '城市记忆', '怀旧'],
    '花香': ['花香', '紫罗兰', '玫瑰', '可食用花', '桂花', '茉莉'],
    '烟熏': ['烟熏', '油洗', '梅斯卡尔', '正山小种', '泥煤'],
    '清爽': ['清爽', '气泡', '长饮', '轻盈', '极简'],
}
INDEPENDENT_TIERS = {'独立小店', '社区店', '主题概念店'}


def hit(text, q):
    return q in (text or '')


def is_sweet(s):
    if s['id'] in SWEET_IDS:
        return True
    blob = s['name'] + s['public_description'] + ' '.join(s['flavor'])
    return sum(w in blob for w in SWEET_WORDS) >= 2


def haystack(s):
    b = BARS.get(s['bar'], {})
    parts = [s['name'], s.get('name_en', ''), s['bar'], s['city'],
             ' '.join(s['flavor']), s['public_description'], s['anchor_note'],
             s.get('classic_anchor') or '', s['why'],
             b.get('menu_idea', ''), b.get('why_interesting', ''),
             b.get('menu_concept', ''), ' '.join(b.get('ideas', [])),
             ' '.join(b.get('signature_ingredients', [])),
             s['replica']['method'], s['replica']['note'],
             ' '.join(i['name'] for i in s['replica']['ingredients']),
             ' '.join(t['lever'] + t['change'] + t['effect'] for t in s['twists'])]
    return ' '.join(parts)


def flavor_score(s, q):
    """按命中位置打分：风味标签 > 酒名/公开描述 > 配方与说明 > 店级标签 > 微调方向"""
    terms = FLAVOR_SYNONYMS.get(q, [q])
    b = BARS.get(s['bar'], {})
    zones = [
        (5, ' '.join(s['flavor']) + ' ' + s['name']),
        (3, s['public_description'] + ' ' + s['why']),
        (2, s['anchor_note'] + ' ' + (s.get('classic_anchor') or '') + ' '
         + ' '.join(i['name'] for i in s['replica']['ingredients'])
         + ' ' + s['replica']['method'] + ' ' + s['replica']['note']),
        (1, b.get('menu_idea', '') + ' ' + b.get('menu_concept', '') + ' '
         + ' '.join(b.get('ideas', [])) + ' ' + ' '.join(b.get('signature_ingredients', []))),
        (1, ' '.join(t['lever'] + t['change'] + t['effect'] for t in s['twists'])),
    ]
    best = 0
    for weight, text in zones:
        if any(t in text for t in terms):
            best = max(best, weight)
    return best


def brief(s, prefix='  ', warn_sweet=False):
    anchor = s.get('classic_anchor') or '无同名经典（原创结构）'
    conf = {'high': '高', 'medium': '中', 'low': '低'}[s.get('confidence', 'medium')]
    price = f" ¥{s['price']}" if s.get('price') else ''
    b = BARS.get(s['bar'], {})
    print(f"{prefix}🥃 {s['name']}{price}  ·  {s['bar']}（{s['city']}）")
    print(f"{prefix}   {' / '.join(s['flavor'])}  |  经典锚点：{anchor}  |  置信度：{conf}")
    print(fresh_line(s, f"{prefix}   "))
    if b.get('menu_idea'):
        print(f"{prefix}   酒单想法：{b['menu_idea'][:52]}")
    if warn_sweet and is_sweet(s):
        print(f"{prefix}   ⚠️ 偏甜：已降权，用于失落 / 疲惫场景必须先走减糖版 twists")


def bar_brief(b, prefix='  '):
    tag = '📖' if b.get('concept_only') else '🥃'
    fr = eff_bar_freshness(b)
    ms = b.get('menu_status', 'unknown')
    extra = ' · 持续换季' if ms in ('rotating', 'no_menu') else ''
    print(f"{prefix}{tag} {b['name']} · {b['city']} · {b['tier']}{extra}")
    print(f"{prefix}   想法：{b['menu_idea']}")
    print(f"{prefix}   {FRESH_MARK.get(fr, '⚪')} 资料 {b.get('source_date', '未标注')} · "
          f"{age_text(b.get('source_date'))} · {FRESH_LABEL.get(fr, fr)} · "
          f"招牌档案 {b.get('signature_count', 0)} 杯")
    print(f"{prefix}   思路：{' / '.join(b['ideas'])}")


def print_snapshots(b, prefix='  '):
    snaps = b.get('menu_snapshots', [])
    if not snaps:
        return
    print(f"\n{prefix}【多期酒单快照对照】{len(snaps)} 期 —— 酒单换季最直观的证据")
    for i, sn in enumerate(snaps, 1):
        _f = classify(sn.get('as_of'))
        print(f"{prefix}  {i}. {sn.get('as_of')} · {sn.get('label')} · {age_text(sn.get('as_of'))} "
              f"[{FRESH_MARK.get(_f, '⚪')} {FRESH_LABEL.get(_f, '')}]")
        print(f"{prefix}     主题：{sn.get('theme')}")
        for dr in sn.get('drinks', []):
            print(f"{prefix}       · {dr}")
        if sn.get('note'):
            print(f"{prefix}     说明：{sn['note']}")
        print(f"{prefix}     出处：{', '.join(sn.get('source_ids', []))}")


def bar_detail(b):
    print('\n' + '=' * 64)
    print(f"  {b['name']}  ·  {b['city']}  ·  {b['tier']}")
    print('=' * 64)
    print(f"  【这张酒单怎么想的】{b['menu_idea']}")
    print(f"  【为什么有意思】{b['why_interesting']}")
    print(f"  【酒单结构】{b['menu_concept']}")
    print(f"  【思路标签】{' / '.join(b['ideas'])}")
    if b.get('signature_ingredients'):
        print(f"  【常用材料】{' / '.join(b['signature_ingredients'])}")
    if b.get('accolade'):
        print(f"  【榜单背景（仅参考，不是收录理由）】{b['accolade']}")
    fr = eff_bar_freshness(b)
    print(f"\n  【酒单状态】{MENU_STATUS_LABEL.get(b.get('menu_status'), '未确认是否换季')}")
    print(f"  【资料时效】{FRESH_MARK.get(fr, '⚪')} {FRESH_LABEL.get(fr, fr)} "
          f"· 资料日期 {b.get('source_date', '未标注')} · {age_text(b.get('source_date'))} "
          f"· 口径 {AS_OF}")
    if b.get('current_menu_advice'):
        print(f"\n  【⚠️ 到店前必读】{b['current_menu_advice']}")
    if b.get('taste_note'):
        print(f"\n  【公开口味争议】{b['taste_note']}")
    print_snapshots(b)

    mine = [s for s in SIGS if s['bar'] == b['name']]
    cur = [s for s in mine if eff_freshness(s) != 'historical']
    old = [s for s in mine if eff_freshness(s) == 'historical']
    print(f"\n  【非历史快照中的可复刻款（可能偏旧或日期未知，须核对当日酒单）】{len(cur)} 杯")
    for s in cur:
        print(f"    · {s['name']}  {FRESH_MARK.get(eff_freshness(s), '⚪')} "
              f"快照 {s.get('menu_snapshot', '?')} · {age_text(s.get('menu_snapshot'))}"
              f"（锚点：{s.get('classic_anchor') or '无'}）")
    if old:
        print(f"\n  【历史快照 · 已换季，仅作思路参考】{len(old)} 杯（默认不进推荐）")
        for s in old:
            print(f"    · {s['name']}  ⚪ 快照 {s.get('menu_snapshot', '?')} "
                  f"· {age_text(s.get('menu_snapshot'))}")
        print(f"     查这些老款：--archive / --snapshots {b['name']} / <酒名>")
    if b.get('concept_only'):
        print(f"\n  ⚠️ 这家店只有酒单概念、没有公开配方材料，本库不编造比例。")
        print(f"     可照搬的是上面的「酒单结构」，用 --concepts 看全套骨架。")
    srcs = [SOURCES[x]['publisher'] for x in b.get('source_ids', []) if x in SOURCES]
    print(f"\n  【出处】{'、'.join(srcs)}（{', '.join(b.get('source_ids', []))}）"
          f" · 资料日期 {b.get('source_date') or '见来源'}")
    print(f"  【诚实边界】好不好喝是主观判断，本库不评分不排名；酒单会换季/闭店/换址，")
    print(f"              任何快照都不能替代店家当日酒单。")


def detail(s):
    b = BARS.get(s['bar'], {})
    print('\n' + '=' * 64)
    print(f"  {s['name']}  {s.get('name_en') or ''}")
    print('=' * 64)
    if s.get('price'):
        print(f"  公开参考价：¥{s['price']}（报道口径，随年份变动）")
    print(f"  出自：{s['bar']} / {s['city']} / {b.get('tier', '')}")
    fr = eff_freshness(s)
    print(f"  【酒单快照】{s.get('menu_snapshot', '未标注')} · {age_text(s.get('menu_snapshot'))} "
          f"· {FRESH_LABEL.get(fr, fr)} · 状态 {eff_status(s)} · 口径 {AS_OF}")
    print(f"  【店家酒单状态】{MENU_STATUS_LABEL.get(b.get('menu_status'), '未确认是否换季')}")
    if fr != 'recent' or b.get('menu_status') in ('rotating', 'no_menu'):
        print(f"  ⚠️ 这一杯只是某一期酒单的快照，不代表现在还在售；请核对店家当日酒单。")
    if b.get('current_menu_advice'):
        print(f"  ⚠️ {b['current_menu_advice']}")
    if b.get('menu_idea'):
        print(f"  这张酒单的想法：{b['menu_idea']}")
    if b.get('accolade'):
        print(f"  榜单背景（仅参考）：{b['accolade']}")
    print(f"  风味：{' / '.join(s['flavor'])}   置信度：{s.get('confidence', 'medium')}")
    print(f"\n  【公开描述】{s['public_description']}")
    print(f"\n  【经典锚点】{s.get('classic_anchor') or '无（原创结构）'}")
    print(f"  {s['anchor_note']}")

    rp = s['replica']
    print(f"\n  【风味复刻 · 参考比例】（{rp['type']}）")
    for i in rp['ingredients']:
        if i['amount'] is None:
            amt = '补满' if i['unit'] == 'topping' else (i['unit'] or '未公开')
        else:
            amt = f"{i['amount']}{i['unit']}"
        print(f"    · {i['name']}  {amt}")
    print(f"    技法 {rp['method']}  |  杯型 {rp['glass']}  |  装饰 {rp['garnish']}")
    print(f"    备注：{rp['note']}")

    print(f"\n  【往哪微调能更好】")
    for i, t in enumerate(s['twists'], 1):
        print(f"    {i}. {t['lever']}：{t['change']}")
        print(f"       → {t['effect']}")

    print(f"\n  【为什么值得复刻】{s['why']}")
    if b.get('taste_note'):
        print(f"\n  【这家店的公开口味争议】{b['taste_note']}")
    print(f"\n  【材料不设限】找不到的在地食材，用 4.3 替换或第十四章旋钮绕过去；")
    print(f"  技术类（油洗 / 奶洗 / 澄清 / 发酵 / 浸渍）注意上面标注的预处理时间。")
    print(f"  【出处】{'、'.join(SOURCES[x]['publisher'] for x in s['source_ids'] if x in SOURCES)}"
          f"（{', '.join(s['source_ids'])}） · 快照来源 {s.get('snapshot_source', '—')}")
    print(f"  ⚠️ 非店家官方原方（verified={str(s['verified']).lower()}），商用请先确认或自行研发。")
    stale_warning(fr)
    if is_sweet(s):
        print(f"  ⚠️ 本杯偏甜：用于失落 / 疲惫场景时先走 twists 里的减糖版。")


def filter_sig(city=None, bar=None, anchor=None, flavor=None, mood=None, q=None,
               idea=None, tier=None, independent=False, freshness=None, archive=False):
    if archive:
        out = [s for s in SIGS if eff_freshness(s) == 'historical']
    elif freshness:
        out = [s for s in SIGS if eff_freshness(s) == freshness]
    else:
        out = active_sigs()  # 默认不推历史酒款（按 AS_OF 实时计算）
    if city:
        out = [s for s in out if city in s['city'] or city in s['bar']]
    if bar:
        out = [s for s in out if bar in s['bar']]
    if anchor:
        out = [s for s in out if s.get('classic_anchor') and (anchor in s['classic_anchor'] or anchor in s['anchor_note'])]
    if flavor:
        out = sorted([s for s in out if flavor_score(s, flavor) > 0],
                     key=lambda s: -flavor_score(s, flavor))
    if q:
        out = [s for s in out if q in s['name'] or q.lower() in (s.get('name_en') or '').lower()
               or q in s['id'] or q in s['bar'] or q in s['public_description']]
    if idea:
        out = [s for s in out if any(idea in t for t in BARS.get(s['bar'], {}).get('ideas', []))
               or idea in haystack(s)]
    if tier:
        out = [s for s in out if BARS.get(s['bar'], {}).get('tier') == tier]
    if independent:
        out = [s for s in out if BARS.get(s['bar'], {}).get('tier') in INDEPENDENT_TIERS]
    if mood:
        cfg = MOOD.get(mood)
        if cfg:
            def score(s):
                base = sum(2 for w in cfg['want'] if any(w in f for f in s['flavor']))
                base += sum(1 for w in cfg['want'] if hit(s['why'], w))
                base -= sum(3 for w in cfg['avoid_words']
                            if hit(s['public_description'], w) or hit(s['why'], w))
                if is_sweet(s):
                    base -= 4
                base += {'high': 1, 'medium': 0, 'low': -1}[s.get('confidence', 'medium')]
                # 独立小店优先；近期快照优先；名气不是加分项
                if BARS.get(s['bar'], {}).get('tier') in INDEPENDENT_TIERS:
                    base += 1
                if eff_freshness(s) == 'recent':
                    base += 1
                return base
            out = sorted(out, key=lambda s: -score(s))
            print(f"\n🎭 情绪「{mood}」· {cfg['note']}")
            print(f"   共 {len(out)} 杯，按贴合度排序；偏甜款已降权，独立小店与近期快照略优先（不按名次）")
            print(f"   💡 进 1.1 第 ② 路线时取前 1~3 条即可，别把整张酒单塞给客人\n")
    return out


def filter_bars(city=None, idea=None, tier=None, independent=False,
                concept_only=False, q=None, rotating=False):
    out = D['bars']
    if city:
        out = [b for b in out if city in b['city'] or city in b['name']]
    if idea:
        out = [b for b in out if any(idea in t for t in b['ideas'])
               or idea in b['menu_idea'] or idea in b['why_interesting']
               or idea in b['menu_concept']]
    if tier:
        out = [b for b in out if b['tier'] == tier]
    if independent:
        out = [b for b in out if b['tier'] in INDEPENDENT_TIERS]
    if concept_only:
        out = [b for b in out if b.get('concept_only')]
    if rotating:
        out = [b for b in out if b.get('menu_status') in ('rotating', 'no_menu', 'seasonal')]
    if q:
        out = [b for b in out if q in b['name'] or q in b['menu_idea']
               or q in b['why_interesting'] or q in b['menu_concept']]
    return out


def show_map():
    groups = collections.defaultdict(list)
    for b in D['bars']:
        groups[b['city']].append(b)
    print(f"\n🗺  公开可查的吧台地图 · {len(groups)} 个城市 / {len(D['bars'])} 家店")
    print(f"   收录看「酒单有没有想法」，不按名次排序 · 资料截至 {D['coverage']['as_of']} "
          f"· 时效按 {AS_OF} 实时计算\n")
    for city in sorted(groups, key=lambda c: -len(groups[c])):
        bs = groups[city]
        print(f"  【{city}】{len(bs)} 家")
        for b in bs:
            mark = '📖' if b.get('concept_only') else '🥃'
            stale = ' ⏳' if eff_bar_freshness(b) in ('aging', 'historical') else ''
            rot = ' 🔄' if b.get('menu_status') in ('rotating', 'no_menu') else ''
            print(f"    {mark} {b['name']}（{b['tier']}）{stale}{rot} — {b['menu_idea'][:40]}")
        print()
    print('  🥃 有可复刻招牌   📖 只有酒单概念   ⏳ 资料偏旧/历史   🔄 持续换季或无酒单')
    print('  ⚠️ 带 ⏳ / 🔄 的店，酒款大概率已换；--snapshots 看多期对照，--stale 看全部过期款')
    print('  💡 --bars 看逐店完整档案；--idea 在地食材 按思路找；--concepts 看可照搬骨架')


def show_stats():
    st = D['stats']
    cov = D['coverage']
    fp = D.get('freshness_policy', {})
    print(f"\n📊 覆盖统计 · {D['name']} v{D['version']}\n")
    for k, label in [('bars', '店家'), ('cities', '城市'), ('signatures', '可复刻招牌'),
                     ('menu_concepts', '酒单骨架'), ('twist_levers', '微调手法'),
                     ('sources', '公开来源'), ('independent', '独立/社区/主题概念店')]:
        print(f"  {label:<24} {st[k]}")
    print(f"\n  【酒单时效 · 按 {AS_OF} 实时计算（v2.6.2）】")
    efb = collections.Counter(eff_bar_freshness(b) for b in D['bars'])
    efs = collections.Counter(eff_freshness(s) for s in SIGS)
    print(f"    店家  🟢 近期 {efb['recent']} / 🟡 偏旧 {efb['aging']} "
          f"/ ⚪ 历史 {efb['historical']} / 不详 {efb['unknown']}")
    print(f"    招牌  🟢 {efs['recent']} / 🟡 {efs['aging']} / ⚪ {efs['historical']} "
          f"（历史 {efs['historical']} 杯默认不进推荐）")
    drift_b = sum(1 for b in D['bars'] if b.get('freshness') != eff_bar_freshness(b))
    drift_s = sum(1 for s in SIGS if s.get('freshness') != eff_freshness(s))
    print(f"    建档基线（2026-11-17 静态标签）：店家 🟢 {st.get('recent_bars', 0)} "
          f"/ 🟡 {st.get('aging_bars', 0)} / ⚪ {st.get('historical_bars', 0)}")
    print(f"    ⏳ 随时间已漂移：{drift_b} 家店 / {drift_s} 杯招牌 → 一律以实时计算为准")
    print(f"    持续换季 / 无酒单吧台 {st.get('rotating_menus', 0)} 家 · 多期快照 {st.get('menu_snapshots', 0)} 期")
    if fp.get('principle'):
        print(f"\n  【时效原则】{fp['principle']}")
    if fp.get('stale_rule'):
        print(f"  【过期规则】{fp['stale_rule']}")
    fc = fp.get('freshness_computation', {})
    if fc:
        print(f"  【怎么算的】{fc.get('rule', '')}")
        print(f"  【复现】--as-of YYYY-MM-DD 可指定计算日期；--as-of {D['coverage']['as_of']} 回到建档当天")
    print(f"\n  【收录标准】{D['selection_policy']['criteria']}")
    print(f"  【不按什么排】{D['selection_policy']['not_ranked_by']}")
    print(f"  【口味立场】{D['selection_policy']['taste_is_subjective']}")
    print(f"\n  ⚠️ {cov['honest_note']}")
    print(f"  【已知缺口】{'；'.join(cov['known_gaps'][:2])}")
    print(f"  【怎么补全】{cov['how_to_extend']}")
    if fp.get('photo_sources', {}).get('known_platform_limits'):
        print(f"\n  【平台限制·如实说明】{fp['photo_sources']['known_platform_limits']}")


def show_snapshots(name=None):
    if name:
        bs = filter_bars(q=name)
        if not bs:
            print(f'❌ 没找到店「{name}」。用 --map 看全部城市。')
            sys.exit(1)
        b = next((x for x in bs if x['name'] == name), bs[0])
        print(f"\n📅 {b['name']} · 酒单快照对照")
        print(f"   {MENU_STATUS_LABEL.get(b.get('menu_status'), '未确认是否换季')}")
        if not b.get('menu_snapshots'):
            print(f"   本库只记录到一期资料（{b.get('source_date', '未标注')}），没有多期对照。")
        print_snapshots(b)
        if b.get('current_menu_advice'):
            print(f"\n  ⚠️ {b['current_menu_advice']}")
        return
    rows = [(b, sn) for b in D['bars'] for sn in b.get('menu_snapshots', [])]
    print(f"\n📅 全库多期酒单快照 · {len(rows)} 期 / {len({b['name'] for b, _ in rows})} 家店\n")
    for b, sn in rows:
        print(f"  【{b['name']} · {b['city']}】{sn.get('as_of')} · {sn.get('label')}")
        print(f"     {sn.get('theme')}")
        print(f"     酒款：{'、'.join(sn.get('drinks', [])[:4])}"
              f"{' …' if len(sn.get('drinks', [])) > 4 else ''}")
        _f = classify(sn.get('as_of'))
        print(f"     {FRESH_MARK.get(_f, '⚪')} {FRESH_LABEL.get(_f, '')} · {age_text(sn.get('as_of'))}\n")
    print('  💡 --snapshots <店名> 看单店完整对照；--archive 只看历史酒款')


def show_stale():
    rows = [s for s in SIGS if eff_freshness(s) in ('aging', 'historical', 'unknown')]
    groups = collections.defaultdict(list)
    for s in rows:
        groups[s['bar']].append(s)
    print(f"\n⏳ 已过期 / 存疑的酒单快照 · {len(rows)} 杯 / {len(groups)} 家店 · 口径 {AS_OF}")
    print(f"   这些酒款默认不进推荐，只作历史样本与酒单思路参考\n")
    for bar in sorted(groups, key=lambda x: -len(groups[x])):
        ss = groups[bar]
        b = BARS.get(bar, {})
        print(f"  【{bar} · {ss[0]['city']}】{len(ss)} 杯 · {b.get('menu_status', 'unknown')}")
        for s in ss:
            _f = eff_freshness(s)
            print(f"    {FRESH_MARK.get(_f, '⚪')} {s['name']}  "
                  f"快照 {s.get('menu_snapshot', '?')} · {age_text(s.get('menu_snapshot'))}  "
                  f"{FRESH_LABEL.get(_f, '')}")
        print()
    print('  💡 想补全：按 freshness_policy.update_hint 往 menu_snapshots 追加新一期并登记出处')


def main():
    p = argparse.ArgumentParser(description='有意思的酒单 · 公开可查的吧台地图查询器（含酒单时效）')
    p.add_argument('drink', nargs='?', help='酒名 / 店名 / 关键词')
    p.add_argument('--map', action='store_true', help='城市地图')
    p.add_argument('--stats', action='store_true', help='覆盖统计、实时时效分布与诚实边界')
    p.add_argument('--as-of', help='按指定日期计算时效（YYYY-MM-DD），便于复现与回归测试')
    p.add_argument('--list', action='store_true', help='列出当前/近期快照中的可复刻招牌')
    p.add_argument('--bars', action='store_true', help='逐店完整档案')
    p.add_argument('--city', help='按城市')
    p.add_argument('--bar', help='按店名（输出店档案 + 多期快照 + 该店招牌）')
    p.add_argument('--idea', help='按酒单思路，如 在地食材 / 无酒单即兴 / 怀旧零食')
    p.add_argument('--tier', help='按店型：独立小店 / 社区店 / 主题概念店 / 酒店酒吧 / 榜单名店')
    p.add_argument('--independent', action='store_true', help='只看独立/社区/主题概念店')
    p.add_argument('--concept-only', action='store_true', help='只看只有酒单概念的店')
    p.add_argument('--rotating', action='store_true', help='只看持续换季 / 无酒单吧台')
    p.add_argument('--taste', action='store_true', help='查看公开口味争议')
    p.add_argument('--snapshots', nargs='?', const='__all__', help='多期酒单快照对照（可接店名）')
    p.add_argument('--freshness', choices=['recent', 'aging', 'historical', 'unknown'],
                    help='按酒单快照时效筛选')
    p.add_argument('--archive', action='store_true', help='只看历史酒单快照')
    p.add_argument('--stale', action='store_true', help='列出所有已过期/存疑的酒款')
    p.add_argument('--anchor', help='按经典锚点')
    p.add_argument('--flavor', help='按风味')
    p.add_argument('--mood', help='按情绪')
    p.add_argument('--concepts', action='store_true', help='可照搬的整套酒单骨架')
    p.add_argument('--levers', action='store_true', help='微调手法')
    p.add_argument('--json', action='store_true', help='输出原始 JSON')
    a = p.parse_args()

    global AS_OF
    if a.as_of:
        try:
            AS_OF = _dt.date.fromisoformat(a.as_of)
        except ValueError:
            p.error('--as-of 需为 YYYY-MM-DD，例如 2027-11-17')

    if a.map:
        show_map()
        return
    if a.stats:
        show_stats()
        return
    if a.stale:
        show_stale()
        return
    if a.snapshots is not None:
        # 店名常带空格（MIXY BAR）：把 --snapshots 的值与后续位置参数拼起来
        target = None if a.snapshots == '__all__' else \
            ' '.join(x for x in (a.snapshots, a.drink) if x)
        show_snapshots(target)
        return
    if a.taste:
        print(f"\n⚖️  {D['taste_disclaimer']}\n")
        for b in D['bars']:
            if b.get('taste_note'):
                print(f"  【{b['name']} · {b['city']}】{b['taste_note']}\n")
        return

    if a.concepts:
        print(f"\n📋 可照搬的整套酒单骨架 · {len(D['menu_concepts'])} 套\n")
        for c in D['menu_concepts']:
            print(f"  【{c['bar']}】{c['name']}")
            print(f"    怎么做：{c['how']}")
            print(f"    为什么：{c['why']}\n")
        return

    if a.levers:
        print(f"\n🎛 {len(D['twist_levers'])} 种微调与酒单手法\n")
        for i, t in enumerate(D['twist_levers'], 1):
            print(f"  {i}. {t['name']}：{t['how']}")
            print(f"     → {t['effect']}\n")
        return

    # --bar：完整店档案（不是只筛招牌）
    if a.bar:
        bs = filter_bars(q=a.bar)
        if not bs:
            print(f'❌ 没找到店「{a.bar}」。用 --map 看全部城市。')
            sys.exit(1)
        if len(bs) > 1 and not any(b['name'] == a.bar for b in bs):
            print(f'\n找到 {len(bs)} 家，请说得更具体：')
            for b in bs:
                bar_brief(b)
            return
        b = next((x for x in bs if x['name'] == a.bar), bs[0])
        if a.json:
            print(json.dumps(b, ensure_ascii=False, indent=2))
        else:
            bar_detail(b)
        return

    # --bars / --idea / --tier / --concept-only / --rotating 且无招牌筛选条件时 → 输出店清单
    shop_mode = (a.bars or bool(a.idea) or bool(a.tier) or a.independent
                 or a.concept_only or a.rotating)
    sig_mode = any([a.list, a.city and not a.bars, a.anchor, a.flavor, a.mood,
                    a.freshness, a.archive])
    if shop_mode and not sig_mode:
        bs = filter_bars(a.city, a.idea, a.tier, a.independent, a.concept_only,
                         a.drink, a.rotating)
        if a.json:
            print(json.dumps(bs, ensure_ascii=False, indent=2))
            return
        title = ' · '.join(f'{k}={v}' for k, v in
                           [('城市', a.city), ('思路', a.idea), ('店型', a.tier),
                            ('仅独立小店', '是' if a.independent else ''),
                            ('仅概念', '是' if a.concept_only else ''),
                            ('换季吧台', '是' if a.rotating else ''), ('关键词', a.drink)] if v)
        print(f"\n🏮 有意思的酒单 · {title or '全部店家'}  →  {len(bs)} 家\n")
        if not bs:
            print('  （无匹配；--map 看全部城市，--bars 不加参数看全部店）')
            return
        for b in bs:
            bar_brief(b)
            print(f"      为什么有意思：{b['why_interesting'][:70]}")
            print()
        print('  💡 查单店：--bar <店名>；看快照对照：--snapshots；看骨架：--concepts')
        print('  ⚠️ 收录看酒单想法，不按名次；本库不评价好不好喝，也不承诺酒款仍在售。')
        return

    # 单词精确查询 → 招牌优先，找不到再当店名
    if a.drink and not any([a.list, a.city, a.anchor, a.flavor, a.mood, a.idea, a.tier,
                            a.freshness, a.archive]):
        s = BY_NAME.get(a.drink) or BY_ID.get(a.drink)
        if not s:
            cand = [x for x in SIGS if a.drink in x['name'] or a.drink in x['bar']
                    or a.drink in x['public_description']]
            if len(cand) == 1:
                s = cand[0]
            elif cand:
                print(f'\n找到 {len(cand)} 杯，请说得更具体：')
                for x in cand:
                    brief(x)
                return
            else:
                bs = filter_bars(q=a.drink)
                if bs:
                    bar_detail(bs[0])
                    return
                print(f'❌ 没找到「{a.drink}」。用 --map / --list 看全部，或用 --idea 按思路找。')
                sys.exit(1)
        if a.json:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            detail(s)
        return

    out = filter_sig(a.city, None, a.anchor, a.flavor, a.mood, a.drink,
                     a.idea, a.tier, a.independent, a.freshness, a.archive)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    title = ' · '.join(f'{k}={v}' for k, v in
                       [('城市', a.city), ('锚点', a.anchor), ('风味', a.flavor),
                        ('情绪', a.mood), ('思路', a.idea), ('店型', a.tier),
                        ('时效', a.freshness), ('仅历史', '是' if a.archive else ''),
                        ('关键词', a.drink)] if v)
    print(f"\n🏮 可复刻招牌 · {title or '当前/近期快照'}  →  {len(out)} 杯"
          f"  【时效按 {AS_OF} 实时计算】\n")
    if not a.archive:
        print(f"  （默认已排除 {len(SIGS) - len(active_sigs())} 杯历史酒款；--archive 查看）\n")
    if not out:
        print('  （无匹配；--anchor 用经典名找同源改编，--idea 按酒单思路找店）')
        return
    low_sweet = a.mood in ('失落', '疲惫', '治愈')
    for s in out:
        brief(s, warn_sweet=low_sweet)
        print(f"      {s['why'][:72]}")
        print()
    print('  💡 查单杯完整档案：<酒名>；查店档案：--bar <店名>；看换季对照：--snapshots')
    print('  ⚠️ 所有比例为风味复刻参考，非店家官方原方；收录不按名次，酒款不承诺仍在售。')


if __name__ == '__main__':
    main()
