"""
AI News Aggregator v2.1
改进：
1. 外部配置（config.yaml）
2. 保存完整原始内容，确保AI能生成200-250字摘要
3. 失败重试机制
4. 更好的日志记录
"""
import requests
import feedparser
import json
import re
import os
import sqlite3
import yaml
import logging
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed

# 尝试导入可选依赖
try:
    import trafilatura
    USE_TRAFILATURA = True
except ImportError:
    USE_TRAFILATURA = False

from bs4 import BeautifulSoup
from generate_summary import generate_summary

# 默认配置
DEFAULT_CONFIG = {
    'fetch': {'max_workers': 4, 'request_timeout': 15, 'max_retries': 3, 'retry_delay': 2},
    'date_range': {'days_back': 1},
    'output': {'top_n': 10, 'save_raw_content': True, 'raw_content_length': 3000},
    'summary': {'target_min': 200, 'target_max': 250, 'generate_by': 'ai'},
    'push': {
        'openclaw': {'enabled': True, 'output_file': 'data/openclaw_message.txt', 'format': 'markdown'},
        'telegram': {'enabled': False, 'bot_token': '', 'channel_id': ''},
        'discord': {'enabled': False, 'webhook_url': ''}
    },
    'logging': {'level': 'INFO', 'file': 'data/fetch.log', 'max_size_mb': 10, 'backup_count': 5}
}

# 新闻源权重
SOURCE_WEIGHTS = {
    "量子位": 1.3, "机器之心": 1.3, "36氪": 1.3, "新智元": 1.3, 
    "智东西": 1.3, "InfoQ": 1.3,
    "雷锋网": 1.1, "钛媒体": 1.1, "AI科技评论": 1.1, "极客公园": 1.1,
    "虎嗅": 1.0,
    "TechCrunch AI": 1.2, "The Verge AI": 1.2, "MIT Tech Review": 1.2,
}

# RSS 新闻源
SOURCES = {
    "qbitai": {"name": "量子位", "rss": "https://www.qbitai.com/feed", "type": "rss"},
    "jiqizhixin": {"name": "机器之心", "rss": "https://www.jiqizhixin.com/rss", "type": "rss"},
    "infoq": {"name": "InfoQ", "rss": "https://www.infoq.cn/feed", "type": "rss"},
    "36kr": {"name": "36氪", "rss": "https://36kr.com/feed", "type": "rss"},
    "leiphone": {"name": "雷锋网", "rss": "https://www.leiphone.com/feed", "type": "rss"},
    "tmtpost": {"name": "钛媒体", "rss": "https://www.tmtpost.com/feed", "type": "rss"},
    "zhidx": {"name": "智东西", "rss": "https://www.zhidx.com/feed", "type": "rss"},
    "geekpark": {"name": "极客公园", "rss": "https://www.geekpark.net/rss", "type": "rss"},
    "huxiu": {"name": "虎嗅", "rss": "https://www.huxiu.com/rss", "type": "rss"},
    "techcrunch_ai": {"name": "TechCrunch AI", "rss": "https://techcrunch.com/category/artificial-intelligence/feed/", "type": "rss"},
    "theverge_ai": {"name": "The Verge AI", "rss": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "type": "rss"},
    "mit_tech_review": {"name": "MIT Tech Review", "rss": "https://www.technologyreview.com/feed/", "type": "rss"},
}

# AI 核心关键词
AI_KEYWORDS = [
    "AI", "人工智能", "机器学习", "深度学习", "大模型", "LLM", "神经网络", 
    "多模态", "Agent", "智能体", "AGI", "生成式AI", "AIGC", "具身智能",
    "GPT", "ChatGPT", "OpenAI", "o1", "o3", "GPT-4", "GPT-5", "Sora", "DALL-E",
    "Claude", "Anthropic", "Gemini", "Google AI", "Bard", "PaLM",
    "Llama", "Meta AI", "文心一言", "文心大模型", "通义千问", "通义", "Qwen",
    "智谱", "GLM", "ChatGLM", "月之暗面", "Kimi", "DeepSeek", "豆包", "字节AI",
    "混元", "腾讯AI", "Mistral", "Grok", "xAI", "Perplexity", "Midjourney",
    "Stable Diffusion", "Copilot", "GitHub Copilot", "人形机器人", "自动驾驶",
    "算力", "芯片", "英伟达", "NVIDIA", "GPU", "AI芯片", "H100", "H200"
]

FILTER_PATTERNS = [r'早报|晨报|晚报|日报', r'要闻提示|今日头条', r'降价|被骂|骂惨', r'游戏|电竞|手游', r'明星|娱乐|八卦']


def load_config():
    """加载配置文件"""
    config_path = 'config/config.yaml'
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    # 深度合并配置
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in config:
                            config[key].update(value)
                        else:
                            config[key] = value
        except Exception as e:
            print(f"[配置警告] 读取 config.yaml 失败: {e}, 使用默认配置")
    
    # 从环境变量读取敏感配置
    if not config['push']['telegram']['bot_token']:
        config['push']['telegram']['bot_token'] = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if not config['push']['telegram']['channel_id']:
        config['push']['telegram']['channel_id'] = os.getenv('TELEGRAM_CHANNEL_ID', '')
    if not config['push']['discord']['webhook_url']:
        config['push']['discord']['webhook_url'] = os.getenv('DISCORD_WEBHOOK_URL', '')
    
    return config


def setup_logging(config):
    """设置日志"""
    log_level = getattr(logging, config['logging']['level'].upper(), logging.INFO)
    log_file = config['logging']['file']
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


class NewsDatabase:
    """SQLite 数据库管理 - v2.1 改进版，保存原始内容"""
    
    def __init__(self, db_path='data/news.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 文章表 - 增加 raw_content 字段保存完整原始内容
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                normalized_url TEXT NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                summary TEXT,
                raw_content TEXT,           -- 新增：保存完整原始内容
                score INTEGER,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_normalized_url ON articles(normalized_url)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fetched_at ON articles(fetched_at)')
        conn.commit()
        conn.close()
    
    def exists(self, normalized_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM articles WHERE normalized_url = ?', (normalized_url,))
        result = cursor.fetchone() is not None
        conn.close()
        return result
    
    def get_article(self, normalized_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, url, title, source, summary, raw_content, score 
            FROM articles 
            WHERE normalized_url = ?
        ''', (normalized_url,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0], 'url': row[1], 'title': row[2], 'source': row[3],
                'summary': row[4], 'raw_content': row[5], 'score': row[6]
            }
        return None
    
    def save_article(self, url, normalized_url, title, source, summary, raw_content, score):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, normalized_url, title, source, summary, raw_content, score, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (url, normalized_url, title, source, summary, raw_content, score))
            article_id = cursor.lastrowid
            conn.commit()
            return article_id
        except Exception as e:
            logging.error(f"[DB] 保存失败: {e}")
            return None
        finally:
            conn.close()


class NewsDeduplicator:
    """新闻去重器"""
    
    def __init__(self, db, threshold=0.35):
        self.db = db
        self.seen_urls = set()
        self.seen_articles = []
        self.threshold = threshold
    
    def normalize_url(self, url):
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc.replace('www.', '')
            path = parsed.path.rstrip('/')
            return f"{netloc}{path}".lower()
        except:
            return url.lower()
    
    def text_similarity(self, text1, text2):
        t1 = re.sub(r'\s+', '', text1.lower())
        t2 = re.sub(r'\s+', '', text2.lower())
        if not t1 or not t2:
            return 0.0
        return SequenceMatcher(None, t1, t2).ratio()
    
    def is_duplicate(self, url, title, summary=""):
        norm_url = self.normalize_url(url)
        
        if norm_url in self.seen_urls:
            return True, None
        
        for seen_title, seen_summary in self.seen_articles:
            if self.text_similarity(title, seen_title) > self.threshold:
                return True, None
            if summary and seen_summary:
                if self.text_similarity(summary, seen_summary) > self.threshold:
                    return True, None
        
        article = self.db.get_article(norm_url)
        if article:
            return True, article
        
        self.seen_urls.add(norm_url)
        self.seen_articles.append((title, summary))
        return False, None


def fetch_with_retry(url, headers, timeout, max_retries, delay):
    """带重试的请求"""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                logging.warning(f"请求失败 ({attempt+1}/{max_retries}): {url}, 错误: {e}")
                time.sleep(delay * (attempt + 1))  # 指数退避
            else:
                logging.error(f"请求最终失败: {url}, 错误: {e}")
                raise
    return None


def fetch_article_content(url, source_name, config):
    """抓取文章正文 - 保存完整内容供AI生成摘要"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        timeout = config['fetch']['request_timeout']
        max_retries = config['fetch']['max_retries']
        delay = config['fetch']['retry_delay']
        
        # 使用 trafilatura 抓取
        if USE_TRAFILATURA:
            try:
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    text = trafilatura.extract(
                        downloaded, include_comments=False,
                        include_tables=False, no_fallback=True, target_language='zh'
                    )
                    if text and len(text) > 100:
                        return text[:config['output']['raw_content_length']]
            except Exception as e:
                logging.warning(f"[trafilatura] 抓取失败 {source_name}: {e}")
        
        # 备用：BeautifulSoup
        resp = fetch_with_retry(url, headers, timeout, max_retries, delay)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 移除无关元素
        for elem in soup(["script", "style", "nav", "header", "footer", "aside"]):
            elem.decompose()
        
        content = ""
        selectors = ['article', '.article-content', '.post-content', '.entry-content', '.content']
        
        for selector in selectors:
            container = soup.select_one(selector)
            if container:
                paragraphs = container.find_all('p')
                texts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 30 and not any(x in text for x in ['相关阅读', '版权所有', '不得转载']):
                        texts.append(text)
                if texts:
                    content = '\n'.join(texts)
                    break
        
        if not content:
            all_texts = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 50]
            content = '\n'.join(all_texts[:15])
        
        return re.sub(r'\s+', ' ', content)[:config['output']['raw_content_length']].strip()
        
    except Exception as e:
        logging.error(f"[抓取错误] {source_name}: {e}")
        return ""


def is_ai_related(title, summary="", source=""):
    """判断是否为AI相关新闻"""
    title_lower = title.lower()
    
    for pattern in FILTER_PATTERNS:
        if re.search(pattern, title):
            has_strong_ai = any(kw.lower() in title_lower for kw in AI_KEYWORDS)
            if not has_strong_ai:
                return False, 0
    
    core_matches = sum(1 for kw in AI_KEYWORDS if kw.lower() in title_lower)
    if core_matches == 0:
        return False, 0
    
    score = core_matches * 10
    weight = SOURCE_WEIGHTS.get(source, 1.0)
    score = int(score * weight)
    
    return True, score


def fetch_rss_source(source_key, source_config, deduplicator, db, config):
    """抓取 RSS 源"""
    items = []
    skipped = 0
    source_name = source_config['name']
    
    days_back = config['date_range']['days_back']
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        timeout = config['fetch']['request_timeout']
        max_retries = config['fetch']['max_retries']
        delay = config['fetch']['retry_delay']
        
        resp = fetch_with_retry(source_config['rss'], headers, timeout, max_retries, delay)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        feed = feedparser.parse(resp.content)
        
        for entry in feed.entries[:30]:
            title = entry.get('title', '').strip()
            url = entry.get('link', '')
            
            if not title or not url:
                continue
            
            # 检查时间
            published = entry.get('published_parsed') or entry.get('updated_parsed')
            if published:
                pub_date = datetime(*published[:6])
                if pub_date < cutoff_date:
                    continue
            
            rss_summary = re.sub(r'<[^>]+>', '', entry.get('summary', ''))
            
            is_dup, article = deduplicator.is_duplicate(url, title, rss_summary)
            if is_dup:
                if article:
                    items.append(article)
                    skipped += 1
                continue
            
            is_ai, score = is_ai_related(title, rss_summary, source_name)
            if not is_ai:
                continue
            
            # 抓取完整内容
            raw_content = fetch_article_content(url, source_name, config)
            
            # 保存原始内容，摘要留空（由AI后续生成）
            summary = "" if config['summary']['generate_by'] == 'ai' else raw_content[:250]
            
            norm_url = deduplicator.normalize_url(url)
            article_id = db.save_article(url, norm_url, title, source_name, summary, raw_content, score)
            
            items.append({
                'id': article_id, 'title': title, 'url': url,
                'source': source_name, 'summary': summary, 'raw_content': raw_content, 'score': score
            })
            
    except Exception as e:
        logging.error(f"[{source_name}] 抓取错误: {e}")
    
    logging.info(f"[{source_name}] 获取 {len(items)} 条, 跳过 {skipped} 条已存在")
    return items


def generate_openclaw_message(news_items, date_str):
    """生成 OpenClaw 推送消息 - 每条新闻生成 250-300 字中文摘要，英文自动翻译"""
    from translator import translate_text
    import re
    
    lines = [
        f"📰 **AI 每日新闻 - {date_str}**",
        "",
        f"共 {len(news_items)} 条精选",
        "──────────────────────────────",
        ""
    ]
    
    for i, item in enumerate(news_items, 1):
        # 翻译英文标题
        title = item['title']
        source = item['source']
        
        # 检测标题语言并翻译
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', title[:100]))
        english_words = len(re.findall(r'[a-zA-Z]+', title[:100]))
        is_english = chinese_chars * 2 < english_words
        
        if is_english:
            try:
                title = translate_text(title, 'en', 'zh')
            except Exception as e:
                print(f"标题翻译失败：{e}")
        
        lines.append(f"**{i}. [{source}] {title}**")
        lines.append("")
        
        # 生成 250-300 字中文摘要，英文自动翻译
        raw_content = item.get('raw_content', '') or item.get('summary', '')
        summary = generate_summary(item['title'], raw_content, source)
        
        lines.append(summary)
        lines.append(f"🔗 [阅读原文]({item['url']})")
        lines.append("")
    
    lines.append("──────────────────────────────")
    lines.append("🤖 AI News Aggregator | 每日更新")
    
    return '\n'.join(lines)

def main():
    """主程序"""
    # 加载配置
    config = load_config()
    
    # 设置日志
    logger = setup_logging(config)
    logger.info("="*60)
    logger.info("AI 新闻日报 v2.1 启动")
    logger.info("="*60)
    
    # 初始化
    db = NewsDatabase()
    deduplicator = NewsDeduplicator(db)
    all_news = []
    
    # 并发抓取
    logger.info(f"启动并发抓取（{config['fetch']['max_workers']} 线程）...")
    
    with ThreadPoolExecutor(max_workers=config['fetch']['max_workers']) as executor:
        futures = {
            executor.submit(fetch_rss_source, k, v, deduplicator, db, config): v['name']
            for k, v in SOURCES.items()
        }
        
        for future in as_completed(futures):
            source_name = futures[future]
            try:
                items = future.result()
                all_news.extend(items)
            except Exception as e:
                logger.error(f"[{source_name}] 处理失败: {e}")
    
    logger.info(f"总计: {len(all_news)} 条新闻")
    
    # 去重（全局）
    seen_titles = set()
    unique_news = []
    for item in all_news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
    
    logger.info(f"去重后: {len(unique_news)} 条")
    
    # 按分数排序，取前 N
    unique_news.sort(key=lambda x: x['score'], reverse=True)
    selected = unique_news[:config['output']['top_n']]
    
    logger.info(f"精选: {len(selected)} 条")
    
    # 生成日期
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y年%m月%d日')
    
    # 生成推送消息
    message = generate_openclaw_message(selected, yesterday)
    
    # 保存到文件
    os.makedirs('data', exist_ok=True)
    output_file = config['push']['openclaw']['output_file']
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    logger.info(f"推送消息已保存: {output_file}")
    logger.info("="*60)
    
    return message


if __name__ == "__main__":
    result = main()
    print(result)
