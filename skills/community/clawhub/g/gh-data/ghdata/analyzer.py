"""
16维全量分析引擎 — 对一只股票进行深度剖析
==============================================
"""
from . import config, data_fetcher as fetcher, db_manager as db
from . import predictor, pattern_miner


def analyze(stock_code, market=None, stock_name=""):
    """
    对某只股票进行16维全量分析。

    Parameters
    ----------
    stock_code : str
        股票代码，如 '600028'
    market : str, optional
        'sh' 或 'sz'，不传则从数据库读取
    stock_name : str, optional
        股票名称

    Returns
    -------
    dict
        包含 16 个维度的分析结果
    """
    if not market:
        stocks = db.get_stock_list()
        for s in stocks:
            if s['stock_code'] == stock_code:
                market = s['market']
                stock_name = s['stock_name'] or stock_name
                break

    if not market:
        return {"error": f"未找到股票 {stock_code}"}

    result = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "market": market,
    }

    # 1. 实时行情
    try:
        realtime = fetcher.fetch_realtime(stock_code)
        if realtime:
            result["实时行情"] = realtime
    except Exception:
        pass

    # 2-3. K线数据 & 技术指标
    klines_raw = db.get_kline(stock_code, limit=200)
    if klines_raw:
        klines = sorted(klines_raw, key=lambda x: x['trade_date'])
        # 统一字段名
        klines_list = []
        for k in klines:
            klines_list.append({
                "date": k['trade_date'].strftime('%Y-%m-%d') if hasattr(k['trade_date'], 'strftime') else str(k['trade_date']),
                "open": float(k['open']),
                "close": float(k['close']),
                "high": float(k['high']),
                "low": float(k['low']),
                "volume": float(k['volume']),
                "amount": float(k.get('amount', 0)),
            })

        result["K线数量"] = len(klines_list)
        result["最新价"] = klines_list[-1]["close"]
        result["最新日期"] = klines_list[-1]["date"]

        # 涨跌幅
        if len(klines_list) >= 2:
            last_chg = (klines_list[-1]["close"] - klines_list[-2]["close"]) / klines_list[-2]["close"] * 100
            result["昨日涨跌幅"] = f"{last_chg:+.2f}%"

        # 均线
        closes = [k["close"] for k in klines_list]
        if len(closes) >= 20:
            result["MA5"] = f"{sum(closes[-5:])/5:.2f}"
            result["MA10"] = f"{sum(closes[-10:])/10:.2f}"
            result["MA20"] = f"{sum(closes[-20:])/20:.2f}"

        # 3. 方向预测（7规则投票）
        pred = predictor.analyze(None, klines_list)
        result["方向预测"] = pred

        # 4. 规律挖掘
        patterns = pattern_miner.mine_all(klines_list)
        result["规律挖掘"] = patterns

    # 5. 准确率统计
    try:
        acc = db.get_accuracy_stats(stock_code)
        result["方向准确率"] = acc
    except Exception:
        pass

    # 6. 最新预测记录
    try:
        latest = db.get_latest_prediction(stock_code)
        if latest:
            result["上次预测"] = {
                "日期": latest['predict_date'].strftime('%Y-%m-%d') if hasattr(latest['predict_date'], 'strftime') else str(latest['predict_date']),
                "方向": latest['direction'],
                "得分": latest['total_score'],
            }
    except Exception:
        pass

    # 7. 自学习摘要
    try:
        patterns_db = db.get_patterns(stock_code)
        if patterns_db:
            from collections import defaultdict
            groups = defaultdict(list)
            for p in patterns_db:
                groups[p['pattern_type']].append(p)

            summary = []
            for idx, (ptype, plist) in enumerate(sorted(groups.items()), 1):
                plist_sorted = sorted(plist, key=lambda x: x['created_at'] or '', reverse=True)
                latest_p = plist_sorted[0]
                verify_count = len(plist_sorted)
                desc = latest_p['description'] or ''
                summary.append({
                    "id": idx,
                    "name": ptype,
                    "verify_count": verify_count,
                    "description": desc,
                    "conclusion": f"第{verify_count}次验证: {desc}" if verify_count > 1 else f"首次发现: {desc}"
                })
            result["自学习摘要"] = summary
    except Exception:
        pass

    return result


def analyze_batch(stock_codes):
    """
    批量分析多只股票。

    Parameters
    ----------
    stock_codes : list[str]
        股票代码列表

    Returns
    -------
    list[dict]
    """
    results = []
    for code in stock_codes:
        try:
            r = analyze(code)
            results.append(r)
        except Exception as e:
            results.append({"stock_code": code, "error": str(e)})
    return results
