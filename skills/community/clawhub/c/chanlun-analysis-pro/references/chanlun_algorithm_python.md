# 缠论核心算法 Python 实现

> 基于缠中说禅108课理论的缠论量化实现，集成 czsc 框架与 chan.py 开源项目。
> 涵盖：数据获取、分型识别、笔/线段/中枢构建、背驰判定、三类买卖点量化识别。

---

## 一、环境配置与数据获取

### 1.1 安装依赖

```bash
pip install czsc akshare baostock numpy pandas mplfinance
# 可选：chan.py（更灵活的框架）
pip install chanpy
```

### 1.2 使用 AKShare 获取 A股数据

```python
import akshare as ak
import pandas as pd

def get_stock_data(stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取A股日线数据
    stock_code: 上证如 "600519"（贵州茅台），深证如 "000001"（平安银行）
    """
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,  # 格式：YYYYMMDD
        end_date=end_date,
        adjust="qfq"  # 前复权
    )

    # 标准化列名
    df = df.rename(columns={
        "日期": "dt",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "vol"
    })
    df["dt"] = pd.to_datetime(df["dt"])
    return df[["dt", "open", "high", "low", "close", "vol"]]

# 示例：获取贵州茅台2023-2025年数据
df = get_stock_data("600519", "20230101", "20260101")
print(df.tail())
```

### 1.3 使用 Baostock 获取分钟线数据

```python
import baostock as bs

def get_minute_data(stock_code: str, frequency: str = "30") -> pd.DataFrame:
    """
    获取分钟K线数据
    frequency: 5/15/30/60 分钟
    """
    bs.login()
    rs = bs.query_history_k_data_plus(
        stock_code,
        "date,time,open,high,low,close,volume",
        start_date="2024-01-01",
        end_date="2025-01-01",
        frequency=frequency,
        adjust="qfq"
    )

    data_list = []
    while rs.error_code == "0" and rs.next():
        data_list.append(rs.get_row_data())

    bs.logout()
    return pd.DataFrame(data_list, columns=["dt", "time", "open", "high", "low", "close", "vol"])
```

---

## 二、分型识别算法

### 2.1 顶分型与底分型判定

```python
def identify_fractals(klines: list) -> list:
    """
    识别顶分型和底分型
    klines: list of (high, low) tuples
    返回: list of {"type": "top"/"bottom", "index": int}
    """
    if len(klines) < 3:
        return []

    results = []
    for i in range(1, len(klines) - 1):
        prev = klines[i - 1]
        curr = klines[i]
        next_k = klines[i + 1]

        # 顶分型：中间K线高点最高，低点也最高
        if (curr["high"] > prev["high"] and curr["high"] > next_k["high"] and
                curr["low"] > prev["low"] and curr["low"] > next_k["low"]):
            results.append({"type": "top", "index": i, "price": curr["high"]})

        # 底分型：中间K线低点最低，高点也最低
        elif (curr["low"] < prev["low"] and curr["low"] < next_k["low"] and
              curr["high"] < prev["high"] and curr["high"] < next_k["high"]):
            results.append({"type": "bottom", "index": i, "price": curr["low"]})

    return results
```

### 2.2 包含关系处理（化简K线）

```python
def process_inclusive_klines(klines: list) -> list:
    """
    处理K线的包含关系（化简K线）
    包含关系：两根K线，一根完全在另一根的范围内
    处理规则：
      上升K线（第一根低点<=第二根低点）：取高高（高取高，低也取高）
      下降K线（第一根低点>第二根低点）：取低低（高取低，低也取低）
    """
    if len(klines) < 2:
        return klines

    processed = [klines[0]]
    direction = None  # 初始化方向

    for i in range(1, len(klines)):
        current = klines[i]
        last = processed[-1]

        # 判断是否存在包含关系
        has_include = (
            (last["low"] <= current["low"] and last["high"] >= current["high"]) or
            (current["low"] <= last["low"] and current["high"] >= last["high"])
        )

        if not has_include:
            # 无包含关系，直接加入
            processed.append(current)
        else:
            # 存在包含关系，需要处理
            # 先确定方向（第一根K线之后确定）
            if direction is None:
                direction = "up" if last["low"] <= current["low"] else "down"

            if direction == "up":
                # 上升K线：取高高
                new_k = {
                    "high": max(last["high"], current["high"]),
                    "low": max(last["low"], current["low"])
                }
            else:
                # 下降K线：取低低
                new_k = {
                    "high": min(last["high"], current["high"]),
                    "low": min(last["low"], current["low"])
                }

            processed[-1] = new_k

    return processed
```

---

## 三、笔的划分算法

```python
def identify_bi(klines: list, min_bars: int = 5) -> list:
    """
    笔的严格划分算法
    规则：
      1. 顶底分型之间至少有5根（不含包含关系处理后的）K线
      2. 顶底分型之间不存在共用K线
      3. 笔的方向由顶底分型的高低决定
    min_bars: 笔之间最少K线数，默认5根
    返回: list of {"type": "up"/"down", "start_idx": int, "end_idx": int}
    """
    # Step 1: 化简K线
    simplified = process_inclusive_klines(klines)

    # Step 2: 识别分型
    fractals = identify_fractals(simplified)

    # Step 3: 划分笔
    if len(fractals) < 2:
        return []

    bi_list = []
    last_valid = fractals[0]

    for i in range(1, len(fractals)):
        current = fractals[i]

        # 检查是否为同类型（连续两个顶分型或底分型，取后面的）
        if current["type"] == last_valid["type"]:
            last_valid = current
            continue

        # 计算两根分型之间的K线数
        kline_count = current["index"] - last_valid["index"] - 1

        # 判断是否为有效笔
        if kline_count >= min_bars:
            direction = "up" if current["type"] == "top" else "down"
            bi_list.append({
                "type": direction,
                "start_idx": last_valid["index"],
                "end_idx": current["index"],
                "start_price": simplified[last_valid["index"]]["high"] if direction == "down"
                              else simplified[last_valid["index"]]["low"],
                "end_price": simplified[current["index"]]["high"] if direction == "up"
                            else simplified[current["index"]]["low"]
            })
            last_valid = current

    return bi_list
```

---

## 四、线段构建算法

```python
def identify_xianduan(bi_list: list) -> list:
    """
    线段识别算法
    规则：
      1. 线段由连续三笔构成，且方向一致
      2. 线段被破坏：反向一笔突破线段最后一个高点/低点
      3. 线段破坏需要反向三笔确认
    """
    if len(bi_list) < 3:
        return []

    xianduan_list = []
    current_xianduan = {
        "direction": bi_list[0]["type"],
        "start_idx": bi_list[0]["start_idx"],
        "bi_list": [bi_list[0]]
    }

    for i in range(1, len(bi_list)):
        bi = bi_list[i]

        if bi["type"] == current_xianduan["direction"]:
            # 同向笔，加入当前线段
            current_xianduan["bi_list"].append(bi)
        else:
            # 反向笔
            if len(current_xianduan["bi_list"]) >= 3:
                # 已有3笔，检查是否构成线段
                last_bi = current_xianduan["bi_list"][-1]
                second_last_bi = current_xianduan["bi_list"][-2]

                # 判断线段是否被破坏
                if bi["type"] == "up":
                    # 需要向下突破才能破坏向上线段
                    if bi["end_price"] < last_bi["start_price"]:
                        # 线段结束
                        xianduan_list.append({
                            "direction": current_xianduan["direction"],
                            "start_idx": current_xianduan["start_idx"],
                            "end_idx": last_bi["end_idx"],
                            "peak_trough": last_bi["end_price"]
                        })
                        current_xianduan = {
                            "direction": bi["type"],
                            "start_idx": last_bi["end_idx"],
                            "bi_list": [last_bi, bi]
                        }
                    else:
                        current_xianduan["bi_list"].append(bi)
                else:
                    if bi["end_price"] > last_bi["start_price"]:
                        xianduan_list.append({
                            "direction": current_xianduan["direction"],
                            "start_idx": current_xianduan["start_idx"],
                            "end_idx": last_bi["end_idx"],
                            "peak_trough": last_bi["end_price"]
                        })
                        current_xianduan = {
                            "direction": bi["type"],
                            "start_idx": last_bi["end_idx"],
                            "bi_list": [last_bi, bi]
                        }
                    else:
                        current_xianduan["bi_list"].append(bi)
            else:
                current_xianduan["bi_list"].append(bi)

    # 处理最后一个线段
    if len(current_xianduan["bi_list"]) >= 3:
        last_bi = current_xianduan["bi_list"][-1]
        xianduan_list.append({
            "direction": current_xianduan["direction"],
            "start_idx": current_xianduan["start_idx"],
            "end_idx": last_bi["end_idx"],
            "peak_trough": last_bi["end_price"]
        })

    return xianduan_list
```

---

## 五、中枢构建算法

```python
def identify_zhongshu(xianduan_list: list) -> list:
    """
    中枢识别算法
    中枢定义：由至少三段（线段或笔）重叠部分构成的价格区间
    中枢区间：[ZD（中枢低点）, ZG（中枢高点）]
    """
    if len(xianduan_list) < 3:
        return []

    zhongshu_list = []
    i = 0

    while i < len(xianduan_list) - 2:
        # 取连续三段
        seg1 = xianduan_list[i]
        seg2 = xianduan_list[i + 1]
        seg3 = xianduan_list[i + 2]

        # 计算重叠区间
        ranges = []
        for seg in [seg1, seg2, seg3]:
            if seg["direction"] == "up":
                ranges.append({"high": seg["end_price"], "low": seg["start_price"]})
            else:
                ranges.append({"high": seg["start_price"], "low": seg["end_price"]})

        # 计算重叠部分
        overlap_high = min(r[0]["high"] for r in ranges)
        overlap_low = max(r[0]["low"] for r in ranges)

        if overlap_low < overlap_high:  # 有有效重叠
            zhongshu_list.append({
                "ZG": overlap_high,
                "ZD": overlap_low,
                "start_idx": seg1["start_idx"],
                "end_idx": seg3["end_idx"],
                "segments": [seg1, seg2, seg3]
            })
            i += 3  # 至少跳过一个中枢
        else:
            i += 1

    return zhongshu_list


def get_zhongshu_direction(zhongshu_list: list, idx: int) -> str:
    """判断中枢的方向"""
    if len(zhongshu_list) <= 1:
        return "neutral"  # 盘整

    current = zhongshu_list[idx]
    current_peak_trough = xianduan_list[current["start_idx"]:current["end_idx"]+1]

    # 比较中枢前后走势的方向
    # （简化实现，完整实现需跟踪线段方向）
    return "up" if len(zhongshu_list) > 1 else "neutral"
```

---

## 六、背驰判定算法（动力学核心）

```python
import numpy as np
import pandas as pd

def calculate_macd(close_prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    计算MACD指标（辅助背驰判定）
    """
    ema_fast = close_prices.ewm(span=fast, adjust=False).mean()
    ema_slow = close_prices.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    bar = 2 * (dif - dea)

    return pd.DataFrame({"DIF": dif, "DEA": dea, "BAR": bar})


def calculate_macd_area(price_segment: pd.DataFrame) -> float:
    """
    计算某段走势的MACD面积（用于背驰判定）
    面积 = Σ(BAR_i × 涨幅_i)，正值累加为红柱面积，负值累加为绿柱面积
    """
    macd = calculate_macd(price_segment["close"])
    bar = macd["BAR"].values

    # 计算红柱面积（正值）
    red_area = np.sum(bar[bar > 0])
    # 计算绿柱面积（负值的绝对值）
    green_area = np.abs(np.sum(bar[bar < 0]))

    return {"red_area": red_area, "green_area": green_area, "net_area": red_area - green_area}


def check_divergence(df: pd.DataFrame, price_col: str = "close", lookback: int = 50) -> dict:
    """
    背驰检测（顶背驰/底背驰）
    逻辑：
      顶背驰：价格创阶段新高，但MACD不创新高
      底背驰：价格创阶段新低，但MACD不创新低
    """
    recent = df.tail(lookback)
    macd = calculate_macd(df[price_col])

    # 找到最近的高点和低点
    recent_macd = macd.tail(lookback)

    # 顶背驰检测
    price_high = recent[price_col].max()
    dif_high = recent_macd["DIF"].max()

    # 检查历史高点
    historical = df.head(len(df) - lookback)
    hist_macd = calculate_macd(historical[price_col])
    hist_price_high = historical[price_col].max()
    hist_dif_high = hist_macd["DIF"].max()

    # 顶背驰判定：价格创新高，但DIF不创新高
    is_top_divergence = (
        price_high > hist_price_high and
        dif_high < hist_dif_high
    )

    # 底背驰检测
    price_low = recent[price_col].min()
    dif_low = recent_macd["DIF"].min()
    hist_price_low = historical[price_col].min()
    hist_dif_low = hist_macd["DIF"].min()

    is_bottom_divergence = (
        price_low < hist_price_low and
        dif_low > hist_dif_low
    )

    return {
        "is_top_divergence": is_top_divergence,
        "is_bottom_divergence": is_bottom_divergence,
        "details": {
            "current_price_high": price_high,
            "historical_price_high": hist_price_high,
            "current_dif_high": dif_high,
            "historical_dif_high": hist_dif_high,
            "divergence_strength": abs(dif_high - hist_dif_high) / hist_dif_high if hist_dif_high != 0 else 0
        }
    }
```

---

## 七、三类买卖点量化判定

```python
def find_buy_sell_points(df: pd.DataFrame) -> dict:
    """
    缠论三类买卖点量化识别
    返回: 包含各类买卖点位置的字典
    """
    # Step 1: 计算缠论结构
    klines = df.to_dict("records")

    # Step 2: 识别笔
    bi_list = identify_bi(klines)
    if len(bi_list) < 5:
        return {"error": "数据不足以形成笔结构"}

    # Step 3: 识别线段
    xianduan_list = identify_xianduan(bi_list)

    # Step 4: 识别中枢
    zhongshu_list = identify_zhongshu(xianduan_list)

    # Step 5: 计算MACD
    macd_df = calculate_macd(df["close"])
    df_with_macd = df.copy()
    df_with_macd["DIF"] = macd_df["DIF"].values
    df_with_macd["DEA"] = macd_df["DEA"].values
    df_with_macd["BAR"] = macd_df["BAR"].values

    # Step 6: 买卖点识别
    buy_points = {"first": [], "second": [], "third": []}
    sell_points = {"first": [], "second": [], "third": []}

    # 第一类买点：趋势背驰点
    if len(zhongshu_list) >= 2 and len(bi_list) >= 5:
        last_down_bi = None
        for bi in reversed(bi_list):
            if bi["type"] == "down":
                last_down_bi = bi
                break

        if last_down_bi:
            # 检查背驰
            bi_idx = last_down_bi["end_idx"]
            segment_data = df_with_macd.iloc[max(0, bi_idx-50):bi_idx+1]
            divergence = check_divergence(segment_data)
            if divergence["is_bottom_divergence"]:
                buy_points["first"].append({
                    "price": last_down_bi["end_price"],
                    "index": bi_idx,
                    "背驰强度": divergence["details"].get("divergence_strength", 0)
                })

    # 第二类买点：第一类买点后向上笔回调不破低点
    if buy_points["first"] and len(bi_list) >= 6:
        first_buy = buy_points["first"][-1]
        first_buy_idx = first_buy["index"]
        for bi in bi_list:
            if bi["start_idx"] > first_buy_idx and bi["type"] == "up":
                # 找到向上笔之后的向下笔
                next_down = None
                for later_bi in bi_list:
                    if later_bi["start_idx"] > bi["end_idx"] and later_bi["type"] == "down":
                        next_down = later_bi
                        break
                if next_down and next_down["end_price"] > first_buy["price"]:
                    buy_points["second"].append({
                        "price": next_down["end_price"],
                        "index": next_down["end_idx"]
                    })
                break

    # 第三类买点：向上离开中枢后回调不进中枢
    if len(zhongshu_list) >= 1 and len(bi_list) >= 4:
        last_zs = zhongshu_list[-1]
        for bi in reversed(bi_list):
            if bi["type"] == "up" and bi["start_idx"] >= last_zs["end_idx"]:
                if bi["end_price"] > last_zs["ZG"]:
                    # 向上离开中枢，检查是否回调不进
                    for later_bi in bi_list:
                        if later_bi["start_idx"] > bi["end_idx"] and later_bi["type"] == "down":
                            if later_bi["end_price"] > last_zs["ZD"]:
                                buy_points["third"].append({
                                    "price": later_bi["end_price"],
                                    "index": later_bi["end_idx"],
                                    "中枢ZG": last_zs["ZG"],
                                    "中枢ZD": last_zs["ZD"]
                                })
                            break
                break

    return {
        "buy_points": buy_points,
        "sell_points": sell_points,  # 对称逻辑可得
        "中枢": zhongshu_list[-1] if zhongshu_list else None,
        "最近笔": bi_list[-1] if bi_list else None
    }
```

---

## 八、czsc框架集成（推荐使用）

```python
# 使用 czsc 框架进行缠论分析（更完整实现）
from czsc import CZSC, CZSC_ANlaysis
from czsc.utils import get_default_config
import akshare as ak

def chanlun_analysis_czsc(stock_code: str, end_date: str = None):
    """
    使用czsc框架进行缠论分析（推荐方式）
    """
    # Step 1: 获取数据
    df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")

    # Step 2: 构建缠论对象
    c = CZSC(df, freq="日线")

    # Step 3: 获取分型
    fengxing = c.fengxing

    # Step 4: 获取笔
    bi = c.bi

    # Step 5: 获取线段
    xd = c.xianduan

    # Step 6: 获取中枢
    zs = c.zhongshu

    # Step 7: 获取买卖点信号
    signals = c.get_signals()

    # Step 8: 生成分析报告
    report = {
        "股票代码": stock_code,
        "最新价格": df["close"].iloc[-1],
        "分型数量": len(fengxing),
        "笔数量": len(bi),
        "线段数量": len(xd),
        "中枢数量": len(zs),
        "最新买卖点": signals[-1] if signals else None,
    }

    return report
```

---

## 九、可视化缠论结构

```python
import matplotlib.pyplot as plt
import mplfinance as mpf

def plot_chanlun(df: pd.DataFrame, bi_list: list, zhongshu_list: list, save_path: str = None):
    """
    缠论结构可视化
    """
    fig, axes = plt.subplots(2, 1, figsize=(16, 10),
                              gridspec_kw={'height_ratios': [3, 1]})

    # 上图：K线 + 笔 + 中枢
    ax1 = axes[0]
    mpf.plot(df.set_index("dt"), type="candle", ax=ax1, style="charles",
             show_nontrading=False, mav=(5, 10, 20))

    # 标注笔
    colors = {"up": "r", "down": "g"}
    for bi in bi_list[-20:]:  # 最近20笔
        start = bi["start_idx"]
        end = bi["end_idx"]
        ax1.annotate("", xy=(end, bi["end_price"]), xytext=(start, bi["start_price"]),
                    arrowprops=dict(arrowstyle="->", color=colors[bi["type"]], lw=2))

    # 标注中枢
    for zs in zhongshu_list[-3:]:
        ax1.axhline(y=zs["ZG"], color="purple", linestyle="--", alpha=0.5)
        ax1.axhline(y=zs["ZD"], color="purple", linestyle="--", alpha=0.5)
        ax1.fill_between(range(len(df)), zs["ZD"], zs["ZG"], alpha=0.1, color="purple")

    # 下图：MACD
    ax2 = axes[1]
    macd = calculate_macd(df["close"])
    ax2.plot(macd["DIF"], label="DIF", color="blue")
    ax2.plot(macd["DEA"], label="DEA", color="orange")
    ax2.bar(range(len(macd)), macd["BAR"], label="BAR", color="red", alpha=0.5)
    ax2.legend()
    ax2.set_title("MACD指标（辅助背驰判定）")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
```

---

## 十、性能优化建议

| 优化方向 | 方法 | 效果 |
|---------|------|------|
| 数据处理 | 使用numpy向量化替代循环 | 速度提升10-50倍 |
| 分型识别 | Cython编译热点函数 | 速度提升5-20倍 |
| 实时计算 | 只计算新增K线的笔/线段变化 | 实时性提升 |
| 可视化 | 使用mplfinance而非matplotlib原生 | 更快更美观 |
| 数据存储 | 使用SQLite存储历史数据 | 避免重复下载 |

---

> 📌 **合规提示**：缠论量化分析仅供参考，实盘操作前请充分回测，切勿盲目依赖单一指标。
