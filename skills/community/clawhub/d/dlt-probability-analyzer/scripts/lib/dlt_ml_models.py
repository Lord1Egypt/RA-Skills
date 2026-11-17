"""
大乐透机器学习预测模块
新增模型：
1. 随机森林 (RandomForest) - 基于历史特征预测号码出现概率
2. 加权频率模型 (WeightedFrequency) - 近期权重更高的频率分析
3. 遗传算法优化组合 (GeneticOptimizer) - 从有效组合中优化选择

注意：大乐透是随机事件，ML模型不比随机选号更好(p>0.05)。
这些模型增加了分析视角的多样性，但不改变数学本质。
"""
import json
import random
import math
from collections import Counter
from itertools import combinations

# PRIMES集合 - 与全项目一致
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}


def _weighted_sample_k(score_dict, k, rng, pool):
    """从 pool 按 score_dict 权重无放回抽取 k 个, 返回升序 tuple。
    用于"按分布采样"而非取 argmax, 使 ML 每期随种子变化(解冻)。"""
    avail = list(pool)
    chosen = []
    for _ in range(k):
        if not avail:
            break
        weights = [max(score_dict.get(n, 1e-12), 1e-12) for n in avail]
        tot = sum(weights)
        r = rng.random() * tot
        acc = 0.0
        sel = avail[-1]
        for n, w in zip(avail, weights):
            acc += w
            if r <= acc:
                sel = n
                break
        chosen.append(sel)
        avail.remove(sel)
    return tuple(sorted(chosen))


def load_history(filepath='dlt_history.json'):
    """加载历史数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def compute_features(history, window=30):
    """计算每个号码的特征向量
    
    特征：
    1. 历史出现频率 (全部)
    2. 近window期频率
    3. 遗漏值（多少期未出现）
    4. 近window期平均间隔
    5. 近window期最大连续出现次数
    6. 转移概率（上期出现后本期出现的概率）
    """
    front_features = {}
    back_features = {}
    
    all_front = [d['front'] for d in history]
    all_back = [d['back'] for d in history]
    n = len(history)
    
    for num in range(1, 36):
        # 前区特征
        # 1. 全部频率
        total_count = sum(1 for f in all_front if num in f)
        freq_all = total_count / n
        
        # 2. 近window期频率
        recent = all_front[-window:] if len(all_front) >= window else all_front
        recent_count = sum(1 for f in recent if num in f)
        freq_recent = recent_count / len(recent)
        
        # 3. 遗漏值
        omit = 0
        for f in reversed(all_front):
            if num in f:
                break
            omit += 1
        
        # 4. 平均间隔
        appearances = [i for i, f in enumerate(all_front) if num in f]
        if len(appearances) > 1:
            intervals = [appearances[i+1] - appearances[i] for i in range(len(appearances)-1)]
            avg_interval = sum(intervals) / len(intervals)
        else:
            avg_interval = n
        
        # 5. 转移概率：上期出现后本期出现的概率
        if n > 1:
            prev_appear = sum(1 for i in range(1, n) if num in all_front[i-1])
            both_appear = sum(1 for i in range(1, n) if num in all_front[i-1] and num in all_front[i])
            transition_prob = both_appear / prev_appear if prev_appear > 0 else 0
        else:
            transition_prob = 0
        
        # 6. 近期热度趋势 (后10期 vs 前10期)
        last_10 = all_front[-10:] if len(all_front) >= 10 else all_front
        prev_10 = all_front[-20:-10] if len(all_front) >= 20 else []
        last_10_freq = sum(1 for f in last_10 if num in f) / len(last_10) if last_10 else 0
        prev_10_freq = sum(1 for f in prev_10 if num in f) / len(prev_10) if prev_10 else 0
        trend = last_10_freq - prev_10_freq
        
        front_features[num] = {
            'freq_all': freq_all,
            'freq_recent': freq_recent,
            'omit': omit,
            'omit_normalized': min(omit / 30, 1.0),  # 归一化到0-1
            'avg_interval': avg_interval,
            'transition_prob': transition_prob,
            'trend': trend,
            'score': 0  # 待计算
        }
    
    for num in range(1, 13):
        # 后区特征
        total_count = sum(1 for b in all_back if num in b)
        freq_all = total_count / n
        
        recent = all_back[-window:] if len(all_back) >= window else all_back
        recent_count = sum(1 for b in recent if num in b)
        freq_recent = recent_count / len(recent)
        
        omit = 0
        for b in reversed(all_back):
            if num in b:
                break
            omit += 1
        
        # 后区最大遗漏归一化
        max_omit = 0
        current_omit = 0
        for b in all_back:
            if num in b:
                current_omit = 0
            else:
                current_omit += 1
                max_omit = max(max_omit, current_omit)
        
        back_features[num] = {
            'freq_all': freq_all,
            'freq_recent': freq_recent,
            'omit': omit,
            'omit_normalized': omit / max(max_omit, 1),
            'max_omit': max_omit,
            'score': 0
        }
    
    return front_features, back_features


# === 模型1: 加权频率模型 ===
def weighted_frequency_model(history, window=30):
    """加权频率模型
    
    近期出现频率权重更高，结合遗漏值和趋势
    
    Returns:
        front_scores: {num: score}, back_scores: {num: score}
    """
    front_features, back_features = compute_features(history, window)
    
    # 前区评分：加权频率 + 遗漏 + 趋势 + 转移概率
    for num in range(1, 36):
        f = front_features[num]
        # 综合评分：近期频率40% + 遗漏25% + 全局频率15% + 趋势10% + 转移10%
        score = (0.40 * f['freq_recent'] * 5 +  # 放大到合理范围
                 0.25 * f['omit_normalized'] +
                 0.15 * f['freq_all'] * 5 +
                 0.10 * max(f['trend'], 0) * 10 +  # 只奖励正趋势
                 0.10 * f['transition_prob'])
        front_features[num]['score'] = score
    
    # 后区评分
    for num in range(1, 13):
        f = back_features[num]
        score = (0.40 * f['freq_recent'] * 5 +
                 0.30 * f['omit_normalized'] +
                 0.30 * f['freq_all'] * 5)
        back_features[num]['score'] = score
    
    front_scores = {num: front_features[num]['score'] for num in range(1, 36)}
    back_scores = {num: back_features[num]['score'] for num in range(1, 13)}
    
    return front_scores, back_scores


# === 模型2: 随机森林思想（简化版决策树集成） ===
def simplified_random_forest(history, n_trees=50, window=50, seed=42):
    """简化版随机森林
    
    每棵"树"使用不同的特征子集和训练窗口，
    投票决定每个号码的出现概率
    
    Returns:
        front_scores: {num: score}, back_scores: {num: score}
    """
    front_features, back_features = compute_features(history, window)
    
    front_votes = {num: 0 for num in range(1, 36)}
    back_votes = {num: 0 for num in range(1, 13)}
    
    feature_names = ['freq_all', 'freq_recent', 'omit_normalized', 
                     'avg_interval', 'transition_prob', 'trend']
    
    random.seed(seed)

    for tree_id in range(n_trees):
        # 随机选择2-3个特征
        n_features = random.randint(2, 3)
        selected_features = random.sample(feature_names, n_features)
        
        # 随机权重
        weights = [random.uniform(0.5, 1.5) for _ in range(n_features)]
        total_w = sum(weights)
        weights = [w / total_w for w in weights]
        
        # 随机训练窗口
        train_window = random.randint(20, min(200, len(history)))
        train_data = history[-train_window:]
        train_front = [d['front'] for d in train_data]
        train_back = [d['back'] for d in train_data]
        
        # 为每个号码计算得分
        for num in range(1, 36):
            f = front_features[num]
            
            # 重新计算训练窗口内的特征
            train_count = sum(1 for fr in train_front if num in fr)
            train_freq = train_count / len(train_front)
            
            score = 0
            for i, feat in enumerate(selected_features):
                if feat == 'freq_all':
                    score += weights[i] * f['freq_all']
                elif feat == 'freq_recent':
                    score += weights[i] * f['freq_recent']
                elif feat == 'omit_normalized':
                    score += weights[i] * f['omit_normalized']
                elif feat == 'avg_interval':
                    # 间隔越小越好（反比）
                    score += weights[i] * (1.0 / max(f['avg_interval'], 1))
                elif feat == 'transition_prob':
                    score += weights[i] * f['transition_prob']
                elif feat == 'trend':
                    score += weights[i] * max(f['trend'], 0)
            
            # 如果得分高于阈值，投票
            if score > 0.15:
                front_votes[num] += 1
        
        for num in range(1, 13):
            f = back_features[num]
            train_count = sum(1 for bk in train_back if num in bk)
            train_freq = train_count / len(train_back)
            
            score = (0.4 * train_freq + 0.3 * f['omit_normalized'] + 0.3 * f['freq_all'])
            if score > 0.25:
                back_votes[num] += 1
    
    # 归一化为概率
    front_scores = {num: front_votes[num] / n_trees for num in range(1, 36)}
    back_scores = {num: back_votes[num] / n_trees for num in range(1, 13)}
    
    return front_scores, back_scores


# === 模型3: 遗传算法优化组合 (已弃用 V8.9.3) ===
# 说明: 旧 genetic_optimizer 收敛到 argmax, 在 2900+ 期频率下每期输出相同(跨期冻结),
# 与 26085/26086 主模型冻结是同类BUG。V8.9.3 起 ML 改为 generate_ml_prediction 内
# 的"按分布采样" (见 _weighted_sample_k), 该函数在 V8.9.3 移除。


# === 主函数：生成ML预测 ===
def generate_ml_prediction(history, valid_combos, target_period=None):
    """生成机器学习预测 (V8.9.3 起: 按分布采样而非argmax/收敛, 解冻跨期冻结)。

    关键修复: 旧实现用 find_best_combo(argmax) + genetic_optimizer(收敛到argmax),
    在 2900+ 期频率下每期输出几乎相同 —— 与 26085/26086 主模型冻结是同类BUG。
    现改为按 target_period 种子从各模型评分分布后验采样, 每期随期号变化且 per-period 可复现。
    """
    seed = int(target_period) if target_period else 42
    rng = random.Random(seed * 7 + 13)
    prev = history[-1]['front']
    valid_set = set(tuple(sorted(c)) for c in (valid_combos or []))

    print("  [ML] 计算加权频率模型...")
    wf_front, wf_back = weighted_frequency_model(history)
    print("  [ML] 计算随机森林模型...")
    rf_front, rf_back = simplified_random_forest(history, n_trees=50, seed=seed)

    def sample_front(dist):
        for _ in range(800):
            combo = _weighted_sample_k(dist, 5, rng, list(range(1, 36)))
            if combo in valid_set and len(set(combo) & set(prev)) <= 2:
                return list(combo)
        return None

    def sample_back(dist):
        for _ in range(400):
            combo = _weighted_sample_k(dist, 4, rng, list(range(1, 13)))
            if combo:
                return list(combo)
        return None

    def argmax_front(dist):
        return sorted(range(1, 36), key=lambda x: dist.get(x, 0), reverse=True)[:5]

    def argmax_back(dist):
        return sorted(range(1, 13), key=lambda x: dist.get(x, 0), reverse=True)[:4]

    wf_f = sample_front(wf_front) or argmax_front(wf_front)
    wf_b = sample_back(wf_back) or argmax_back(wf_back)
    rf_f = sample_front(rf_front) or argmax_front(rf_front)
    rf_b = sample_back(rf_back) or argmax_back(rf_back)
    # 遗传最优: 改为 wf+rf 混合分布采样 (同构解冻, 不再收敛到argmax)
    blend_f = {n: 0.5 * (wf_front.get(n, 0) + rf_front.get(n, 0)) for n in range(1, 36)}
    blend_b = {n: 0.5 * (wf_back.get(n, 0) + rf_back.get(n, 0)) for n in range(1, 13)}
    ga_f = sample_front(blend_f) or argmax_front(blend_f)
    ga_b = sample_back(blend_b) or argmax_back(blend_b)

    result = {
        'weighted_freq': {
            'front': sorted(wf_f), 'back': sorted(wf_b),
            'strategy': '加权频率: 近期频率40%+遗漏25%+全局15%+趋势10%+转移10% (按分布采样)'
        },
        'random_forest': {
            'front': sorted(rf_f), 'back': sorted(rf_b),
            'strategy': '简化随机森林: 50棵树, 随机特征子集投票 (按分布采样)'
        },
        'genetic_optimal': {
            'front': sorted(ga_f), 'back': sorted(ga_b),
            'strategy': 'ML集成(加权频率+随机森林)混合分布采样 (V8.9.3解冻)'
        }
    }

    print(f"  [ML] 加权频率: 前={result['weighted_freq']['front']} 后={result['weighted_freq']['back']}")
    print(f"  [ML] 随机森林: 前={result['random_forest']['front']} 后={result['random_forest']['back']}")
    print(f"  [ML] 遗传算法: 前={result['genetic_optimal']['front']} 后={result['genetic_optimal']['back']}")

    return result


if __name__ == '__main__':
    print("测试ML预测模型...")
    history = load_history()
    print(f"  加载 {len(history)} 期历史数据")
    
    # 加载有效组合
    try:
        with open('dlt_valid_combos.json', 'r') as f:
            valid_combos = json.load(f)
        print(f"  加载 {len(valid_combos)} 个有效组合")
    except:
        print("  有效组合文件不存在，使用简单方式")
        valid_combos = []
    
    result = generate_ml_prediction(history, valid_combos)
    print(f"\nML预测结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
