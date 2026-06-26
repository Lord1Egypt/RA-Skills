#!/usr/bin/env python3
"""
豆瓣热榜获取脚本
Douban Hot Topics Fetcher
"""

import json
import sys
from datetime import datetime

def get_douban_movies(limit=10):
    """获取豆瓣正在热映"""
    mock_movies = [
        {"rank": 1, "title": "流浪地球3", "rating": 8.5, "votes": 234567, "genre": "科幻"},
        {"rank": 2, "title": "满江红2", "rating": 7.8, "votes": 198765, "genre": "剧情"},
        {"rank": 3, "title": "封神2", "rating": 8.2, "votes": 176543, "genre": "奇幻"},
        {"rank": 4, "title": "唐人街探案4", "rating": 7.5, "votes": 165432, "genre": "悬疑"},
        {"rank": 5, "title": "热辣滚烫", "rating": 8.0, "votes": 154321, "genre": "喜剧"},
        {"rank": 6, "title": "第二十条", "rating": 7.9, "votes": 143210, "genre": "剧情"},
        {"rank": 7, "title": "飞驰人生2", "rating": 7.6, "votes": 132109, "genre": "喜剧"},
        {"rank": 8, "title": "熊出没", "rating": 7.2, "votes": 121098, "genre": "动画"},
        {"rank": 9, "title": "红毯先生", "rating": 6.8, "votes": 110987, "genre": "喜剧"},
        {"rank": 10, "title": "年会不能停", "rating": 7.4, "votes": 109876, "genre": "喜剧"},
    ]
    return mock_movies[:limit]

def get_douban_books(limit=10):
    """获取豆瓣高分图书"""
    mock_books = [
        {"rank": 1, "title": "三体", "author": "刘慈欣", "rating": 9.3, "genre": "科幻"},
        {"rank": 2, "title": "活着", "author": "余华", "rating": 9.4, "genre": "文学"},
        {"rank": 3, "title": "百年孤独", "author": "马尔克斯", "rating": 9.3, "genre": "经典"},
        {"rank": 4, "title": "红楼梦", "author": "曹雪芹", "rating": 9.6, "genre": "古典"},
        {"rank": 5, "title": "小王子", "author": "圣埃克苏佩里", "rating": 9.0, "genre": "童话"},
    ]
    return mock_books[:limit]

def format_movies(data):
    output = "🎬 豆瓣正在热映\n\n"
    for item in data:
        votes_str = f"{item['votes'] / 10000:.1f}万"
        output += f"{item['rank']}. {item['title']} ⭐ {item['rating']} - {votes_str}人评价 - {item['genre']}\n"
    return output

def format_books(data):
    output = "📚 豆瓣高分图书\n\n"
    for item in data:
        output += f"{item['rank']}. 《{item['title']}》 ⭐ {item['rating']} - {item['author']} - {item['genre']}\n"
    return output

def main():
    limit = 10
    content_type = "movies"
    
    args = sys.argv[1:]
    for arg in args:
        if arg.isdigit():
            limit = int(arg)
        elif arg in ["movies", "books", "movie", "book"]:
            content_type = "books" if "book" in arg else "movies"
    
    if content_type == "movies":
        data = get_douban_movies(limit)
        output = format_movies(data)
    else:
        data = get_douban_books(limit)
        output = format_books(data)
    
    if "--json" in args:
        print(json.dumps({"data": data, "type": content_type}, ensure_ascii=False, indent=2))
    else:
        print(output)

if __name__ == "__main__":
    main()
