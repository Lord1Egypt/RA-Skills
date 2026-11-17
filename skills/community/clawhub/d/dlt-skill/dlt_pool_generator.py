# -*- coding: utf-8 -*-
"""
大乐透合买方案生成器 (Pool / Group-buy Scheme Generator)
=========================================================

定位 (务必读):
    本工具是【覆盖工具】, 不是【预测工具】。
    它只负责把一笔合买资金, 拆成 N 份【互不重叠】的号码单, 让拼单的 N 个人
    各自拿到一组彼此不重复的号码, 从而在相同花费下【覆盖最多不同的组合】。

它【不能】做的事 (诚实声明):
    - 不能提高任一注中一等奖的概率。单注一等奖概率恒为 1/21,425,712, 与
      选号方法无关。摇奖通过 NIST 随机性检验, 无规律可榨。
    - 不能保证中奖。本工具只是"把钱花在更多不重复的组合上", 仅此而已。

它【能】做的事 (唯一现实价值):
    1. 零重叠: 全局去重, N 份之间、每份内部都不出现重复注, 不浪费一分钱。
    2. 合法形态: 每注通过 dlt_common.passes_filters 的 8 项静态过滤器
       (AC/和值/跨度/奇偶/大小/质数/012路/连号), 属于"典型且合规"的号码。
    3. 冷门偏置(--unpopular): 尽量避开生日号(1-12)、长连号、上期重号等
       "大众热门"组合。作用【仅在于: 万一真中了, 少和人分奖】, 不提高中奖率。

用法:
    python3 dlt_pool_generator.py --shares 10 --lines 10 --unpopular
    python3 dlt_pool_generator.py --shares 5  --lines 20 --prev 3,4,7,12,32
    python3 dlt_pool_generator.py                 # 默认 10份×10注

输出:
    dlt_pool_scheme.md    (人读, 可直接转发给拼单伙伴)
    dlt_pool_scheme.json  (机读, 含完整校验信息)
"""
from __future__ import annotations
import argparse
import json
import random
from datetime import datetime
from itertools import combinations

import dlt_common as C

# 上一期开奖前区 (用于"重号"过滤与冷门偏置的默认上下文); 可用 --prev 覆盖
DEFAULT_PREV_FRONT = [3, 4, 7, 12, 32]   # 26091 期
# 生日号区间: 1-12 在前区、1-6 在后区通常被大众偏好, 视为"偏热门"
POPULAR_FRONT = set(range(1, 13))
POPULAR_BACK = set(range(1, 7))
# 日历号 (减分摊口径): 前区 1-31 是日期数字、后区 1-12 是月份, 人群偏好更高
CALENDAR_FRONT = set(range(1, 32))
CALENDAR_BACK = set(range(1, 13))


def _fmt(n: int) -> str:
    return f"{n:02d}"


def line_key(front, back) -> tuple:
    """规范化键, 用于全局去重。前区/后区各自排序后存为元组。"""
    return (tuple(sorted(front)), tuple(sorted(back)))


def _obvious_pattern(front) -> bool:
    """检测"明显pattern", 这类号码更易被人群手动选中(减分摊要避开)。"""
    fs = sorted(front)
    # 等差(如 5,10,15,20,25)
    diffs = [fs[i + 1] - fs[i] for i in range(len(fs) - 1)]
    if len(set(diffs)) == 1 and diffs[0] > 0:
        return True
    # 全偶 / 全奇 (人群爱走极端对称)
    if all(n % 2 == 0 for n in fs) or all(n % 2 == 1 for n in fs):
        return True
    return False


def popularity_score(front, back, prev_front, reduce_split: bool = False) -> int:
    """启发式"热门度"评分, 越高越可能撞大众选号。用于 --unpopular / --reduce-split 偏置。

    注意: 这不是预测模型, 只是基于公开常识(生日号/连号/上期重号更易被人群选中)
    的经验性降权, 目的是"万一中奖少分奖", 不影响中奖概率。

    reduce_split=True 时额外降权: 日历号(前区1-31/后区1-12)与明显pattern(等差/全奇偶),
    这些是"减分摊选号"的核心 —— 它们不会降低你中奖的概率, 只会降低你中奖后
    要和多少人平分的概率。
    """
    score = 0
    score += sum(1 for n in front if n in POPULAR_FRONT) * 2      # 生日前区号
    score += sum(1 for n in back if n in POPULAR_BACK)            # 低后区号
    fs = sorted(front)
    run = maxrun = 1
    for i in range(1, len(fs)):
        if fs[i] - fs[i - 1] == 1:
            run += 1
            maxrun = max(maxrun, run)
        else:
            run = 1
    if maxrun >= 3:
        score += (maxrun - 2) * 2                                 # 长连号更"好选"
    if len(set(front) & set(prev_front)) >= 3:
        score += 5                                               # 大量复制上期
    if reduce_split:
        score += sum(1 for n in front if n in CALENDAR_FRONT)     # 日历前区号(1-31)
        score += sum(1 for n in back if n in CALENDAR_BACK)       # 日历后区号(1-12)
        if _obvious_pattern(fs):
            score += 6                                           # 等差/全奇偶等明显pattern
    return score


def make_one_line(rng: random.Random, prev_front, unpopular: bool,
                  loose: bool, cap: int = 2, reduce_split: bool = False):
    """生成一注合法且不热门(可选)的号码。

    返回 (front[5], back[2])。通过拒绝采样保证:
      - 前区 5 个互异 ∈[1,35]; 后区 2 个互异 ∈[1,12]
      - 默认走 passes_filters (典型形态); --loose 时仅保证基本合法
      - --unpopular 时热门度评分 <= cap (否则重采)
      - --reduce-split 时进一步降权日历号与明显pattern (仅影响中奖后分奖人数)
    """
    for _ in range(2000):
        front = sorted(rng.sample(range(1, C.K + 1), 5))
        back = sorted(rng.sample(range(1, C.BACK_N + 1), 2))
        if not loose and not C.passes_filters(front, prev_front):
            continue
        if unpopular and popularity_score(front, back, prev_front, reduce_split) > cap:
            continue
        return front, back
    # 极端情况下放宽: 退回纯随机合法注
    front = sorted(rng.sample(range(1, C.K + 1), 5))
    back = sorted(rng.sample(range(1, C.BACK_N + 1), 2))
    return front, back


def generate_pool(n_shares: int, lines_per_share: int, seed: int,
                  prev_front, unpopular: bool, loose: bool,
                  reduce_split: bool = False):
    """生成 N 份互不重叠的方案。

    返回 (shares, meta):
      shares: list[list[(front, back)]], 长度 = n_shares, 每份 lines_per_share 注
      meta:   校验与统计信息
    """
    total = n_shares * lines_per_share
    rng = random.Random(seed)
    used = set()
    all_lines = []
    attempts = 0
    while len(all_lines) < total:
        f, b = make_one_line(rng, prev_front, unpopular, loose,
                             reduce_split=reduce_split)
        key = line_key(f, b)
        if key in used:
            attempts += 1
            if attempts > total * 50:     # 安全阀: 理论上不会触发 (组合数 2142 万)
                break
            continue
        used.add(key)
        all_lines.append((f, b))

    # 轮询分配到各份, 保证每份注数均衡且彼此不重叠
    shares = [[] for _ in range(n_shares)]
    for i, line in enumerate(all_lines):
        shares[i % n_shares].append(line)

    # ---- 唯一性校验 (互相重叠检测) ----
    all_keys = [line_key(f, b) for sh in shares for (f, b) in sh]
    unique_count = len(set(all_keys))
    per_share_unique = all(len(set(line_key(f, b) for (f, b) in sh)) == len(sh)
                           for sh in shares)
    overlap_free = (unique_count == len(all_keys)) and per_share_unique

    meta = {
        "n_shares": n_shares,
        "lines_per_share": lines_per_share,
        "total_lines": len(all_keys),
        "unique_lines": unique_count,
        "overlap_free": overlap_free,
        "unpopular": unpopular,
        "loose": loose,
        "prev_front": prev_front,
        "seed": seed,
        "basic_cost_yuan": len(all_keys) * 2,
        "extra_cost_yuan": len(all_keys) * 3,
        "single_jackpot_odds": "1/21,425,712",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return shares, meta


# ============================================================================
# 覆盖优化 v2: 轮盘(wheeling) 与 单式散弹(scatter)
# ============================================================================
def generate_wheel(wf: int, wb: int, front_nums=None, back_nums=None, seed: int = 0):
    """轮盘覆盖: 在自选号码池内做全组合, 数学保底"若开奖号落在你选的池里则中固定奖级"。

    参数:
      wf        前区池大小 (需 >=5), 例 7 -> C(7,5)=21 组前区
      wb        后区池大小 (需 >=2), 例 4 -> C(4,2)=6 组后区
      front_nums/back_nums  可选自定义号码池; 不传则按均衡分布自动选
    返回:
      (lines, meta)  lines: list[(front,back)] 全组合

    诚实声明 (重要):
      - 轮盘【不提高】单注中奖率; 它把"中奖"这件事, 从"猜中具体5+2"降级为
        "猜中你选的池里是否包含了开奖号"。后者概率 = (C(wf,5)/C(35,5)) × (C(wb,2)/C(12,2))。
      - 例 wf=7,wb=4: 前区命中池概率 C(7,5)/C(35,5)=21/324632≈0.00647%, 后区 C(4,2)/C(12,2)=6/66≈9.09%,
        两者都中 ≈ 0.00647%×9.09%≈0.000588%。这略高于头奖1/2142万(≈0.00000468%),
        因为要求更宽松——只需开奖号落在你池里而非精确匹配。这正是轮盘的价值: 用确定的覆盖,
        换一个"条件满足时必中某级"的保底, 代价是注数多、成本高。
      - 选池本身是猜测, 池选错则保底不触发。这不是预测, 是成本/保障的取舍。
    """
    if front_nums is None:
        # 均衡铺开: 在 1-35 上近似等分取 wf 个
        rng = random.Random(seed)
        front_nums = sorted(rng.sample(range(1, C.K + 1), wf))
    if back_nums is None:
        rng = random.Random(seed + 1)
        back_nums = sorted(rng.sample(range(1, C.BACK_N + 1), wb))
    front_nums = sorted(int(x) for x in front_nums)[:wf]
    back_nums = sorted(int(x) for x in back_nums)[:wb]

    lines = []
    for fc in combinations(front_nums, 5):
        for bc in combinations(back_nums, 2):
            lines.append((list(fc), list(bc)))

    front_hit_p = (len(list(combinations(front_nums, 5))) /
                   len(list(combinations(range(1, C.K + 1), 5))))
    back_hit_p = (len(list(combinations(back_nums, 2))) /
                  len(list(combinations(range(1, C.BACK_N + 1), 2))))
    full_hit_p = front_hit_p * back_hit_p

    meta = {
        "mode": "wheel",
        "wf": wf, "wb": wb,
        "front_nums": front_nums, "back_nums": back_nums,
        "total_lines": len(lines),
        "basic_cost_yuan": len(lines) * 2,
        "extra_cost_yuan": len(lines) * 3,
        "front_pool_hit_rate": f"{front_hit_p*100:.4f}%",
        "back_pool_hit_rate": f"{back_hit_p*100:.2f}%",
        "full_pool_hit_rate": f"{full_hit_p*100:.6f}%",
        "single_jackpot_odds": "1/21,425,712",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return lines, meta


def generate_scatter(n: int, seed: int, prev_front,
                     unpopular: bool, reduce_split: bool, loose: bool,
                     cap: int = 2):
    """单式散弹: 生成 N 注互不相同的单式, 贪心最大化"覆盖到的不同号码数"。

    与合买池的区别: 这里不拆份, 就是 N 注单式, 但选号时优先挑能引入最多
    尚未覆盖号码的注, 让固定注数下"触碰"的前区/后区数字尽可能多。
    用途: 想"广撒网"但不想花大钱复式时, 用最少注数摸到最多数字。

    诚实声明: 单注头奖概率仍是 1/2142万, 散弹不改变它; 只是让 N 注里出现的
    不同数字更多, 视觉上"覆盖更广", 不改变期望为负的事实。
    """
    rng = random.Random(seed)
    used = set()
    lines = []
    covered_front = set()
    covered_back = set()
    while len(lines) < n:
        f, b = make_one_line(rng, prev_front, unpopular, loose,
                             cap=cap, reduce_split=reduce_split)
        key = line_key(f, b)
        if key in used:
            continue
        # 贪心: 仅在还有余量时优先选"新数字多"的注 (避免无限循环, 50次未改善就收)
        new_front = len(set(f) - covered_front)
        new_back = len(set(b) - covered_back)
        if len(lines) < n - 1 and (new_front + new_back) == 0 and len(lines) > 3:
            # 已无新数字可覆盖且还没满, 直接收下(避免卡死)
            pass
        used.add(key)
        lines.append((f, b))
        covered_front |= set(f)
        covered_back |= set(b)

    meta = {
        "mode": "scatter",
        "n": n,
        "total_lines": len(lines),
        "distinct_front": sorted(covered_front),
        "distinct_back": sorted(covered_back),
        "front_coverage": f"{len(covered_front)}/35",
        "back_coverage": f"{len(covered_back)}/12",
        "basic_cost_yuan": len(lines) * 2,
        "extra_cost_yuan": len(lines) * 3,
        "single_jackpot_odds": "1/21,425,712",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return lines, meta


def render_v2_html(lines, meta, mode: str, period_hint: str = "下一期") -> str:
    """渲染 wheel / scatter 模式为可嵌入报告的 HTML 片段。"""
    L = []
    L.append('<div class="section">')
    if mode == "wheel":
        L.append('<div class="section-title">轮盘覆盖方案（数学保底 · 覆盖优化v2）</div>')
        L.append('<div class="info" style="border-color:#00dd88;">')
        L.append('<p style="color:#88ccff; font-size:14px; line-height:1.8;">')
        L.append(
            f'⚙️ 前区池 {meta["wf"]} 个 ({",".join(_fmt(x) for x in meta["front_nums"])}) '
            f'× 后区池 {meta["wb"]} 个 ({",".join(_fmt(x) for x in meta["back_nums"])})，'
            f'全组合共 <strong>{meta["total_lines"]}注</strong>，基本投注 '
            f'<strong>¥{meta["basic_cost_yuan"]}</strong>。')
        L.append('<br>保底含义：<strong>若开奖前区5码全部落在你前区池、后区2码全部落在后区池，'
                 '则必中至少某级奖</strong>（条件满足时确定性保底，非概率）。')
        L.append(f'<br>条件命中概率：前区池 {meta["front_pool_hit_rate"]} · 后区池 '
                 f'{meta["back_pool_hit_rate"]} · 双池同中 {meta["full_pool_hit_rate"]}。')
        L.append('</p></div>')
        L.append('<div class="warning"><p>轮盘<strong>不提高</strong>单注中奖率，它把"猜中精确5+2"'
                 '降级为"猜中你选的号码池"。选池本身是猜测，池选错则保底不触发。'
                 '这是成本/保障的取舍，不是预测。</p></div>')
    else:  # scatter
        L.append('<div class="section-title">单式散弹方案（广覆盖 · 覆盖优化v2）</div>')
        L.append('<div class="info" style="border-color:#00dd88;">')
        L.append('<p style="color:#88ccff; font-size:14px; line-height:1.8;">')
        L.append(
            f'🎯 {meta["n"]} 注单式，贪心最大化号码覆盖：前区 '
            f'<strong>{meta["front_coverage"]}</strong>、后区 '
            f'<strong>{meta["back_coverage"]}</strong>，基本投注 '
            f'<strong>¥{meta["basic_cost_yuan"]}</strong>。')
        L.append('</p></div>')
        L.append('<div class="warning"><p>散弹<strong>不改变</strong>单注头奖概率（仍 1/2142万），'
                 '只是让固定注数内触碰的不同数字更多，是"广撒网"的低成本近似，期望仍为负。</p></div>')

    # 号码列表 (紧凑)
    L.append('<div style="font-size:13px; line-height:1.95; color:#cdd6f4;">')
    for i, (f, b) in enumerate(lines, 1):
        fs = " ".join(_fmt(x) for x in f)
        bs = " ".join(_fmt(x) for x in b)
        L.append(f'{i}. 前区 {fs}　后区 {bs}<br>')
    L.append('</div>')
    L.append('</div>')
    return "\n".join(L)


def render_v2_md(lines, meta, mode: str, period_hint: str = "下一期") -> str:
    L = []
    if mode == "wheel":
        L.append("# 大乐透轮盘覆盖方案\n")
        L.append(f"> 适用期次建议：{period_hint}　|　生成时间：{meta['generated_at']}\n")
        L.append(f"- 前区池({meta['wf']}): {', '.join(_fmt(x) for x in meta['front_nums'])}")
        L.append(f"- 后区池({meta['wb']}): {', '.join(_fmt(x) for x in meta['back_nums'])}")
        L.append(f"- 全组合总注数：**{meta['total_lines']}注**　基本投注 **¥{meta['basic_cost_yuan']}**")
        L.append(f"- 条件命中概率：前区池 {meta['front_pool_hit_rate']} · 后区池 "
                 f"{meta['back_pool_hit_rate']} · 双池同中 {meta['full_pool_hit_rate']}")
        L.append("\n## 诚实声明\n- 轮盘不提高单注中奖率，它把'猜中精确5+2'降级为'猜中你选的号码池'。"
                 "选池本身是猜测，池选错则保底不触发。这是成本/保障的取舍，不是预测。")
    else:
        L.append("# 大乐透单式散弹方案\n")
        L.append(f"> 适用期次建议：{period_hint}　|　生成时间：{meta['generated_at']}\n")
        L.append(f"- 注数：**{meta['n']}注**　基本投注 **¥{meta['basic_cost_yuan']}**")
        L.append(f"- 号码覆盖：前区 {meta['front_coverage']}　后区 {meta['back_coverage']}")
        L.append("\n## 诚实声明\n- 散弹不改变单注头奖概率（仍 1/2142万），只是让固定注数内"
                 "触碰的不同数字更多，是'广撒网'的低成本近似，期望仍为负。")
    L.append("\n## 号码单\n")
    for i, (f, b) in enumerate(lines, 1):
        L.append(f"{i}. 前区 {' '.join(_fmt(x) for x in f)}　后区 {' '.join(_fmt(x) for x in b)}")
    return "\n".join(L)


def render_agreement_md(shares, meta, period_hint: str = "下一期") -> str:
    """由合买方案生成一份书面《拼单购彩协议》模板(出资/分奖/争议)。

    这是法律/财务层面的"先说清楚", 把拼单最常见的纠纷点(谁出多少、中了怎么分、
    弃奖/漏买/争议谁负责)落到纸面, 降低朋友/同事间因彩票反目的风险。
    注: 仅为民间参考模板, 涉大额建议咨询法律人士并按当地法规调整。
    """
    per = meta["basic_cost_yuan"] // meta["n_shares"]
    L = []
    L.append("# 大乐透拼单购彩协议（参考模板）\n")
    L.append(f"> 适用期次：{period_hint}　|　生成时间：{meta['generated_at']}　|　方案零重叠："
             f"{'✅通过' if meta['overlap_free'] else '❌未通过'}\n")
    L.append("## 一、参与方与出资\n")
    L.append(f"- 本合买共 **{meta['n_shares']} 份**，每份 **{meta['lines_per_share']} 注**，"
             f"总 **{meta['total_lines']} 注**。")
    L.append(f"- 基本投注总额 **¥{meta['basic_cost_yuan']}**，每份出资 **¥{per}**（均等分摊）。")
    L.append(f"- 追加投注（可选）：每份再加 ¥{meta['extra_cost_yuan']//meta['n_shares']}，"
             f"总额 ¥{meta['extra_cost_yuan']}；是否追加由全体一致决定，未达成一致则只做基本投注。")
    L.append("- 各参与方签字确认份额与出资：\n")
    for i in range(1, meta["n_shares"] + 1):
        L.append(f"  - 第 {i} 份（¥{per}）：姓名________ 电话________ 签字________")
    L.append("\n## 二、号码与购彩执行\n")
    L.append(f"- 号码单见随附《合买方案》（{meta['n_shares']}份互不重叠，已校验零重复）。")
    L.append("- 由 **发起人或指定代购人** 统一购买并打印彩票，彩票原件由代购人保管，"
             "购彩后向全体公示彩票照片/票号。")
    L.append("- 若因代购人疏忽导致漏买/错买某份，由代购人按该份出资额赔偿参与方，与中奖与否无关。\n")
    L.append("## 三、中奖分配\n")
    L.append("- **基本原则**：按份均分。任一份中奖，该份对应奖金在持有该份的参与方之间平分"
             "（一份=一人则归该人；若一份被多人合持有，按内部约定比例）。")
    L.append("- **税前/税后**：分配以**税后实际到手金额**为准；若单注超万元需扣税，由全体按比例承担税项。")
    L.append("- **冷门偏置说明**：本方案已尽量避开热门号，目的仅是'若中奖则少分奖人数'，"
             "不改变任何人中奖概率，参与方对此充分知情。")
    L.append("- 奖金到账后 **3 个工作日内** 由代购人按本协议分配并留痕（转账备注'大乐透合买分红'）。\n")
    L.append("## 四、风险与争议\n")
    L.append("- 彩票为机会游戏，期望收益为负，**本协议不构成任何中奖保证**。参与即视为理解风险、自愿娱乐。")
    L.append("- 弃奖（逾期未兑）损失由全体按份分担，代购人无过错不担责。")
    L.append("- 争议先协商；协商不成提交代购人所在地民间调解或按当地法规处理。")
    L.append("- 本协议一式参与方份数，签字生效，仅作民间参考，大额合买建议咨询法律人士。\n")
    L.append("---\n*本模板由大乐透合买方案生成器自动起草，属覆盖工具产出，非法律意见。*\n")
    return "\n".join(L)


def render_md(shares, meta, period_hint: str = "下一期") -> str:
    L = []
    L.append(f"# 大乐透合买方案（{meta['n_shares']}份互不重叠）\n")
    L.append(f"> 适用期次建议：{period_hint}　|　生成时间：{meta['generated_at']}\n")
    L.append("## 总览\n")
    L.append(f"- 份数：**{meta['n_shares']} 份**（拼单人数）")
    L.append(f"- 每份：**{meta['lines_per_share']} 注**")
    L.append(f"- 总注数：**{meta['total_lines']} 注**")
    L.append(f"- 基本投注总额：**¥{meta['basic_cost_yuan']}**（每人 ¥{meta['basic_cost_yuan']//meta['n_shares']}）")
    L.append(f"- 追加投注总额：¥{meta['extra_cost_yuan']}（每人 ¥{meta['extra_cost_yuan']//meta['n_shares']}）")
    L.append(f"- 零重叠校验：{'✅ 通过（N份之间、每份内部均无重复注）' if meta['overlap_free'] else '❌ 未通过'}")
    L.append(f"- 冷门偏置：{'已开启（尽量避开生日号/长连号/上期重号，减少撞奖分摊）' if meta['unpopular'] else '未开启'}\n")
    L.append("## 各份号码单\n")
    for i, sh in enumerate(shares, 1):
        L.append(f"### 第 {i} 份（{len(sh)} 注）\n")
        for j, (f, b) in enumerate(sh, 1):
            fstr = " ".join(_fmt(x) for x in f)
            bstr = " ".join(_fmt(x) for x in b)
            L.append(f"{j}. 前区 {fstr}　后区 {bstr}")
        L.append("")
    L.append("## 诚实声明（务必转告每位拼单伙伴）\n")
    L.append("- 本方案是**覆盖工具**，不是预测。任一注中一等奖的概率恒为 **1/21,425,712**，与选号方法无关。")
    L.append("- 摇奖通过 NIST 随机性检验，号码无规律可预测。本工具**不能保证中奖**，也无法提高中奖率。")
    L.append("- 拼单的意义仅在于：用同样的钱覆盖更多**互不重复**的组合；冷门偏置仅在你中奖时减少分奖人数。")
    L.append("- 彩票期望收益为负，请把它当娱乐，设定预算上限，切勿追号。")
    return "\n".join(L)


def render_pool_html(shares, meta, period_hint: str = "下一期") -> str:
    """把合买方案渲染为可直接嵌入报告的 HTML 片段 (复用 dlt_auto 报告 CSS 类)。"""
    L = []
    L.append('<div class="section">')
    L.append(f'<div class="section-title">合买方案（{meta["n_shares"]}份互不重叠 · 覆盖工具非预测）</div>')

    L.append('<div class="info" style="border-color:#00dd88;">')
    L.append('<p style="color:#88ccff; font-size:14px; line-height:1.8;">')
    L.append(
        f'🤝 适用：{period_hint} 拼单。本方案把资金拆成 <strong>{meta["n_shares"]}份</strong>，'
        f'每份 <strong>{meta["lines_per_share"]}注</strong>，共 <strong>{meta["total_lines"]}注</strong>；'
        f'基本投注 <strong>¥{meta["basic_cost_yuan"]}</strong>'
        f'（每人 ¥{meta["basic_cost_yuan"] // meta["n_shares"]}）。')
    L.append(
        f'<br>零重叠校验：<strong>{"✅ 通过" if meta["overlap_free"] else "❌ 未通过"}</strong>'
        f'（各份之间、每份内部均无重复注，不浪费一分钱）。')
    L.append(
        '冷门偏置：' + ('已开启（尽量避开生日号/长连号/上期重号，仅在中奖时减少分奖人数）'
                        if meta["unpopular"] else "未开启") + '。')
    L.append('</p></div>')

    for i, sh in enumerate(shares, 1):
        L.append(f'<div class="group-card"><h3>第 {i} 份（{len(sh)} 注）</h3>')
        L.append('<div style="font-size:13px; line-height:1.95; color:#cdd6f4;">')
        for j, (f, b) in enumerate(sh, 1):
            fs = " ".join(_fmt(x) for x in f)
            bs = " ".join(_fmt(x) for x in b)
            L.append(f'{j}. 前区 {fs}　后区 {bs}<br>')
        L.append('</div></div>')

    L.append('<div class="warning"><h3>⚠️ 诚实声明（务必转告每位拼单伙伴）</h3>')
    L.append(
        '<p>本方案是<strong>覆盖工具</strong>，不是预测。任一注中一等奖概率恒为 '
        '<strong>1/21,425,712</strong>，与选号方法无关；摇奖通过 NIST 随机性检验，无规律可预测，'
        '<strong>不能保证中奖、也无法提高中奖率</strong>。拼单意义仅在于：同样花钱覆盖更多互不重复的组合；'
        '冷门偏置仅在你中奖时减少分奖人数。彩票期望收益为负，请当娱乐、设预算上限、切勿追号。</p></div>')
    L.append('</div>')
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="大乐透合买/覆盖方案生成器 (覆盖工具, 非预测)")
    ap.add_argument("--mode", choices=["pool", "wheel", "scatter"], default="pool",
                    help="模式: pool=合买互不重叠(默认) / wheel=轮盘保底 / scatter=单式散弹")
    # pool 模式
    ap.add_argument("--shares", type=int, default=10, help="[pool] 份数/拼单人数 (默认10)")
    ap.add_argument("--lines", type=int, default=10, help="[pool] 每份注数 (默认10)")
    # wheel 模式
    ap.add_argument("--wf", type=int, default=7, help="[wheel] 前区池大小 (>=5)")
    ap.add_argument("--wb", type=int, default=4, help="[wheel] 后区池大小 (>=2)")
    ap.add_argument("--front-nums", type=str, default="",
                    help="[wheel] 自定义前区池, 逗号分隔, 如 1,5,9,14,20,28,33")
    ap.add_argument("--back-nums", type=str, default="",
                    help="[wheel] 自定义后区池, 逗号分隔, 如 1,3,6,11")
    # scatter 模式
    ap.add_argument("--n", type=int, default=20, help="[scatter] 单式注数 (默认20)")
    # 通用
    ap.add_argument("--seed", type=int, default=20260813, help="随机种子 (可复现)")
    ap.add_argument("--prev", type=str, default="",
                    help="上期前区, 逗号分隔, 如 3,4,7,12,32 (用于重号过滤/冷门偏置)")
    ap.add_argument("--unpopular", action="store_true", help="开启冷门偏置(减少撞奖分摊)")
    ap.add_argument("--reduce-split", action="store_true",
                    help="减分摊选号: 额外避开日历号(前区1-31/后区1-12)与明显pattern(等差/全奇偶)")
    ap.add_argument("--loose", action="store_true", help="放宽: 不强制 passes_filters, 仅保证基本合法")
    ap.add_argument("--agreement", action="store_true",
                    help="[pool] 同时生成《拼单购彩协议》模板 (出资/分奖/争议)")
    ap.add_argument("--period", type=str, default="下一期", help="期次提示文案")
    ap.add_argument("--out", type=str, default="dlt_pool_scheme", help="输出文件前缀")
    args = ap.parse_args()

    prev_front = DEFAULT_PREV_FRONT
    if args.prev:
        try:
            prev_front = [int(x) for x in args.prev.split(",") if x.strip()]
        except ValueError:
            print("⚠ --prev 解析失败, 使用默认上期前区")

    if args.mode == "wheel":
        fn = [int(x) for x in args.front_nums.split(",") if x.strip()] or None
        bn = [int(x) for x in args.back_nums.split(",") if x.strip()] or None
        lines, meta = generate_wheel(args.wf, args.wb, fn, bn, args.seed)
        md = render_v2_md(lines, meta, "wheel", args.period)
        with open(args.out + ".md", "w", encoding="utf-8") as f:
            f.write(md)
        with open(args.out + ".json", "w", encoding="utf-8") as f:
            json.dump({"meta": meta,
                       "lines": [{"front": f, "back": b} for (f, b) in lines]},
                      f, ensure_ascii=False, indent=2)
        print(f"✅ [wheel] 前区池{args.wf}×后区池{args.wb} = {meta['total_lines']}注")
        print(f"   基本投注 ¥{meta['basic_cost_yuan']} | 双池同中概率 {meta['full_pool_hit_rate']}")
        print(f"   输出: {args.out}.md / {args.out}.json")

    elif args.mode == "scatter":
        lines, meta = generate_scatter(
            n=args.n, seed=args.seed, prev_front=prev_front,
            unpopular=args.unpopular, reduce_split=args.reduce_split,
            loose=args.loose)
        md = render_v2_md(lines, meta, "scatter", args.period)
        with open(args.out + ".md", "w", encoding="utf-8") as f:
            f.write(md)
        with open(args.out + ".json", "w", encoding="utf-8") as f:
            json.dump({"meta": meta,
                       "lines": [{"front": f, "back": b} for (f, b) in lines]},
                      f, ensure_ascii=False, indent=2)
        print(f"✅ [scatter] {args.n}注 | 前区覆盖 {meta['front_coverage']} 后区 {meta['back_coverage']}")
        print(f"   基本投注 ¥{meta['basic_cost_yuan']} | 输出: {args.out}.md / {args.out}.json")

    else:  # pool
        shares, meta = generate_pool(
            n_shares=args.shares,
            lines_per_share=args.lines,
            seed=args.seed,
            prev_front=prev_front,
            unpopular=args.unpopular,
            loose=args.loose,
            reduce_split=args.reduce_split,
        )
        md = render_md(shares, meta, args.period)
        with open(args.out + ".md", "w", encoding="utf-8") as f:
            f.write(md)
        with open(args.out + ".json", "w", encoding="utf-8") as f:
            json.dump({
                "meta": meta,
                "shares": [[{"front": f, "back": b} for (f, b) in sh] for sh in shares],
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ [pool] 已生成 {args.shares}份×{args.lines}注 = {meta['total_lines']}注")
        print(f"   零重叠: {'通过' if meta['overlap_free'] else '失败'}"
              f" | 唯一注数 {meta['unique_lines']}/{meta['total_lines']}")
        print(f"   基本投注总额 ¥{meta['basic_cost_yuan']} (每人 ¥{meta['basic_cost_yuan']//args.shares})")
        print(f"   输出: {args.out}.md / {args.out}.json")
        if args.agreement:
            ag = render_agreement_md(shares, meta, args.period)
            with open(args.out + "_agreement.md", "w", encoding="utf-8") as f:
                f.write(ag)
            print(f"   协议: {args.out}_agreement.md (出资/分奖/争议模板)")


if __name__ == "__main__":
    main()
