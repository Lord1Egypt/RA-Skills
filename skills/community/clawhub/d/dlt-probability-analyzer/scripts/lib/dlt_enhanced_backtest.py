"""
大乐透增强回测模块
1. 扩展回测到300期（已支持）
2. 新增ML模型回测（加权频率/随机森林）
3. 新增命中分布统计（0-5球各多少次）
4. 新增"5组全买"模拟回测
"""
import json
import random
import math
from collections import Counter
from datetime import datetime

# 导入ML模型和核心引擎
from dlt_ml_models import weighted_frequency_model, simplified_random_forest
from dlt_exhaustive import load_valid_combos, compute_prediction_pipeline

PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}


def load_history():
    """加载历史数据"""
    with open('dlt_history.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def enhanced_backtest(draws, test_periods=200, random_trials=100):
    """增强回测
    
    测试内容：
    1. 原有5种策略（随机/CDM/马尔可夫/频率/V8组合）
    2. ML模型（加权频率/随机森林）
    3. 命中分布统计
    4. 5组全买模拟
    
    Args:
        draws: 全部历史数据
        test_periods: 测试期数
        random_trials: 随机试验次数
    """
    random.seed(42)
    
    print("\n" + "=" * 70)
    print("【V8.5 增强回测 - 200期 + ML模型 + 命中分布】")
    print("=" * 70)
    
    # 加载有效组合
    valid_combos = load_valid_combos()
    valid_set = set(tuple(sorted(c)) for c in valid_combos) if valid_combos else set()
    print(f"  有效组合: {len(valid_combos):,}个")
    print(f"  测试期数: {test_periods}")
    print(f"  随机试验: {random_trials}次/期")
    
    results = {
        'random_avg': [],
        'cdm': [],
        'markov': [],
        'frequency': [],
        'combined_v8': [],
        'combined_filtered': [],
        'ml_weighted': [],
        'ml_forest': [],
        'back_hits': [],
        'back_random': [],
        # 5组全买模拟
        'five_group_front_hits': [],
        'five_group_back_hits': [],
    }
    
    # 命中分布
    hit_distribution = {
        'combined_v8': Counter(),
        'combined_filtered': Counter(),
        'ml_weighted': Counter(),
        'ml_forest': Counter(),
    }
    
    test_start = len(draws) - test_periods
    
    for t in range(test_start, len(draws)):
        train = draws[:t]
        if len(train) < 50:
            continue
        
        actual_next_front = set(draws[t]['front'])
        actual_next_back = set(draws[t]['back'])
        prev_front = draws[t-1]['front']
        
        # 随机基线
        random_hits = []
        for _ in range(random_trials):
            pred = set(sorted(random.sample(range(1, 36), 5)))
            random_hits.append(len(pred & actual_next_front))
        results['random_avg'].append(sum(random_hits) / len(random_hits))
        
        # 随机后区基线
        random_back_hits = []
        for _ in range(random_trials):
            pred_back = set(sorted(random.sample(range(1, 13), 2)))
            random_back_hits.append(len(pred_back & actual_next_back))
        results['back_random'].append(sum(random_back_hits) / len(random_back_hits))
        
        # 核心预测管线
        combined_score, cdm_probs, markov_prob, freq_30, front_omit, back_top4 = \
            compute_prediction_pipeline(train, valid_combos, prev_front)
        
        # CDM策略
        pred_cdm = set([n for n, _ in sorted(cdm_probs.items(), key=lambda x: x[1], reverse=True)[:5]])
        hit_cdm = len(pred_cdm & actual_next_front)
        results['cdm'].append(hit_cdm)
        
        # 马尔可夫策略
        pred_markov = set([n for n, _ in sorted(markov_prob.items(), key=lambda x: x[1], reverse=True)[:5]])
        results['markov'].append(len(pred_markov & actual_next_front))
        
        # 频率法
        front_freq = Counter()
        for d in train:
            for n in d['front']:
                front_freq[n] += 1
        pred_freq = set([n for n, _ in front_freq.most_common(5)])
        results['frequency'].append(len(pred_freq & actual_next_front))
        
        # V8组合策略
        pred_v8 = set([n for n, _ in sorted(combined_score.items(), key=lambda x: x[1], reverse=True)[:5]])
        hit_v8 = len(pred_v8 & actual_next_front)
        results['combined_v8'].append(hit_v8)
        hit_distribution['combined_v8'][hit_v8] += 1
        
        # V8从有效组合中选
        if valid_combos:
            valid_dynamic = [c for c in valid_combos if len(set(c) & set(prev_front)) <= 2]
            scored = [(c, sum(combined_score[n] for n in c)/5) for c in valid_dynamic]
            scored.sort(key=lambda x: x[1], reverse=True)
            if scored:
                best = set(scored[0][0])
                hit_f = len(best & actual_next_front)
                results['combined_filtered'].append(hit_f)
                hit_distribution['combined_filtered'][hit_f] += 1
            else:
                results['combined_filtered'].append(0)
                hit_distribution['combined_filtered'][0] += 1
        else:
            results['combined_filtered'].append(hit_v8)
            hit_distribution['combined_filtered'][hit_v8] += 1
        
        # ML模型: 加权频率
        wf_front, wf_back = weighted_frequency_model(train, window=30)
        # 从有效组合中选评分最高的
        if valid_combos:
            valid_dynamic = [c for c in valid_combos if len(set(c) & set(prev_front)) <= 2]
            scored_wf = [(c, sum(wf_front[n] for n in c)/5) for c in valid_dynamic]
            scored_wf.sort(key=lambda x: x[1], reverse=True)
            if scored_wf:
                pred_wf = set(scored_wf[0][0])
            else:
                pred_wf = set(sorted(range(1,36), key=lambda x: wf_front[x], reverse=True)[:5])
        else:
            pred_wf = set(sorted(range(1,36), key=lambda x: wf_front[x], reverse=True)[:5])
        hit_wf = len(pred_wf & actual_next_front)
        results['ml_weighted'].append(hit_wf)
        hit_distribution['ml_weighted'][hit_wf] += 1
        
        # ML模型: 随机森林
        rf_front, rf_back = simplified_random_forest(train, n_trees=30, window=50)
        if valid_combos:
            scored_rf = [(c, sum(rf_front[n] for n in c)/5) for c in valid_dynamic]
            scored_rf.sort(key=lambda x: x[1], reverse=True)
            if scored_rf:
                pred_rf = set(scored_rf[0][0])
            else:
                pred_rf = set(sorted(range(1,36), key=lambda x: rf_front[x], reverse=True)[:5])
        else:
            pred_rf = set(sorted(range(1,36), key=lambda x: rf_front[x], reverse=True)[:5])
        hit_rf = len(pred_rf & actual_next_front)
        results['ml_forest'].append(hit_rf)
        hit_distribution['ml_forest'][hit_rf] += 1
        
        # 后区命中
        back_hit = len(set(back_top4[:2]) & set(draws[t]['back']))
        results['back_hits'].append(back_hit)
        
        # 5组全买模拟（前区）
        # 取5种策略的TOP5组合
        five_groups = [pred_cdm, pred_markov, pred_freq, pred_v8]
        if valid_combos and scored:
            five_groups.append(set(scored[0][0]))
        else:
            five_groups.append(pred_v8)
        
        # 5组前区总命中数（去重后覆盖了多少个正确号码）
        all_pred_front = set()
        for g in five_groups:
            all_pred_front |= g
        results['five_group_front_hits'].append(len(all_pred_front & actual_next_front))
        
        # 5组后区总命中数
        all_pred_back = set(back_top4[:4])  # 后区4码
        results['five_group_back_hits'].append(len(all_pred_back & actual_next_back))
        
        # 进度
        if (t - test_start) % 50 == 0:
            print(f"  进度: {t - test_start}/{test_periods} 期")
    
    # 统计分析
    def stats(data):
        n = len(data)
        if n == 0:
            return 0, 0
        mean = sum(data) / n
        var = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else 0
        std = var ** 0.5
        return mean, std
    
    def t_p_value(t_stat, df):
        if df > 30:
            z = abs(t_stat)
            return 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
        else:
            z = abs(t_stat)
            p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
            return min(p * (1 + (z**2 + 1) / (4 * df)), 1.0)
    
    random_mean, random_std = stats(results['random_avg'])
    back_random_mean, _ = stats(results['back_random'])
    
    print(f"\n  测试期数: {len(results['random_avg'])}")
    print(f"\n  {'策略':<28} {'均值':<10} {'标准差':<10} {'vs随机':<10} {'t值':<8} {'p值':<10} {'显著?'}")
    print("  " + "-" * 95)
    
    strategy_labels = {
        'random_avg': '随机基线(100次/期)',
        'cdm': 'CDM贝叶斯',
        'markov': '马尔可夫链',
        'frequency': '频率法',
        'combined_v8': 'V8组合(0.40/0.25/0.20/0.15)',
        'combined_filtered': 'V8组合+有效组合过滤',
        'ml_weighted': 'ML-加权频率模型',
        'ml_forest': 'ML-随机森林(30树)',
    }
    
    summary = {}
    for strategy in ['random_avg', 'cdm', 'markov', 'frequency', 
                     'combined_v8', 'combined_filtered', 'ml_weighted', 'ml_forest']:
        if strategy not in results or not results[strategy]:
            continue
        hits = results[strategy]
        mean, std = stats(hits)
        n = len(hits)
        se = std / (n ** 0.5)
        
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
            p_val = t_p_value(t_stat, len(diffs) - 1)
            vs = f"{mean - random_mean:+.4f}"
            if p_val < 0.05:
                sig = "显著更差" if mean < random_mean else "显著更好"
            else:
                sig = "不显著"
        
        label = strategy_labels.get(strategy, strategy)
        print(f"  {label:<28} {mean:<10.4f} {std:<10.4f} {vs:<10} {t_stat:<8.3f} {p_val:<10.4f} {sig}")
        summary[strategy] = {'mean': mean, 'std': std, 'p_val': p_val, 'significant': p_val < 0.05}
    
    # 后区回测
    print(f"\n  --- 后区回测 ---")
    back_mean, back_std = stats(results['back_hits'])
    print(f"  {'后区(2码)命中':<28} {back_mean:<10.4f} {back_std:<10.4f} {back_mean - back_random_mean:+.4f}")
    print(f"  {'后区随机基线':<28} {back_random_mean:<10.4f}")
    
    # 5组全买模拟
    print(f"\n  --- 5组全买模拟 ---")
    fg_front_mean, fg_front_std = stats(results['five_group_front_hits'])
    fg_back_mean, _ = stats(results['five_group_back_hits'])
    print(f"  {'5组前区覆盖命中':<28} {fg_front_mean:<10.4f} (5组覆盖{fg_front_mean}/5个正确号码)")
    print(f"  {'5组后区覆盖命中':<28} {fg_back_mean:<10.4f} (4码覆盖{fg_back_mean}/2个正确号码)")
    
    # 命中分布
    print(f"\n  --- 命中分布 (200期) ---")
    print(f"  {'策略':<28} {'0球':<8} {'1球':<8} {'2球':<8} {'3球':<8} {'4球':<8} {'5球':<8}")
    print("  " + "-" * 75)
    for strategy in ['combined_v8', 'combined_filtered', 'ml_weighted', 'ml_forest']:
        dist = hit_distribution[strategy]
        total = sum(dist.values())
        label = strategy_labels.get(strategy, strategy)
        counts = [dist.get(i, 0) for i in range(6)]
        pcts = [f"{c}({c/total*100:.1f}%)" if total > 0 else "0" for c in counts]
        print(f"  {label:<28} {pcts[0]:<8} {pcts[1]:<8} {pcts[2]:<8} {pcts[3]:<8} {pcts[4]:<8} {pcts[5]:<8}")
    
    # 结论
    better_significant = any(s.get('significant', False) and s.get('mean', 0) > random_mean 
                            for k, s in summary.items() if k != 'random_avg')
    worse_significant = any(s.get('significant', False) and s.get('mean', 0) < random_mean 
                           for k, s in summary.items() if k != 'random_avg')
    
    print(f"\n  {'=' * 50}")
    if better_significant:
        print(f"  ⚠ 发现显著优于随机的策略！需要进一步验证。")
    elif worse_significant:
        print(f"  ⚠ 部分策略显著差于随机（过拟合），但无策略显著优于随机。")
        print(f"  ✓ 结论不变：大乐透是随机事件，预测不比随机选号更好。")
    else:
        print(f"  ✓ 所有策略均不显著(p>0.05)，与随机基线无统计差异。")
        print(f"  ✓ 结论不变：大乐透是随机事件，预测不比随机选号更好。")
    print(f"  {'=' * 50}")
    
    return results, summary, hit_distribution


if __name__ == '__main__':
    print("=" * 70)
    print("大乐透V8.5增强回测")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    draws = load_history()
    print(f"加载 {len(draws)} 期历史数据")
    
    results, summary, hit_dist = enhanced_backtest(draws, test_periods=200, random_trials=100)
