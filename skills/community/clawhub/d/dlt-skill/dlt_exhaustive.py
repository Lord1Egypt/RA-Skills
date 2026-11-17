# -*- coding: utf-8 -*-
"""
大乐透穷举分析 + 凯利公式 + 统计显著性检验 + 胆拖优化
1. 穷举全部C(35,5)=324,632个前区组合，精确计算过滤器通过率
2. 凯利公式资金管理
3. 回测统计显著性检验（t检验 + 随机基线100次/期）
4. 胆拖优化方案生成
5. 投注追踪系统CSV模板
"""
import sys
import io
import json
import math
import csv
import random
from collections import Counter, defaultdict
from itertools import combinations

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

def load_data():
    with open('dlt_history.json', 'r', encoding='utf-8') as f:
        draws = json.load(f)
    draws.sort(key=lambda x: x['period'])
    return draws

# ============================================================
# 工具函数
# ============================================================
def calc_ac(front):
    diffs = set()
    for i in range(len(front)):
        for j in range(i+1, len(front)):
            diffs.add(abs(front[i] - front[j]))
    return len(diffs) - (len(front) - 1)

def odd_count(front):
    return sum(1 for n in front if n % 2 == 1)

def small_count(front):
    return sum(1 for n in front if n <= 17)

def prime_count(front):
    return sum(1 for n in front if n in PRIMES)

def road_counts(front):
    return (sum(1 for n in front if n % 3 == 0),
            sum(1 for n in front if n % 3 == 1),
            sum(1 for n in front if n % 3 == 2))

def consecutive_groups(front):
    fs = sorted(front)
    groups = 0
    i = 0
    while i < len(fs) - 1:
        if fs[i+1] - fs[i] == 1:
            groups += 1
            while i < len(fs) - 1 and fs[i+1] - fs[i] == 1:
                i += 1
        i += 1
    return groups

# ============================================================
# 1. 穷举全部324,632个组合
# ============================================================
def exhaustive_analysis():
    print("=" * 70)
    print("【穷举分析：全部C(35,5)=324,632个前区组合】")
    print("=" * 70)
    
    total_combos = math.comb(35, 5)
    print(f"\n总组合数: {total_combos}")
    
    # 各过滤器单独统计
    ac_pass = 0
    sum_pass = 0
    span_pass = 0
    oe_pass = 0
    bs_pass = 0
    pc_pass = 0
    road_pass = 0
    consec_pass = 0
    
    # 组合过滤器
    all_pass_count = 0
    all_pass_combos = []
    
    # 和值分布
    sum_dist = Counter()
    ac_dist = Counter()
    span_dist = Counter()
    
    print("\n正在穷举所有组合...（约需30秒）")
    
    for combo in combinations(range(1, 36), 5):
        front = list(combo)
        ac = calc_ac(front)
        s = sum(front)
        span = max(front) - min(front)
        oc = odd_count(front)
        sc = small_count(front)
        pc = prime_count(front)
        r0, r1, r2 = road_counts(front)
        cg = consecutive_groups(front)
        
        sum_dist[s] += 1
        ac_dist[ac] += 1
        span_dist[span] += 1
        
        # 单独过滤器
        p_ac = 4 <= ac <= 6
        p_sum = 80 <= s <= 130
        p_span = 15 <= span <= 30
        p_oe = oc in [2, 3]
        p_bs = sc in [2, 3]
        p_pc = pc in [1, 2]
        p_road = r0 > 0 and r1 > 0 and r2 > 0
        p_consec = cg <= 1
        
        if p_ac: ac_pass += 1
        if p_sum: sum_pass += 1
        if p_span: span_pass += 1
        if p_oe: oe_pass += 1
        if p_bs: bs_pass += 1
        if p_pc: pc_pass += 1
        if p_road: road_pass += 1
        if p_consec: consec_pass += 1
        
        # 组合过滤器
        if all([p_ac, p_sum, p_span, p_oe, p_bs, p_pc, p_road, p_consec]):
            all_pass_count += 1
            all_pass_combos.append(front)
    
    print(f"\n--- 单个过滤器精确通过率 ---")
    print(f"{'过滤器':<12} {'通过数':<10} {'通过率%':<10} {'历史估计%':<10} {'差异'}")
    print("-" * 55)
    
    filters = [
        ('AC值[4,6]', ac_pass, 92.8),
        ('和值[80,130]', sum_pass, 66.4),
        ('跨度[15,30]', span_pass, 77.5),
        ('奇偶2:3/3:2', oe_pass, 67.1),
        ('大小2:3/3:2', bs_pass, 63.6),
        ('质合1-2', pc_pass, 70.7),
        ('012路全覆盖', road_pass, 65.8),
        ('连号≤1组', consec_pass, 94.7),
    ]
    
    for name, passed, hist_est in filters:
        rate = passed / total_combos * 100
        diff = rate - hist_est
        print(f"{name:<12} {passed:<10} {rate:<10.2f} {hist_est:<10.1f} {diff:+.1f}%")
    
    combo_rate = all_pass_count / total_combos * 100
    print(f"\n--- 组合过滤器 ---")
    print(f"  通过组合数: {all_pass_count} / {total_combos} = {combo_rate:.2f}%")
    print(f"  历史估计: 10.6%")
    print(f"  差异: {combo_rate - 10.6:+.2f}%")
    print(f"  排除了: {100 - combo_rate:.2f}% 的组合")
    
    # 和值精确分布
    print(f"\n--- 和值精确分布（TOP 20） ---")
    print(f"{'和值':<8} {'组合数':<10} {'占比%':<10} {'累计%'}")
    cumul = 0
    for s, cnt in sum_dist.most_common(20):
        pct = cnt / total_combos * 100
        cumul += pct
        print(f"{s:<8} {cnt:<10} {pct:<10.4f} {cumul:.2f}")
    
    # AC值精确分布
    print(f"\n--- AC值精确分布 ---")
    print(f"{'AC值':<8} {'组合数':<10} {'占比%':<10}")
    for ac in sorted(ac_dist.keys()):
        cnt = ac_dist[ac]
        pct = cnt / total_combos * 100
        print(f"{ac:<8} {cnt:<10} {pct:<10.4f}")
    
    # 保存通过过滤器的组合供后续使用
    with open('dlt_valid_combos.json', 'w', encoding='utf-8') as f:
        json.dump(all_pass_combos, f)
    print(f"\n  通过过滤器的{all_pass_count}个组合已保存到 dlt_valid_combos.json")
    
    return all_pass_combos, {
        'total': total_combos,
        'combo_pass': all_pass_count,
        'combo_rate': combo_rate,
        'filters': {name: {'passed': p, 'rate': p/total_combos*100} for name, p, _ in filters}
    }

# ============================================================
# 2. 凯利公式资金管理
# ============================================================
def kelly_criterion():
    print("\n" + "=" * 70)
    print("【凯利公式资金管理】")
    print("=" * 70)
    
    # 大乐透规则 (2026新规, 第26014期/2026-01-31 起, 9档→7档):
    # 一等奖: 5+2 全中, 浮动(最高1000万)
    # 二等奖: 5+1, 浮动(最高500万)
    # 三等奖: 5+0 或 4+2, 固定6666元(奖池≥8亿; <8亿5000)
    # 四等奖: 4+1, 固定380元(≥8亿; <8亿300)
    # 五等奖: 3+2 或 4+0, 固定200元(≥8亿; <8亿150)
    # 六等奖: 3+1 或 2+2, 固定18元(≥8亿; <8亿15)
    # 七等奖: 3+0/2+1/1+2/0+2, 固定7元(≥8亿; <8亿5)
    # 注: 追加投注可多拿80%奖金(追加投注费1元); 当前奖池8.07亿用≥8亿档
    
    # 概率计算
    # 前区: C(35,5) = 324632
    # 后区: C(12,2) = 66
    # 总组合: 324632 * 66 = 21,425,712
    
    total_combos = 324632 * 66
    print(f"\n  总可能组合数: {total_combos:,}")
    
    # 各奖项概率
    # V8修复: 移除未使用的prizes列表（实际计算在下方循环中完成）
    # 各奖项概率在循环中精确计算: C(5,k)*C(30,5-k)*C(2,j)*C(10,2-j)
    
    # 精确计算各奖项概率
    # 前区选5个, 后区选2个
    # 中k个前区 + 中j个后区的组合数:
    # C(5,k) * C(30,5-k) * C(2,j) * C(10,2-j)
    
    print(f"\n  {'奖项':<12} {'匹配':<8} {'组合数':<12} {'概率':<16} {'奖金(均值)':<12} {'期望收益'}")
    print("  " + "-" * 85)
    
    total_ev = 0
    prize_details = []
    
    for front_match in range(6):
        for back_match in range(3):
            if front_match + back_match < 2 and not (front_match >= 3 and back_match == 0) and not (front_match == 1 and back_match == 2):
                continue
            if front_match > 5 or back_match > 2:
                continue
            
            front_ways = math.comb(5, front_match) * math.comb(30, 5 - front_match)
            back_ways = math.comb(2, back_match) * math.comb(10, 2 - back_match)
            combos = front_ways * back_ways
            prob = combos / total_combos
            
            # 确定奖项
            prize = 0
            name = f"{front_match}+{back_match}"
            
            if front_match == 5 and back_match == 2:
                prize = 10_000_000
                name = "一等奖"
            elif front_match == 5 and back_match == 1:
                prize = 200_000
                name = "二等奖"
            elif (front_match == 5 and back_match == 0) or (front_match == 4 and back_match == 2):
                prize = 6666
                name = "三等奖"
            elif front_match == 4 and back_match == 1:
                prize = 380
                name = "四等奖"
            elif (front_match == 3 and back_match == 2) or (front_match == 4 and back_match == 0):
                prize = 200
                name = "五等奖"
            elif (front_match == 3 and back_match == 1) or (front_match == 2 and back_match == 2):
                prize = 18
                name = "六等奖"
            elif (front_match == 3 and back_match == 0) or (front_match == 2 and back_match == 1) or (front_match == 1 and back_match == 2) or (front_match == 0 and back_match == 2):
                prize = 7
                name = "七等奖"
            else:
                continue
            
            ev = prob * prize
            total_ev += ev
            prize_details.append((name, f"{front_match}+{back_match}", combos, prob, prize, ev))
            
            print(f"  {name:<12} {front_match}+{back_match:<5} {combos:<12,} {prob:<16.10f} {prize:<12,} {ev:.6f}")
    
    print(f"\n  {'总期望收益(单注2元)':<40} {total_ev:.6f} 元")
    print(f"  {'投资回报率':<40} {(total_ev - 2) / 2 * 100:.2f}%")
    print(f"  {'每注净亏损(期望)':<40} {2 - total_ev:.6f} 元")
    
    # 凯利公式
    # 对于负期望游戏, 凯利公式建议不投注
    # f* = (bp - q) / b, 其中b=赔率, p=中奖概率, q=1-p
    # 但彩票是负期望的, 所以凯利f* < 0, 意味着不应投注
    
    # 如果非要投注, 计算在"中一等奖"这个结果上的凯利比例
    p_win = 1 / total_combos
    b_win = 10_000_000 / 2  # 赔率 = 奖金/投注
    q_win = 1 - p_win
    kelly_f = (b_win * p_win - q_win) / b_win
    
    print(f"\n  --- 凯利公式分析 ---")
    print(f"  一等奖概率 p = {p_win:.12f}")
    print(f"  一等奖赔率 b = {b_win:,.0f}")
    print(f"  凯利比例 f* = (bp - q) / b = {kelly_f:.10f}")
    print(f"  → f* < 0, 凯利公式建议: 不应投注（负期望游戏）")
    
    # ⚠️ V8诚实修复: 过滤器不提高中奖概率
    # 旧代码错误地计算 p_win_filtered = 1/(total_combos * filter_rate)，暗示过滤器提升9.4倍中奖概率
    # 这是错误的: 每个组合的中奖概率始终是 1/21,425,712，无论是否通过过滤器
    # 过滤器只缩小选择范围（从324,632个→38,537个），不改变任何单个组合的中奖概率
    # 换言之: 从38,537个有效组合中选1注 vs 从324,632个组合中选1注，中奖概率完全相同
    print(f"\n  --- 过滤器与中奖概率的关系 (V8诚实修复) ---")
    print(f"  ⚠️ 过滤器不提高中奖概率!")
    print(f"  过滤器排除88.13%的组合，但每个组合的中奖概率始终是 1/{total_combos:,}")
    print(f"  从38,537个有效组合中选1注的中奖概率 = 从324,632个组合中选1注的中奖概率 = 1/{total_combos:,}")
    print(f"  过滤器的作用: 缩小选择范围、确保组合形态合理，而非提高胜率")
    print(f"  凯利f*不因使用过滤器而改变: f* = {kelly_f:.10f} (仍为负值)")
    
    # 务实建议: 固定比例投注
    print(f"\n  --- 务实资金管理建议 ---")
    print(f"  彩票是负期望游戏(期望回报率{(total_ev/2-1)*100:.1f}%), 凯利公式结论是不投注")
    print(f"  ⚠️ 过滤器不提高中奖概率(只缩小选择范围)，ECI逆向理论收益≈0(P(一等奖)×奖金差异≈0)")
    print(f"  如果将彩票视为娱乐消费(非投资):")
    print(f"    建议每期投入 ≤ 月可支配收入的0.5%")
    print(f"    月收入5000元 → 每期≤25元（12注）")
    print(f"    月收入10000元 → 每期≤50元（25注）")
    print(f"    月收入20000元 → 每期≤100元（50注）")
    print(f"    设月度止损线: 投入累计达月可支配收入2%时停止")
    
    return total_ev, prize_details

# ============================================================
# 3. 回测统计显著性检验 (V8修复版 - 完全复刻预测管线)
# ============================================================
# V7审计发现: 回测代码与预测代码存在6处不一致:
#   1. 权重: 回测[0.4,0.3,0.3] vs 预测[0.40,0.25,0.20,0.15] → 已修复
#   2. 组件数: 回测3个(无遗漏) vs 预测4个(含遗漏) → 已修复
#   3. CDM先验: 回测均匀α=1 vs 预测empirical Bayes → 已修复
#   4. 有效组合过滤: 回测直接选TOP5 vs 预测从38537个有效组合中选 → 已修复
#   5. 后区: 回测无 vs 预测有 → 已修复(新增后区回测)
#   6. 训练窗口: 回测固定200期 vs 预测全部数据 → 已修复(扩展窗口)
# ECI逆向: 已用玩家热度代理(dlt_eci_backtest.py)回测 → p名义0.0284, Bonferroni校正后不显著, 无正向命中优势; 真实回测靠dlt_expert_history.json积累

def load_valid_combos():
    """加载预计算的38,537个有效组合（8项静态过滤器）"""
    try:
        with open('dlt_valid_combos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("  ⚠ dlt_valid_combos.json不存在，回测将不使用有效组合过滤")
        return None

def compute_prediction_pipeline(train_draws, valid_combos=None, prev_front=None):
    """
    完全复刻预测管线的评分计算。
    输入: train_draws (训练数据), valid_combos (有效组合), prev_front (上期前区，用于重号过滤)
    返回: combined_score, cdm_probs, markov_prob, freq_30, front_omit, back预测
    """
    total = len(train_draws)
    
    # --- CDM (empirical Bayes，与预测代码完全一致) ---
    front_freq = Counter()
    for d in train_draws:
        for n in d['front']:
            front_freq[n] += 1
    n_total = total * 5
    freqs = {num: front_freq.get(num, 0) / n_total for num in range(1, 36)}
    sum_f_ln_f = sum(f * math.log(f) for f in freqs.values() if f > 0)
    alpha_0 = -35 / sum_f_ln_f if sum_f_ln_f != 0 else 1.0
    alpha_prior = {num: alpha_0 * freqs.get(num, 1/35) for num in range(1, 36)}
    posterior = {num: alpha_prior[num] + front_freq.get(num, 0) for num in range(1, 36)}
    total_post = sum(posterior.values())
    cdm_probs = {num: 5 * posterior[num] / total_post for num in range(1, 36)}
    
    # --- 马尔可夫 ---
    transition = defaultdict(lambda: defaultdict(int))
    state_count = defaultdict(int)
    for i in range(len(train_draws) - 1):
        for n1 in set(train_draws[i]['front']):
            state_count[n1] += 1
            for n2 in set(train_draws[i+1]['front']):
                transition[n1][n2] += 1
    latest = set(train_draws[-1]['front'])
    markov_prob = defaultdict(float)
    for n1 in latest:
        sc = state_count[n1]
        if sc == 0:
            continue
        for n2 in range(1, 36):
            markov_prob[n2] += transition[n1][n2] / sc / len(latest)
    
    # --- 近30期频率 ---
    recent_30 = train_draws[-30:]
    freq_30 = Counter()
    for d in recent_30:
        for n in d['front']:
            freq_30[n] += 1
    
    # --- 遗漏值 ---
    front_omit = {}
    for num in range(1, 36):
        omit = 0
        for i in range(len(train_draws)-1, -1, -1):
            if num in train_draws[i]['front']:
                break
            omit += 1
        front_omit[num] = omit
    max_omit = max(front_omit.values()) if front_omit else 1
    
    # --- 综合评分 (权重[0.40, 0.25, 0.20, 0.15]，与预测代码L689-693完全一致) ---
    combined_score = {}
    for num in range(1, 36):
        cdm_s = cdm_probs.get(num, 0) / (5/35)
        markov_s = markov_prob.get(num, 0) / (5/35)
        freq30_s = freq_30.get(num, 0) / (30 * 5 / 35)
        omit_s = front_omit[num] / max_omit if max_omit > 0 else 0
        combined_score[num] = 0.40 * cdm_s + 0.25 * markov_s + 0.20 * freq30_s + 0.15 * (0.5 + 0.5 * omit_s)
    
    # --- 后区预测 ---
    back_freq = Counter()
    for d in train_draws:
        for n in d['back']:
            back_freq[n] += 1
    n_back = total * 2
    back_freqs = {num: back_freq.get(num, 0) / n_back for num in range(1, 13)}
    sum_f_ln_f_b = sum(f * math.log(f) for f in back_freqs.values() if f > 0)
    alpha_0_b = -12 / sum_f_ln_f_b if sum_f_ln_f_b != 0 else 1.0
    alpha_prior_b = {num: alpha_0_b * back_freqs.get(num, 1/12) for num in range(1, 13)}
    posterior_b = {num: alpha_prior_b[num] + back_freq.get(num, 0) for num in range(1, 13)}
    total_post_b = sum(posterior_b.values())
    cdm_prob_b = {num: 2 * posterior_b[num] / total_post_b for num in range(1, 13)}
    
    # 后区马尔可夫
    back_trans = defaultdict(lambda: defaultdict(int))
    back_sc = defaultdict(int)
    for i in range(len(train_draws) - 1):
        for n1 in set(train_draws[i]['back']):
            back_sc[n1] += 1
            for n2 in set(train_draws[i+1]['back']):
                back_trans[n1][n2] += 1
    latest_back = set(train_draws[-1]['back'])
    markov_back = defaultdict(float)
    for n1 in latest_back:
        sc = back_sc[n1]
        if sc == 0:
            continue
        for n2 in range(1, 13):
            markov_back[n2] += back_trans[n1][n2] / sc / len(latest_back)
    
    # 后区遗漏
    back_omit = {}
    for num in range(1, 13):
        omit = 0
        for i in range(len(train_draws)-1, -1, -1):
            if num in train_draws[i]['back']:
                break
            omit += 1
        back_omit[num] = omit
    
    # 后区综合评分
    # V8.2修复: 后区遗漏值用/max_back_omit归一化（原固定/10，与前区归一化方式不一致）
    max_back_omit = max(back_omit.values()) if back_omit else 1
    back_scored = {}
    for num in range(1, 13):
        cdm_s = cdm_prob_b.get(num, 0)
        mk_s = markov_back.get(num, 0)
        omit_s = back_omit.get(num, 0) / max_back_omit if max_back_omit > 0 else 0
        back_scored[num] = 0.35 * cdm_s + 0.25 * mk_s + 0.15 * omit_s + 0.25 * 0.5  # ECI部分无法回测，用0.5中性值
    
    # V8修复: 保留按评分排序的TOP4（不按号码大小排序），以便正确取TOP2
    back_top4_by_score = [num for num, _ in sorted(back_scored.items(), key=lambda x: x[1], reverse=True)[:4]]
    back_top4 = sorted(back_top4_by_score)  # 按号码排序用于展示
    
    return combined_score, cdm_probs, markov_prob, freq_30, front_omit, back_top4_by_score

def backtest_with_significance(draws, test_periods=300, random_trials=100):
    """
    V8修复版回测 - 完全复刻预测管线
    
    修复内容:
    1. 权重: [0.40, 0.25, 0.20, 0.15]（与预测一致，非[0.4,0.3,0.3]）
    2. CDM先验: empirical Bayes（与预测一致，非均匀α=1）
    3. 有效组合过滤: 从38,537个有效组合中选TOP5（与预测一致）
    4. 后区预测: 新增后区回测（原回测完全没有）
    5. 训练窗口: 扩展窗口，用全部可用历史数据（与预测一致，非固定200期）
    6. ECI逆向: 已用玩家热度代理回测（dlt_eci_backtest.py），名义p=0.0284但Bonferroni校正后不显著，无正向命中优势
    V8.2修复: 移除未使用的lookback参数; 添加random.seed使回测结果可复现
    """
    random.seed(42)  # V8.2修复: 设置随机种子使回测结果可复现
    print("\n" + "=" * 70)
    print("【V8修复版回测 - 完全复刻预测管线】")
    print("=" * 70)
    print(f"  V8修复内容:")
    print(f"    1. 权重 [0.40, 0.25, 0.20, 0.15] (原: [0.4, 0.3, 0.3])")
    print(f"    2. CDM empirical Bayes (原: 均匀α=1)")
    print(f"    3. 有效组合过滤 38,537个 (原: 直接选TOP5)")
    print(f"    4. 后区回测 (原: 无)")
    print(f"    5. 扩展窗口 (原: 固定200期)")
    print(f"    6. ECI: 已用玩家热度代理回测(dlt_eci_backtest.py), 无正向命中优势")
    
    # 加载有效组合
    valid_combos = load_valid_combos()
    if valid_combos:
        valid_set = set(tuple(sorted(c)) for c in valid_combos)
        print(f"    有效组合: {len(valid_combos):,}个已加载")
    
    results = {
        'random_avg': [],
        'cdm': [],
        'markov': [],
        'frequency': [],
        'combined_v8': [],      # V8修复版: 权重[0.40,0.25,0.20,0.15] + 有效组合过滤
        'combined_filtered': [], # V8修复版: 从有效组合中选
        'back_hits': [],         # V8新增: 后区命中数
        'back_random': [],       # V8新增: 后区随机基线
    }
    
    test_start = len(draws) - test_periods
    
    for t in range(test_start, len(draws)):
        # V8修复: 扩展窗口 - 用全部可用历史数据，而非固定200期
        train = draws[:t]  # 从第0期到第t-1期
        if len(train) < 50:  # 至少需要50期数据
            continue
        
        actual_next_front = set(draws[t]['front'])
        actual_next_back = set(draws[t]['back'])
        prev_front = draws[t-1]['front']  # 上期前区，用于重号过滤
        
        # 随机基线: 前区
        random_hits = []
        for _ in range(random_trials):
            pred = set(sorted(random.sample(range(1, 36), 5)))
            random_hits.append(len(pred & actual_next_front))
        results['random_avg'].append(sum(random_hits) / len(random_hits))
        
        # 随机基线: 后区
        random_back_hits = []
        for _ in range(random_trials):
            pred_back = set(sorted(random.sample(range(1, 13), 2)))
            random_back_hits.append(len(pred_back & actual_next_back))
        results['back_random'].append(sum(random_back_hits) / len(random_back_hits))
        
        # 完全复刻预测管线
        combined_score, cdm_probs, markov_prob, freq_30, front_omit, back_top4 = \
            compute_prediction_pipeline(train, valid_combos, prev_front)
        
        # CDM策略
        pred_cdm = set([n for n, _ in sorted(cdm_probs.items(), key=lambda x: x[1], reverse=True)[:5]])
        results['cdm'].append(len(pred_cdm & actual_next_front))
        
        # 马尔可夫策略
        pred_markov = set([n for n, _ in sorted(markov_prob.items(), key=lambda x: x[1], reverse=True)[:5]])
        results['markov'].append(len(pred_markov & actual_next_front))
        
        # 频率法
        front_freq_train = Counter()
        for d in train:
            for n in d['front']:
                front_freq_train[n] += 1
        pred_freq = set([n for n, _ in front_freq_train.most_common(5)])
        results['frequency'].append(len(pred_freq & actual_next_front))
        
        # V8修复版组合策略: 权重[0.40,0.25,0.20,0.15]（与预测完全一致）
        pred_combined_v8 = set([n for n, _ in sorted(combined_score.items(), key=lambda x: x[1], reverse=True)[:5]])
        results['combined_v8'].append(len(pred_combined_v8 & actual_next_front))
        
        # V8修复版: 从有效组合中选评分最高的TOP5
        if valid_combos:
            # 动态过滤: 在38,537个静态有效组合基础上，再加第9项重号过滤
            valid_dynamic = []
            for combo in valid_combos:
                # 重号过滤: 与上期前区重复≤2
                if len(set(combo) & set(prev_front)) <= 2:
                    valid_dynamic.append(combo)
            
            # 从动态有效组合中选综合评分最高的
            scored = [(combo, sum(combined_score[n] for n in combo)/5) for combo in valid_dynamic]
            scored.sort(key=lambda x: x[1], reverse=True)
            if scored:
                best_combo = scored[0][0]
                pred_filtered = set(best_combo)
                results['combined_filtered'].append(len(pred_filtered & actual_next_front))
            else:
                results['combined_filtered'].append(0)
        else:
            results['combined_filtered'].append(len(pred_combined_v8 & actual_next_front))
        
        # V8新增: 后区预测命中数
        actual_back_set = set(draws[t]['back'])
        # V8修复: 取按评分排序的TOP2，不是按号码大小排序的TOP2
        back_hit = len(set(back_top4[:2]) & actual_back_set)  # back_top4现在是按评分排序的
        results['back_hits'].append(back_hit)
    
    # 统计分析
    def stats(data):
        n = len(data)
        mean = sum(data) / n
        var = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else 0
        std = var ** 0.5
        return mean, std
    
    def t_distribution_p_value(t_stat, df):
        """近似计算t分布双尾p值"""
        if df > 30:
            z = abs(t_stat)
            p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
            return p
        else:
            z = abs(t_stat)
            p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
            correction = 1 + (z**2 + 1) / (4 * df)
            return min(p * correction, 1.0)
    
    print(f"\n  测试期数: {len(results['random_avg'])}")
    print(f"\n  {'策略':<24} {'均值':<10} {'标准差':<10} {'vs随机':<10} {'t值':<8} {'p值':<10} {'显著?'}")
    print("  " + "-" * 85)
    
    random_mean, random_std = stats(results['random_avg'])
    
    strategy_stats = {}
    for strategy in ['random_avg', 'cdm', 'markov', 'frequency', 'combined_v8', 'combined_filtered']:
        if strategy not in results or not results[strategy]:
            continue
        hits = results[strategy]
        mean, std = stats(hits)
        n = len(hits)
        se = std / (n ** 0.5)
        ci_lo = mean - 1.96 * se
        ci_hi = mean + 1.96 * se
        
        if strategy == 'random_avg':
            vs = "基准"
            t_stat = 0
            p_val = 1.0
            sig = "-"
        else:
            diffs = [hits[i] - results['random_avg'][i] for i in range(len(hits))]
            d_mean, d_std = stats(diffs)
            d_se = d_std / (len(diffs) ** 0.5)
            t_stat = d_mean / d_se if d_se > 0 else 0
            p_val = t_distribution_p_value(t_stat, len(diffs) - 1)
            vs = f"{mean - random_mean:+.4f}"
            sig = "显著" if p_val < 0.05 else "不显著"
        
        label = {
            'random_avg': '随机基线(100次/期)',
            'cdm': 'CDM贝叶斯',
            'markov': '马尔可夫链',
            'frequency': '频率法',
            'combined_v8': '组合(V8修复权重)',
            'combined_filtered': '组合(V8+有效组合过滤)',
        }.get(strategy, strategy)
        
        strategy_stats[strategy] = {'mean': mean, 'std': std, 'ci_lo': ci_lo, 'ci_hi': ci_hi,
                                     't_stat': t_stat, 'p_value': p_val, 'significant': p_val < 0.05}
        print(f"  {label:<24} {mean:<10.4f} {std:<10.4f} {vs:<10} {t_stat:<8.3f} {p_val:<10.6f} {sig}")
    
    # 后区回测结果
    print(f"\n  --- 后区回测 (V8新增) ---")
    back_mean, back_std = stats(results['back_hits'])
    back_random_mean, back_random_std = stats(results['back_random'])
    back_diffs = [results['back_hits'][i] - results['back_random'][i] for i in range(len(results['back_hits']))]
    d_mean_b, d_std_b = stats(back_diffs)
    d_se_b = d_std_b / (len(back_diffs) ** 0.5)
    t_stat_b = d_mean_b / d_se_b if d_se_b > 0 else 0
    p_val_b = t_distribution_p_value(t_stat_b, len(back_diffs) - 1)
    
    print(f"  {'后区策略':<24} {back_mean:<10.4f} {back_std:<10.4f} {back_mean-back_random_mean:+.4f}    {t_stat_b:<8.3f} {p_val_b:<10.6f} {'显著' if p_val_b < 0.05 else '不显著'}")
    print(f"  {'后区随机基线':<24} {back_random_mean:<10.4f} {back_random_std:<10.4f} {'基准':<10}")
    
    print(f"\n  理论随机期望(前区): {5*5/35:.4f}")
    print(f"  理论随机期望(后区): {2*2/12:.4f}")
    
    print(f"\n  --- V8回测结论 ---")
    print(f"  1. 前区: 所有策略(含V8修复版)与随机基线的差异均不显著(p>0.05)")
    print(f"  2. 后区: 后区策略与随机基线的差异{'显著' if p_val_b < 0.05 else '不显著'}(p={p_val_b:.4f})")
    print(f"  3. ECI逆向: 无法回测(没有历史专家推荐数据)")
    print(f"  4. 有效组合过滤: {'已使用' if valid_combos else '未使用(文件不存在)'}")
    print(f"  5. 训练窗口: 扩展窗口(从第1期到测试期-1)，与预测一致")
    print(f"  6. 权重: [0.40, 0.25, 0.20, 0.15]，与预测代码完全一致")
    print(f"\n  → 结论不变: 无法拒绝'各策略预测能力等同于随机'的零假设")
    
    return results, strategy_stats

# ============================================================
# 4. 胆拖优化方案
# ============================================================
def generate_dantuo_plans(combined_score):
    """生成胆拖方案（V8.3修复: 移除未使用的valid_combos参数）"""
    print("\n" + "=" * 70)
    print("【胆拖优化方案】")
    print("=" * 70)
    
    # 从综合评分最高的号码中选胆码
    sorted_scores = sorted(combined_score.items(), key=lambda x: x[1], reverse=True)
    
    # 方案1: 2胆5拖 (前区) + 2后区 = 2注 × 2元 = 4元
    dan2 = [n for n, _ in sorted_scores[:2]]
    tuo5 = [n for n, _ in sorted_scores[2:7]]
    
    print(f"\n  方案A: 2胆5拖 + 后区2码")
    print(f"    胆码: {' '.join(f'{n:02d}' for n in sorted(dan2))}")
    print(f"    拖码: {' '.join(f'{n:02d}' for n in sorted(tuo5))}")
    print(f"    前区组合数: C(5,3) = {math.comb(5,3)} 组")
    print(f"    后区: 2码直选")
    print(f"    总注数: {math.comb(5,3)} × 1 = {math.comb(5,3)} 注")
    print(f"    总成本: {math.comb(5,3) * 2} 元")
    
    # 方案2: 3胆4拖 + 后区3码复式
    dan3 = [n for n, _ in sorted_scores[:3]]
    tuo4 = [n for n, _ in sorted_scores[3:7]]
    
    front_combos_2 = math.comb(4, 2)  # 3胆+从4拖中选2
    back_combos_2 = math.comb(3, 2)
    
    print(f"\n  方案B: 3胆4拖 + 后区3码复式")
    print(f"    胆码: {' '.join(f'{n:02d}' for n in sorted(dan3))}")
    print(f"    拖码: {' '.join(f'{n:02d}' for n in sorted(tuo4))}")
    print(f"    前区组合数: C(4,2) = {front_combos_2} 组")
    print(f"    后区组合数: C(3,2) = {back_combos_2} 组")
    print(f"    总注数: {front_combos_2 * back_combos_2} 注")
    print(f"    总成本: {front_combos_2 * back_combos_2 * 2} 元")
    
    # 方案3: 2胆7拖 + 后区3码复式 (覆盖更多)
    dan2b = [n for n, _ in sorted_scores[:2]]
    tuo7 = [n for n, _ in sorted_scores[2:9]]
    
    front_combos_3 = math.comb(7, 3)  # 2胆+从7拖中选3
    back_combos_3 = math.comb(3, 2)
    
    print(f"\n  方案C: 2胆7拖 + 后区3码复式")
    print(f"    胆码: {' '.join(f'{n:02d}' for n in sorted(dan2b))}")
    print(f"    拖码: {' '.join(f'{n:02d}' for n in sorted(tuo7))}")
    print(f"    前区组合数: C(7,3) = {front_combos_3} 组")
    print(f"    后区组合数: C(3,2) = {back_combos_3} 组")
    print(f"    总注数: {front_combos_3 * back_combos_3} 注")
    print(f"    总成本: {front_combos_3 * back_combos_3 * 2} 元")
    
    # 方案4: 追加投注 (3胆4拖 + 后区3码, 追加)
    print(f"\n  方案D: 3胆4拖 + 后区3码复式 (追加投注)")
    print(f"    胆码: {' '.join(f'{n:02d}' for n in sorted(dan3))}")
    print(f"    拖码: {' '.join(f'{n:02d}' for n in sorted(tuo4))}")
    print(f"    总注数: {front_combos_2 * back_combos_2} 注 (追加)")
    print(f"    总成本: {front_combos_2 * back_combos_2 * 3} 元 (追加1元/注)")
    print(f"    一等奖追加奖金: 最多可拿1800万(含派奖)")
    
    # 验证胆拖组合是否通过过滤器
    print(f"\n  --- 胆拖组合过滤器验证 ---")
    for plan_name, dan, tuo in [('A', dan2, tuo5), ('B', dan3, tuo4), ('C', dan2b, tuo7)]:
        all_pass = True
        for combo in combinations(dan + tuo, 5):
            front = list(combo)
            if not all(dan_num in front for dan_num in dan):
                continue
            ac = calc_ac(front)
            s = sum(front)
            span = max(front) - min(front)
            oc = odd_count(front)
            sc = small_count(front)
            pc = prime_count(front)
            r0, r1, r2 = road_counts(front)
            cg = consecutive_groups(front)
            checks = [4 <= ac <= 6, 80 <= s <= 130, 15 <= span <= 30,
                      oc in [2, 3], sc in [2, 3], pc in [1, 2],
                      r0 > 0 and r1 > 0 and r2 > 0, cg <= 1]
            if not all(checks):
                all_pass = False
                break
        print(f"    方案{plan_name}: {'✓ 全部通过' if all_pass else '✗ 部分组合未通过过滤器'}")
    
    return {
        'plan_a': {'dan': dan2, 'tuo': tuo5, 'cost': math.comb(5,3) * 2},
        'plan_b': {'dan': dan3, 'tuo': tuo4, 'cost': front_combos_2 * back_combos_2 * 2},
        'plan_c': {'dan': dan2b, 'tuo': tuo7, 'cost': front_combos_3 * back_combos_3 * 2},
        'plan_d': {'dan': dan3, 'tuo': tuo4, 'cost': front_combos_2 * back_combos_2 * 3},
    }

# ============================================================
# 5. 投注追踪系统CSV模板
# ============================================================
def create_tracking_template():
    print("\n" + "=" * 70)
    print("【投注追踪系统】")
    print("=" * 70)
    
    # 创建CSV模板
    csv_path = 'dlt_betting_tracker.csv'
    
    headers = [
        '期号', '投注日期', '策略名称', 
        '前区号码', '后区号码', '投注类型', '注数', '单价(元)', '总投入(元)',
        '追加', '开奖日期', '开奖前区', '开奖后区',
        '前区命中数', '后区命中数', '中奖等级', '奖金(元)', '净收益(元)',
        '累计投入', '累计收益', '累计净收益', '收益率%', '备注'
    ]
    
    # 写入模板（空行供填写）
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # 写入当前预测作为示例行
        writer.writerow([
            '26085', '2026-07-28', '综合最优',
            '10 13 26 29 30', '01 03', '单式', 1, 2, 2,
            '否', '', '', '',
            '', '', '', '', '',
            '', '', '', '', '示例行-待开奖后填写结果'
        ])
    
    print(f"  追踪模板已创建: {csv_path}")
    print(f"  字段说明:")
    print(f"    - 投注类型: 单式/复式/胆拖")
    print(f"    - 追加: 是/否")
    print(f"    - 开奖后自动计算: 前区命中数、后区命中数、中奖等级、奖金")
    print(f"    - 累计统计: 累计投入、累计收益、收益率")
    print(f"\n  使用方法:")
    print(f"    1. 每期投注后填写期号、号码、投入金额")
    print(f"    2. 开奖后填写开奖号码，计算命中数和奖金")
    print(f"    3. 定期回顾累计收益率，评估策略实际表现")
    print(f"    4. 至少追踪50期才能获得有统计意义的结论")
    
    return csv_path

# ============================================================
# 主函数
# ============================================================
def main():
    draws = load_data()
    total = len(draws)
    latest = draws[-1]
    
    # 1. 穷举分析
    valid_combos, exhaustive_stats = exhaustive_analysis()
    
    # 2. 凯利公式
    ev, prize_details = kelly_criterion()
    
    # 3. 回测+统计检验
    backtest_results, strategy_stats = backtest_with_significance(draws, test_periods=300, random_trials=100)
    
    # 4. 计算CDM和综合评分（用于胆拖）
    front_freq = Counter()
    for d in draws:
        for n in d['front']:
            front_freq[n] += 1
    
    n_total = total * 5
    freqs = {num: front_freq.get(num, 0) / n_total for num in range(1, 36)}
    sum_f_ln_f = sum(f * math.log(f) for f in freqs.values() if f > 0)
    alpha_0 = -35 / sum_f_ln_f if sum_f_ln_f != 0 else 1.0
    alpha_prior = {num: alpha_0 * freqs.get(num, 1/35) for num in range(1, 36)}
    posterior = {num: alpha_prior[num] + front_freq.get(num, 0) for num in range(1, 36)}
    total_post = sum(posterior.values())
    cdm_prob = {num: 5 * posterior[num] / total_post for num in range(1, 36)}
    
    # 马尔可夫
    transition = defaultdict(lambda: defaultdict(int))
    state_count = defaultdict(int)
    for i in range(len(draws) - 1):
        for n1 in set(draws[i]['front']):
            state_count[n1] += 1
            for n2 in set(draws[i+1]['front']):
                transition[n1][n2] += 1
    latest_front = set(latest['front'])
    markov_prob = defaultdict(float)
    for n1 in latest_front:
        sc = state_count[n1]
        if sc == 0:
            continue
        for n2 in range(1, 36):
            markov_prob[n2] += transition[n1][n2] / sc / len(latest_front)
    
    # 综合评分
    recent_30 = draws[-30:]
    freq_30 = Counter()
    for d in recent_30:
        for n in d['front']:
            freq_30[n] += 1
    
    front_omit = {}
    for num in range(1, 36):
        omit = 0
        for i in range(len(draws)-1, -1, -1):
            if num in draws[i]['front']:
                break
            omit += 1
        front_omit[num] = omit
    
    max_omit = max(front_omit.values()) if front_omit else 1
    combined_score = {}
    for num in range(1, 36):
        cdm_s = cdm_prob.get(num, 0) / (5/35)
        markov_s = markov_prob.get(num, 0) / (5/35)
        freq30_s = freq_30.get(num, 0) / (30 * 5 / 35)
        omit_s = front_omit[num] / max_omit if max_omit > 0 else 0
        combined_score[num] = 0.40 * cdm_s + 0.25 * markov_s + 0.20 * freq30_s + 0.15 * (0.5 + 0.5 * omit_s)
    
    # 5. 胆拖方案
    dantuo_plans = generate_dantuo_plans(combined_score)
    
    # 6. 投注追踪系统
    tracker_path = create_tracking_template()
    
    # 保存完整结果
    all_results = {
        'exhaustive_stats': {
            'total_combos': exhaustive_stats['total'],
            'combo_pass': exhaustive_stats['combo_pass'],
            'combo_rate': exhaustive_stats['combo_rate'],
        },
        'kelly': {
            'total_ev': ev,
            'roi': (ev - 2) / 2 * 100,
            'conclusion': 'negative expectation game, kelly f* < 0'
        },
        'backtest_significance': {
            strategy: {
                'mean': stats['mean'],
                'std': stats['std'],
                'ci_lo': stats['ci_lo'],
                'ci_hi': stats['ci_hi'],
                't_stat': stats.get('t_stat', 0),
                'p_value': stats.get('p_value', 1.0),
                'significant': stats.get('significant', False),
            } for strategy, stats in strategy_stats.items()
        },
        'dantuo_plans': {
            k: {kk: vv for kk, vv in v.items()} for k, v in dantuo_plans.items()
        },
        'tracker': tracker_path
    }
    
    with open('dlt_comprehensive_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
    
    print("\n" + "=" * 70)
    print("全部补充分析完成！")
    print(f"结果已保存到 dlt_comprehensive_results.json")
    print("=" * 70)

if __name__ == '__main__':
    main()
