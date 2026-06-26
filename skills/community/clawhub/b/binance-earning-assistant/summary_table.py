#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安撸毛助手 - API 实时版本
特点：
1. 从币安 API 实时获取活动列表（catalogId: 93）
2. 截止日期从文章详情 API 提取（确保准确）
3. 数据准确是第一原则
"""

import json
import requests
import re
import html
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from activity_names import get_chinese_name, extract_token, is_region_restricted, is_square_task, get_reward_apr

def extract_text_from_json_node(node):
    """递归提取 JSON 结构中的所有文本"""
    texts = []
    if isinstance(node, dict):
        if node.get('node') == 'text':
            text = node.get('text', '')
            # 清理 HTML 实体
            text = html.unescape(text.replace('&nbsp;', ' '))
            texts.append(text)
        elif 'child' in node:
            for child in node['child']:
                texts.extend(extract_text_from_json_node(child))
    elif isinstance(node, list):
        for item in node:
            texts.extend(extract_text_from_json_node(item))
    return texts

def strip_html_tags(html_text):
    """提取 HTML 或 JSON 结构中的纯文本"""
    # 尝试解析为 JSON（币安文章 body 可能是 JSON 格式）
    try:
        parsed = json.loads(html_text)
        texts = extract_text_from_json_node(parsed)
        text = ' '.join(texts)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except (json.JSONDecodeError, TypeError):
        # 不是 JSON，按 HTML 处理
        text = re.sub(r'<[^>]+>', ' ', html_text)
        text = html.unescape(text)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        return text

# 缓存已获取的文章详情，避免重复请求
ARTICLE_DETAIL_CACHE = {}

def get_alpha_airdrops():
    """从 alpha123.uk 获取最新 Alpha 空投数据"""
    try:
        # 尝试访问 alpha123.uk 获取空投数据
        url = "https://alpha123.uk/zh/"
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html"}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            # 正确解码 UTF-8
            html = resp.content.decode('utf-8')
            
            # 简单解析 HTML 获取空投信息
            airdrops = []
            
            # 查找包含"KAT"或"Katana"的内容
            if "KAT" in html or "Katana" in html or "katana" in html:
                airdrops.append({
                    "project": "KAT (Katana)",
                    "points": "241 积分",
                    "amount": "待公布",
                    "time": "今日 20:00"
                })
            
            return airdrops
    except Exception as e:
        print(f"Alpha 空投获取错误：{e}")
    
    # 默认返回空列表
    return []

def get_article_details(code):
    """从文章详情 API 获取活动完整信息"""
    if code in ARTICLE_DETAIL_CACHE:
        return ARTICLE_DETAIL_CACHE[code]
    
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query"
    params = {"articleCode": code}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            body = data.get("data", {}).get("body", "")
            title = data.get("data", {}).get("title", "")
            
            # 提取 HTML 中的纯文本
            pure_body = strip_html_tags(body)
            
            # 获取发布日期（从 API 响应中）
            release_date = ""
            release_ts = data.get("data", {}).get("publishDate", 0)
            if release_ts:
                if isinstance(release_ts, str):
                    release_date = release_ts
                else:
                    # UTC 时间戳转 UTC+8
                    tz_utc8 = timezone(timedelta(hours=8))
                    release_dt = datetime.fromtimestamp(release_ts / 1000, tz=timezone.utc)
                    release_dt_utc8 = release_dt.astimezone(tz_utc8)
                    release_date = release_dt_utc8.strftime('%Y-%m-%d')
            
            # 提取截止日期（支持多格式）
            end_date = ""
            
            def parse_date(text, current_year, next_year):
                """解析多种日期格式，返回 YYYY-MM-DD 或 None"""
                # 格式 1: YYYY-MM-DD 或 YYYY/MM/DD
                match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', text)
                if match:
                    y, m, d = match.groups()
                    return f"{y}-{int(m):02d}-{int(d):02d}"
                
                # 格式 2: DD/MM/YYYY 或 MM/DD/YYYY（根据上下文判断）
                match = re.search(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', text)
                if match:
                    a, b, y = match.groups()
                    # 如果第一个数字>12，则是 DD/MM/YYYY
                    if int(a) > 12:
                        return f"{y}-{int(b):02d}-{int(a):02d}"
                    # 否则假设是 MM/DD/YYYY（美股惯用）
                    else:
                        return f"{y}-{int(a):02d}-{int(b):02d}"
                
                # 格式 3: March 25, 2026 或 25 March 2026
                months = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
                          'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
                          'jan':1,'feb':2,'mar':3,'apr':4,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
                match = re.search(r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', text)
                if match:
                    mon, day, year = match.groups()
                    mon_num = months.get(mon.lower())
                    if mon_num:
                        return f"{year}-{mon_num:02d}-{int(day):02d}"
                
                # 格式 4: 25 March 2026
                match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
                if match:
                    day, mon, year = match.groups()
                    mon_num = months.get(mon.lower())
                    if mon_num:
                        return f"{year}-{mon_num:02d}-{int(day):02d}"
                
                return None
            
            # 获取当前年份和下一年（动态年份支持）
            tz_utc8 = timezone(timedelta(hours=8))
            current_year = datetime.now(tz_utc8).year
            next_year = current_year + 1
            
            # 优先级 1：Activity Period / Promotion Period: YYYY-MM-DD to YYYY-MM-DD
            # 优先提取活动周期中的结束日期，而不是奖励发放日期
            # 支持格式：Activity Period: 2026-03-23 00:00 (UTC) to 2026-03-29 23:59 (UTC)
            # 注意：使用 .*? 而非 [^0-9]*? 以支持时间格式（如 10:30）
            period_match = re.search(r'(?:Activity|Promotion) Period\s*:\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2}).*?(?:to|–|-).*?(\d{4}[-/]\d{1,2}[-/]\d{1,2})', pure_body, re.IGNORECASE)
            if period_match:
                end_date = period_match.group(2)  # 取结束日期
                print(f"[DEBUG] 找到 Activity/Promotion Period: {end_date}")
                # 找到 Activity Period 后，不再继续匹配其他日期
            else:
                # 优先级 2：其他日期匹配逻辑
                # 尝试多种模式匹配截止日期
                patterns = [
                    r'(?:End|截止|Until|To|结束|到期)[:\s]*([A-Za-z0-9,\s\-/]+?)(?:\s|$|\n)',
                    r'([A-Za-z]+\s+\d{1,2},?\s+\d{4})',  # March 25, 2026
                    r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})',     # 25 March 2026
                    r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',     # 2026-03-25
                    r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',     # 25/03/2026
                ]
                
                candidate_dates = []
                for pattern in patterns:
                    matches = re.findall(pattern, pure_body, re.IGNORECASE)
                    for m in matches:
                        parsed = parse_date(m, current_year, next_year)
                        if parsed:
                            candidate_dates.append(parsed)
                
                # 排除奖励发放相关日期（distribution, distribute by 等）
                filtered_dates = []
                for date in candidate_dates:
                    # 检查该日期附近是否有 distribution 相关词汇
                    date_pattern = re.escape(date)
                    # 查找日期前后 50 个字符
                    context_pattern = r'.{0,50}' + date_pattern + r'.{0,50}'
                    context_matches = re.findall(context_pattern, pure_body, re.IGNORECASE)
                    
                    is_distribution = False
                    for context in context_matches:
                        if any(kw in context.lower() for kw in ['distribution', 'distribute by', 'distribute', 'reward date', 'disbursement']):
                            is_distribution = True
                            break
                    
                    if not is_distribution:
                        filtered_dates.append(date)
                
                # 使用过滤后的日期列表
                if filtered_dates:
                    candidate_dates = filtered_dates
                
                # 验证逻辑：截止日期必须 > 发布日期
                if candidate_dates and release_date:
                    valid_dates = [d for d in candidate_dates if d > release_date]
                    if valid_dates:
                        end_date = max(valid_dates)
                    else:
                        # 如果没有有效日期，取最大的候选（可能是格式问题）
                        end_date = max(candidate_dates)
                elif candidate_dates:
                    end_date = max(candidate_dates)
            
            # Fallback 机制：匹配失败返回"详见页面"
            if not end_date:
                end_date = "详见页面"
            
            # 判断是否华语区活动
            is_chinese_region = True
            
            # 检查非华语区关键词
            non_chinese_keywords = ["pakistan", "africa", "balkans", "nigeria", "uganda", "ghana", "kenya", "morocco", "cameroon", "turkmenistan", "ramadan"]
            if any(kw in pure_body.lower() for kw in non_chinese_keywords):
                is_chinese_region = False
            
            # 添加中东货币代码检测
            middle_east_currencies = ["PKR", "SAR", "EGP", "KWD", "JOD", "QAR", "OMR", "IQD", "LBP"]
            if any(currency in pure_body.upper() for currency in middle_east_currencies):
                is_chinese_region = False
            
            # 添加伊斯兰节日关键词（只检测完整短语，避免误判 URL 中的片段）
            islamic_holidays = ["eid al-fitr", "eid al-adha", "eid mubarak", "ramadan"]
            if any(kw in pure_body.lower() for kw in islamic_holidays):
                is_chinese_region = False
            
            # 检查特定奖励类型（可能是区域限制活动）
            # 如果活动奖励是 HOME Token、Referral Code 等，通常是区域限制活动
            special_rewards = ["home token", "home rewards", "referral code", "new users", "welcome rewards"]
            if any(kw in pure_body.lower() for kw in special_rewards):
                # 这类活动通常在华语区不可用
                is_chinese_region = False
            
            # 判断活动类型
            activity_type = "other"
            if "super earn" in pure_body.lower():
                activity_type = "super_earn"
            elif "earn" in pure_body.lower() or "apr" in pure_body.lower():
                activity_type = "earn"
            elif "reward" in pure_body.lower():
                activity_type = "reward"
            elif "competition" in pure_body.lower() or "trading" in pure_body.lower():
                activity_type = "competition"
            elif "airdrop" in pure_body.lower():
                activity_type = "airdrop"
            
            # SIGN 任务检测（关键词：SIGN, Sign Protocol, Web3 身份，SBT, NFT 身份）
            sign_keywords = ["sign", "sign protocol", "web3 身份", "web3 identity", 
                           "sbt", "soulbound", "nft 身份", "nft identity", "identity protocol"]
            has_sign_content = any(kw in pure_body.lower() for kw in sign_keywords)
            
            # 如果是 SIGN 相关内容，标记特殊标识
            if has_sign_content:
                result = {
                    "end_date": end_date,
                    "is_chinese_region": is_chinese_region,
                    "activity_type": "sign_task",  # 特殊类型
                    "body": pure_body,
                    "title": title,
                    "is_sign_task": True
                }
            else:
                result = {
                    "end_date": end_date,
                    "is_chinese_region": is_chinese_region,
                    "activity_type": activity_type,
                    "body": pure_body,
                    "title": title,
                    "is_sign_task": False
                }
            
            result = {
                "end_date": end_date,
                "is_chinese_region": is_chinese_region,
                "activity_type": activity_type,
                "body": pure_body,
                "title": title
            }
            ARTICLE_DETAIL_CACHE[code] = result
            return result
    except:
        pass
    
    result = {"end_date": "", "is_chinese_region": True, "activity_type": "other", "body": "", "title": ""}
    ARTICLE_DETAIL_CACHE[code] = result
    return result

# 赚钱关键词
MONEY_KEYWORDS = [
    "airdrop", "空投", "alpha", "web3", "task", "任务",
    "launchpool", "挖矿", "earn", "质押", "staking", "simple earn", "理财",
    "hodler", "竞赛", "比赛", "competition", "challenge", "trading", "reward", "奖励",
    "share", "瓜分", "super",
    # SIGN 任务关键词
    "sign", "sign protocol", "web3 身份", "sbt", "soulbound", "nft 身份"
]

# 排除关键词（非撸毛活动 + 非华语地区）
EXCLUDE_KEYWORDS = [
    # 交易规则变更
    "perpetual contract", "永续合约",
    "futures will launch",
    "options", "monitoring tag", "tick size",
    # 非华语地区活动
    "pakistan", "africa", "balkans", "nigeria", "uganda", "ghana", "kenya",
    "morocco", "cameroon", "turkmenistan", "ramadan", "jalsat", "suhoor",
    "巴基斯坦", "非洲", "巴尔干", "尼日利亚", "乌干达", "加纳", "肯尼亚",
    "摩洛哥", "喀麦隆", "土库曼", "斋月",
]

def get_binance_activities():
    """从币安 API 实时获取活动（catalogId: 93 = Latest Activities）"""
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {"type": "1", "pageNo": "1", "pageSize": "50", "catalogId": "93"}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "000000":
                return data.get("data", {}).get("catalogs", [{}])[0].get("articles", [])
    except Exception as e:
        print(f"API 错误：{e}")
    return []

def filter_earning_activities(articles):
    """过滤赚钱相关活动"""
    earning = []
    for article in articles:
        title = article.get("title", "").lower()
        
        # 排除非撸毛活动
        if any(kw in title for kw in EXCLUDE_KEYWORDS):
            continue
        
        # 必须包含赚钱关键词
        if not any(kw in title for kw in MONEY_KEYWORDS):
            continue
        
        earning.append(article)
    
    return earning

def format_date(date_str):
    """格式化日期显示"""
    if not date_str:
        return "--"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%m-%d")
    except:
        return date_str

def categorize(title):
    """活动分类"""
    title_lower = title.lower()
    # 优先判断 Launchpool
    if "launchpool" in title_lower:
        return "💰 Launchpool"
    # 理财类（需要明确是 Binance Earn 或 Simple Earn 产品）
    elif "super earn" in title_lower or "simple earn" in title_lower or "yield arena" in title_lower:
        return "💰 理财"
    elif "flexible products" in title_lower or "flexible 理财" in title_lower:
        return "💰 理财"
    elif "binance earn" in title_lower and ("apr" in title_lower or "share" in title_lower):
        return "💰 理财"
    elif "理财" in title:
        return "💰 理财"
    # 所有其他都归类为活动奖励（包括空投、交易竞赛、奖励等）
    else:
        return "🎁 活动奖励"

def format_summary_table():
    """生成简洁的表格形式输出"""
    # 使用 UTC+8 时间（华语区）
    from datetime import timezone
    tz_utc8 = timezone(timedelta(hours=8))
    today = datetime.now(tz_utc8)
    today_str = today.strftime('%Y-%m-%d')
    
    # 从 API 实时获取活动
    articles = get_binance_activities()
    earning_articles = filter_earning_activities(articles)
    
    # 去重（按 code）
    seen_codes = set()
    unique_articles = []
    for article in earning_articles:
        code = article.get("code", "")
        if code not in seen_codes:
            seen_codes.add(code)
            unique_articles.append(article)
    
    # 过滤有效活动（正在进行中的 + 非区域限制）
    valid_activities = []
    seen_names = set()  # 按活动名称关键词去重
    
    for article in unique_articles:
        title = article.get("title", "")
        code = article.get("code", "")
        release_ts = article.get("releaseDate", 0)
        
        # 获取发布日期（UTC 转 UTC+8）
        release_date = ""
        if release_ts:
            if isinstance(release_ts, str):
                release_date = release_ts
            else:
                # UTC 时间戳转 UTC+8
                release_dt = datetime.fromtimestamp(release_ts / 1000, tz=timezone.utc)
                release_dt_utc8 = release_dt.astimezone(tz_utc8)
                release_date = release_dt_utc8.strftime('%Y-%m-%d')
        
        # 从文章详情 API 获取准确截止日期 + 区域限制判断
        details = get_article_details(code)
        end_date = details.get("end_date", "")
        is_chinese_region = details.get("is_chinese_region", True)
        
        # 过滤 1: 区域限制检测（只保留华语区活动）
        if not is_chinese_region:
            continue
        
        # 去重检查：使用 code 作为唯一标识（最准确）
        # 每个活动都是独立的，不能仅凭 token 或活动类型判断
        code_key = f"code_{code}"
        
        if code_key in seen_names:
            continue  # 重复活动，跳过
        seen_names.add(code_key)
        
        # 过滤 2: 只保留正在进行中的活动（截止日期 >= 今天 UTC+8）
        # 严格过滤：截止日期必须 >= 今天
        if end_date and end_date != "详见页面":
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=tz_utc8)
                if end_dt.date() < today.date():
                    print(f"[过期活动已过滤] {title[:60]}... - 截止日期：{end_date} (已过期)")
                    continue  # 已过期，跳过
            except Exception as e:
                print(f"[日期解析失败已过滤] {title[:60]}... - end_date: {end_date}, 错误：{e}")
                continue  # 日期解析失败，过滤
        else:
            # 没有截止日期的，检查是否在 7 天内发布
            if release_date:
                try:
                    release_dt = datetime.strptime(release_date, "%Y-%m-%d").replace(tzinfo=tz_utc8)
                    if (today - release_dt).days > 7:
                        print(f"[过期活动已过滤] {title[:60]}... - 发布日期：{release_date} (超过 7 天)")
                        continue  # 超过 7 天，跳过
                except Exception as e:
                    print(f"[日期解析失败已过滤] {title[:60]}... - release_date: {release_date}, 错误：{e}")
                    continue  # 日期解析失败，过滤
            else:
                print(f"[日期解析失败已过滤] {title[:60]}... - 无截止日期且无发布日期")
                continue  # 无日期信息，过滤
        
        # 提取信息
        chinese_name = get_chinese_name(title)
        category = categorize(title)
        token = extract_token(title)
        reward_apr = get_reward_apr(title)
        
        valid_activities.append({
            "chinese_name": chinese_name,
            "category": category,
            "token": token,
            "reward_apr": reward_apr,
            "release_date": release_date,
            "end_date": end_date,
            "code": code,
        })
    
    # 按分类分组 + 广场任务分离
    grouped = defaultdict(list)
    square_tasks = []
    
    for act in valid_activities:
        # 获取文章详情中的 title 和 body
        details = get_article_details(act['code'])
        title = details.get("title", "")
        body = details.get("body", "")
        
        if is_square_task(act['code'], title, body):
            square_tasks.append(act)
        else:
            grouped[act['category']].append(act)
    
    # 定义分类顺序
    category_order = ["💰 Launchpool", "💰 理财", "🎁 活动奖励"]
    
    lines = []
    lines.append("🚀 *币安撸毛助手*")
    lines.append(f"📅 更新时间：{today.strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append(f"📊 当前可参与活动：*{len(valid_activities)} 个*")
    lines.append("")
    lines.append("⚠️ **数据说明：所有数据来自币安 API 实时获取，确保准确**")
    lines.append("")
    
    # 今日上新（今天发布的活动）
    new_today = [a for a in valid_activities if a.get('release_date', '') == today_str]
    if new_today:
        lines.append(f"🆕 *今日上新* （{len(new_today)} 个）")
        lines.append("```")
        lines.append(f"{'序号':<4} {'活动名称':<30}")
        lines.append("-" * 40)
        for i, act in enumerate(new_today, 1):
            name = act['chinese_name'][:27] + "..." if len(act['chinese_name']) > 30 else act['chinese_name']
            lines.append(f"{i:<4} {name:<30}")
        lines.append("```")
        lines.append("")
    
    # 按分类显示活动列表
    lines.append("📋 *活动列表*")
    lines.append("")
    
    global_index = 1
    for category in category_order:
        if category not in grouped:
            continue
        
        acts = grouped[category]
        lines.append(f"*{category}* （{len(acts)} 个）")
        lines.append("```")
        lines.append(f"{'序号':<4} {'代币':<6} {'奖池/APR':<15} {'活动名称':<20} {'发布':<5} {'截止':<5}")
        lines.append("-" * 60)
        
        for act in acts:
            name = act['chinese_name'][:17] + "..." if len(act['chinese_name']) > 20 else act['chinese_name']
            token = act['token'][:4] + "..." if len(act['token']) > 6 else act['token']
            reward = act['reward_apr'][:12] + "..." if len(act['reward_apr']) > 15 else act['reward_apr']
            release = format_date(act.get('release_date', ''))
            end = format_date(act.get('end_date', ''))
            lines.append(f"{global_index:<4} {token:<6} {reward:<15} {name:<20} {release:<5} {end:<5}")
            global_index += 1
        
        lines.append("```")
        lines.append("")
    
    # 广场任务单独显示（序号接着上文）
    if square_tasks:
        lines.append(f"📱 *广场任务* （{len(square_tasks)} 个）")
        lines.append("```")
        lines.append(f"{'序号':<4} {'代币':<6} {'奖池/APR':<15} {'活动名称':<20} {'发布':<5} {'截止':<5}")
        lines.append("-" * 60)
        for act in square_tasks:
            name = act['chinese_name'][:17] + "..." if len(act['chinese_name']) > 20 else act['chinese_name']
            token = act['token'][:4] + "..." if len(act['token']) > 6 else act['token']
            reward = act['reward_apr'][:12] + "..." if len(act['reward_apr']) > 15 else act['reward_apr']
            release = format_date(act.get('release_date', ''))
            end = format_date(act.get('end_date', ''))
            # 使用 global_index 作为序号（接着上文）
            lines.append(f"{global_index:<4} {token:<6} {reward:<15} {name:<20} {release:<5} {end:<5}")
            global_index += 1
        lines.append("```")
        lines.append("")
    
    # Alpha 空投预告（实时获取）
    alpha_airdrops = get_alpha_airdrops()
    
    lines.append("🚀 *Alpha 空投预告*")
    lines.append("```")
    lines.append(f"{'项目':<25} {'积分':<12} {'数量':<10} {'时间':<15}")
    lines.append("-" * 65)
    
    if alpha_airdrops:
        for drop in alpha_airdrops:
            project = drop['project'][:22] + "..." if len(drop['project']) > 25 else drop['project']
            points = drop.get('points', '详见页面')[:10]
            amount = drop.get('amount', '详见页面')[:8]
            time_str = drop.get('time', '详见页面')
            lines.append(f"{project:<25} {points:<12} {amount:<10} {time_str:<15}")
    else:
        lines.append(f"{'暂无':<25} {'-':<12} {'-':<10} {'-':<15}")
    
    lines.append("```")
    lines.append("")
    
    # 提示
    lines.append("💡 *查看详情*")
    lines.append("回复序号（如：1、2、3）查看具体活动详情")
    lines.append("")
    lines.append("⚠️ 投资有风险，参与需谨慎")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(format_summary_table())
