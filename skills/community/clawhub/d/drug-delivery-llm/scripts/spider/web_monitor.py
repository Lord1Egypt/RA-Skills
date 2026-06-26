import requests
import feedparser
import xml.etree.ElementTree as ET
import time
import os
import hashlib
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# === 配置区域 ===

# 1. 定义数据存储结构
# 创建专门的文件夹来存储抓取到的情报，方便 Agent 读取
DATA_DIR = "knowledge_data"
# 所有的更新都会追加到这个文件中
KNOWLEDGE_DB_PATH = os.path.join(DATA_DIR, "latest_research.txt")

# 2. 关注的 ArXiv 论文关键词 (支持布尔逻辑)
# 针对药物递送、光响应材料、量子计算和生成式 AI 的组合搜索
ARXIV_QUERIES = [
    'ti:"drug delivery" AND (AI OR "machine learning" OR "deep learning")',
    'ti:"photoresponsive" AND (material OR molecule)',
    'all:"quantum machine learning" AND chemistry',
    'all:"generative model" AND molecule'
]

# 3. 关注的 Google News 关键词
NEWS_KEYWORDS = [
    "Drug Delivery Systems", 
    "Photoresponsive Materials", 
    "AI in Drug Discovery",
    "Nanomedicine breakthroughs"
]

# 4. 配置日志输出
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebMonitor:
    def __init__(self):
        self.filepath = KNOWLEDGE_DB_PATH
        self._ensure_directory_exists()
        self.existing_hashes = self._load_existing_hashes()
        
    def _ensure_directory_exists(self):
        """确保存储目录存在"""
        if not os.path.exists(DATA_DIR):
            try:
                os.makedirs(DATA_DIR)
                logging.info(f"已创建数据目录: {DATA_DIR}")
            except OSError as e:
                logging.error(f"创建目录失败: {e}")

    def _load_existing_hashes(self):
        """加载已存在内容的哈希值，防止重复抓取"""
        hashes = set()
        if not os.path.exists(self.filepath):
            return hashes
        
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    # 识别文件中记录的 ID_HASH 标记
                    if line.startswith("ID_HASH:"):
                        hashes.add(line.strip().split(":")[1])
        except Exception as e:
            logging.error(f"读取历史记录失败: {e}")
        return hashes

    def _generate_hash(self, text):
        """生成内容的唯一指纹 (MD5)"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def fetch_arxiv_papers(self):
        """并发抓取 ArXiv 最新科研论文"""
        logging.info("正在搜索 ArXiv 最新论文...")
        base_url = "http://export.arxiv.org/api/query?"
        results = []
        
        def _fetch_single_query(query):
            try:
                # 按提交时间降序，每个关键词取最新的 3 篇
                params = f"search_query={query}&start=0&max_results=3&sortBy=submittedDate&sortOrder=desc"
                resp = requests.get(base_url + params, timeout=20)
                if resp.status_code != 200:
                    return []
                
                feed = ET.fromstring(resp.content)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = []
                
                for entry in feed.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    link = entry.find('atom:id', ns).text.strip()
                    published = entry.find('atom:published', ns).text[:10]
                    
                    # 生成唯一ID (标题+链接)
                    content_hash = self._generate_hash(title + link)
                    
                    # 只有当这是新内容时才添加
                    if content_hash not in self.existing_hashes:
                        entry_text = (
                            f"【ArXiv Paper】({published})\n"
                            f"Title: {title}\n"
                            f"Summary: {summary[:300]}...\n" # 摘要只取前300字，节省 Token
                            f"Link: {link}\n"
                            f"ID_HASH:{content_hash}\n" # 关键：写入哈希值供下次比对
                        )
                        entries.append(entry_text)
                        self.existing_hashes.add(content_hash) # 更新内存中的哈希集
                return entries
            except Exception as e:
                logging.error(f"ArXiv 查询失败 '{query}': {e}")
                return []

        # 使用线程池并发执行，提高速度
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_query = {executor.submit(_fetch_single_query, q): q for q in ARXIV_QUERIES}
            for future in as_completed(future_to_query):
                results.extend(future.result())
        
        return results

    def fetch_google_news(self):
        """抓取 Google News RSS"""
        logging.info("正在获取 Google News 实时动态...")
        new_items = []
        
        # Google News RSS 接口
        base_url = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"
        
        def _fetch_news(keyword):
            try:
                feed_url = base_url.format(keyword.replace(" ", "+"))
                feed = feedparser.parse(feed_url)
                entries = []
                
                # 每个关键词取前 2 条最新新闻
                for entry in feed.entries[:2]:
                    title = entry.title
                    link = entry.link
                    published = entry.published if 'published' in entry else datetime.now().strftime("%Y-%m-%d")
                    
                    content_hash = self._generate_hash(title)
                    
                    if content_hash not in self.existing_hashes:
                        item_text = (
                            f"【News】({published})\n"
                            f"Topic: {keyword}\n"
                            f"Title: {title}\n"
                            f"Link: {link}\n"
                            f"ID_HASH:{content_hash}\n"
                        )
                        entries.append(item_text)
                        self.existing_hashes.add(content_hash)
                return entries
            except Exception as e:
                logging.error(f"News 抓取失败 '{keyword}': {e}")
                return []

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_kw = {executor.submit(_fetch_news, kw): kw for kw in NEWS_KEYWORDS}
            for future in as_completed(future_to_kw):
                new_items.extend(future.result())
                
        return new_items

    def save_updates(self, content_list):
        """将新内容追加写入文件"""
        if not content_list:
            return 0
        
        try:
            # 使用 'a' (append) 模式追加内容
            with open(self.filepath, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"\n\n=== [情报更新] {timestamp} ===\n")
                for item in content_list:
                    f.write(item + "\n" + "-"*50 + "\n")
            return len(content_list)
        except Exception as e:
            logging.error(f"写入知识库文件失败: {e}")
            return 0

# === 供 Agent 调用的统一入口 ===
def run_monitor_update():
    """
    Agent 调用此函数来触发更新。
    它会自动检查是否有新文件夹，抓取新数据，并写入文件。
    """
    print("启动智能情报监测系统...")
    monitor = WebMonitor()
    
    # 并行执行 ArXiv 和 News 的抓取
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_arxiv = executor.submit(monitor.fetch_arxiv_papers)
        future_news = executor.submit(monitor.fetch_google_news)
        
        arxiv_updates = future_arxiv.result()
        news_updates = future_news.result()
    
    all_updates = arxiv_updates + news_updates
    
    count = monitor.save_updates(all_updates)
    
    result_msg = ""
    if count > 0:
        result_msg = f"情报更新成功：新增 {len(arxiv_updates)} 篇论文，{len(news_updates)} 条新闻。\n已写入: {KNOWLEDGE_DB_PATH}"
    else:
        result_msg = "情报监测完成：暂无最新相关内容（已过滤重复项）。"
    
    print(result_msg)
    return result_msg

if __name__ == "__main__":
    # 本地测试代码
    run_monitor_update()