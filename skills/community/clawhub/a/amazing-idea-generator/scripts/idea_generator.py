#!/usr/bin/env python3
"""
Amazing Idea Generator v0.3.2
Author: 张权 (Zhang Quan)
Brand: Luckydesigner（行运设计师）
Pen Name: 伯衡君

Features:
- Memory system: Track seen ideas
- Personality: Playful tone
- Persistence: Auto-detect workspace path (portable across users)
- Detail view: Reply number to see full plan
- Category filter: Support specific category
- User submission: Submit new ideas
- Favorites: Save favorite ideas
- User guide: Help command
- Quality check: Rate ideas
- Command logging: Track command execution
- Multi-language: Auto-detect user language and respond accordingly
- Extended categories: 10 categories, 200 ideas (reference folder)
- Reference folder: JSON files for each category
- DuckDuckGo: Web search for trending ideas with auto-fallback
- Dynamic deep analysis: On-demand web search for tech stack, market analysis, resources
- Hybrid mode: Static basics + dynamic deep content
"""

import json
import random
import os
import re
from datetime import datetime

# Voting system (5位名人Agent投票)
try:
    from idea_voting import IdeaVotingSystem, format_vote_result
    VOTING_AVAILABLE = True
except ImportError:
    VOTING_AVAILABLE = False

# DuckDuckGo search support (optional)
try:
    from duckduckgo_search import DDGS
    DUCKDUCKGO_AVAILABLE = True
except ImportError:
    DUCKDUCKGO_AVAILABLE = False

# Reference folder path
REFERENCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reference")

# Trending keywords that trigger web search
TRENDING_KEYWORDS = [
    '趋势', 'trending', '最新', 'latest', '2024', '2025', '2026',
    '热门', 'hot', 'new', '新', '流行', 'popular', '前沿', 'cutting-edge',
    '创新', 'innovative', '未来', 'future', '当下', 'current'
]

def search_trending_ideas(query, max_results=5):
    """Search for trending ideas using DuckDuckGo"""
    if not DUCKDUCKGO_AVAILABLE:
        return None
    
    try:
        with DDGS() as ddgs:
            # Search for trending ideas/projects
            search_query = f"{query} app idea project 2024 2025"
            results = list(ddgs.text(search_query, max_results=max_results, timelimit='m'))
            
            ideas = []
            for r in results:
                ideas.append({
                    'id': f"web_{len(ideas)+1}",
                    'name': r.get('title', 'Unknown')[:50],
                    'name_en': r.get('title', 'Unknown')[:50],
                    'desc': r.get('body', '')[:100],
                    'desc_en': r.get('body', '')[:100],
                    'detail': f"来源: {r.get('href', 'N/A')}\n{r.get('body', '')}",
                    'detail_en': f"Source: {r.get('href', 'N/A')}\n{r.get('body', '')}",
                    'category': '网络趋势',
                    'difficulty': '中等',
                    'source': 'web'
                })
            return ideas
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
        return None

def should_search_web(user_input):
    """Check if user input contains trending keywords"""
    user_lower = user_input.lower()
    return any(kw in user_lower for kw in TRENDING_KEYWORDS)

# Deep analysis keywords
DEEP_ANALYSIS_KEYWORDS = [
    '深度分析', 'deep analysis', '详细方案', 'detailed plan',
    '技术栈', 'tech stack', '架构', 'architecture',
    '市场分析', 'market analysis', '竞品', 'competitor',
    '变现', 'monetization', '商业模式', 'business model',
    '开发成本', 'dev cost', '实现方案', 'implementation'
]

def should_deep_analyze(user_input):
    """Check if user wants deep analysis"""
    user_lower = user_input.lower()
    return any(kw in user_lower for kw in DEEP_ANALYSIS_KEYWORDS)

def deep_analyze_idea(idea, lang='zh'):
    """Generate deep analysis for an idea using web search (with cache)"""
    idea_id = idea.get('id', idea.get('name', 'unknown'))
    
    # Check cache first
    cached = get_cached_deep(idea_id)
    if cached:
        return cached + "\n\n💡 提示：此内容来自缓存（7天内有效）"
    
    if not DUCKDUCKGO_AVAILABLE:
        return generate_fallback_deep(idea, lang)
    
    name = idea.get('name', idea.get('name_en', 'Unknown'))
    name_en = idea.get('name_en', name)
    
    # Search queries for different aspects
    queries = [
        f"{name_en} implementation tutorial",
        f"{name_en} open source github",
        f"{name_en} market analysis competitors",
        f"{name_en} business model monetization"
    ]
    
    results = {}
    try:
        with DDGS() as ddgs:
            for i, query in enumerate(queries[:2]):  # Limit to 2 searches to avoid rate limit
                try:
                    r = list(ddgs.text(query, max_results=3))
                    results[f'query_{i}'] = r
                except:
                    pass
    except Exception as e:
        return generate_fallback_deep(idea, lang)
    
    # Generate deep analysis from search results
    return format_deep_analysis(idea, results, lang)

def generate_fallback_deep(idea, lang='zh'):
    """Generate fallback deep analysis when web search fails"""
    name = idea.get('name', idea.get('name_en', 'Unknown'))
    detail = idea.get('detail', idea.get('detail_en', ''))
    
    if lang == 'zh':
        return f"""─── 📊 深度分析（离线模式）───

⚠️ 网络搜索暂时不可用，以下为基础分析：

📋 基础方案：
{detail}

💡 提示：请稍后重试，或手动搜索 "{name}" 获取更多信息。
"""
    else:
        return f"""─── 📊 Deep Analysis (Offline Mode) ───

⚠️ Web search unavailable. Basic analysis:

📋 Basic Plan:
{detail}

💡 Tip: Try again later or search "{name}" manually.
"""

def format_deep_analysis(idea, search_results, lang='zh'):
    """Format deep analysis from search results and cache it"""
    idea_id = idea.get('id', idea.get('name', 'unknown'))
    name = idea.get('name', idea.get('name_en', 'Unknown'))
    detail = idea.get('detail', idea.get('detail_en', ''))
    
    # Extract useful info from search results
    tech_info = []
    resources = []
    
    for key, results in search_results.items():
        for r in results[:3]:
            title = r.get('title', '')
            href = r.get('href', '')
            body = r.get('body', '')[:100]
            
            if 'github' in href.lower() or 'tutorial' in title.lower():
                resources.append(f"• {title}: {href}")
            elif body:
                tech_info.append(body)
    
    if lang == 'zh':
        result = f"""─── 📊 深度分析（实时生成）───

🔧 技术方向：
{chr(10).join(tech_info[:3]) if tech_info else '请搜索相关技术文档'}

📚 学习资源：
{chr(10).join(resources[:3]) if resources else '暂无推荐资源'}

💡 提示：以上内容基于实时网络搜索生成
"""
    else:
        result = f"""─── 📊 Deep Analysis (Live) ───

🔧 Tech Direction:
{chr(10).join(tech_info[:3]) if tech_info else 'Search for technical docs'}

📚 Learning Resources:
{chr(10).join(resources[:3]) if resources else 'No resources found'}

💡 Note: Generated from live web search
"""
    
    # Cache the result
    set_cached_deep(idea_id, result)
    return result

def load_ideas_from_reference():
    """Load ideas from reference folder JSON files"""
    ideas = {}
    if not os.path.exists(REFERENCE_DIR):
        return ideas
    
    for filename in os.listdir(REFERENCE_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(REFERENCE_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    category = data.get('category', filename.replace('.json', ''))
                    ideas[category] = data.get('ideas', [])
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return ideas

# Load reference ideas at startup
REFERENCE_IDEAS = load_ideas_from_reference()

# Cross-domain ideas (跨领域点子) - 每次生成都会包含1个
CROSS_DOMAIN_IDEAS = [
    {
        "id": "cross_001",
        "name": "持仓交响曲",
        "name_en": "Portfolio Symphony",
        "desc": "将股票波动率转化为音乐，MIDI实时生成",
        "desc_en": "Convert stock volatility into music, real-time MIDI generation",
        "detail": "把K线涨跌幅映射为音高和节奏，构建属于你的财富旋律",
        "detail_en": "Map K-line changes to pitch and rhythm, build your own wealth melody",
        "difficulty": "中等",
        "tags": ["投资", "音乐", "量化"]
    },
    {
        "id": "cross_002",
        "name": "代码写歌词",
        "name_en": "Code Lyrics",
        "desc": "用代码逻辑写歌：if 思念 > 阈值 → chorus++",
        "desc_en": "Write lyrics using code logic: if longing > threshold then chorus++",
        "detail": "支持Python/JS/C++风格，生成City Pop/古风/rap",
        "detail_en": "Support Python/JS/C++ styles, generate City Pop/ancient/rap",
        "difficulty": "简单",
        "tags": ["编程", "音乐", "创意"]
    },
    {
        "id": "cross_003",
        "name": "时间胶囊日报",
        "name_en": "Time Capsule Daily",
        "desc": "每天生成未来报纸，预测明天大事",
        "desc_en": "Generate daily 'future newspaper' predicting tomorrow's events",
        "detail": "用GPT生成，日期写成明天，赛博时空胶囊",
        "detail_en": "Written by GPT with tomorrow's date, cyber time capsule",
        "difficulty": "中等",
        "tags": ["AI", "创意", "玄学"]
    },
    {
        "id": "cross_004",
        "name": "梦境投资报告",
        "name_en": "Dream Investment Report",
        "desc": "记录梦境，荣格原型解读+投资决策分析",
        "desc_en": "Record dreams, Jung archetype interpretation + investment analysis",
        "detail": "分析潜意识偏见，解读梦境与持仓的隐藏联系",
        "detail_en": "Analyze subconscious bias, interpret dreams and holdings",
        "difficulty": "困难",
        "tags": ["投资", "心理学", "梦境"]
    },
    {
        "id": "cross_005",
        "name": "推歌算卦",
        "name_en": "Song Fortune",
        "desc": "随机播放三首歌，根据歌名算今日运势",
        "desc_en": "Play 3 random songs, read fortune from song titles",
        "detail": "赛博玄学+音乐推荐，每日运势由天决定",
        "detail_en": "Cyber mysticism + music recommendation, daily fortune by fate",
        "difficulty": "简单",
        "tags": ["音乐", "玄学", "休闲"]
    },
    {
        "id": "cross_006",
        "name": "K线解梦",
        "name_en": "K-Line Dream Interpreter",
        "desc": "睡前看K线，记录梦境第二天复盘",
        "desc_name_en": "Review K-lines before sleep, record dreams for next-day review",
        "detail": "梦见跌停=回调预警，梦见涨停=继续冲",
        "detail_en": "Dream of limit down = pullback warning, dream of limit up = keep going",
        "difficulty": "中等",
        "tags": ["投资", "玄学", "日记"]
    },
    {
        "id": "cross_007",
        "name": "体重涨停板",
        "name_en": "Weight Limit Up",
        "desc": "减肥目标=涨停板，打卡=交易，突破=涨停",
        "desc_en": "Weight loss target = limit up, check-in = trade, break = limit up",
        "detail": "连续破功=跌停，连续达标=连板涨停",
        "detail_en": "Repeated failure = limit down, consistent success = consecutive limit up",
        "difficulty": "简单",
        "tags": ["健康", "游戏化", "投资"]
    },
    {
        "id": "cross_008",
        "name": "读书燃烧卡",
        "name_en": "Reading Burn Card",
        "desc": "边读书边举铁，页数=重量×次数",
        "desc_en": "Read while lifting, pages = weight × reps",
        "detail": "读完一本书解锁成就，燃烧卡路里",
        "detail_en": "Complete a book to unlock achievement, burn calories",
        "difficulty": "中等",
        "tags": ["阅读", "健身", "游戏化"]
    },
    {
        "id": "cross_009",
        "name": "代码情诗",
        "name_en": "Code Love Poem",
        "desc": "用SQL写情书：SELECT * FROM heart WHERE you='true'",
        "desc_en": "Write love letters in SQL: SELECT * FROM heart WHERE you='true'",
        "detail": "程序员专属浪漫，支持多语言版本",
        "detail_en": "Programmer-exclusive romance, multi-language support",
        "difficulty": "简单",
        "tags": ["编程", "创意", "浪漫"]
    },
    {
        "id": "cross_010",
        "name": "错频聊天",
        "name_en": "Delayed Chat",
        "desc": "随机延迟回复1-10秒，模拟正在输入",
        "desc_en": "Randomly delay replies 1-10s, simulate typing",
        "detail": "让聊天更有悬念，测试对方耐心",
        "detail_en": "Make chat more suspenseful, test partner's patience",
        "difficulty": "简单",
        "tags": ["社交", "恶搞", "聊天"]
    }
]

# Multi-language support
LANGUAGES = {
    "zh": {
        "name": "中文",
        "greeting": "嘿，又是你！今天有什么事情想不开？来，给你五个让你脑子晃悠晃的点子：",
        "help_title": "📖 Amazing Idea Generator 使用指南",
        "detail_title": "📖 【{name}】详情 - 让我来给你展开说说～",
        "detail_intro": "💡 一句话概括：{desc}",
        "detail_category": "📂 分类：{category}",
        "detail_plan": "📋 完整方案这就呈上：",
        "fav_title": "❤️ 你的收藏夹：",
        "fav_empty": "📂 你还没有收藏任何点子～",
        "fav_added": "🎉 收入囊中！「{name}」已加入你的宝藏清单～\n\n💡 说「查看收藏」可以随时回顾你的宝贝点子",
        "fav_exists": "🤔 这个点子已经在收藏夹里了～别重复收藏啦！",
        "feedback_good": "👍 收到！Thanks for the love on 「{name}」～让我们知道什么点子更靠谱！",
        "feedback_bad": "📝 收到！We'll work harder on 「{name}」～感谢直言不讳！",
        "feedback_score": "⭐ 记下了！{score}分是对「{name}」的肯定，我们会继续加油！",
        "submit_success": "🚀 点子已发射！你的「{name} - {desc}」已被收录，下次生成可能就是惊喜！",
        "error_no_idea": "没有这个点子哦～",
        "error_unknown": "😅 抱歉，我没听懂～可以说\"help\"查看帮助",
        "hint": "💡 回复数字查看详情，说\"收藏+数字\"收藏，\"好评/差评+数字\"评价，\"help\"查看帮助",
        "hint_detail": "💡 说\"收藏{n}\"收藏，\"好评{n}\"或\"差评{n}\"评价，或\"再来一批\"继续浪～",
        "direction_prompt": "🎯 这次想要什么方向的点子？\n\nA) 提高效率 - 工具、脚本、自动化\nB) 健康生活 - 运动、饮食、心理\nC) 创意娱乐 - 游戏、艺术、音乐\nD) 学习成长 - 阅读、课程、知识\nE) 都可以 - 随机给我来点新鲜的！\n\n💡 回复 A/B/C/D/E 或直接说选项～",
        "direction_confirm": "🎲 收到！让我来给你生成一组{-direction}的点子：",
        "categories": {
            "工具类": "🛠️ 工具类",
            "游戏类": "🎮 游戏类",
            "应用类": "📱 应用类",
            "职场类": "💼 职场类",
            "艺术类": "🎨 艺术类",
            "AI类": "🤖 AI类",
            "生活类": "🏠 生活类",
            "社交类": "💬 社交类",
            "学习类": "📚 学习类",
            "健康类": "💪 健康类",
            "用户投稿": "📥 用户投稿"
        }
    },
    "en": {
        "name": "English",
        "greeting": "Hey, you again! What's bugging you today? Here are 5 ideas to shake up your brain:",
        "help_title": "📖 Amazing Idea Generator User Guide",
        "details_title": "📖 【{name}】详情来啦 - 让我给你展开说说～",
        "detail_intro": "💡 一句话概括：{desc}",
        "detail_category": "📂 Category: {category}",
        "detail_plan": "📋 完整方案这就呈上：",
        "fav_title": "❤️ Your Favorites:",
        "fav_empty": "📂 You haven't saved any ideas yet~",
        "fav_added": "✅ Saved: {name} - {desc}",
        "fav_exists": "⚠️ This idea is already in your favorites~",
        "feedback_good": "⭐ Liked: \"{name}\" Thanks for your feedback! Helps us improve~",
        "feedback_bad": "⭐ Disliked: \"{name}\" Thanks for your feedback! We'll try harder~",
        "feedback_score": "⭐ Rated {score}/5: \"{name}\" Thanks for your feedback!",
        "submit_success": "✅ Submitted! Your idea \"{name} - {desc}\" has been saved. Might appear next time~",
        "error_no_idea": "No such idea~",
        "error_unknown": "😅 Sorry, I didn't get that~ Type \"help\" for instructions",
        "hint": "💡 Reply number for details, \"fav+N\" to save, \"good/bad+N\" to rate, \"help\" for guide",
        "hint_detail": "💡 Say \"fav{n}\" to save, \"good{n}\" or \"bad{n}\" to rate, or \"more\" for more ideas~",
        "direction_prompt": "🎯 What direction do you want this time?\n\nA) Efficiency - Tools, Scripts, Automation\nB) Health - Sports, Diet, Mental\nC) Creative Fun - Games, Art, Music\nD) Learning - Reading, Courses, Knowledge\nE) Random - Surprise me!\n\n💡 Reply A/B/C/D/E or just say the option~",
        "direction_confirm": "🎲 Got it! Generating {-direction} ideas for you:",
        "categories": {
            "工具类": "🛠️ Tools",
            "游戏类": "🎮 Games",
            "应用类": "📱 Apps",
            "职场类": "💼 Workplace",
            "艺术类": "🎨 Art",
            "AI类": "🤖 AI",
            "生活类": "🏠 Lifestyle",
            "社交类": "💬 Social",
            "学习类": "📚 Learning",
            "健康类": "💪 Health",
            "用户投稿": "📥 User Submitted"
        }
    },
    "ja": {
        "name": "日本語",
        "greeting": "よう！また会ったね。今日は何か悩みでも？脳みそを揺さぶる5つのアイデアをどうぞ：",
        "help_title": "📖 Amazing Idea Generator 使い方ガイド",
        "detail_title": "📖 【{name}】詳細",
        "detail_intro": "💡 概要：{desc}",
        "detail_category": "📂 カテゴリー：{category}",
        "detail_plan": "📋 完全なプラン：",
        "fav_title": "❤️ お気に入り：",
        "fav_empty": "📂 まだお気に入りがないよ～",
        "fav_added": "✅ 保存完了：{name} - {desc}",
        "fav_exists": "⚠️ このアイデアは既にお気に入りに入ってるよ～",
        "feedback_good": "⭐ 高評価：「{name}」フィードバックありがとう！",
        "feedback_bad": "⭐ 低評価：「{name}」フィードバックありがとう！改善するね～",
        "feedback_score": "⭐ {score}点：「{name}」フィードバックありがとう！",
        "submit_success": "✅ 投稿完了！「{name} - {desc}」が保存されたよ。次回登場するかも～",
        "error_no_idea": "そんなアイデアはないよ～",
        "error_unknown": "😅 ごめん、わからなかった～「help」で使い方を見てね",
        "hint": "💡 番号で詳細、「fav+番号」で保存、「good/bad+番号」で評価、「help」でガイド",
        "hint_detail": "💡 「fav{n}」で保存、「good{n}」か「bad{n}」で評価、「more」で次のアイデア～",
        "categories": {
            "工具类": "🛠️ ツール",
            "游戏类": "🎮 ゲーム",
            "应用类": "📱 アプリ",
            "职场类": "💼 仕事",
            "艺术类": "🎨 アート",
            "AI类": "🤖 AI",
            "生活类": "🏠 ライフスタイル",
            "社交类": "💬 ソーシャル",
            "学习类": "📚 学習",
            "健康类": "💪 健康",
            "用户投稿": "📥 ユーザー投稿"
        }
    },
    "ko": {
        "name": "한국어",
        "greeting": "야, 또 왔네! 오늘 무슨 고민 있어? 뇌를 흔들어줄 5가지 아이디어를 줄게:",
        "help_title": "📖 Amazing Idea Generator 사용 가이드",
        "detail_title": "📖 【{name}】상세",
        "detail_intro": "💡 소개: {desc}",
        "detail_category": "📂 카테고리: {category}",
        "detail_plan": "📋 전체 계획:",
        "fav_title": "❤️ 즐겨찾기:",
        "fav_empty": "📂 아직 저장된 아이디어가 없어요~",
        "fav_added": "✅ 저장됨: {name} - {desc}",
        "fav_exists": "⚠️ 이미 즐겨찾기에 있어요~",
        "feedback_good": "⭐ 좋아요: 「{name}」피드백 고마워요!",
        "feedback_bad": "⭐ 싫어요: 「{name}」피드백 고마워요! 더 노력할게요~",
        "feedback_score": "⭐ {score}점: 「{name}」피드백 고마워요!",
        "submit_success": "✅ 제출 완료! 「{name} - {desc}」가 저장됐어요. 다음에 나올 수도~",
        "error_no_idea": "그런 아이디어는 없어요~",
        "error_unknown": "😅 미안, 못 알아들었어~ \"help\"를 입력해봐",
        "hint": "💡 번호로 상세보기, \"fav+번호\"로 저장, \"good/bad+번호\"로 평가, \"help\"로 가이드",
        "hint_detail": "💡 \"fav{n}\"로 저장, \"good{n}\" 또는 \"bad{n}\"로 평가, \"more\"로 더 보기~",
        "categories": {
            "工具类": "🛠️ 도구",
            "游戏类": "🎮 게임",
            "应用类": "📱 앱",
            "职场类": "💼 직장",
            "艺术类": "🎨 예술",
            "AI类": "🤖 AI",
            "生活类": "🏠 라이프스타일",
            "社交类": "💬 소셜",
            "学习类": "📚 학습",
            "健康类": "💪 건강",
            "用户投稿": "📥 사용자 제출"
        }
    },
    "es": {
        "name": "Español",
        "greeting": "¡Hola otra vez! ¿Qué te preocupa hoy? Aquí tienes 5 ideas para sacudir tu cerebro:",
        "help_title": "📖 Guía de Amazing Idea Generator",
        "detail_title": "📖 【{name}】Detalles",
        "detail_intro": "💡 Resumen: {desc}",
        "detail_category": "📂 Categoría: {category}",
        "detail_plan": "📋 Plan completo:",
        "fav_title": "❤️ Tus favoritos:",
        "fav_empty": "📂 Aún no tienes ideas guardadas~",
        "fav_added": "✅ Guardado: {name} - {desc}",
        "fav_exists": "⚠️ Esta idea ya está en tus favoritos~",
        "feedback_good": "⭐ Me gusta: \"{name}\" ¡Gracias por tu feedback!",
        "feedback_bad": "⭐ No me gusta: \"{name}\" ¡Gracias! Intentaremos mejorar~",
        "feedback_score": "⭐ {score}/5: \"{name}\" ¡Gracias por tu feedback!",
        "submit_success": "✅ ¡Enviado! Tu idea \"{name} - {desc}\" ha sido guardada. Podría aparecer pronto~",
        "error_no_idea": "No existe esa idea~",
        "error_unknown": "😅 Perdón, no entendí~ Escribe \"help\" para instrucciones",
        "hint": "💡 Responde el número para detalles, \"fav+N\" para guardar, \"good/bad+N\" para calificar",
        "hint_detail": "💡 Di \"fav{n}\" para guardar, \"good{n}\" o \"bad{n}\" para calificar, \"more\" para más~",
        "categories": {
            "工具类": "🛠️ Herramientas",
            "游戏类": "🎮 Juegos",
            "应用类": "📱 Apps",
            "职场类": "💼 Trabajo",
            "艺术类": "🎨 Arte",
            "AI类": "🤖 IA",
            "生活类": "🏠 Estilo de vida",
            "社交类": "💬 Social",
            "学习类": "📚 Aprendizaje",
            "健康类": "💪 Salud",
            "用户投稿": "📥 Enviados"
        }
    },
    "fr": {
        "name": "Français",
        "greeting": "Salut encore ! Qu'est-ce qui te tracasse ? Voici 5 idées pour secouer ton cerveau :",
        "help_title": "📖 Guide Amazing Idea Generator",
        "detail_title": "📖 【{name}】Détails",
        "detail_intro": "💡 Résumé : {desc}",
        "detail_category": "📂 Catégorie : {category}",
        "detail_plan": "📋 Plan complet :",
        "fav_title": "❤️ Vos favoris :",
        "fav_empty": "📂 Vous n'avez pas encore d'idées enregistrées~",
        "fav_added": "✅ Enregistré : {name} - {desc}",
        "fav_exists": "⚠️ Cette idée est déjà dans vos favoris~",
        "feedback_good": "⭐ J'aime : « {name} » Merci pour votre feedback !",
        "feedback_bad": "⭐ J'aime pas : « {name} » Merci ! On va essayer de s'améliorer~",
        "feedback_score": "⭐ {score}/5 : « {name} » Merci pour votre feedback !",
        "submit_success": "✅ Soumis ! Votre idée « {name} - {desc} » a été enregistrée. Elle pourrait apparaître bientôt~",
        "error_no_idea": "Cette idée n'existe pas~",
        "error_unknown": "😅 Désolé, je n'ai pas compris~ Tapez \"help\" pour les instructions",
        "hint": "💡 Répondez le numéro pour les détails, \"fav+N\" pour sauvegarder, \"good/bad+N\" pour noter",
        "hint_detail": "💡 Dites \"fav{n}\" pour sauvegarder, \"good{n}\" ou \"bad{n}\" pour noter, \"more\" pour plus~",
        "categories": {
            "工具类": "🛠️ Outils",
            "游戏类": "🎮 Jeux",
            "应用类": "📱 Apps",
            "职场类": "💼 Travail",
            "艺术类": "🎨 Art",
            "AI类": "🤖 IA",
            "生活类": "🏠 Style de vie",
            "社交类": "💬 Social",
            "学习类": "📚 Apprentissage",
            "健康类": "💪 Santé",
            "用户投稿": "📥 Soumis"
        }
    }
}

# Idea database (10 categories, 10 ideas each) + details
IDEAS = {
    "工具类": [
        {"id": "tool_001", "name": "微信语音烧录器", "name_en": "WeChat Voice Burner", "desc": "把语音消息转化成拉丁舞音频，扔群里整活", "desc_en": "Convert voice messages to Latin dance audio for group fun",
         "detail": "实现思路：调用微信语音转文字API + 文字转语音(TTS) + 随机音乐混合。\n适用场景：朋友生日、整蛊群友、化解尴尬。\n技术栈：Python + WeChat SDK + edge-tts",
         "detail_en": "Approach: WeChat voice-to-text API + TTS + random music mixing.\nUse cases: Birthday pranks, group fun, breaking awkwardness.\nTech: Python + WeChat SDK + edge-tts"},
        {"id": "tool_002", "name": "截图识别菜谱", "name_en": "Screenshot Recipe Reader", "desc": "自动识别图片中的菜谱，生成购物清单", "desc_en": "Auto-recognize recipes from images, generate shopping lists",
         "detail": "实现思路：截图 → OCR识别菜名 → 搜索菜谱API → 生成食材清单。\n适用场景：做饭前采购、看到美食图片想复制。\n技术栈：Python + OCR + 菜谱API",
         "detail_en": "Approach: Screenshot → OCR → Recipe API → Ingredient list.\nUse cases: Pre-cooking shopping, copying food photos.\nTech: Python + OCR + Recipe API"},
        {"id": "tool_003", "name": "快递敲锣提醒", "name_en": "Package Gong Alert", "desc": "包裹到货时播放锣声，神般提醒", "desc_en": "Play gong sound when package arrives, divine notification",
         "detail": "实现思路：接入快递API → 监测物流状态 → 到货时触发音效。\n适用场景：双十一等快递高峰期、怕错过取件码。\n技术栈：Python + 快递鸟API + 音频播放",
         "detail_en": "Approach: Express API → Track status → Trigger sound on arrival.\nUse cases: Shopping festivals, never miss pickup codes.\nTech: Python + Express API + Audio playback"},
        {"id": "tool_004", "name": "电量焦虑预警", "name_en": "Battery Anxiety Alert", "desc": "电量低于20%时自动弹窗，别再摸鱼了", "desc_en": "Auto popup when battery < 20%, stop slacking",
         "detail": "实现思路：系统电量API → 低于阈值弹窗/推送。\n适用场景：提醒充电、续航焦虑症患者。\n技术栈：Python + 系统API",
         "detail_en": "Approach: System battery API → Popup/push when below threshold.\nUse cases: Charging reminders, battery anxiety relief.\nTech: Python + System API"},
        {"id": "tool_005", "name": "会议表情包版", "name_en": "Meeting Meme Generator", "desc": "自动把会议纪要转成表情包，绿色通道", "desc_en": "Auto-convert meeting notes to memes, green channel",
         "detail": "实现思路：会议录音 → 转文字 → 提取关键句 + 生成表情包。\n适用场景：会议纪要存档、给同事分享。\n技术栈：Python + Whisper + 表情包API",
         "detail_en": "Approach: Meeting audio → Text → Key phrases + Meme generation.\nUse cases: Meeting archives, sharing with colleagues.\nTech: Python + Whisper + Meme API"},
        {"id": "tool_006", "name": "自动记账助手", "name_en": "Auto Expense Tracker", "desc": "截图支付记录自动录入账本", "desc_en": "Auto-log expenses from payment screenshots",
         "detail": "实现思路：截图监听 → OCR识别金额/商家 → 自动分类记账。\n适用场景：懒得手动记账、月底对账。\n技术栈：Python + OCR + 记账API",
         "detail_en": "Approach: Screenshot listener → OCR for amount/merchant → Auto-categorize.\nUse cases: Lazy bookkeeping, monthly reconciliation.\nTech: Python + OCR + Accounting API"},
        {"id": "tool_007", "name": "WiFi密码找回器", "name_en": "WiFi Password Recovery", "desc": "一键导出所有连过的WiFi密码", "desc_en": "Export all saved WiFi passwords instantly",
         "detail": "实现思路：读取系统WiFi配置 → 解密保存的密码 → 导出为QR码。\n适用场景：朋友来家里、换手机。\n技术栈：Python + 系统命令 + QR生成",
         "detail_en": "Approach: Read system WiFi config → Decrypt saved passwords → Export as QR.\nUse cases: Friends visiting, new phone setup.\nTech: Python + System commands + QR generation"},
        {"id": "tool_008", "name": "文件重复清理器", "name_en": "Duplicate File Cleaner", "desc": "智能识别并清理重复文件释放空间", "desc_en": "Smart detect and clean duplicate files to free space",
         "detail": "实现思路：文件哈希比对 → 智能保留最新/最大版本 → 批量清理。\n适用场景：磁盘空间不足、下载文件夹混乱。\n技术栈：Python + hashlib",
         "detail_en": "Approach: File hash comparison → Keep newest/largest → Batch clean.\nUse cases: Low disk space, messy downloads folder.\nTech: Python + hashlib"},
        {"id": "tool_009", "name": "剪贴板历史管理", "name_en": "Clipboard History Manager", "desc": "保存剪贴板历史，随时调用", "desc_en": "Save clipboard history, recall anytime",
         "detail": "实现思路：后台监听剪贴板 → 存储历史记录 → 快捷键调出选择。\n适用场景：频繁复制粘贴、代码片段管理。\n技术栈：Python + pyperclip + GUI",
         "detail_en": "Approach: Background clipboard listener → Store history → Hotkey to recall.\nUse cases: Frequent copy-paste, code snippet management.\nTech: Python + pyperclip + GUI"},
        {"id": "tool_010", "name": "批量重命名工具", "name_en": "Batch Rename Tool", "desc": "按规则批量重命名文件，解放双手", "desc_en": "Batch rename files by rules, free your hands",
         "detail": "实现思路：选择文件 → 设置命名规则(序号/日期/替换) → 预览后执行。\n适用场景：照片整理、下载文件重命名。\n技术栈：Python + 正则表达式",
         "detail_en": "Approach: Select files → Set naming rules (sequence/date/replace) → Preview & execute.\nUse cases: Photo organization, downloaded file renaming.\nTech: Python + Regex"},
    ],
    "游戏类": [
        {"id": "game_001", "name": "emoji海龟汤", "name_en": "Emoji Turtle Soup", "desc": "用表情符号玩推理游戏，猜猜什么鬼东西", "desc_en": "Play mystery games with emojis, guess what the heck",
         "detail": "实现思路：预设emoji谜题 → 用户猜答案 → AI判断对错。\n适用场景：群聊互动、破冰游戏。\n技术栈：Python + 猜谜逻辑",
         "detail_en": "Approach: Preset emoji puzzles → User guesses → AI judges.\nUse cases: Group chat fun, ice-breaking.\nTech: Python + Puzzle logic"},
        {"id": "game_002", "name": "盲盒抽卡聊天", "name_en": "Blind Box Chat Cards", "desc": "每次回复都抽一张随机卡牌，增添乐趣", "desc_en": "Draw random cards with each reply, add fun",
         "detail": "实现思路：卡牌池 → 随机抽取 → 带特效展示。\n适用场景：日常聊天、抽卡欧气检测。\n技术栈：Python + 随机池",
         "detail_en": "Approach: Card pool → Random draw → Display with effects.\nUse cases: Daily chat, luck testing.\nTech: Python + Random pool"},
        {"id": "game_003", "name": "角色扮演Bot", "name_en": "Roleplay Bot", "desc": "扮演任意角色24小时，尽情撒欢", "desc_en": "Play any character for 24 hours, go wild",
         "detail": "实现思路：输入角色名 → 设置系统提示词 → 对话模式。\n适用场景：娱乐、创意写作、角色体验。\n技术栈：Python + LLM API",
         "detail_en": "Approach: Input character → Set system prompt → Chat mode.\nUse cases: Entertainment, creative writing, role experience.\nTech: Python + LLM API"},
        {"id": "game_004", "name": "倒计时竞猜", "name_en": "Countdown Betting", "desc": "猜某个事件发生时间，赢家可乱来", "desc_en": "Guess when events happen, winner gets to do whatever",
         "detail": "实现思路：设置事件 → 多人竞猜 → 最近者获胜。\n适用场景：发布会竞猜、比赛结果预测。\n技术栈：Python + 计时逻辑",
         "detail_en": "Approach: Set event → Multiple guesses → Closest wins.\nUse cases: Launch predictions, match results.\nTech: Python + Timer logic"},
        {"id": "game_005", "name": "狼人杀聊天室", "name_en": "Werewolf Chat Room", "desc": "简化版狼人杀，AI当法官", "desc_en": "Simplified Werewolf game, AI as judge",
         "detail": "实现思路：AI控制流程 → 夜间操作 → 白天发言 → 投票。\n适用场景：线上狼人杀、缺法官时。\n技术栈：Python + 状态机",
         "detail_en": "Approach: AI controls flow → Night actions → Day discussion → Vote.\nUse cases: Online Werewolf, when no judge available.\nTech: Python + State machine"},
        {"id": "game_006", "name": "成语接龙AI", "name_en": "Idiom Chain AI", "desc": "和AI玩成语接龙，看谁先词穷", "desc_en": "Play idiom chain with AI, see who runs out first",
         "detail": "实现思路：成语词库 → 首尾字匹配 → AI快速响应。\n适用场景：语文学习、群聊游戏。\n技术栈：Python + 成语数据库",
         "detail_en": "Approach: Idiom database → Match last/first character → AI quick response.\nUse cases: Language learning, group chat games.\nTech: Python + Idiom database"},
        {"id": "game_007", "name": "你画我猜AI版", "name_en": "AI Pictionary", "desc": "AI画图你来猜，或者你画AI猜", "desc_en": "AI draws you guess, or you draw AI guesses",
         "detail": "实现思路：文字转图像生成 → 用户猜词 / 图像识别 → AI猜词。\n适用场景：亲子互动、创意游戏。\n技术栈：Python + DALL-E / CLIP",
         "detail_en": "Approach: Text-to-image generation → User guesses / Image recognition → AI guesses.\nUse cases: Family fun, creative games.\nTech: Python + DALL-E / CLIP"},
        {"id": "game_008", "name": "文字冒险游戏", "name_en": "Text Adventure Game", "desc": "AI生成无限剧情的文字冒险", "desc_en": "AI-generated infinite text adventure",
         "detail": "实现思路：用户选择 → AI生成剧情分支 → 实时响应。\n适用场景：消磨时间、创意体验。\n技术栈：Python + LLM",
         "detail_en": "Approach: User choice → AI generates story branch → Real-time response.\nUse cases: Killing time, creative experience.\nTech: Python + LLM"},
        {"id": "game_009", "name": "谁是卧底AI版", "name_en": "AI Spyfall", "desc": "AI主持谁是卧底游戏", "desc_en": "AI hosts Spyfall game",
         "detail": "实现思路：分配角色 → AI主持投票 → 揭示结果。\n适用场景：群聊游戏、聚会活动。\n技术栈：Python + 游戏逻辑",
         "detail_en": "Approach: Assign roles → AI hosts voting → Reveal results.\nUse cases: Group chat games, party activities.\nTech: Python + Game logic"},
        {"id": "game_010", "name": "每日一谜", "name_en": "Daily Riddle", "desc": "每天推送一个谜题，答对有积分", "desc_en": "Daily riddle push, points for correct answers",
         "detail": "实现思路：谜题库 → 定时推送 → 答案验证 → 积分系统。\n适用场景：日常脑力锻炼、群聊互动。\n技术栈：Python + 定时任务 + 数据库",
         "detail_en": "Approach: Riddle database → Scheduled push → Answer verification → Points system.\nUse cases: Daily brain exercise, group interaction.\nTech: Python + Scheduled tasks + Database"},
    ],
    "应用类": [
        {"id": "app_001", "name": "已读不回检测", "name_en": "Read-Ignored Detector", "desc": "检测好友是否狠狠地不回你", "desc_en": "Detect if friends read but ignore you",
         "detail": "实现思路：监听消息状态 → 记录已读时间 → 超过阈值提醒。\n适用场景：测试友情、好奇心驱动。\n技术栈：iOS Shortcut / Android Tasker",
         "detail_en": "Approach: Monitor message status → Record read time → Alert if timeout.\nUse cases: Testing friendship, curiosity.\nTech: iOS Shortcut / Android Tasker"},
        {"id": "app_002", "name": "反向TodoList", "name_en": "Reverse TodoList", "desc": "记录'不要做什么'，防惹麻烦", "desc_en": "Record 'what NOT to do', avoid trouble",
         "detail": "实现思路：记录负面清单 → 触发时提醒。\n适用场景：自律、避免踩坑。\n技术栈：Notion API + 提醒",
         "detail_en": "Approach: Record negative list → Remind when triggered.\nUse cases: Self-discipline, avoiding pitfalls.\nTech: Notion API + Reminders"},
        {"id": "app_003", "name": "夸夸日记", "name_en": "Praise Diary", "desc": "每天生成3条夸自己的文案", "desc_en": "Generate 3 self-praise lines daily",
         "detail": "实现思路：预设夸夸模板 → 随机组合 → 定时推送。\n适用场景：自信提升、正能量每日打卡。\n技术栈：Python + 定时任务",
         "detail_en": "Approach: Praise templates → Random combination → Scheduled push.\nUse cases: Confidence boost, daily positivity.\nTech: Python + Scheduled tasks"},
        {"id": "app_004", "name": "决策疲劳缓解", "name_en": "Decision Fatigue Relief", "desc": "累了就让我帮你做简单决定", "desc_en": "Let me make simple decisions when you're tired",
         "detail": "实现思路：输入选项 → 随机/加权选择。\n适用场景：选择困难症、日常纠结。\n技术栈：Python",
         "detail_en": "Approach: Input options → Random/weighted selection.\nUse cases: Choice paralysis, daily dilemmas.\nTech: Python"},
        {"id": "app_005", "name": "懒人闹钟", "name_en": "Lazy Alarm", "desc": "设置后需要解数学题才能关闭，爬不起的挣扎", "desc_en": "Solve math problems to turn off, struggle to wake up",
         "detail": "实现思路：闹钟响起 → 显示数学题 → 答对才能关闭。\n适用场景：起床困难户。\n技术栈：Android Tasker / iOS Shortcut",
         "detail_en": "Approach: Alarm rings → Show math problem → Correct answer to dismiss.\nUse cases: Heavy sleepers.\nTech: Android Tasker / iOS Shortcut"},
        {"id": "app_006", "name": "心情天气日记", "name_en": "Mood Weather Diary", "desc": "根据天气自动生成心情日记模板", "desc_en": "Auto-generate mood diary templates based on weather",
         "detail": "实现思路：获取天气API → 匹配心情模板 → 生成日记框架。\n适用场景：日记爱好者、情绪记录。\n技术栈：Python + 天气API + 模板",
         "detail_en": "Approach: Weather API → Match mood template → Generate diary framework.\nUse cases: Diary enthusiasts, mood tracking.\nTech: Python + Weather API + Templates"},
        {"id": "app_007", "name": "专注番茄钟", "name_en": "Focus Pomodoro", "desc": "带白噪音和成就系统的番茄钟", "desc_en": "Pomodoro timer with white noise and achievements",
         "detail": "实现思路：计时器 → 白噪音播放 → 完成后成就解锁。\n适用场景：学习工作、专注力训练。\n技术栈：Python + 音频播放 + GUI",
         "detail_en": "Approach: Timer → White noise playback → Achievement unlock on completion.\nUse cases: Study/work, focus training.\nTech: Python + Audio playback + GUI"},
        {"id": "app_008", "name": "习惯养成追踪", "name_en": "Habit Tracker", "desc": "可视化习惯养成进度，连续打卡奖励", "desc_en": "Visualize habit progress, streak rewards",
         "detail": "实现思路：记录打卡 → 连续天数统计 → 可视化图表 → 奖励系统。\n适用场景：健身、阅读、早起等习惯养成。\n技术栈：Python + 数据可视化",
         "detail_en": "Approach: Log check-ins → Streak counting → Visual charts → Reward system.\nUse cases: Fitness, reading, early rising habits.\nTech: Python + Data visualization"},
        {"id": "app_009", "name": "随机午餐选择器", "name_en": "Random Lunch Picker", "desc": "解决每天中午吃什么的终极问题", "desc_en": "Solve the ultimate 'what to eat for lunch' problem",
         "detail": "实现思路：附近餐厅列表 → 随机选择 → 显示评分/距离。\n适用场景：选择困难症、午餐纠结。\n技术栈：Python + 地图API",
         "detail_en": "Approach: Nearby restaurant list → Random pick → Show rating/distance.\nUse cases: Choice paralysis, lunch dilemmas.\nTech: Python + Map API"},
        {"id": "app_010", "name": "年度回顾生成器", "name_en": "Year in Review Generator", "desc": "自动生成年度总结报告", "desc_en": "Auto-generate annual summary report",
         "detail": "实现思路：汇总年度数据 → 生成图表 → AI撰写总结文案。\n适用场景：年终总结、朋友圈年度回顾。\n技术栈：Python + 数据分析 + LLM",
         "detail_en": "Approach: Aggregate yearly data → Generate charts → AI writes summary.\nUse cases: Year-end summary, social media annual review.\nTech: Python + Data analysis + LLM"},
    ],
    "职场类": [
        {"id": "work_001", "name": "会议表情包版", "name_en": "Meeting Meme Version", "desc": "会议纪要自动转表情包版", "desc_en": "Auto-convert meeting notes to meme version",
         "detail": "同工具类会议表情包版。", "detail_en": "Same as Tools category Meeting Meme Generator."},
        {"id": "work_002", "name": "AI辞职信写手", "name_en": "AI Resignation Writer", "desc": "带槽点的搞笑辞职信", "desc_en": "Funny resignation letters with sass",
         "detail": "实现思路：输入公司名/离职原因 → 生成搞笑辞职信。\n适用场景：离职整活、朋友圈素材。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input company/reason → Generate funny resignation.\nUse cases: Resignation pranks, social media content.\nTech: Python + LLM"},
        {"id": "work_003", "name": "摸鱼时间计算", "name_en": "Slacking Time Calculator", "desc": "计算你今天摸鱼的时长", "desc_en": "Calculate how long you've slacked today",
         "detail": "实现思路：记录工作时间内的空闲时段 → 统计摸鱼时长。\n适用场景：自我审计、摸鱼成就感。\n技术栈：Python + 时间追踪",
         "detail_en": "Approach: Track idle time during work hours → Calculate slacking time.\nUse cases: Self-audit, slacking achievement.\nTech: Python + Time tracking"},
        {"id": "work_004", "name": "职场黑话翻译", "name_en": "Corporate Jargon Translator", "desc": "把官话翻成通俗语", "desc_en": "Translate corporate speak to plain language",
         "detail": "实现思路：预设黑话词库 → 替换为直白表达。\n适用场景：职场新人、开会听不懂。\n技术栈：Python + 词库",
         "detail_en": "Approach: Preset jargon dictionary → Replace with plain language.\nUse cases: New employees, confusing meetings.\nTech: Python + Dictionary"},
        {"id": "work_005", "name": "同事情绪监测", "name_en": "Colleague Mood Monitor", "desc": "通过聊天分析同事心情", "desc_en": "Analyze colleague mood through chat",
         "detail": "实现思路：分析聊天语气 → 判断情绪倾向（仅供娱乐）。\n适用场景：同事关系、避坑。\n技术栈：Python + 情感分析",
         "detail_en": "Approach: Analyze chat tone → Determine mood (for fun only).\nUse cases: Office politics, avoiding pitfalls.\nTech: Python + Sentiment analysis"},
        {"id": "work_006", "name": "周报自动生成", "name_en": "Weekly Report Generator", "desc": "根据工作记录自动生成周报", "desc_en": "Auto-generate weekly report from work logs",
         "detail": "实现思路：汇总本周任务 → AI生成周报模板 → 填充关键数据。\n适用场景：周报焦虑、汇报准备。\n技术栈：Python + LLM + 任务API",
         "detail_en": "Approach: Summarize weekly tasks → AI generates template → Fill key data.\nUse cases: Weekly report anxiety, presentation prep.\nTech: Python + LLM + Task API"},
        {"id": "work_007", "name": "会议效率分析", "name_en": "Meeting Efficiency Analyzer", "desc": "分析会议时长和产出比", "desc_en": "Analyze meeting duration vs output ratio",
         "detail": "实现思路：记录会议时长 → 统计决策数量 → 计算效率分数。\n适用场景：优化会议、团队管理。\n技术栈：Python + 数据分析",
         "detail_en": "Approach: Log meeting duration → Count decisions → Calculate efficiency score.\nUse cases: Meeting optimization, team management.\nTech: Python + Data analysis"},
        {"id": "work_008", "name": "邮件智能回复", "name_en": "Smart Email Reply", "desc": "一键生成得体的邮件回复", "desc_en": "One-click generate professional email replies",
         "detail": "实现思路：分析邮件内容 → 识别意图 → 生成回复选项。\n适用场景：邮件堆积、回复焦虑。\n技术栈：Python + LLM + 邮件API",
         "detail_en": "Approach: Analyze email content → Identify intent → Generate reply options.\nUse cases: Email backlog, reply anxiety.\nTech: Python + LLM + Email API"},
        {"id": "work_009", "name": "加班时长统计", "name_en": "Overtime Tracker", "desc": "自动统计加班时长，生成调休建议", "desc_en": "Auto-track overtime, generate time-off suggestions",
         "detail": "实现思路：打卡记录分析 → 计算加班时长 → 生成调休报告。\n适用场景：加班维权、调休管理。\n技术栈：Python + 数据分析",
         "detail_en": "Approach: Analyze clock-in records → Calculate overtime → Generate time-off report.\nUse cases: Overtime tracking, time-off management.\nTech: Python + Data analysis"},
        {"id": "work_010", "name": "简历优化助手", "name_en": "Resume Optimizer", "desc": "AI优化简历，提高面试邀请率", "desc_en": "AI optimize resume, increase interview invites",
         "detail": "实现思路：分析职位JD → 对比简历 → 生成优化建议。\n适用场景：求职、跳槽。\n技术栈：Python + LLM",
         "detail_en": "Approach: Analyze job description → Compare with resume → Generate optimization tips.\nUse cases: Job hunting, career change.\nTech: Python + LLM"},
    ],
    "艺术类": [
        {"id": "art_001", "name": "歌单生成抽象画", "name_en": "Playlist Abstract Art", "desc": "根据听歌记录生成独特艺术作品", "desc_en": "Generate unique art from listening history",
         "detail": "实现思路：获取网易云/QQ音乐播放记录 → 提取特征 → AI绘画。\n适用场景：专属头像、朋友圈装X。\n技术栈：Python + Midjourney/Stable Diffusion",
         "detail_en": "Approach: Get music history → Extract features → AI art.\nUse cases: Custom avatars, social media flex.\nTech: Python + Midjourney/Stable Diffusion"},
        {"id": "art_002", "name": "梦境解析AI", "name_en": "Dream Interpreter AI", "desc": "输入梦境，AI给你解读梦意", "desc_en": "Input dreams, AI interprets meaning",
         "detail": "实现思路：梦境描述 → 解析模型 → 生成解释。\n适用场景：好奇宝宝、睡前娱乐。\n技术栈：Python + LLM",
         "detail_en": "Approach: Dream description → Analysis model → Generate interpretation.\nUse cases: Curious minds, bedtime fun.\nTech: Python + LLM"},
        {"id": "art_003", "name": "随机诗歌生成", "name_en": "Random Poetry Generator", "desc": "根据心情随机生成一首诗", "desc_en": "Generate random poems based on mood",
         "detail": "实现思路：输入心情/关键词 → 生成诗歌。\n适用场景：文案灵感、情绪表达。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input mood/keywords → Generate poem.\nUse cases: Copywriting inspiration, emotional expression.\nTech: Python + LLM"},
        {"id": "art_004", "name": "音乐可视化背景", "name_en": "Music Visualizer Background", "desc": "把歌曲转成动态聊天背景", "desc_en": "Convert songs to dynamic chat backgrounds",
         "detail": "实现思路：音频分析 → 生成动态背景。\n适用场景：个性化聊天背景。\n技术栈：Python + 音频可视化",
         "detail_en": "Approach: Audio analysis → Generate dynamic background.\nUse cases: Personalized chat backgrounds.\nTech: Python + Audio visualization"},
        {"id": "art_005", "name": "朋友圈配文生成", "name_en": "Social Media Caption Generator", "desc": "为你的照片生成煽情配文", "desc_en": "Generate emotional captions for your photos",
         "detail": "实现思路：图片识别 → 生成配文。\n适用场景：朋友圈更新、社交媒体。\n技术栈：Python + CV + LLM",
         "detail_en": "Approach: Image recognition → Generate caption.\nUse cases: Social media updates.\nTech: Python + CV + LLM"},
        {"id": "art_006", "name": "AI头像生成器", "name_en": "AI Avatar Generator", "desc": "根据描述生成个性化头像", "desc_en": "Generate personalized avatars from description",
         "detail": "实现思路：输入风格描述 → AI生成头像 → 多风格选择。\n适用场景：社交媒体头像、游戏角色。\n技术栈：Python + Stable Diffusion",
         "detail_en": "Approach: Input style description → AI generates avatar → Multiple style options.\nUse cases: Social media avatars, game characters.\nTech: Python + Stable Diffusion"},
        {"id": "art_007", "name": "歌词续写助手", "name_en": "Lyric Continuation Helper", "desc": "输入开头，AI帮你写完整歌词", "desc_en": "Input beginning, AI writes complete lyrics",
         "detail": "实现思路：分析已有歌词风格 → 续写押韵歌词 → 多版本选择。\n适用场景：音乐创作、歌词灵感。\n技术栈：Python + LLM",
         "detail_en": "Approach: Analyze existing lyric style → Continue with rhyming lyrics → Multiple versions.\nUse cases: Music creation, lyric inspiration.\nTech: Python + LLM"},
        {"id": "art_008", "name": "故事开头生成器", "name_en": "Story Starter Generator", "desc": "生成各种类型的故事开头", "desc_en": "Generate story openings of various genres",
         "detail": "实现思路：选择类型 → AI生成开头 → 可继续续写。\n适用场景：写作灵感、创意练习。\n技术栈：Python + LLM",
         "detail_en": "Approach: Select genre → AI generates opening → Can continue writing.\nUse cases: Writing inspiration, creative practice.\nTech: Python + LLM"},
        {"id": "art_009", "name": "表情包生成器", "name_en": "Meme Generator", "desc": "根据文字自动生成表情包", "desc_en": "Auto-generate memes from text",
         "detail": "实现思路：文字分析 → 匹配表情模板 → 生成表情包。\n适用场景：聊天斗图、社交媒体。\n技术栈：Python + 图像处理 + 模板库",
         "detail_en": "Approach: Text analysis → Match meme template → Generate meme.\nUse cases: Chat battles, social media.\nTech: Python + Image processing + Template library"},
        {"id": "art_010", "name": "配色方案生成", "name_en": "Color Palette Generator", "desc": "根据主题生成配色方案", "desc_en": "Generate color palettes based on themes",
         "detail": "实现思路：输入主题/图片 → 提取主色调 → 生成配色方案。\n适用场景：设计灵感、PPT配色。\n技术栈：Python + 图像处理",
         "detail_en": "Approach: Input theme/image → Extract dominant colors → Generate palette.\nUse cases: Design inspiration, PPT color schemes.\nTech: Python + Image processing"},
    ],
    "AI类": [
        {"id": "ai_001", "name": "AI辞职信写手", "name_en": "AI Resignation Writer", "desc": "给我写个带槽点的辞职信", "desc_en": "Write a sassy resignation letter",
         "detail": "同职场类AI辞职信写手。", "detail_en": "Same as Workplace category AI Resignation Writer."},
        {"id": "ai_002", "name": "AI替你吵架", "name_en": "AI Argues For You", "desc": "输进去对话，我帮你怼回去", "desc_en": "Input conversation, I'll argue back for you",
         "detail": "实现思路：输入对方言论 → 生成怼人回复（仅供娱乐）。\n适用场景：键盘侠对决、吵架练习。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input opponent's words → Generate comeback (for fun only).\nUse cases: Keyboard warrior battles, argument practice.\nTech: Python + LLM"},
        {"id": "ai_003", "name": "梦境续写", "name_en": "Dream Continuation", "desc": "接上你的梦境继续写", "desc_en": "Continue writing your dreams",
         "detail": "实现思路：输入梦境片段 → AI续写。\n适用场景：梦境记录、创意写作。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input dream fragment → AI continues.\nUse cases: Dream journaling, creative writing.\nTech: Python + LLM"},
        {"id": "ai_004", "name": "AI心理咨询", "name_en": "AI Counseling", "desc": "轻度心理问题，AI来帮你调皮", "desc_en": "Light psychological issues, AI helps playfully",
         "detail": "实现思路：情感分析 + 安慰话术。\n适用场景：情绪疏导、倾诉对象。\n技术栈：Python + LLM（注意：仅供娱乐，严重问题请就医）",
         "detail_en": "Approach: Sentiment analysis + Comforting scripts.\nUse cases: Emotional venting, listening ear.\nTech: Python + LLM (Note: For fun only, seek professional help for serious issues)"},
        {"id": "ai_005", "name": "自动道歉生成", "name_en": "Auto Apology Generator", "desc": "帮你生成道歉语句，减少社交尴尬", "desc_en": "Generate apology messages, reduce social awkwardness",
         "detail": "实现思路：输入情境 → 生成道歉文案。\n适用场景：道歉困难户、社交尴尬。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input situation → Generate apology.\nUse cases: Apology-challenged, social awkwardness.\nTech: Python + LLM"},
        {"id": "ai_006", "name": "AI面试官", "name_en": "AI Interviewer", "desc": "模拟面试场景，帮你练习", "desc_en": "Simulate interview scenarios, help you practice",
         "detail": "实现思路：输入职位 → AI扮演面试官 → 实时反馈。\n适用场景：求职准备、面试练习。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input position → AI plays interviewer → Real-time feedback.\nUse cases: Job hunting prep, interview practice.\nTech: Python + LLM"},
        {"id": "ai_007", "name": "AI辩论对手", "name_en": "AI Debate Opponent", "desc": "选择立场，和AI辩论练习", "desc_en": "Choose a stance, practice debating with AI",
         "detail": "实现思路：输入辩题 → AI扮演反方 → 实时反驳。\n适用场景：辩论训练、思维锻炼。\n技术栈：Python + LLM",
         "detail_en": "Approach: Input debate topic → AI plays opposition → Real-time rebuttal.\nUse cases: Debate training, critical thinking.\nTech: Python + LLM"},
        {"id": "ai_008", "name": "AI翻译官", "name_en": "AI Translator", "desc": "带语境理解的智能翻译", "desc_en": "Smart translation with context understanding",
         "detail": "实现思路：分析语境 → 选择专业术语 → 生成自然翻译。\n适用场景：跨语言沟通、文档翻译。\n技术栈：Python + LLM",
         "detail_en": "Approach: Analyze context → Select professional terms → Generate natural translation.\nUse cases: Cross-language communication, document translation.\nTech: Python + LLM"},
        {"id": "ai_009", "name": "AI代码审查", "name_en": "AI Code Reviewer", "desc": "自动审查代码，提出优化建议", "desc_en": "Auto-review code, suggest optimizations",
         "detail": "实现思路：代码分析 → 识别问题 → 生成优化建议。\n适用场景：代码质量提升、学习编程。\n技术栈：Python + LLM",
         "detail_en": "Approach: Code analysis → Identify issues → Generate optimization suggestions.\nUse cases: Code quality improvement, learning programming.\nTech: Python + LLM"},
        {"id": "ai_010", "name": "AI学习助手", "name_en": "AI Study Buddy", "desc": "根据学习内容生成练习题", "desc_en": "Generate practice questions from study material",
         "detail": "实现思路：分析学习内容 → 生成测验题 → 检验理解程度。\n适用场景：考试复习、知识巩固。\n技术栈：Python + LLM",
         "detail_en": "Approach: Analyze study material → Generate quiz questions → Test understanding.\nUse cases: Exam prep, knowledge consolidation.\nTech: Python + LLM"},
    ],
    "生活类": [
        {"id": "life_001", "name": "冰箱食材管理", "name_en": "Fridge Ingredient Manager", "desc": "记录冰箱食材，提醒保质期", "desc_en": "Track fridge ingredients, remind expiration dates",
         "detail": "实现思路：拍照识别/手动录入 → 追踪保质期 → 临期提醒。\n适用场景：减少食物浪费、购物规划。\n技术栈：Python + OCR + 数据库",
         "detail_en": "Approach: Photo recognition/manual entry → Track expiration → Near-expiry alerts.\nUse cases: Reduce food waste, shopping planning.\nTech: Python + OCR + Database"},
        {"id": "life_002", "name": "植物养护提醒", "name_en": "Plant Care Reminder", "desc": "根据植物类型提醒浇水施肥", "desc_en": "Remind watering and fertilizing based on plant type",
         "detail": "实现思路：录入植物信息 → 根据品种设置养护周期 → 定时提醒。\n适用场景：植物杀手、养花新手。\n技术栈：Python + 定时任务 + 植物数据库",
         "detail_en": "Approach: Log plant info → Set care cycle by species → Scheduled reminders.\nUse cases: Plant killers, gardening beginners.\nTech: Python + Scheduled tasks + Plant database"},
        {"id": "life_003", "name": "宠物健康记录", "name_en": "Pet Health Tracker", "desc": "记录宠物体重、疫苗、驱虫时间", "desc_en": "Track pet weight, vaccines, deworming schedule",
         "detail": "实现思路：录入宠物信息 → 追踪健康数据 → 疫苗驱虫提醒。\n适用场景：多宠物家庭、新手养宠。\n技术栈：Python + 数据库 + 提醒系统",
         "detail_en": "Approach: Log pet info → Track health data → Vaccine/deworming reminders.\nUse cases: Multi-pet households, new pet owners.\nTech: Python + Database + Reminder system"},
        {"id": "life_004", "name": "家庭账本", "name_en": "Family Budget Book", "desc": "多成员共享的家庭财务记录", "desc_en": "Multi-member shared family finance tracker",
         "detail": "实现思路：多用户记账 → 分类统计 → 月度报告。\n适用场景：家庭财务管理、预算控制。\n技术栈：Python + 数据库 + Web界面",
         "detail_en": "Approach: Multi-user bookkeeping → Category statistics → Monthly reports.\nUse cases: Family finance management, budget control.\nTech: Python + Database + Web interface"},
        {"id": "life_005", "name": "旅行清单生成", "name_en": "Travel Checklist Generator", "desc": "根据目的地和天数生成打包清单", "desc_en": "Generate packing list based on destination and duration",
         "detail": "实现思路：输入目的地/天数 → 匹配清单模板 → 生成个性化清单。\n适用场景：旅行准备、出差打包。\n技术栈：Python + 清单数据库",
         "detail_en": "Approach: Input destination/duration → Match checklist template → Generate personalized list.\nUse cases: Travel prep, business trip packing.\nTech: Python + Checklist database"},
        {"id": "life_006", "name": "家务分工轮值", "name_en": "Household Chores Rotation", "desc": "自动分配家务任务，公平轮值", "desc_en": "Auto-assign household tasks, fair rotation",
         "detail": "实现思路：录入家庭成员和任务 → 自动轮值分配 → 完成打卡。\n适用场景：合租、家庭家务分配。\n技术栈：Python + 轮值算法 + 通知",
         "detail_en": "Approach: Log members and tasks → Auto rotation assignment → Completion check-in.\nUse cases: Shared housing, family chore distribution.\nTech: Python + Rotation algorithm + Notifications"},
        {"id": "life_007", "name": "菜谱推荐器", "name_en": "Recipe Recommender", "desc": "根据现有食材推荐菜谱", "desc_en": "Recommend recipes based on available ingredients",
         "detail": "实现思路：输入现有食材 → 匹配菜谱数据库 → 推荐可做菜品。\n适用场景：不知道做什么菜、食材利用。\n技术栈：Python + 菜谱API + 匹配算法",
         "detail_en": "Approach: Input available ingredients → Match recipe database → Recommend dishes.\nUse cases: Don't know what to cook, ingredient utilization.\nTech: Python + Recipe API + Matching algorithm"},
        {"id": "life_008", "name": "天气穿衣建议", "name_en": "Weather Outfit Advisor", "desc": "根据天气推荐今日穿搭", "desc_en": "Recommend today's outfit based on weather",
         "detail": "实现思路：获取天气 → 匹配穿衣规则 → 生成穿搭建议。\n适用场景：选择困难、天气变化大。\n技术栈：Python + 天气API + 穿搭规则",
         "detail_en": "Approach: Get weather → Match outfit rules → Generate outfit suggestions.\nUse cases: Choice paralysis, variable weather.\nTech: Python + Weather API + Outfit rules"},
        {"id": "life_009", "name": "快递代收点地图", "name_en": "Package Pickup Map", "desc": "标记附近快递代收点，一键导航", "desc_en": "Mark nearby pickup points, one-click navigation",
         "detail": "实现思路：定位 → 搜索附近代收点 → 显示评分和导航。\n适用场景：新小区、不熟悉周边。\n技术栈：Python + 地图API + 定位",
         "detail_en": "Approach: Location → Search nearby pickup points → Show ratings and navigation.\nUse cases: New neighborhood, unfamiliar area.\nTech: Python + Map API + Location"},
        {"id": "life_010", "name": "纪念日倒计时", "name_en": "Anniversary Countdown", "desc": "重要日期提醒，提前准备礼物", "desc_en": "Important date reminders, prep gifts in advance",
         "detail": "实现思路：录入重要日期 → 提前N天提醒 → 礼物建议。\n适用场景：忘记纪念日、生日准备。\n技术栈：Python + 定时任务 + 提醒",
         "detail_en": "Approach: Log important dates → Remind N days ahead → Gift suggestions.\nUse cases: Forgetting anniversaries, birthday prep.\nTech: Python + Scheduled tasks + Reminders"},
    ],
    "社交类": [
        {"id": "social_001", "name": "群聊活跃度分析", "name_en": "Group Chat Activity Analyzer", "desc": "分析群聊活跃度，找出潜水党", "desc_en": "Analyze group chat activity, find lurkers",
         "detail": "实现思路：统计发言频率 → 生成活跃度报告 → 识别潜水成员。\n适用场景：群管理、社群运营。\n技术栈：Python + 数据分析",
         "detail_en": "Approach: Count message frequency → Generate activity report → Identify lurkers.\nUse cases: Group management, community operations.\nTech: Python + Data analysis"},
        {"id": "social_002", "name": "朋友圈定时发布", "name_en": "Scheduled Moments Post", "desc": "定时发布朋友圈，不错过黄金时段", "desc_en": "Schedule moments posts, never miss prime time",
         "detail": "实现思路：编辑内容 → 设置发布时间 → 自动发布。\n适用场景：营销号、生活记录。\n技术栈：Python + 自动化脚本",
         "detail_en": "Approach: Edit content → Set publish time → Auto publish.\nUse cases: Marketing accounts, life logging.\nTech: Python + Automation scripts"},
        {"id": "social_003", "name": "群发消息助手", "name_en": "Mass Message Helper", "desc": "个性化群发消息，避免群发感", "desc_en": "Personalized mass messaging, avoid spam feel",
         "detail": "实现思路：导入联系人 → 设置变量替换 → 个性化群发。\n适用场景：节日祝福、活动通知。\n技术栈：Python + 通讯录API",
         "detail_en": "Approach: Import contacts → Set variable replacement → Personalized mass send.\nUse cases: Holiday greetings, event notifications.\nTech: Python + Contacts API"},
        {"id": "social_004", "name": "社交礼仪提醒", "name_en": "Social Etiquette Reminder", "desc": "提醒回复消息、生日祝福等", "desc_en": "Remind to reply messages, send birthday wishes",
         "detail": "实现思路：监测未回复消息 → 生日提醒 → 礼仪建议。\n适用场景：社交焦虑、健忘症。\n技术栈：Python + 提醒系统",
         "detail_en": "Approach: Monitor unreplied messages → Birthday reminders → Etiquette tips.\nUse cases: Social anxiety, forgetfulness.\nTech: Python + Reminder system"},
        {"id": "social_005", "name": "聊天话题生成", "name_en": "Chat Topic Generator", "desc": "根据对方兴趣生成聊天话题", "desc_en": "Generate chat topics based on their interests",
         "detail": "实现思路：分析对方社交动态 → 提取兴趣标签 → 生成话题建议。\n适用场景：相亲、社交尴尬、破冰。\n技术栈：Python + LLM + 社交API",
         "detail_en": "Approach: Analyze their social posts → Extract interest tags → Generate topic suggestions.\nUse cases: Dating, social awkwardness, ice-breaking.\nTech: Python + LLM + Social API"},
        {"id": "social_006", "name": "红包提醒助手", "name_en": "Red Packet Alert", "desc": "群红包秒提醒，不再错过", "desc_en": "Instant red packet alerts, never miss again",
         "detail": "实现思路：监听群消息 → 识别红包 → 立即通知。\n适用场景：红包群、手慢无。\n技术栈：Python + 消息监听",
         "detail_en": "Approach: Monitor group messages → Detect red packet → Instant notification.\nUse cases: Red packet groups, slow fingers.\nTech: Python + Message listener"},
        {"id": "social_007", "name": "好友标签管理", "name_en": "Friend Tag Manager", "desc": "智能分类好友，添加标签备注", "desc_en": "Smart friend categorization, add tags and notes",
         "detail": "实现思路：分析互动频率 → 自动分类 → 标签管理。\n适用场景：好友太多、人脉管理。\n技术栈：Python + 通讯录API",
         "detail_en": "Approach: Analyze interaction frequency → Auto categorize → Tag management.\nUse cases: Too many friends, network management.\nTech: Python + Contacts API"},
        {"id": "social_008", "name": "群聊关键词提醒", "name_en": "Group Keyword Alert", "desc": "群聊出现关键词时提醒你", "desc_en": "Alert when keywords appear in group chat",
         "detail": "实现思路：设置关键词 → 监听群消息 → 匹配时通知。\n适用场景：关注特定话题、工作群。\n技术栈：Python + 消息监听",
         "detail_en": "Approach: Set keywords → Monitor group messages → Notify on match.\nUse cases: Following specific topics, work groups.\nTech: Python + Message listener"},
        {"id": "social_009", "name": "社交倦怠检测", "name_en": "Social Burnout Detector", "desc": "分析社交频率，提醒适当休息", "desc_en": "Analyze social frequency, remind to rest",
         "detail": "实现思路：统计社交时长 → 分析疲劳度 → 生成休息建议。\n适用场景：社交过度、内向者充电。\n技术栈：Python + 数据分析",
         "detail_en": "Approach: Count social time → Analyze fatigue level → Generate rest suggestions.\nUse cases: Social overload, introvert recharging.\nTech: Python + Data analysis"},
        {"id": "social_010", "name": "表情包收藏整理", "name_en": "Meme Collection Organizer", "desc": "自动分类整理收藏的表情包", "desc_en": "Auto-categorize saved memes",
         "detail": "实现思路：识别表情包内容 → 自动分类 → 快速搜索。\n适用场景：表情包太多、斗图需求。\n技术栈：Python + 图像识别 + 分类算法",
         "detail_en": "Approach: Recognize meme content → Auto categorize → Quick search.\nUse cases: Too many memes, chat battle needs.\nTech: Python + Image recognition + Classification"},
    ],
    "学习类": [
        {"id": "learn_001", "name": "单词记忆卡片", "name_en": "Vocabulary Flashcard", "desc": "艾宾浩斯遗忘曲线背单词", "desc_en": "Ebbinghaus curve vocabulary learning",
         "detail": "实现思路：录入单词 → 按遗忘曲线安排复习 → 测试记忆效果。\n适用场景：英语学习、考试备考。\n技术栈：Python + 间隔重复算法",
         "detail_en": "Approach: Log words → Schedule review by forgetting curve → Test memory.\nUse cases: English learning, exam prep.\nTech: Python + Spaced repetition algorithm"},
        {"id": "learn_002", "name": "读书笔记整理", "name_en": "Reading Notes Organizer", "desc": "自动整理读书笔记，生成摘要", "desc_en": "Auto-organize reading notes, generate summary",
         "detail": "实现思路：导入笔记 → AI提取要点 → 生成结构化摘要。\n适用场景：阅读爱好者、知识管理。\n技术栈：Python + LLM",
         "detail_en": "Approach: Import notes → AI extracts key points → Generate structured summary.\nUse cases: Book lovers, knowledge management.\nTech: Python + LLM"},
        {"id": "learn_003", "name": "知识点关联图", "name_en": "Knowledge Graph Builder", "desc": "可视化知识点之间的关联", "desc_en": "Visualize connections between knowledge points",
         "detail": "实现思路：分析学习内容 → 提取概念关系 → 生成知识图谱。\n适用场景：系统学习、知识梳理。\n技术栈：Python + 知识图谱 + 可视化",
         "detail_en": "Approach: Analyze learning content → Extract concept relations → Generate knowledge graph.\nUse cases: Systematic learning, knowledge organization.\nTech: Python + Knowledge graph + Visualization"},
        {"id": "learn_004", "name": "错题本智能整理", "name_en": "Smart Mistake Notebook", "desc": "自动分类错题，推荐相似题练习", "desc_en": "Auto-categorize mistakes, recommend similar problems",
         "detail": "实现思路：录入错题 → 分析错误类型 → 推荐同类题目。\n适用场景：考试复习、薄弱点攻克。\n技术栈：Python + 题库API + 分类算法",
         "detail_en": "Approach: Log mistakes → Analyze error types → Recommend similar problems.\nUse cases: Exam review, weakness targeting.\nTech: Python + Question bank API + Classification"},
        {"id": "learn_005", "name": "学习时长统计", "name_en": "Study Time Tracker", "desc": "统计各科目学习时长，分析效率", "desc_en": "Track study time by subject, analyze efficiency",
         "detail": "实现思路：记录学习时间 → 分类统计 → 生成效率报告。\n适用场景：时间管理、学习规划。\n技术栈：Python + 数据分析",
         "detail_en": "Approach: Log study time → Categorize statistics → Generate efficiency report.\nUse cases: Time management, study planning.\nTech: Python + Data analysis"},
        {"id": "learn_006", "name": "论文参考文献管理", "name_en": "Paper Reference Manager", "desc": "自动格式化参考文献，一键导出", "desc_en": "Auto-format references, one-click export",
         "detail": "实现思路：导入文献信息 → 选择引用格式 → 自动生成引用。\n适用场景：论文写作、学术研究。\n技术栈：Python + 文献数据库",
         "detail_en": "Approach: Import reference info → Select citation format → Auto-generate citation.\nUse cases: Paper writing, academic research.\nTech: Python + Reference database"},
        {"id": "learn_007", "name": "在线课程进度追踪", "name_en": "Online Course Progress Tracker", "desc": "追踪多平台课程进度，统一管理", "desc_en": "Track multi-platform course progress, unified management",
         "detail": "实现思路：导入课程列表 → 记录观看进度 → 统一展示。\n适用场景：多平台学习、课程管理。\n技术栈：Python + 数据库 + Web界面",
         "detail_en": "Approach: Import course list → Record viewing progress → Unified display.\nUse cases: Multi-platform learning, course management.\nTech: Python + Database + Web interface"},
        {"id": "learn_008", "name": "知识点测验生成", "name_en": "Knowledge Quiz Generator", "desc": "根据学习内容自动生成测验题", "desc_en": "Auto-generate quiz from learning content",
         "detail": "实现思路：分析学习材料 → 提取关键概念 → 生成测验题。\n适用场景：自测、复习巩固。\n技术栈：Python + LLM",
         "detail_en": "Approach: Analyze learning material → Extract key concepts → Generate quiz.\nUse cases: Self-testing, review consolidation.\nTech: Python + LLM"},
        {"id": "learn_009", "name": "学习小组匹配", "name_en": "Study Group Matcher", "desc": "匹配学习目标和时间相近的伙伴", "desc_en": "Match study partners with similar goals and schedules",
         "detail": "实现思路：录入学习目标/时间 → 匹配算法 → 推荐学习伙伴。\n适用场景：找学习搭子、互相监督。\n技术栈：Python + 匹配算法",
         "detail_en": "Approach: Log study goals/schedule → Matching algorithm → Recommend study partners.\nUse cases: Finding study buddies, mutual accountability.\nTech: Python + Matching algorithm"},
        {"id": "learn_010", "name": "思维导图生成", "name_en": "Mind Map Generator", "desc": "根据笔记自动生成思维导图", "desc_en": "Auto-generate mind map from notes",
         "detail": "实现思路：分析笔记结构 → 提取层级关系 → 生成思维导图。\n适用场景：知识整理、复习总结。\n技术栈：Python + NLP + 思维导图库",
         "detail_en": "Approach: Analyze note structure → Extract hierarchy → Generate mind map.\nUse cases: Knowledge organization, review summary.\nTech: Python + NLP + Mind map library"},
    ],
    "健康类": [
        {"id": "health_001", "name": "喝水提醒助手", "name_en": "Water Intake Reminder", "desc": "定时提醒喝水，记录每日饮水量", "desc_en": "Timed water reminders, track daily intake",
         "detail": "实现思路：设置饮水目标 → 定时提醒 → 记录饮水量 → 生成报告。\n适用场景：不爱喝水、健康管理。\n技术栈：Python + 定时任务 + 数据可视化",
         "detail_en": "Approach: Set intake goal → Timed reminders → Log intake → Generate report.\nUse cases: Don't like water, health management.\nTech: Python + Scheduled tasks + Data visualization"},
        {"id": "health_002", "name": "久坐提醒", "name_en": "Sedentary Alert", "desc": "久坐后提醒起身活动", "desc_en": "Remind to stand up after sitting too long",
         "detail": "实现思路：监测电脑使用时间 → 超过阈值提醒 → 推荐简单运动。\n适用场景：办公室工作、程序员。\n技术栈：Python + 系统监测 + 提醒",
         "detail_en": "Approach: Monitor computer usage → Alert when over threshold → Recommend simple exercises.\nUse cases: Office work, programmers.\nTech: Python + System monitoring + Reminders"},
        {"id": "health_003", "name": "睡眠质量分析", "name_en": "Sleep Quality Analyzer", "desc": "分析睡眠数据，给出改善建议", "desc_en": "Analyze sleep data, provide improvement tips",
         "detail": "实现思路：导入睡眠数据 → 分析睡眠周期 → 生成改善建议。\n适用场景：睡眠质量差、作息调整。\n技术栈：Python + 数据分析 + LLM",
         "detail_en": "Approach: Import sleep data → Analyze sleep cycles → Generate improvement tips.\nUse cases: Poor sleep quality, schedule adjustment.\nTech: Python + Data analysis + LLM"},
        {"id": "health_004", "name": "运动计划生成", "name_en": "Workout Plan Generator", "desc": "根据目标生成个性化运动计划", "desc_en": "Generate personalized workout plan based on goals",
         "detail": "实现思路：输入目标/时间/设备 → 匹配运动库 → 生成周计划。\n适用场景：健身新手、减脂增肌。\n技术栈：Python + 运动数据库 + 计划算法",
         "detail_en": "Approach: Input goal/time/equipment → Match exercise library → Generate weekly plan.\nUse cases: Fitness beginners, fat loss/muscle gain.\nTech: Python + Exercise database + Planning algorithm"},
        {"id": "health_005", "name": "卡路里计算器", "name_en": "Calorie Calculator", "desc": "拍照识别食物热量，记录每日摄入", "desc_en": "Photo-recognize food calories, track daily intake",
         "detail": "实现思路：拍照识别食物 → 查询热量数据库 → 记录每日摄入。\n适用场景：减肥、饮食控制。\n技术栈：Python + 图像识别 + 热量数据库",
         "detail_en": "Approach: Photo recognize food → Query calorie database → Log daily intake.\nUse cases: Weight loss, diet control.\nTech: Python + Image recognition + Calorie database"},
        {"id": "health_006", "name": "用药提醒", "name_en": "Medication Reminder", "desc": "定时提醒服药，记录用药历史", "desc_en": "Timed medication reminders, track history",
         "detail": "实现思路：录入药物信息 → 设置服药时间 → 提醒并记录。\n适用场景：长期服药、老人关怀。\n技术栈：Python + 定时任务 + 数据库",
         "detail_en": "Approach: Log medication info → Set reminder times → Remind and record.\nUse cases: Long-term medication, elderly care.\nTech: Python + Scheduled tasks + Database"},
        {"id": "health_007", "name": "步数目标追踪", "name_en": "Step Goal Tracker", "desc": "追踪每日步数，完成目标奖励", "desc_en": "Track daily steps, reward on goal completion",
         "detail": "实现思路：读取手机步数 → 对比目标 → 达成奖励。\n适用场景：运动激励、健康管理。\n技术栈：Python + 健康API + 游戏化",
         "detail_en": "Approach: Read phone step count → Compare to goal → Reward on achievement.\nUse cases: Exercise motivation, health management.\nTech: Python + Health API + Gamification"},
        {"id": "health_008", "name": "心情日记", "name_en": "Mood Diary", "desc": "记录每日心情，分析情绪趋势", "desc_en": "Log daily mood, analyze emotional trends",
         "detail": "实现思路：记录心情评分 → 添加标签 → 生成趋势图表。\n适用场景：情绪管理、心理咨询辅助。\n技术栈：Python + 数据可视化",
         "detail_en": "Approach: Log mood rating → Add tags → Generate trend charts.\nUse cases: Emotion management, counseling support.\nTech: Python + Data visualization"},
        {"id": "health_009", "name": "体检报告解读", "name_en": "Health Checkup Interpreter", "desc": "AI解读体检报告，给出健康建议", "desc_en": "AI interprets checkup report, gives health advice",
         "detail": "实现思路：OCR识别体检报告 → 分析异常指标 → 生成健康建议。\n适用场景：看不懂体检报告、健康管理。\n技术栈：Python + OCR + LLM",
         "detail_en": "Approach: OCR recognize report → Analyze abnormal indicators → Generate health advice.\nUse cases: Can't understand reports, health management.\nTech: Python + OCR + LLM"},
        {"id": "health_010", "name": "眼保健操提醒", "name_en": "Eye Exercise Reminder", "desc": "定时提醒做眼保健操，保护视力", "desc_en": "Timed eye exercise reminders, protect vision",
         "detail": "实现思路：监测屏幕时间 → 定时提醒 → 播放眼保健操音频。\n适用场景：长时间用眼、近视防控。\n技术栈：Python + 系统监测 + 音频播放",
         "detail_en": "Approach: Monitor screen time → Timed reminder → Play eye exercise audio.\nUse cases: Prolonged screen use, myopia prevention.\nTech: Python + System monitoring + Audio playback"},
    ]
}

# File paths - Auto-detect workspace for portability
def get_workspace_dir():
    """Get workspace directory, supporting multiple environments"""
    # Priority: Environment variable > Default locations
    if os.environ.get("OPENCLAW_WORKSPACE"):
        return os.environ.get("OPENCLAW_WORKSPACE")
    if os.environ.get("WORKSPACE"):
        return os.environ.get("WORKSPACE")
    # Check common locations
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".openclaw", "workspace"),
        "/root/.openclaw/workspace",
        os.path.join(home, "workspace"),
        os.getcwd(),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # Fallback: create in home directory
    fallback = os.path.join(home, ".openclaw", "workspace")
    os.makedirs(fallback, exist_ok=True)
    return fallback

REPORT_DIR = os.path.join(get_workspace_dir(), "reports", "ideas")
MEMORY_FILE = os.path.join(REPORT_DIR, "memory.json")
FAVORITES_FILE = os.path.join(REPORT_DIR, "favorites.json")
SUBMISSIONS_FILE = os.path.join(REPORT_DIR, "submissions.json")
LAST_IDEAS_FILE = os.path.join(REPORT_DIR, "last_ideas.json")
FEEDBACK_FILE = os.path.join(REPORT_DIR, "feedback.json")
COMMAND_LOG_FILE = os.path.join(REPORT_DIR, "command_log.json")


def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return default



# Deep analysis cache (7 days validity)
def load_deep_cache():
    """Load deep analysis cache"""
    cache_file = os.path.join(get_workspace_dir(), "reports", "ideas", "deep_cache.json")
    return load_json(cache_file, {"cache": {}, "created": {}})

def save_deep_cache(cache):
    """Save deep analysis cache"""
    cache_file = os.path.join(get_workspace_dir(), "reports", "ideas", "deep_cache.json")
    save_json(cache_file, cache)

def get_cached_deep(idea_id):
    """Get cached deep analysis if valid (within 7 days)"""
    cache = load_deep_cache()
    if idea_id in cache["cache"]:
        created_time = cache["created"].get(idea_id, 0)
        # 7 days = 7 * 24 * 60 * 60 = 604800 seconds
        if datetime.now().timestamp() - created_time < 604800:
            return cache["cache"][idea_id]
    return None

def set_cached_deep(idea_id, deep_content):
    """Cache deep analysis with timestamp"""
    cache = load_deep_cache()
    cache["cache"][idea_id] = deep_content
    cache["created"][idea_id] = datetime.now().timestamp()
    save_deep_cache(cache)

def save_json(filepath, data):
    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_memory():
    return load_json(MEMORY_FILE, {"seen_ids": []})


def save_memory(memory):
    save_json(MEMORY_FILE, memory)


def load_favorites():
    return load_json(FAVORITES_FILE, {"favorites": []})


def save_favorites(favorites):
    save_json(FAVORITES_FILE, favorites)


def load_submissions():
    return load_json(SUBMISSIONS_FILE, {"submissions": []})


def save_submissions(submissions):
    save_json(SUBMISSIONS_FILE, submissions)


def load_feedback():
    return load_json(FEEDBACK_FILE, {"feedbacks": []})


def save_feedback(feedback):
    save_json(FEEDBACK_FILE, feedback)


def load_last_ideas():
    return load_json(LAST_IDEAS_FILE, {"ideas": []})


def save_last_ideas(ideas):
    save_json(LAST_IDEAS_FILE, {"ideas": ideas})


def load_command_log():
    return load_json(COMMAND_LOG_FILE, {"logs": []})


def save_command_log(log):
    save_json(COMMAND_LOG_FILE, log)


def detect_language(text):
    """Detect user language from input text"""
    text_lower = text.lower()
    
    # Japanese (hiragana/katakana) - check first
    if re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
        return "ja"
    
    # Korean (hangul)
    if re.search(r'[\uac00-\ud7af]', text):
        return "ko"
    
    # Chinese characters
    if re.search(r'[\u4e00-\u9fff]', text):
        # Check for Japanese-only words
        japanese_words = ['アイデア', 'ください', '面白', 'もっと', 'いい']
        if any(w in text for w in japanese_words):
            return "ja"
        return "zh"
    
    # English keywords
    english_keywords = ['give me', 'ideas', 'interesting', 'help', 'more', 'again', 'good', 'bad', 'favorite', 'submit', 'rate', 'score', 'some']
    if any(kw in text_lower for kw in english_keywords):
        return "en"
    
    # Spanish keywords
    spanish_keywords = ['dame', 'quiero', 'ayuda', 'bueno', 'malo', 'favorito', 'más', 'interesantes']
    if any(kw in text_lower for kw in spanish_keywords):
        return "es"
    
    # French keywords
    french_keywords = ['donne', 'je veux', 'aide', 'bon', 'mauvais', 'favori', 'plus', 'intéressantes']
    if any(kw in text_lower for kw in french_keywords):
        return "fr"
    
    # Default to English
    return "en"


def get_text(lang, key, **kwargs):
    """Get localized text"""
    if lang not in LANGUAGES:
        lang = "en"
    text = LANGUAGES[lang].get(key, LANGUAGES["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def get_idea_text(idea, lang, field):
    """Get idea text in appropriate language"""
    if lang == "zh":
        return idea.get(field, "")
    else:
        return idea.get(f"{field}_en", idea.get(field, ""))


# 难度映射
DIFFICULTY_MAP = {
    "工具类": "简单",
    "游戏类": "中等",
    "应用类": "中等",
    "职场类": "中等",
    "艺术类": "中等",
    "AI类": "困难",
    "生活类": "简单",
    "社交类": "简单",
    "学习类": "简单",
    "健康类": "简单",
}

# 难度翻译
DIFFICULTY_TEXT = {
    "zh": {"简单": "🟢 简单", "中等": "🟡 中等", "困难": "🔴 困难"},
    "en": {"简单": "🟢 Easy", "中等": "🟡 Medium", "困难": "🔴 Hard"},
    "ja": {"简单": "🟢 簡単", "中等": "🟡 中級", "困难": "🔴 難しい"},
    "ko": {"简单": "🟢 쉬움", "中等": "🟡 보통", "困难": "🔴 어려움"},
    "es": {"简单": "🟢 Fácil", "中等": "🟡 Medio", "困难": "🔴 Difícil"},
    "fr": {"简单": "🟢 Facile", "中等": "🟡 Moyen", "困难": "🔴 Difficile"},
}

def get_idea_difficulty(category):
    """Get difficulty for a category"""
    return DIFFICULTY_MAP.get(category, "中等")

def get_idea_rating(idea_id):
    """Get average rating for an idea from feedback"""
    try:
        feedback = load_feedback()
        ratings = [f["score"] for f in feedback.get("feedbacks", []) if f["id"] == idea_id]
        if ratings:
            avg = sum(ratings) / len(ratings)
            return round(avg, 1)
    except:
        pass
    return None

def get_all_ideas():
    """Get all ideas - prefer reference folder if available"""
    all_ideas = []
    
    # First try reference folder (200 ideas)
    if REFERENCE_IDEAS:
        for category, ideas in REFERENCE_IDEAS.items():
            for idea in ideas:
                idea_copy = idea.copy()
                idea_copy["category"] = category
                idea_copy["difficulty"] = idea.get("difficulty", get_idea_difficulty(category))
                all_ideas.append(idea_copy)
    else:
        # Fallback to embedded IDEAS
        for category, ideas in IDEAS.items():
            for idea in ideas:
                idea_copy = idea.copy()
                idea_copy["category"] = category
                idea_copy["difficulty"] = get_idea_difficulty(category)
                all_ideas.append(idea_copy)
    
    # Merge user submissions
    submissions = load_submissions()
    for sub in submissions.get("submissions", []):
        all_ideas.append({
            "id": f"sub_{sub['id']}",
            "name": sub["name"],
            "name_en": sub.get("name_en", sub["name"]),
            "desc": sub["desc"],
            "desc_en": sub.get("desc_en", sub["desc"]),
            "detail": sub.get("detail", "用户投稿点子"),
            "detail_en": sub.get("detail_en", "User submitted idea"),
            "category": "用户投稿",
            "difficulty": "中等",
            "is_submission": True
        })
    return all_ideas


def generate_ideas(count=5, seen_ids=None, category=None, user_input=None, use_llm_fallback=True, cross_counter=0):
    """Generate ideas, optionally filtered by category
    If user_input contains trending keywords, try web search first
    Fallback to local reference data if web search fails
    Supports personalized ideas based on user profile (v0.4.2)
    
    When use_llm_fallback=True and all local ideas are exhausted,
    returns a special response to trigger LLM generation in current conversation.
    """
    if seen_ids is None:
        seen_ids = []

    # Check if we should try web search for trending ideas
    if user_input and should_search_web(user_input):
        web_ideas = search_trending_ideas(user_input, max_results=count)
        if web_ideas and len(web_ideas) >= count:
            return web_ideas
        # Web search failed or returned few results, fall through to local

    # Get user context for personalized ideas
    personalized_ideas = []
    is_personalized_request = False
    
    # 检测是否是通用随机请求（没有指定分类）
    user_input_lower = user_input.lower() if user_input else ""
    general_keywords = ["有趣", "点子", "idea", "随机", "random", "今日", "今天"]
    has_category = any(cat in user_input_lower for cat in ["工具", "游戏", "应用", "职场", "艺术", "ai", "生活", "社交", "学习", "健康", "金融", "旅行", "亲子", "宠物", "绿色"])
    
    if user_input and any(kw in user_input_lower for kw in general_keywords) and not has_category:
        # 用户没有指定分类，尝试生成个性化点子
        try:
            user_profile, recent_memory = get_user_context()
            if user_profile or recent_memory:
                personalized_ideas = generate_personalized_ideas(user_profile, recent_memory)
                if personalized_ideas:
                    is_personalized_request = True
        except:
            pass

    # Use local reference data
    all_ideas = get_all_ideas()

    # Category filter
    if category:
        all_ideas = [i for i in all_ideas if i.get("category") == category]

    # Exclude seen
    available = [i for i in all_ideas if i["id"] not in seen_ids]
    
    # 检测用户语言（提前）
    user_lang = detect_lang(user_input) if user_input else 'zh'
    
    # 获取用户兴趣（提前）
    user_interests = []
    try:
        user_profile, recent_memory = get_user_context()
        if user_profile:
            user_interests = extract_user_interests(user_profile, recent_memory)
    except:
        pass
    
    # 检查是否需要强制生成非投资相关点子（每3次至少1次非投资）
    force_non_finance = False
    counter = cross_counter
    if counter >= 3:
        force_non_finance = True
        counter = 0
    
    # 如果所有常规点子都见过了，用LLM补充前4个，第5个跨领域仍用单独prompt
    if use_llm_fallback and len(available) < 4 and len(all_ideas) > 4:
        # 需要LLM补充常规点子
        llm_prompt = build_llm_fallback_prompt(category, user_input)
        # 同时也生成跨领域prompt
        cross_prompt = build_cross_domain_prompt(user_lang, user_interests, force_non_finance)
        # 返回None表示需要LLM补充，但带上两个prompt
        return None, f"{llm_prompt}\n\n---\n\n{cross_prompt}"
    
    # 删除之前的逻辑：不再把已见过点子重新放回来
    # if len(available) < count:
    #     available = all_ideas

    # 每次生成5个点子：4个常规 + 1个跨领域（由LLM实时生成）
    
    # 构建跨领域点子 prompt（供外部LLM使用）
    cross_prompt = build_cross_domain_prompt(user_lang, user_interests, force_non_finance)
    
    # 选择4个常规点子
    available_regular = [i for i in available if not i.get("id", "").startswith("cross_") and not i.get("id", "").startswith("personalized_")]
    
    # 如果剩余点子不足4个，触发LLM补充（而不是重复已见过的）
    if len(available_regular) < 4 and len(all_ideas) > 4:
        # 返回None和LLM生成提示，让外部LLM补充点子
        return None, build_llm_fallback_prompt(category, user_input)
    
    selected = random.sample(available_regular, min(4, len(available_regular)))
    
    # 如果有个性化点子，随机混入
    if is_personalized_request and personalized_ideas and len(selected) > 0:
        replace_idx = random.randint(0, len(selected)-1)
        if replace_idx < len(personalized_ideas):
            p = personalized_ideas[replace_idx]
            # 生成唯一ID（使用时间戳+随机数，避免重复）
            unique_id = f"personalized_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100,999)}"
            selected[replace_idx] = {
                "id": unique_id,
                "name": p.get("name", p.get("name_en", "")),
                "name_en": p.get("name_en", p.get("name", "")),
                "desc": p.get("desc", p.get("desc_en", "")),
                "desc_en": p.get("desc_en", p.get("desc", "")),
                "category": p.get("category", "个性化"),
                "category_en": p.get("category_en", p.get("category", "")),
                "detail": f"✨个性化推荐：{p.get('desc', '')}",
                "detail_en": f"✨ Personalized: {p.get('desc_en', '')}",
                "difficulty": p.get("difficulty", "中等"),
                "is_personalized": True
            }
    
    # 返回4个常规点子 + 跨领域prompt（供外部LLM生成第5个）
    return selected, cross_prompt


def build_llm_fallback_prompt(category=None, user_input=None):
    """Build a prompt for the current conversation model to generate new ideas
    
    This is called when all local ideas have been seen, so we need to
    use the current conversation's LLM to generate fresh ideas.
    """
    
    # Get category info
    categories_zh = {
        "工具类": "实用工具类点子，帮助提高效率的小工具或脚本",
        "游戏类": "有趣的互动游戏或娱乐应用",
        "应用类": "移动端或桌面应用程序创意",
        "职场类": "工作场景相关的效率工具或办公辅助",
        "艺术类": "创意艺术、内容创作相关工具",
        "AI类": "人工智能相关的应用或工具",
        "生活类": "日常生活便利化相关点子",
        "社交类": "社交媒体或沟通相关应用",
        "学习类": "教育、学习、知识管理相关",
        "健康类": "健康、运动、医疗相关",
        "金融类": "投资、理财、财务管理相关",
        "旅行类": "旅行、出行、旅游相关",
        "亲子类": "亲子、儿童、家庭相关",
        "宠物类": "宠物、养宠相关",
        "绿色类": "环保、可持续发展、低碳生活相关",
    }
    
    # Build the prompt
    category_hint = ""
    if category and category in categories_zh:
        category_hint = f"\n- 指定分类：{category}（{categories_zh[category]}）"
    
    # Determine user preferences if possible
    user_prefs = ""
    try:
        user_profile, recent_memory = get_user_context()
        if user_profile:
            interests = []
            if user_profile.get("interests"):
                interests.extend(user_profile["interests"])
            if user_profile.get("skills"):
                interests.extend(user_profile["skills"])
            if interests:
                user_prefs = f"\n- 用户兴趣：{', '.join(interests[:5])}"
    except:
        pass
    
    prompt = f"""⚡ 点子生成任务

你需要生成5个独特的、有创意的点子。{category_hint}{user_prefs}

要求：
1. 每个点子必须包含：名称（中文）、一句话描述、难度级别（简单/中等/困难）
2. 点子要有趣、可执行，不是老生常谈
3. 如果指定了分类，确保点子符合该分类
4. 优先生成与用户兴趣相关的点子

请直接输出5个点子，格式如下：
1. [点子名称] - [一句话描述] [难度]
2. [点子名称] - [一句话描述] [难度]
3. [点子名称] - [一句话描述] [难度]
4. [点子名称] - [一句话描述] [难度]
5. [点子名称] - [一句话描述] [难度]"""
    
    return prompt


def build_cross_domain_prompt(lang='zh', user_interests=None, force_non_finance=False):
    """Build a prompt for LLM to generate cross-domain ideas in the user's language
    
    Args:
        lang: 用户语言
        user_interests: 用户兴趣列表
        force_non_finance: 是否强制生成非投资相关点子（每3次至少1次）
    """
    
    # 跨领域点子示例池（随机选择）
    cross_examples = {
        'zh': [
            '持仓交响曲 - 将股票波动率转化为音乐，MIDI实时生成 - 中等',
            '代码写歌词 - 用代码逻辑写歌：if 思念 > 阈值 → chorus++ - 简单',
            '时间胶囊日报 - 每天生成未来报纸，预测明天大事 - 中等',
            '梦境投资报告 - 记录梦境，荣格原型解读+投资决策分析 - 困难',
            '推歌算卦 - 随机播放三首歌，根据歌名算今日运势 - 简单'
        ],
        'en': [
            'Portfolio Symphony - Convert stock volatility into music, real-time MIDI - Medium',
            'Code Lyrics - Write lyrics using code logic: if longing > threshold then chorus++ - Easy',
            'Time Capsule Daily - Generate daily future newspaper predicting tomorrow - Medium',
            'Dream Investment Report - Record dreams, Jung archetype + investment analysis - Hard',
            'Song Fortune - Random 3 songs, read fortune from song titles - Easy'
        ]
    }
    
    # 语言对应的描述（根据force_non_finance调整规则）
    if force_non_finance:
        # 强制生成非投资相关
        lang_descs = {
            'zh': {
                'title': '🎯 跨领域点子生成任务（重要！）',
                'req': '生成1个独特的跨领域有趣点子（禁止投资相关！）',
                'interests_label': '用户兴趣',
                'rule1': '必须结合两个不同领域，且【禁止】包含：投资、理财、股票、基金、金融、财富、赚钱等任何相关内容',
                'rule2': '点子要有创意、可执行、略带荒诞但能落地',
                'rule3': '建议方向：生活+游戏、职场+玄学、健康+音乐、租房+整理、做饭+游戏等',
                'rule4': '语言必须与用户一致（中文）',
                'format': '直接输出1个点子，格式：名称 - 一句话描述 - 难度（简单/中等/困难）',
            },
            'en': {
                'title': '🎯 Cross-Domain Idea Generation Task (IMPORTANT!)',
                'req': 'Generate 1 unique cross-domain interesting idea (NO finance/investment allowed!)',
                'interests_label': 'User interests',
                'rule1': 'Must combine two different fields, and MUST NOT include: investment, stocks, funds, finance, wealth, money-making',
                'rule2': 'Idea should be creative, achievable, slightly absurd but practical',
                'rule3': 'Suggested: lifestyle+gaming, work+fortune-telling, health+music, cooking+gaming',
                'rule4': 'Language must match user (English)',
                'format': 'Output 1 idea in format: Name - One-line description - Difficulty (Easy/Medium/Hard)',
            }
        }
    else:
        lang_descs = {
            'zh': {
                'title': '🎯 跨领域点子生成任务',
                'req': '生成1个独特的跨领域有趣点子',
                'interests_label': '用户兴趣',
                'rule1': '必须结合两个【不相关】的领域，创造出意想不到的有趣效果！例如：生活+游戏、职场+玄学、健康+音乐、租房+整理、做饭+游戏、社交+心理、健身+游戏',
                'rule2': '点子要有创意、可执行、略带荒诞但能落地',
                'rule3': '禁止包含任何投资、理财、股票、基金、金融、财富、赚钱相关的内容',
                'rule4': '语言必须与用户一致（中文）',
                'format': '直接输出1个点子，格式：名称 - 一句话描述 - 难度（简单/中等/困难）',
                'examples': '租房俄罗斯方块、刷牙舞步计数器、泡面计时器、外卖选择轮盘、键盘文学家、错频聊天、电梯俯卧撑、深夜食堂雷达、袜子配对AI、起床气闹钟'
            },
            'en': {
                'title': '🎯 Cross-Domain Idea Generation Task',
                'req': 'Generate 1 unique cross-domain interesting idea',
                'interests_label': 'User interests',
                'rule1': 'Must combine TWO UNRELATED fields to create unexpected fun! Examples: lifestyle+gaming, work+fortune-telling, health+music, cooking+gaming, social+psychology',
                'rule2': 'Idea should be creative, achievable, slightly absurd but practical',
                'rule3': 'MUST NOT include any investment, stocks, funds, finance, wealth, money-making',
                'rule4': 'Language must match user (English)',
                'format': 'Output 1 idea in format: Name - One-line description - Difficulty (Easy/Medium/Hard)',
                'examples': 'Rental Tetris, Toothbrush Dancer, Ramen Timer, Food Roulette, Keyboard Novelist, Delayed Chat, Elevator Workout, Late Night Food Radar, Sock Matcher, Groggy Alarm'
            },
            'ja': {
                'title': '🎯 分野横断的なアイデア生成タスク',
                'req': '1つの独特の分野横断的な面白いアイデアを生成',
                'interests_label': 'ユーザーの興味',
                'rule1': '2つの【无关】分野を組み合わせる！例：生活+ゲーム、仕事+风水、健康+音楽、料理+ゲーム',
                'rule2': 'アイデアは創造的で実行可能、少し奇妙だが実践可能',
                'rule3': '投資、株式、金融相关内容は禁止',
                'rule4': '言語はユーザーと一致（日本語）',
                'format': '1つのアイデアを入力：名前 - 1行の説明 - 難易度（簡単/普通/難しい）',
                'examples': '賃貸テト里斯、刷牙ダンス、ラーメンタイマー'
            },
            'ko': {
                'title': '🎯 분야 통합 아이디어 생성 작업',
                'req': '1개의 독특한 분야 통합 흥미로운 아이디어 생성',
                'interests_label': '사용자 관심사',
                'rule1': '2개의 【관련 없는】 분야를 결합！예: 생활+게임, 건강+음악, 요리+게임',
                'rule2': '아이디어는 창의적이고 실행 가능하며 약간은 터무니없지만 실현 가능',
                'rule3': '투자, 주식, 금융 관련 내용은 금지',
                'rule4': '언어는 사용자와 일치 (한국어)',
                'format': '1개 아이디어 출력: 이름 - 한 줄 설명 - 난이도 (쉬움/보통/어려움)',
                'examples': '임대 테트리스, 양치 댄서, 라멘 타이머'
            },
            'es': {
                'title': '🎯 Tarea de Generación de Ideas Transversales',
                'req': 'Genera 1 idea única e interesante que combine dos campos diferentes',
                'interests_label': 'Intereses del usuario',
                'rule1': '¡Debe COMBINAR dos campos NO relacionados! Ej: vida+juguet, trabajo+astrología, salud+música, cocina+game',
                'rule2': 'La idea debe ser creativa, realizable, un poco absurda pero práctica',
                'rule3': 'PROHIBIDO incluir inversión, acciones, fondos, finanzas, dinero',
                'rule4': 'El idioma debe coincidir con el usuario (Español)',
                'format': 'Salida: 1 idea en formato: Nombre - Descripción - Dificultad (Fácil/Medio/Difícil)',
                'examples': 'Tetris de alquiler, Bailarín de cepillos, Temporizador de ramen'
            },
            'fr': {
                'title': '🎯 Tâche de Génération d\'Idées Transversales',
                'req': 'Générez 1 idée unique et interesante combinant deux domaines différents',
                'interests_label': 'Intérêts de l\'utilisateur',
                'rule1': 'Doit combiner deux domaines SANS rapport ! Ex: vie+jeu, travail+astrologie, santé+musique, cuisine+jeu',
                'rule2': 'L\'idée doit être créative, réalisable, un peu absurde mais pratique',
                'rule3': 'INTERDIT d\'inclure investissement, actions, fonds, finance, argent',
                'rule4': 'La langue doit correspondre à celle de l\'utilisateur (Français)',
                'format': 'Sortie: 1 idée au format: Nom - Description - Difficulté (Facile/Moyen/Difficile)',
                'examples': 'Tetris de location, Danseur de brosse, Minuteur de ramen'
            }
        }
    
    # 默认使用中文
    d = lang_descs.get(lang, lang_descs['zh'])
    
    # 兴趣标签翻译映射（根据目标语言翻译）
    interests_translation = {
        'zh': {
            '金融类': '金融类', '艺术类': '艺术类', '理财': '理财',
            '投资': '投资', '音乐': '音乐', 'AI': 'AI', '开发': '开发',
            '学习': '学习', '健康': '健康', '职场': '职场',
            'Finance': '金融类', 'Art': '艺术类', 'Wealth Management': '理财',
            'Investment': '投资', 'Music': '音乐', 'AI': 'AI'
        },
        'en': {
            '金融类': 'Finance', '艺术类': 'Art', '理财': 'Wealth Management',
            '投资': 'Investment', '音乐': 'Music', 'AI': 'AI', '开发': 'Development',
            '学习': 'Learning', '健康': 'Health', '职场': 'Career',
            'Finance': 'Finance', 'Art': 'Art', 'Wealth Management': 'Wealth Management',
            'Investment': 'Investment', 'Music': 'Music', 'AI': 'AI'
        },
        'ja': {
            '金融类': '金融', '芸術': '芸術', '音楽': '音楽',
        },
        'ko': {
            '금융': '금융', '예술': '예술', '투자': '투자',
        },
        'es': {
            '金融类': 'Finanzas', '艺术类': 'Arte', '理财': 'Gestión patrimonial',
            '投资': 'Inversión', '音乐': 'Música', 'AI': 'IA', '开发': 'Desarrollo',
            '学习': 'Aprendizaje', '健康': 'Salud', 'trabajo': 'Carrera',
            'Finance': 'Finanzas', 'Art': 'Arte', 'Wealth Management': 'Gestión patrimonial',
            'Investment': 'Inversión', 'Music': 'Música', 'AI': 'IA'
        },
        'fr': {
            '金融类': 'Finance', 'art': 'Art', '理财': 'Gestion de patrimoine',
            '投资': 'Investissement', '音乐': 'Musique', 'AI': 'IA', '开发': 'Développement',
            '学习': 'Apprentissage', '健康': 'Santé', '职场': 'Carrière',
            'Finance': 'Finance', 'Art': 'Art', 'Wealth Management': 'Gestion de patrimoine',
            'Investment': 'Investissement', 'Music': 'Musique', 'AI': 'IA'
        }
    }
    
    # 翻译用户兴趣到对应语言
    translated_interests = []
    trans_map = interests_translation.get(lang, interests_translation.get('en', {}))
    for interest in (user_interests or []):
        translated_interests.append(trans_map.get(interest, interest))
    
    # 获取用户兴趣（根据语言显示标签）
    interests_label = d.get('interests_label', 'User interests')
    interests_str = ""
    if translated_interests:
        interests_str = f"\n- {interests_label}：{', '.join(translated_interests[:3])}"
    
    prompt = f"""{d['title']}

{d['req']}。{interests_str}

要求：
{d['rule1']}
{d['rule2']}
{d['rule3']}
{d['rule4'] if 'rule4' in d else ''}

{d['format']}

参考示例（非投资相关）：{d.get('examples', '')}"""
    
    return prompt


def detect_lang(user_input):
    """Detect user language from input"""
    if not user_input:
        return 'zh'
    
    user_lower = user_input.lower()
    
    # 检测语言特征
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in user_input)
    has_japanese = any(c in 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン' for c in user_input)
    has_korean = any('\uac00' <= c <= '\ud7a3' for c in user_input)
    
    # 西班牙语特征词
    has_spanish = any(w in user_lower for w in [
        'hola', 'gracias', 'por favor', 'ideas', 'generar', 'dame', 
        'quiero', 'necesito', 'bueno', 'muy', 'bien', 'algo'
    ])
    
    # 法语特征词
    has_french = any(w in user_lower for w in [
        'bonjour', 'merci', 's\'il vous plaît', 'idée', 'générer', 'donne',
        'je veux', 'besoin', 'bien', 'quelque chose', 'encore'
    ])
    
    if has_chinese:
        return 'zh'
    elif has_japanese:
        return 'ja'
    elif has_korean:
        return 'ko'
    elif has_spanish:
        return 'es'
    elif has_french:
        return 'fr'
    elif any(w in user_lower for w in ['hello', 'give me', 'idea', 'generate', 'want', 'need', 'some']):
        return 'en'
    
    return 'zh'  # 默认中文


def save_to_report(ideas, report_type="daily"):
    """Save to report"""
    today = datetime.now().strftime("%Y-%m-%d")
    if report_type == "daily":
        report_file = os.path.join(REPORT_DIR, f"{today}-ideas.md")
        lines = [f"# {today} Ideas Generated", "", "## Ideas", ""]
        for idea in ideas:
            lines.append(f"- {idea['name']} ({idea.get('category', 'Unknown')})")
        content = "\n".join(lines)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)


def parse_command(user_input, lang="en"):
    """Parse user command"""
    user_input_lower = user_input.strip().lower()

    # Help commands (multi-language)
    help_keywords = ['help', '帮助', '?', 'hilfe', 'aide', 'ayuda', 'ヘルプ', '도움말', 'hjälp', 'aiuto']
    if any(kw in user_input_lower for kw in help_keywords):
        return {"type": "help"}

    # Good rating (multi-language)
    good_patterns = [
        r'(good|like|top|great|好|赞|好评|点赞|いいね|좋아|bueno|bon|gut|bra)\s*(\d+)',
        r'(\d+)\s*(good|like|top|great|好|赞|好评|点赞|いいね|좋아|bueno|bon|gut|bra)',
        r'👍\s*(\d+)',
        r'(\d+)\s*👍'
    ]
    for pattern in good_patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            groups = match.groups()
            for g in groups:
                if g.isdigit():
                    return {"type": "feedback", "rating": "good", "index": int(g)}

    # Bad rating (multi-language)
    bad_patterns = [
        r'(bad|dislike|sucks|差|烂|差评|踩|悪い|싫어|malo|mauvais|schlecht|dålig)\s*(\d+)',
        r'(\d+)\s*(bad|dislike|sucks|差|烂|差评|踩|悪い|싫어|malo|mauvais|schlecht|dålig)',
        r'👎\s*(\d+)',
        r'(\d+)\s*👎'
    ]
    for pattern in bad_patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            groups = match.groups()
            for g in groups:
                if g.isdigit():
                    return {"type": "feedback", "rating": "bad", "index": int(g)}

    # Score rating (multi-language)
    score_patterns = [
        r'(rate|score|评分|点数|점수|nota|note|bewertung|betyg)\s*(\d+)\s*(\d)',
        r'(\d+)\s*(rate|score|评分|点数|점수|nota|note|bewertung|betyg)\s*(\d)'
    ]
    for pattern in score_patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            groups = match.groups()
            for i, g in enumerate(groups):
                if g.isdigit():
                    if i + 1 < len(groups) and groups[i + 1].isdigit():
                        continue
                    idx = int(g)
                    for g2 in groups:
                        if g2.isdigit() and int(g2) != idx:
                            score = int(g2)
                            if 1 <= score <= 5:
                                return {"type": "feedback", "rating": "score", "index": idx, "score": score}

    # Category filter (multi-language)
    category_map = {
        "工具类": ["tool", "tools", "工具", "ツール", "도구", "herramienta", "outil", "verktyg"],
        "游戏类": ["game", "games", "游戏", "ゲーム", "게임", "juego", "jeu", "spel"],
        "应用类": ["app", "apps", "应用", "アプリ", "앱", "aplicación", "application", "applikation"],
        "职场类": ["work", "workplace", "职场", "仕事", "직장", "trabajo", "travail", "arbete"],
        "艺术类": ["art", "arts", "艺术", "アート", "예술", "arte", "konst"],
        "AI类": ["ai", "人工智能", "人工知能", "인공지능", "ia", "ki"],
        "生活类": ["life", "lifestyle", "生活", "ライフスタイル", "라이프스타일", "vida", "vie", "livsstil"],
        "社交类": ["social", "社交", "ソーシャル", "소셜", "sociala"],
        "学习类": ["learn", "learning", "study", "学习", "学習", "학습", "aprendizaje", "apprentissage", "lärande"],
        "健康类": ["health", "healthy", "健康", "健康", "건강", "salud", "santé", "hälsa"],
        "金融类": ["finance", "金融", "理财", "投资", "记账", "财务", "股票", "基金", "money", "invest"],
        "旅行类": ["travel", "旅行", "出行", "旅游", "机票", "酒店", "攻略", "trip", "vacation"],
        "亲子类": ["parenting", "亲子", "育儿", "儿童", "宝宝", "孩子", "baby", "kid", "family"],
        "宠物类": ["pets", "宠物", "猫", "狗", "饲养", "pet", "cat", "dog", "animal"],
        "绿色类": ["green", "绿色", "环保", "节能", "低碳", "可持续", "eco", "sustainable"],
    }
    for cat, keywords in category_map.items():
        for kw in keywords:
            if kw in user_input_lower:
                return {"type": "generate", "category": cat}

    # Favorite add (multi-language)
    fav_patterns = [
        r'(fav|favorite|收藏|お気に入り|즐겨찾기|favorito|favori|favorit)\s*(\d+)',
        r'(\d+)\s*(fav|favorite|收藏|お気に入り|즐겨찾기|favorito|favori|favorit)',
        r'❤️\s*(\d+)',
        r'(\d+)\s*❤️'
    ]
    for pattern in fav_patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            groups = match.groups()
            for g in groups:
                if g.isdigit():
                    return {"type": "fav_add", "index": int(g)}

    # View favorites (multi-language)
    fav_view_keywords = ['favorites', 'fav', '收藏', 'お気に入り', '즐겨찾기', 'favoritos', 'favoris', 'favoriter', '❤️']
    if any(kw in user_input_lower for kw in fav_view_keywords):
        return {"type": "favorites"}

    # User submission (multi-language)
    submit_keywords = ['i have an idea', 'submit', '我有一个点子', '投稿', 'アイデアがある', '아이디어가 있어', 'tengo una idea', "j'ai une idée", 'ich habe eine idee']
    if any(kw in user_input_lower for kw in submit_keywords):
        match = re.search(r"[：:](.+?)[-,](.+)", user_input)
        if match:
            return {"type": "submit", "name": match.group(1).strip(), "desc": match.group(2).strip()}

    # View detail (number only)
    if user_input.strip().isdigit():
        return {"type": "detail", "index": int(user_input.strip())}

    # Deep analysis (multi-language)
    deep_patterns = [
        r'(深度|deep|详细|detailed|分析|analysis)\s*(\d+)',
        r'(\d+)\s*(深度|deep|详细|detailed|分析|analysis)',
        r'(技术栈|tech|架构|architecture)\s*(\d+)',
        r'(\d+)\s*(技术栈|tech|架构|architecture)'
    ]
    for pattern in deep_patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            groups = match.groups()
            for g in groups:
                if g.isdigit():
                    return {"type": "deep_analyze", "index": int(g)}

    # More ideas (multi-language)
    more_keywords = ['more', 'again', '再来', '再生成', 'もっと', '더', 'más', 'plus', 'encore', 'nochmal', 'igen', 'mer']
    if any(kw in user_input_lower for kw in more_keywords):
        # 检查是否有待处理的方向选择
        user_input_stripped = user_input.strip().upper() if user_input else ""
        if user_input_stripped in ['A', 'B', 'C', 'D', 'E', '提高效率', '健康生活', '创意娱乐', '学习成长', '都可以', '效率', '健康', '创意', '学习', '随机']:
            # 用户选择了方向
            direction_map = {
                'A': '提高效率', '提高效率': '提高效率',
                'B': '健康生活', '健康生活': '健康生活',
                'C': '创意娱乐', '创意娱乐': '创意娱乐',
                'D': '学习成长', '学习成长': '学习成长',
                'E': '都可以', '都可以': '都可以', '随机': '都可以',
                '效率': '提高效率', '健康': '健康生活', '创意': '创意娱乐', '学习': '学习成长'
            }
            direction = direction_map.get(user_input_stripped, '都可以')
            return {"type": "generate", "direction": direction}
        else:
            # 没有方向，返回方向选择请求
            return {"type": "ask_direction"}
    
    # Vote command (5位名人Agent筛选)
    vote_keywords = ['vote', '投票', '筛选', '评判', '评价', '评分', '点评']
    if any(kw in user_input_lower for kw in vote_keywords):
        return {"type": "vote"}

    # Default generate
    return {"type": "generate"}


def handle_command(cmd, memory, last_ideas, lang="en", user_input=None):
    """Handle command"""
    result = {"lang": lang}

    if cmd["type"] == "help":
        result["message"] = "help"
        return result

    # 处理方向选择请求
    if cmd["type"] == "ask_direction":
        result["message"] = "ask_direction"
        return result

    if cmd["type"] == "generate":
        direction = cmd.get("direction")  # 获取用户选择的方向
        category = None
        
        # 根据方向映射到分类
        direction_to_category = {
            "提高效率": ["工具类", "职场类", "AI类"],
            "健康生活": ["健康类", "生活类"],
            "创意娱乐": ["游戏类", "艺术类", "生活类"],
            "学习成长": ["学习类", "AI类"],
        }
        
        if direction and direction != "都可以":
            # 用户选择了方向，随机选择一个对应分类
            categories = direction_to_category.get(direction, [])
            if categories:
                category = random.choice(categories)
        
        seen_ids = memory.get("seen_ids", [])
        cross_counter = memory.get("cross_finance_counter", 0)
        # Pass user_input to enable web search for trending keywords
        ideas, cross_prompt = generate_ideas(5, seen_ids, category, user_input=user_input, use_llm_fallback=True, cross_counter=cross_counter)
        
        # If no new ideas in library (all seen)
        if ideas is None and cross_prompt:
            result["message"] = "llm_fallback"
            result["llm_prompt"] = cross_prompt
            result["category"] = category
            return result

        # 4个常规点子 + 跨领域prompt（供外部LLM生成第5个）
        result["ideas"] = ideas
        result["cross_prompt"] = cross_prompt
        result["needs_llm_cross"] = True  # 标记需要LLM生成跨领域点子
        
        # 如果有方向，标记为 direction_generated
        if direction:
            result["direction"] = direction
            result["message"] = "direction_generated"
        else:
            result["message"] = "generate"
        
        # 保存已见的点子ID
        new_ids = [i["id"] for i in ideas]
        memory["seen_ids"].extend(new_ids)
        save_memory(memory)
        save_to_report(ideas)

    elif cmd["type"] == "detail":
        idx = cmd["index"]
        if 1 <= idx <= len(last_ideas):
            idea = last_ideas[idx - 1]
            result["message"] = "detail"
            result["idea"] = idea
        else:
            result["message"] = "error"
            result["text"] = get_text(lang, "error_no_idea")

    elif cmd["type"] == "deep_analyze":
        idx = cmd["index"]
        if 1 <= idx <= len(last_ideas):
            idea = last_ideas[idx - 1]
            deep_content = deep_analyze_idea(idea, lang)
            result["message"] = "deep_analyze"
            result["idea"] = idea
            result["deep_content"] = deep_content
        else:
            result["message"] = "error"
            result["text"] = get_text(lang, "error_no_idea")

    elif cmd["type"] == "favorites":
        favs = load_favorites()
        result["message"] = "favorites"
        result["favorites"] = favs.get("favorites", [])

    elif cmd["type"] == "fav_add":
        idx = cmd["index"]
        if 1 <= idx <= len(last_ideas):
            idea = last_ideas[idx - 1]
            favs = load_favorites()
            if not any(f["id"] == idea["id"] for f in favs["favorites"]):
                favs["favorites"].append({
                    "id": idea["id"],
                    "name": idea["name"],
                    "name_en": idea.get("name_en", idea["name"]),
                    "desc": idea["desc"],
                    "desc_en": idea.get("desc_en", idea["desc"]),
                    "category": idea.get("category", "Unknown"),
                    "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_favorites(favs)
                
                # 更新跨领域点子计数器
                # 检测是否包含投资/金融相关关键词
                finance_keywords = ['投资', '理财', '股票', '基金', '金融', '财富', '持仓', '涨停', '跌停', '盈利', '亏损', '市值', '估值', 
                                   'investment', 'stock', 'fund', 'finance', 'wealth', 'portfolio', 'trading']
                idea_text = (idea.get('name', '') + ' ' + idea.get('desc', '') + ' ' + idea.get('name_en', '') + ' ' + idea.get('desc_en', '')).lower()
                is_finance = any(kw.lower() in idea_text for kw in finance_keywords)
                
                current_counter = memory.get("cross_finance_counter", 0)
                if is_finance:
                    # 如果是投资相关，计数器+1
                    memory["cross_finance_counter"] = current_counter + 1
                else:
                    # 如果非投资相关，计数器重置
                    memory["cross_finance_counter"] = 0
                save_memory(memory)
                
                result["message"] = "fav_added"
                result["idea"] = idea
            else:
                result["message"] = "already_fav"
        else:
            result["message"] = "error"
            result["text"] = get_text(lang, "error_no_idea")

    elif cmd["type"] == "feedback":
        idx = cmd["index"]
        if 1 <= idx <= len(last_ideas):
            idea = last_ideas[idx - 1]
            feedback = load_feedback()

            rating = cmd.get("rating")
            if rating == "good":
                score = 5
                feedback_text = get_text(lang, "feedback_good", name=get_idea_text(idea, lang, "name"))
            elif rating == "bad":
                score = 1
                feedback_text = get_text(lang, "feedback_bad", name=get_idea_text(idea, lang, "name"))
            elif rating == "score":
                score = cmd.get("score", 3)
                feedback_text = get_text(lang, "feedback_score", name=get_idea_text(idea, lang, "name"), score=score)
            else:
                score = 3
                feedback_text = "Thanks for feedback!"

            feedback["feedbacks"].append({
                "id": idea["id"],
                "name": idea["name"],
                "score": score,
                "rating": feedback_text,
                "feedback_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_feedback(feedback)

            result["message"] = "feedback_done"
            result["idea"] = idea
            result["feedback_text"] = feedback_text
        else:
            result["message"] = "error"
            result["text"] = get_text(lang, "error_no_idea")

    elif cmd["type"] == "submit":
        submissions = load_submissions()
        new_id = len(submissions.get("submissions", [])) + 1
        new_sub = {
            "id": new_id,
            "name": cmd["name"],
            "desc": cmd["desc"],
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        submissions["submissions"].append(new_sub)
        save_submissions(submissions)
        result["message"] = "submitted"
        result["submission"] = new_sub

    elif cmd["type"] == "vote":
        # 运行5位名人Agent投票筛选
        if not VOTING_AVAILABLE:
            result["message"] = "error"
            result["text"] = "投票系统暂不可用"
        elif not last_ideas:
            result["message"] = "error"
            result["text"] = "没有可投票的点子，请先生成点子"
        else:
            voting = IdeaVotingSystem(threshold=7.0)
            vote_result = voting.vote(last_ideas, user_lang=lang)
            result["message"] = "vote_result"
            result["vote_data"] = vote_result
            # 将通过的点子更新到last_ideas
            if vote_result["passed"]:
                result["filtered_ideas"] = [r["idea"] for r in vote_result["passed"]]

    else:
        result["message"] = "unknown"

    return result


def format_output(result, last_ideas):
    """Format output"""
    msg = result["message"]
    lang = result.get("lang", "en")

    if msg == "help":
        if lang == "zh":
            return """📖 **Amazing Idea Generator 使用指南**

**🎮 基础指令**
• "今天有什么有趣的点子" / "给我点子" - 生成5个随机点子
• "再来一批" / "再生成" / "more" - 重新生成新点子

**🔥 趋势点子**（联网搜索）
• "最新点子" / "热门点子" / "trending ideas" - 获取实时热门创意
• 支持关键词：趋势、最新、热门、2024、2025、2026、trending、latest

**🎯 定向生成**
• "给我职场类点子" / "我要游戏类" / "tool ideas" 等

**📂 分类列表** (10大类，200+点子)
• 🛠️ 工具类 • 🎮 游戏类 • 📱 应用类 • 💼 职场类
• 🎨 艺术类 • 🤖 AI类 • 🏠 生活类 • 💬 社交类
• 📚 学习类 • 💪 健康类

**📖 查看详情**
• 回复数字 "1" "2" "3" 等 - 查看基础方案
• "深度分析1" - 联网获取技术栈、市场分析、学习资源
• 难度标识：🟢简单 🟡中等 🔴困难

**❤️ 收藏功能**
• "收藏1" / "fav 1" - 收藏第1个点子
• "收藏" / "favorites" - 查看收藏夹

**✍️ 投稿**
• "我有一个点子:名称 - 描述" / "I have an idea: name - desc"

**⭐ 质检评价**
• "好评1" / "good 1" - 给第1个点子好评
• "差评1" / "bad 1" - 给第1个点子差评
• "评分15" / "rate 1 5" - 给第1个点子5分(1-5分)

**🌐 支持语言**
• 中文 • English • 日本語 • 한국어 • Español • Français

**❓ 帮助**
• "help" / "帮助" / "?" - 显示本指南

---
💡 试试输入 "今天有什么有趣的点子" 开始吧！"""
        else:
            return """📖 **Amazing Idea Generator User Guide**

**🎮 Basic Commands**
• "give me ideas" / "interesting ideas" / "点子" - Generate 5 random ideas
• "more" / "again" / "再来" - Generate new ideas

**🔥 Trending Ideas** (Web Search)
• "trending ideas" / "latest ideas" / "最新点子" - Get real-time hot ideas
• Keywords: trending, latest, hot, new, 2024, 2025, 2026

**🎯 Category Filter**
• "tool ideas" / "game ideas" / "work ideas" / "职场类" etc.

**📂 Categories** (10 categories, 200+ ideas)
• 🛠️ Tools • 🎮 Games • 📱 Apps • 💼 Workplace
• 🎨 Art • 🤖 AI • 🏠 Lifestyle • 💬 Social
• 📚 Learning • 💪 Health

**📖 View Details**
• Reply number "1" "2" "3" etc. - View basic plan
• "deep 1" / "深度分析1" - Get tech stack, market analysis, resources via web search
• Difficulty: 🟢Easy 🟡Medium 🔴Hard

**❤️ Favorites**
• "fav 1" / "收藏1" - Save idea #1
• "favorites" / "收藏" - View saved ideas

**✍️ Submit**
• "I have an idea: name - description" / "我有一个点子: 名称 - 描述"

**⭐ Rate Ideas**
• "good 1" / "好评1" - Like idea #1
• "bad 1" / "差评1" - Dislike idea #1
• "rate 1 5" / "评分15" - Rate idea #1 as 5/5

**🌐 Supported Languages**
• 中文 • English • 日本語 • 한국어 • Español • Français

**❓ Help**
• "help" / "帮助" / "?" - Show this guide

---
💡 Try "give me some ideas" to start!"""

    if msg == "generate":
        ideas = result["ideas"]
        
        lines = [get_text(lang, "greeting") + "\n"]
        for i, idea in enumerate(ideas, 1):
            name = get_idea_text(idea, lang, "name")
            desc = get_idea_text(idea, lang, "desc")
            difficulty = idea.get("difficulty", "中等")
            diff_text = DIFFICULTY_TEXT.get(lang, DIFFICULTY_TEXT["en"]).get(difficulty, difficulty)
            rating = get_idea_rating(idea.get("id", ""))
            rating_text = f" ⭐{rating}" if rating else ""
            
            # 跨领域点子添加标记
            is_cross = "cross_" in idea.get("id", "")
            cross_tag = " 🎯跨领域" if is_cross else ""
            
            lines.append(f"{i}. {name} - {desc} {diff_text}{rating_text}{cross_tag}")
        
        # 如果需要外部LLM生成跨领域点子，添加标记
        if result.get("needs_llm_cross"):
            cross_prompt = result.get("cross_prompt", "")
            if cross_prompt:
                lines.append(f"\n🎯[LLM_GEN]{cross_prompt}")
        
        lines.append("\n" + get_text(lang, "hint"))
        return "\n".join(lines)

    elif msg == "llm_fallback":
        # 当本地点子库已用完时，使用当前对话的LLM生成新点子
        prompt = result.get("llm_prompt", "")
        category = result.get("category", "")
        
        if lang == "zh":
            return f"""🎲 嗯...本地点子库有点撑不住了！

来点新鲜的——我用当前对话的AI帮你生成5个独特的点子：

{prompt}"""
        else:
            return f"""🎲 Hmm... we've run through the local idea library!

Let's get fresh - I'll use the current conversation's AI to generate 5 unique ideas for you:

{prompt}"""

    elif msg == "detail":
        idea = result["idea"]
        name = get_idea_text(idea, lang, "name")
        desc = get_idea_text(idea, lang, "desc")
        detail = get_idea_text(idea, lang, "detail")
        category = idea.get("category", "Unknown")
        
        cat_trans = LANGUAGES.get(lang, LANGUAGES["en"])["categories"].get(category, category)
        
        lines = [
            get_text(lang, "detail_title", name=name),
            "",
            get_text(lang, "detail_intro", desc=desc),
            get_text(lang, "detail_category", category=cat_trans),
            "",
            get_text(lang, "detail_plan"),
            detail,
        ]
        
        # Add deep content if available
        deep = idea.get("deep", {})
        if deep:
            lines.append("")
            lines.append("─── 📊 深度分析 ───")
            
            if deep.get("tech_stack"):
                techs = ", ".join(deep["tech_stack"][:5])
                lines.append(f"🔧 技术栈: {techs}")
            
            if deep.get("architecture"):
                lines.append(f"📐 架构: {deep['architecture'][:200]}...")
            
            if deep.get("target_users"):
                users = ", ".join(deep["target_users"][:3])
                lines.append(f"👥 目标用户: {users}")
            
            if deep.get("dev_time"):
                lines.append(f"⏱️ 开发周期: {deep['dev_time']}")
            
            if deep.get("cost"):
                lines.append(f"💰 成本: {deep['cost'][:100]}")
            
            if deep.get("monetization"):
                lines.append(f"💵 变现: {deep['monetization'][:150]}")
            
            if deep.get("risks"):
                risks = ", ".join(deep["risks"][:3])
                lines.append(f"⚠️ 风险: {risks}")
            
            if deep.get("resources"):
                lines.append("📚 资源:")
                for res in deep["resources"][:3]:
                    lines.append(f"   • {res['title']}: {res['url']}")
        
        lines.append("")
        lines.append(get_text(lang, "hint_detail", n=list(last_ideas).index(idea)+1 if idea in last_ideas else 1))
        return "\n".join(lines)

    elif msg == "favorites":
        favs = result["favorites"]
        if not favs:
            return get_text(lang, "fav_empty")
        lines = [get_text(lang, "fav_title") + "\n"]
        for i, fav in enumerate(favs, 1):
            name = fav.get("name_en" if lang != "zh" else "name", fav["name"])
            desc = fav.get("desc_en" if lang != "zh" else "desc", fav["desc"])
            cat = fav.get("category", "")
            cat_trans = LANGUAGES.get(lang, LANGUAGES["en"])["categories"].get(cat, cat)
            lines.append(f"{i}. {name} - {desc} ({cat_trans})")
        return "\n".join(lines)

    elif msg == "fav_added":
        idea = result["idea"]
        name = get_idea_text(idea, lang, "name")
        desc = get_idea_text(idea, lang, "desc")
        return get_text(lang, "fav_added", name=name, desc=desc) + "\n" + get_text(lang, "hint")

    elif msg == "already_fav":
        return get_text(lang, "fav_exists")

    elif msg == "feedback_done":
        return result.get("feedback_text", "Thanks for feedback!")

    elif msg == "submitted":
        sub = result["submission"]
        return get_text(lang, "submit_success", name=sub["name"], desc=sub["desc"])

    elif msg == "error":
        return result.get("text", get_text(lang, "error_no_idea"))

    elif msg == "vote_result":
        vote_data = result.get("vote_data", {})
        if not vote_data:
            return "没有投票数据"
        
        # 格式化投票结果
        return format_vote_result(vote_data, user_lang=lang)

    elif msg == "deep_analyze":
        idea = result["idea"]
        deep_content = result["deep_content"]
        name = get_idea_text(idea, lang, "name")
        
        lines = [
            f"🔍 【{name}】深度分析",
            "",
            deep_content,
            "",
            "💡 说\"1\"查看基础详情，或\"再来一批\"继续探索"
        ]
        return "\n".join(lines)

    elif msg == "ask_direction":
        return get_text(lang, "direction_prompt")

    elif msg == "direction_generated":
        direction = result.get("direction", "")
        direction_text = {
            "提高效率": "提高效率类",
            "健康生活": "健康生活类",
            "创意娱乐": "创意娱乐类",
            "学习成长": "学习成长类",
            "都可以": "随机"
        }.get(direction, "")
        confirm_text = get_text(lang, "direction_confirm", direction=direction_text)
        # 返回点子生成结果
        ideas = result.get("ideas", [])
        cross_prompt = result.get("cross_prompt", "")
        
        lines = [confirm_text + "\n"]
        for i, idea in enumerate(ideas, 1):
            name = get_idea_text(idea, lang, "name")
            desc = get_idea_text(idea, lang, "desc")
            difficulty = idea.get("difficulty", "")
            diff_text = DIFFICULTY_TEXT.get(lang, DIFFICULTY_TEXT["en"]).get(difficulty, difficulty)
            lines.append(f"{i}. {name} - {desc} {diff_text}")
        
        if cross_prompt:
            lines.append("\n" + cross_prompt)
        
        lines.append("\n" + get_text(lang, "hint"))
        return "\n".join(lines)

    else:
        return get_text(lang, "error_unknown")


def log_command(user_input, cmd, result):
    """Log command execution"""
    log = load_command_log()
    log["logs"].append({
        "input": user_input[:100],
        "command_type": cmd.get("type", "unknown"),
        "result": result.get("message", "unknown"),
        "language": result.get("lang", "en"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    if len(log["logs"]) > 100:
        log["logs"] = log["logs"][-100:]
    save_command_log(log)


def main(user_input=""):
    last_data = load_last_ideas()
    last_generated_ideas = last_data.get("ideas", [])

    lang = detect_language(user_input) if user_input else "en"

    memory = load_memory()

    if not user_input:
        cmd = {"type": "generate"}
    else:
        cmd = parse_command(user_input, lang)

    result = handle_command(cmd, memory, last_generated_ideas, lang, user_input=user_input)

    log_command(user_input, cmd, result)

    if cmd["type"] == "generate" and result.get("ideas"):
        save_last_ideas(result["ideas"])

    return format_output(result, last_generated_ideas)



# ========== 用户画像读取模块 (v0.4.2新增) ==========

USER_PROFILE_FILE = os.path.expanduser("~/.openclaw/workspace/USER.md")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
SESSION_DIR = "/root/.openclaw/agents/main/sessions"

def get_workspace_path():
    for path in [os.environ.get("OPENCLAW_WORKSPACE"), os.environ.get("WORKSPACE"),
                 os.path.expanduser("~/.openclaw/workspace"), "/root/.openclaw/workspace", "."]:
        if path and os.path.exists(path):
            return path
    return "."

def load_user_profile():
    profile_path = os.path.join(get_workspace_path(), "USER.md")
    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""
    return ""

def load_recent_memory(days=3):
    memory_dir = os.path.join(get_workspace_path(), "memory")
    if not os.path.exists(memory_dir):
        return ""
    import datetime
    contents = []
    for i in range(days):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        filename = f"{date.strftime('%Y-%m-%d')}.md"
        filepath = os.path.join(memory_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    contents.append(f.read())
            except:
                pass
    return "\n".join(contents)

def extract_user_interests(user_profile, recent_memory):
    full_text = user_profile + "\n" + recent_memory
    interest_mapping = {
        "投资": ["金融类", "理财", "投资组合", "股票", "基金"],
        "量化": ["金融类", "量化", "投资模型"],
        "财富": ["金融类", "理财", "资产"],
        "音乐": ["艺术类", "音乐", "Suno", "专辑"],
        "插画": ["艺术类", "插画", "绘画", "设计"],
        "创作": ["艺术类", "创作", "内容生成"],
        "AI": ["AI类", "人工智能", "大模型"],
        "开发": ["工具类", "职场类", "开发", "代码"],
        "OpenClaw": ["工具类", "AI类", "自动化", "技能"],
        "学习": ["学习类", "知识", "教育"],
        "认知": ["学习类", "思维", "认知"],
        "健康": ["健康类", "运动", "健身"],
        "宠物": ["宠物类", "猫", "狗"],
        "亲子": ["亲子类", "育儿", "儿童"],
        "旅行": ["旅行类", "出行", "旅游"],
        "绿色": ["绿色类", "环保", "可持续"],
    }
    interests = {}
    for keyword, categories in interest_mapping.items():
        if keyword.lower() in full_text.lower():
            for cat in categories:
                interests[cat] = interests.get(cat, 0) + 1
    sorted_interests = sorted(interests.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_interests[:3]]

def generate_personalized_ideas(user_profile, recent_memory):
    interests = extract_user_interests(user_profile, recent_memory)
    if not interests:
        return []
    
    # 收集所有匹配的点子
    all_matched = []
    
    if "金融类" in interests or "理财" in interests:
        all_matched.append({"name": "量化投资回测系统", "desc": "回测历史数据，验证投资策略有效性", "category": "金融类", "difficulty": "中等"})
    if "艺术类" in interests or "音乐" in interests:
        all_matched.append({"name": "AI音乐词曲助手", "desc": "辅助生成歌词和旋律提示词", "category": "艺术类", "difficulty": "中等"})
    if "AI类" in interests or "OpenClaw" in interests:
        all_matched.append({"name": "自定义技能生成器", "desc": "根据描述自动生成OpenClaw技能", "category": "AI类", "difficulty": "困难"})
    if "工具类" in interests or "开发" in interests:
        all_matched.append({"name": "代码片段管理库", "desc": "收藏和管理常用代码片段", "category": "工具类", "difficulty": "简单"})
    if "绿色类" in interests:
        all_matched.append({"name": "碳足迹追踪面板", "desc": "可视化每日碳排放数据", "category": "绿色生活", "difficulty": "简单"})
    
    # 随机打乱，只取1-2个，避免总是推荐相同的
    import random
    random.shuffle(all_matched)
    return all_matched[:2]  # 最多返回2个，且随机顺序

_user_profile_cache = None
_recent_memory_cache = None

def get_user_context():
    global _user_profile_cache, _recent_memory_cache
    if _user_profile_cache is None:
        _user_profile_cache = load_user_profile()
    if _recent_memory_cache is None:
        _recent_memory_cache = load_recent_memory(days=3)
    return _user_profile_cache, _recent_memory_cache

    user_input = sys.argv[1] if len(sys.argv) > 1 else ""
    print(main(user_input))
# ========== 用户画像读取模块 (v0.4.2新增) ==========

USER_PROFILE_FILE = os.path.expanduser("~/.openclaw/workspace/USER.md")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
SESSION_DIR = "/root/.openclaw/agents/main/sessions"

def get_workspace_path():
    """获取工作区路径"""
    for path in [os.environ.get("OPENCLAW_WORKSPACE"), os.environ.get("WORKSPACE"),
                 os.path.expanduser("~/.openclaw/workspace"), "/root/.openclaw/workspace", "."]:
        if path and os.path.exists(path):
            return path
    return "."

def load_user_profile():
    """读取用户画像 USER.md"""
    profile_path = os.path.join(get_workspace_path(), "USER.md")
    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""
    return ""

def load_recent_memory(days=3):
    """读取近期memory文件"""
    memory_dir = os.path.join(get_workspace_path(), "memory")
    if not os.path.exists(memory_dir):
        return ""
    
    import datetime
    contents = []
    for i in range(days):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        filename = f"{date.strftime('%Y-%m-%d')}.md"
        filepath = os.path.join(memory_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    contents.append(f.read())
            except:
                pass
    return "\n".join(contents)

def extract_user_interests(user_profile, recent_memory):
    """从用户信息中提取兴趣关键词"""
    # 合并内容
    full_text = user_profile + "\n" + recent_memory
    
    # 定义兴趣关键词映射到分类
    interest_mapping = {
        # 投资理财
        "投资": ["金融类", "理财", "投资组合", "股票", "基金"],
        "量化": ["金融类", "量化", "投资模型"],
        "财富": ["金融类", "理财", "资产"],
        
        # 音乐/艺术
        "音乐": ["艺术类", "音乐", "Suno", "专辑"],
        "插画": ["艺术类", "插画", "绘画", "设计"],
        "创作": ["艺术类", "创作", "内容生成"],
        
        # AI/技术
        "AI": ["AI类", "人工智能", "大模型"],
        "开发": ["工具类", "职场类", "开发", "代码"],
        "OpenClaw": ["工具类", "AI类", "自动化", "技能"],
        
        # 学习
        "学习": ["学习类", "知识", "教育"],
        "认知": ["学习类", "思维", "认知"],
        
        # 生活
        "健康": ["健康类", "运动", "健身"],
        "宠物": ["宠物类", "猫", "狗"],
        "亲子": ["亲子类", "育儿", "儿童"],
        "旅行": ["旅行类", "出行", "旅游"],
        "绿色": ["绿色类", "环保", "可持续"],
    }
    
    # 统计兴趣权重
    interests = {}
    for keyword, categories in interest_mapping.items():
        if keyword.lower() in full_text.lower():
            for cat in categories:
                interests[cat] = interests.get(cat, 0) + 1
    
    # 按权重排序，返回用户最感兴趣的分类
    sorted_interests = sorted(interests.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_interests[:3]]

def generate_personalized_ideas(user_profile, recent_memory):
    """根据用户画像生成个性化点子"""
    interests = extract_user_interests(user_profile, recent_memory)
    
    # 如果没有识别到兴趣，返回空列表让系统使用随机
    if not interests:
        return []
    
    # 生成与用户兴趣相关的个性化点子描述
    personalized = []
    
    if "金融类" in interests or "理财" in interests:
        personalized.append({
            "name": "量化投资回测系统",
            "name_en": "Quantitative Investment Backtester",
            "desc": "回测历史数据，验证投资策略有效性",
            "desc_en": "Backtest historical data to validate investment strategies",
            "category": "金融类",
            "category_en": "Finance",
            "difficulty": "中等"
        })
    
    if "艺术类" in interests or "音乐" in interests:
        personalized.append({
            "name": "AI音乐词曲助手",
            "name_en": "AI Lyrics & Melody Assistant",
            "desc": "辅助生成歌词和旋律提示词",
            "desc_en": "Generate lyrics and melody prompts with AI",
            "category": "艺术类",
            "category_en": "Art",
            "difficulty": "中等"
        })
    
    if "AI类" in interests or "OpenClaw" in interests:
        personalized.append({
            "name": "自定义技能生成器",
            "name_en": "Custom Skill Generator",
            "desc": "根据描述自动生成OpenClaw技能",
            "desc_en": "Auto-generate OpenClaw skills from descriptions",
            "category": "AI类",
            "category_en": "AI",
            "difficulty": "困难"
        })
    
    if "工具类" in interests or "开发" in interests:
        personalized.append({
            "name": "代码片段管理库",
            "name_en": "Code Snippet Manager",
            "desc": "收藏和管理常用代码片段",
            "desc_en": "Save and manage frequently used code snippets",
            "category": "工具类",
            "category_en": "Tools",
            "difficulty": "简单"
        })
    
    if "绿色类" in interests:
        personalized.append({
            "name": "碳足迹追踪面板",
            "name_en": "Carbon Footprint Tracker",
            "desc": "可视化每日碳排放数据",
            "desc_en": "Visualize daily carbon emission data",
            "category": "绿色生活",
            "category_en": "Green Living",
            "difficulty": "简单"
        })
    
    return personalized[:3]  # 最多返回3个个性化点子

# 初始化用户画像（延迟加载）
_user_profile_cache = None
_recent_memory_cache = None

def get_user_context():
    """获取用户上下文（带缓存）"""
    global _user_profile_cache, _recent_memory_cache
    if _user_profile_cache is None:
        _user_profile_cache = load_user_profile()
    if _recent_memory_cache is None:
        _recent_memory_cache = load_recent_memory(days=3)
    return _user_profile_cache, _recent_memory_cache


if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else ""
    print(main(user_input))

