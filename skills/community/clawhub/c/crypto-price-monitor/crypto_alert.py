#!/usr/bin/env python3
"""Crypto Price Alert Script — works with crypto-price-alerts skill"""
import requests
import json
import sys
import os
from datetime import datetime

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_price(coin_id):
    url = f"{COINGECKO_API}/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[coin_id]["usd"], data[coin_id].get("usd_24h_change", 0)

def check_alerts(alerts_config):
    triggered = []
    for alert in alerts_config.get("alerts", []):
        coin = alert["coin"]
        condition = alert["condition"]
        target = alert["price"]
        message = alert["message"]
        
        try:
            price, change_24h = get_price(coin)
        except Exception as e:
            print(f"Error fetching {coin}: {e}")
            continue
        
        should_fire = False
        if condition == "above" and price >= target:
            should_fire = True
        elif condition == "below" and price <= target:
            should_fire = True
        
        if should_fire:
            triggered.append({
                "coin": coin,
                "price": price,
                "target": target,
                "condition": condition,
                "message": message,
                "change_24h": change_24h,
                "time": datetime.now().isoformat()
            })
            print(f"🚨 ALERT: {message} (Current: ${price:,.2f})")
        else:
            print(f"  {coin.upper()}: ${price:,.2f} (24h: {change_24h:+.2f}%) | {condition} ${target:,.2f}")
    
    return triggered

def send_telegram(message, bot_token, chat_id):
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload, timeout=10)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "crypto-alerts.json")
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        print("No crypto-alerts.json found. Checking default coins.")
        config = {
            "alerts": [
                {"coin": "bitcoin", "symbol": "btc", "condition": "above", "price": 0},
                {"coin": "ethereum", "symbol": "eth", "condition": "above", "price": 0},
                {"coin": "solana", "symbol": "sol", "condition": "above", "price": 0}
            ]
        }
    
    triggered = check_alerts(config)
    
    if triggered:
        summary = "🚨 <b>Crypto Alert Triggered</b>\n\n"
        for t in triggered:
            summary += f"{t['message']}\n"
            summary += f"Price: ${t['price']:,.2f} | 24h: {t['change_24h']:+.2f}%\n\n"
        
        bot_token = config.get("telegram_bot_token")
        chat_id = config.get("telegram_chat_id")
        if bot_token and chat_id:
            send_telegram(summary, bot_token, chat_id)
