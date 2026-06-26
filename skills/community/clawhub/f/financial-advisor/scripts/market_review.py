#!/usr/bin/env python3
"""
大盘复盘工具
生成主要指数、市场概况、板块表现的报告（支持 Markdown / JSON 输出）
数据源：腾讯财经 API（A股/港股）→ yfinance 兜底（美股/全球）
无 akshare 硬依赖
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install requests pandas numpy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    import akshare as ak
except ImportError:
    ak = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'http://stock.finance.qq.com/'
}


# ─────────────────────── 腾讯 API 工具函数 ───────────────────────

def _tencent_kline(tc_code, is_hk, count=5):
    """腾讯财经 K 线接口，返回 DataFrame 或 None"""
    base = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get" if is_hk \
        else "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    url = f"{base}?param={tc_code},day,,,{count},qfq"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        data = resp.json()
        if data.get('code') != 0:
            return None
        stock_data = data.get('data', {}).get(tc_code)
        if not stock_data:
            return None
        klines = None
        for key in ('qfqday', 'day'):
            if key in stock_data and stock_data[key]:
                klines = stock_data[key]
                break
        if not klines:
            return None
        rows = []
        for item in klines:
            h, l = float(item[3]), float(item[4])
            rows.append({
                'Date': item[0],
                'Open': float(item[1]),
                'Close': float(item[2]),
                'High': max(h, l),
                'Low': min(h, l),
                'Volume': float(item[5]),
            })
        df = pd.DataFrame(rows)
        df['Change_Pct'] = df['Close'].pct_change().fillna(0) * 100
        return df
    except Exception as e:
        logger.debug(f"腾讯 K 线 {tc_code} 失败: {e}")
        return None


def _tencent_realtime_batch(codes):
    """
    腾讯实时行情批量接口
    codes: list of tencent code strings like ['sh000001', 'sz399001']
    返回 {tc_code: {price, change_pct, ...}}
    """
    if not codes:
        return {}
    url = f"http://qt.gtimg.cn/q={','.join(codes)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.encoding = 'gbk'
        results = {}
        for line in resp.text.strip().split('\n'):
            if '~' not in line:
                continue
            # 提取 code 和字段
            eq_pos = line.find('="')
            if eq_pos < 0:
                continue
            var_part = line[:eq_pos]
            tc_code = var_part.split('_')[-1] if '_' in var_part else ''
            fields = line[eq_pos + 2:].rstrip('";').split('~')
            if len(fields) < 46:
                continue
            try:
                results[tc_code] = {
                    'name': fields[1],
                    'code': fields[2],
                    'price': float(fields[3]) if fields[3] else 0,
                    'yesterday_close': float(fields[4]) if fields[4] else 0,
                    'open': float(fields[5]) if fields[5] else 0,
                    'volume': float(fields[6]) if fields[6] else 0,
                    'high': float(fields[33]) if fields[33] else 0,
                    'low': float(fields[34]) if fields[34] else 0,
                    'change_pct': float(fields[32]) if fields[32] else 0,
                    'change': float(fields[31]) if fields[31] else 0,
                    'amount': float(fields[37]) if fields[37] else 0,
                    'turnover': float(fields[38]) if fields[38] else 0,
                }
            except (ValueError, IndexError):
                continue
        return results
    except Exception as e:
        logger.debug(f"腾讯批量行情失败: {e}")
        return {}


# ─────────────────────── 指数配置 ───────────────────────

INDICES_CONFIG = {
    'cn': [
        {'tc_code': 'sh000001', 'name': '上证指数', 'is_hk': False},
        {'tc_code': 'sz399001', 'name': '深证成指', 'is_hk': False},
        {'tc_code': 'sz399006', 'name': '创业板指', 'is_hk': False},
        {'tc_code': 'sh000688', 'name': '科创50', 'is_hk': False},
    ],
    'hk': [
        {'tc_code': 'hkHSI',    'name': '恒生指数', 'is_hk': True},
        {'tc_code': 'hkHSCEI',  'name': '国企指数', 'is_hk': True},
        {'tc_code': 'hkHSTECH', 'name': '恒生科技', 'is_hk': True},
    ],
    'us': [
        {'yf_code': '^GSPC',  'name': '标普500'},
        {'yf_code': '^DJI',   'name': '道琼斯'},
        {'yf_code': '^IXIC',  'name': '纳斯达克'},
    ],
}


# ─────────────────────── 获取指数 ───────────────────────

def get_main_indices(region='cn'):
    """获取主要指数数据，返回 list[dict]"""
    config = INDICES_CONFIG.get(region, [])
    if not config:
        return []

    # 美股 → yfinance
    if region == 'us':
        return _get_indices_yfinance(config)

    # A 股 / 港股 → 腾讯实时批量接口
    indices = _get_indices_tencent_realtime(config)
    if indices:
        return indices

    # 腾讯实时接口失败 → 逐个 K 线兜底
    indices = _get_indices_tencent_kline(config)
    if indices:
        return indices

    # 最终兜底 → akshare（仅 A 股）
    if region == 'cn' and ak:
        return _get_indices_akshare_cn()

    return []


def _get_indices_tencent_realtime(config):
    """腾讯实时批量接口获取指数"""
    tc_codes = [c['tc_code'] for c in config]
    batch = _tencent_realtime_batch(tc_codes)
    if not batch:
        return []
    indices = []
    for conf in config:
        info = batch.get(conf['tc_code'])
        if info and info['price'] > 0:
            indices.append({
                'name': conf['name'],
                'code': conf['tc_code'],
                'price': info['price'],
                'change_pct': info['change_pct'],
                'change': info['change'],
                'volume': info['volume'],
                'source': 'tencent_realtime',
            })
    return indices


def _get_indices_tencent_kline(config):
    """腾讯 K 线接口逐个获取"""
    indices = []
    for conf in config:
        df = _tencent_kline(conf['tc_code'], conf.get('is_hk', False), count=5)
        if df is not None and not df.empty:
            row = df.iloc[-1]
            prev_close = df.iloc[-2]['Close'] if len(df) >= 2 else row['Open']
            change = row['Close'] - prev_close
            change_pct = (change / prev_close * 100) if prev_close else 0
            indices.append({
                'name': conf['name'],
                'code': conf['tc_code'],
                'price': row['Close'],
                'change_pct': round(change_pct, 2),
                'change': round(change, 2),
                'volume': row['Volume'],
                'source': 'tencent_kline',
            })
        time.sleep(0.3)
    return indices


def _get_indices_akshare_cn():
    """akshare 兜底获取 A 股指数"""
    try:
        df = ak.stock_zh_index_spot_em()
        mapping = {'000001': '上证指数', '399001': '深证成指', '399006': '创业板指'}
        indices = []
        for code, name in mapping.items():
            row = df[df['代码'] == code]
            if not row.empty:
                r = row.iloc[0]
                indices.append({
                    'name': name,
                    'code': code,
                    'price': float(r['最新价']),
                    'change_pct': float(r['涨跌幅']),
                    'change': float(r.get('涨跌额', 0)),
                    'volume': float(r.get('成交量', 0)),
                    'source': 'akshare',
                })
        return indices
    except Exception as e:
        logger.warning(f"akshare 获取 A 股指数失败: {e}")
        return []


def _get_indices_yfinance(config):
    """yfinance 获取指数（美股）"""
    if yf is None:
        logger.warning("yfinance 未安装，无法获取美股指数")
        return []
    indices = []
    for conf in config:
        try:
            ticker = yf.Ticker(conf['yf_code'])
            hist = ticker.history(period='5d')
            if hist.empty:
                continue
            price = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) >= 2 else price
            change = price - prev
            change_pct = (change / prev * 100) if prev else 0
            indices.append({
                'name': conf['name'],
                'code': conf['yf_code'],
                'price': round(float(price), 2),
                'change_pct': round(float(change_pct), 2),
                'change': round(float(change), 2),
                'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                'source': 'yfinance',
            })
        except Exception as e:
            logger.warning(f"yfinance 获取 {conf['name']} 失败: {e}")
        time.sleep(0.5)
    return indices


# ─────────────────────── 市场统计 ───────────────────────

def get_market_stats(region='cn'):
    """获取市场涨跌统计（仅 A 股支持）"""
    if region != 'cn':
        return {}

    # 优先 akshare
    if ak:
        try:
            df = ak.stock_zh_a_spot_em()
            up_count = int((df['涨跌幅'] > 0).sum())
            down_count = int((df['涨跌幅'] < 0).sum())
            flat_count = int((df['涨跌幅'] == 0).sum())
            limit_up = int((df['涨跌幅'] >= 9.9).sum())
            limit_down = int((df['涨跌幅'] <= -9.9).sum())
            return {
                'up_count': up_count,
                'down_count': down_count,
                'flat_count': flat_count,
                'limit_up': limit_up,
                'limit_down': limit_down,
                'total': len(df),
                'source': 'akshare',
            }
        except Exception as e:
            logger.warning(f"akshare 获取市场统计失败: {e}")

    # 无 akshare 或失败 → 返回空（腾讯 API 无全市场统计接口）
    return {}


# ─────────────────────── 板块排行 ───────────────────────

def get_sector_rankings(n=5):
    """获取板块排行（仅 A 股，依赖 akshare）"""
    if not ak:
        return [], []
    try:
        df = ak.stock_board_industry_name_em()
        top_gainers = df.nlargest(n, '涨跌幅')
        top_losers = df.nsmallest(n, '涨跌幅')
        gainers = [
            {'name': row['板块名称'], 'change_pct': float(row['涨跌幅'])}
            for _, row in top_gainers.iterrows()
        ]
        losers = [
            {'name': row['板块名称'], 'change_pct': float(row['涨跌幅'])}
            for _, row in top_losers.iterrows()
        ]
        return gainers, losers
    except Exception as e:
        logger.warning(f"获取板块排行失败: {e}")
        return [], []


# ─────────────────────── 报告生成 ───────────────────────

REGION_LABEL = {'cn': 'A股', 'hk': '港股', 'us': '美股'}


def generate_market_review(region='cn'):
    """生成大盘复盘数据（dict），可序列化为 JSON 或 Markdown"""
    label = REGION_LABEL.get(region, region)
    logger.info(f"开始生成大盘复盘（区域: {label}）...")

    indices = get_main_indices(region)
    stats = get_market_stats(region)
    top_gainers, top_losers = (get_sector_rankings(n=5) if region == 'cn' else ([], []))

    review = {
        'region': region,
        'region_label': label,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'indices': indices,
        'market_stats': stats,
        'top_gainers': top_gainers,
        'top_losers': top_losers,
    }
    return review


def review_to_markdown(review):
    """将复盘 dict 转换为 Markdown"""
    md = f"""# 🎯 {review['date']} 大盘复盘

**区域**: {review['region_label']}  
**生成时间**: {review['generated_at']}

---

## 📊 主要指数

"""
    for idx in review['indices']:
        emoji = '🟢' if idx['change_pct'] > 0 else '🔴' if idx['change_pct'] < 0 else '⚪'
        md += f"- **{idx['name']}**: {idx['price']:.2f} ({emoji}{idx['change_pct']:+.2f}%)\n"

    md += "\n---\n\n## 📈 市场概况\n\n"
    stats = review.get('market_stats', {})
    if stats:
        md += f"""- **上涨**: {stats['up_count']} | **下跌**: {stats['down_count']} | **平盘**: {stats['flat_count']}
- **涨停**: {stats['limit_up']} | **跌停**: {stats['limit_down']}
- **总股票数**: {stats['total']}
"""
    else:
        md += "暂无市场统计数据\n"

    md += "\n---\n\n## 🔥 板块表现\n\n"
    if review.get('top_gainers'):
        md += "### 领涨板块\n\n"
        for s in review['top_gainers']:
            md += f"- {s['name']}: {s['change_pct']:+.2f}%\n"
        md += "\n"
    if review.get('top_losers'):
        md += "### 领跌板块\n\n"
        for s in review['top_losers']:
            md += f"- {s['name']}: {s['change_pct']:+.2f}%\n"
        md += "\n"

    md += f"""---

## 💡 数据来源

"""
    sources = set(idx.get('source', 'unknown') for idx in review['indices'])
    for src in sorted(sources):
        md += f"- {src}\n"

    md += f"\n**生成时间**: {review['generated_at']}\n"
    return md


def generate_multi_region_review(regions):
    """生成多区域复盘（合并结果）"""
    all_reviews = []
    for region in regions:
        review = generate_market_review(region)
        all_reviews.append(review)
    return all_reviews


# ─────────────────────── 主入口 ───────────────────────

def main():
    parser = argparse.ArgumentParser(description='大盘复盘工具（支持 A股/港股/美股）')
    parser.add_argument('--region', default='cn', choices=['cn', 'hk', 'us', 'all'],
                        help='市场区域：cn=A股, hk=港股, us=美股, all=全部')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', default='json', choices=['json', 'md', 'markdown'],
                        help='输出格式：json 或 md/markdown')
    args = parser.parse_args()

    # 确定要采集的区域
    if args.region == 'all':
        regions = ['cn', 'hk', 'us']
    else:
        regions = [args.region]

    # 生成复盘数据
    reviews = []
    for region in regions:
        review = generate_market_review(region)
        reviews.append(review)

    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fmt = args.format.lower()
    if fmt == 'json':
        # JSON 输出：单区域返回 dict，多区域返回 list
        output_data = reviews[0] if len(reviews) == 1 else reviews
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
    else:
        # Markdown 输出
        md_parts = [review_to_markdown(r) for r in reviews]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(md_parts))

    # 输出摘要到 stdout
    for review in reviews:
        label = review['region_label']
        idx_count = len(review['indices'])
        logger.info(f"[{label}] 获取到 {idx_count} 个指数")
        for idx in review['indices']:
            emoji = '🟢' if idx['change_pct'] > 0 else '🔴' if idx['change_pct'] < 0 else '⚪'
            logger.info(f"  {idx['name']}: {idx['price']:.2f} ({emoji}{idx['change_pct']:+.2f}%) [{idx.get('source', '')}]")

    logger.info("=" * 60)
    logger.info(f"✅ 大盘复盘已生成: {output_path}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
