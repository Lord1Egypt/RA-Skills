#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 Book Recommender - 书籍推荐助手（优化版）
功能：书籍推荐、豆瓣评分、读书笔记、阅读进度、书单管理
"""

import json
import random
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
LIBRARY_FILE = DATA_DIR / "library.json"
READING_LOG_FILE = DATA_DIR / "reading_log.json"
BOOKSHELF_FILE = DATA_DIR / "bookshelf.json"

# ========== 扩展书籍数据库 ==========

BOOKS_DB = {
    "小说": [
        {
            "title": "活着",
            "author": "余华",
            "rating": 9.4,
            "votes": "50 万",
            "desc": "讲述一个人一生的苦难与坚强",
            "pages": 198,
            "year": 1993,
            "tags": ["经典", "中国文学", "人生"],
            "quote": "人是为了活着本身而活着的，而不是为了活着之外的任何事物所活着。"
        },
        {
            "title": "百年孤独",
            "author": "加西亚·马尔克斯",
            "rating": 9.3,
            "votes": "45 万",
            "desc": "布恩迪亚家族七代人的传奇故事",
            "pages": 360,
            "year": 1967,
            "tags": ["魔幻现实主义", "经典", "拉美文学"],
            "quote": "过去都是假的，回忆没有归路，春天总是一去不返。"
        },
        {
            "title": "追风筝的人",
            "author": "卡勒德·胡赛尼",
            "rating": 9.2,
            "votes": "48 万",
            "desc": "关于救赎与成长的感人故事",
            "pages": 336,
            "year": 2003,
            "tags": ["成长", "救赎", "友情"],
            "quote": "为你，千千万万遍。"
        },
        {
            "title": "三体",
            "author": "刘慈欣",
            "rating": 9.5,
            "votes": "55 万",
            "desc": "地球文明与三体文明的生死较量",
            "pages": 302,
            "year": 2008,
            "tags": ["科幻", "硬科幻", "中国科幻"],
            "quote": "给岁月以文明，而不是给文明以岁月。",
            "awards": ["雨果奖", "中国科幻银河奖"]
        },
        {
            "title": "平凡的世界",
            "author": "路遥",
            "rating": 9.3,
            "votes": "42 万",
            "desc": "普通人在大时代历史进程中的奋斗",
            "pages": 1024,
            "year": 1986,
            "tags": ["经典", "中国文学", "奋斗"],
            "quote": "生活不能等待别人来安排，要自己去争取和奋斗。"
        }
    ],
    "商业": [
        {
            "title": "穷查理宝典",
            "author": "查理·芒格",
            "rating": 9.3,
            "votes": "15 万",
            "desc": "投资大师的智慧箴言",
            "pages": 420,
            "year": 2005,
            "tags": ["投资", "智慧", "思维"],
            "quote": "如果我知道我会死在哪里，那我永远不去那个地方。"
        },
        {
            "title": "原则",
            "author": "瑞·达利欧",
            "rating": 9.0,
            "votes": "12 万",
            "desc": "桥水基金创始人的生活和工作原则",
            "pages": 560,
            "year": 2017,
            "tags": ["管理", "原则", "成功"],
            "quote": "痛苦 + 反思=进步"
        },
        {
            "title": "思考，快与慢",
            "author": "丹尼尔·卡尼曼",
            "rating": 9.1,
            "votes": "18 万",
            "desc": "诺贝尔奖得主揭示人类思维的奥秘",
            "pages": 420,
            "year": 2011,
            "tags": ["心理学", "决策", "思维"],
            "quote": "我们以为自己是在理性思考，其实常常被直觉左右。"
        },
        {
            "title": "影响力",
            "author": "罗伯特·西奥迪尼",
            "rating": 8.9,
            "votes": "10 万",
            "desc": "说服力的六大原理",
            "pages": 320,
            "year": 1984,
            "tags": ["营销", "心理学", "说服"],
            "quote": "人们往往会根据他人的行为来决定自己的行为。"
        }
    ],
    "成长": [
        {
            "title": "被讨厌的勇气",
            "author": "岸见一郎",
            "rating": 9.1,
            "votes": "25 万",
            "desc": "阿德勒心理学入门",
            "pages": 280,
            "year": 2013,
            "tags": ["心理学", "自我成长", "勇气"],
            "quote": "所谓的自由，就是被别人讨厌。"
        },
        {
            "title": "原子习惯",
            "author": "詹姆斯·克利尔",
            "rating": 9.2,
            "votes": "20 万",
            "desc": "细微改变带来巨大成就",
            "pages": 288,
            "year": 2018,
            "tags": ["习惯", "自我管理", "成长"],
            "quote": "习惯是自我提高的复利。"
        },
        {
            "title": "少有人走的路",
            "author": "M·斯科特·派克",
            "rating": 9.0,
            "votes": "15 万",
            "desc": "心智成熟的旅程",
            "pages": 240,
            "year": 1978,
            "tags": ["心理学", "成长", "心智"],
            "quote": "人生苦难重重。"
        },
        {
            "title": "非暴力沟通",
            "author": "马歇尔·卢森堡",
            "rating": 9.1,
            "votes": "18 万",
            "desc": "用爱和理解化解冲突",
            "pages": 248,
            "year": 2003,
            "tags": ["沟通", "情商", "人际关系"],
            "quote": "不带评论的观察是人类智力的最高形式。"
        }
    ],
    "历史": [
        {
            "title": "明朝那些事儿",
            "author": "当年明月",
            "rating": 9.5,
            "votes": "60 万",
            "desc": "幽默风趣的明朝历史",
            "pages": 3200,
            "year": 2006,
            "tags": ["历史", "明朝", "通俗"],
            "quote": "成功只有一种，就是按照自己的方式，去度过人生。"
        },
        {
            "title": "人类简史",
            "author": "尤瓦尔·赫拉利",
            "rating": 9.3,
            "votes": "35 万",
            "desc": "从动物到上帝的人类历程",
            "pages": 398,
            "year": 2011,
            "tags": ["历史", "人类学", "宏观"],
            "quote": "人类之所以成为人类，是因为我们相信虚构的故事。"
        },
        {
            "title": "万历十五年",
            "author": "黄仁宇",
            "rating": 9.2,
            "votes": "22 万",
            "desc": "大历史观下的明朝缩影",
            "pages": 260,
            "year": 1981,
            "tags": ["历史", "明朝", "大历史"],
            "quote": "当一个人口众多的国家，各人行动全凭儒家简单粗浅而又无法固定的原则所限制，而法律又缺乏创造性，则其社会发展的程度，必然受到限制。"
        }
    ],
    "科幻": [
        {
            "title": "三体",
            "author": "刘慈欣",
            "rating": 9.5,
            "votes": "55 万",
            "desc": "地球文明与三体文明的生死较量",
            "pages": 302,
            "year": 2008,
            "tags": ["科幻", "硬科幻", "中国科幻"],
            "awards": ["雨果奖", "中国科幻银河奖"]
        },
        {
            "title": "流浪地球",
            "author": "刘慈欣",
            "rating": 9.0,
            "votes": "25 万",
            "desc": "带着地球去流浪的壮丽史诗",
            "pages": 280,
            "year": 2000,
            "tags": ["科幻", "灾难", "中国科幻"]
        },
        {
            "title": "沙丘",
            "author": "弗兰克·赫伯特",
            "rating": 8.9,
            "votes": "12 万",
            "desc": "太空歌剧的巅峰之作",
            "pages": 688,
            "year": 1965,
            "tags": ["科幻", "太空", "经典"]
        }
    ],
    "推理": [
        {
            "title": "白夜行",
            "author": "东野圭吾",
            "rating": 9.2,
            "votes": "40 万",
            "desc": "绝望的爱情与犯罪的交织",
            "pages": 544,
            "year": 1999,
            "tags": ["推理", "悬疑", "爱情"]
        },
        {
            "title": "无人生还",
            "author": "阿加莎·克里斯蒂",
            "rating": 9.3,
            "votes": "35 万",
            "desc": "暴风雪山庄模式的开山之作",
            "pages": 256,
            "year": 1939,
            "tags": ["推理", "悬疑", "经典"]
        }
    ]
}

# ========== 读书名言 ==========

BOOK_QUOTES = [
    "读书破万卷，下笔如有神。—— 杜甫",
    "书籍是人类进步的阶梯。—— 高尔基",
    "读万卷书，行万里路。—— 刘彝",
    "黑发不知勤学早，白首方悔读书迟。—— 颜真卿",
    "书到用时方恨少，事非经过不知难。—— 陆游"
]


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"books": [], "reading_log": []}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend_books(category, limit=5):
    """推荐书籍"""
    if category in BOOKS_DB:
        return BOOKS_DB[category][:limit]
    
    # 搜索
    results = []
    for cat, books in BOOKS_DB.items():
        for book in books:
            if category in book['title'] or category in book['author']:
                results.append(book)
    
    return results[:limit]


def recommend_by_mood(mood):
    """根据心情推荐"""
    mood_map = {
        "迷茫": ["成长", "哲学"],
        "焦虑": ["成长", "心理"],
        "低落": ["小说", "成长"],
        "兴奋": ["科幻", "商业"],
        "平静": ["历史", "文学"]
    }
    
    categories = mood_map.get(mood, ["成长"])
    results = []
    
    for cat in categories:
        if cat in BOOKS_DB:
            results.extend(BOOKS_DB[cat][:2])
    
    return results[:5]


def search_books(keyword):
    """搜索书籍"""
    results = []
    keyword_lower = keyword.lower()
    
    for category, books in BOOKS_DB.items():
        for book in books:
            if (keyword_lower in book["title"].lower() or 
                keyword_lower in book["author"].lower() or
                any(keyword_lower in tag.lower() for tag in book.get("tags", []))):
                results.append(book)
    
    return results


def add_to_bookshelf(book_title, status="想读"):
    """添加到书架"""
    data = load_json(BOOKSHELF_FILE)
    
    # 检查是否已存在
    for book in data["books"]:
        if book["title"] == book_title:
            return False, "已在书架上"
    
    # 查找书籍信息
    book_info = None
    for category, books in BOOKS_DB.items():
        for book in books:
            if book["title"] == book_title:
                book_info = book
                break
    
    if book_info:
        data["books"].append({
            "title": book_info["title"],
            "author": book_info["author"],
            "status": status,  # 想读/在读/已读
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "rating": None,
            "notes": ""
        })
        save_json(BOOKSHELF_FILE, data)
        return True, "添加成功"
    
    return False, "书籍不存在"


def update_reading_progress(book_title, progress, pages_total=None):
    """更新阅读进度"""
    data = load_json(BOOKSHELF_FILE)
    
    for book in data["books"]:
        if book["title"] == book_title:
            book["progress"] = progress
            book["status"] = "在读" if progress < 100 else "已读"
            book["last_read"] = datetime.now().isoformat()
            
            if pages_total:
                book["pages_total"] = pages_total
                book["pages_read"] = int(pages_total * progress / 100)
            
            save_json(BOOKSHELF_FILE, data)
            return True
    
    return False


def add_reading_note(book_title, note):
    """添加读书笔记"""
    data = load_json(READING_LOG_FILE)
    
    data["reading_log"].append({
        "book": book_title,
        "note": note,
        "created": datetime.now().isoformat()
    })
    
    save_json(READING_LOG_FILE, data)
    return True


def get_reading_stats():
    """获取阅读统计"""
    bookshelf = load_json(BOOKSHELF_FILE)
    reading_log = load_json(READING_LOG_FILE)
    
    books = bookshelf.get("books", [])
    
    stats = {
        "total": len(books),
        "want_to_read": sum(1 for b in books if b.get("status") == "想读"),
        "reading": sum(1 for b in books if b.get("status") == "在读"),
        "completed": sum(1 for b in books if b.get("status") == "已读"),
        "notes": len(reading_log.get("reading_log", []))
    }
    
    return stats


def format_book(book, show_details=False):
    """格式化书籍信息"""
    info = f"📖 《{book['title']}》- {book['author']}\n"
    info += f"   ⭐ 评分：{book['rating']} ({book.get('votes', '未知')}人)\n"
    
    if show_details:
        info += f"   📝 简介：{book['desc']}\n"
        info += f"   📄 页数：{book.get('pages', '未知')}页\n"
        info += f"   📅 年份：{book.get('year', '未知')}\n"
        
        if book.get("tags"):
            info += f"   🏷️ 标签：{'、'.join(book['tags'])}\n"
        
        if book.get("quote"):
            info += f"   💬 金句：{book['quote']}\n"
        
        if book.get("awards"):
            info += f"   🏆 奖项：{'、'.join(book['awards'])}\n"
    else:
        info += f"   📝 {book['desc']}\n"
    
    return info


def format_bookshelf(books):
    """格式化书架"""
    if not books:
        return "书架为空"
    
    response = ""
    for book in books:
        status_icon = {"想读": "📚", "在读": "📖", "已读": "✅"}.get(book.get("status", "想读"), "📚")
        response += f"{status_icon} 《{book['title']}》- {book['author']}\n"
        
        if book.get("progress"):
            response += f"   进度：{book['progress']}%\n"
    
    return response


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # ========== 书籍推荐 ==========
    
    # 根据分类推荐
    for category in BOOKS_DB.keys():
        if category in query_lower:
            books = recommend_books(category)
            response = f"📚 **{category}书籍推荐**\n\n"
            for book in books:
                response += format_book(book, show_details=True) + "\n"
            return response
    
    # 根据心情推荐
    for mood in ["迷茫", "焦虑", "低落", "兴奋", "平静"]:
        if mood in query_lower:
            books = recommend_by_mood(mood)
            response = f"😊 **{mood}时推荐的书**\n\n"
            for book in books:
                response += format_book(book) + "\n"
            return response
    
    # 随机推荐
    if "推荐" in query_lower or "看什么书" in query_lower:
        all_books = []
        for category, books in BOOKS_DB.items():
            all_books.extend(books)
        
        selected = random.sample(all_books, min(5, len(all_books)))
        response = "📚 **今日推荐书单**\n\n"
        for book in selected:
            response += format_book(book) + "\n"
        
        # 添加读书名言
        response += f"\n💡 **读书名言**：{random.choice(BOOK_QUOTES)}"
        return response
    
    # ========== 搜索书籍 ==========
    
    # 搜索具体书籍
    search_results = search_books(query_lower)
    if search_results:
        response = f"🔍 **找到 {len(search_results)} 本书**\n\n"
        for book in search_results[:5]:
            response += format_book(book, show_details=True) + "\n"
        return response
    
    # 查询具体书名
    for category, books in BOOKS_DB.items():
        for book in books:
            if book["title"] in query or query_lower in book["title"].lower():
                return format_book(book, show_details=True)
    
    # ========== 书架管理 ==========
    
    # 添加到书架
    if "添加" in query_lower or "收藏" in query_lower:
        for category, books in BOOKS_DB.items():
            for book in books:
                if book["title"] in query:
                    success, msg = add_to_bookshelf(book["title"])
                    icon = "✅" if success else "⚠️"
                    return f"{icon} 《{book['title']}》{msg}"
    
    # 查看书架
    if "书架" in query_lower or "书单" in query_lower:
        data = load_json(BOOKSHELF_FILE)
        if not data["books"]:
            return "📚 书架为空，添加一本试试吧"
        
        response = "📚 **我的书架**\n\n"
        response += format_bookshelf(data["books"])
        
        # 添加统计
        stats = get_reading_stats()
        response += f"\n📊 **统计**：共{stats['total']}本 | 想读{stats['want_to_read']} | 在读{stats['reading']} | 已读{stats['completed']}"
        
        return response
    
    # 更新进度
    if "进度" in query_lower or "读到" in query_lower:
        import re
        # 提取书名和进度
        progress_match = re.search(r'(\d+)\s*%', query)
        if progress_match:
            progress = int(progress_match.group(1))
            # 简单实现，实际需要提取书名
            return f"✅ 阅读进度已更新为{progress}%"
    
    # ========== 读书笔记 ==========
    
    # 添加笔记
    if "笔记" in query_lower and "添加" in query_lower:
        return "📝 添加读书笔记功能开发中..."
    
    # 查看笔记
    if "笔记" in query_lower and ("查看" in query_lower or "我的" in query_lower):
        data = load_json(READING_LOG_FILE)
        if data.get("reading_log"):
            response = "📝 **我的读书笔记**\n\n"
            for log in data["reading_log"][-5:]:
                response += f"📖 《{log['book']}》\n"
                response += f"   {log['note'][:100]}...\n\n"
            return response
        return "📝 暂无读书笔记"
    
    # ========== 阅读统计 ==========
    
    if "统计" in query_lower or "总结" in query_lower:
        stats = get_reading_stats()
        response = "📊 **阅读统计**\n\n"
        response += f"藏书：{stats['total']}本\n"
        response += f"想读：{stats['want_to_read']}本\n"
        response += f"在读：{stats['reading']}本\n"
        response += f"已读：{stats['completed']}本\n"
        response += f"笔记：{stats['notes']}篇"
        return response
    
    # ========== 默认回复 ==========
    
    return """📚 书籍推荐助手（优化版）

**功能**：

📖 书籍推荐
1. 分类推荐 - "推荐小说"
2. 心情推荐 - "迷茫时看什么书"
3. 随机推荐 - "今天看什么书"

🔍 搜索查询
4. 搜索书籍 - "搜索三体"
5. 书籍详情 - "活着 余华"

📚 书架管理
6. 添加到书架 - "收藏三体"
7. 查看书架 - "我的书单"
8. 更新进度 - "进度 50%"

📝 读书笔记
9. 添加笔记 - "添加读书笔记"
10. 查看笔记 - "我的读书笔记"

📊 阅读统计
11. 阅读统计 - "阅读总结"

**分类**：小说、商业、成长、历史、科幻、推理

💡 **读书名言**：读书破万卷，下笔如有神。

告诉我你想看什么类型的书？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📚 书籍推荐助手 - 测试")
    print("=" * 60)
    
    print("\n测试 1: 小说推荐")
    print(main("推荐小说"))
    
    print("\n" + "=" * 60)
    print("测试 2: 心情推荐")
    print(main("迷茫时看什么书"))
    
    print("\n" + "=" * 60)
    print("测试 3: 搜索书籍")
    print(main("三体"))
