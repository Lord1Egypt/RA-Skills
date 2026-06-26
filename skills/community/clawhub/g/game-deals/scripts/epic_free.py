#!/usr/bin/env python3
"""
获取 Epic Games Store 当前限免游戏
"""

import requests
import json
from datetime import datetime

def get_epic_free_games():
    """获取 Epic 限免游戏"""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": "zh-CN",
        "country": "CN",
        "allowCountries": "CN"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        games = []
        
        # 处理错误情况，API 可能返回 errors 但仍有数据
        catalog = data.get("data", {}).get("Catalog", {}) or {}
        search_store = catalog.get("searchStore", {}) or {}
        elements = search_store.get("elements", []) or []
        
        for game in elements:
            # 检查是否有促销活动
            promotions = game.get("promotions", {}) or {}
            promo_offers = promotions.get("promotionalOffers", [])
            
            # 只处理有促销的游戏（discountPercentage 为 0 表示免费）
            if promo_offers and len(promo_offers) > 0:
                offer_list = promo_offers[0].get("promotionalOffers", [])
                if offer_list:
                    offer = offer_list[0]
                    discount_pct = offer.get("discountSetting", {}).get("discountPercentage", 100)
                    
                    # 100% 折扣 = 免费
                    if discount_pct == 0:
                        start_date = offer.get("startDate", "")
                        end_date = offer.get("endDate", "")
                        
                        # 获取封面图
                        images = game.get("keyImages", [])
                        image_url = ""
                        for img in images:
                            if img.get("type") == "OfferImageWide":
                                image_url = img.get("url", "")
                                break
                        
                        # 获取价格信息
                        price_info = game.get("price", {}).get("totalPrice", {})
                        original_price = price_info.get("originalPrice", 0)
                        currency = price_info.get("currencyCode", "CNY")
                        
                        game_info = {
                            "title": game.get("title", "未知"),
                            "description": game.get("description", ""),
                            "image": image_url,
                            "startDate": start_date,
                            "endDate": end_date,
                            "originalPrice": original_price / 100 if original_price else 0,  # 转换为元
                            "currency": currency,
                            "url": f"https://store.epicgames.com/zh-CN/p/{game.get('productSlug', game.get('urlSlug', game.get('id', '')))}"
                        }
                        games.append(game_info)
        
        return games
    
    except Exception as e:
        return {"error": str(e)}

def format_output(games):
    """格式化输出"""
    if isinstance(games, dict) and "error" in games:
        return f"❌ 获取失败: {games['error']}"
    
    if not games:
        return "🎮 Epic 当前没有限免游戏"
    
    output = ["🎮 Epic Games 限免游戏", "=" * 40]
    
    for game in games:
        output.append(f"\n🎯 {game['title']}")
        if game['originalPrice'] > 0:
            output.append(f"💰 原价: ¥{game['originalPrice']:.0f}")
        output.append(f"📅 截止: {game['endDate'][:10] if game['endDate'] else '未知'}")
        output.append(f"🔗 {game['url']}")
        if game['description']:
            desc = game['description'][:100] + "..." if len(game['description']) > 100 else game['description']
            output.append(f"📝 {desc}")
        output.append("-" * 40)
    
    return "\n".join(output)

if __name__ == "__main__":
    games = get_epic_free_games()
    print(format_output(games))
