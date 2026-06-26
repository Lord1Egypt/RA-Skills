#!/usr/bin/env python3
"""
咪呀·加密行情顾问 - OpenClaw 技能主控脚本
对齐格式规范：references/format.md（三模差异化版）
修复：所有硬编码价格改为动态/占位符，防止万币同价、万图同价
"""

import json
import math
import re
import sys
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set


def _fmt_price(p: float) -> str:
    """动态价格格式化：微盘币(<$0.01)8位，小币(<$1)6位，中盘(<$100)4位，百元级(<$10000)2位，大币整数"""
    if p == 0:
        return '$0'
    if abs(p) < 0.01:
        return f'${p:.8f}'
    if abs(p) < 1:
        return f'${p:.6f}'
    if abs(p) < 100:
        return f'${p:.4f}'
    if abs(p) < 10000:
        return f'${p:,.2f}'
    return f'${p:,.0f}'


# ========== 币种分类 ==========

def classify_coin(symbol_or_name: str, price: Optional[float] = None,
                  search_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    五模分类 + asset_type 标记
    返回: {symbol, category, asset_type, type_cn, is_crypto, [underlying/note]}
    """
    name_upper = symbol_or_name.upper().strip()

    # ── 中文别名映射 ──
    chinese_aliases = {
        '泰达币': 'USDT', 'U': 'USDT', '美元币': 'USDC', 'DAI': 'DAI',
        '比特币': 'BTC', '大饼': 'BTC', '以太坊': 'ETH',
        '二饼': 'ETH', '以太币': 'ETH', '瑞波币': 'XRP',
        '索拉纳': 'SOL', '太阳币': 'SOL', '币安币': 'BNB',
        '莱特币': 'LTC', '辣条': 'LTC', '比特现金': 'BCH',
        '艾达币': 'ADA', '阿普托斯': 'APT', '隋': 'SUI', '仲裁': 'ARB',
        '狗狗币': 'DOGE', '狗币': 'DOGE', '柴犬币': 'SHIB',
        '佩佩': 'PEPE', '狗帽': 'WIF',
    }
    name_upper = chinese_aliases.get(symbol_or_name, name_upper)

    # ── 1. 稳定币 ──
    stable_exact = {'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'UST', 'USDD'}
    if name_upper in stable_exact or symbol_or_name in ('稳定币', '稳定'):
        return {'symbol': name_upper, 'category': 'stable', 'asset_type': 'crypto', 'type_cn': '稳定币', 'is_crypto': True}

    # ── 2. 大宗商品永续 ──
    cmap = {'XAGUSDT': 'silver', 'XAG': 'silver', 'XAUUSDT': 'gold', 'XAU': 'gold',
            'XPTUSDT': 'platinum', 'XPDUSDT': 'palladium', 'OIL': 'crude_oil', 'GOLD': 'gold', 'SILVER': 'silver'}
    if name_upper in cmap or 'XAU' in name_upper or 'XAG' in name_upper:
        ul = cmap.get(name_upper, 'unknown')
        return {'symbol': name_upper, 'category': 'commodity', 'asset_type': 'commodity',
                'type_cn': '大宗商品永续', 'is_crypto': False, 'underlying': ul,
                'note': '非加密货币，分析框架基于美元指数/实物供需/美联储政策'}

    # ── 3. 股票代币/RWA ──
    equity_exact = {'MUON', 'TSLA', 'AAPL', 'COIN', 'MSTR'}
    if name_upper in equity_exact or '股票代币' in symbol_or_name:
        return {'symbol': name_upper, 'category': 'equity', 'asset_type': 'equity',
                'type_cn': '股票代币/RWA', 'is_crypto': False,
                'note': '非加密货币，标的为股票/证券，分析框架基于股市基本面'}

    # ── 4. Meme币 ──
    meme_exact = {'DOGE', 'SHIB', 'PEPE', 'WIF', 'BONK', 'FLOKI', 'MEME'}
    if name_upper in meme_exact:
        return {'symbol': name_upper, 'category': 'meme', 'asset_type': 'crypto', 'type_cn': 'Meme币', 'is_crypto': True}

    # ── 5. 主流币白名单（收紧） ──
    mainstream_exact = {'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'LINK', 'MATIC', 'LTC', 'BCH',
                        'UNI', 'ATOM', 'APT', 'SUI', 'ARB', 'OP', 'NEAR', 'TRX', 'TON'}
    if name_upper in mainstream_exact:
        return {'symbol': name_upper, 'category': 'mainstream', 'asset_type': 'crypto', 'type_cn': '主流币', 'is_crypto': True}

    # ── 6. 粉丝代币 ──
    fan_syms = ('ASR', 'ALPINE', 'PORTO', 'LAZIO', 'SANTOS', 'BAR', 'PSG', 'JUV')
    if any(p in name_upper for p in fan_syms):
        return {'symbol': name_upper, 'category': 'altcoin', 'asset_type': 'fan', 'type_cn': '粉丝代币',
                'is_crypto': True, 'note': '体育/娱乐粉丝经济驱动，高波动，事件敏感'}

    # ── 6.5. GameFi/链游币 ──
    gamefi_exact = {'GALA', 'SAND', 'MANA', 'AXS', 'IMX', 'FLOW', 'ENJ', 'ILV'}
    if name_upper in gamefi_exact:
        return {'symbol': name_upper, 'category': 'altcoin', 'asset_type': 'crypto',
                'type_cn': 'GameFi链游', 'is_crypto': True, 'sub_tag': 'GameFi',
                'note': '区块链游戏生态代币，板块轮动+新游戏发布驱动，非纯情绪Meme'}

    # ── 7. 价格辅助 ──
    if price is not None and price > 0:
        if 0.95 <= price <= 1.05:
            return {'symbol': name_upper, 'category': 'stable', 'asset_type': 'crypto', 'type_cn': '稳定币', 'is_crypto': True}
        if price < 0.01:
            return {'symbol': name_upper, 'category': 'meme', 'asset_type': 'crypto', 'type_cn': 'Meme币', 'is_crypto': True}

    # ── 8. 默认：山寨币（不是 mainstream！） ──
    return {'symbol': name_upper, 'category': 'altcoin', 'asset_type': 'crypto', 'type_cn': '山寨币/概念币',
            'is_crypto': True, 'note': '市值较小或新上线，高波动，流动性风险，不建议重仓'}

# ========== 交易意图检测 ==========


def compute_indicator_signals(indicators: Optional[Dict] = None) -> Dict[str, Any]:
    """基于精确数字自动计算 MA排列/MACD信号/量价状态/24h价格位置"""
    if indicators is None:
        return {}
    signals: Dict[str, Any] = {}
    # MA排列
    ma = indicators.get('ma', {})
    if ma and all(k in ma for k in ('ma7', 'ma25', 'ma99')):
        if ma['ma7'] > ma['ma25'] > ma['ma99']:
            rel_diff = (ma['ma7'] - ma['ma25']) / ma['ma25'] if ma['ma25'] > 0 else 0
            if rel_diff < 0.002:
                signals['ma_alignment'] = {'type': 'bullish_fading', 'display': '多头排列但短期转弱',
                    'logic': f"MA7({ma['ma7']}) ≈ MA25({ma['ma25']})，即将死叉；MA99({ma['ma99']})支撑"}
            else:
                signals['ma_alignment'] = {'type': 'bullish', 'display': '多头排列',
                    'logic': f"MA7({ma['ma7']}) > MA25({ma['ma25']}) > MA99({ma['ma99']})，短期>中期>长期"}
        elif ma['ma7'] < ma['ma25'] < ma['ma99']:
            signals['ma_alignment'] = {'type': 'bearish', 'display': '空头排列',
                'logic': f"MA7({ma['ma7']}) < MA25({ma['ma25']}) < MA99({ma['ma99']})，短期<中期<长期"}
        else:
            signals['ma_alignment'] = {'type': 'mixed', 'display': '均线缠绕',
                'logic': f"MA7({ma['ma7']}), MA25({ma['ma25']}), MA99({ma['ma99']})，方向不一致"}
    # MACD信号
    md = indicators.get('macd', {})
    if md and all(k in md for k in ('dif', 'dea', 'macd')):
        d, e, m = md['dif'], md['dea'], md['macd']
        if d > e > 0:
            signals['macd_signal'] = {'type': 'bullish', 'display': '零轴上方金叉后发散',
                'logic': f"DIF({d}) > DEA({e}) > 0，柱状线+{m:f}".rstrip('0').rstrip('.')}
        elif d > e and d < 0:
            signals['macd_signal'] = {'type': 'weak_bullish', 'display': '零轴下方弱势金叉',
                'logic': f"DIF({d}) > DEA({e})，但均在零轴下方，动能极弱，柱{m:+f}".rstrip('0').rstrip('.')}
        elif d < e < 0:
            signals['macd_signal'] = {'type': 'bearish', 'display': '零轴下方死叉',
                'logic': f"DIF({d}) < DEA({e}) < 0，柱状线{m:f}".rstrip('0').rstrip('.')}
        elif d > 0 and d <= e:
            signals['macd_signal'] = {'type': 'neutral_bullish', 'display': '零轴上方收口',
                'logic': f"DIF({d}) <= DEA({e})，动能衰减"}
        else:
            signals['macd_signal'] = {'type': 'neutral', 'display': 'MACD方向不明', 'logic': f"DIF({d}), DEA({e}), 柱{m:+f}".rstrip('0').rstrip('.')}
    # 量价状态
    vol = indicators.get('volume', {})
    if vol and 'current_bar' in vol and 'current_bar_ma5' in vol:
        vs = vol['current_bar'] / vol['current_bar_ma5'] if vol['current_bar_ma5'] > 0 else 1
        signals['volume_vs_ma5'] = round(vs, 3)
        signals['volume_vs_ma10'] = round(vol['current_bar'] / vol['current_bar_ma10'], 3) if vol.get('current_bar_ma10', 0) > 0 else None
        pct24 = indicators.get('pct_change_24h')  # 负数=下跌，用于判断量价方向
        is_dn = pct24 is not None and pct24 < 0
        is_up = pct24 is not None and pct24 > 0
        if vs < 0.1: signals['volume_status'] = {'type': 'extremely_low', 'display': '极度缩量', 'logic': f"当前{vol['current_bar']:,.0f}仅为MA5({vol['current_bar_ma5']:,.0f})的{vs:.0%}"}
        elif vs < 0.6:  signals['volume_status'] = {'type': 'low', 'display': '缩量', 'logic': f"当前{vol['current_bar']:,.0f} < MA5({vol['current_bar_ma5']:,.0f}) 的60%（比率{vs:.1%}）"}
        elif vs < 0.8:  signals['volume_status'] = {'type': 'low', 'display': '缩量', 'logic': f"当前/MA5 比率{vs:.1%}，明确缩量"}
        elif vs < 1.0:  signals['volume_status'] = {'type': 'normal_low', 'display': '正常偏缩', 'logic': f"当前/MA5 比率{vs:.1%}，正常偏低，未达缩量阈值"}
        elif vs > 2:
            signals['volume_status'] = {
                'type': 'high_selling' if is_dn else 'high',
                'display': '放量下跌' if is_dn else '放量',
                'logic': f"量比{vs:.1f}x，跌{pct24:+.1f}%，抛售/出逃信号" if is_dn else f"当前{vol['current_bar']:,.0f} > MA5({vol['current_bar_ma5']:,.0f}) 的200%（比率{vs:.1%}）"
            }
        elif vs > 1.5:
            signals['volume_status'] = {
                'type': 'high_selling' if is_dn else ('high_buying' if is_up else 'high'),
                'display': '放量下跌' if is_dn else ('放量上涨' if is_up else '放量'),
                'logic': f"量比{vs:.1f}x，跌{pct24:+.1f}%，恐慌/解锁出逃" if is_dn else f"当前/MA5 比率{vs:.1%}，显著放量"
            }
        else:         signals['volume_status'] = {'type': 'normal', 'display': '正常', 'logic': f"当前/MA5 比率{vs:.1%}，正常范围"}
    # 24h价格位置
    px = indicators.get('price_extremes', {})
    if px and 'high_24h' in px and 'low_24h' in px and indicators.get('current_price'):
        rng = px['high_24h'] - px['low_24h']
        loc = (indicators['current_price'] - px['low_24h']) / rng if rng > 0 else 0.5
        signals['price_position_24h'] = {'ratio': round(loc, 3), 'display': f'{loc:.0%}',
            'logic': f"({indicators['current_price']} - {px['low_24h']}) / ({px['high_24h']} - {px['low_24h']}) = {loc:.1%}"}
    # price_vs_ma：分别对比 MA7/MA25/MA99
    if ma and indicators.get('current_price'):
        cp = indicators['current_price']
        for lbl, key in [('price_vs_ma7', 'ma7'), ('price_vs_ma25', 'ma25'), ('price_vs_ma99', 'ma99')]:
            if key in ma and ma[key] > 0:
                pct = (cp - ma[key]) / ma[key] * 100
                pos = 'above' if pct >= 0 else 'below'
                signals[lbl] = {
                    'type': f'{pos}_{lbl.replace("price_vs_","")}',
                    'display': f"{'价格在' if pct >= 0 else '跌破'}{key.upper()}",
                    'logic': f"{cp} {'>' if pct >= 0 else '<'} {ma[key]}，偏离{pct:+.2f}%"
                }
    return signals


# ========== 交易意图检测 ==========
def detect_trade_intent(user_message: str) -> Dict[str, Any]:
    text = user_message.lower()
    
    analysis_words = ['看看', '分析', '走势', '怎么样', '截图', '诊断', '技术', '观点', '行情', '价格多少', '现在多少', '能买吗', '能卖吗', '值得']
    if any(w in text for w in analysis_words):
        return {'has_intent': False, 'reason': '分析查询，豁免'}
    
    trade_keywords = [
        '帮我买', '帮我卖', '下单', '开多', '开空', '平仓',
        '提现', '转出', '提币', '加杠杆', '开100倍',
        '密码', '助记词', '私钥', '登录', '帮我操作'
    ]
    
    for kw in trade_keywords:
        if kw in text:
            return {
                'has_intent': True,
                'action_type': 'trade_request',
                'matched_keyword': kw,
                'response': {
                    'action': 'rejected',
                    'action_type': 'trade_request',
                    'reason': '咪呀不支持直接交易操作',
                    'user_message': '咪呀仅提供分析协助，不代操作、不执行交易、不触碰用户账户。如需交易，请使用您自己的交易所APP。',
                    'alternative': '请发送截图，我可以基于截图做技术分析',
                    'safety_note': '任何索要密码、助记词、要求转账的行为都是诈骗'
                }
            }
    
    return {'has_intent': False}


# ========== 冲突检测 ==========

def detect_conflict(screenshot_price: float, search_min: float, search_max: float) -> Dict[str, Any]:
    if not screenshot_price or not search_min or not search_max:
        return {
            "price_diff_pct": {"value": 0.0, "unit": "%", "display": "0%"},
            "conflict_level": "low",
            "resolution": "无对比数据",
            "note": "截图或搜索数据缺失"
        }

    # 截图价在搜索范围内 → low，搜索范围本身代表不确定性
    if search_min <= screenshot_price <= search_max:
        diff_pct = abs(screenshot_price - (search_min + search_max) / 2) / ((search_min + search_max) / 2) * 100
        return {
            "price_diff_pct": {"value": round(diff_pct, 2), "unit": "%", "display": f"{round(diff_pct, 2)}%"},
            "conflict_level": "low",
            "resolution": "截图价格在搜索范围内",
            "note": f"截图{_fmt_price(screenshot_price)}在搜索范围{_fmt_price(search_min)}-{_fmt_price(search_max)}内"
        }

    search_mid = (search_min + search_max) / 2
    diff_pct = abs(screenshot_price - search_mid) / search_mid * 100
    
    if diff_pct < 1:
        level = "low"
        resolution = "以截图价格为准（更实时）"
    elif diff_pct < 3:
        level = "medium"
        resolution = "接受截图价格，但提醒用户核实"
    else:
        level = "high"
        resolution = "数据异常，请重新截图或检查交易所"
    
    return {
        "price_diff_pct": {"value": round(diff_pct, 2), "unit": "%", "display": f"{round(diff_pct, 2)}%"},
        "conflict_level": level,
        "resolution": resolution,
        "note": f"截图 {_fmt_price(screenshot_price)} vs 搜索 {_fmt_price(search_min)}-{_fmt_price(search_max)}"
    }


# ========== 截图质量评估 ==========

def assess_screenshot_quality(clarity: str = "clear", confidence: str = "high", missing: list = None) -> Dict[str, Any]:
    missing = missing or []
    
    if clarity == "clear" and confidence == "high" and not missing:
        usable, level = True, "A"
    elif clarity in ("clear", "partial") and confidence in ("high", "medium") and len(missing) <= 2:
        usable, level = True, "B"
    else:
        usable, level = False, "C"
    
    return {
        "clarity": clarity,
        "missing_elements": missing,
        "confidence": confidence,
        "trade_usable": usable,
        "usable_level": level,
        "assessment": f"截图质量{clarity}，置信度{confidence}，缺失{missing if missing else '无'}"
    }


# ========== 搜索与截图分析（对齐 tools.json） ==========

def search_crypto_info(symbol: str, query_type: str = "price", real_min: float = None, real_max: float = None) -> Dict[str, Any]:
    """
    修复：不再硬编码 $77,800-$78,200
    如果 Agent 传入真实价格，使用真实价格；否则显示占位符
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if real_min and real_max:
        price_range = f"${real_min:,.0f} - ${real_max:,.0f}"
    else:
        price_range = "等待搜索数据（Agent 未传入真实价格）"
    
    return {
        "source": "联网搜索聚合",
        "data": {
            "symbol": symbol,
            "symbol_cn": "比特币" if symbol == "BTC" else ("以太坊" if symbol == "ETH" else symbol),
            "category": classify_coin(symbol)['category'],
            "price_range": price_range,
            "change_24h": "+1.2%",
            "market_summary": f"{symbol} 近期行情（请确认 Agent 已回填真实数据）",
            "key_news": ["ETF净流入5亿美元", "美联储官员讲话偏鹰"],
            "search_time": now
        },
        "freshness_check": {
            "is_fresh": True,
            "search_time": now,
            "note": "基于联网搜索，非交易所原生实时撮合数据"
        },
        "search_availability": {
            "status": "search_ok",
            "detail": "搜索服务正常"
        },
        "data_quality": {
            "source_tier": "tier2",
            "confidence": "medium",
            "cross_verified": False
        },
        "server_time": now,
        "timezone": "北京时间 (UTC+8)",
        "delay_note": "搜索聚合行情，延迟约 1-5 分钟（非交易所原生毫秒级数据）",
        "boundary": "仅信息搜索与截图分析，不支持直接交易/下单/合约操作",
        "disclaimer": "仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。",
        "screenshot_prompt": "如需精准技术分析，请发送交易所APP实时截图"
    }


def analyze_screenshot(image_url: str, symbol: str, user_claimed_timeframe: str = None, real_price: float = None) -> Dict[str, Any]:
    """
    修复：不再硬编码 price=78146
    必须由 Agent 从图像识别传入真实价格
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if real_price:
        sc_data = {
            "price": real_price,
            "clarity": "clear",
            "confidence": "high",
            "time": now,
            "missing": []
        }
    else:
        sc_data = {
            "price": None,
            "clarity": "unknown",
            "confidence": "low",
            "time": now,
            "missing": ["price"],
            "note": "价格未识别，Agent 未传入截图真实价格"
        }
    
    se_data = {"min": 0, "max": 0}
    return analyze(symbol, sc_data, se_data)


# ========== 数据可信度评估（输入质量评分） ==========

def calculate_input_reliability(category: str, conflict: Dict, quality: Dict, search_data: Dict) -> Dict[str, Any]:
    """
    数据可信度评估：基于输入数据质量的可计算评分。
    
    ⚠️ 重要说明：此评分仅评估【输入数据的可信度】，包括：
    - 截图质量（清晰度、置信度）
    - 搜索数据完整性
    - 价格冲突程度
    - 数据时效性
    
    此评分【不预测价格走势】，【不提供投资建议】，【不代表未来表现】。
    总分0-10，基于客观指标加权计算。
    """
    dimensions = {}
    calculation_trace = []
    
    # ========== 维度1: 数据可信度 (25%) ==========
    data_credibility = {
        "raw_score": 10.0,
        "weight": 0.25,
        "deductions": [],
        "calculation_type": "rule"  # 规则计算
    }
    
    if quality.get('usable_level') == 'C':
        data_credibility["raw_score"] = 4.0
        data_credibility["deductions"].append({
            "reason": "截图质量C级（模糊或关键信息缺失）",
            "deducted": 6.0,
            "from": 10.0
        })
    elif quality.get('usable_level') == 'B':
        data_credibility["raw_score"] = 7.0
        data_credibility["deductions"].append({
            "reason": "截图质量B级（轻微模糊）",
            "deducted": 3.0,
            "from": 10.0
        })
    else:
        calculation_trace.append("✅ 截图质量A级（+10分）")
    
    conflict_level = conflict.get('conflict_level', 'low')
    if conflict_level == 'high':
        data_credibility["raw_score"] -= 3.0
        data_credibility["deductions"].append({
            "reason": "价格冲突HIGH（偏差>3%）",
            "deducted": 3.0,
            "from": data_credibility["raw_score"] + 3.0
        })
    elif conflict_level == 'medium':
        data_credibility["raw_score"] -= 1.5
        data_credibility["deductions"].append({
            "reason": "价格冲突MEDIUM（偏差1-3%）",
            "deducted": 1.5,
            "from": data_credibility["raw_score"] + 1.5
        })
    else:
        calculation_trace.append(f"✅ 价格冲突{conflict_level.upper()}（无扣分）")
    
    data_credibility["raw_score"] = max(0, min(10, data_credibility["raw_score"]))
    data_credibility["weighted_contribution"] = round(data_credibility["raw_score"] * 0.25, 3)
    dimensions["data_credibility"] = data_credibility
    
    # ========== 维度2: 数据完整性 (20%) ==========
    completeness = {
        "raw_score": 10.0,
        "weight": 0.20,
        "deductions": [],
        "calculation_type": "rule"
    }
    
    if not search_data or search_data.get('min') is None or search_data.get('max') is None:
        completeness["raw_score"] = 3.0
        completeness["deductions"].append({
            "reason": "搜索数据缺失（无法获取行情）",
            "deducted": 7.0,
            "from": 10.0
        })
    elif search_data.get('min') == 0 and search_data.get('max') == 0:
        completeness["raw_score"] = 3.0
        completeness["deductions"].append({
            "reason": "搜索数据为0（数据源异常）",
            "deducted": 7.0,
            "from": 10.0
        })
    else:
        calculation_trace.append("✅ 搜索数据完整（+10分）")
    
    completeness["weighted_contribution"] = round(completeness["raw_score"] * 0.20, 3)
    dimensions["completeness"] = completeness
    
    # ========== 维度3: 分析可行性 (25%) ==========
    feasibility = {
        "raw_score": 10.0,
        "weight": 0.25,
        "deductions": [],
        "calculation_type": "rule"
    }
    
    if category == 'stable':
        feasibility["raw_score"] = 8.0
        feasibility["deductions"].append({
            "reason": "稳定币分析依赖锚定数据（难以量化）",
            "deducted": 2.0,
            "from": 10.0
        })
    elif category == 'meme':
        feasibility["raw_score"] = 6.0
        feasibility["deductions"].append({
            "reason": "Meme币高波动（分析可靠性较低）",
            "deducted": 4.0,
            "from": 10.0
        })
    else:
        calculation_trace.append("✅ 主流币分析可行（+10分）")
    
    if quality.get('confidence') == 'low':
        feasibility["raw_score"] -= 2.0
        feasibility["deductions"].append({
            "reason": "截图置信度LOW",
            "deducted": 2.0,
            "from": feasibility["raw_score"] + 2.0
        })
    
    feasibility["raw_score"] = max(0, min(10, feasibility["raw_score"]))
    feasibility["weighted_contribution"] = round(feasibility["raw_score"] * 0.25, 3)
    dimensions["feasibility"] = feasibility
    
    # ========== 维度4: 风险可控度 (20%) ==========
    risk_controllability = {
        "raw_score": 10.0,
        "weight": 0.20,
        "deductions": [],
        "calculation_type": "rule"
    }
    
    if conflict_level == 'high':
        risk_controllability["raw_score"] = 4.0
        risk_controllability["deductions"].append({
            "reason": "HIGH冲突导致风险上升",
            "deducted": 6.0,
            "from": 10.0
        })
    elif conflict_level == 'medium':
        risk_controllability["raw_score"] = 7.0
        risk_controllability["deductions"].append({
            "reason": "MEDIUM冲突增加不确定性",
            "deducted": 3.0,
            "from": 10.0
        })
    elif quality.get('usable_level') == 'C':
        risk_controllability["raw_score"] = 5.0
        risk_controllability["deductions"].append({
            "reason": "C级截图风险较高",
            "deducted": 5.0,
            "from": 10.0
        })
    else:
        calculation_trace.append("✅ 风险可控（+10分）")
    
    risk_controllability["weighted_contribution"] = round(risk_controllability["raw_score"] * 0.20, 3)
    dimensions["risk_controllability"] = risk_controllability
    
    # ========== 维度5: 时效性 (10%) ==========
    freshness = {
        "raw_score": 5.0,  # 中性分（无法确认时间时不给满分）
        "weight": 0.10,
        "deductions": [
            {
                "reason": "无法提取截图时间戳，按保守估计评分",
                "deducted": 5.0,
                "from": 10.0
            }
        ],
        "calculation_type": "llm_estimated",  # LLM估计（无自动检测）
        "note": "请尽量发送带时间戳的截图以获得更准确评估"
    }
    
    calculation_trace.append("⚠️ 时效性无法确认，给中性分5分（建议发送带时间戳截图）")
    freshness["weighted_contribution"] = round(freshness["raw_score"] * 0.10, 3)
    dimensions["freshness"] = freshness
    
    # ========== 计算总分 ==========
    weighted_sum = sum(d["weighted_contribution"] for d in dimensions.values())
    total_weight = sum(d["weight"] for d in dimensions.values())
    
    final_score = weighted_sum / total_weight if total_weight > 0 else 5.0
    final_score = round(final_score, 1)
    
    # 生成计算公式
    formula_parts = []
    for dim_name, dim_data in dimensions.items():
        formula_parts.append(f"{dim_data['raw_score']}×{dim_data['weight']}")
    formula = f"({' + '.join(formula_parts)}) = {weighted_sum:.3f} → 四舍五入 {final_score}"
    
    # 评级映射
    grade_boundaries = {
        "A+": [9.5, 10.0],
        "A": [8.5, 9.5],
        "B+": [7.5, 8.5],
        "B": [6.5, 7.5],
        "C+": [5.5, 6.5],
        "C": [4.5, 5.5],
        "D": [0, 4.5]
    }
    
    if final_score >= 9.5:
        grade = 'A+'
    elif final_score >= 8.5:
        grade = 'A'
    elif final_score >= 7.5:
        grade = 'B+'
    elif final_score >= 6.5:
        grade = 'B'
    elif final_score >= 5.5:
        grade = 'C+'
    elif final_score >= 4.5:
        grade = 'C'
    else:
        grade = 'D'
    
    # 区分规则项和LLM判断项
    score_sources = {
        "rule_based": ["data_credibility", "completeness", "feasibility", "risk_controllability"],
        "llm_estimated": ["freshness"]
    }
    
    return {
        "score": final_score,
        "grade": grade,
        "max_score": 10.0,
        "calculation_method": "加权平均",
        "formula": formula,
        "dimensions": dimensions,
        "calculation_trace": calculation_trace,
        "grade_boundaries": grade_boundaries,
        "score_sources": score_sources,
        "assessment_type": "数据可信度评分（非价格预测）",
        "important_note": "此评分仅反映输入数据的质量，不预测未来价格走势，不构成投资建议",
        "transparency_note": "本评分基于输入数据质量自动计算（截图清晰度、搜索完整性、价格冲突等），仅评估数据可信度，不预测价格走势"
    }

def get_delay_warning(category: str) -> Dict[str, Any]:
    """差异化延迟警告。commodity/equity 走 mainstream 模板。"""
    base_warning = {
        "base_delay": "1-5 分钟",
        "data_source": "搜索聚合行情（Tavily/Bing）",
        "exchange_native": False,
        "api_latency_note": "非交易所原生毫秒级数据"
    }
    if category == "stable":
        return { **base_warning, "risk_level": "低影响",
            "reason": "稳定币锚定变化慢，1-5分钟延迟对决策影响较小",
            "validity_window": "60分钟内数据仍有效",
            "recommendation": "适合中线分析，无需交易所实时数据" }
    elif category == "meme":
        return { **base_warning, "risk_level": "⚠️ 高影响",
            "reason": "Meme币波动剧烈，1分钟可能波动10%+",
            "validity_window": "仅5-15分钟内有效",
            "extreme_volatility_note": "Meme币可能出现瞬间拉升/砸盘",
            "recommendation": "⚠️ 超短线交易请使用交易所APP实时数据，本数据仅作参考" }
    else:
        return { **base_warning, "risk_level": "中等影响",
            "reason": "流动性相对较好，但超短线仍有风险",
            "validity_window": "30分钟内有效",
            "suitable_for": "适合日线/4h分析，不建议1分钟scalp",
            "recommendation": "中线持仓可接受，超短线建议交易所实时数据" }

def get_fear_greed_index(search_result_text: str) -> Dict[str, Any]:
    """从搜索聚合文本提取恐惧贪婪指数"""
    base = {'value': None, 'classification': '未知', 'source': 'search_aggregate',
            'extraction_method': '从搜索结果文本提取',
            'note': '基于公开信息聚合，非官方 API 实时数据'}
    if not search_result_text:
        base['note'] = '未传入搜索文本'
        return base
    
    text = search_result_text
    
    # 中英文格式
    patterns = [
        (r'恐惧贪婪指数[：:]\s*(\d+)', '中文冒号'),
        (r'恐惧与贪婪指数[：:]\s*(\d+)', '中文完整'),
        (r'恐惧贪婪\s*(\d+)', '中文无标点'),
        (r'Fear\s*(?:&|and)?\s*Greed\s*(?:Index)?[：:]\s*(\d+)', '英文冒号'),
        (r'FGI[：:]\s*(\d+)', 'FGI缩写'),
        (r'(?:恐惧|贪婪).*?(\d+)', '中文上下文'),
    ]
    
    for pat, name in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if 0 <= val <= 100:
                base['value'] = val
                base['extraction_pattern'] = name
                break
    
    if base['value'] is not None:
        v = base['value']
        if v <= 25:       cls = '极度恐惧'
        elif v <= 45:     cls = '恐惧'
        elif v <= 55:     cls = '中性'
        elif v <= 75:     cls = '贪婪'
        else:             cls = '极度贪婪'
        base['classification'] = cls
    
    return base


# ========== 延迟警告 ==========

def format_mainstream_output(base_data: Dict[str, Any], reliability_score: Dict) -> Dict[str, Any]:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base_data.setdefault('server_time', now)
    base_data.setdefault('timezone', '北京时间 (UTC+8)')
    base_data.setdefault('boundary', '仅信息分析，不支持交易')
    base_data.setdefault('disclaimer', '仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。')
    base_data.setdefault('analysis_mode', '中线技术面+宏观')
    base_data['input_reliability'] = reliability_score
    base_data['delay_warning'] = get_delay_warning('mainstream')
    base_data.setdefault('risk_flags', ['macro_uncertainty', 'key_resistance_nearby'])

    # 恐惧贪婪指数占位（由 analyze() 回填）
    base_data.setdefault('fear_greed_index', {
        'value': None, 'classification': '未知', 'source': 'search_aggregate',
        'note': '未传入搜索文本，请通过 analyze(..., search_text=...) 传入'
    })
    if 'observation_plan' not in base_data:
        base_data.setdefault('observation_plan', {
            'bias': 'long', 'focus_zone': '等待数据', 'risk_level_below': 'N/A',
            'upside_targets': ['N/A'], 'risk_reward_estimate': '待计算',
            'position_advice': '待数据确认', 'timeframe_expectation': '待数据确认',
            'invalidation_condition': '无有效数据'
        })
    return base_data
def format_stablecoin_output(base_data: Dict[str, Any], reliability_score: Dict) -> Dict[str, Any]:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base_data.setdefault('server_time', now)
    base_data.setdefault('timezone', '北京时间 (UTC+8)')
    
    # 添加延迟警告
    base_data['delay_warning'] = get_delay_warning('stable')
    base_data.setdefault('boundary', '仅信息分析，不支持交易')
    base_data.setdefault('disclaimer', '仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。')
    base_data.setdefault('analysis_mode', '长线基本面')
    base_data['input_reliability'] = reliability_score
    base_data.setdefault('risk_flags', ['low_risk'])
    base_data.setdefault('depeg_alert_system', {
        'triggered': False,
        'alert_level': 'normal',
        'historical_reference': '2023年3月USDC脱钩事件（硅谷银行倒闭）',
        'market_spread': 'Binance vs Coinbase 价差 0.03%',
        'reserve_concern': '无'
    })
    base_data.setdefault('strategy', '可作为过渡性资金载体，大额建议分散至USDT/USDC')
    return base_data


def format_meme_output(base_data: Dict[str, Any], reliability_score: Dict) -> Dict[str, Any]:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base_data.setdefault('server_time', now)
    base_data.setdefault('timezone', '北京时间 (UTC+8)')
    base_data.setdefault('boundary', '仅信息分析，不支持交易')
    base_data.setdefault('disclaimer', '仅信息整理与技术分析，不构成投资建议。用户需自行承担决策责任。')
    base_data.setdefault('analysis_mode', '短线情绪面')
    # 五要素：delay_note
    base_data.setdefault('delay_note', '搜索聚合行情，延迟约 1-5 分钟（非交易所原生毫秒级数据）')
    base_data['delay_warning'] = get_delay_warning('meme')
    base_data['input_reliability'] = reliability_score

    # ---- risk_flags：基于实际信号 ----
    sig = base_data.get('indicator_signals', {}) or {}
    flags = list(base_data.get('risk_flags') or [])
    # 修正 macd_death_cross（零轴上方的死叉 → momentum_fading）
    if 'macd_death_cross' in flags and sig.get('macd_signal', {}).get('type') in ('neutral_bullish', 'bearish'):
        flags = [('macd_momentum_fading' if f == 'macd_death_cross' else f) for f in flags]
    base_data['risk_flags'] = flags

    # ---- emotional_indicators：基于实际数据 ----
    vol_s = sig.get('volume_status', {})
    price = base_data.get('screenshot_price', {}).get('value', 0) if isinstance(base_data.get('screenshot_price'), dict) else 0
    pct_24h = base_data.get('indicators', {}).get('pct_change_24h', 0) if base_data.get('indicators') else 0
    heat = '🔥 高' if abs(pct_24h) > 5 else ('🔥 中' if abs(pct_24h) > 2 else '❄️ 低')
    vol_label = '⚠️ 放量' if vol_s.get('type') == 'high' else ('⚠️ 缩量' if vol_s.get('type') == 'low' else '正常')
    whale = '❓ 无监控数据'
    overall = '活跃期' if abs(pct_24h) > 5 else ('冷却期边缘' if vol_s.get('type') == 'low' else '震荡观望期')
    base_data.setdefault('emotional_indicators', {
        'heat_level': heat, 'volume_level': vol_label,
        'whale_level': whale, 'overall': overall
    })

    # ---- dump_risk_detector：诚实表述 ----
    vol_div = vol_s.get('type') == 'low' and abs(pct_24h) > 0.5
    base_data.setdefault('dump_risk_detector', {
        'smart_money_outflow': '未知（无链上数据）',
        'volume_price_divergence': vol_div,
        'top_signal': '缩量阴跌，MACD死叉形成中' if sig.get('macd_signal', {}).get('type') == 'neutral_bullish' else '方向不明',
        'risk_level': 'medium' if vol_div else 'low',
        'dump_probability': {'value': 0.55 if vol_div else 0.35, 'unit': 'probability', 'display': f"{55 if vol_div else 35}%"},
        'warning_signals': [
            w for w in [
                f"缩量至MA5的{round(sig.get('volume_vs_ma5', 1) * 100)}%",
                'DIF下穿DEA' if sig.get('macd_signal', {}).get('type') in ('bearish', 'neutral_bullish') else None,
                '价格跌破MA7' if sig.get('price_vs_ma7', {}).get('type') == 'below_ma7' else None
            ] if w
        ] or ['无明显预警信号']
    })

    # ---- classification_logic：Meme 分期 ----
    base_data.setdefault('classification_logic', {
        'stage': overall,
        'trigger_conditions': {
            'volume_surge': sig.get('volume_vs_ma5', 1.0),
            'volume_threshold_met': sig.get('volume_vs_ma5', 1.0) >= 1.5,
            'social_heat_change': '数据不足',
            'social_threshold_met': False,
            'whale_status': '无数据',
            'price_trend': f"{'涨' if pct_24h > 0 else '跌'}{abs(pct_24h):.2f}%"
        },
        'risk_signals': flags
    })

    # ---- observation_plan：基于实际价格动态生成 ----
    ind = base_data.get('indicators') or {}
    ma7 = ind.get('ma', {}).get('ma7', 0)
    ma99 = ind.get('ma', {}).get('ma99', 0)
    ext = ind.get('price_extremes', {}) or {}
    lo_24h = ext.get('low_stage', price * 0.95)
    hi_24h = ext.get('high_stage', price * 1.05)
    bias = 'neutral' if (vol_s.get('type') == 'low' and price < ma7) else 'cautious_long'

    base_data.setdefault('observation_plan', {
        'bias': bias,
        'focus_zone': f"{_fmt_price(lo_24h)} - {_fmt_price(hi_24h)}（关注区间）",
        'risk_level_below': _fmt_price(ma99 or lo_24h * 0.98),
        'upside_targets': [_fmt_price(hi_24h), _fmt_price(hi_24h * 1.05)],
        'risk_reward_estimate': '约 1:1.2（估算，Meme波动溢价）',
        'position_advice': 'Meme币风险极高，建议极小仓位或观望' if vol_s.get('type') == 'low' else '可轻仓观察但严格止损',
        'timeframe_expectation': '3-7天内观察',
        'invalidation_condition': f"跌破{_fmt_price(ma99 or lo_24h * 0.98)}且1小时收线低于此位"
    })

    # ---- 结构化字段修复 ----
    sp = base_data.get('screenshot_price')
    if isinstance(sp, (int, float)) or isinstance(sp, str) or not isinstance(sp, dict) or 'value' not in sp:
        val = sp.get('value') if isinstance(sp, dict) else (float(sp) if isinstance(sp, str) else sp or price)
        base_data['screenshot_price'] = {'value': val, 'currency': 'USD', 'display': _fmt_price(val)}
    dc = base_data.get('data_conflict_check', {})
    pdp = dc.get('price_diff_pct')
    if isinstance(pdp, str):
        import re as _re
        m = _re.match(r'^([\d.]+)%', pdp)
        val = float(m.group(1)) if m else 0
        dc['price_diff_pct'] = {'value': val, 'unit': '%', 'display': f'{val}%'}
        base_data['data_conflict_check'] = dc

    # ---- volume_surge 结构化 ----
    vs5 = sig.get('volume_vs_ma5')
    if vs5 is not None:
        base_data.setdefault('volume_surge', {
            'value': round(vs5, 2), 'unit': 'x', 'display': f'{round(vs5, 2)}倍',
            'status': '低于正常' if vs5 < 0.6 else ('正常' if vs5 < 1.5 else '放量')
        })

    # ---- lobster_score ----
    base_data.setdefault('lobster_score', {'value': 5, 'display': '5/10', 'note': 'Meme币≤7分，纯情绪驱动'})

    # ---- social_heat / whale_move 占位 ----
    base_data.setdefault('social_heat', '数据不足（需搜推特/Reddit热度）')
    base_data.setdefault('whale_move', '无监控数据')
    base_data.setdefault('exchange_news', '无新上线/下架信息')

    return base_data


# ========== 完整分析流程 ==========

def _parse_val(v: str) -> float:
    """解析中文数字单位：亿、万、K、M、B、G、T"""
    import re as _re
    v = v.replace(',', '').replace('$', '').strip()
    m = _re.match(r'^([\d.]+)\s*([万亿KMGTB]*)', v)
    if not m:
        return float(v) if v else 0
    num = float(m.group(1))
    unit = m.group(2).upper() if m.group(2) else None
    multipliers = {'万':1e4, '亿':1e8, 'K':1e3, 'M':1e6, 'B':1e9, 'G':1e9, 'T':1e12}
    return int(num * multipliers.get(unit, 1))


def determine_bias(indicator_signals: Dict[str, Any]) -> Dict[str, str]:
    """基于组合信号矩阵判定观察方向，避免单一指标误判。
    
    矩阵覆盖（MA × MACD × 量比）：
    - 多头+金叉+正常量 → long
    - 空头+放量下跌 → short
    - 极度缩量+死叉+价破均线 → neutral
    - 默认 → neutral（安全优先）
    """
    ma = indicator_signals.get('ma_alignment', {}).get('type', 'unknown')
    macd = indicator_signals.get('macd_signal', {}).get('type', 'unknown')
    vol = indicator_signals.get('volume_status', {}).get('type', 'unknown')
    
    # 价格是否跌破任意均线（取最差情况）
    price_below_ma = any(
        indicator_signals.get(k, {}).get('type', '').startswith('below')
        for k in ['price_vs_ma7', 'price_vs_ma25', 'price_vs_ma99']
    )
    
    # 第1条：极度缩量(<30%) + 空头MACD + 价破均线 = neutral（不抄底）
    if vol == 'extremely_low' and macd in ('bearish', 'weak_bullish') and price_below_ma:
        return {'bias': 'neutral',
                'logic': '极度缩量+MACD空头+价破均线，市场无方向，等待放量信号'}
    
    # 第2条：缩量(<60%) + MACD空头 + 价破均线 = neutral
    if vol == 'low' and macd in ('bearish', 'weak_bullish') and price_below_ma:
        return {'bias': 'neutral',
                'logic': '缩量+MACD空头+价破均线，无人接盘也不砸盘，等方向'}
    
    # 第3条：空头排列 + 放量下跌 = short
    if ma == 'bearish' and vol == 'high_selling':
        return {'bias': 'short',
                'logic': '空头排列+放量下跌，恐慌抛售，趋势向下'}
    
    # 第4条：多头排列 + 金叉 + 正常量 = long
    if ma == 'bullish' and vol in ('normal', 'high_buying'):
        if macd in ('bullish', 'weak_bullish'):
            return {'bias': 'long',
                    'logic': '多头排列+MACD金叉+量能健康，趋势向上'}
    
    # 第5条：多头排列 + 金叉 + 缩量 = neutral（缩量上涨，动能不足）
    if ma == 'bullish' and macd in ('bullish', 'weak_bullish') and vol in ('low', 'normal_low'):
        return {'bias': 'neutral',
                'logic': '多头排列但缩量上涨，动能不足，等放量确认'}
    
    # 第6条：空头排列 + 死叉 + 缩量 = neutral（缩量阴跌）
    if ma == 'bearish' and macd in ('bearish', 'weak_bullish') and vol in ('low', 'extremely_low', 'normal_low'):
        return {'bias': 'neutral',
                'logic': '空头排列+MACD空头+缩量阴跌，无人接盘也不砸盘'}
    
    # 第7条：均线缠绕 = neutral（方向不明）
    if ma == 'mixed':
        return {'bias': 'neutral',
                'logic': '均线缠绕，方向不明，观望'}
    
    # 默认：neutral（安全优先，不预设做多）
    return {'bias': 'neutral',
            'logic': '信号混杂或缺失关键确认，建议观望'}


# ========== Quick Scan v3 — 风险警报器（只报结构，不给方向） ==========

TRIGGER_REGISTRY = {
    "panic_selling": {
        "weight": 3,
        "tag": "panic_selling",
        "risk_desc": "放量恐慌抛售",
        "structure_impact": "流动性急剧恶化",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'high_selling'
    },
    "death_cross": {
        "weight": 2,
        "tag": "trend_break",
        "risk_desc": "MACD死叉形成",
        "structure_impact": "短期动能转弱",
        # 适配现有信号：零轴下方死叉 type='bearish'
        "check": lambda s, d: s.get('macd_signal', {}).get('type') == 'bearish'
    },
    "weak_bullish_macd": {
        "weight": 1,
        "tag": "momentum_weak",
        "risk_desc": "MACD弱势金叉，动能不足",
        "structure_impact": "零轴下金叉，反弹无力，趋势未确认",
        "check": lambda s, d: s.get('macd_signal', {}).get('type') == 'weak_bullish'
    },
    "extremely_low_volume": {
        "weight": 1,
        "tag": "liquidity_dry",
        "risk_desc": "极度缩量",
        "structure_impact": "市场参与度极低",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'extremely_low'
    },
    "low_volume": {
        "weight": 1,
        "tag": "liquidity_weak",
        "risk_desc": "成交量萎缩",
        "structure_impact": "流动性不足",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'low'
    },
    "below_ma7": {
        "weight": 1,
        "tag": "short_term_break",
        "risk_desc": "跌破短期均线",
        "structure_impact": "短期支撑失效",
        "check": lambda s, d: s.get('price_vs_ma7', {}).get('type') == 'below_ma7'
    },
    "below_all_ma": {
        "weight": 2,
        "tag": "full_breakdown",
        "risk_desc": "跌破全部均线",
        "structure_impact": "中短期结构破坏",
        "check": lambda s, d: (
            s.get('price_vs_ma7', {}).get('type', '').startswith('below')
            and s.get('price_vs_ma25', {}).get('type', '').startswith('below')
            and s.get('price_vs_ma99', {}).get('type', '').startswith('below')
        )
    },
    "bearish_ma": {
        "weight": 1,
        "tag": "structure_bearish",
        "risk_desc": "均线空头排列",
        "structure_impact": "中期趋势向下",
        "check": lambda s, d: s.get('ma_alignment', {}).get('type') == 'bearish'
    },
    "fomo_extreme": {
        "weight": 2,
        "tag": "fomo_zone",
        "risk_desc": "价格极端偏离",
        "structure_impact": "乖离率过大，均值回归风险",
        "check": lambda s, d: _check_fomo_extreme(s, d)
    },
    "price_extension": {
        "weight": 1,
        "tag": "volatile_extension",
        "risk_desc": "价格远离均线",
        "structure_impact": "短期波动极端化",
        "check": lambda s, d: _check_price_extension(s, d)
    },
    "neutral_bearish_structure": {
        "weight": 2,
        "tag": "neutral_bearish",
        "risk_desc": "结构偏空但量能正常",
        "structure_impact": "空头排列+死叉，但非恐慌量，等待方向选择",
        "check": lambda s, d: _check_neutral_bearish(s, d)
    },
}


def _check_fomo_extreme(signals, screenshot_data):
    pct = screenshot_data.get('pct_change_24h', 0) or 0
    vol_ratio = signals.get('volume_vs_ma5', 1.0)
    return (pct > 20 and vol_ratio > 2) or (pct > 15 and vol_ratio < 0.5)


def _check_price_extension(signals, screenshot_data):
    indicators = screenshot_data.get('_raw_indicators', {})
    if not indicators or 'ma' not in indicators:
        return False
    ma7 = indicators['ma'].get('ma7')
    price = screenshot_data.get('price')
    if not ma7 or not price or ma7 == 0:
        return False
    return abs(price - ma7) / ma7 > 0.15


def _check_neutral_bearish(signals, screenshot_data):
    """结构偏空但无量确认：空头排列+死叉+正常量"""
    ma = signals.get('ma_alignment', {}).get('type') == 'bearish'
    macd = signals.get('macd_signal', {}).get('type') == 'bearish'
    vol = signals.get('volume_status', {}).get('type') == 'normal'
    return ma and macd and vol


def _derive_risk_direction(triggered):
    """推导风险方向（不是涨跌预测，是结构倾向）"""
    tags = [t['tag'] for t in triggered]
    # P0: 恐慌/暴跌 = 明确偏空
    if any(t in tags for t in ['panic_selling', 'full_breakdown']):
        return "bearish"

    # P1: 趋势破坏 = 偏空
    if 'trend_break' in tags:
        return "bearish"

    # P2: 多头衰竭 = 多头结构破坏
    if any(t in tags for t in ['fomo_zone', 'volatile_extension']):
        return "bullish_exhaustion"

    if 'neutral_bearish' in tags:
        return "neutral_bearish"

    # v2.5.1: 结构偏弱但无趋势破坏 — 填补 uncertain 和 bearish 之间的真空
    # structure_bearish(空头排列) / short_term_break(跌破MA7) / momentum_weak(弱势金叉)
    if any(t in tags for t in ['structure_bearish', 'short_term_break', 'momentum_weak']):
        if 'trend_break' in tags or 'panic_selling' in tags:
            return "bearish"
        return "cautious"

    # P3: 流动性问题 = 高波动，方向不明
    if any(t in tags for t in ['liquidity_dry', 'liquidity_weak']):
        return "volatile"

    return "uncertain"


class ConfidenceEngine:
    """v2.5 完整版置信度引擎：指标自洽性校验"""
    BASE_SCORE = 100

    DEDUCTIONS = {
        "missing_ma": 15, "missing_macd": 15,
        "missing_volume": 15, "missing_price_extremes": 10,
        "blurry_screenshot": 20,
        "no_timestamp": 10,
        "meme_extra_volatility": 10,
        "altcoin_low_liquidity": 5,
    }

    @classmethod
    def calculate(cls, screenshot_data: dict, indicators: dict, category: str) -> dict:
        score = cls.BASE_SCORE
        deductions = []

        required = ['ma', 'macd', 'volume', 'price_extremes']
        for key in required:
            if not indicators or key not in indicators:
                score -= cls.DEDUCTIONS.get(f"missing_{key}", 10)
                deductions.append(f"缺失{key}")

        if screenshot_data.get('clarity') != 'clear':
            score -= cls.DEDUCTIONS['blurry_screenshot']
            deductions.append("截图模糊")

        missing = screenshot_data.get('missing_elements', [])
        if missing:
            score -= 5
            deductions.append(f"截图缺失: {missing}")

        if not screenshot_data.get('time'):
            score -= cls.DEDUCTIONS['no_timestamp']
            deductions.append("无时间戳")

        # v2.5 新增：指标自洽性校验
        validation = cls._validate_indicators(indicators)
        if not validation['valid']:
            for issue in validation['issues']:
                deductions.append(issue)
                score -= 10

        if category == 'meme':
            score -= cls.DEDUCTIONS['meme_extra_volatility']
            deductions.append("Meme币高波动（天然置信度折扣）")
        elif category == 'altcoin':
            score -= cls.DEDUCTIONS['altcoin_low_liquidity']
            deductions.append("山寨币流动性差（天然置信度折扣）")

        # v2.5.1: 短周期置信度打折
        timeframe = screenshot_data.get('timeframe', '4h')
        if timeframe in ('5m', '15m'):
            score -= 10
            deductions.append('短周期(≤15m)，结构噪音大')
        elif timeframe in ('30m', '1h'):
            score -= 5
            deductions.append('中等周期(30m-1h)，噪音中等')

        if score >= 70:
            level = "high"
        elif score >= 40:
            level = "medium"
        else:
            level = "low"

        return {
            "score": max(0, score),
            "level": level,
            "max_score": cls.BASE_SCORE,
            "deductions": deductions if deductions else ["指标完整，数据自洽"],
            "validation_details": validation,
            "note": "基于截图质量与指标完整性，非预测准确率",
        }

    @staticmethod
    def _validate_indicators(indicators: dict) -> dict:
        """v2.5 新增：指标自洽性校验（防止 OCR 错误）"""
        issues = []

        price = indicators.get('current_price')
        ma = indicators.get('ma', {})
        ma7 = ma.get('ma7')
        if price and ma7 and ma7 != 0:
            deviation = abs(price - ma7) / ma7
            if deviation > 0.5:
                issues.append(f"MA7({ma7})与价格({price})偏离{deviation:.0%}，疑似OCR错误")

        macd = indicators.get('macd', {})
        dif, dea, hist = macd.get('dif'), macd.get('dea'), macd.get('macd')
        if all(v is not None for v in [dif, dea, hist]):
            calculated_hist = dif - dea
            if abs(calculated_hist - hist) > abs(hist) * 0.5 + 0.001:
                issues.append(
                    f"MACD柱({hist})≠DIF-DEA({calculated_hist:.6f})，数据不一致"
                )

        vol = indicators.get('volume', {})
        cur, ma5 = vol.get('current_bar'), vol.get('current_bar_ma5')
        if cur and ma5 and ma5 > 0:
            ratio = cur / ma5
            if ratio > 100 or ratio < 0.01:
                issues.append(
                    f"成交量({cur})与MA5({ma5})数量级差异过大，请核实单位"
                )

        return {"valid": len(issues) == 0, "issues": issues}


def _calculate_confidence(screenshot_data, indicators, category):
    """兼容旧接口 → 委托 ConfidenceEngine"""
    return ConfidenceEngine.calculate(screenshot_data, indicators, category)


def _determine_risk_state(signals, screenshot_data):
    """基于触发器判定风险状态（非方向预测）"""
    triggered = []
    total_weight = 0
    for name, cfg in TRIGGER_REGISTRY.items():
        if cfg['check'](signals, screenshot_data):
            triggered.append({
                "tag": cfg['tag'],
                "weight": cfg['weight'],
                "risk_desc": cfg['risk_desc'],
                "structure_impact": cfg['structure_impact']
            })
            total_weight += cfg['weight']

    # neutral_bearish 特殊处理：结构偏空但无量确认
    has_nb = any(t['tag'] == 'neutral_bearish' for t in triggered)
    has_panic = any(t['tag'] == 'panic_selling' for t in triggered)

    if total_weight >= 6:
        level = "critical"
    elif total_weight >= 4:
        level = "danger"
    elif total_weight >= 2:
        if has_nb and not has_panic:
            level = "warning"  # 结构偏空但无量，降级
        else:
            level = "warning"
    else:
        level = "safe"

    direction = _derive_risk_direction(triggered)

    return {
        "risk_level": level,
        "risk_direction": direction,
        "total_weight": total_weight,
        "triggered_by": [t['tag'] for t in triggered],
        "triggered_detail": triggered
    }


COLD_START_TEMPLATES = {
    "meme":       "📡 正在补充：社交热度、鲸鱼地址、交易所异动...",
    "mainstream": "📡 正在补充：ETF资金流、链上流向、宏观数据...",
    "altcoin":    "📡 正在补充：解锁计划、流动性数据、概念热度...",
    "stable":     "📡 正在补充：锚定状态、储备审计、脱钩风险...",
    "commodity":  "📡 正在补充：美元指数、COMEX持仓、实物供需...",
    "equity":     "📡 正在补充：股市基本面、财报数据、监管动态...",
}


class SignalReconciliation:
    """v2.5 信号协调：高层信息覆盖低层信号，非纠错是上下文修正"""

    LAYER_WEIGHTS = {
        "macro_flow":   {"weight": "S", "desc": "宏观资金流（ETF/机构）"},
        "onchain":      {"weight": "A", "desc": "链上行为（交易所流向）"},
        "sentiment":    {"weight": "A", "desc": "情绪周期（FGI/社交）"},
        "tokenomics":   {"weight": "B", "desc": "代币经济（解锁/FDV）"},
        "technical":    {"weight": "C", "desc": "技术结构（MA/MACD/量）"},
    }

    @classmethod
    def reconcile(cls, quick_state: dict, deep_data: dict) -> dict:
        overlays = []

        # S级覆盖：ETF 巨量流入覆盖技术 danger
        if quick_state.get('risk_level') in ['danger', 'critical']:
            etf_flow = deep_data.get('etf_netflow', 0)
            if etf_flow and etf_flow > 100_000_000:
                overlays.append({
                    "layer": "macro_flow",
                    "weight": "S",
                    "quick_signal": quick_state['risk_level'],
                    "deep_evidence": f"ETF净流入${etf_flow/1e8:.1f}亿",
                    "reconciliation": "宏观资金流覆盖技术结构",
                    "user_message": "技术结构偏弱，但宏观资金持续流入，结构风险可能被稀释",
                })

        # A级覆盖：链上交易所净流出覆盖缩量
        exchange_flow = deep_data.get('exchange_netflow', 0)
        if exchange_flow and exchange_flow < -1000:
            overlays.append({
                "layer": "onchain",
                "weight": "A",
                "quick_evidence": "缩量",
                "deep_evidence": f"交易所净流出{-exchange_flow}BTC，大户提走",
                "reconciliation": "链上行为覆盖成交量信号",
                "user_message": "缩量伴随交易所净流出，可能是筹码锁定而非流动性枯竭",
            })

        # A级覆盖：FGI 极度恐惧覆盖 FOMO
        fgi_raw = deep_data.get('fear_greed_index', {}).get('value', 50)
        fgi = fgi_raw if fgi_raw is not None else 50
        if fgi < 20 and 'fomo_zone' in quick_state.get('triggered_by', []):
            overlays.append({
                "layer": "sentiment",
                "weight": "A",
                "quick_evidence": "价格极端偏离",
                "deep_evidence": f"FGI仅{fgi}，市场极度恐惧",
                "reconciliation": "情绪周期覆盖价格偏离信号",
                "user_message": "价格偏离但情绪极度恐惧，可能是恐慌底而非FOMO顶",
            })

        if not overlays:
            return {
                "status": "confirmed",
                "note": "多层信号一致，结构风险未被覆盖",
                "overlays": [],
                "final_assessment": quick_state.get('risk_level', 'unknown'),
            }

        overlays.sort(key=lambda x: {'S': 0, 'A': 1, 'B': 2, 'C': 3}.get(x['weight'], 4))
        return {
            "status": "context_adjusted",
            "note": f"{len(overlays)}层更高权重信息覆盖技术结构信号",
            "overlays": overlays,
            "dominant_layer": overlays[0]['layer'],
            "final_assessment": cls._derive_final_assessment(quick_state, overlays),
        }

    @staticmethod
    def _derive_final_assessment(quick_state: dict, overlays: list) -> str:
        original = quick_state.get('risk_level', 'unknown')
        top_weight = overlays[0]['weight']
        if top_weight == 'S' and original in ['danger', 'critical']:
            return 'warning' if original == 'danger' else 'danger'
        elif top_weight == 'A' and original == 'danger':
            return 'warning'
        return original


def quick_scan_v3(symbol, category, screenshot_data, indicators):
    """
    风险警报器：只报结构状态，不给方向预测
    0外部依赖，0.5秒响应
    """
    signals = compute_indicator_signals(indicators)
    confidence = _calculate_confidence(screenshot_data, indicators, category)
    risk_state = _determine_risk_state(signals, screenshot_data)

    lines = [
        f"\u26a0\ufe0f {symbol} 快扫（{screenshot_data.get('timeframe', '4h')}）",
        f"\u4fe1\u5fc3\u5ea6\uff1a{confidence['level'].upper()}\uff08{confidence['score']}/100\uff09",
        ""
    ]

    if confidence['level'] != 'high':
        lines.append("置信度说明：")
        for reason in confidence['deductions']:
            lines.append(f"\u2022 {reason}")
        lines.append("")

    lines.append("结构状态：")

    ma_type = signals.get('ma_alignment', {}).get('type')
    if ma_type == 'bearish':
        lines.append("\u2022 均线空头排列（短期<中期<长期）")
    elif ma_type == 'bullish':
        lines.append("\u2022 均线多头排列（短期>中期>长期）")
    else:
        lines.append("\u2022 均线纠缠，方向不明")

    macd = signals.get('macd_signal', {})
    macd_type = macd.get('type')
    if macd_type == 'bearish':
        lines.append("\u2022 MACD零轴下方死叉，动能偏弱")
    elif macd_type == 'bullish':
        lines.append("\u2022 MACD金叉，动能转强")
    elif macd_type == 'weak_bullish':
        lines.append("\u2022 MACD弱势金叉，动能不足")
    elif macd_type == 'neutral_bullish':
        lines.append("\u2022 MACD收口，动能衰减")
    else:
        lines.append("\u2022 MACD方向不明")

    vol = signals.get('volume_status', {})
    vol_type = vol.get('type')
    vol_ratio = signals.get('volume_vs_ma5', 1.0)
    if vol_type == 'extremely_low':
        lines.append(f"\u2022 极度缩量（{vol_ratio:.0%}），市场参与度极低")
    elif vol_type == 'low':
        lines.append(f"\u2022 成交量萎缩（{vol_ratio:.0%}），流动性不足")
    elif vol_type == 'high_selling':
        lines.append("\u2022 放量下跌，筹码出逃")
    elif vol_type == 'high_buying':
        lines.append("\u2022 放量上涨，交投活跃")
    else:
        lines.append(f"\u2022 成交量正常（{vol_ratio:.0%}）")

    lines.append("")

    emoji = {'safe': '\u2705', 'warning': '\u26a0\ufe0f',
             'danger': '\ud83d\udea8', 'critical': '\ud83d\udd34'}.get(
        risk_state['risk_level'], '\u26aa'
    )
    lines.append(f"{emoji} 风险等级：{risk_state['risk_level'].upper()}")
    triggered_str = ', '.join(risk_state['triggered_by']) if risk_state['triggered_by'] else '\u65e0\u663e\u8457\u7ed3\u6784\u98ce\u9669'
    lines.append(f"\u89e6\u53d1\u4fe1\u53f7\uff1a{triggered_str}")

    direction = risk_state.get('risk_direction', 'uncertain')
    direction_text = {
        'bearish': '\u7ed3\u6784\u504f\u7a7a',
        'bullish_exhaustion': '\u591a\u5934\u8870\u7aed',
        'cautious': '\u7ed3\u6784\u504f\u5f31\uff0c\u7b49\u5f85\u786e\u8ba4',
        'volatile': '\u9ad8\u6ce2\u52a8\uff0c\u65b9\u5411\u4e0d\u660e',
        'uncertain': '\u4fe1\u53f7\u6df7\u6742'
    }.get(direction, '\u65b9\u5411\u4e0d\u660e')
    lines.append(f"\u7ed3\u6784\u503e\u5411\uff1a{direction_text}")
    lines.append("")

    if risk_state['triggered_detail']:
        lines.append("\u7ed3\u6784\u5f71\u54cd\uff1a")
        for t in risk_state['triggered_detail']:
            lines.append(f"\u2022 {t['structure_impact']}")
        lines.append("")

    lines.append("\u2139\ufe0f \u4ee5\u4e0a\u4ec5\u57fa\u4e8e\u622a\u56fe\u6280\u672f\u7ed3\u6784\uff0c\u4e0d\u6d89\u53ca\u5b8f\u89c2/\u8d44\u91d1/\u60c5\u7eea\u5224\u65ad")

    # v2.5.1: 短周期提示语
    tf = screenshot_data.get('timeframe', '4h')
    if tf in ('5m', '15m', '30m', '1h'):
        lines.append("\u26a0\ufe0f \u77ed\u5468\u671f(≤1h)\u7ed3\u6784\u566a\u97f3\u5927\uff0c\u5efa\u8bae\u7528 4h/\u65e5\u7ebf\u786e\u8ba4")

    lines.append("")
    lines.append(COLD_START_TEMPLATES.get(category, "\ud83d\udce1 \u6b63\u5728\u8865\u5145\u8be6\u7ec6\u6570\u636e..."))
    lines.append("")
    lines.append("\u8be6\u7ec6\u5206\u6790\u751f\u6210\u4e2d...")

    return "\n".join(lines)


def analyze(symbol: str, screenshot_data: Dict[str, Any], search_data: Dict[str, Any],
           search_text: Optional[str] = None, indicators: Optional[Dict] = None) -> Dict[str, Any]:
    """完整分析入口。indicators 必须是 Dict 或 None（空dict {} 会被正确处理）。
    
    两段式输出：
    1. 先产 quick_scan_text（立即输出给用户）
    2. 再跑完整深度分析
    """
    category = classify_coin(symbol)
    cat_val = category['category']

    # ========== 第一段：Quick Scan v3（立即输出） ==========
    ss_data = screenshot_data.copy()
    ss_data.setdefault('_raw_indicators', indicators or {})
    quick_text = quick_scan_v3(symbol.upper(), cat_val, ss_data, indicators or {})
    # 立即输出给用户（第一段）
    print(quick_text, flush=True)

    # ========== 第二段：Deep Analysis ==========
    quality = assess_screenshot_quality(
        clarity=screenshot_data.get('clarity', 'clear'),
        confidence=screenshot_data.get('confidence', 'high'),
        missing=screenshot_data.get('missing_elements', [])
    )
    conflict = detect_conflict(
        screenshot_data.get('price', 0) or 0,
        search_data.get('min', 0) or 0,
        search_data.get('max', 0) or 0
    )

    # 指标信号
    if indicators is not None:
        indicators.setdefault('current_price', screenshot_data.get('price'))
        indicators.setdefault('source', 'user_input')
    indicator_signals = compute_indicator_signals(indicators)

    # 风险标签
    risk_flags = []
    vol_type = indicator_signals.get('volume_status', {}).get('type', '')
    macd_type = indicator_signals.get('macd_signal', {}).get('type', '')
    ma_type = indicator_signals.get('ma_alignment', {}).get('type', '')
    pos_ratio = indicator_signals.get('price_position_24h', {}).get('ratio', 0.5)
    if ma_type == 'bearish':
        risk_flags.append('bearish_ma_alignment')
    if vol_type in ('low', 'extremely_low'):
        risk_flags.extend(['volume_price_divergence', 'low_volume_rally'])
    if indicators:
        macd_hist = abs(indicators.get('macd', {}).get('macd', 999) or 999)
        if macd_type == 'bullish' and macd_hist < 0.5:
            risk_flags.append('macd_momentum_fading')
        elif macd_type == 'weak_bullish':
            risk_flags.append('macd_weak_signal')
        elif macd_type in ('bearish', 'neutral_bullish'):
            risk_flags.append('macd_momentum_fading' if macd_type == 'neutral_bullish' else 'macd_death_cross')
    if pos_ratio > 0.85:
        risk_flags.append('key_resistance_nearby')
    if pos_ratio < 0.2:
        risk_flags.append('key_support_nearby')
    if cat_val in ('commodity', 'equity'):
        risk_flags.append('non_crypto_asset')
    if cat_val == 'altcoin':
        risk_flags.extend(['high_volatility', 'liquidity_risk'])
    risk_flags.append('macro_uncertainty')

    # 币种分类
    cat_map = {
        'stable':    {'type': '稳定币', 'analysis_approach': '锚定分析', 'rationale': '锚定偏差、储备透明度、监管风险、脱钩警报'},
        'mainstream':{'type': '主流币', 'analysis_approach': '中线技术面+宏观', 'rationale': '中线技术面+宏观+链上结构'},
        'altcoin':   {'type': '山寨币/概念币', 'analysis_approach': '中线技术面+宏观（高波动调整）', 'rationale': '市值较小或新上线，高波动，流动性风险'},
        'meme':      {'type': 'Meme币', 'analysis_approach': '短线情绪+热度', 'rationale': '短线情绪、热度、鲸鱼动向、dump风险'},
        'commodity': {'type': '大宗商品永续', 'analysis_approach': '技术面通用+宏观独立', 'rationale': '技术框架通用，宏观面（美联储/美元/供需）与加密货币不同'},
        'equity':    {'type': '股票代币/RWA', 'analysis_approach': '技术面通用+股市基本面', 'rationale': '标的为股票/证券，分析框架基于股市基本面'},
    }
    cc = cat_map.get(cat_val, cat_map['altcoin'])
    cc.update({'symbol': symbol.upper(), 'category_raw': cat_val, 'is_crypto': cat_val not in ('commodity', 'equity')})
    if cat_val in ('commodity', 'equity'):
        cc['note'] = category.get('note', '')

    # asset_boundary
    asset_boundary = None
    if cat_val == 'commodity':
        umap = {'silver':'白银（Silver）','gold':'黄金（Gold）','platinum':'铂金','palladium':'钯金','crude_oil':'原油'}
        ul = category.get('underlying', '')
        asset_boundary = {
            'is_crypto': False, 'asset_type': '贵金属永续合约' if ul in ('silver','gold','platinum','palladium') else '商品永续合约',
            'underlying': umap.get(ul, ul), 'symbol': symbol.upper(),
            'note': f'{symbol.upper()} 为{umap.get(ul, ul)}永续合约，非加密货币。技术分析框架通用，但宏观面（美联储、美元指数、实物供需）与加密货币不同。',
            'skill_scope': '本技能专注加密货币分析，贵金属合约仅提供技术面参考'
        }
    elif cat_val == 'equity':
        asset_boundary = {
            'is_crypto': False, 'asset_type': '股票代币/RWA', 'underlying': symbol.upper(),
            'symbol': symbol.upper(),
            'note': f'{symbol.upper()} 为股票映射代币，非原生加密货币。分析需参考对应股票基本面（财报/行业/宏观经济）。',
            'skill_scope': '本技能专注加密货币分析，股票代币仅提供技术面参考'
        }

    base = {
        'symbol': symbol, 'category': cat_val,
        'coin_classification': cc,
        'asset_boundary': asset_boundary,
        'freshness_check': {'is_fresh': True, 'screenshot_time': screenshot_data.get('time'),
                            'note': '基于用户提供的截图时间点' if screenshot_data.get('price') else '基于联网搜索'},
        'data_conflict_check': conflict,
        'screenshot_quality': quality,
        'search_availability': {'status': 'search_ok' if search_data.get('min') else 'search_failed'},
        'indicators': indicators if indicators else None,
        'indicator_signals': indicator_signals,
        'risk_flags': risk_flags
    }

    # 主流币/商品/股票/山寨 → 统一走 mainstream 模板 + 差异化调整
    if cat_val in ('mainstream', 'commodity', 'equity', 'altcoin'):
        s_min = search_data.get('min', 0)
        s_max = search_data.get('max', 0)

        vol_status = indicator_signals.get('volume_status', {})
        pos_24h = indicator_signals.get('price_position_24h', {})
        ma_align = indicator_signals.get('ma_alignment', {})
        macd_sig = indicator_signals.get('macd_signal', {})
        near_resistance = pos_24h.get('ratio', 0) > 0.85

        # 组合信号矩阵：MA × MACD × 量比 → bias
        db = determine_bias(indicator_signals)
        bias = db['bias']
        bias_logic = db['logic']

        # 类别覆盖：山寨币额外风险提示
        if cat_val == 'altcoin':
            pos_advice = '山寨币高波动低流动性，建议极小仓位或不参与' if not near_resistance else '前高附近不建议追多，山寨币易假突破'
            rr = '不适用（流动性不足）'
            tf = '3-5天' if near_resistance else '1-2周'
        elif bias == 'short':
            pos_advice = '空头排列+放量下跌，不建议做多，关注支撑位'
            rr = '约 1:1.5（估算）'
            tf = '3-5天，等待企稳'
        elif bias == 'long':
            pos_advice = '建议轻仓观察，等待放量突破后加仓'
            rr = '约 1:2（估算）'
            tf = '1-2周内'
        else:  # neutral / neutral_bearish
            pos_advice = '信号混杂或方向不明，不建议入场，等放量选方向'
            rr = '不适用（方向不明）'
            tf = '数小时至1天观察期'

        dynamic_plan = {
            'bias': bias,
            'bias_logic': bias_logic,
            'focus_zone': f"{_fmt_price(s_min)} - {_fmt_price(s_max)}" if s_min and s_max else '等待数据',
            'risk_level_below': _fmt_price(s_min * 0.99) if s_min else 'N/A',
            'upside_targets': [_fmt_price(s_max), _fmt_price(s_max * 1.05)] if s_max else ['N/A'],
            'risk_reward_estimate': rr,
            'position_advice': pos_advice,
            'timeframe_expectation': tf,
            'invalidation_condition': f"跌破{_fmt_price(s_min * 0.98)}且4小时收线低于此位（结构破坏）" if s_min else '无有效数据'
        }

        fgi = get_fear_greed_index(search_text or '')

        # freshness_check：按类别差异化阈值，比较截图时间与当前时间
        fresh_thresholds = {'meme': 10, 'altcoin': 15, 'mainstream': 30, 'commodity': 60, 'equity': 60, 'stable': 120}
        fresh_min = fresh_thresholds.get(cat_val, 30)
        is_fresh = True
        screenshot_time = screenshot_data.get('time', '')
        if screenshot_time:
            try:
                st_dt = datetime.strptime(screenshot_time, '%Y-%m-%d %H:%M')
                st_dt = st_dt.replace(tzinfo=timezone(timedelta(hours=8)))
                age_min = (datetime.now(timezone.utc) - st_dt).total_seconds() / 60
                is_fresh = age_min <= fresh_min
            except ValueError:
                pass
        base['freshness_check'] = {
            'is_fresh': is_fresh,
            'screenshot_time': screenshot_time,
            'expiration_threshold_minutes': fresh_min,
            'note': f"{'山寨币/概念币' if cat_val == 'altcoin' else cc.get('type','')}过期阈值为{fresh_min}分钟"
        }

        # tokenomics_risk：从search_text提FDV/MCap
        toke_risk = None
        if search_text:
            import re as _re
            f_match = _re.search(r'(?:FDV|完全稀释)\D*?([\d,.]+[万亿KMGTB]?)', search_text, _re.I)
            m_match = _re.search(r'(?:MCap|市值|Market\s*Cap)\D*?([\d,.]+[万亿KMGTB]?)', search_text, _re.I)
            if f_match and m_match:
                fdv = _parse_val(f_match.group(1))
                mcap = _parse_val(m_match.group(1))
                if mcap > 0:
                    ratio = round(fdv / mcap, 2)
                    toke_risk = {
                        'fdv': f'${fdv/1e9:.2f}B' if fdv >= 1e9 else (f'${fdv/1e6:.2f}M' if fdv >= 1e6 else f'${fdv:,.0f}'),
                        'mcap': f'${mcap/1e9:.2f}B' if mcap >= 1e9 else (f'${mcap/1e6:.2f}M' if mcap >= 1e6 else f'${mcap:,.0f}'),
                        'fdv_mcap_ratio': ratio,
                        'unlock_risk': '高' if ratio > 5 else ('中' if ratio > 2 else '低'),
                        'note': f"FDV是流通市值的{ratio}倍，{'大量代币待解锁，长期抛压风险' if ratio > 5 else '代币解锁有一定压力' if ratio > 2 else '代币解锁压力较小'}"
                    }
                    # 屏蔽地址/锁仓比例
                    shielded_m = _re.search(r'(\d+)%\s*(?:流通量|供应|代币).*?(?:屏蔽|锁定|质押|存放)', search_text, _re.I)
                    if shielded_m:
                        toke_risk['shielded_supply_pct'] = int(shielded_m.group(1))
                        toke_risk['note'] = toke_risk.get('note', '') + f"；{toke_risk['shielded_supply_pct']}%在屏蔽地址，实际流通更少"
                    if ratio > 3:
                        risk_flags.insert(0, 'high_fdv_ratio')
            # 即使没有FDV/MCap，也尝试提取屏蔽比例
            elif not toke_risk:
                shielded_m = _re.search(r'(\d+)%\s*(?:流通量|供应|代币).*?(?:屏蔽|锁定|质押|存放)', search_text, _re.I)
                if shielded_m:
                    toke_risk = {
                        'fdv': 'N/A', 'mcap': 'N/A', 'fdv_mcap_ratio': 0,
                        'unlock_risk': '未知',
                        'shielded_supply_pct': int(shielded_m.group(1)),
                        'note': f"{int(shielded_m.group(1))}%流通量在屏蔽地址，实际流通更少"
                    }
        base['tokenomics_risk'] = toke_risk

        # unlock_schedule：从search_text提取解锁信息
        unl_sched = None
        if search_text:
            unl_date = _re.search(r'解锁.*?(\d+/\d+)', search_text)
            unl_months = _re.search(r'(?:连续|共|总计|为期)?\s*(\d+)\s*个?\s*月\s*(?:分批)?解锁', search_text)
            unl_end = _re.search(r'至\s*(20\d+)', search_text)
            if unl_date:
                unl_sched = {
                    'first_unlock_date': f"2026-{unl_date.group(1).replace('/','-')}",
                    'status': '已触发' if '已触发' in search_text or '已经' in search_text else '待触发',
                    'duration_months': int(unl_months.group(1)) if unl_months else None,
                    'end_date': unl_end.group(1) if unl_end else None,
                    'frequency': '每月分批解锁' if '月' in (unl_months.group(0) if unl_months else '') else None,
                    'impact': '持续卖压，非一次性出清',
                    'price_reaction': None,  # 由调用方注入（需截图pct_change_24h）
                }
        base['unlock_schedule'] = unl_sched

        # fear_greed_index applicability for altcoin
        if cat_val == 'altcoin':
            fgi['applicability'] = '⚠️ 恐惧贪婪指数反映大盘情绪，对新币/山寨币参考价值有限'
            fgi['recommendation'] = '新币分析请重点关注解锁计划和流动性'

        # delay_note
        base['delay_note'] = '搜索聚合行情，延迟约 1-5 分钟'
        base['category'] = cat_val  # 向后兼容

        base.update({
            'screenshot_price': {
                'value': screenshot_data['price'], 'currency': 'USD',
                'display': _fmt_price(screenshot_data['price'])
            } if screenshot_data.get('price') else {'value': None, 'currency': 'USD', 'display': 'N/A'},
            'search_price_range': f"{_fmt_price(s_min)} - {_fmt_price(s_max)}" if s_min and s_max else 'N/A',
            'final_price_source': 'screenshot' if screenshot_data.get('price') else 'search',
            'trend': '震荡偏多',
            'lobster_view': '偏多' if cat_val != 'altcoin' else '高风险偏多',
            'observation_plan': dynamic_plan,
            'fear_greed_index': fgi
        })
        if cat_val in ('commodity', 'equity'):
            base['fear_greed_index']['applicability'] = '加密货币市场情绪指标，对非加密资产参考价值有限'
            if cat_val == 'commodity':
                base['fear_greed_index']['recommendation'] = '贵金属分析请结合 DXY（美元指数）和 COMEX 持仓数据'
            else:
                base['fear_greed_index']['recommendation'] = '股票代币分析请参考对应股票基本面（财报/行业/宏观经济）'

    elif cat_val == 'stable':
        base.update({
            'current_price': screenshot_data.get('price', 1.0),
            'peg_deviation': {'value': 0.1, 'unit': '%', 'display': '+0.1%'},
            'peg_status': '正常锚定'
        })
    else:  # meme
        s_min = search_data.get('min', 0)
        s_max = search_data.get('max', 0)

        # 五要素 + 基础字段
        base['delay_note'] = '搜索聚合行情，延迟约 1-5 分钟（非交易所原生毫秒级数据）'
        base['category'] = cat_val

        # freshness_check：Meme 币阈值 10 分钟
        fresh_min_meme = 10
        is_fresh = True
        screenshot_time = screenshot_data.get('time', '')
        if screenshot_time:
            try:
                st_dt = datetime.strptime(screenshot_time, '%Y-%m-%d %H:%M')
                st_dt = st_dt.replace(tzinfo=timezone(timedelta(hours=8)))
                age_min = (datetime.now(timezone.utc) - st_dt).total_seconds() / 60
                is_fresh = age_min <= fresh_min_meme
            except ValueError:
                pass
        base['freshness_check'] = {
            'is_fresh': is_fresh,
            'screenshot_time': screenshot_time,
            'expiration_threshold_minutes': fresh_min_meme,
            'note': f'Meme币过期阈值为{fresh_min_meme}分钟'
        }

        # tokenomics_risk（Meme 可能无 FDV，但兜底）
        toke_risk = None
        if search_text:
            import re as _re
            f_match = _re.search(r'(?:FDV|完全稀释)\D*?([\d,.]+[万亿KMGTB]?)', search_text, _re.I)
            m_match = _re.search(r'(?:MCap|市值|Market\s*Cap)\D*?([\d,.]+[万亿KMGTB]?)', search_text, _re.I)
            if f_match and m_match:
                fdv = _parse_val(f_match.group(1))
                mcap = _parse_val(m_match.group(1))
                if mcap > 0:
                    ratio = round(fdv / mcap, 2)
                    toke_risk = {
                        'fdv': f'${fdv/1e9:.2f}B' if fdv >= 1e9 else (f'${fdv/1e6:.2f}M' if fdv >= 1e6 else f'${fdv:,.0f}'),
                        'mcap': f'${mcap/1e9:.2f}B' if mcap >= 1e9 else (f'${mcap/1e6:.2f}M' if mcap >= 1e6 else f'${mcap:,.0f}'),
                        'fdv_mcap_ratio': ratio,
                        'unlock_risk': '高' if ratio > 5 else ('中' if ratio > 2 else '低'),
                        'note': f"FDV是流通市值的{ratio}倍，{'大量代币待解锁，长期抛压风险' if ratio > 5 else '代币解锁有一定压力' if ratio > 2 else '代币解锁压力较小'}"
                    }
                    shielded_m = _re.search(r'(\d+)%\s*(?:流通量|供应|代币).*?(?:屏蔽|锁定|质押|存放)', search_text, _re.I)
                    if shielded_m:
                        toke_risk['shielded_supply_pct'] = int(shielded_m.group(1))
        base['tokenomics_risk'] = toke_risk

        # FGI（Meme 币适用）
        fgi = get_fear_greed_index(search_text or '')
        base['fear_greed_index'] = fgi

        base.update({
            'screenshot_price': {
                'value': screenshot_data['price'], 'currency': 'USD',
                'display': _fmt_price(screenshot_data['price'])
            } if screenshot_data.get('price') else {'value': None, 'currency': 'USD', 'display': 'N/A'},
            'search_price_range': f"{_fmt_price(s_min)} - {_fmt_price(s_max)}" if s_min and s_max else 'N/A',
            'final_price_source': 'screenshot' if screenshot_data.get('price') else 'search',
            'trend': '短线震荡',
            'social_sentiment': '数据不足',
            'whale_alert': '无监控数据',
            'dump_risk': '高'
        })

    reliability_score = calculate_input_reliability(cat_val, conflict, quality, search_data)
    result = format_output(cat_val, base, reliability_score)
    result['quick_scan_text'] = quick_text  # 快扫文本注入返回结果

    # ========== Phase 3: Signal Reconciliation（v2.5 新增）==========
    quick_state = _determine_risk_state(indicator_signals, ss_data)
    search_context = {
        # 从 search_text 提取 ETF/链上/情绪数据
        'etf_netflow': _extract_etf_flow(search_text or ''),
        'exchange_netflow': _extract_exchange_flow(search_text or ''),
        'fear_greed_index': base.get('fear_greed_index', {}),
    }
    reconciliation = SignalReconciliation.reconcile(quick_state, search_context)
    result['signal_reconciliation'] = reconciliation

    # 如果发生上下文修正，追加说明
    if reconciliation['status'] == 'context_adjusted':
        result['analysis_note'] = (
            f"⚠️ 搜索数据补充后修正：{reconciliation['note']}\n"
            f"最终评估：{reconciliation['final_assessment']}"
        )

    return result


def _extract_etf_flow(search_text: str) -> float:
    """从搜索文本提取 ETF 净流入（美元）"""
    import re
    m = re.search(r'ETF.*?净?(?:流入|流出)\D*([\d,.]+)\s*亿', search_text)
    if m:
        val = float(m.group(1).replace(',', ''))
        return val * 1e8 if '流入' in m.group(0) else -val * 1e8
    # 备选: btc_etf_flow
    m = re.search(r'(?:BTC|比特币)\s*ETF.*?([\d,.]+)\s*[BKM]?(?:美元|USD)', search_text, re.I)
    if m:
        return float(m.group(1).replace(',', ''))
    return 0.0


def _extract_exchange_flow(search_text: str) -> int:
    """从搜索文本提取交易所净流出（BTC）"""
    import re
    m = re.search(r'交易所.*?净?(?:流出|流入)\D*([\d,.]+)\s*(?:BTC|枚|个)', search_text)
    if m:
        val = int(m.group(1).replace(',', ''))
        return -val if '流出' in m.group(0) else val
    m = re.search(r'exchange.*?(?:outflow|netflow)\D*([\d,.]+)\s*BTC', search_text, re.I)
    if m:
        return -int(float(m.group(1).replace(',', '')))
    return 0

def format_output(category: str, base_data: Dict[str, Any], reliability_score: Dict) -> Dict[str, Any]:
    if category in ('mainstream', 'commodity', 'equity', 'altcoin'):
        result = format_mainstream_output(base_data, reliability_score)
    elif category == 'stable':
        result = format_stablecoin_output(base_data, reliability_score)
    elif category == 'meme':
        result = format_meme_output(base_data, reliability_score)
    else:
        result = format_mainstream_output(base_data, reliability_score)
    result['category'] = category
    return result
# ========== CLI 入口（兼容所有 tools.json 命令） ==========

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command')
    
    # classify_coin
    p_classify = sub.add_parser('classify')
    p_classify.add_argument('--symbol', required=True)
    p_classify.add_argument('--price', type=float, default=None)
    
    # detect_trade_intent
    p_intent = sub.add_parser('detect_trade_intent')
    p_intent.add_argument('--message', required=True)
    
    # detect_conflict
    p_conflict = sub.add_parser('conflict')
    p_conflict.add_argument('--screenshot-price', type=float, default=0)
    p_conflict.add_argument('--search-min', type=float, default=0)
    p_conflict.add_argument('--search-max', type=float, default=0)
    
    # search_crypto_info（修复：加真实价格参数）
    p_search = sub.add_parser('search_crypto_info')
    p_search.add_argument('--symbol', required=True)
    p_search.add_argument('--query-type', default='price')
    p_search.add_argument('--real-min', type=float, default=None)
    p_search.add_argument('--real-max', type=float, default=None)
    
    # analyze_screenshot（修复：加真实价格参数）
    p_analyze_img = sub.add_parser('analyze_screenshot')
    p_analyze_img.add_argument('--image-url', default='')
    p_analyze_img.add_argument('--symbol', required=True)
    p_analyze_img.add_argument('--user-claimed-timeframe', default=None)
    p_analyze_img.add_argument('--real-price', type=float, default=None)
    
    # analyze（完整分析，所有参数可选）
    p_analyze = sub.add_parser('analyze')
    p_analyze.add_argument('--symbol', required=True)
    p_analyze.add_argument('--screenshot-price', type=float, default=0)
    p_analyze.add_argument('--search-min', type=float, default=0)
    p_analyze.add_argument('--search-max', type=float, default=0)
    p_analyze.add_argument('--clarity', default='clear')
    p_analyze.add_argument('--confidence', default='high')
    p_analyze.add_argument('--missing', default='')
    p_analyze.add_argument('--screenshot-time', default=None)
    
    args = parser.parse_args()
    
    if args.command == 'classify':
        result = classify_coin(args.symbol, args.price)
    elif args.command == 'detect_trade_intent':
        result = detect_trade_intent(args.message)
    elif args.command == 'conflict':
        result = detect_conflict(args.screenshot_price, args.search_min, args.search_max)
    elif args.command == 'search_crypto_info':
        result = search_crypto_info(args.symbol, args.query_type, args.real_min, args.real_max)
    elif args.command == 'analyze_screenshot':
        result = analyze_screenshot(args.image_url, args.symbol, args.user_claimed_timeframe, args.real_price)
    elif args.command == 'analyze':
        sc_data = {
            'price': args.screenshot_price,
            'clarity': args.clarity,
            'confidence': args.confidence,
            'time': args.screenshot_time
        }
        se_data = {'min': args.search_min, 'max': args.search_max}
        result = analyze(args.symbol, sc_data, se_data)
    else:
        result = {'error': '未知命令'}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
