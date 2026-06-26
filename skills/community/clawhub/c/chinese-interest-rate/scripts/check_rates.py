#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Interest Rate Monitor - Rate Check Script (v2.0)

真实抓取中国利率数据，对比历史，有变化则输出通知。

⚠️ 本脚本可独立运行，真正从网络抓取数据。
⚠️ 不需要外部 agent 喂数据。
⚠️ 抓取失败时使用上次保存的数据（不发送错误通知）。

使用方式：
  python check_rates.py           # 独立运行：抓取 + 对比 + 通知
  python check_rates.py '{"LPR":{"1year":"3.45"}}'  # agent 传入数据时
"""

import json
import sys
import os
import re
import time
import urllib.request
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/rates.json')

# ========== 网络抓取 ==========

def fetch_url(url, timeout=10):
    """抓取 URL 内容，失败返回 None"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Python/3)',
            'Accept': 'text/html,application/json',
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"[WARN] Fetch failed for {url}: {e}", file=sys.stderr)
        return None

def fetch_yahoo_china_bond():
    """从 Yahoo Finance 抓取中国国债收益率"""
    results = {}
    tickers = {
        'CN10Y=X': '10year',
        'CN2Y=X': '3year',
        'CN1Y=X': '1year',
    }
    for ticker, label in tickers.items():
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
        try:
            data = fetch_url(url)
            if data:
                import json as _json
                d = _json.loads(data)
                meta = d.get('chart', {}).get('result', [{}])[0]
                meta_data = meta.get('meta', {})
                rate = meta_data.get('regularMarketPrice')
                if rate:
                    results[f'bond_{label}'] = f"{float(rate):.3f}"
                    print(f"[OK] {ticker} = {rate}")
        except Exception as e:
            print(f"[WARN] Failed to parse {ticker}: {e}", file=sys.stderr)
    return results

def fetch_shibor():
    """从上海银行间同业拆借中心抓取 SHIBOR"""
    results = {}
    # 尝试多个数据源
    urls = [
        ('https://www.shibor.org/shibor/web-htmls/shibor.html', 'shibor'),
        ('https://www.chinamoney.com.cn/ags/ms/cm-u-bond-shibor/Shibor', 'shibor2'),
    ]
    for url, name in urls:
        content = fetch_url(url)
        if not content:
            continue
        # 尝试从 HTML 中提取 SHIBOR 数据
        patterns = {
            'ON': [r'O/N.*?(\d+\.?\d*)', r'隔夜.*?(\d+\.?\d*)'],
            '1W': [r'1W.*?(\d+\.?\d*)', r'1周.*?(\d+\.?\d*)'],
            '1M': [r'1M.*?(\d+\.?\d*)', r'1月.*?(\d+\.?\d*)'],
            '3M': [r'3M.*?(\d+\.?\d*)', r'3月.*?(\d+\.?\d*)'],
        }
        for tenor, pats in patterns.items():
            for pat in pats:
                m = re.search(pat, content, re.IGNORECASE)
                if m:
                    val = m.group(1)
                    results[f'SHIBOR_{tenor}'] = val
                    print(f"[OK] SHIBOR {tenor} = {val}")
                    break
        if results:
            break
    return results

def fetch_pbc_lpr():
    """从中国人民银行网站抓取 LPR（备用：使用 Yahoo Finance）"""
    # Yahoo Finance 有 LPR 相关数据
    results = {}
    # CNLPR1Y=X 是 1年期 LPR
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/CNLPR1Y%3DX'
    data = fetch_url(url)
    if data:
        try:
            import json as _json
            d = _json.loads(data)
            rate = d.get('chart', {}).get('result', [{}])[0].get('meta', {}).get('regularMarketPrice')
            if rate:
                results['LPR_1Y'] = f"{float(rate):.3f}"
                print(f"[OK] LPR 1Y = {rate}")
        except Exception as e:
            print(f"[WARN] Failed CNLPR1Y: {e}", file=sys.stderr)
    return results

def fetch_all_rates():
    """
    抓取所有利率数据
    ⚠️ 网络抓取可能有失败，返回已成功抓取的数据
    """
    all_rates = {}
    
    print(f"[INFO] Fetching China interest rates at {datetime.now().strftime('%Y-%m-%d %H:%M')}...")
    
    # 国债收益率（Yahoo Finance）
    print("[INFO] Fetching China bond yields...")
    bond_data = fetch_yahoo_china_bond()
    all_rates.update(bond_data)
    time.sleep(1)
    
    # SHIBOR
    print("[INFO] Fetching SHIBOR...")
    shibor_data = fetch_shibor()
    all_rates.update(shibor_data)
    time.sleep(1)
    
    # LPR
    print("[INFO] Fetching LPR...")
    lpr_data = fetch_pbc_lpr()
    all_rates.update(lpr_data)
    
    print(f"[INFO] Fetch complete. Got {len(all_rates)} rate(s).")
    return all_rates

# ========== 数据存储 ==========

def load_current_rates():
    """从文件加载历史利率数据"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_rates(data):
    """保存利率数据到文件"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== 对比逻辑 ==========

def compare_and_format(old_data, new_rates):
    """对比新旧数据，返回变化列表"""
    changes = []
    
    # 映射表
    field_map = {
        'bond_10year': ('bondYields', '10year'),
        'bond_3year': ('bondYields', '3year'),
        'bond_1year': ('bondYields', '1year'),
        'SHIBOR_ON': ('SHIBOR', 'ON'),
        'SHIBOR_1W': ('SHIBOR', '1W'),
        'SHIBOR_1M': ('SHIBOR', '1M'),
        'SHIBOR_3M': ('SHIBOR', '3M'),
        'LPR_1Y': ('LPR', '1year'),
    }
    
    for key, new_val in new_rates.items():
        if key not in field_map:
            continue
        cat, sub_key = field_map[key]
        if cat not in old_data:
            old_data[cat] = {}
        old_val = old_data[cat].get(sub_key, '')
        
        if not old_val:
            # 首次抓取，不算变化
            continue
        
        if old_val == new_val:
            continue
        
        try:
            diff = float(new_val) - float(old_val)
            diff_bp = round(diff * 100, 1)
            changes.append({
                'category': cat,
                'key': sub_key,
                'old': old_val,
                'new': new_val,
                'diff': f"{diff:+.3f}% ({diff_bp:+.0f}bp)"
            })
        except (ValueError, TypeError):
            pass
    
    return changes

def format_notification(changes, new_rates, today):
    """格式化通知（中英双语）"""
    msg = f"📊 中国利率变动日报 | {today}\n\n"
    
    by_cat = {}
    for c in changes:
        by_cat.setdefault(c['category'], []).append(c)
    
    labels = {
        'bondYields': {'10year': '🏦 10年期国债', '3year': '🏦 3年期国债', '1year': '🏦 1年期国债'},
        'SHIBOR': {'ON': '💧 SHIBOR隔夜(O/N)', '1W': '💧 SHIBOR 1周', '1M': '💧 SHIBOR 1月', '3M': '💧 SHIBOR 3月'},
        'LPR': {'1year': '📊 LPR 1年期', '5yearPlus': '📊 LPR 5年期以上'},
    }
    
    for cat, items in by_cat.items():
        for c in items:
            label_map = labels.get(cat, {})
            label = label_map.get(c['key'], f"{cat}.{c['key']}")
            msg += f"- {label}: {c['new']}% ({c['diff']})\n"
        msg += "\n"
    
    msg += "━━━━━━━━━━━━━━━━━━━━\n"
    msg += "⚠️ 利率变动可能影响房贷月供和理财收益，请关注。\n"
    msg += "数据来源：Yahoo Finance / 中国人民银行\n"
    msg += "⚠️ Disclaimer: Data for reference only, not financial advice.\n"
    
    return msg

# ========== 主程序 ==========

def main():
    """
    支持两种运行模式：
    1. 无参数：独立抓取 + 对比 + 通知
    2. 有 JSON 参数：对比传入数据 + 通知
    """
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    old_data = load_current_rates()
    
    # 有参数：从 agent 传入数据
    if len(sys.argv) > 1 and sys.argv[1].strip():
        try:
            agent_data = json.loads(sys.argv[1])
            # agent 传入的格式可能与本地格式不同，转换一下
            new_rates = {}
            for cat, fields in agent_data.items():
                if isinstance(fields, dict):
                    for k, v in fields.items():
                        new_rates[f"{cat}_{k}"] = v
            print(f"[INFO] Using agent-supplied data: {len(new_rates)} rates")
        except Exception as e:
            print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
            new_rates = {}
    else:
        # 无参数：自己抓取
        new_rates = fetch_all_rates()
    
    if not new_rates:
        print("[WARN] No rate data available. Skipping.")
        sys.exit(0)
    
    # 对比变化
    changes = compare_and_format(old_data, new_rates)
    
    # 构建新数据
    new_data = old_data.copy()
    new_data['updateDate'] = today
    
    # 合并新抓取的数据
    field_map = {
        'bond_10year': ('bondYields', '10year'),
        'bond_3year': ('bondYields', '3year'),
        'bond_1year': ('bondYields', '1year'),
        'SHIBOR_ON': ('SHIBOR', 'ON'),
        'SHIBOR_1W': ('SHIBOR', '1W'),
        'SHIBOR_1M': ('SHIBOR', '1M'),
        'SHIBOR_3M': ('SHIBOR', '3M'),
        'LPR_1Y': ('LPR', '1year'),
    }
    for key, val in new_rates.items():
        if key in field_map:
            cat, sub = field_map[key]
            new_data.setdefault(cat, {})[sub] = val
    
    # 有变化则输出通知
    if changes:
        notification = format_notification(changes, new_rates, today)
        print("[NOTIFY]")
        print(notification)
        print("[/NOTIFY]")
        print(f"[OK] {len(changes)} rate(s) changed. Data saved.")
    else:
        print("[OK] No changes detected. Data saved.")
    
    # 保存
    save_rates(new_data)

if __name__ == '__main__':
    main()
