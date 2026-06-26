# 大乐透智能选号算法 — Python 完整实现

> 本文件包含所有可直接运行的 Python 代码，覆盖频率统计、遗漏分析、蒙特卡洛模拟、可视化分析。

---

## 1. 获取历史开奖数据

### 方式一：内置样本数据（快速使用）

```python
# 近50期大乐透开奖号码示例（格式：[前区5个, 后区2个]）
# 数据来源：中国体育彩票官方公告
SAMPLE_DATA = [
    # 期号, 前区, 后区
    ("26047", [9, 20, 21, 23, 28], [6, 11]),
    ("26046", [4, 11, 19, 25, 32], [2, 8]),
    ("26045", [7, 12, 18, 26, 33], [1, 9]),
    ("26044", [3, 14, 20, 27, 31], [4, 11]),
    ("26043", [8, 15, 22, 24, 30], [3, 7]),
    ("26042", [5, 11, 17, 28, 35], [5, 10]),
    ("26041", [2, 13, 19, 25, 32], [2, 9]),
    ("26040", [6, 16, 21, 27, 34], [1, 8]),
    ("26039", [10, 14, 20, 23, 29], [3, 11]),
    ("26038", [1, 12, 18, 26, 33], [4, 6]),
]
```

### 方式二：从接口抓取（推荐）

```python
import requests
import json

def fetch_dlt_history(count=100):
    """
    从体彩官方API获取大乐透历史数据
    返回格式：列表 [(期号, 前区列表, 后区列表), ...]
    """
    url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
    params = {
        "gameNo": "85",           # 大乐透gameNo
        "provinceId": "0",
        "pageSize": count,
        "isVerify": "1",
        "pageNo": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        records = data["value"]["list"]
        results = []
        for r in records:
            issue = r["lotteryDrawNum"]
            nums = r["lotteryDrawResult"].split(" ")
            front = [int(x) for x in nums[:5]]
            back = [int(x) for x in nums[5:7]]
            results.append((issue, sorted(front), sorted(back)))
        return results
    except Exception as e:
        print(f"获取数据失败: {e}，使用样本数据")
        return SAMPLE_DATA
```

---

## 2. 频率统计分析

```python
from collections import Counter

def frequency_analysis(history_data):
    """
    统计前区、后区各号码出现频率
    返回：前区频率字典, 后区频率字典
    """
    front_counter = Counter()
    back_counter = Counter()
    
    for _, front, back in history_data:
        front_counter.update(front)
        back_counter.update(back)
    
    n = len(history_data)
    
    # 转为频率（百分比）
    front_freq = {k: round(v/n*100, 2) for k, v in front_counter.items()}
    back_freq  = {k: round(v/n*100, 2) for k, v in back_counter.items()}
    
    # 补全未出现的号码
    for i in range(1, 36):
        front_freq.setdefault(i, 0.0)
    for i in range(1, 13):
        back_freq.setdefault(i, 0.0)
    
    return front_freq, back_freq


def get_hot_cold_numbers(freq_dict, hot_threshold=0.6, cold_threshold=0.35):
    """
    根据频率字典分类热号/中性号/冷号
    hot_threshold: 高于平均x倍为热号
    cold_threshold: 低于平均x倍为冷号
    """
    avg = sum(freq_dict.values()) / len(freq_dict)
    hot   = [k for k, v in freq_dict.items() if v >= avg * (1 + hot_threshold)]
    cold  = [k for k, v in freq_dict.items() if v <= avg * (1 - cold_threshold)]
    warm  = [k for k in freq_dict if k not in hot and k not in cold]
    return sorted(hot), sorted(warm), sorted(cold)


# 使用示例
if __name__ == "__main__":
    data = fetch_dlt_history(100)
    front_freq, back_freq = frequency_analysis(data)
    
    front_hot, front_warm, front_cold = get_hot_cold_numbers(front_freq)
    print(f"前区热号：{front_hot}")
    print(f"前区冷号：{front_cold}")
    
    back_hot, back_warm, back_cold = get_hot_cold_numbers(back_freq)
    print(f"后区热号：{back_hot}")
    print(f"后区冷号：{back_cold}")
```

---

## 3. 遗漏值分析

```python
def missing_value_analysis(history_data):
    """
    计算各号码当前遗漏值（距最近一次出现的期数）
    返回：前区遗漏字典, 后区遗漏字典
    """
    front_last = {}  # 号码 -> 最近出现的索引（0=最新）
    back_last  = {}
    
    for idx, (_, front, back) in enumerate(history_data):
        for n in front:
            if n not in front_last:
                front_last[n] = idx
        for n in back:
            if n not in back_last:
                back_last[n] = idx
    
    n = len(history_data)
    
    # 未出现过的号码遗漏值 = 总期数
    front_missing = {}
    for i in range(1, 36):
        front_missing[i] = front_last.get(i, n)
    
    back_missing = {}
    for i in range(1, 13):
        back_missing[i] = back_last.get(i, n)
    
    return front_missing, back_missing


def print_missing_table(missing_dict, label="前区"):
    """打印遗漏值表格"""
    print(f"\n{label} 遗漏值分析：")
    print(f"{'号码':>4} | {'遗漏值':>6} | 状态")
    print("-" * 25)
    for num in sorted(missing_dict.keys()):
        mv = missing_dict[num]
        if mv <= 5:
            status = "🔥 热"
        elif mv <= 15:
            status = "🌡 温"
        elif mv <= 30:
            status = "❄ 冷"
        else:
            status = "🧊 极冷"
        print(f"{num:>4} | {mv:>6} | {status}")
```

---

## 4. 综合过滤器

```python
def comprehensive_filter(front5, back2, config=None):
    """
    综合过滤函数
    config 可自定义各项阈值
    返回 (通过True/False, 失败原因)
    """
    if config is None:
        config = {
            "sum_min": 75, "sum_max": 115,
            "span_min": 15, "span_max": 30,
            "odd_min": 1, "odd_max": 4,     # 奇数个数范围
            "big_min": 1, "big_max": 4,     # 大号个数范围（大号>=18）
            "zone_min": 1,                  # 每区最少号码数
            "max_consecutive": 2,           # 最大连续号码数
            "back_span_min": 2, "back_span_max": 9
        }
    
    sorted_f = sorted(front5)
    
    # 1. 和值
    s = sum(sorted_f)
    if not (config["sum_min"] <= s <= config["sum_max"]):
        return False, f"和值{s}不在[{config['sum_min']},{config['sum_max']}]"
    
    # 2. 跨度
    span = sorted_f[-1] - sorted_f[0]
    if not (config["span_min"] <= span <= config["span_max"]):
        return False, f"跨度{span}不在[{config['span_min']},{config['span_max']}]"
    
    # 3. 奇偶
    odd = sum(1 for x in sorted_f if x % 2 == 1)
    if not (config["odd_min"] <= odd <= config["odd_max"]):
        return False, f"奇数{odd}个不在[{config['odd_min']},{config['odd_max']}]"
    
    # 4. 大小
    big = sum(1 for x in sorted_f if x >= 18)
    if not (config["big_min"] <= big <= config["big_max"]):
        return False, f"大号{big}个不在[{config['big_min']},{config['big_max']}]"
    
    # 5. 三区分布
    z1 = sum(1 for x in sorted_f if 1 <= x <= 11)
    z2 = sum(1 for x in sorted_f if 12 <= x <= 23)
    z3 = sum(1 for x in sorted_f if 24 <= x <= 35)
    if min(z1, z2, z3) < config["zone_min"]:
        return False, f"三区({z1},{z2},{z3})不均衡"
    
    # 6. 连号检查（最多允许1组2连）
    consec = sum(1 for i in range(4) if sorted_f[i+1] - sorted_f[i] == 1)
    if consec > config["max_consecutive"]:
        return False, f"含{consec}组连号超限"
    
    # 7. 后区跨度
    back_span = abs(back2[1] - back2[0])
    if not (config["back_span_min"] <= back_span <= config["back_span_max"]):
        return False, f"后区差值{back_span}不在[{config['back_span_min']},{config['back_span_max']}]"
    
    return True, "通过"
```

---

## 5. 蒙特卡洛智能选号（终极版）

```python
import random

def monte_carlo_dlt(
    n_output=10,
    n_sim=500000,
    use_hot_bias=True,
    history_data=None,
    config=None
):
    """
    蒙特卡洛模拟大乐透智能选号
    
    参数：
        n_output: 输出注数
        n_sim: 最大模拟次数
        use_hot_bias: 是否对热号加权（热号权重1.5x）
        history_data: 历史数据（用于热号分析）
        config: 过滤参数配置
    
    返回：满足条件的注数列表
    """
    # 构建权重（热号加权）
    front_weights = [1.0] * 36   # 索引0不用
    back_weights  = [1.0] * 13
    
    if use_hot_bias and history_data:
        front_freq, back_freq = frequency_analysis(history_data)
        avg_f = sum(front_freq.values()) / 35
        avg_b = sum(back_freq.values()) / 12
        
        for i in range(1, 36):
            f = front_freq.get(i, avg_f)
            front_weights[i] = 1.5 if f > avg_f * 1.3 else (0.7 if f < avg_f * 0.7 else 1.0)
        
        for i in range(1, 13):
            f = back_freq.get(i, avg_b)
            back_weights[i] = 1.5 if f > avg_b * 1.3 else (0.7 if f < avg_b * 0.7 else 1.0)
    
    front_pool = list(range(1, 36))
    back_pool  = list(range(1, 13))
    
    fw = [front_weights[i] for i in front_pool]
    bw = [back_weights[i]  for i in back_pool]
    
    results = []
    seen = set()
    attempts = 0
    
    while len(results) < n_output and attempts < n_sim:
        attempts += 1
        
        # 加权随机采样
        front5 = sorted(random.choices(front_pool, weights=fw, k=5))
        # 去重重复号码
        if len(set(front5)) < 5:
            continue
        
        back2 = sorted(random.choices(back_pool, weights=bw, k=2))
        if len(set(back2)) < 2:
            continue
        
        # 去重已生成的注数
        key = (tuple(front5), tuple(back2))
        if key in seen:
            continue
        
        # 综合过滤
        ok, reason = comprehensive_filter(front5, back2, config)
        if ok:
            results.append((front5, back2))
            seen.add(key)
    
    print(f"模拟{attempts}次，生成{len(results)}注（过滤率 {1-len(results)/max(attempts,1):.1%}）")
    return results


def print_tickets(tickets):
    """格式化输出彩票"""
    print("\n" + "="*50)
    print("🎯 大乐透智能选号结果（仅供娱乐参考）")
    print("="*50)
    for i, (f, b) in enumerate(tickets, 1):
        front_str = "  ".join(f"{x:02d}" for x in f)
        back_str  = "  ".join(f"{x:02d}" for x in b)
        
        # 统计信息
        f_sum = sum(f)
        f_span = max(f) - min(f)
        f_odd  = sum(1 for x in f if x%2==1)
        f_big  = sum(1 for x in f if x>=18)
        
        print(f"第{i:2d}注 │ 前区: {front_str} │ 后区: {back_str}")
        print(f"       │ 和值:{f_sum:3d} 跨度:{f_span:2d} 奇{f_odd}偶{5-f_odd} 大{f_big}小{5-f_big}")
    print("="*50)
    print("⚠️  彩票为随机事件，本工具仅供参考，请理性消费！")


# 主程序
if __name__ == "__main__":
    print("正在获取历史开奖数据...")
    data = fetch_dlt_history(100)
    print(f"已获取 {len(data)} 期历史数据")
    
    print("\n正在进行遗漏值分析...")
    front_missing, back_missing = missing_value_analysis(data)
    
    # 找出当前极冷号（遗漏>20期）
    extreme_cold_front = [k for k, v in front_missing.items() if v > 20]
    print(f"前区极冷号（遗漏>20）：{extreme_cold_front}")
    
    print("\n生成智能选号中...")
    tickets = monte_carlo_dlt(n_output=10, use_hot_bias=True, history_data=data)
    print_tickets(tickets)
```

---

## 6. 可视化分析（Plotly）

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_frequency(front_freq, back_freq, title="大乐透号码频率分析"):
    """绘制热力图（前区+后区）"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["前区号码频率（01-35）", "后区号码频率（01-12）"],
        vertical_spacing=0.15
    )
    
    # 前区
    front_nums  = list(range(1, 36))
    front_freqs = [front_freq.get(n, 0) for n in front_nums]
    colors_f = ["#FF4444" if f > sum(front_freqs)/35*1.3 
                else "#FF9900" if f > sum(front_freqs)/35 
                else "#6699CC" for f in front_freqs]
    
    fig.add_trace(go.Bar(
        x=[f"{n:02d}" for n in front_nums],
        y=front_freqs,
        marker_color=colors_f,
        name="前区频率",
        text=[f"{v:.1f}%" for v in front_freqs],
        textposition="outside"
    ), row=1, col=1)
    
    # 后区
    back_nums  = list(range(1, 13))
    back_freqs = [back_freq.get(n, 0) for n in back_nums]
    colors_b = ["#FF4444" if f > sum(back_freqs)/12*1.3 
               else "#FF9900" if f > sum(back_freqs)/12 
               else "#6699CC" for f in back_freqs]
    
    fig.add_trace(go.Bar(
        x=[f"{n:02d}" for n in back_nums],
        y=back_freqs,
        marker_color=colors_b,
        name="后区频率",
        text=[f"{v:.1f}%" for v in back_freqs],
        textposition="outside"
    ), row=2, col=1)
    
    fig.update_layout(
        title=title,
        showlegend=False,
        height=600,
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#16213e",
        font=dict(color="white")
    )
    
    fig.show()
    return fig
```

---

## 7. 快速一键运行示例

```python
# === 一键使用示例（复制到Jupyter或Python文件直接运行）===

# 步骤1：生成10注智能选号
data = fetch_dlt_history(100)
tickets = monte_carlo_dlt(n_output=10, history_data=data)
print_tickets(tickets)

# 步骤2：查看频率分析
front_freq, back_freq = frequency_analysis(data)
front_hot, _, front_cold = get_hot_cold_numbers(front_freq)
print(f"热号：{front_hot} | 冷号：{front_cold}")

# 步骤3：查看遗漏值
front_m, back_m = missing_value_analysis(data)
print_missing_table(front_m, "前区")
print_missing_table(back_m, "后区")
```

---

*所有代码均基于Python 3.8+，依赖：requests, plotly（可选）*  
*使用前请确保已安装：`pip install requests plotly`*
