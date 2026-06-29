"""
K线图表绘制 — 基于 mplfinance 的专业日K线图
=============================================
"""
import os
import tempfile
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplfinance as mpf

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans SC', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
# 压制CJK字体缺失警告（Windows下仅警告，不影响图生成）
warnings.filterwarnings('ignore', message='Glyph.*missing from font')


def generate_kline_chart(klines, title="", save_path=None):
    """
    生成专业日K线图（含成交量、MA5/MA10/MA20、MACD）。

    Parameters
    ----------
    klines : list[dict]
        K线数据，需含 date, open, close, high, low, volume
    title : str
        图表标题
    save_path : str or None
        保存路径，None则生成临时文件

    Returns
    -------
    str
        图片文件路径
    """
    if not klines or len(klines) < 5:
        return None

    # 数据准备
    df = pd.DataFrame(klines)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.rename(columns={
        'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'
    }, inplace=True)

    # 确保必要列存在
    for col in ['Open', 'Close', 'High', 'Low', 'Volume']:
        if col not in df.columns:
            return None

    # 计算均线
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(20).mean()

    # 计算MACD
    exp12 = df['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['Signal']

    # 构图
    add_plots = [
        mpf.make_addplot(df['MA5'], color='blue', width=0.8),
        mpf.make_addplot(df['MA10'], color='orange', width=0.8),
        mpf.make_addplot(df['MA20'], color='green', width=0.8),
    ]

    macd_colors = ['red' if v >= 0 else 'green' for v in df['MACD_Hist']]

    # 使用 subplot 显示 MACD
    apds = [
        mpf.make_addplot(df['MA5'], color='blue', width=0.8),
        mpf.make_addplot(df['MA10'], color='orange', width=0.8),
        mpf.make_addplot(df['MA20'], color='green', width=0.8),
        mpf.make_addplot(df['MACD'], color='purple', width=0.7, panel=2, ylabel='MACD'),
        mpf.make_addplot(df['Signal'], color='gray', width=0.7, panel=2),
    ]

    kwargs = dict(
        type='candle',
        volume=True,
        figsize=(14, 9),
        panel_ratios=(4, 1, 1.5),
        title=title,
        style='yahoo',
        addplot=apds,
        volume_panel=1,
        tight_layout=True,
        returnfig=True,
    )

    fig, axes = mpf.plot(df.tail(120), **kwargs)

    # MACD 柱状图
    ax_macd = axes[3]
    bars = ax_macd.bar(
        df.tail(120).index,
        df.tail(120)['MACD_Hist'],
        color=macd_colors[-120:],
        alpha=0.6,
        width=0.6
    )

    if save_path is None:
        fd, save_path = tempfile.mkstemp(suffix='.png')
        os.close(fd)

    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return save_path


def generate_simple_chart(klines, title="", save_path=None):
    """
    生成简洁K线图（不含MACD，适合报告快速插入）。
    """
    if not klines or len(klines) < 5:
        return None

    df = pd.DataFrame(klines)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.rename(columns={
        'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'volume': 'Volume'
    }, inplace=True)

    apds = [
        mpf.make_addplot(df['Close'].rolling(5).mean(), color='blue', width=0.8),
        mpf.make_addplot(df['Close'].rolling(10).mean(), color='orange', width=0.8),
        mpf.make_addplot(df['Close'].rolling(20).mean(), color='green', width=0.8),
    ]

    if save_path is None:
        fd, save_path = tempfile.mkstemp(suffix='.png')
        os.close(fd)

    mpf.plot(
        df.tail(60),
        type='candle',
        volume=True,
        figsize=(12, 7),
        title=title,
        style='yahoo',
        addplot=apds,
        savefig=save_path,
    )
    return save_path


def generate(code: str, name: str = "", days: int = 60, date: str = "", output_dir: str = None) -> str:
    """
    按股票代码直接生成K线图（自动从腾讯API获取数据）
    
    参数:
        code: 股票代码
        name: 股票名称（可选）
        days: 显示最近多少个交易日
        date: 指定日期（可选）
        output_dir: 输出目录（默认 ./doc）
    
    返回:
        图片文件路径
    """
    from . import data_fetcher as fetcher
    from datetime import datetime
    
    if output_dir is None:
        from . import config as cfg
        output_dir = cfg.DOC_DIR
    os.makedirs(output_dir, exist_ok=True)

    # 从腾讯API获取K线
    klines = fetcher.fetch_kline(code, days + 30)
    if not klines:
        print(f"[chart] {code}: 从腾讯API获取K线失败")
        return ""

    today = date if date else datetime.now().strftime("%Y%m%d")
    filename = f"{code}_{name}_{today}.png" if name else f"{code}_{today}.png"
    filepath = os.path.join(output_dir, filename)

    title_str = f"{name}({code}) {today}" if name else f"{code} {today}"
    return generate_kline_chart(klines[-days:], title=title_str, save_path=filepath)


# 兼容别名
generate_chart = generate
