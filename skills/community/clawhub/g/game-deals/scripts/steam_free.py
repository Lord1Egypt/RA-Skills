#!/usr/bin/env python3
"""
获取 Steam 限免/免费游戏信息
"""

import requests
import json

def get_steam_free_games():
    """获取 Steam 免费游戏 - 使用搜索 API"""
    games = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://store.steampowered.com/"
    }
    
    try:
        # Steam 搜索 API - 搜索免费游戏
        url = "https://store.steampowered.com/api/search"
        params = {
            "term": "",
            "max_results": 20,
            "filters": "price:free"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            for item in items:
                games.append({
                    "appid": item.get("id"),
                    "name": item.get("name"),
                    "url": f"https://store.steampowered.com/app/{item.get('id')}/",
                    "type": "免费游戏"
                })
        
        # 如果没有结果，提供常用免费游戏列表
        if not games:
            games = [
                {"appid": "730", "name": "Counter-Strike 2", "url": "https://store.steampowered.com/app/730/", "type": "免费开玩"},
                {"appid": "570", "name": "Dota 2", "url": "https://store.steampowered.com/app/570/", "type": "免费开玩"},
                {"appid": "440", "name": "Team Fortress 2", "url": "https://store.steampowered.com/app/440/", "type": "免费开玩"},
                {"appid": "1172470", "name": "Apex Legends", "url": "https://store.steampowered.com/app/1172470/", "type": "免费开玩"},
                {"appid": "1085660", "name": "Destiny 2", "url": "https://store.steampowered.com/app/1085660/", "type": "免费开玩"},
            ]
                
    except Exception as e:
        # 出错时返回常用免费游戏
        games = [
            {"appid": "730", "name": "Counter-Strike 2", "url": "https://store.steampowered.com/app/730/", "type": "免费开玩"},
            {"appid": "570", "name": "Dota 2", "url": "https://store.steampowered.com/app/570/", "type": "免费开玩"},
            {"appid": "440", "name": "Team Fortress 2", "url": "https://store.steampowered.com/app/440/", "type": "免费开玩"},
        ]
    
    return games[:10]

def format_output(games):
    """格式化输出"""
    if isinstance(games, dict) and "error" in games:
        return f"❌ 获取失败: {games['error']}"
    
    if not games:
        return "🎮 Steam 暂无特别限免游戏"
    
    output = ["🎮 Steam 免费游戏推荐", "=" * 40]
    
    for game in games:
        output.append(f"\n🎯 {game['name']}")
        output.append(f"📌 {game['type']}")
        output.append(f"🔗 {game['url']}")
        output.append("-" * 40)
    
    output.append("\n更多免费游戏：https://store.steampowered.com/genre/Free%20to%20Play/")
    
    return "\n".join(output)

if __name__ == "__main__":
    games = get_steam_free_games()
    print(format_output(games))
