#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺数据接口 v2
官方免费接口，测试时间: 2026-04-05

正确接口路径（已验证）：
  - 实时/五档: /v2/realhead/hs_{code}/last.js
  - 分时日K:   /v6/line/hs_{code}/01/last.js
  - 1分钟K:    /v6/line/hs_{code}/11/last.js
  - 五档盘口:  /v2/fiverange/hs_{code}/last.js
  - 资金流向:  /v2/moneyflow/hs_{code}/last.js

关键：必须先建立会话（访问 https://stockpage.10jqka.com.cn/{code}/）
否则分日和日K接口返回404。
"""

import requests
import re
import json
from typing import List, Optional, Dict

# 全局会话（保持Cookie）
_session = None

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": "https://stockpage.10jqka.com.cn/",
    "Accept": "application/javascript, */*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def _get_session():
    """获取或创建共享会话（自动建立同花顺Cookie）"""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(HEADERS)
    return _session


def _ensure_session(code: str):
    """确保会话已建立（首次调用时访问股票页面以建立Cookie）"""
    _get_session()
    # 访问股票页面以建立Cookie
    _session.get(f"https://stockpage.10jqka.com.cn/{code}/", timeout=10)


def _parse_jsonp(text: str) -> dict:
    """解析JSONP格式响应"""
    if not text:
        return {}
    m = re.search(r'\((\{.*\})\)', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return {}


def _parse_records(records_str: str) -> List[dict]:
    """将分号分隔的字符串解析为记录列表"""
    if not records_str:
        return []
    records = []
    for row in records_str.split(';'):
        row = row.strip()
        if not row:
            continue
        parts = row.split(',')
        if len(parts) < 6:
            continue
        try:
            records.append({
                'date': parts[0],
                'open': float(parts[1]),
                'high': float(parts[2]),
                'low': float(parts[3]),
                'close': float(parts[4]),
                'volume': float(parts[5]),
                'amount': float(parts[6]) if len(parts) > 6 else 0.0,
                'turnover': float(parts[7]) if len(parts) > 7 else 0.0,
            })
        except (ValueError, IndexError):
            continue
    return records


# ========================
# 日K线
# ========================

def get_daily_k(code: str) -> List[dict]:
    """获取日K线（同花顺）

    Args:
        code: 股票代码，如 "300006"（莱美药业）

    Returns:
        list: [{date, open, high, low, close, volume, amount, turnover}, ...]
        按日期升序排列

    注意：
        - 同花顺日K每次最多140条（总量约3856条）
        - 必须先建立会话（_ensure_session自动处理）
        - 如需更多历史数据，请使用翻页逻辑
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v6/line/hs_{code}/01/last.js"
    resp = _session.get(url, timeout=10)
    resp.encoding = 'utf-8'

    data = _parse_jsonp(resp.text)
    records_str = data.get('data', '')
    records = _parse_records(records_str)
    records.sort(key=lambda x: x['date'])
    return records


def get_daily_k_page(code: str, end_date: str = None) -> dict:
    """翻页获取更早的日K线（同花顺）

    Args:
        code: 股票代码，如 "300006"
        end_date: 截止日期YYYYMMDD，用第一条最老记录的日期往前取

    Returns:
        dict: {records: [...], total: 总条数, has_more: bool}
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v6/line/hs_{code}/01/last.js"
    if end_date:
        url += f"?end={end_date}"

    resp = _session.get(url, timeout=10)
    resp.encoding = 'utf-8'

    data = _parse_jsonp(resp.text)
    records_str = data.get('data', '')
    records = _parse_records(records_str)
    records.sort(key=lambda x: x['date'])

    return {
        'records': records,
        'total': int(data.get('total', 0)),
        'has_more': len(records) > 0,
    }


# ========================
# 1分钟K线
# ========================

def get_1min_k(code: str) -> List[dict]:
    """获取1分钟K线（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        list: [{date, open, high, low, close, volume, amount, turnover}, ...]
        按日期升序排列

    注意：
        - 同花顺1分钟K含全部历史（约821条，2009年至今）
        - 完全免费，无需注册，远超其他免费源
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v6/line/hs_{code}/11/last.js"
    resp = _session.get(url, timeout=10)
    resp.encoding = 'utf-8'

    data = _parse_jsonp(resp.text)
    records_str = data.get('data', '')
    records = _parse_records(records_str)
    records.sort(key=lambda x: x['date'])
    return records


# ========================
# 60分钟K线
# ========================

def get_60min_k(code: str) -> List[dict]:
    """获取60分钟K线（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        list: [{date(含时间如202604031500), open, high, low, close, volume, amount, turnover}, ...]
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v6/line/hs_{code}/60/last.js"
    resp = _session.get(url, timeout=10)
    resp.encoding = 'utf-8'

    data = _parse_jsonp(resp.text)
    records_str = data.get('data', '')
    records = _parse_records(records_str)
    records.sort(key=lambda x: x['date'])
    return records


# ========================
# 分时数据
# ========================

def get_intraday(code: str) -> dict:
    """获取分时数据（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        dict: {
            'records': [{time, price, volume, amount, cum_volume, cum_amount}, ...],
            'total': 总条数,
            'num': 本次返回条数,
            'date': 交易日期
        }

    注意：
        - 分时数据包含当日每分钟汇总（累计成交量+累计成交额）
        - 差分计算每分钟增量：volume_diff = current - prev
        - 覆盖9:30~15:00（约140条/日）
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v6/line/hs_{code}/01/last.js"
    resp = _session.get(url, timeout=10)
    resp.encoding = 'utf-8'

    data = _parse_jsonp(resp.text)
    records_str = data.get('data', '')

    # 分时数据解析（同日K格式，但需要差分）
    all_rows = []
    for row in records_str.split(';'):
        row = row.strip()
        if not row:
            continue
        parts = row.split(',')
        if len(parts) < 7:
            continue
        try:
            all_rows.append({
                'date': parts[0],
                'open': float(parts[1]),
                'high': float(parts[2]),
                'low': float(parts[3]),
                'close': float(parts[4]),
                'volume': float(parts[5]),
                'amount': float(parts[6]),
            })
        except (ValueError, IndexError):
            continue

    all_rows.sort(key=lambda x: x['date'])

    # 差分计算每分钟增量
    prev_vol = 0.0
    prev_amount = 0.0
    minute_records = []
    for rec in all_rows:
        vol_incr = max(0, rec['volume'] - prev_vol)
        amount_incr = max(0, rec['amount'] - prev_amount)
        minute_records.append({
            'time': rec['date'],
            'price': rec['close'],
            'volume': vol_incr,
            'amount': amount_incr,
            'cum_volume': rec['volume'],
            'cum_amount': rec['amount'],
        })
        prev_vol = rec['volume']
        prev_amount = rec['amount']

    return {
        'records': minute_records,
        'total': int(data.get('total', 0)),
        'num': int(data.get('num', 0)),
        'date': all_rows[-1]['date'] if all_rows else None,
    }


# ========================
# 实时行情 + 五档
# ========================

def get_realtime(code: str) -> Optional[dict]:
    """获取实时行情快照 + 五档买卖盘（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        dict: {
            'price': 当前价,
            'open': 开盘,
            'high': 最高,
            'low': 最低,
            'prev_close': 昨收,
            'volume': 成交量,
            'amount': 成交额,
            'buy1'~'buy5': 买一~买五价,
            'buy1_vol'~'buy5_vol': 买一~买五量,
            'sell1'~'sell5': 卖一~卖五价,
            'sell1_vol'~'sell5_vol': 卖一~卖五量,
        }
        返回 None 表示请求失败
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v2/realhead/hs_{code}/last.js"
    try:
        resp = _session.get(url, timeout=8)
        resp.encoding = 'utf-8'
        data = _parse_jsonp(resp.text)
        items = data.get('items', {})
        if not items:
            return None

        def f(key):
            try:
                val = items[key]
                if val in ('', '-1'):
                    return None
                return float(val)
            except (KeyError, ValueError):
                return None

        result = {
            'code': items.get('5'),
            'name': items.get('name'),
            'time': items.get('time'),
            'price': f('10'),     # 当前价
            'open': f('7'),       # 今日开盘
            'high': f('8'),       # 今日最高
            'low': f('9'),        # 今日最低
            'prev_close': f('6'), # 昨日收盘
            'volume': f('13'),     # 成交量
            'amount': f('19'),    # 成交额
            # 五档买盘
            'buy1': f('24'), 'buy1_vol': f('25'),
            'buy2': f('26'), 'buy2_vol': f('27'),
            'buy3': f('28'), 'buy3_vol': f('29'),
            'buy4': f('154'), 'buy4_vol': f('155'),
            'buy5': f('150'), 'buy5_vol': f('151'),
            # 五档卖盘
            'sell1': f('69'), 'sell1_vol': f('70'),
            'sell2': None, 'sell2_vol': None,
            'sell3': None, 'sell3_vol': None,
            'sell4': None, 'sell4_vol': None,
            'sell5': None, 'sell5_vol': None,
        }
        return result
    except Exception:
        return None


def get_fiverange(code: str) -> Optional[dict]:
    """获取五档买卖盘详情（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        dict: {
            'buy': [{price, volume}, ...],  # 5档买家（按价格降序）
            'sell': [{price, volume}, ...]  # 5档卖家（按价格升序）
        }
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v2/fiverange/hs_{code}/last.js"
    try:
        resp = _session.get(url, timeout=8)
        resp.encoding = 'utf-8'
        data = _parse_jsonp(resp.text)
        items = data.get('items', {})
        if not items:
            return None

        def parse_float(val):
            try:
                if val in ('', '-1'):
                    return None
                return float(val)
            except (ValueError, TypeError):
                return None

        # 五档买盘（fiverange格式）
        result = {'buy': [], 'sell': []}
        buy_keys = [('24', '25'), ('26', '27'), ('28', '29'), ('154', '155'), ('150', '151')]
        for price_key, vol_key in buy_keys:
            price = parse_float(items.get(price_key))
            vol = parse_float(items.get(vol_key))
            if price is not None:
                result['buy'].append({'price': price, 'volume': vol})

        # 五档卖盘
        sell_keys = [('69', '70'), ('85',), ('127',)]
        for sk in sell_keys:
            price = parse_float(items.get(sk[0]))
            vol = parse_float(items.get(sk[1])) if len(sk) > 1 else None
            if price is not None:
                result['sell'].append({'price': price, 'volume': vol})

        # 按价格排序
        result['buy'].sort(key=lambda x: x['price'], reverse=True)
        result['sell'].sort(key=lambda x: x['price'])
        return result
    except Exception:
        return None


def get_moneyflow(code: str) -> Optional[dict]:
    """获取资金流向数据（同花顺）

    Args:
        code: 股票代码，如 "300006"

    Returns:
        dict: 资金流向数据
    """
    code = _normalize(code)
    _ensure_session(code)

    url = f"https://d.10jqka.com.cn/v2/moneyflow/hs_{code}/last.js"
    try:
        resp = _session.get(url, timeout=8)
        resp.encoding = 'utf-8'
        data = _parse_jsonp(resp.text)
        return data.get(code, {})
    except Exception:
        return None


# ========================
# 批量获取
# ========================

def get_multi_realtime(codes: List[str]) -> List[dict]:
    """批量获取实时行情（遍历，非批量接口）

    Args:
        codes: 代码列表，如 ["300006", "002560"]

    Returns:
        list: 各股票的实时行情dict（含code字段）
    """
    results = []
    for code in codes:
        code = _normalize(code)
        r = get_realtime(code)
        if r:
            r['code'] = code
            results.append(r)
    return results


# ========================
# 工具函数
# ========================

def _normalize(code: str) -> str:
    """标准化股票代码为纯数字"""
    code = str(code).strip().lower()
    for prefix in ['sz', 'sh', 'hs_']:
        if code.startswith(prefix):
            code = code[len(prefix):]
    return code


def reset_session():
    """重置共享会话（清除Cookie，重新建立）"""
    global _session
    _session = None


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    print("同花顺数据接口测试")
    print("=" * 60)

    # 测试日K
    print("\n[1] 日K线（莱美药业 300006）")
    records = get_daily_k("300006")
    print(f"    获取 {len(records)} 条")
    if records:
        print(f"    最新: {records[-1]}")
        print(f"    最老: {records[0]}")

    # 测试1分钟K
    print("\n[2] 1分钟K线（莱美药业 300006）")
    records = get_1min_k("300006")
    print(f"    总共 {len(records)} 条")
    if records:
        print(f"    最新: {records[-1]}")
        print(f"    最老: {records[0]}")

    # 测试分时
    print("\n[3] 分时数据（莱美药业 300006）")
    result = get_intraday("300006")
    print(f"    当日 {result.get('date')} 共 {result['num']} 条")
    if result['records']:
        print(f"    最新分钟: {result['records'][-1]}")
        print(f"    前5条分钟增量:")
        for r in result['records'][:5]:
            print(f"      {r['time']} | 价格:{r['price']} | 增量:{r['volume']:,.0f}手")

    # 测试实时
    print("\n[4] 实时行情（莱美药业 300006）")
    rt = get_realtime("300006")
    if rt:
        print(f"    {rt}")
    else:
        print("    获取失败")

    # 测试五档
    print("\n[5] 五档盘口（莱美药业 300006）")
    fr = get_fiverange("300006")
    if fr:
        print(f"    买盘: {fr.get('buy')}")
        print(f"    卖盘: {fr.get('sell')}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
