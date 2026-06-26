#!/usr/bin/env python3
"""
K线图报告模块
- 通过腾讯行情API获取股票日K数据（前复权）
- 使用 mplfinance 绘制带 MA 指标的 K 线图
- 保存图片到 reports/ 目录
"""

import json
import os
import subprocess
import sys
from datetime import datetime

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import mplfinance as mpf


# 尝试设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def _check_font_support():
    """检查当前字体是否支持中文"""
    try:
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.set_title('中文测试')
        fig.canvas.draw()
        plt.close(fig)
        return True
    except Exception:
        return False


# 报告输出目录
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# 股票代码映射：{ 股票代码: 市场前缀 }
# 000xxx -> sz, 002xxx -> sz, 300xxx -> sz
# 600xxx -> sh, 601xxx -> sh, 603xxx -> sh
def get_market_prefix(code: str) -> str:
    """根据股票代码返回市场前缀"""
    code = code.strip()
    if code.startswith(('6', '9')):
        return 'sh'
    else:
        return 'sz'


def fetch_kline_data(code: str, days: int = 60) -> pd.DataFrame:
    """
    从腾讯行情API获取日K线数据（前复权）

    API: http://ifzq.gtimg.cn/appstock/app/fqkline/get?param=<market><code>,day,,,<count>,qfq

    返回: DataFrame, columns = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
    Date 为 datetime 类型且作为索引
    """
    prefix = get_market_prefix(code)
    symbol = f"{prefix}{code}"
    # 取 days 条数据，预留一些冗余
    count = min(max(days + 20, 60), 800)

    url = (
        f"http://ifzq.gtimg.cn/appstock/app/fqkline/get"
        f"?param={symbol},day,,,{count},qfq"
    )

    try:
        r = subprocess.run(
            ['curl.exe', '-s', url, '-L', '--max-time', '15'],
            capture_output=True, timeout=20
        )
        raw = r.stdout.decode('utf-8', errors='ignore')
        data = json.loads(raw)

        if data.get('code') != 0:
            raise ValueError(f"API 返回异常: {data.get('msg', 'unknown error')}")

        days_data = data.get('data', {}).get(symbol, {}).get('qfqday', [])
        if not days_data:
            raise ValueError(f"未获取到 {code} 的K线数据")

        # 取最近 days 条
        klines = days_data[-days:]

        rows = []
        for k in klines:
            # 格式: [date, open, close, high, low, volume]
            dt = pd.to_datetime(k[0])
            rows.append({
                'Date': dt,
                'Open': float(k[1]),
                'Close': float(k[2]),
                'High': float(k[3]),
                'Low': float(k[4]),
                'Volume': int(float(k[5])),
            })

        df = pd.DataFrame(rows)
        df.set_index('Date', inplace=True)
        return df

    except json.JSONDecodeError as e:
        raise ValueError(f"解析API返回数据失败: {e}")
    except subprocess.TimeoutExpired:
        raise ValueError("请求腾讯行情API超时")
    except Exception as e:
        raise ValueError(f"获取K线数据失败: {e}")


def generate_kline(code: str, name: str = "", days: int = 60) -> str:
    """
    生成单只股票的K线图

    参数:
        code: 股票代码，如 '000009'
        name: 股票名称，如 '中国宝安'（用于图标题）
        days: 获取最近多少天的数据

    返回:
        保存的图片文件路径
    """
    try:
        df = fetch_kline_data(code, days)
    except Exception as e:
        print(f"❌ 获取 {code} ({name}) K线数据失败: {e}")
        return ""

    if df.empty:
        print(f"❌ {code} ({name}) 无K线数据")
        return ""

    # 构造文件名
    safe_name = name if name else code
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kline_{code}_{safe_name}_{ts}.png"
    filepath = os.path.join(REPORT_DIR, filename)

    # 计算 MA 均线
    ma_periods = [5, 10, 20, 30, 60]
    apds = []
    for p in ma_periods:
        if len(df) >= p:
            apds.append(mpf.make_addplot(
                df['Close'].rolling(window=p).mean(),
                label=f"MA{p}",
                width=0.8,
            ))

    # 设置图表样式
    mc = mpf.make_marketcolors(
        up='red', down='green',
        edge='inherit',
        wick={'up': 'red', 'down': 'green'},
        volume={'up': 'red', 'down': 'green'},
    )
    s = mpf.make_mpf_style(
        marketcolors=mc,
        gridaxis='both',
        gridstyle='--',
        y_on_right=False,
    )

    # 设置标题（使用英文以避免中文显示问题）
    display_name = name if name else code
    title = f"{display_name} ({code}) K-Line Chart (Last {days} Days)"

    figsize = (14, 8)

    try:
        mpf.plot(
            df,
            type='candle',
            style=s,
            title=title,
            ylabel='价格 (元)',
            ylabel_lower='成交量 (手)',
            volume=True,
            addplot=apds,
            savefig=dict(fname=filepath, dpi=120, bbox_inches='tight'),
            figsize=figsize,
            tight_layout=True,
        )
        print(f"✅ K线图已保存: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ 绘制K线图失败: {e}")
        return ""


def generate_report() -> str:
    """
    生成主要盯盘股的K线图报告

    当前: 中国宝安(000009), 仙琚制药(002332)
    """
    stocks = [
        ('000009', '中国宝安'),
        ('002332', '仙琚制药'),
    ]

    saved_files = []
    for code, name in stocks:
        print(f"\n📊 正在生成 {name}({code}) K线图...")
        fp = generate_kline(code, name, days=60)
        if fp:
            saved_files.append(fp)

    print(f"\n{'=' * 50}")
    if saved_files:
        print(f"✅ K线图报告完成，共生成 {len(saved_files)} 张图片")
        for f in saved_files:
            print(f"   📁 {f}")
    else:
        print("❌ K线图报告生成失败，未生成任何图片")

    return "\n".join(saved_files)


if __name__ == "__main__":
    print("📊 K线图报告生成器")
    print("=" * 50)

    if len(sys.argv) > 1:
        code = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        generate_kline(code, name, days)
    else:
        generate_report()
