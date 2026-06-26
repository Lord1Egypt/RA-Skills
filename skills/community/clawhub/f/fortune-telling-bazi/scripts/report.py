#!/usr/bin/env python3
"""
八字展示报告模块

与 scripts/calc.py 的 Fate dataclass 解耦：
  - 接收 Fate 对象或 dict（兼容旧数据）
  - 输出格式化字符串

命名映射（scripts/calc.py → scripts/report.py）：
  stem/stem_el    = 天干/天干五行
  branch/branch_el = 地支/地支五行
  ten_god         = 十神
  na_yin          = 纳音
  hidden_stems    = 藏干
  void            = 旬空
  vitality        = 旺衰
  favorable       = 喜用
  afflictions     = 神煞
"""
from typing import List
from calc import Fate


def _safe_get(obj, key, default=''):
    """兼容 Fate dataclass 和 dict"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _get_pillar_detail(fate, pillar_key, is_fate=True):
    """
    取某柱的完整数据
    is_fate=True  → Fate dataclass
    is_fate=False → dict（旧格式）
    """
    if is_fate:
        pillar = getattr(fate, f"{pillar_key}_pillar", None)
        if pillar is None:
            return {}
        return {
            'stem':        pillar.stem,
            'branch':      pillar.branch,
            'stem_el':     pillar.stem_el,
            'branch_el':   pillar.branch_el,
            'yinyang':     pillar.yinyang,
            'ten_god':     pillar.ten_god,
            'na_yin':      pillar.na_yin,
            'hidden':      pillar.hidden,
            'vacant':      pillar.vacant,
        }
    # dict 旧格式
    detail = fate.get('detail', {})
    return detail.get(pillar_key, {})


def view_single(name, user_data):
    """
    输出单人完整八字报告
    user_data: dict with 'birth' + 'bazi' keys
    bazi 可能是 dict（旧格式）或 Fate dataclass（新格式）
    """
    birth   = user_data["birth"]
    bazi    = user_data.get("bazi", {})
    is_fate = isinstance(bazi, Fate)

    gender_d = "男" if str(birth.get("gender", birth.get("gender_d", 1))) in ('1', '男') else "女"

    hour_str = (
        f"{birth['hour']}:{int(birth.get('minute', 0)):02d}"
        if birth.get('minute') is not None
        else f"{birth['hour']}点"
    )

    # ── 从 bazi 取字段（统一接口） ────────────────────────────────────────────
    if is_fate:
        f         = bazi
        bazi_str  = f.bazi_str
        lunar_str = f.lunar_str
        shengxiao = f.shengxiao
        mingge    = f.mingge
        vitality  = f.vitality
        favorable = f.favorable
        void      = f.void
        vacant    = f.void
        afflictions = f.afflictions
        taiyuan   = f.taiyuan
        taixi     = f.taixi
        life_palace = f.minggong    # 命宫
        destiny_palace = f.shengong  # 身宫
        dayun     = f.dayun
        day_stem  = f.day_stem
        elem_counts = f.wuxing_count

        # 四柱干支
        bazi_ganzhi = {
            "year":  f.year_pillar.stem  + f.year_pillar.branch,
            "month": f.month_pillar.stem + f.month_pillar.branch,
            "day":   f.day_pillar.stem   + f.day_pillar.branch,
            "hour":  f.hour_pillar.stem  + f.hour_pillar.branch,
        }

        # 五行字符串
        wx_str = ' '.join([
            f.year_pillar.stem_el  + f.year_pillar.branch_el,
            f.month_pillar.stem_el + f.month_pillar.branch_el,
            f.day_pillar.stem_el   + f.day_pillar.branch_el,
            f.hour_pillar.stem_el  + f.hour_pillar.branch_el,
        ])

        # 纳音
        nayin_y = f.year_pillar.na_yin
        nayin_m = f.month_pillar.na_yin
        nayin_d = f.day_pillar.na_yin
        nayin_h = f.hour_pillar.na_yin
        yinyang = f.day_pillar.yinyang

    else:
        # 旧 dict 格式（兼容）
        bazi_ganzhi_raw = bazi.get("bazi", {})
        if isinstance(bazi_ganzhi_raw, dict):
            bazi_str = " ".join(bazi_ganzhi_raw.values())
            bazi_ganzhi = bazi_ganzhi_raw
        else:
            bazi_str = str(bazi_ganzhi_raw)
            bazi_ganzhi = {}

        lunar_str     = bazi.get('lunar_str', '')
        shengxiao     = bazi.get('shengxiao', '')
        mingge        = bazi.get('mingge', '')
        vitality      = bazi.get('wangshuai', '')
        favorable     = bazi.get('xiyong', '')
        vacant        = bazi.get('kongwang', '')
        afflictions   = bazi.get('shensha', [])
        taiyuan       = bazi.get('taiyuan', '')
        taixi         = bazi.get('taixi', '')
        life_palace   = bazi.get('minggong', '')
        destiny_palace= bazi.get('shengong', '')
        dayun         = bazi.get('dayun', [])
        day_stem      = bazi.get('me', '')
        elem_counts   = bazi.get('wuxing_count', {})

        wx_str        = bazi.get('wuxing', '')
        nayin_y       = bazi.get('nayin', {}).get('year', '')
        nayin_m       = bazi.get('nayin', {}).get('month', '')
        nayin_d       = bazi.get('nayin', {}).get('day', '')
        nayin_h       = bazi.get('nayin', {}).get('hour', '')
        yinyang       = bazi.get('yinyang', '')

    # ── 逐柱输出 ──────────────────────────────────────────────────────────────
    lines = [
        f"━━━ {name} 八字详情 ━━━",
        f"性别：{gender_d}",
        f"公历：{birth['year']}年{birth['month']}月{birth['day']}日{hour_str}",
        f"农历：{lunar_str}",
        f"生肖：{shengxiao}",
        f"━━━ 四柱 ━━━",
    ]

    for p_key, label in [('year','年柱'),('month','月柱'),('day','日柱'),('hour','时柱')]:
        d = _get_pillar_detail(bazi, p_key, is_fate)

        stem_v     = d.get('stem', '')
        branch_v    = d.get('branch', '')
        stem_el_v   = d.get('stem_el', '')
        branch_el_v = d.get('branch_el', '')
        yinyang_v   = d.get('yinyang', '')
        ten_god_v   = d.get('ten_god', '日主' if p_key == 'day' else '')
        na_yin_v    = d.get('na_yin', '')
        hidden_v    = d.get('hidden', [])
        vacant_v    = d.get('vacant', '')
        ganzhi_v    = bazi_ganzhi.get(p_key, '') if isinstance(bazi_ganzhi, dict) else ''

        lines.append(f"{label}：{ganzhi_v}（{na_yin_v}）")
        lines.append(f"  天干：{stem_v} {yinyang_v} {stem_el_v} 【{ten_god_v}】")
        lines.append(f"  地支：{branch_v} {yinyang_v} 藏干：{','.join(hidden_v)} 旬空：{vacant_v}")

    lines += [
        f"━━━ 命理 ━━━",
        f"日主：{day_stem}（{yinyang}）",
        f"五行：{wx_str}",
        f"  统计：{elem_counts}",
        f"纳音：{nayin_y} / {nayin_m} / {nayin_d} / {nayin_h}",
        f"命格：{mingge}",
        f"旺衰：{vitality}",
        f"喜用：{favorable}",
        f"旬空：{vacant}",
        f"胎元：{taiyuan}",
        f"胎息：{taixi}",
        f"命宫：{life_palace}",
        f"身宫：{destiny_palace}",
        f"神煞：{', '.join(afflictions) if afflictions else '无'}",
        f"━━━ 大运 ━━━",
    ]

    if dayun:
        for i, d in enumerate(dayun[:8]):
            lines.append(
                f"  {i+1}. {d.get('ganzhi','')} "
                f"{d.get('start_age','')}-{d.get('end_age','')}岁"
                f"（{d.get('start_year','')}年）旬空：{d.get('vacant', d.get('void',''))}"
            )
    else:
        lines.append("  （大运数据不可用）")

    return '\n'.join(lines)


# ════════════════════════════════════════════════════════════════════════════════
# 联合分析
# ════════════════════════════════════════════════════════════════════════════════

def _get_branch(bazi, pillar_key, is_fate):
    """取某柱地支"""
    if is_fate:
        pillar = getattr(bazi, f"{pillar_key}_pillar", None)
        return pillar.branch if pillar else ''
    raw = bazi.get("bazi", {})
    if isinstance(raw, dict):
        v = raw.get(pillar_key, '')
        return v[-1:] if v else ''
    return ''


def _get_stems(bazi, is_fate):
    """取四柱天干列表"""
    if is_fate:
        return [
            bazi.year_pillar.stem, bazi.month_pillar.stem,
            bazi.day_pillar.stem,  bazi.hour_pillar.stem,
        ]
    raw = bazi.get("bazi", {})
    if isinstance(raw, dict):
        return [v[:-1] if v else '' for v in raw.values()]
    return []


def _branch_interaction(branches: List[str]) -> str:
    """
    判断地支间合冲刑害关系
    branches: 地支列表
    """
    from calc import BranchRelation

    rels, seen = [], set()
    for i in range(len(branches)):
        for j in range(i + 1, len(branches)):
            a, b = branches[i], branches[j]
            if not a or not b:
                continue
            key = (a, b)
            if key in BranchRelation.HEX:
                r = f"{a}{BranchRelation.HEX[key][-1]}{b}"
                if r not in seen:
                    seen.add(r); rels.append(f"{r}（吉）")
            elif key in BranchRelation.CLASH:
                r = f"{a}{BranchRelation.CLASH[key][-1]}{b}"
                if r not in seen:
                    seen.add(r); rels.append(f"{r}（冲）")
            elif key in BranchRelation.PUNISHMENT:
                r = BranchRelation.PUNISHMENT[key]
                if r not in seen:
                    seen.add(r); rels.append(f"{r}（刑）")
    return '无明显合冲刑害' if not rels else ' / '.join(rels)


def _wuxing_affinity(char_sets: List[str]) -> str:
    """
    五行相生相克分析
    char_sets: 每个八字的所有字符（干支混合）
    """
    from calc import Stem

    def char_to_element(c: str) -> str:
        if c in Stem.ELEMENT:
            return Stem.ELEMENT[c]
        from calc import Branch
        if c in Branch.ELEMENT:
            return Branch.ELEMENT[c]
        return ''

    sheng_pairs = {('木','火'), ('火','土'), ('土','金'), ('金','水'), ('水','木')}

    elem_sets = []
    for chars in char_sets:
        elems = set()
        for c in chars:
            e = char_to_element(c)
            if e:
                elems.add(e)
        elem_sets.append(elems)

    results = []
    for i in range(len(elem_sets)):
        for j in range(i + 1, len(elem_sets)):
            for e1 in elem_sets[i]:
                for e2 in elem_sets[j]:
                    if (e1, e2) in sheng_pairs:
                        results.append(f"{e1}→{e2}")
                    if (e2, e1) in sheng_pairs:
                        results.append(f"{e2}→{e1}")

    if not results:
        return "五行无明显相生关系，较为独立"
    seen = list(dict.fromkeys(results))
    return "五行相生：" + '、'.join(seen)


def _marriage_analysis(d1: dict, d2: dict) -> str:
    """婚配分析（两人）"""
    from calc import BranchRelation

    def zhi_rel(zhis):
        rels, seen = [], set()
        for i in range(len(zhis)):
            for j in range(i + 1, len(zhis)):
                a, b = zhis[i], zhis[j]
                if not a or not b:
                    continue
                key = (a, b)
                if key in BranchRelation.HEX:
                    r = f"{a}{BranchRelation.HEX[key][-1]}{b}"
                    if r not in seen: seen.add(r); rels.append(f"{r}（吉）")
                elif key in BranchRelation.CLASH:
                    r = f"{a}{BranchRelation.CLASH[key][-1]}{b}"
                    if r not in seen: seen.add(r); rels.append(f"{r}（冲）")
                elif key in BranchRelation.PUNISHMENT:
                    r = BranchRelation.PUNISHMENT[key]
                    if r not in seen: seen.add(r); rels.append(f"{r}（刑）")
        return '无明显合冲刑害' if not rels else ' / '.join(rels)

    def get_key(bazi, key, default=''):
        if isinstance(bazi, Fate):
            val = getattr(bazi, key, None)
            if val is not None and val != '':
                return val
            # xiyong fallback → favorable（兼容 xiyong 为空的 Fate 对象）
            if key == 'xiyong':
                return getattr(bazi, 'favorable', '')
            return default
        return bazi.get(key, default)

    def get_branch(bazi, pillar_key):
        return _get_branch(bazi, pillar_key, isinstance(bazi, Fate))

    bazi1, bazi2 = d1["bazi"], d2["bazi"]

    yz1 = get_branch(bazi1, 'year')
    yz2 = get_branch(bazi2, 'year')
    dz1 = get_branch(bazi1, 'day')
    dz2 = get_branch(bazi2, 'day')

    favorable1 = get_key(bazi1, 'xiyong', '')
    favorable2 = get_key(bazi2, 'xiyong', '')

    shensha1 = set(get_key(bazi1, 'shensha', []))
    shensha2 = set(get_key(bazi2, 'shensha', []))

    lines = [
        f"日支关系：{zhi_rel([dz1, dz2])}（{d1['name']}:{dz1} / {d2['name']}:{dz2}）",
        f"年支关系：{zhi_rel([yz1, yz2])}（{d1['name']}:{yz1} / {d2['name']}:{yz2}）",
        f"喜用互补：{favorable1[:30]} | {favorable2[:30]}",
    ]

    if "桃花" in shensha1 and "桃花" in shensha2:
        lines.append("⚠️ 双方均带桃花，感情需注意经营")
    if "天乙贵人" in shensha1 and "天乙贵人" in shensha2:
        lines.append("✅ 双方均有天乙贵人，互助有缘")

    return '\n'.join(lines)


def view_joint(data_list):
    """
    输出多人联合分析报告
    data_list: [{"name": str, "birth": dict, "bazi": Fate/dict}, ...]
    """
    lines = ["━━━ 联合分析 ━━━"]

    for d in data_list:
        bazi    = d["bazi"]
        is_fate = isinstance(bazi, Fate)
        gender_d = "男" if str(d["birth"].get("gender", '1')) in ('1', '男') else "女"

        if is_fate:
            bazi_str = bazi.bazi_str
            mingge_v = bazi.mingge
        else:
            raw = bazi.get("bazi", {})
            bazi_str = " ".join(raw.values()) if isinstance(raw, dict) else str(raw)
            mingge_v = bazi.get("mingge", "")

        lines.append(f"【{d['name']}】{gender_d} | {bazi_str} | {mingge_v}")

    lines.append("━━━ 合冲刑害 ━━━")

    # 年支关系
    year_rels = [_get_branch(d["bazi"], "year", isinstance(d["bazi"], Fate)) for d in data_list]
    year_rel_label = _branch_interaction(year_rels)
    year_zhis_label = ', '.join([f"{d['name']}{z}" for d, z in zip(data_list, year_rels)])
    lines.append(f"年支关系：{year_rel_label}（{year_zhis_label}）")

    # 日支关系
    day_rels = [_get_branch(d["bazi"], "day", isinstance(d["bazi"], Fate)) for d in data_list]
    day_rel_label = _branch_interaction(day_rels)
    day_zhis_label = ', '.join([f"{d['name']}{z}" for d, z in zip(data_list, day_rels)])
    lines.append(f"日支关系：{day_rel_label}（{day_zhis_label}）")

    # 月支关系
    month_rels = [_get_branch(d["bazi"], "month", isinstance(d["bazi"], Fate)) for d in data_list]
    lines.append(
        f"月支关系：{_branch_interaction(month_rels)}"
    )

    # 五行契合
    if len(data_list) >= 2:
        char_sets = []
        for d in data_list:
            bazi = d["bazi"]
            if isinstance(bazi, Fate):
                chars = (
                    bazi.year_pillar.stem  + bazi.year_pillar.branch  +
                    bazi.month_pillar.stem + bazi.month_pillar.branch +
                    bazi.day_pillar.stem   + bazi.day_pillar.branch   +
                    bazi.hour_pillar.stem  + bazi.hour_pillar.branch
                )
            else:
                raw = bazi.get("bazi", {})
                chars = ''.join(raw.values()) if isinstance(raw, dict) else ''
            char_sets.append(chars)
        lines += ["", "━━━ 五行契合 ━━━", _wuxing_affinity(char_sets)]

    # 婚配分析（两人）
    if len(data_list) == 2:
        lines += ["", "━━━ 婚配分析 ━━━", _marriage_analysis(data_list[0], data_list[1])]

    return '\n'.join(lines)
