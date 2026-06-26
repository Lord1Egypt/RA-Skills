# 福彩3D Python算法完整代码

> 完整可运行的Python代码，复制即可使用。涵盖：数据获取、频率分析、遗漏分析、和值跨度、012路分析、组选分析、蒙特卡洛模拟、可视化图表。

---

## 1. 环境准备

```bash
pip install requests pandas plotly kaleido
```

---

## 2. 数据获取

### 2.1 爬取历史开奖数据

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_fc3d_history(periods=200):
    """
    从500彩票网获取福彩3D历史开奖数据
    periods: 获取期数，默认200期
    """
    url = "https://datachart.500.com/ssq/history/newinc/history.php"
    params = {"start": None, "end": None}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://datachart.500.com/fc3d/"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.encoding = 'gbk'
        text = response.text
        
        # 解析HTML提取数据
        import re
        # 找到所有开奖记录
        pattern = r'<tr class="t_tr1">(.*?)</tr>'
        matches = re.findall(pattern, text, re.DOTALL)
        
        records = []
        for match in matches[:periods]:
            # 提取期号和开奖号码
            num_pattern = r'<td>(\d+)</td>\s*<td>(\d)</td>\s*<td>(\d)</td>\s*<td>(\d)</td>'
            nums = re.search(num_pattern, match)
            if nums:
                period = nums.group(1)
                b, s, g = nums.group(2), nums.group(3), nums.group(4)
                records.append({
                    'period': period,
                    'bai': int(b),
                    'shi': int(s),
                    'ge': int(g),
                    'number': f"{b}{s}{g}"
                })
        
        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['period'].str[:8], format='%Y%m%d', errors='coerce')
        return df
        
    except Exception as e:
        print(f"数据获取失败: {e}")
        return None

# 测试
df = fetch_fc3d_history(200)
print(df.head(10))
```

### 2.2 备选：手动录入数据

```python
def load_from_csv(filepath):
    """从CSV文件加载数据"""
    df = pd.read_csv(filepath)
    df.columns = ['period', 'bai', 'shi', 'ge', 'number']
    return df

# 示例CSV格式:
# period,bai,shi,ge,number
# 2024128001,5,2,8,528
# 2024127999,3,1,7,317
```

---

## 3. 频率热力分析

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def frequency_analysis(df):
    """频率热力分析 - 统计各位置0-9出现次数"""
    
    positions = ['bai', 'shi', 'ge']
    position_names = {'bai': '百位', 'shi': '十位', 'ge': '个位'}
    
    fig = make_subplots(rows=1, cols=3, 
                       subplot_titles=['百位频率', '十位频率', '个位频率'],
                       horizontal_spacing=0.08)
    
    for i, pos in enumerate(positions):
        freq = df[pos].value_counts().sort_index()
        all_digits = pd.Series([freq.get(d, 0) for d in range(10)], index=range(10))
        
        colors = []
        avg = all_digits.mean()
        for v in all_digits:
            if v > avg * 1.2:
                colors.append('#e74c3c')  # 热号 - 红
            elif v < avg * 0.8:
                colors.append('#3498db')  # 冷号 - 蓝
            else:
                colors.append('#95a5a6')  # 温号 - 灰
        
        fig.add_trace(
            go.Bar(x=list(range(10)), y=all_digits.values, 
                   marker_color=colors, name=position_names[pos],
                   text=all_digits.values, textposition='outside'),
            row=1, col=i+1
        )
        # 添加平均线
        fig.add_hline(y=avg, line_dash="dash", line_color="green",
                     annotation_text=f"均值:{avg:.1f}", row=1, col=i+1)
    
    fig.update_layout(
        title="📊 福彩3D频率热力分析（近200期）",
        showlegend=False,
        height=400
    )
    
    return fig

# 调用
fig = frequency_analysis(df)
fig.show()
fig.write_html("fc3d_frequency.html")
```

---

## 4. 遗漏值分析

```python
def missing_analysis(df):
    """遗漏值分析 - 统计每个数字当前遗漏期数和历史平均遗漏"""
    
    positions = ['bai', 'shi', 'ge']
    results = {}
    
    for pos in positions:
        latest = df[pos].iloc[0]  # 最新一期
        position_history = df[pos].tolist()
        
        missing_info = {}
        for digit in range(10):
            # 当前遗漏
            current_missing = 0
            for i, val in enumerate(position_history):
                if val == digit:
                    break
                current_missing += 1
            
            # 历史平均遗漏（理论值=10）
            avg_missing = 10
            
            # 历史最大遗漏
            max_missing = 0
            current_streak = 0
            for val in position_history:
                if val == digit:
                    max_missing = max(max_missing, current_streak)
                    current_streak = 0
                else:
                    current_streak += 1
            max_missing = max(max_missing, current_streak)
            
            missing_info[digit] = {
                'current': current_missing,
                'avg': avg_missing,
                'max': max_missing,
                'status': '🔥热' if current_missing < 3 else ('🧊冷' if current_missing > 15 else '🌡温')
            }
        
        results[pos] = missing_info
    
    # 打印分析结果
    print("=" * 60)
    print("遗漏值分析报告")
    print("=" * 60)
    
    for pos in positions:
        print(f"\n【{pos.upper()}位】")
        print(f"{'数字':<6}{'当前遗漏':<10}{'历史最大':<10}{'状态':<8}")
        print("-" * 40)
        for digit, info in sorted(results[pos].items()):
            print(f"  {digit}    {info['current']:<10}{info['max']:<10}{info['status']}")
    
    return results

# 调用
missing_data = missing_analysis(df)
```

---

## 5. 和值与跨度分析

```python
def sum_range_analysis(df):
    """和值分析 - 统计3位数之和的分布"""
    
    df = df.copy()
    df['sum'] = df['bai'] + df['shi'] + df['ge']
    df['span'] = df[['bai', 'shi', 'ge']].max(axis=1) - df[['bai', 'shi', 'ge']].min(axis=1)
    
    # 和值分布
    sum_counts = df['sum'].value_counts().sort_index()
    all_sums = pd.Series([sum_counts.get(s, 0) for s in range(28)], index=range(28))
    
    # 跨度分布
    span_counts = df['span'].value_counts().sort_index()
    all_spans = pd.Series([span_counts.get(s, 0) for s in range(10)], index=range(10))
    
    # 高频和值推荐（历史Top5）
    top_sums = sum_counts.head(5)
    print("📈 高频和值 TOP5:")
    for s, c in top_sums.items():
        pct = c / len(df) * 100
        print(f"   和值 {s:2d}: {c:3d}次 ({pct:.1f}%)")
    
    # 跨度分析
    print("\n📉 跨度分布:")
    for sp, c in span_counts.items():
        pct = c / len(df) * 100
        bar = "█" * int(pct)
        print(f"   跨度 {sp}: {bar} {c}次 ({pct:.1f}%)")
    
    return df

# 调用
df_analyzed = sum_range_analysis(df)
```

---

## 6. 012路分析

```python
def road_analysis(df):
    """012路分析 - 除3余数分析"""
    
    df = df.copy()
    df['bai_road'] = df['bai'] % 3
    df['shi_road'] = df['shi'] % 3
    df['ge_road'] = df['ge'] % 3
    
    # 012路组合统计
    df['road_combo'] = df['bai_road'].astype(str) + df['shi_road'].astype(str) + df['ge_road'].astype(str)
    combo_counts = df['road_combo'].value_counts().head(10)
    
    print("🔢 012路组合分布（Top10）:")
    for combo, count in combo_counts.items():
        pct = count / len(df) * 100
        print(f"   [{combo[0]}-{combo[1]}-{combo[2]}] {count:3d}次 ({pct:.1f}%)")
    
    # 各路出现频率
    print("\n📊 各路出现频率:")
    for pos in ['bai_road', 'shi_road', 'ge_road']:
        pos_name = pos.split('_')[0].upper()
        counts = df[pos].value_counts().sort_index()
        total = len(df)
        print(f"   {pos_name}位: 0路={counts.get(0,0)}({counts.get(0,0)/total*100:.1f}%) "
              f"1路={counts.get(1,0)}({counts.get(1,0)/total*100:.1f}%) "
              f"2路={counts.get(2,0)}({counts.get(2,0)/total*100:.1f}%)")
    
    return df

# 调用
df_with_road = road_analysis(df)
```

---

## 7. 组选类型分析

```python
def group_type_analysis(df):
    """组选类型分析 - 判断直选/组三/组六"""
    
    def classify_number(row):
        digits = sorted([row['bai'], row['shi'], row['ge']])
        if digits[0] == digits[1] == digits[2]:
            return '豹子'  # 三同号
        elif digits[0] == digits[1] or digits[1] == digits[2]:
            return '组三'  # 两个相同
        else:
            return '组六'  # 三个不同
    
    df = df.copy()
    df['type'] = df.apply(classify_number, axis=1)
    
    type_counts = df['type'].value_counts()
    total = len(df)
    
    print("🎯 组选类型分布（近{}期）:".format(total))
    for t, c in type_counts.items():
        pct = c / total * 100
        expected = {'豹子': 10, '组三': 270, '组六': 720}
        exp_pct = expected.get(t, 0) / 1000 * 100
        deviation = pct - exp_pct
        symbol = "↑" if deviation > 0 else "↓"
        print(f"   {t}: {c:3d}次 ({pct:.1f}%) | 理论值:{exp_pct:.1f}% {symbol}{abs(deviation):.1f}%")
    
    return df

# 调用
df_typed = group_type_analysis(df)
```

---

## 8. 蒙特卡洛模拟筛选

```python
import random
from itertools import combinations

def monte_carlo_filter(df, iterations=50000, filters=None):
    """
    蒙特卡洛模拟 + 多重过滤
    模拟大量随机号码，根据历史规律过滤出高质量候选
    """
    
    if filters is None:
        filters = {
            'sum_range': (6, 22),        # 和值范围
            'span_range': (2, 8),        # 跨度范围
            'avoid_same_parity': True,   # 避免全奇全偶
            'road_balance': True,        # 012路均衡
            'max_consecutive': 2         # 最大连续号数
        }
    
    # 统计历史规律
    df['sum'] = df['bai'] + df['shi'] + df['ge']
    df['span'] = df[['bai', 'shi', 'ge']].max(axis=1) - df[['bai', 'shi', 'ge']].min(axis=1)
    
    sum_avg = df['sum'].mean()
    span_avg = df['span'].mean()
    
    # 过滤函数
    def passes_filter(nums):
        nums = [int(n) for n in nums]
        
        # 和值过滤
        s = sum(nums)
        if not (filters['sum_range'][0] <= s <= filters['sum_range'][1]):
            return False
        
        # 跨度过滤
        sp = max(nums) - min(nums)
        if not (filters['span_range'][0] <= sp <= filters['span_range'][1]):
            return False
        
        # 奇偶过滤
        if filters['avoid_same_parity']:
            odds = sum(1 for n in nums if n % 2 == 1)
            if odds == 0 or odds == 3:
                return False
        
        # 012路均衡
        if filters['road_balance']:
            roads = [n % 3 for n in nums]
            road_set = set(roads)
            if len(road_set) == 1:  # 全同路
                return False
        
        # 连续号过滤
        sorted_nums = sorted(nums)
        consecutive = 1
        for i in range(len(sorted_nums) - 1):
            if sorted_nums[i+1] - sorted_nums[i] == 1:
                consecutive += 1
                if consecutive > filters['max_consecutive']:
                    return False
            else:
                consecutive = 1
        
        return True
    
    # 蒙特卡洛模拟
    candidates = set()
    generated = 0
    
    while len(candidates) < iterations and generated < iterations * 3:
        generated += 1
        nums = [random.randint(0, 9) for _ in range(3)]
        if passes_filter(nums):
            candidates.add(tuple(nums))
    
    print(f"✅ 蒙特卡洛筛选完成: 模拟{generated}次 → {len(candidates)}注候选")
    
    # 按和值分布展示候选
    from collections import Counter
    sum_dist = Counter(sum(c) for c in candidates)
    
    print("\n📊 候选号码和值分布:")
    for s in sorted(sum_dist.keys()):
        cnt = sum_dist[s]
        bar = "●" * int(cnt / max(sum_dist.values()) * 20)
        print(f"   和值{s:2d}: {bar} {cnt}注")
    
    return list(candidates)

# 调用
candidates = monte_carlo_filter(df, iterations=50000)
print(f"\n🎰 共筛选出 {len(candidates)} 注候选号码")
```

---

## 9. 综合选号推荐

```python
def generate_recommendation(df, num_recommendations=5):
    """
    综合多维度分析，生成最终选号推荐
    """
    
    print("=" * 60)
    print("🎯 福彩3D综合选号推荐")
    print("=" * 60)
    
    # 1. 获取各位置热号
    def get_hot_digits(pos, top_n=4):
        counts = df[pos].value_counts()
        return list(counts.head(top_n).index)
    
    hot_bai = get_hot_digits('bai')
    hot_shi = get_hot_digits('shi')
    hot_ge = get_hot_digits('ge')
    
    print(f"\n🔥 各位置热号: 百{hot_bai} 十{hot_shi} 个{hot_ge}")
    
    # 2. 获取冷号（待回补）
    def get_cold_digits(pos, bottom_n=2):
        counts = df[pos].value_counts()
        return list(counts.tail(bottom_n).index)
    
    cold_bai = get_cold_digits('bai')
    cold_shi = get_cold_digits('shi')
    cold_ge = get_cold_digits('ge')
    
    print(f"🧊 各位置冷号: 百{cold_bai} 十{cold_shi} 个{cold_ge}")
    
    # 3. 生成推荐组合
    recommendations = []
    
    # 策略A: 追热号（稳健型）
    print("\n📌 策略A - 追热号（稳健型）:")
    for i in range(num_recommendations):
        rec = (
            random.choice(hot_bai),
            random.choice(hot_shi),
            random.choice(hot_ge)
        )
        recommendations.append(('A', rec))
        print(f"   {i+1}. {rec[0]}{rec[1]}{rec[2]}")
    
    # 策略B: 冷热搭配
    print("\n📌 策略B - 冷热搭配:")
    for i in range(num_recommendations):
        rec = (
            random.choice(hot_bai + cold_bai),
            random.choice(hot_shi + cold_shi),
            random.choice(hot_ge + cold_ge)
        )
        recommendations.append(('B', rec))
        print(f"   {i+1}. {rec[0]}{rec[1]}{rec[2]}")
    
    # 策略C: 全奇偶均衡
    print("\n📌 策略C - 奇偶均衡:")
    for i in range(num_recommendations):
        rec = (
            random.choice([d for d in range(10) if d % 2 == 0] + [d for d in range(10) if d % 2 == 1]),
            random.choice([d for d in range(10) if d % 2 == 0] + [d for d in range(10) if d % 2 == 1]),
            random.choice([d for d in range(10) if d % 2 == 0] + [d for d in range(10) if d % 2 == 1])
        )
        recommendations.append(('C', rec))
        print(f"   {i+1}. {rec[0]}{rec[1]}{rec[2]}")
    
    return recommendations

# 调用
recs = generate_recommendation(df)
```

---

## 10. 完整报告生成

```python
def generate_full_report(df, output_path="fc3d_report.html"):
    """生成完整的可视化分析报告"""
    
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    df = df.copy()
    df['sum'] = df['bai'] + df['shi'] + df['ge']
    df['span'] = df[['bai', 'shi', 'ge']].max(axis=1) - df[['bai', 'shi', 'ge']].min(axis=1)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('百位走势', '十位走势', '和值分布', '跨度分布'),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "histogram"}, {"type": "histogram"}]]
    )
    
    # 百位走势
    fig.add_trace(
        go.Scatter(x=list(range(len(df))), y=df['bai'], 
                   mode='lines+markers', name='百位', line=dict(color='#e74c3c')),
        row=1, col=1
    )
    
    # 十位走势
    fig.add_trace(
        go.Scatter(x=list(range(len(df))), y=df['shi'],
                   mode='lines+markers', name='十位', line=dict(color='#3498db')),
        row=1, col=1
    )
    
    # 个位走势
    fig.add_trace(
        go.Scatter(x=list(range(len(df))), y=df['ge'],
                   mode='lines+markers', name='个位', line=dict(color='#2ecc71')),
        row=1, col=1
    )
    
    # 和值分布
    fig.add_trace(
        go.Histogram(x=df['sum'], name='和值', marker_color='#9b59b6'),
        row=2, col=1
    )
    
    # 跨度分布
    fig.add_trace(
        go.Histogram(x=df['span'], name='跨度', marker_color='#f39c12'),
        row=2, col=2
    )
    
    fig.update_layout(
        title="📊 福彩3D综合数据分析报告",
        height=700,
        showlegend=True
    )
    
    fig.write_html(output_path)
    print(f"✅ 报告已生成: {output_path}")

# 调用
generate_full_report(df)
```

---

> 💡 **使用建议**：将以上代码保存为 `fc3d_analysis.py`，安装依赖后直接运行即可生成完整分析报告。
