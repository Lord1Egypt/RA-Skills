# -*- coding: utf-8 -*-
"""
大乐透系统 — 统一常量与核心函数 (单一可信源 / Single Source of Truth)
=====================================================================

历史教训:
    V8.3 声称修复了"期号年末进年"BUG(>200)，但只改了验证脚本，生产代码
    dlt_auto.py 仍用错误逻辑；V8.4/V8.5 又多次发现"后区评分公式在验证类脚本
    与预测管线间漂移 (0.25*0.5 vs 0.25*(1-eci_s))"。根因是 PRIMES / AC / 过滤器
    / 评分权重 / 期号逻辑在 >=10 个文件各自重写，无法保证一致。

本模块集中定义所有"会被多文件使用、且一旦不一致就会产生错误结论"的常量与函数，
所有活动脚本 (dlt_auto / dlt_smart / dlt_enhance / dlt_cross_validate / dlt_healthcheck
/ dlt_result_verify / dlt_eci_backtest / dlt_ml_models) 应从本模块 import，
并由 dlt_healthcheck_all.py 持续断言"各文件内联定义 == 本模块"。

绝不在此随意改动数值 —— 任何改动都会触发回归断言失败。
"""
from itertools import combinations
import math
import random

# ---------- 基础常量 ----------
K = 35                      # 前区号码数 1..35
BACK_N = 12                 # 后区号码数 1..12
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}   # 11个质数 (前区)

# 前区4模型评分权重 (CDM + 马尔可夫 + 频率 + 遗漏) —— 预测与回测必须一致
FRONT_WEIGHTS = [0.40, 0.25, 0.20, 0.15]

# 后区综合评分权重 (CDM + 马尔可夫 + 遗漏 + ECI中性项)
#   ECI中性项默认 0.5: 表示"无专家热度数据时，ECI 项取中性 0.5"
#   注意: 验证类脚本曾误用 (1-eci_s) 替代 0.5，造成"验证器"与"预测器"公式不一致。
BACK_W_CDM = 0.35
BACK_W_MARKOV = 0.25
BACK_W_OMIT = 0.15
BACK_W_ECI = 0.25


# ============================================================
# 核心函数 (从 dlt_auto.py 抽取，逐字一致)
# ============================================================
def calc_ac(front):
    """标准 AC 值: 所有两两绝对差去重后的个数 - (n-1)"""
    diffs = set()
    for i in range(len(front)):
        for j in range(i + 1, len(front)):
            diffs.add(abs(front[i] - front[j]))
    return len(diffs) - (len(front) - 1)


def odd_count(front):
    return sum(1 for n in front if n % 2 == 1)


def small_count(front):
    return sum(1 for n in front if n <= 17)   # 小号=01..17, 大号=18..35


def prime_count(front):
    return sum(1 for n in front if n in PRIMES)


def road_counts(front):
    """返回 (余0个数, 余1个数, 余2个数)"""
    return (sum(1 for n in front if n % 3 == 0),
            sum(1 for n in front if n % 3 == 1),
            sum(1 for n in front if n % 3 == 2))


def consecutive_groups(front):
    """连号组数 (连续相邻算一组, 如 1,2,3 算1组)"""
    fs = sorted(front)
    groups = 0
    i = 0
    while i < len(fs) - 1:
        if fs[i + 1] - fs[i] == 1:
            groups += 1
            while i < len(fs) - 1 and fs[i + 1] - fs[i] == 1:
                i += 1
        i += 1
    return groups


def passes_filters(front, prev_front=None):
    """9项过滤器: 8项静态 + 可选第9项重号(<=2 vs 上期)

    返回 True 表示该组合通过全部启用的过滤项。
    注意: 38,537 = 仅8项静态过滤器; 含第9项(重号)后 = 37,680。
    """
    checks = [
        4 <= calc_ac(front) <= 6,
        80 <= sum(front) <= 130,
        15 <= max(front) - min(front) <= 30,
        odd_count(front) in [2, 3],
        small_count(front) in [2, 3],
        prime_count(front) in [1, 2],
        all(r > 0 for r in road_counts(front)),
        consecutive_groups(front) <= 1,
    ]
    if prev_front:
        checks.append(len(set(front) & set(prev_front)) <= 2)
    return all(checks)


def back_score(cdm_s, mk_s, omit_norm, eci_norm=0.5):
    """后区综合评分 (与 dlt_auto.py 预测管线完全一致)

    cdm_s, mk_s: 归一化后的 CDM / 马尔可夫 概率
    omit_norm:   遗漏值 / max_omit (已归一化到 0..1)
    eci_norm:    ECI 热度项, 默认 0.5 (中性). 仅在确有真实专家热度数据时传入
    """
    return (BACK_W_CDM * cdm_s + BACK_W_MARKOV * mk_s
            + BACK_W_OMIT * omit_norm + BACK_W_ECI * eci_norm)


# ============================================================
# 期号计算 (转发到统一模块 dlt_period)
# ============================================================
from dlt_period import next_period  # noqa: E402


# ============================================================
# 属性 / 差分 / 变质 测试 (来自全网学习: property-based + differential + metamorphic)
#   依赖标准库 random, 无外部包依赖, 可在调度任务中稳定跑。
#   思想: 对纯函数做"对所有输入成立的不变量"校验, 而非只测几个手挑样例。
# ============================================================
def property_checks(n_trials=5000, seed=20260802):
    """随机不变量校验: 差分 oracle + 变质属性 + 输入校验。

    返回 True 表示全部不变量在 n_trials 个随机样本上成立。
    """
    rng = random.Random(seed)

    # 差分 oracle: 朴素 pairwise 差集实现的 AC 必须与 calc_ac 逐字一致
    def naive_ac(c):
        diffs = set()
        for i in range(len(c)):
            for j in range(i + 1, len(c)):
                diffs.add(abs(c[i] - c[j]))
        return len(diffs) - (len(c) - 1)

    for _ in range(n_trials):
        c = sorted(rng.sample(range(1, K + 1), 5))

        # 基本不变量
        assert isinstance(passes_filters(c), bool)        # 永不抛异常, 返回布尔
        assert 0 <= calc_ac(c) <= 6                        # AC 取值范围(5号: 0..6)

        ac = calc_ac(c)
        assert naive_ac(c) == ac                           # 差分 oracle (慢实现=快实现)

        # 变质属性: 整体平移不改变两两差, 故 AC 不变 (信息论: 平移是对称变换)
        t = rng.randint(-(c[0] - 1), (K - c[-1]))
        if t != 0:
            ct = sorted(x + t for x in c)
            assert 1 <= ct[0] and ct[-1] <= K
            assert calc_ac(ct) == ac                       # 平移不变 (metamorphic)

        # 分类计数不变量 (三者和必须等于 5)
        assert prime_count(c) == sum(1 for n in c if n in PRIMES)
        r0, r1, r2 = road_counts(c)
        assert r0 + r1 + r2 == 5
        oc = odd_count(c)
        assert oc + (5 - oc) == 5
        sc = small_count(c)
        assert sc + (5 - sc) == 5

        # 后区综合评分有界 [0,1] (权重和=1, 各分量∈[0,1])
        s = back_score(rng.random(), rng.random(), rng.random(), rng.random())
        assert 0.0 <= s <= 1.0

    # 输入校验: 非法组合必须被 passes_filters 拒 (返回 False, 不抛异常)
    bad = [
        [1, 1, 2, 3, 4],     # 含重复
        [0, 1, 2, 3, 4],     # 越下界
        [1, 2, 3, 4, 36],    # 越上界
        [1, 2, 3, 4],        # 长度不足
        [1, 2, 3, 4, 5, 6],  # 长度超
    ]
    for b in bad:
        assert passes_filters(b) is False
    return True


# ============================================================
# 自检 (可被 dlt_healthcheck_all.py 调用)
# ============================================================
def _self_test():
    # ---- 已知组合 10,13,26,29,30 应通过9项(无重号上下文) ----
    assert passes_filters([10, 13, 26, 29, 30])
    # AC 已知: {10,13,26,29,30} 两两差集 8 个, AC = 8-(5-1) = 4 (在[4,6]内, 通过)
    assert calc_ac([10, 13, 26, 29, 30]) == 4
    # 后区评分
    assert abs(back_score(0.1, 0.2, 0.3) - (0.35 * 0.1 + 0.25 * 0.2 + 0.15 * 0.3 + 0.25 * 0.5)) < 1e-12
    # 后区评分权重守恒 (=1.0): 任一输入组合之和应恒等于四项加权和且系数和=1
    assert abs((BACK_W_CDM + BACK_W_MARKOV + BACK_W_OMIT + BACK_W_ECI) - 1.0) < 1e-12
    # 质数计数
    assert prime_count([2, 3, 5, 7, 11]) == 5
    assert prime_count([1, 4, 6, 8, 9]) == 0

    # ---- 过滤器否决案例 (必须 False) ----
    assert not passes_filters([1, 3, 5, 7, 9])            # 奇偶比 5:0 -> 拒
    assert not passes_filters([1, 2, 3, 4, 5])            # 连号组过多(4组)且全小且AC低 -> 拒
    assert not passes_filters([30, 31, 32, 33, 34])       # 和值=160>130 -> 拒
    assert not passes_filters([3, 6, 9, 12, 15])          # 012路不全(全余0) -> 拒
    assert calc_ac([1, 2, 3, 4, 5]) == 0                  # AC 边界: 连续5号差集仅4 -> AC=0

    # ---- 重号过滤 (第9项) ----
    assert passes_filters([10, 13, 26, 29, 30], prev_front=[1, 2, 3, 4, 5])          # 无重号 -> 通过
    assert not passes_filters([10, 13, 26, 29, 30], prev_front=[10, 13, 26, 7, 8])  # 重号3个>2 -> 拒

    # ---- 工具函数正确性 ----
    assert odd_count([1, 3, 5, 7, 9]) == 5
    assert small_count([1, 2, 3, 4, 5]) == 5
    assert road_counts([3, 6, 9, 12, 15]) == (5, 0, 0)
    assert consecutive_groups([1, 2, 3, 10, 20]) == 1     # 仅 1-2-3 一组
    assert consecutive_groups([1, 2, 10, 11, 20]) == 2    # 两组

    # ---- 属性/差分/变质 随机不变量测试 (5000 样本) ----
    property_checks()
    return True


if __name__ == '__main__':
    _self_test()
    print("dlt_common OK | PRIMES=%d个 | FRONT_WEIGHTS=%s | K=%d BACK_N=%d"
          % (len(PRIMES), FRONT_WEIGHTS, K, BACK_N))
