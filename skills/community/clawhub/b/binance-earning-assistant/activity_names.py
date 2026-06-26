#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动名称中文化映射 + 区域限制检测
"""

# 区域限制关键词（华语地区）
REGION_RESTRICTED_KEYWORDS = [
    "not available in your region",
    "香港居民不可参与",
    "香港用户不可参与",
    "中国大陆用户不可参与",
    "中国用户不可参与",
    "台湾用户不可参与",
    "澳门用户不可参与",
    "restricted regions",
    "excluded jurisdictions",
    "unavailable in certain regions",
    # 非华语地区
    "pakistan", "africa", "balkans", "nigeria", "uganda", "ghana", "kenya",
    "morocco", "cameroon", "turkmenistan", "ramadan", "jalsat", "suhoor",
    "巴基斯坦", "非洲", "巴尔干", "尼日利亚", "乌干达", "加纳", "肯尼亚",
    "摩洛哥", "喀麦隆", "土库曼", "斋月"
]

# 英文标题 -> 中文标题映射
ACTIVITY_NAMES = {
    # 理财产品
    "Enjoy Up to 8% APR with RLUSD Flexible Products": "RLUSD 灵活理财 8% 年化",
    "Binance Earn Yield Arena: Earn Up to 11.5% APR": "Yield Arena 理财 最高 11.5% 年化",
    "Binance Will Add Midnight (NIGHT) on Earn": "NIGHT 代币理财上线",
    "Binance Will Add Opinion (OPN) on Earn": "OPN 代币理财上线",
    "Enjoy Up to 10.5% APR with U Flexible Products": "U 灵活理财 10.5% 年化",
    "Subscribe to Binance Earn Products & Share 2,000 USDC": "理财申购瓜分 2000 USDC",
    "Introducing Midnight (NIGHT) on Binance Super Earn": "Midnight (NIGHT) 超级赚币",
    "Binance Earn: Share 10 Million SHELL Rewards": "SHELL 代币奖励（1000 万）",
    "Africa Exclusive: Create and Share Videos": "非洲专属：视频创作赢奖励",
    "Binance Earn: Enjoy Up to 8% APR with RLUSD": "RLUSD 灵活理财 8% 年化",
    "Binance Earn: Enjoy Up to 35% APR on SXT Flexible Products with 100,000 SXT Personal Limit": "SXT 灵活理财 35% 年化（10 万限额）",
    "Binance Earn: Enjoy Up to 10% APR with U Flexible Products – 20,000 U Limit Available": "U 灵活理财 10% 年化（2 万限额）",
    "Binance Earn: Share 10 Million SHELL Rewards and Enjoy Up to 1.5% APR with ETH Flexible Products": "SHELL 奖励 + ETH 理财 1.5% 年化",
    
    # 活动奖励
    "Share 10 Million SHELL Rewards": "SHELL 代币奖励（1000 万）",
    "Tria Trading Competition": "Tria 交易竞赛",
    "KITE Trading Tournament": "KITE 交易锦标赛",
    "Grab a Share of 2,000,000 NIGHT Rewards": "NIGHT 代币奖励（200 万）",
    "Trade Tokenized Securities on Binance Alpha": "币安 Alpha 代币化证券交易",
    "ETHGas Trading Competition": "ETHGas 交易竞赛",
    "Humanity Protocol Trading Competition": "Humanity Protocol 交易竞赛",
    "Introducing Midnight (NIGHT): Grab a Share of the 90,000,000 NIGHT Token Voucher Prize Pool": "Midnight 空投（9000 万代币）",
    "Balkans Futures Frenzy: Grab a Share of the 17,100 USDC Reward Pool": "巴尔干期货交易（1.7 万 USDC）",
    "Join the Binance Wallet On-Chain Perpetuals Milestone Challenge": "币安钱包链上永续合约挑战",
    "Word of the Day: Test Your Knowledge on": "每日一词：知识测试",
    "Word of the Day: Test Your Knowledge": "每日一词：知识测试",
    "Word of the Day: Test Your Knowledge on \"AI Trading\" to Unlock USDC Rewards": "每日一词：AI Trading 测试赢 USDC",
    "Word of the Day: Test Your Knowledge on \"OpenClaw\" to Unlock HOME Rewards": "每日一词：OpenClaw 测试赢 HOME",
    "Word of the Day: Test Your Knowledge on \"AI Agents\" to Unlock HOME Rewards": "每日一词：AI Agents 测试赢 HOME",
    "Word of the Day: Test Your Knowledge on \"#BinanceJunior\" to Unlock HOME Rewards": "每日一词：BinanceJunior 测试赢 HOME",
    "Velvet Trading Competition: Trade Velvet (VELVET) and Share $200K Worth of Rewards": "Velvet 交易竞赛（20 万美金）",
    "Pakistan Exclusive: Join the Binance x Islamabad United Referral Challenge": "巴基斯坦专属：推荐挑战赛",
    "Grab a Share of 1,968,000 SIGN Rewards on CreatorPad": "SIGN 创作者奖励（196.8 万）",
    "Introducing Katana (KAT): Grab a Share of the 25,000,000 KAT Token Voucher Prize Pool": "Katana 空投（2500 万 KAT）",
    "Hold USD1 in Binance Spot, Funding, Margin and Futures Accounts to Share 135 Million WLFI Tokens": "持 USD1 瓜分 1.35 亿 WLFI",
    "SAHARA Trading Tournament: Trade to Share Up to 4,000,000 SAHARA Token Vouchers": "SAHARA 交易锦标赛（400 万代币）",
    "Block Street Trading Competition: Trade Block Street (BSB) and Share $100K Worth of Rewards": "BSB 交易竞赛（10 万美金）",
    "Unitas Trading Competition: Trade Unitas (UP) and Share $200K Worth of Rewards": "Unitas 交易竞赛（20 万美金）",
    "CFG Trading Tournament: Trade to Share Up to 835,000 CFG Token Vouchers": "CFG 交易锦标赛（83.5 万代币）",
    "Grab a Share of 2,000,000 NIGHT Rewards on CreatorPad": "NIGHT 创作者奖励（200 万）",
    "Celebrate Eid al Fitr with Binance P2P: Enjoy Zero Fees & Share Cashback Rewards": "开斋节 P2P 零手续费 + 返现",
    "CIS User Exclusive: Celebrate Nowruz Together! Gifts are Ready—Up to 300 USDT in Surprise Boxes": "独联体专属：诺鲁孜节惊喜盒（300 USDT）",
    "Binance KOL Introduction Program: Introduce KOLs to Join Binance Affiliate Program and Earn Up to 8,000 USDC": "KOL 推荐计划（最高 8000 USDC）",
    "Join the Angels Square AMA & Win Rewards: Women in Crypto, Investing 101 & Earning with Binance": "Women in Crypto AMA 赢奖励",
    
    # 其他活动
    "Introducing Fabric Protocol (ROBO)": "Fabric Protocol (ROBO) 介绍",
    "Introducing Fabric Protocol (ROBO): Grab a Share of 8,600,000 ROBO Token Vouchers": "ROBO 空投（860 万代币）",
    "Introducing Opinion (OPN)": "Opinion (OPN) 代币介绍",
    "Introducing Katana (KAT): Grab a Share of the 25,000,000 KAT Token Voucher Prize Pool": "Katana 空投（2500 万 KAT）",
    "Introducing Midnight (NIGHT): Grab a Share of the 90,000,000 NIGHT Token Voucher Prize Pool": "Midnight 空投（9000 万 NIGHT）",
    "Introducing Midnight (NIGHT) on Binance Super Earn: Share Up to 120M NIGHT Quarterly, Under a Total Rewards Grant of 480M NIGHT": "Midnight 超级赚币（1.2 亿/季度）",
}

# 代币提取规则
TOKEN_PATTERNS = {
    "RLUSD": "RLUSD",
    "NIGHT": "NIGHT",
    "OPN": "OPN",
    "SHELL": "SHELL",
    "TRIA": "TRIA",
    "Tria": "TRIA",
    "KITE": "KITE",
    "ETHGas": "ETHGas",
    "GWEI": "GWEI",
    "ROBO": "ROBO",
    "USDC": "USDC",
    "U": "U",
    "ETH": "ETH",
    "BNB": "BNB",
    "FDUSD": "FDUSD",
    "VELVET": "VELVET",
    "H": "H",
    "CFG": "CFG",
    "Midnight": "NIGHT",
    # 新增代币
    "SIGN": "SIGN",
    "KAT": "KAT",
    "Katana": "KAT",
    "SXT": "SXT",
    "WLFI": "WLFI",
    "SAHARA": "SAHARA",
    "BSB": "BSB",
    "Block Street": "BSB",
    "Unitas": "UP",
    "USD1": "USD1",
    "SXT Flexible": "SXT",
}

def get_chinese_name(english_title):
    """获取中文名称（支持模糊匹配 + LLM fallback）"""
    import re
    
    # 先精确匹配
    if english_title in ACTIVITY_NAMES:
        return ACTIVITY_NAMES[english_title]
    
    # 去除末尾标点符号后再精确匹配（处理 ! ? 等差异）
    title_stripped = english_title.rstrip('!?.')
    if title_stripped in ACTIVITY_NAMES:
        return ACTIVITY_NAMES[title_stripped]
    
    # 标准化处理：统一大小写、去除多余空格和标点
    def normalize(text):
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)  # 多个空格变一个
        text = re.sub(r'[^\w\s]', '', text)  # 去除标点
        return text
    
    title_normalized = normalize(english_title)
    
    # 模糊匹配：标准化后匹配
    for en, zh in ACTIVITY_NAMES.items():
        en_normalized = normalize(en)
        if en_normalized == title_normalized:
            return zh
    
    # 关键词匹配（改进版：支持大小写、标点符号）
    title_lower = english_title.lower()
    
    # 提取关键信息：代币名 + 活动类型
    tokens = ["shell", "night", "opn", "robo", "tria", "kite", "velvet", "ethgas", 
              "humanity", "kat", "sign", "sxt", "wlfi", "sahara", "bsb", "cfg", 
              "unitas", "midnight", "fabric", "opinion", "block street", "u "]
    
    activity_types = {
        "earn": "理财", "reward": "奖励", "competition": "竞赛", 
        "tournament": "锦标赛", "airdrop": "空投", "trading": "交易",
        "grab a share": "瓜分", "introducing": "介绍", "flexible": "灵活",
        "super earn": "超级赚币", "yield arena": "Yield Arena"
    }
    
    best_match = None
    best_score = 0
    
    for en, zh in ACTIVITY_NAMES.items():
        en_lower = en.lower()
        score = 0
        
        # 代币匹配（权重高）
        for token in tokens:
            if token in en_lower and token in title_lower:
                score += 10
        
        # 活动类型匹配（权重中）
        for en_kw, zh_kw in activity_types.items():
            if en_kw in en_lower and en_kw in title_lower:
                score += 5
        
        # 数字匹配（奖池金额、APR 等）
        en_numbers = re.findall(r'[\d,]+(?:\s*(?:million|thousand|万|%))?', en_lower)
        title_numbers = re.findall(r'[\d,]+(?:\s*(?:million|thousand|万|%))?', title_lower)
        for num in en_numbers:
            if num in title_numbers:
                score += 3
        
        # 如果分数足够高，认为是匹配
        if score > best_score and score >= 10:
            best_score = score
            best_match = zh
    
    if best_match:
        return best_match
    
    # 没有匹配就返回原标题
    return english_title

def extract_token(title):
    """从标题提取代币名称"""
    title_upper = title.upper()
    
    # 特殊处理 1：ETHGas 的代币是 GWEI
    if "ETHGAS" in title_upper:
        return "GWEI"
    
    # 特殊处理 2：Yield Arena 是理财竞技场，代币不固定
    if "YIELD ARENA" in title_upper:
        return "多币种"
    
    # 特殊处理 3：Velvet 交易竞赛
    if "VELVET" in title_upper:
        return "VELVET"
    
    # 特殊处理 4：Midnight 的代币是 NIGHT
    if "MIDNIGHT" in title_upper:
        return "NIGHT"
    
    # 特殊处理 5：Humanity Protocol 的代币是 H
    if "HUMANITY PROTOCOL" in title_upper:
        return "H"
    
    # 特殊处理 6：Opinion 的代币是 OPN
    if "OPINION" in title_upper or "(OPN)" in title_upper:
        return "OPN"
    
    # 特殊处理 7：单独字母 U 需要前后是空格或标点（避免匹配到 OpenClaw 等）
    import re
    # 检查是否有 " U " 或 " U," 或 " U." 等模式（U 币理财）
    if re.search(r'\bU\s+(Flexible|理财|Products)', title, re.IGNORECASE):
        return "U"
    
    # 特殊处理 8：Unitas 的代币是 UP（需要同时有 Unitas 或 (UP)）
    if "UNITAS" in title_upper or re.search(r'\(UP\)', title_upper):
        return "UP"
    
    # 特殊处理 9：Block Street 的代币是 BSB
    if "BLOCK STREET" in title_upper or "(BSB)" in title_upper:
        return "BSB"
    
    # 特殊处理 10：Katana 的代币是 KAT
    if "KATANA" in title_upper:
        return "KAT"
    
    # 特殊处理 11：CreatorPad 任务通常是 SIGN 或 NIGHT
    if "CREATORPAD" in title_upper:
        if "SIGN" in title_upper:
            return "SIGN"
        elif "NIGHT" in title_upper:
            return "NIGHT"
    
    # 先检查完整代币名（按长度倒序，优先匹配长的）
    for token in sorted(TOKEN_PATTERNS.keys(), key=len, reverse=True):
        # 使用单词边界匹配，避免部分匹配
        if re.search(r'\b' + re.escape(token) + r'\b', title, re.IGNORECASE):
            return TOKEN_PATTERNS[token]
    
    # 如果没有匹配，检查是否是交易竞赛（通常标题里有代币名）
    if "TRADING COMPETITION" in title_upper or "交易竞赛" in title:
        # 尝试从标题提取第一个大写字母组合（至少 2 个字母）
        match = re.search(r'\b([A-Z]{2,10})\b', title)
        if match:
            return match.group(1)
    
    return "多币种"

def is_region_restricted(content_text):
    """检测内容是否有区域限制（华语地区）"""
    if not content_text:
        return False
    
    content_lower = content_text.lower()
    for keyword in REGION_RESTRICTED_KEYWORDS:
        if keyword.lower() in content_lower:
            return True
    return False

def is_square_task(code, title="", body=""):
    """识别是否是广场任务（通过 CreatorPad code 匹配 + 文章详情标识）"""
    import re
    
    # 手动维护的广场任务列表（CreatorPad 任务）
    square_codes = [
        "d6fd86054b00445a97897606033970d8",  # NIGHT CreatorPad - 广场任务 ✅
        "820d2bb637d04f17983048ab7f4bf1f1",  # ROBO CreatorPad - 广场任务 ✅
        "d0886cd0da82460ba8c32b466f7b2cc1",  # SIGN CreatorPad - 广场任务 ✅ (已修正)
    ]
    
    # 如果 code 匹配，直接返回 True
    if code in square_codes:
        return True
    
    # 通过关键词判断（改进版）
    content = (title + " " + body).lower()
    
    # SIGN 专属关键词（最高优先级）
    sign_keywords = ["sign protocol", "sign rewards", "sign 创作者", "1,968,000 sign", "sign 奖励"]
    for kw in sign_keywords:
        if kw.lower() in content:
            return True
    
    # CreatorPad 标识（支持正则匹配）
    creatorpad_patterns = [
        r'\bcreatorpad\b',
        r'\bcreator\s*pad\b',
        r'\bcreator-pad\b',
        r'on\s+creatorpad',
    ]
    for pattern in creatorpad_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    # Square Task 标识
    square_keywords = ["binance square", "广场任务", "square task", "square post",
                       "发贴", "发帖", "share on square", "publish on square"]
    for kw in square_keywords:
        if kw in content:
            return True
    
    # 在文章详情中查找特殊标识（HTML 标签或特定文本）
    # 通常 CreatorPad 任务会有特殊的 badge 或标签
    html_indicators = [
        'data-task-type="creatorpad"',
        'class="creatorpad"',
        'square-badge',
        '广场任务标识',
    ]
    for indicator in html_indicators:
        if indicator in body.lower():
            return True
    
    return False

def get_reward_apr(title):
    """从标题提取奖池或 APR 信息"""
    import re
    
    # 提取 APR（如 8%、11.5%）
    apr_match = re.search(r'(\d+\.?\d*)\s*%\s*APR', title, re.IGNORECASE)
    if apr_match:
        return f"{apr_match.group(1)}% APR"
    
    # 提取奖池（如 2000 USDC、1000 万 SHELL）
    reward_patterns = [
        r'(\d+[,\d]*\s*(?: 万)?\s*(?:USDC|USDT|BUSD|RLUSD|SHIB|NIGHT|OPN|ROBO|TRIA|KITE|VELVET|H|SIGN|KAT|SXT|WLFI|SAHARA|BSB|CFG))',
        r'\$\s*(\d+[,\d]*(?:K|M|B)?)',  # $200K, $500K
        r'(\d+\s*USDT)',  # 100 USDT
    ]
    
    for pattern in reward_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # 特定活动（只针对明确的活动名称）
    if "Yield Arena" in title:
        return "11.5% APR"
    elif "Share Up to 120M NIGHT" in title:
        return "1.2 亿 NIGHT"
    elif "Grab a Share of the 90,000,000 NIGHT" in title:
        return "9000 万 NIGHT"
    elif "2,500,000 OPN Token Voucher" in title:
        return "250 万 OPN"
    elif "Share 10 Million SHELL Rewards" in title:
        return "1000 万 SHELL"
    elif "Grab a Share of 8,600,000 ROBO" in title:
        return "860 万 ROBO"
    elif "Trading Competition" in title and "$200K" in title:
        return "20 万美金"
    # 新增活动
    elif "1,968,000 SIGN" in title:
        return "196.8 万 SIGN"
    elif "25,000,000 KAT" in title:
        return "2500 万 KAT"
    elif "135 Million WLFI" in title:
        return "1.35 亿 WLFI"
    elif "4,000,000 SAHARA" in title:
        return "400 万 SAHARA"
    elif "835,000 CFG" in title:
        return "83.5 万 CFG"
    elif "2,000,000 NIGHT" in title and "CreatorPad" in title:
        return "200 万 NIGHT"
    elif "35% APR" in title and "SXT" in title:
        return "35% APR"
    elif "10% APR" in title and "U Flexible" in title:
        return "10% APR"
    elif "300 USDT" in title:
        return "300 USDT"
    elif "8,000 USDC" in title:
        return "8000 USDC"
    elif "$100K" in title and "BSB" in title:
        return "10 万美金"
    
    return "详见页面"
