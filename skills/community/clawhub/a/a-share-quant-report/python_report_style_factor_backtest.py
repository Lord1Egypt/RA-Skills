import warnings
warnings.filterwarnings('ignore')

import os
import math
import json
import base64
from io import BytesIO
from typing import List, Dict

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
import akshare as ak

OUT_DIR = os.getenv('OUT_DIR', '/mnt/user-data/outputs/report_style_backtest_demo_v2')
START = os.getenv('START', '2022-01-01')
END = os.getenv('END', '2025-05-01')
BENCHMARK = os.getenv('BENCHMARK', '510300.SS')
TOP_N = int(os.getenv('TOP_N', '20'))
QUANTILES = int(os.getenv('QUANTILES', '5'))
TCOST_ONE_WAY = float(os.getenv('TCOST_ONE_WAY', '0.0015'))
TARGET_DOWNLOAD_STOCKS = int(os.getenv('TARGET_DOWNLOAD_STOCKS', '1000'))
MIN_HISTORY = int(os.getenv('MIN_HISTORY', '400'))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '60'))
INDEX_SYMBOLS = os.getenv('INDEX_SYMBOLS', '000300,000905,000852').split(',')
REPORT_TITLE = os.getenv('REPORT_TITLE', 'A-share Factor Research Backtest')
RESEARCH_QUESTION = os.getenv('RESEARCH_QUESTION', '该因子是否具有稳定的横截面选股能力，并能否转化为可交易组合收益？')
FACTOR_NARRATIVE = os.getenv('FACTOR_NARRATIVE', '短期反转 + 量能冲击 - 波动率惩罚')
UNIVERSE_NOTE = os.getenv('UNIVERSE_NOTE', '默认使用沪深300 + 中证500 + 中证1000 当前成分股并集，作为可扩展到1000只以上的A股液态股票池。')

os.makedirs(OUT_DIR, exist_ok=True)

PLOT_FILES = [
    '01_factor_distribution.png',
    '02_rankic_timeseries.png',
    '03_monthly_rankic_heatmap.png',
    '04_quantile_nav.png',
    '05_long_vs_benchmark_nav.png',
    '06_long_short_nav.png',
    '07_excess_and_drawdown.png',
    '08_turnover_and_coverage.png',
]

CAPTIONS = {
    '01_factor_distribution.png': '因子分布图：检查横截面分布是否偏态、是否存在极端值，以及预处理后是否便于排序使用。',
    '02_rankic_timeseries.png': 'RankIC时间序列：观察因子预测方向是否稳定、阶段性失效是否明显，以及滚动均值是否长期位于零轴上方。',
    '03_monthly_rankic_heatmap.png': '月度RankIC热力图：以月份和年份双维度展示因子有效性的时变特征，识别高胜率区间和失效阶段。',
    '04_quantile_nav.png': '分层累计收益图：验证分组收益是否具有单调性，并观察顶层与底层组合之间的收益差异。',
    '05_long_vs_benchmark_nav.png': '多头组合与基准净值图：比较策略多头组合相对基准的累计表现，查看超额收益是否稳定。',
    '06_long_short_nav.png': '多空组合净值图：在更纯粹的因子检验口径下评估因子方向性和可交易性。',
    '07_excess_and_drawdown.png': '超额净值与回撤图：上图展示相对基准累计超额，下图展示策略净值回撤路径，更符合研报展示习惯。',
    '08_turnover_and_coverage.png': '换手率与覆盖率图：同时评估组合交易强度和因子样本覆盖稳定性，辅助判断可实施性。',
}


def winsorize_row(row: pd.Series, n: float = 3.0) -> pd.Series:
    s = row.copy()
    mu = s.mean()
    sd = s.std()
    if pd.isna(sd) or sd == 0:
        return s
    return s.clip(mu - n * sd, mu + n * sd)



def zscore_row(row: pd.Series) -> pd.Series:
    s = row.copy()
    sd = s.std()
    if pd.isna(sd) or sd == 0:
        return s * 0
    return (s - s.mean()) / sd



def safe_float(x):
    try:
        if pd.isna(x):
            return np.nan
        return float(x)
    except Exception:
        return np.nan



def annual_return_from_nav(nav: pd.Series) -> float:
    nav = pd.Series(nav).dropna().astype(float)
    if len(nav) < 2:
        return np.nan
    years = max((nav.index[-1] - nav.index[0]).days / 365.25, 1e-9)
    return nav.iloc[-1] ** (1 / years) - 1



def calc_metrics(ret: pd.Series) -> Dict[str, float]:
    ret = pd.Series(ret).dropna().astype(float)
    if len(ret) == 0:
        return {
            '累计收益': np.nan,
            '年化收益': np.nan,
            '年化波动': np.nan,
            'Sharpe': np.nan,
            '最大回撤': np.nan,
            '日胜率': np.nan,
        }
    nav = (1 + ret).cumprod()
    ann = annual_return_from_nav(nav)
    vol = ret.std() * np.sqrt(252)
    sharpe = (ret.mean() * 252 / vol) if vol and vol > 0 else np.nan
    dd = nav / nav.cummax() - 1
    return {
        '累计收益': nav.iloc[-1] - 1,
        '年化收益': ann,
        '年化波动': vol,
        'Sharpe': sharpe,
        '最大回撤': dd.min(),
        '日胜率': (ret > 0).mean(),
    }



def format_pct(x):
    return '-' if pd.isna(x) else f'{x:.2%}'



def format_num(x):
    return '-' if pd.isna(x) else f'{x:.4f}'



def markdown_table(df: pd.DataFrame, float_pct_cols=None, float_num_cols=None) -> str:
    float_pct_cols = set(float_pct_cols or [])
    float_num_cols = set(float_num_cols or [])
    cols = list(df.columns)
    header = '| ' + ' | '.join(cols) + ' |'
    sep = '| ' + ' | '.join(['---'] * len(cols)) + ' |'
    lines = [header, sep]
    for _, row in df.iterrows():
        vals = []
        for c in cols:
            v = row[c]
            if c in float_pct_cols:
                vals.append(format_pct(v) if isinstance(v, (float, int, np.floating, np.integer)) or pd.isna(v) else str(v))
            elif c in float_num_cols:
                vals.append(format_num(v) if isinstance(v, (float, int, np.floating, np.integer)) or pd.isna(v) else str(v))
            else:
                vals.append(str(v))
        lines.append('| ' + ' | '.join(vals) + ' |')
    return '\n'.join(lines)



def to_yf(code: str) -> str:
    return f'{code}.SS' if str(code).startswith(('5', '6', '9')) else f'{code}.SZ'



def get_universe(target_download_stocks: int = TARGET_DOWNLOAD_STOCKS) -> List[str]:
    tickers = []
    seen = set()
    for sym in INDEX_SYMBOLS:
        try:
            cons = ak.index_stock_cons(symbol=sym.strip())
            codes = cons['品种代码'].astype(str).str.zfill(6).tolist()
            for c in codes:
                t = to_yf(c)
                if t not in seen:
                    seen.add(t)
                    tickers.append(t)
        except Exception:
            continue
    if target_download_stocks > 0:
        tickers = tickers[:max(target_download_stocks, 0)]
    return tickers



def extract_from_download(raw, ticker: str):
    if raw is None or len(raw) == 0:
        return None
    try:
        if isinstance(raw.columns, pd.MultiIndex):
            lvl0 = raw.columns.get_level_values(0)
            lvl1 = raw.columns.get_level_values(1)
            if ticker in lvl0:
                sub = raw[ticker].copy()
            elif ticker in lvl1:
                sub = raw.xs(ticker, axis=1, level=1).copy()
            else:
                return None
        else:
            sub = raw.copy()
        needed = {'Close', 'Volume'}
        if not needed.issubset(set(sub.columns)):
            return None
        close = pd.Series(sub['Close']).rename(ticker)
        volume = pd.Series(sub['Volume']).rename(ticker)
        return close, volume
    except Exception:
        return None



def download_panel(tickers: List[str]):
    close, volume = {}, {}
    failed = []
    for i in range(0, len(tickers), CHUNK_SIZE):
        chunk = tickers[i:i + CHUNK_SIZE]
        try:
            raw = yf.download(chunk, start=START, end=END, auto_adjust=True, progress=False, group_by='ticker', threads=False)
        except Exception:
            raw = None
        for t in chunk:
            out = extract_from_download(raw, t)
            if out is None:
                failed.append(t)
                continue
            c, v = out
            if c.notna().sum() >= MIN_HISTORY:
                close[t] = c
                volume[t] = v
            else:
                failed.append(t)
    close = pd.DataFrame(close).sort_index()
    volume = pd.DataFrame(volume).reindex(close.index)
    return close, volume, failed



def build_factor(close: pd.DataFrame, volume: pd.DataFrame):
    ret1 = close.pct_change()
    ret5 = close.pct_change(5)
    vol_ratio = volume / volume.rolling(20).mean() - 1
    vol20 = ret1.rolling(20).std()
    alpha_raw = (
        (-ret5).rank(axis=1, pct=True) +
        0.5 * vol_ratio.rank(axis=1, pct=True) -
        0.5 * vol20.rank(axis=1, pct=True)
    )
    alpha = alpha_raw.apply(winsorize_row, axis=1).apply(zscore_row, axis=1)
    return alpha, ret1



def calc_ic(alpha: pd.DataFrame, fwd_ret: pd.DataFrame):
    rank_ic, ic = [], []
    idx = alpha.index.intersection(fwd_ret.index)
    for d in idx:
        x = alpha.loc[d]
        y = fwd_ret.loc[d]
        df = pd.concat([x, y], axis=1).dropna()
        if len(df) < 20:
            ic.append(np.nan)
            rank_ic.append(np.nan)
            continue
        ic.append(df.iloc[:, 0].corr(df.iloc[:, 1], method='pearson'))
        rank_ic.append(df.iloc[:, 0].corr(df.iloc[:, 1], method='spearman'))
    out = pd.DataFrame({'IC': ic, 'RankIC': rank_ic}, index=idx)
    out['month'] = out.index.to_period('M').astype(str)
    return out



def assign_quantiles(row: pd.Series, q: int = 5):
    s = row.dropna()
    if len(s) < q:
        return pd.Series(index=row.index, dtype=float)
    try:
        bins = pd.qcut(s.rank(method='first'), q, labels=False) + 1
        out = pd.Series(index=row.index, dtype=float)
        out.loc[s.index] = bins.astype(float)
        return out
    except Exception:
        return pd.Series(index=row.index, dtype=float)



def quantile_backtest(alpha: pd.DataFrame, next_ret: pd.DataFrame, q: int = 5):
    quantiles = alpha.apply(assign_quantiles, axis=1, q=q)
    group_ret = pd.DataFrame(index=alpha.index, columns=[f'G{i}' for i in range(1, q + 1)], dtype=float)
    for d in alpha.index:
        qrow = quantiles.loc[d]
        rrow = next_ret.loc[d]
        for i in range(1, q + 1):
            mask = qrow == i
            vals = rrow[mask.fillna(False)]
            group_ret.loc[d, f'G{i}'] = vals.mean() if len(vals) else np.nan
    group_ret = group_ret.fillna(0.0)
    group_ret['Long-Short'] = group_ret[f'G{q}'] - group_ret['G1']
    group_ret['Long-Only-TopQ'] = group_ret[f'G{q}']
    return quantiles, group_ret



def rebalance_mask(index: pd.DatetimeIndex):
    return index.weekday == 4



def weekly_topn_portfolio(alpha: pd.DataFrame, ret1: pd.DataFrame, top_n: int = 20, cost: float = 0.0015):
    rebalance_dates = alpha.index[rebalance_mask(alpha.index)]
    weights = pd.DataFrame(0.0, index=alpha.index, columns=alpha.columns)
    cost_series = pd.Series(0.0, index=alpha.index)
    turnover = pd.Series(0.0, index=alpha.index)
    prev_w = pd.Series(0.0, index=alpha.columns)
    for i, d in enumerate(rebalance_dates):
        sig = alpha.loc[d].dropna().sort_values(ascending=False)
        picks = sig.head(top_n).index.tolist()
        w = pd.Series(0.0, index=alpha.columns)
        if picks:
            w.loc[picks] = 1.0 / len(picks)
        pos = alpha.index.get_indexer([d])[0]
        start_pos = pos + 1
        end_d = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else alpha.index[-1]
        end_pos = alpha.index.get_indexer([end_d])[0]
        if start_pos < len(alpha.index):
            tv = (w - prev_w).abs().sum()
            weights.iloc[start_pos:end_pos + 1] = w.values
            cost_series.iloc[start_pos] = tv * cost
            turnover.iloc[start_pos] = tv
            prev_w = w
    gross_ret = (weights.shift(1).fillna(0.0) * ret1).sum(axis=1).fillna(0.0)
    ret = gross_ret - cost_series.fillna(0.0)
    return ret, turnover, weights



def monthly_heatmap(ic_df: pd.DataFrame):
    monthly = ic_df.copy()
    monthly['year'] = monthly.index.year
    monthly['month_num'] = monthly.index.month
    heat = monthly.pivot_table(index='year', columns='month_num', values='RankIC', aggfunc='mean').sort_index()
    for m in range(1, 13):
        if m not in heat.columns:
            heat[m] = np.nan
    heat = heat[sorted(heat.columns)]
    return heat



def make_plots(alpha, ic_df, group_ret, port_nav, bench_nav, ls_nav, turnover, coverage, out_dir):
    plt.style.use('seaborn-v0_8-whitegrid')

    factor_sample = alpha.stack().dropna()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={'width_ratios': [2.4, 1]})
    axes[0].hist(factor_sample, bins=60, color='#4472c4', alpha=0.88)
    axes[0].axvline(factor_sample.mean(), color='black', linestyle='--', linewidth=1.2)
    axes[0].set_title('Factor Distribution')
    axes[0].set_xlabel('Standardized factor value')
    axes[0].set_ylabel('Count')
    axes[1].boxplot(factor_sample.values, vert=True, patch_artist=True, boxprops=dict(facecolor='#A9C4EB'))
    axes[1].set_title('Boxplot')
    axes[1].set_xticks([])
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '01_factor_distribution.png'), dpi=180)
    plt.close(fig)

    rankic = ic_df['RankIC'].copy()
    rolling = rankic.rolling(20, min_periods=5).mean()
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(rankic.index, rankic.values, width=2.5, color=np.where(rankic.fillna(0) >= 0, '#70ad47', '#c00000'), alpha=0.55, label='Daily RankIC')
    ax.plot(rolling.index, rolling.values, color='#1f4e79', linewidth=2.0, label='20D Rolling Mean')
    ax.axhline(0, color='black', linewidth=1)
    ax.axhline(rankic.mean(), color='#7f6000', linestyle='--', linewidth=1.4, label='Mean RankIC')
    ax.set_title('RankIC Time Series')
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '02_rankic_timeseries.png'), dpi=180)
    plt.close(fig)

    heat = monthly_heatmap(ic_df)
    arr = heat.values.astype(float)
    masked = np.ma.masked_invalid(arr)
    cmap = plt.cm.RdBu_r.copy()
    cmap.set_bad(color='#d9d9d9')
    vmax = np.nanmax(np.abs(arr)) if np.isfinite(np.nanmax(np.abs(arr))) else 0.1
    vmax = vmax if vmax > 0 else 0.1
    fig, ax = plt.subplots(figsize=(11, 4.8))
    im = ax.imshow(masked, aspect='auto', cmap=cmap, vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(12))
    ax.set_xticklabels([f'M{i}' for i in range(1, 13)])
    ax.set_yticks(range(len(heat.index)))
    ax.set_yticklabels([str(y) for y in heat.index])
    ax.set_title('Monthly RankIC Heatmap')
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if not np.isnan(arr[i, j]):
                ax.text(j, i, f'{arr[i, j]:.02f}', ha='center', va='center', fontsize=8, color='black')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Avg Monthly RankIC')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '03_monthly_rankic_heatmap.png'), dpi=180)
    plt.close(fig)

    q_cols = [c for c in group_ret.columns if c.startswith('G')]
    q_nav = (1 + group_ret[q_cols]).cumprod()
    palette = ['#C00000', '#ED7D31', '#A5A5A5', '#5B9BD5', '#4472C4']
    fig, ax = plt.subplots(figsize=(11, 6))
    for i, c in enumerate(q_cols):
        ax.plot(q_nav.index, q_nav[c], label=c, color=palette[i % len(palette)], linewidth=1.8)
    ax.plot((1 + group_ret['Long-Short']).cumprod().index, (1 + group_ret['Long-Short']).cumprod().values,
            color='black', linestyle='--', linewidth=2.0, label='Long-Short')
    ax.set_title('Quantile Portfolio NAV')
    ax.set_ylabel('NAV')
    ax.legend(ncol=3, loc='upper left')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '04_quantile_nav.png'), dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(port_nav.index, port_nav.values, label='TopN Long-only', linewidth=2.1, color='#1f77b4')
    ax.plot(bench_nav.index, bench_nav.values, label='Benchmark', linewidth=1.9, color='#ff7f0e')
    ax.set_title('Long-only Portfolio vs Benchmark')
    ax.set_ylabel('NAV (start=1)')
    ax.legend(loc='upper left')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '05_long_vs_benchmark_nav.png'), dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.plot(ls_nav.index, ls_nav.values, label='Long-Short', linewidth=2.1, color='#2f5597')
    ax.axhline(1.0, color='black', linewidth=1.0, linestyle='--')
    ax.set_title('Long-Short Portfolio NAV')
    ax.set_ylabel('NAV (start=1)')
    ax.legend(loc='upper left')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '06_long_short_nav.png'), dpi=180)
    plt.close(fig)

    excess_nav = (port_nav / bench_nav).replace([np.inf, -np.inf], np.nan).ffill()
    drawdown = port_nav / port_nav.cummax() - 1
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios': [2.1, 1]})
    axes[0].plot(excess_nav.index, excess_nav.values, color='#4472c4', linewidth=2)
    axes[0].set_title('Excess NAV over Benchmark')
    axes[0].set_ylabel('Excess NAV')
    axes[1].fill_between(drawdown.index, drawdown.values, 0, color='#c00000', alpha=0.28)
    axes[1].plot(drawdown.index, drawdown.values, color='#c00000', linewidth=1.1)
    axes[1].set_title('Portfolio Drawdown')
    axes[1].set_ylabel('Drawdown')
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '07_excess_and_drawdown.png'), dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios': [1.6, 1.2]})
    axes[0].bar(turnover.index, turnover.values, color='#70ad47', width=4)
    axes[0].set_title('Portfolio Turnover')
    axes[0].set_ylabel('Turnover')
    axes[1].plot(coverage.index, coverage.values, color='#7030a0', linewidth=1.8)
    axes[1].set_title('Factor Coverage Ratio')
    axes[1].set_ylabel('Coverage')
    axes[1].set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '08_turnover_and_coverage.png'), dpi=180)
    plt.close(fig)



def image_to_base64(path: str) -> str:
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')



def write_reports(summary, factor_diag, ic_summary, quant_metrics, perf, yearly, out_dir):
    factor_diag_md = markdown_table(
        factor_diag[['指标', '数值']],
        float_pct_cols={'数值'} if False else set(),
        float_num_cols={'数值'}
    )
    ic_summary_md = markdown_table(ic_summary[['指标', '数值']], float_num_cols={'数值'})

    quant_df = quant_metrics.reset_index().rename(columns={'index': '分组'})
    quant_df['累计收益'] = quant_df['累计收益']
    quant_df['年化收益'] = quant_df['年化收益']
    quant_df['年化波动'] = quant_df['年化波动']
    quant_df['Sharpe'] = quant_df['Sharpe']
    quant_df['最大回撤'] = quant_df['最大回撤']
    quant_df = quant_df[['分组', '累计收益', '年化收益', '年化波动', 'Sharpe', '最大回撤']]
    quant_md = markdown_table(quant_df, float_pct_cols={'累计收益', '年化收益', '年化波动', '最大回撤'}, float_num_cols={'Sharpe'})

    perf_df = perf.reset_index().rename(columns={'index': '组合'})
    perf_df['超额年化'] = np.nan
    if '多头组合' in perf.index and '基准' in perf.index:
        perf_df.loc[perf_df['组合'] == '多头组合', '超额年化'] = perf.loc['多头组合', '年化收益'] - perf.loc['基准', '年化收益']
    perf_df = perf_df[['组合', '累计收益', '年化收益', '超额年化', 'Sharpe', '最大回撤', '年化波动', '日胜率', '换手率']]
    perf_md = markdown_table(perf_df, float_pct_cols={'累计收益', '年化收益', '超额年化', '最大回撤', '年化波动', '日胜率', '换手率'}, float_num_cols={'Sharpe'})

    yearly_df = yearly.reset_index()
    yearly_df = yearly_df.rename(columns={yearly_df.columns[0]: '年份'})
    yearly_df['年份'] = yearly_df['年份'].astype(str)
    yearly_md = markdown_table(yearly_df, float_pct_cols={'多头组合', '多空组合', '基准', '超额'})

    image_section_md = []
    for fname in PLOT_FILES:
        image_section_md.append(f'### {fname}')
        image_section_md.append(f'![]({fname})')
        image_section_md.append(CAPTIONS[fname])
        image_section_md.append('')
    image_section_md = '\n'.join(image_section_md)

    report_md = f'''# {REPORT_TITLE}\n\n## 一、研究问题与核心结论\n- 研究问题：{RESEARCH_QUESTION}\n- 因子逻辑：{FACTOR_NARRATIVE}\n- 结论摘要：本框架遵循“因子定义 -> 因子检验 -> 分层回测 -> 组合回测 -> 风险与可实施性”这一金工研报主线，并自动输出图表化结果。\n\n## 二、因子构建与经济含义\n- 最小可运行表达式：`rank(-ret_5) + 0.5 * rank(volume / mean(volume, 20) - 1) - 0.5 * rank(std(ret_1, 20))`\n- 预处理：横截面去极值、标准化。\n- 经济含义：结合短期反转、量能冲击与波动惩罚，观察资金博弈后的横截面收益差异。\n\n## 三、样本与回测设定\n- 候选池说明：{UNIVERSE_NOTE}\n- 目标下载股票数：{summary['target_download_stocks']}\n- 实际成功下载股票数：{summary['actual_download_stocks']}\n- 下载失败或历史长度不足数量：{summary['failed_or_short_history']}\n- 回测区间：{summary['date_start']} 至 {summary['date_end']}\n- 调仓频率：周频\n- 持仓数：Top {TOP_N}\n- 分组数：{QUANTILES}\n- 基准：{BENCHMARK}\n- 成本假设：单边 {TCOST_ONE_WAY:.2%}\n\n## 四、因子诊断\n{factor_diag_md}\n\n## 五、因子有效性\n{ic_summary_md}\n\n## 六、分层回测结果\n{quant_md}\n\n## 七、组合绩效汇总\n{perf_md}\n\n## 八、分年收益\n{yearly_md}\n\n## 九、图表展示\n{image_section_md}\n\n## 十、复现偏差说明\n- 当前脚本默认使用公开可获取行情源与指数成分股并集，和研报正式数据库口径可能存在差异。\n- 若要严格复现A股金工研报，需进一步补充ST、停牌、涨跌停、上市天数、行业中性化、流通市值中性化和成交约束。\n- 若研究属于“市场热点追踪型”而非“纯因子定价型”，则应改为“指数/行业/概念/个股分层统计 + 规则筛选结果展示”，而不应强行套用多空回测。\n\n## 十一、对话推送摘要\n1. 先说研究问题与原研报主结论。\n2. 再说因子/信号定义与经济解释。\n3. 再说样本、过滤规则、下载股票数。\n4. 再展示IC、分层、组合、回撤。\n5. 最后说明与原研报不一致之处。\n'''

    with open(os.path.join(out_dir, 'report.md'), 'w', encoding='utf-8') as f:
        f.write(report_md)

    image_blocks = []
    for fname in PLOT_FILES:
        img64 = image_to_base64(os.path.join(out_dir, fname))
        image_blocks.append(f"<h3>{fname}</h3><img src='data:image/png;base64,{img64}' style='max-width:100%;border:1px solid #ddd;border-radius:8px'/><p>{CAPTIONS[fname]}</p>")

    report_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<title>{REPORT_TITLE}</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; line-height: 1.6; margin: 28px auto; max-width: 1100px; color: #222; }}
h1, h2, h3 {{ color: #1f4e79; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0 20px 0; }}
th, td {{ border: 1px solid #d9d9d9; padding: 8px 10px; text-align: right; }}
th:first-child, td:first-child {{ text-align: left; }}
.card {{ background: #f8fbff; border: 1px solid #dbe5f1; border-radius: 10px; padding: 14px 18px; margin: 12px 0; }}
.small {{ color: #666; font-size: 13px; }}
</style>
</head>
<body>
<h1>{REPORT_TITLE}</h1>
<div class="card">
<h2>研究问题与核心结论</h2>
<p><b>研究问题：</b>{RESEARCH_QUESTION}</p>
<p><b>因子逻辑：</b>{FACTOR_NARRATIVE}</p>
<p>本报告自动按照金工研报的典型展示链路输出：因子定义、有效性检验、分层收益、组合回测、风险与可实施性。</p>
</div>
<div class="card">
<h2>样本与回测设定</h2>
<ul>
<li>目标下载股票数：{summary['target_download_stocks']}</li>
<li>实际成功下载股票数：{summary['actual_download_stocks']}</li>
<li>下载失败或历史长度不足数量：{summary['failed_or_short_history']}</li>
<li>回测区间：{summary['date_start']} 至 {summary['date_end']}</li>
<li>调仓频率：周频</li>
<li>持仓数：Top {TOP_N}</li>
<li>分组数：{QUANTILES}</li>
<li>基准：{BENCHMARK}</li>
<li>成本假设：单边 {TCOST_ONE_WAY:.2%}</li>
</ul>
<p class="small">候选池说明：{UNIVERSE_NOTE}</p>
</div>
<div class="card">
<h2>图表展示</h2>
{''.join(image_blocks)}
</div>
</body>
</html>'''

    with open(os.path.join(out_dir, 'report.html'), 'w', encoding='utf-8') as f:
        f.write(report_html)

    conversation_push = f'''# 对话推送模板\n\n## 1. 研究问题与原研报主结论\n本次复现围绕“{RESEARCH_QUESTION}”展开，先明确原研报研究的是市场现象还是因子定价问题，再给出一句话主结论。\n\n## 2. 因子/信号定义与经济解释\n- 因子逻辑：{FACTOR_NARRATIVE}\n- 最小表达式：rank(-ret_5) + 0.5 * rank(volume / mean(volume, 20) - 1) - 0.5 * rank(std(ret_1, 20))\n- 解释该因子为什么可能有效。\n\n## 3. 样本与回测设定\n- 目标下载股票数：{summary['target_download_stocks']}\n- 实际成功下载股票数：{summary['actual_download_stocks']}\n- 持仓数：Top {TOP_N}\n- 回测区间：{summary['date_start']} 至 {summary['date_end']}\n- 基准：{BENCHMARK}\n\n## 4. 因子有效性\n- RankIC均值：{format_num(ic_summary.loc[ic_summary['指标']=='RankIC均值', '数值'].iloc[0]) if 'RankIC均值' in ic_summary['指标'].values else '-'}\n- 月度IC胜率：{format_pct(ic_summary.loc[ic_summary['指标']=='月度IC胜率', '数值'].iloc[0]) if '月度IC胜率' in ic_summary['指标'].values else '-'}\n\n## 5. 组合结果\n- 多头组合年化收益：{format_pct(perf.loc['多头组合', '年化收益']) if '多头组合' in perf.index else '-'}\n- 多头组合最大回撤：{format_pct(perf.loc['多头组合', '最大回撤']) if '多头组合' in perf.index else '-'}\n- 相对基准超额年化：{format_pct((perf.loc['多头组合', '年化收益'] - perf.loc['基准', '年化收益']) if {'多头组合','基准'}.issubset(set(perf.index)) else np.nan)}\n\n## 6. 风险与偏差\n说明数据口径、股票池、交易约束、是否为代理复现。\n\n## 7. 图片展示顺序\n按以下顺序逐张展示：\n{os.linesep.join([f'- {x}: {CAPTIONS[x]}' for x in PLOT_FILES])}\n'''

    with open(os.path.join(out_dir, 'conversation_push.md'), 'w', encoding='utf-8') as f:
        f.write(conversation_push)



def main():
    tickers = get_universe(TARGET_DOWNLOAD_STOCKS)
    close, volume, failed = download_panel(tickers)
    if close.shape[1] < max(TOP_N * 3, 30):
        raise RuntimeError(f'usable universe too small: {close.shape[1]}')

    alpha, ret1 = build_factor(close, volume)
    next_ret = close.pct_change().shift(-1)
    ic_df = calc_ic(alpha, next_ret)
    _, group_ret = quantile_backtest(alpha, next_ret, q=QUANTILES)
    port_ret, turnover, weights = weekly_topn_portfolio(alpha, ret1, top_n=TOP_N, cost=TCOST_ONE_WAY)
    port_nav = (1 + port_ret.fillna(0)).cumprod()

    bench = yf.download(BENCHMARK, start=START, end=END, auto_adjust=True, progress=False, threads=False)
    bench_close = bench['Close'].iloc[:, 0] if isinstance(bench.columns, pd.MultiIndex) else bench['Close']
    bench_ret = pd.Series(bench_close).pct_change().reindex(port_nav.index).fillna(0.0)
    bench_nav = (1 + bench_ret).cumprod()
    ls_ret = group_ret['Long-Short'].reindex(port_nav.index).fillna(0.0)
    ls_nav = (1 + ls_ret).cumprod()
    coverage = alpha.notna().mean(axis=1).reindex(port_nav.index).fillna(method='ffill').fillna(0.0)

    factor_diag = pd.DataFrame({
        '指标': ['因子覆盖率', '缺失率', '因子均值', '因子标准差', '偏度', '峰度'],
        '数值': [
            alpha.notna().mean().mean(),
            alpha.isna().mean().mean(),
            alpha.stack().mean(),
            alpha.stack().std(),
            alpha.stack().skew(),
            alpha.stack().kurt(),
        ]
    })

    rankic_std = ic_df['RankIC'].std()
    rankic_mean = ic_df['RankIC'].mean()
    long_short_t = group_ret['Long-Short'].mean() / group_ret['Long-Short'].std() * np.sqrt(len(group_ret)) if group_ret['Long-Short'].std() and len(group_ret) > 10 else np.nan
    monotonic = '是' if group_ret[[f'G{i}' for i in range(1, QUANTILES + 1)]].mean().is_monotonic_increasing else '否'
    ic_summary = pd.DataFrame({
        '指标': ['IC均值', 'RankIC均值', 'ICIR', '月度IC胜率', '多空单调性', 'Long-Short t统计量'],
        '数值': [
            ic_df['IC'].mean(),
            rankic_mean,
            rankic_mean / rankic_std if rankic_std and not pd.isna(rankic_std) else np.nan,
            (ic_df['RankIC'] > 0).mean(),
            monotonic,
            long_short_t,
        ]
    })

    quant_metrics = []
    for c in [f'G{i}' for i in range(1, QUANTILES + 1)] + ['Long-Short']:
        m = calc_metrics(group_ret[c])
        m['分组'] = c
        quant_metrics.append(m)
    quant_metrics = pd.DataFrame(quant_metrics).set_index('分组')

    perf = pd.DataFrame([
        {'组合': '多头组合', **calc_metrics(port_ret), '换手率': turnover.mean()},
        {'组合': '多空组合', **calc_metrics(ls_ret), '换手率': np.nan},
        {'组合': '基准', **calc_metrics(bench_ret), '换手率': np.nan},
    ]).set_index('组合')

    yearly = pd.DataFrame({'多头组合': port_ret, '多空组合': ls_ret, '基准': bench_ret})
    yearly = yearly.groupby(yearly.index.year).apply(lambda x: (1 + x).prod() - 1)
    yearly['超额'] = yearly['多头组合'] - yearly['基准']

    factor_diag.to_csv(os.path.join(OUT_DIR, 'factor_diagnostics.csv'), index=False, encoding='utf-8-sig')
    ic_df.to_csv(os.path.join(OUT_DIR, 'ic_series.csv'), encoding='utf-8-sig')
    ic_summary.to_csv(os.path.join(OUT_DIR, 'ic_summary.csv'), index=False, encoding='utf-8-sig')
    quant_metrics.to_csv(os.path.join(OUT_DIR, 'quantile_metrics.csv'), encoding='utf-8-sig')
    perf.to_csv(os.path.join(OUT_DIR, 'performance_summary.csv'), encoding='utf-8-sig')
    yearly.to_csv(os.path.join(OUT_DIR, 'yearly_returns.csv'), encoding='utf-8-sig')

    run_summary = {
        'target_download_stocks': TARGET_DOWNLOAD_STOCKS,
        'actual_download_stocks': int(close.shape[1]),
        'failed_or_short_history': int(len(set(failed))),
        'date_start': str(close.index.min().date()),
        'date_end': str(close.index.max().date()),
        'benchmark': BENCHMARK,
        'top_n': TOP_N,
        'quantiles': QUANTILES,
        'transaction_cost_one_way': TCOST_ONE_WAY,
    }
    with open(os.path.join(OUT_DIR, 'run_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(run_summary, f, ensure_ascii=False, indent=2)

    make_plots(alpha, ic_df, group_ret, port_nav, bench_nav, ls_nav, turnover, coverage, OUT_DIR)
    write_reports(run_summary, factor_diag, ic_summary, quant_metrics, perf, yearly, OUT_DIR)

    print('TARGET_DOWNLOAD_STOCKS', TARGET_DOWNLOAD_STOCKS)
    print('ACTUAL_DOWNLOAD_STOCKS', close.shape[1])
    print('FAILED_OR_SHORT_HISTORY', len(set(failed)))
    print('OUTPUT_DIR', OUT_DIR)


if __name__ == '__main__':
    main()
