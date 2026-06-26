#!/usr/bin/env python3
"""
CryptoScope - 加密货币数据分析助手 v1.0.0（付费版）
实时价格查询、技术指标分析、交易信号生成
集成 SkillPay 计费系统
"""
import sys
import json
import argparse
from datetime import datetime
import requests

# ═══════════════════════════════════════════════════
# SkillPay Billing Configuration / 计费配置
# ═══════════════════════════════════════════════════
BILLING_API_URL = 'https://skillpay.me'
BILLING_API_KEY = 'sk_0de94ea93e9aca73aafc2b6457b8de378389a21661f9c6ad4e6b7929e390e971'
SKILL_ID = '0c9fb051-d210-46c4-b4d8-67f6cb6ba624'  # SkillPay正式ID（2026-03-08更新）

PRICE_PER_CALL = 0.05  # USDT / 次

# ═══════════════════════════════════════════════════
# Billing Functions / 计费函数
# ═══════════════════════════════════════════════════

def check_balance(user_id: str) -> dict:
    """
    查询用户余额
    
    Returns:
        {
            "ok": bool,
            "balance": float,
            "payment_url": str (if balance insufficient)
        }
    """
    try:
        resp = requests.post(
            f"{BILLING_API_URL}/api/v1/billing/balance",
            headers={
                "X-API-Key": BILLING_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "user_id": user_id,
                "skill_id": SKILL_ID
            },
            timeout=5
        )
        
        data = resp.json()
        
        if data.get("success"):
            return {"ok": True, "balance": data.get("balance")}
        else:
            return {
                "ok": False,
                "balance": data.get("balance", 0),
                "payment_url": data.get("payment_url")
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}


def charge_user(user_id: str, amount: float = PRICE_PER_CALL) -> dict:
    """
    扣费
    
    Returns:
        {
            "ok": bool,
            "balance": float (if success),
            "payment_url": str (if balance insufficient)
        }
    """
    try:
        resp = requests.post(
            f"{BILLING_API_URL}/api/v1/billing/charge",
            headers={
                "X-API-Key": BILLING_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "user_id": user_id,
                "skill_id": SKILL_ID,
                "amount": amount,
                "currency": "USDT"
            },
            timeout=5
        )
        
        data = resp.json()
        
        if data.get("success"):
            return {
                "ok": True,
                "balance": data.get("balance")
            }
        else:
            return {
                "ok": False,
                "balance": data.get("balance", 0),
                "payment_url": data.get("payment_url")
            }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ═══════════════════════════════════════════════════
# CoinGecko API（免费，无需Key）
# ═══════════════════════════════════════════════════

def get_crypto_price(coin_id: str) -> dict:
    """
    获取加密货币实时价格
    
    Args:
        coin_id: 币种ID（如bitcoin, ethereum）
    
    Returns:
        {
            "symbol": str,
            "name": str,
            "price": float,
            "change_24h": float,
            "volume_24h": float,
            "market_cap": float
        }
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        market_data = data['market_data']
        
        return {
            "symbol": coin_id,
            "name": data['name'],
            "price": market_data['current_price']['usd'],
            "change_24h": market_data['price_change_percentage_24h'],
            "volume_24h": market_data['total_volume']['usd'],
            "market_cap": market_data['market_cap']['usd'],
            "timestamp": int(datetime.now().timestamp())
        }
    
    except Exception as e:
        return {"error": str(e)}


def get_price_history(coin_id: str, days: int = 90) -> list:
    """
    获取历史价格
    
    Args:
        coin_id: 币种ID
        days: 天数
    
    Returns:
        [price1, price2, ...]
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days
        }
        
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        prices = [price[1] for price in data['prices']]
        
        return prices
    
    except Exception as e:
        return []


# ═══════════════════════════════════════════════════
# 技术指标计算
# ═══════════════════════════════════════════════════

def calculate_ma(prices: list, period: int) -> float:
    """计算移动平均线"""
    if len(prices) < period:
        return prices[-1] if prices else 0
    return sum(prices[-period:]) / period


def calculate_rsi(prices: list, period: int = 14) -> float:
    """计算RSI"""
    if len(prices) < period + 1:
        return 50.0
    
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [max(change, 0) for change in changes[-period:]]
    losses = [abs(min(change, 0)) for change in changes[-period:]]
    
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices: list) -> dict:
    """计算MACD"""
    if len(prices) < 26:
        return {"macd": 0, "signal": 0, "trend": "neutral"}
    
    # 简化计算
    ema_12 = sum(prices[-12:]) / 12
    ema_26 = sum(prices[-26:]) / 26
    
    macd = ema_12 - ema_26
    signal = macd * 0.2
    
    if macd > signal:
        trend = "bullish"
    elif macd < signal:
        trend = "bearish"
    else:
        trend = "neutral"
    
    return {
        "macd": round(macd, 2),
        "signal": round(signal, 2),
        "trend": trend
    }


def generate_signal(current_price: float, indicators: dict) -> dict:
    """
    生成交易信号
    
    Returns:
        {
            "signal": "BUY" | "SELL" | "HOLD",
            "confidence": float,
            "reasons": list
        }
    """
    signals = []
    reasons = []
    
    # MA信号（权重30%）
    if indicators['ma_20'] > indicators['ma_50']:
        signals.append(("BUY", 0.3))
        reasons.append("MA20 > MA50（多头趋势）")
    elif indicators['ma_20'] < indicators['ma_50']:
        signals.append(("SELL", 0.3))
        reasons.append("MA20 < MA50（空头趋势）")
    else:
        signals.append(("HOLD", 0.3))
        reasons.append("MA趋势中性")
    
    # RSI信号（权重30%）
    if indicators['rsi'] < 30:
        signals.append(("BUY", 0.3))
        reasons.append(f"RSI={indicators['rsi']:.1f}（超卖）")
    elif indicators['rsi'] > 70:
        signals.append(("SELL", 0.3))
        reasons.append(f"RSI={indicators['rsi']:.1f}（超买）")
    else:
        signals.append(("HOLD", 0.3))
        reasons.append(f"RSI={indicators['rsi']:.1f}（健康区间）")
    
    # MACD信号（权重40%）
    if indicators['macd']['trend'] == 'bullish':
        signals.append(("BUY", 0.4))
        reasons.append("MACD金叉（看涨）")
    elif indicators['macd']['trend'] == 'bearish':
        signals.append(("SELL", 0.4))
        reasons.append("MACD死叉（看跌）")
    else:
        signals.append(("HOLD", 0.4))
        reasons.append("MACD趋势中性")
    
    # 计算综合信号
    buy_score = sum(weight for signal, weight in signals if signal == "BUY")
    sell_score = sum(weight for signal, weight in signals if signal == "SELL")
    hold_score = sum(weight for signal, weight in signals if signal == "HOLD")
    
    max_score = max(buy_score, sell_score, hold_score)
    
    if max_score == buy_score:
        final_signal = "BUY"
        confidence = buy_score
    elif max_score == sell_score:
        final_signal = "SELL"
        confidence = sell_score
    else:
        final_signal = "HOLD"
        confidence = hold_score
    
    # 风险评估
    if confidence > 0.7:
        risk_level = "low"
    elif confidence > 0.5:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    return {
        "signal": final_signal,
        "confidence": round(confidence, 2),
        "reasons": reasons,
        "risk_level": risk_level
    }


# ═══════════════════════════════════════════════════
# 付费接口
# ═══════════════════════════════════════════════════

def get_price_paid(coin_id: str, user_id: str) -> dict:
    """
    获取实时价格（付费版）
    """
    # 1. 检查余额
    balance_check = check_balance(user_id)
    
    if not balance_check.get("ok"):
        return {
            "error": "余额不足",
            "balance": balance_check.get("balance", 0),
            "payment_url": balance_check.get("payment_url"),
            "message": "请充值后继续使用（最低充值$8）"
        }
    
    # 2. 获取数据
    crypto_data = get_crypto_price(coin_id)
    
    if "error" in crypto_data:
        return {
            "error": "获取数据失败",
            "message": crypto_data["error"]
        }
    
    # 3. 扣费
    charge_result = charge_user(user_id)
    
    if not charge_result.get("ok"):
        return {
            "error": "扣费失败",
            "balance": charge_result.get("balance", 0),
            "payment_url": charge_result.get("payment_url"),
            "message": "余额不足，请充值"
        }
    
    # 4. 返回结果
    result = crypto_data.copy()
    result["charged"] = PRICE_PER_CALL
    result["balance"] = charge_result.get("balance")
    
    return result


def analyze_paid(coin_id: str, user_id: str) -> dict:
    """
    技术分析（付费版）
    """
    # 1. 检查余额
    balance_check = check_balance(user_id)
    
    if not balance_check.get("ok"):
        return {
            "error": "余额不足",
            "balance": balance_check.get("balance", 0),
            "payment_url": balance_check.get("payment_url"),
            "message": "请充值后继续使用（最低充值$8）"
        }
    
    # 2. 获取数据
    prices = get_price_history(coin_id, 90)
    
    if not prices:
        return {
            "error": "获取历史数据失败",
            "message": "请检查币种名称或稍后重试"
        }
    
    crypto_data = get_crypto_price(coin_id)
    
    if "error" in crypto_data:
        return {
            "error": "获取实时价格失败"
        }
    
    # 3. 技术分析
    indicators = {
        "ma_20": calculate_ma(prices, 20),
        "ma_50": calculate_ma(prices, 50),
        "rsi": calculate_rsi(prices),
        "macd": calculate_macd(prices)
    }
    
    # 4. 扣费
    charge_result = charge_user(user_id)
    
    if not charge_result.get("ok"):
        return {
            "error": "扣费失败",
            "balance": charge_result.get("balance", 0),
            "payment_url": charge_result.get("payment_url"),
            "message": "余额不足，请充值"
        }
    
    # 5. 返回结果
    return {
        "symbol": coin_id,
        "name": crypto_data.get("name"),
        "price": crypto_data.get("price"),
        "change_24h": crypto_data.get("change_24h"),
        "indicators": indicators,
        "charged": PRICE_PER_CALL,
        "balance": charge_result.get("balance"),
        "timestamp": int(datetime.now().timestamp())
    }


def signal_paid(coin_id: str, user_id: str) -> dict:
    """
    交易信号（付费版）
    """
    # 1. 检查余额
    balance_check = check_balance(user_id)
    
    if not balance_check.get("ok"):
        return {
            "error": "余额不足",
            "balance": balance_check.get("balance", 0),
            "payment_url": balance_check.get("payment_url"),
            "message": "请充值后继续使用（最低充值$8）"
        }
    
    # 2. 获取数据
    prices = get_price_history(coin_id, 90)
    
    if not prices:
        return {
            "error": "获取历史数据失败",
            "message": "请检查币种名称或稍后重试"
        }
    
    crypto_data = get_crypto_price(coin_id)
    
    if "error" in crypto_data:
        return {
            "error": "获取实时价格失败"
        }
    
    # 3. 技术分析
    indicators = {
        "ma_20": calculate_ma(prices, 20),
        "ma_50": calculate_ma(prices, 50),
        "rsi": calculate_rsi(prices),
        "macd": calculate_macd(prices)
    }
    
    # 4. 生成信号
    signal = generate_signal(crypto_data["price"], indicators)
    
    # 5. 扣费
    charge_result = charge_user(user_id)
    
    if not charge_result.get("ok"):
        return {
            "error": "扣费失败",
            "balance": charge_result.get("balance", 0),
            "payment_url": charge_result.get("payment_url"),
            "message": "余额不足，请充值"
        }
    
    # 6. 返回结果
    result = signal.copy()
    result["symbol"] = coin_id
    result["name"] = crypto_data.get("name")
    result["price"] = crypto_data.get("price")
    result["charged"] = PRICE_PER_CALL
    result["balance"] = charge_result.get("balance")
    result["timestamp"] = int(datetime.now().timestamp())
    
    return result


# ═══════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='CryptoScope - 加密货币数据分析助手 v1.0.0（付费版）')
    
    parser.add_argument('command', choices=['price', 'analyze', 'signal'], help='命令')
    parser.add_argument('coin', type=str, nargs='?', help='币种ID（如bitcoin, ethereum）')
    parser.add_argument('--user-id', type=str, required=True, help='用户ID（必填）')
    
    args = parser.parse_args()
    
    if not args.coin:
        print("❌ 错误: 请指定币种ID")
        print("示例: python3 crypto_analyzer_paid.py price bitcoin --user-id user123")
        sys.exit(1)
    
    # 执行命令
    if args.command == 'price':
        result = get_price_paid(args.coin, args.user_id)
    elif args.command == 'analyze':
        result = analyze_paid(args.coin, args.user_id)
    elif args.command == 'signal':
        result = signal_paid(args.coin, args.user_id)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
