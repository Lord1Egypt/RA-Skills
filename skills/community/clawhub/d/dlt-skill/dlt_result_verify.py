# -*- coding: utf-8 -*-
"""
大乐透预测验证 + 性能追踪模块

功能:
1. 自动验证上期预测 vs 实际开奖结果
2. 计算命中数、判断中奖等级
3. 维护历史性能追踪文件 dlt_performance.json
4. 生成性能统计报告

中奖等级规则（大乐透 2026新规, 第26014期/2026-01-31 起, 9档→7档）:
  一等奖: 5+2 (浮动, 最高1000万)
  二等奖: 5+1 (浮动, 最高500万)
  三等奖: 5+0 或 4+2 (奖池≥8亿 6666元; <8亿 5000元)
  四等奖: 4+1 (≥8亿 380元; <8亿 300元)
  五等奖: 3+2 或 4+0 (≥8亿 200元; <8亿 150元)
  六等奖: 3+1 或 2+2 (≥8亿 18元; <8亿 15元)
  七等奖: 3+0, 2+1, 1+2, 0+2 (≥8亿 7元; <8亿 5元)
  未中奖: 其他 (注: 旧规的1+1/0+1等现已不中奖)
"""
import json
import os
from datetime import datetime

PERFORMANCE_FILE = 'dlt_performance.json'


def load_performance():
    """加载性能追踪数据"""
    if os.path.exists(PERFORMANCE_FILE):
        try:
            with open(PERFORMANCE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'records': [], 'stats': {'total_verified': 0, 'avg_front_hits': 0, 'avg_total_hits': 0}}


def save_performance(data):
    """保存性能追踪数据"""
    with open(PERFORMANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_prediction_for_period(period):
    """找到对应期号的预测文件
    
    Args:
        period: 开奖期号 (字符串或整数)
    
    Returns:
        (filepath, version) or (None, None)
    """
    period_str = str(period)
    candidates = [
        f'dlt_prediction_{period_str}_v8.json',
        f'dlt_prediction_{period_str}.json',
    ]
    for c in candidates:
        if os.path.exists(c):
            return c, 'v8' if '_v8' in c else 'v1'
    return None, None


def determine_prize_level(front_hits, back_hits):
    """判断中奖等级 (2026新规, 第26014期起9档→7档)

    **单一权威源**: 本函数不再手写 if/elif 判定, 一律委托
    `dlt_draw_check.prize_of()` —— 奖级/奖金的唯一真相来自
    `dlt_power_engine.PRIZE_PAYOUT`。任何奖金/奖级变更只需改一处
    (PRIZE_PAYOUT), 全系统自动一致, 杜绝"两写漂移"导致 2+1 等
    组合被误判的历史 bug。

    Args:
        front_hits: 前区命中数 (0-5)
        back_hits: 后区命中数 (0-2)

    Returns:
        (等级名称, 预计奖金) — 奖金按当前奖池≥8亿档(实际8.07亿)
    """
    try:
        from dlt_draw_check import prize_of
        name, pay = prize_of(front_hits, back_hits)
    except Exception:
        # 极端故障兜底: 与权威表行为一致(未命中=未中奖), 绝不臆造奖级
        name, pay = ('未中奖', 0)
    if pay == 0:
        money = '0元'
    else:
        money = f'{pay}元(奖池≥8亿)'
    return name, money


def verify_prediction(pred_file, actual_front, actual_back):
    """验证预测 vs 实际开奖
    
    Args:
        pred_file: 预测JSON文件路径
        actual_front: 实际前区开奖 [5个数字]
        actual_back: 实际后区开奖 [2个数字]
    
    Returns:
        list: 每组验证结果
    """
    with open(pred_file, 'r', encoding='utf-8') as f:
        pred = json.load(f)
    
    results = []
    actual_front_set = set(actual_front)
    actual_back_set = set(actual_back)
    
    # 验证每组推荐
    groups = pred.get('groups', [])
    for i, group in enumerate(groups):
        pred_front = set(group.get('front', []))
        pred_back = set(group.get('back', []))
        
        front_hits = len(pred_front & actual_front_set)
        back_hits = len(pred_back & actual_back_set)
        
        # 后区是4选2，计算命中最多的2个
        # 实际投注时从4个后区中选2个，所以最多命中2个
        prize, prize_money = determine_prize_level(front_hits, min(back_hits, 2))
        
        results.append({
            'group': i + 1,
            'name': group.get('name', f'第{i+1}组'),
            'strategy': group.get('strategy', ''),
            'pred_front': sorted(list(pred_front)),
            'pred_back': sorted(list(pred_back)),
            'front_hits': front_hits,
            'back_hits': min(back_hits, 2),
            'back_hits_raw': back_hits,
            'total_hits': front_hits + min(back_hits, 2),
            'prize': prize,
            'prize_money': prize_money,
        })
    
    # 验证胆拖方案
    dantuo = pred.get('dantuo', {})
    if dantuo:
        dan = set(dantuo.get('dan', []))
        tuo = set(dantuo.get('tuo', []))
        dt_back = set(dantuo.get('back', []))
        
        dan_hits = len(dan & actual_front_set)
        tuo_hits = len(tuo & actual_front_set)
        dt_back_hits = len(dt_back & actual_back_set)
        
        # 胆拖的最佳情况：胆全中+拖中剩余+后区全中
        best_front = dan_hits + min(tuo_hits, 5 - len(dan))
        best_back = min(dt_back_hits, 2)
        best_prize, best_money = determine_prize_level(best_front, best_back)
        
        results.append({
            'group': '胆拖',
            'name': dantuo.get('name', '标准胆拖'),
            'dan': sorted(list(dan)),
            'tuo': sorted(list(tuo)),
            'back': sorted(list(dt_back)),
            'dan_hits': dan_hits,
            'tuo_hits': tuo_hits,
            'front_hits': best_front,
            'back_hits': best_back,
            'total_hits': best_front + best_back,
            'prize': best_prize,
            'prize_money': best_money,
        })
    
    return results


def update_performance(period, actual_front, actual_back, verification_results):
    """更新性能追踪文件
    
    Args:
        period: 期号
        actual_front: 实际前区
        actual_back: 实际后区
        verification_results: 验证结果列表
    
    Returns:
        dict: 更新后的性能数据
    """
    perf = load_performance()
    
    # 检查是否已存在该期记录
    existing_idx = None
    for i, r in enumerate(perf['records']):
        if str(r.get('period')) == str(period):
            existing_idx = i
            break
    
    record = {
        'period': str(period),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'actual_front': sorted(actual_front),
        'actual_back': sorted(actual_back),
        'results': verification_results,
    }
    
    if existing_idx is not None:
        perf['records'][existing_idx] = record
        print(f"  更新已有记录: 期号{period}")
    else:
        perf['records'].append(record)
        print(f"  新增验证记录: 期号{period}")
    
    # 重新计算统计
    all_front_hits = []
    all_total_hits = []
    all_back_hits = []
    prize_distribution = {}
    best_results = []
    
    for rec in perf['records']:
        for r in rec.get('results', []):
            if isinstance(r.get('group'), int):
                all_front_hits.append(r['front_hits'])
                all_total_hits.append(r['total_hits'])
                all_back_hits.append(r['back_hits'])
                prize = r.get('prize', '未中奖')
                prize_distribution[prize] = prize_distribution.get(prize, 0) + 1
                best_results.append(r)
    
    perf['stats'] = {
        'total_verified': len(perf['records']),
        'total_predictions': len(all_front_hits),
        'avg_front_hits': round(sum(all_front_hits) / len(all_front_hits), 3) if all_front_hits else 0,
        'avg_back_hits': round(sum(all_back_hits) / len(all_back_hits), 3) if all_back_hits else 0,
        'avg_total_hits': round(sum(all_total_hits) / len(all_total_hits), 3) if all_total_hits else 0,
        'max_front_hits': max(all_front_hits) if all_front_hits else 0,
        'max_total_hits': max(all_total_hits) if all_total_hits else 0,
        'prize_distribution': prize_distribution,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    
    save_performance(perf)
    return perf


def check_and_verify(draws):
    """检查是否有待验证的预测并自动验证
    
    在每次预测运行前调用：
    1. 读取最新实际开奖数据
    2. 查找对应期号的预测文件
    3. 验证并更新性能追踪
    
    Args:
        draws: 全部历史开奖数据 (已排序)
    
    Returns:
        dict or None: 验证结果，None表示无需验证
    """
    if not draws or len(draws) < 2:
        return None
    
    perf = load_performance()
    verified_periods = {str(r.get('period')) for r in perf.get('records', [])}
    
    # 检查最近5期中是否有未验证的预测
    saw_unverified = False
    missing_file = False
    for i in range(len(draws) - 1, max(len(draws) - 6, -1), -1):
        period = str(draws[i]['period'])
        if period in verified_periods:
            continue

        saw_unverified = True
        pred_file, version = find_prediction_for_period(period)
        if pred_file:
            print(f"\n  发现待验证预测: {pred_file}")
            print(f"  实际开奖 {period}: 前区={draws[i]['front']} 后区={draws[i]['back']}")

            results = verify_prediction(pred_file, draws[i]['front'], draws[i]['back'])

            print(f"\n  验证结果:")
            for r in results:
                prize_str = f" → {r['prize']}({r['prize_money']})" if r['prize'] != '未中奖' else ''
                if isinstance(r.get('group'), int):
                    print(f"    第{r['group']}组({r['name']}): "
                          f"前区{r['front_hits']}/5, 后区{r['back_hits']}/2, "
                          f"共{r['total_hits']}球{prize_str}")
                else:
                    print(f"    {r['group']}({r['name']}): "
                          f"前区{r['front_hits']}/5, 后区{r['back_hits']}/2, "
                          f"共{r['total_hits']}球{prize_str} "
                          f"[胆中{r.get('dan_hits',0)}, 拖中{r.get('tuo_hits',0)}]")

            perf = update_performance(period, draws[i]['front'], draws[i]['back'], results)
            return {'period': period, 'results': results, 'perf': perf}
        else:
            missing_file = True

    # 最近5期无待验证预测: 区分"已全部验证"与"有上期但预测文件未留存"
    if saw_unverified and missing_file:
        return {'skipped': True, 'reason': 'no_prediction_files'}
    return {'skipped': True, 'reason': 'all_verified'}


def print_performance_summary():
    """打印性能追踪摘要"""
    perf = load_performance()
    stats = perf.get('stats', {})
    
    print("\n" + "=" * 70)
    print("【性能追踪摘要】")
    print("=" * 70)
    
    if stats.get('total_verified', 0) == 0:
        print("  尚无验证记录。首次运行后将开始追踪。")
        return
    
    print(f"  已验证期数: {stats.get('total_verified', 0)}")
    print(f"  总预测组数: {stats.get('total_predictions', 0)}")
    print(f"  平均前区命中: {stats.get('avg_front_hits', 0):.2f}/5")
    print(f"  平均后区命中: {stats.get('avg_back_hits', 0):.2f}/2")
    print(f"  平均总命中: {stats.get('avg_total_hits', 0):.2f}/7")
    print(f"  最高前区命中: {stats.get('max_front_hits', 0)}/5")
    print(f"  最高总命中: {stats.get('max_total_hits', 0)}/7")
    
    prize_dist = stats.get('prize_distribution', {})
    if prize_dist:
        print(f"\n  中奖分布:")
        for prize, count in sorted(prize_dist.items(), key=lambda x: -x[1]):
            print(f"    {prize}: {count}次")
    
    # 最近5期详情
    records = perf.get('records', [])
    if records:
        print(f"\n  最近验证记录:")
        for rec in records[-3:]:
            period = rec['period']
            actual = f"前{rec['actual_front']} 后{rec['actual_back']}"
            best = max(rec['results'], key=lambda x: x.get('total_hits', 0))
            print(f"    {period}: {actual} → 最佳: {best['name']} "
                  f"命中{best['total_hits']}球 ({best['prize']})")


if __name__ == '__main__':
    # 独立运行：加载历史数据并检查待验证预测
    print("大乐透预测验证模块")
    print("=" * 70)
    
    try:
        with open('dlt_history.json', 'r', encoding='utf-8') as f:
            draws = json.load(f)
        print(f"  已加载 {len(draws)} 期历史数据")
        print(f"  最新期号: {draws[-1]['period']}")
        
        result = check_and_verify(draws)
        if result is None:
            print("\n  开奖数据不足, 无法验证。")
        elif result.get('skipped'):
            print(f"\n  无待验证预测 ({result.get('reason')})。")
        
        print_performance_summary()
        
    except FileNotFoundError:
        print("  dlt_history.json 不存在，请先运行 dlt_auto.py")
