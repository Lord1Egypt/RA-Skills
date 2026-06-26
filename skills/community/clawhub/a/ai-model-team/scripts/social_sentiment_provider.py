"""
Social Sentiment Data Provider - 完整版 (P1 Enhanced)
整合多渠道社会情绪数据,含去噪、来源权重、时间衰减
"""
import requests
import feedparser
import re
import hashlib
import time
from typing import List, Dict, Set, Optional, Callable
from datetime import datetime, timedelta, timezone
from collections import Counter
from functools import wraps

# P1 配置
SENTIMENT_SOURCE_WEIGHTS = {"news": 0.5, "reddit": 0.3, "rss": 0.2}
SENTIMENT_HALF_LIFE_MIN = 180  # 3小时半衰期
SENTIMENT_SPAM_FILTER = True


class ContentDeduplicator:
    """内容去重"""

    def __init__(self):
        self.seen_hashes: Set[str] = set()
        self.seen_titles: Set[str] = set()

    def normalize(self, text: str) -> str:
        """标准化文本用于比较"""
        return re.sub(r'[^\w\s]', '', text.lower()).strip()[:100]

    def is_duplicate(self, text: str) -> bool:
        """检查是否重复"""
        normalized = self.normalize(text)

        # 精确匹配
        if normalized in self.seen_titles:
            return True

        # 相似度匹配 (简单hash)
        text_hash = hashlib.md5(normalized.encode()).hexdigest()[:16]
        if text_hash in self.seen_hashes:
            return True

        # 添加到已见集合
        self.seen_titles.add(normalized)
        self.seen_hashes.add(text_hash)
        return False

    def reset(self):
        self.seen_hashes.clear()
        self.seen_titles.clear()


class SpamFilter:
    """垃圾内容过滤"""

    SPAM_PATTERNS = [
        r'click here', r'buy now', r'limited time',
        r'Act now', r'discount', r'free money',
        r'guaranteed', r'100% winning',
        r'bot account', r'auto-trading bot'
    ]

    LOW_QUALITY_KEYWORDS = [
        r'^RT @', r'follow me', r'subscribe',
        r'check my profile', r'dm me'
    ]

    @classmethod
    def is_spam(cls, title: str) -> bool:
        """判断是否为垃圾内容"""
        title_lower = title.lower()

        # 检查垃圾模式
        for pattern in cls.SPAM_PATTERNS:
            if re.search(pattern, title_lower, re.IGNORECASE):
                return True

        # 检查低质量模式
        for pattern in cls.LOW_QUALITY_KEYWORDS:
            if re.search(pattern, title_lower, re.IGNORECASE):
                return True

        return False


class SocialSentimentProvider:
    """社会情绪数据提供者 (P1增强版)"""

    # Reddit API 需要完整的 User-Agent，否则会被拒绝
    REDDIT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # 秒

    @staticmethod
    def _retry_request(func: Callable) -> Callable:
        """请求重试装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(SocialSentimentProvider.MAX_RETRIES):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < SocialSentimentProvider.MAX_RETRIES - 1:
                        time.sleep(SocialSentimentProvider.RETRY_DELAY * (attempt + 1))
            # 所有重试都失败
            raise last_error
        return wrapper

    RSS_SOURCES = {
        # 加密货币
        "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "cointelegraph": "https://cointelegraph.com/rss",
        "decrypt": "https://decrypt.co/feed",
        # 四大新闻社 (通用财经)
        "bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
        "wsj": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "ft": "https://www.ft.com/rss/home",
        # 其他主流媒体
        "bbc_business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "economist": "https://www.economist.com/finance-and-economics/rss.xml",
        "nytimes": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    }

    # 来源权重
    SOURCE_WEIGHTS = {
        # 加密货币
        "coindesk": 0.15,
        "cointelegraph": 0.15,
        "decrypt": 0.05,
        # 四大新闻社
        "bloomberg": 0.12,
        "wsj": 0.10,
        "cnbc": 0.10,
        "ft": 0.08,
        # 其他媒体
        "bbc_business": 0.08,
        "economist": 0.04,
        "nytimes": 0.03
    }

    # Reddit 板块配置 (按类型分组)
    SUBREDDITS = {
        "crypto": ["cryptocurrency", "BitCoin", "ethereum", "SOLToken", "CardanoEGLD"],
        "stocks": ["stocks", "investing", "wallstreetbets", "StockMarket", "Smallistening"],
        "tech": ["NVDA", "Apple", "TechStock", "Google", "Microsoft"],  # stock-specific
        "general": ["business", "economics", "finance"]
    }

    # 股票相关Reddit板块
    STOCK_SUBREDDITS = ["stocks", "investing", "wallstreetbets", "StockMarket", "Smallistening"]

    # 通用财经/国际新闻RSS (对股市/数字货币影响极大)
    GENERAL_NEWS_SOURCES = {
        "reuters_world": "https://feeds.reuters.com/reuters/worldNews",
        "reuters_business": "https://feeds.reuters.com/reuters/businessNews",
        "reuters_markets": "https://feeds.reuters.com/reuters/marketsNews",
        "bbc_world": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "bbc_us": "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
        "cnn_business": "http://rss.cnn.com/rss/money_latest.rss",
        "guardian_business": "https://www.theguardian.com/business/rss",
        "wsj_world": "https://feeds.a.dj.com/rss/worldNews.xml",
    }

    # 情绪关键词 (扩展版 - 包含宏观经济)
    BULLISH_WORDS = [
        'bull', 'bullish', 'moon', 'pump', 'hodl', 'buy', 'long', 'breakout', 'ath',
        'surge', 'rally', 'gain', 'soar', 'jump', 'rise', 'up', 'growth', 'profit',
        'beat', 'exceed', 'strong', 'optimistic', 'recover', 'boom'
    ]
    BEARISH_WORDS = [
        'bear', 'bearish', 'dump', 'crash', 'sell', 'short', 'bottom', 'capitulation',
        'drop', 'fall', 'plunge', 'tumble', 'decline', 'down', 'loss', 'weak',
        'miss', 'concern', 'recession', 'bubble', 'panic', 'scare'
    ]

    def __init__(self):
        self.dedup = ContentDeduplicator()
        self.spam_filter = SpamFilter()
        self.seen_hashes: Set[str] = set()

    def get_cryptopanic_news(self, currency: str = "BTC", limit: int = 20) -> List[Dict]:
        """获取 CryptoPanic 新闻"""
        try:
            url = f"https://cryptopanic.com/news/{currency.lower()}/"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return []
            html = response.text
            news_items = []
            pattern = r'data-title="([^"]+)".*?data-votes-up="(\d+)".*?data-votes-down="(\d+)"'
            matches = re.findall(pattern, html, re.DOTALL)
            for title, up, down in matches[:limit]:
                # 去重
                if self.dedup.is_duplicate(title):
                    continue

                # 垃圾过滤
                if SENTIMENT_SPAM_FILTER and SpamFilter.is_spam(title):
                    continue

                up_votes = int(up) if up else 0
                down_votes = int(down) if down else 0
                total = up_votes + down_votes
                sentiment = (up_votes - down_votes) / total if total > 0 else 0
                sentiment_label = "positive" if sentiment > 0.2 else "negative" if sentiment < -0.2 else "neutral"

                news_items.append({
                    "source": "cryptopanic",
                    "title": title.strip(),
                    "sentiment_score": round(sentiment, 3),
                    "sentiment_label": sentiment_label,
                    "up_votes": up_votes,
                    "down_votes": down_votes,
                    "weight": self.SOURCE_WEIGHTS.get("cryptopanic", 0.3)
                })
            return news_items
        except:
            return []

    def get_reddit_sentiment(self, subreddit: str = "cryptocurrency", limit: int = 25) -> Dict:
        """获取 Reddit 社区情绪（带错误处理和重试）"""
        # 重试逻辑
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
                response = requests.get(url, headers=self.REDDIT_HEADERS, timeout=15)
                
                # 429 Too Many Requests - 等待后重试
                if response.status_code == 429:
                    wait_time = self.RETRY_DELAY * (attempt + 1)
                    print(f"  ⚠️ Reddit API 限流，等待 {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                if response.status_code != 200:
                    return {"error": f"HTTP {response.status_code}", "posts_analyzed": 0}
                
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                sentiment_data = {
                    "source": "reddit",
                    "subreddit": subreddit,
                    "posts_analyzed": 0,
                    "total_score": 0,
                    "sentiment_indicators": {
                        "bullish_keywords": 0, "bearish_keywords": 0,
                        "fomo_keywords": 0, "fear_keywords": 0
                    },
                    "hot_topics": []
                }
                bullish_words = ['bull', 'bullish', 'moon', 'pump', 'hodl', 'buy', 'long', 'breakout', 'ath']
                bearish_words = ['bear', 'bearish', 'dump', 'crash', 'sell', 'short', 'bottom', 'capitulation']
                fomo_words = ['fomo', 'getting in', 'jump in', "don't miss"]
                fear_words = ['panic', 'scared', 'worried', 'crash coming', 'bubble', 'scam', 'rug pull']

                for post in posts:
                    post_data = post.get("data", {})
                    title = post_data.get("title", "").lower()
                    selftext = post_data.get("selftext", "").lower()
                    full_text = title + " " + selftext

                    # 去重
                    if self.dedup.is_duplicate(post_data.get("title", "")):
                        continue

                    sentiment_data["posts_analyzed"] += 1
                    sentiment_data["total_score"] += post_data.get("score", 0)

                    for word in bullish_words:
                        if word in full_text:
                            sentiment_data["sentiment_indicators"]["bullish_keywords"] += 1
                    for word in bearish_words:
                        if word in full_text:
                            sentiment_data["sentiment_indicators"]["bearish_keywords"] += 1
                    for word in fomo_words:
                        if word in full_text:
                            sentiment_data["sentiment_indicators"]["fomo_keywords"] += 1
                    for word in fear_words:
                        if word in full_text:
                            sentiment_data["sentiment_indicators"]["fear_keywords"] += 1

                    if post_data.get("score", 0) > 50:
                        sentiment_data["hot_topics"].append({
                            "title": post_data.get("title", "")[:100],
                            "score": post_data.get("score", 0)
                        })

                total = sum(sentiment_data["sentiment_indicators"].values())
                if total > 0:
                    b = sentiment_data["sentiment_indicators"]["bullish_keywords"] / total
                    br = sentiment_data["sentiment_indicators"]["bearish_keywords"] / total
                    sentiment_data["overall_sentiment"] = "bullish" if b > br * 1.5 else "bearish" if br > b * 1.5 else "mixed"
                else:
                    sentiment_data["overall_sentiment"] = "neutral"

                # 添加权重
                sentiment_data["weight"] = self.SOURCE_WEIGHTS.get("reddit", 0.25)
                return sentiment_data
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                    continue
        return {"error": str(last_error), "posts_analyzed": 0}

    def get_rss_news(self, source: str = "coindesk", limit: int = 10) -> List[Dict]:
        """获取 RSS 新闻源"""
        rss_url = self.RSS_SOURCES.get(source)
        if not rss_url:
            return []
        try:
            feed = feedparser.parse(rss_url)
            news_items = []
            for entry in feed.entries[:limit]:
                title = entry.get("title", "").lower()

                # 去重
                if self.dedup.is_duplicate(entry.get("title", "")):
                    continue

                positive_words = ['surge', 'rally', 'gain', 'bull', 'breakout', 'adoption', 'partnership', 'soar', 'jump', 'rise']
                negative_words = ['crash', 'dump', 'fall', 'bear', 'ban', 'hack', 'scam', 'fear', 'drop', 'plunge', 'tumble']
                pos_count = sum(1 for w in positive_words if w in title)
                neg_count = sum(1 for w in negative_words if w in title)
                sentiment = "positive" if pos_count > neg_count else "negative" if neg_count > pos_count else "neutral"
                
                news_items.append({
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "sentiment": sentiment,
                    "sentiment_score": (pos_count - neg_count) / max(pos_count + neg_count, 1),  # 添加情绪得分
                    "weight": self.SOURCE_WEIGHTS.get(source, 0.1)
                })
            return news_items
        except:
            return []

    @staticmethod
    def apply_time_decay(sentiment_items: List[Dict], half_life_min: int = SENTIMENT_HALF_LIFE_MIN) -> List[Dict]:
        """应用时间衰减"""
        now = datetime.now(timezone.utc)
        half_life_delta = timedelta(minutes=half_life_min)

        for item in sentiment_items:
            if "timestamp" not in item:
                item["timestamp"] = now.isoformat()

            try:
                item_time = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
                age_min = (now - item_time).total_seconds() / 60
                decay = 0.5 ** (age_min / half_life_min)
                item["time_decay"] = decay
                item["age_min"] = age_min
            except:
                item["time_decay"] = 1.0
                item["age_min"] = 0

        return sentiment_items

    def get_reddit_multi_subreddit(self, currency: str = "BTC", limit: int = 25) -> Dict:
        """从多个subreddit获取情绪 (加密货币 + 股票 + 通用)"""
        combined_data = {
            "posts_analyzed": 0,
            "total_score": 0,
            "sentiment_indicators": {
                "bullish_keywords": 0, "bearish_keywords": 0,
                "fomo_keywords": 0, "fear_keywords": 0
            },
            "hot_topics": []
        }
        
        # 确定查询哪个subreddit组
        # 如果是股票代码(如NVDA, AAPL)，用stocks组；否则用crypto组
        stock_symbols = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'BTC', 'ETH']
        use_stocks = currency.upper() in stock_symbols or len(currency) <= 5
        
        if use_stocks:
            # 股票/通用财经subreddits
            subreddits_to_query = self.STOCK_SUBREDDITS + ["cryptocurrency"]
        else:
            # 加密货币subreddits
            subreddits_to_query = self.SUBREDDITS["crypto"]
        
        for subreddit in subreddits_to_query:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
                response = requests.get(url, headers=self.REDDIT_HEADERS, timeout=10)
                
                # 429 Too Many Requests - 跳过这个subreddit，稍后重试
                if response.status_code == 429:
                    print(f"  ⚠️ Reddit API 限流 (r/{subreddit}), 跳过")
                    continue
                
                if response.status_code != 200:
                    continue
                
                posts = response.json().get("data", {}).get("children", [])
                
                for post in posts[:limit]:
                    post_data = post.get("data", {})
                    title = post_data.get("title", "").lower()
                    selftext = post_data.get("selftext", "").lower()
                    full_text = title + " " + selftext
                    
                    combined_data["posts_analyzed"] += 1
                    combined_data["total_score"] += post_data.get("score", 0)
                    
                    for word in self.BULLISH_WORDS:
                        if word in full_text:
                            combined_data["sentiment_indicators"]["bullish_keywords"] += 1
                    for word in self.BEARISH_WORDS:
                        if word in full_text:
                            combined_data["sentiment_indicators"]["bearish_keywords"] += 1
                    
                    if post_data.get("score", 0) > 100:
                        combined_data["hot_topics"].append({
                            "title": post_data.get("title", "")[:100],
                            "score": post_data.get("score", 0),
                            "subreddit": subreddit
                        })
            except Exception:
                pass
        
        # 计算情绪
        total = sum(combined_data["sentiment_indicators"].values())
        if total > 0:
            b = combined_data["sentiment_indicators"]["bullish_keywords"] / total
            br = combined_data["sentiment_indicators"]["bearish_keywords"] / total
            combined_data["sentiment_score"] = b - br
        else:
            combined_data["sentiment_score"] = 0
        
        return combined_data

    def get_general_news(self, currency: str = "BTC", limit: int = 10) -> List[Dict]:
        """获取通用财经/国际新闻 (对股市/数字货币影响极大)"""
        all_news = []
        
        for source_name, url in self.GENERAL_NEWS_SOURCES.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:limit]:
                    title = entry.get("title", "")
                    
                    # 检查是否与currency相关 (标题中包含相关词)
                    relevance_score = 0
                    title_lower = title.lower()
                    
                    # 加密货币相关关键词
                    crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'coin', 'blockchain', 'solana', 'sol']
                    # 股票/市场关键词
                    stock_keywords = ['stock', 'market', 'nasdaq', 'dow', 's&p', 'fed', 'rate', 'inflation', 'economy']
                    # 地缘政治
                    geo_keywords = ['trump', 'china', 'tariff', 'trade', 'war', 'sanction', 'oil', 'iran', 'russia']
                    
                    # 计算相关性
                    if currency.lower() in title_lower:
                        relevance_score = 1.0
                    else:
                        keywords = crypto_keywords + stock_keywords + geo_keywords
                        for kw in keywords:
                            if kw in title_lower:
                                relevance_score += 0.2
                    
                    # 情绪分析 (使用扩展关键词)
                    title_lower = title.lower()
                    pos_count = sum(1 for w in self.BULLISH_WORDS if w in title_lower)
                    neg_count = sum(1 for w in self.BEARISH_WORDS if w in title_lower)
                    
                    if pos_count > neg_count:
                        sentiment = "positive"
                    elif neg_count > pos_count:
                        sentiment = "negative"
                    else:
                        sentiment = "neutral"
                    
                    all_news.append({
                        "source": source_name,
                        "title": title,
                        "sentiment": sentiment,
                        "sentiment_score": (pos_count - neg_count) / max(pos_count + neg_count, 1),
                        "relevance_score": relevance_score,
                        "weight": 0.1 + relevance_score * 0.2,  # 高相关性 = 高权重
                        "link": entry.get("link", "")
                    })
            except Exception:
                pass
        
        return all_news

        # 应用时间衰减
        rss_news = self.apply_time_decay(rss_news)

        # 加权计算 (RSS新闻)
        weighted_sum = 0
        weight_sum = 0

        for item in rss_news:
            weight = item.get("weight", 0.2) * item.get("time_decay", 1.0)
            sentiment = item.get("sentiment_score", 0) if item.get("sentiment_score") is not None else (0.5 if item.get("sentiment") == "positive" else 0.3 if item.get("sentiment") == "negative" else 0)
            weighted_sum += sentiment * weight
            weight_sum += weight

        news_score = weighted_sum / weight_sum if weight_sum > 0 else 0

    def get_combined_sentiment(self, currency: str = "BTC") -> Dict:
        """获取综合社会情绪 - 扩展版: 多subreddit + 通用财经/国际新闻"""
        print(f"📊 获取 {currency} 社会情绪数据...")

        # 1. Reddit (多subreddit: 股票 + 加密货币)
        print("  ▶ Reddit (多板块)...", end=" ", flush=True)
        reddit_data = self.get_reddit_multi_subreddit(currency, limit=20)
        print(f"✅ {reddit_data.get('posts_analyzed', 0)} 帖")

        # 2. 加密货币RSS
        print("  ▶ 加密货币RSS...", end=" ", flush=True)
        crypto_news = []
        for source in ["coindesk", "cointelegraph", "decrypt"]:
            news = self.get_rss_news(source, limit=5)
            crypto_news.extend(news)
        print(f"✅ {len(crypto_news)} 条")

        # 3. 通用财经/国际新闻 (对股市/数字货币影响极大)
        print("  ▶ 通用财经/国际新闻...", end=" ", flush=True)
        general_news = self.get_general_news(currency, limit=10)
        print(f"✅ {len(general_news)} 条")

        # 4. 四大新闻社RSS
        print("  ▶ 四大新闻社RSS...", end=" ", flush=True)
        major_news = []
        for source in ["bloomberg", "wsj", "cnbc", "ft"]:
            news = self.get_rss_news(source, limit=5)
            major_news.extend(news)
        print(f"✅ {len(major_news)} 条")

        # 计算各维度得分
        # Reddit情绪
        indicators = reddit_data.get("sentiment_indicators", {})
        rb = indicators.get("bullish_keywords", 0)
        rr = indicators.get("bearish_keywords", 0)
        rt = rb + rr
        reddit_score = (rb - rr) / rt if rt > 0 else 0

        # 加密货币新闻得分
        crypto_weighted = 0
        crypto_weight_sum = 0
        for item in crypto_news:
            w = item.get("weight", 0.2) * item.get("time_decay", 1.0)
            sentiment = item.get("sentiment_score", 0) if item.get("sentiment_score") is not None else (0.5 if item.get("sentiment") == "positive" else 0.3 if item.get("sentiment") == "negative" else 0)
            crypto_weighted += sentiment * w
            crypto_weight_sum += w
        crypto_score = crypto_weighted / crypto_weight_sum if crypto_weight_sum > 0 else 0

        # 通用财经/国际新闻得分 (使用相关性加权)
        general_weighted = 0
        general_weight_sum = 0
        for item in general_news:
            w = item.get("weight", 0.2)
            sentiment = item.get("sentiment_score", 0) if item.get("sentiment_score") is not None else (0.5 if item.get("sentiment") == "positive" else 0.3 if item.get("sentiment") == "negative" else 0)
            general_weighted += sentiment * w
            general_weight_sum += w
        general_score = general_weighted / general_weight_sum if general_weight_sum > 0 else 0

        # 四大新闻社得分
        major_weighted = 0
        major_weight_sum = 0
        for item in major_news:
            w = item.get("weight", 0.2) * item.get("time_decay", 1.0)
            sentiment = item.get("sentiment_score", 0) if item.get("sentiment_score") is not None else (0.5 if item.get("sentiment") == "positive" else 0.3 if item.get("sentiment") == "negative" else 0)
            major_weighted += sentiment * w
            major_weight_sum += w
        major_score = major_weighted / major_weight_sum if major_weight_sum > 0 else 0

        # 综合得分 (权重: Reddit 25%, 加密货币 20%, 通用财经 30%, 四大新闻 25%)
        combined = reddit_score * 0.25 + crypto_score * 0.20 + general_score * 0.30 + major_score * 0.25

        all_news = crypto_news + general_news + major_news

        return {
            "currency": currency,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_sentiment": "bullish" if combined > 0.3 else "bearish" if combined < -0.3 else "neutral",
            "sentiment_score": round(combined, 3),
            "breakdown": {
                "reddit_sentiment": round(reddit_score, 3),
                "crypto_news_sentiment": round(crypto_score, 3),
                "general_news_sentiment": round(general_score, 3),
                "major_news_sentiment": round(major_score, 3)
            },
            "statistics": {
                "news_total": len(all_news),
                "news_positive": sum(1 for n in all_news if n.get("sentiment") == "positive"),
                "news_negative": sum(1 for n in all_news if n.get("sentiment") == "negative"),
                "reddit_posts": reddit_data.get("posts_analyzed", 0)
            },
            "recent_headlines": [n.get("title", "") for n in all_news[:5]],
            "hot_topics": reddit_data.get("hot_topics", [])[:3],
            "general_news_sample": [n.get("title", "") for n in general_news[:3]]
        }


def get_social_sentiment(currency: str = "BTC") -> Dict:
    return SocialSentimentProvider().get_combined_sentiment(currency)

def get_news_sentiment(currency: str = "BTC") -> List[Dict]:
    """获取新闻情绪 - 使用RSS源 (修复CryptoPanic JS动态加载问题)"""
    provider = SocialSentimentProvider()
    all_news = []
    # 使用所有RSS源
    for source in provider.RSS_SOURCES.keys():
        news = provider.get_rss_news(source, limit=10)
        all_news.extend(news)
    return all_news[:20]  # 最多返回20条

def get_reddit_discussion(subreddit: str = "cryptocurrency") -> Dict:
    return SocialSentimentProvider().get_reddit_sentiment(subreddit)
