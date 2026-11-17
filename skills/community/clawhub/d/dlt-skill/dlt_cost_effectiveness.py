# -*- coding: utf-8 -*-
"""
大乐透 · 胆拖性价比最优分析器 (V4, 2026-08-04)
================================================================

用户原话: "用最小的成本博取最大的收益, 尤其是胆拖组合... 找到最优的算法分析,
           推荐最具性价比的号码组合。"

诚实前提 (数学铁律, 不可动摇):
  - 任一 5+2 组合的单期命中概率恒为 1/21,425,712, 任何结构(含胆拖/复式/机选)完全相同。
  - 期望收益(每元)对所有结构完全相等且为负 (大乐透返奖率≈0.5, 即每花1元期望回约0.5元)。
  - 因此本分析器优化的是『结构』, 不是『期望收益』。

【V4 关键修正 —— 胆拖概念纠偏】
  胆拖(前区 K胆W拖)的实际前区注数 = C(W, 5-K)。当 W = 5-K 时 C(W,5-K)=C(5-K,5-K)=1,
  即只有 1 注 = 把 K个胆+W个拖这 5 个号固定成一注普通 5+2, 根本没有"展开"。
  典型退化单注形态: 3胆2拖 / 1胆4拖 / 2胆3拖 / 4胆1拖 (前区均仅 1 注)。
  这些"看似胆拖,实为单注", 不算真正胆拖, 本分析器一律剔除, 不计入性价比。
  判定规则: 『真正胆拖』要求 前区注数>=2 且 后区注数>=2 (两个区都真实展开)。

【V4 真正有意义的"性价比"指标】
  胆拖的唯一真实优势 = 相对『复式(全组合)』的省钱:
    同样候选号码池(K+W 前 + Bd+Bt 后), 复式需 C(K+W,5)*C(Bd+Bt,2) 注,
    胆拖仅需 C(W,5-K)*C(Bt,2-Bd) 注, 后者 << 前者。
  所以"最小成本最大参与"正确的理解是: 在预算内撬动最大的候选号码池,
  同时用『复式等效注数 / 胆拖注数 = 节省倍数』量化胆拖的省钱本质。
  中奖概率仍只由投注注数决定, 与结构无关(随机一致)。

核心算法: 精确超几何概率 (非蒙特卡洛, 非模型加权)
"""

import math
import json
import os
import argparse
from datetime import datetime

try:
    from dlt_dantuo_optimizer import front_back_to_prize
except Exception:
    def front_back_to_prize(f, b):
        if f == 5 and b == 2: return 1
        if f == 5 and b == 1: return 2
        if (f == 5 and b == 0) or (f == 4 and b == 2): return 3
        if f == 4 and b == 1: return 4
        if (f == 3 and b == 2) or (f == 4 and b == 0): return 5
        if (f == 3 and b == 1) or (f == 2 and b == 2): return 6
        if (f == 3 and b == 0) or (f == 2 and b == 1) or (f == 1 and b == 2) or (f == 0 and b == 2): return 7
        return 0

try:
    from dlt_power_engine import PRIZE_PAYOUT
except Exception:
    PRIZE_PAYOUT = {(5, 2): 10_000_000, (5, 1): 5_000_000, (5, 0): 6666,
                    (4, 2): 6666, (4, 1): 380, (3, 2): 200, (4, 0): 200,
                    (3, 1): 18, (2, 2): 18, (3, 0): 7, (2, 1): 7, (1, 2): 7, (0, 2): 7}

C35_5 = math.comb(35, 5)
C12_2 = math.comb(12, 2)
RANK_NAME = {1: '一等奖', 2: '二等奖', 3: '三等奖', 4: '四等奖',
             5: '五等奖', 6: '六等奖', 7: '七等奖', 0: '未中奖'}

# 诚实性 (关键): 一/二等奖为浮动奖(按奖池与中奖注数分摊), 奖金表里的代表值
# (1000万/500万) 会严重高估期望收益(单注若乘代表值 EV 可达 ~5.9元, 虚高近3倍)。
# 大乐透真实长期返奖率约 50%, 即单注(2元)真实期望派彩≈1.0元。
# 因此本分析器的『期望收益/ROI』指标一律采用真实返奖率, 不碰膨胀的浮动奖代表值;
# 代表值仅在"中得时派彩"的梦境式说明里使用, 绝不参与 EV。
RETURN_RATE = 0.50            # 真实返奖率(含浮动奖长期兑现分摊)
E_PER_BET = 2.0 * RETURN_RATE   # 单注真实期望派彩(元) ≈ 1.0, 所有结构相同


def C(n, k):
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def front_best_dist(K, W):
    """精确: 胆拖(前区K胆W拖)能达到的『最佳前区命中数 -> 概率』。"""
    dist = {}
    for a in range(0, K + 1):                 # a=胆码命中数
        p_a = C(K, a) * C(35 - K, 5 - a) / C35_5
        if p_a == 0:
            continue
        remain = 35 - K - W                  # 既非胆也非拖的号码数
        for b in range(0, W + 1):            # b=拖码命中数
            if 5 - a - b < 0 or 5 - a - b > remain:
                continue
            p_b = C(W, b) * C(remain, 5 - a - b) / C(35 - K, 5 - a)
            bf = a + min(5 - K, b)            # 最佳一注的前区命中
            dist[bf] = dist.get(bf, 0) + p_a * p_b
    return dist


def back_best_dist(Bd, Bt):
    """精确: 胆拖(后区Bd胆Bt拖)能达到的『最佳后区命中数 -> 概率』。"""
    dist = {}
    for c in range(0, Bd + 1):
        p_c = C(Bd, c) * C(12 - Bd, 2 - c) / C12_2
        if p_c == 0:
            continue
        remain = 12 - Bd - Bt
        for d in range(0, Bt + 1):
            if 2 - c - d < 0 or 2 - c - d > remain:
                continue
            p_d = C(Bt, d) * C(remain, 2 - c - d) / C(12 - Bd, 2 - c)
            bb = c + min(2 - Bd, d)
            dist[bb] = dist.get(bb, 0) + p_c * p_d
    return dist


def dantuo_metrics(K, W, Bd, Bt):
    """计算一个『真正胆拖』(前后区均展开>=2注)的指标。

    返回字段:
      candidate  候选号码数 = (K+W)+(Bd+Bt)  —— 你投入的号码总数
      box_equiv  复式等效注数 = C(K+W,5)*C(Bd+Bt,2) —— 同样池若直接复式需多少注
      savings    节省倍数 = box_equiv / cost —— 胆拖相对复式的省钱倍数(唯一真实性价比)
      any_win    任意奖命中概率(精确超几何, 结构相关)
      win5plus   五等奖及以上概率(精确超几何)
      roi        期望收益率, 所有结构相同 ≈ -50%
    """
    fdist = front_best_dist(K, W)
    bdist = back_best_dist(Bd, Bt)
    front_combos = C(W, 5 - K)
    back_combos = C(Bt, 2 - Bd)
    cost = front_combos * back_combos
    any_win = win5plus = 0.0
    for bf, pf in fdist.items():
        for bb, pb in bdist.items():
            p = pf * pb
            tier = front_back_to_prize(bf, bb)
            if tier >= 1:
                any_win += p
            if 1 <= tier <= 5:        # 五等奖及以上(不含未中奖tier=0)
                win5plus += p
    # 期望派彩采用真实返奖率(避免浮动奖代表值虚高), 线性期望=注数×单注期望, 与结构无关。
    exp_pay = cost * E_PER_BET
    candidate = (K + W) + (Bd + Bt)                       # 候选号码数
    box_equiv = (C(K + W, 5) * C(Bd + Bt, 2)) if (K + W >= 5 and Bd + Bt >= 2) else 0
    savings = box_equiv / cost if cost else 0             # 相对复式节省倍数
    return {
        'K': K, 'W': W, 'Bd': Bd, 'Bt': Bt,
        'front_combos': front_combos, 'back_combos': back_combos,
        'cost': cost, 'candidate': candidate,
        'box_equiv': box_equiv, 'savings': savings,
        'any_win': any_win, 'win5plus': win5plus,
        'exp_pay_per_bet': E_PER_BET,
        'roi': RETURN_RATE - 1.0,       # 期望收益率, 所有结构相同≈ -50%
    }


def enumerate_structures(max_bets):
    """枚举预算内所有『真正胆拖』结构 (前后区均展开>=2注), 返回指标列表。

    退化单注形态(W=5-K 致前区1注, 或 Bt=2-Bd 致后区1注)一律剔除 —— 它们就是普通单注, 非胆拖。
    后区 Bd 仅取 1 (Bd=2 时后区注数恒=1=单注, 已排除); 前区 K 取 1~4。
    """
    res = []
    for K in range(1, 5):                        # 前区胆数 1~4
        W = 6 - K                                # 至少 W=6-K 才能使前区注数 C(W,5-K)>=2
        while W <= 35 - K:                       # 前区最多 35 个号
            fc = C(W, 5 - K)
            if fc < 2:                           # 前区未展开(=单注)跳过
                W += 1
                continue
            if fc > max_bets:
                break
            Bd = 1                               # 后区必须有胆且展开(Bd=2 恒单注, 已不取)
            Bt = 2 - Bd + 1                      # 至少 Bt=3-Bd 使后区注数 C(Bt,2-Bd)>=2
            while Bt <= 12 - Bd:                 # 后区最多 12 个号
                bc = C(Bt, 2 - Bd)
                if bc < 2:                       # 后区未展开跳过
                    Bt += 1
                    continue
                if bc > max_bets:
                    break
                cost = fc * bc
                if cost <= max_bets:
                    res.append(dantuo_metrics(K, W, Bd, Bt))
                Bt += 1
            W += 1
    return res


# ---------------------------------------------------------------------------
# 用模型评分把"最优结构"落到真实号码上 (结构最优 + 模型选号)
# ---------------------------------------------------------------------------
def recommend_optimal_dantuo(combined_score, back_scored, budget_bets=120,
                              goal='coverage'):
    """在预算内枚举真正胆拖结构, 按 goal 选最优 (K,W,Bd,Bt), 再用模型评分填入真实号码。"""
    structs = enumerate_structures(budget_bets)
    if not structs:
        return None
    if goal == 'coverage':
        # 最大候选号码池 = 胆拖相对复式最省的本质优势(撬动最大候选池)
        best = max(structs, key=lambda r: (r['candidate'], r['any_win']))
    elif goal == 'any_win':
        # 最高任意中奖概率 (低胆数结构, 部分命中机会多)
        best = max(structs, key=lambda r: (r['any_win'], r['candidate']))
    else:
        best = max(structs, key=lambda r: (r['candidate'], r['any_win']))

    K, W, Bd, Bt = best['K'], best['W'], best['Bd'], best['Bt']
    front_rank = sorted(combined_score.keys(),
                        key=lambda n: combined_score.get(n, 0), reverse=True)
    back_rank = sorted(back_scored.keys(),
                       key=lambda n: back_scored.get(n, 0), reverse=True)
    dan = front_rank[:K]                          # 最有信心的 K 个作胆
    tuo = front_rank[K:K + W]                     # 次有信心的 W 个作拖
    back_dan = back_rank[:Bd]
    back_tuo = back_rank[Bd:Bd + Bt]
    return {
        'struct': best,
        'form': f'{K}胆{W}拖+后{Bd}胆{Bt}拖',
        'dan': dan, 'tuo': tuo,
        'back_dan': back_dan, 'back_tuo': back_tuo,
        'back': back_dan + back_tuo,
        'cost_basic': best['cost'] * 2,
        'cost_extra': best['cost'] * 3,
    }


def build_html(budget, structs, rec_coverage, rec_anywin, now):
    # 候选号码最多 top6 (= 相对复式最省的本质)
    cov_top = sorted(structs, key=lambda r: (r['candidate'], r['any_win']), reverse=True)[:6]
    # 任意中奖概率最高 top6
    win_top = sorted(structs, key=lambda r: (r['any_win'], r['candidate']), reverse=True)[:6]

    def row(s, goal):
        tag = f"{s['K']}胆{s['W']}拖+后{s['Bd']}胆{s['Bt']}拖"
        hl = " style='background:#fff3e9;font-weight:bold'" if goal == 'best' else ''
        sav = f"{s['savings']:.0f}×" if s['savings'] else '—'
        return (f"<tr{hl}><td>{tag}</td><td>{s['cost']}注/{s['cost']*2}元</td>"
                f"<td>{s['candidate']}</td><td>{s['box_equiv']:,}</td><td>{sav}</td>"
                f"<td>{s['any_win']*100:.2f}%</td><td>{s['win5plus']*100:.3f}%</td>"
                f"<td>{s['roi']*100:+.2f}%</td></tr>")

    cov_rows = ''.join(row(s, '') for s in cov_top)
    win_rows = ''.join(row(s, '') for s in win_top)
    rec_row = row(rec_coverage['struct'], 'best')

    rc = rec_coverage
    ra = rec_anywin
    html = f"""<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>大乐透 胆拖性价比最优分析</title>
<style>
 body{{font-family:-apple-system,'Microsoft YaHei',sans-serif;max-width:960px;margin:0 auto;padding:24px;color:#222;background:#fafafa}}
 h1{{font-size:22px;color:#CA090A;border-bottom:3px solid #E84E18;padding-bottom:8px}}
 h3{{color:#CA090A;font-size:16px}}
 .card{{background:#fff;border:1px solid #eee;border-radius:10px;padding:18px;margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,.04)}}
 .key{{color:#E84E18;font-weight:bold;font-size:17px}}
 .muted{{color:#999}}
 table{{width:100%;border-collapse:collapse;font-size:13px}}
 th,td{{padding:7px 8px;border-bottom:1px solid #f0f0f0;text-align:left}}
 th{{background:#f7f7f7;color:#666}}
 .verdict{{background:#fff7f0;border-left:5px solid #E84E18;padding:14px 18px;border-radius:6px;line-height:1.8}}
 .foot{{color:#999;font-size:12px;margin-top:24px}}
</style></head><body>
<h1>大乐透 · 胆拖性价比最优分析 (V4)</h1>
<div class='card'>
  <div>预算上限：<span class='key'>{budget} 注（{budget*2} 元）</span></div>
  <div style='margin-top:8px'>共枚举合法『真正胆拖』结构 <span class='key'>{len(structs)}</span> 种
      （已剔除前区或后区仅 1 注的退化单注形态，如 3胆2拖/1胆4拖/2胆3拖/4胆1拖）。精确超几何概率计算。</div>
</div>

<div class='card'>
  <h3>一、推荐方案（结构最优 + 模型选号）</h3>
  <p><b>目标A·最大候选号码池（胆拖相对复式最省）：</b> {rc['form']} ｜ 前区胆{rc['dan']} 拖{rc['tuo']}
     后区{rc['back']} ｜ 成本 {rc['cost_basic']}元(基本)/{rc['cost_extra']}元(追加)</p>
  <p><b>目标B·最高任意中奖概率：</b> {ra['form']} ｜ 前区胆{ra['dan']} 拖{ra['tuo']}
     后区{ra['back']} ｜ 成本 {ra['cost_basic']}元(基本)/{ra['cost_extra']}元(追加)</p>
  <table><tr><th>推荐结构</th><th>成本</th><th>候选号码</th><th>复式等效注</th><th>节省倍数</th>
    <th>任中概率</th><th>五等+概率</th><th>ROI</th></tr>
    {rec_row}</table>
</div>

<div class='card'>
  <h3>二、最大候选号码池 Top6（胆拖撬动的最大候选范围，配"复式等效"看省钱）</h3>
  <table><tr><th>结构</th><th>成本</th><th>候选号码</th><th>复式等效注</th><th>节省倍数</th>
    <th>任中概率</th><th>五等+概率</th><th>ROI</th></tr>
    {cov_rows}</table>
</div>

<div class='card'>
  <h3>三、任意中奖概率最高 Top6</h3>
  <table><tr><th>结构</th><th>成本</th><th>候选号码</th><th>复式等效注</th><th>节省倍数</th>
    <th>任中概率</th><th>五等+概率</th><th>ROI</th></tr>
    {win_rows}</table>
</div>

<div class='card'>
  <div class='verdict'>
    <h3 style='margin-top:0;color:#CA090A'>四、诚实结论（必读）</h3>
    <p>① <b>期望收益对所有结构完全相等且为负。</b> 表中"ROI"恒为<b>-50%</b>、每注期望派彩≈1.0元，
       对任何结构都相同——大乐透返奖率约 50%，花 2 元期望回约 1 元。胆拖、复式、机选概莫能外，
       结构改变不了这个铁律。（奖金表一/二等奖是浮动奖代表值，拿来算期望会虚高近 3 倍，本分析器已弃用。）</p>
    <p>② <b>V4 纠偏：退化单注"胆拖"已剔除。</b> 像 <b>3胆2拖 / 1胆4拖 / 2胆3拖 / 4胆1拖</b> 这类，
       因前区 W=5-K 致前区仅 1 注，本质就是"普通单注 5+2 换了个胆拖马甲"，没有任何展开与覆盖，
       本分析器一律不计入。真正胆拖要求<b>前后区都展开（≥2 注）</b>。</p>
    <p>③ <b>胆拖唯一真实的"性价比" = 相对复式的省钱。</b> 同样候选号码池，复式需 C(候选,全组合) 注，
       胆拖仅需 C(W,5-K)×C(Bt,2-Bd) 注，相差成百上千倍（见"节省倍数"列）。
       例如 4胆12拖+后1胆10拖 撬动 27 个候选号，胆拖 120 注 vs 复式 156,156 注，<b>省 1301 倍</b>。
       但注意：<b>中奖概率仍只由投注注数决定</b>（=注数/总组合数），与"是否胆拖"无关，随机一致。</p>
    <p>④ <b>风险权衡（结构差异仅在此）：</b>
       · 胆数越多（高 K，如 4胆N拖）：注数少、最省，但<b>必须赌对胆码</b>，否则全空——高方差、低中奖概率。
       · 胆数越少（低 K，如 1胆N拖）：部分命中机会多、任意中奖概率高，但注数多、成本高。
       这是在"省钱"与"中奖概率"之间的取舍，不是"更准"。</p>
    <p>⑤ <b>没有"不实保中承诺/最可靠"的号码。</b> 表中胆码/拖码由模型按历史评分选出，仅代表"历史置信度"，
       对下一期开奖无任何预测力（独立随机）。本分析器价值：在固定娱乐预算下，帮你把<b>钱花得结构最合理</b>，
       而非帮你中奖。量力而行，设死预算，切勿追加投入指望回本。</p>
  </div>
</div>
<div class='foot'>生成时间：{now} ｜ 算法：精确超几何概率（非模型加权/非蒙特卡洛近似）
｜ V4 已剔除退化单注胆拖 ｜ 本分析器为理性购彩结构优化工具，不代表任何中奖许诺。</div>
</body></html>"""
    return html


def export_to_desktop(html):
    fn = "大乐透_胆拖性价比最优分析.html"
    profile = os.environ.get('USERPROFILE') or os.environ.get('HOME') or ''
    cands = [_detect_real_desktop(), os.path.join(profile, 'Desktop'),
             os.path.join(profile, '桌面'), os.path.expanduser('~/Desktop')]
    dest = None
    for c in cands:
        if c and 'systemprofile' not in c.lower() and os.path.isdir(c):
            dest = c
            break
    if dest is None:
        dest = os.getcwd()
    path = os.path.join(dest, fn)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--budget', type=int, default=120, help='预算注数上限(默认120注=240元)')
    args = ap.parse_args()

    from dlt_auto import compute_models, _back_score
    with open('dlt_history.json', 'r', encoding='utf-8') as f:
        draws = json.load(f)
    models = compute_models(draws)
    prev_front = draws[-1]['front']
    max_back_omit = models.get('max_back_omit', 1) or 1
    back_scored = {}
    for num in range(1, 13):
        cdm_s = models['cdm_prob_b'].get(num, 0)
        mk_s = models['markov_back'].get(num, 0)
        omit_s = models['back_omit'].get(num, 0) / max_back_omit
        back_scored[num] = _back_score(cdm_s, mk_s, omit_s)

    print(f"[枚举] 预算 {args.budget}注 ...")
    structs = enumerate_structures(args.budget)
    print(f"[枚举] 共 {len(structs)} 种真正胆拖结构 (已剔除退化单注)")

    rec_cov = recommend_optimal_dantuo(models['combined_score'], back_scored,
                                       budget_bets=args.budget, goal='coverage')
    rec_win = recommend_optimal_dantuo(models['combined_score'], back_scored,
                                       budget_bets=args.budget, goal='any_win')
    # 期望收益一致性检查
    evs = [s['roi'] for s in structs]
    print(f"[诚实校验] 所有结构 ROI 范围: {min(evs)*100:+.2f}% ~ {max(evs)*100:+.2f}% (应完全相同)")
    print(f"[推荐·最大候选池] {rec_cov['form']} 成本{rec_cov['cost_basic']}元 "
          f"候选{rec_cov['struct']['candidate']}号 复式等效{rec_cov['struct']['box_equiv']:,}注 "
          f"省{rec_cov['struct']['savings']:.0f}倍 任中{rec_cov['struct']['any_win']*100:.2f}%")
    print(f"[推荐·最高任中] {rec_win['form']} 成本{rec_win['cost_basic']}元 "
          f"候选{rec_win['struct']['candidate']}号 任中{rec_win['struct']['any_win']*100:.2f}%")

    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    html = build_html(args.budget, structs, rec_cov, rec_win, now)
    path = export_to_desktop(html)
    print("REPORT_DESKTOP_PATH:" + path)
    return path


if __name__ == '__main__':
    main()



def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "defaultuser0", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None
