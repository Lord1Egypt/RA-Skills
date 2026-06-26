#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 资讯抓取脚本 v3 - 整合用户反馈和可信度验证
- 智能重试机制
- 失败自动记录和降权
- 智能去重
- 热点排序(GPU权重最高)
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta

# 导入重试和去重模块
from smart_retry import (
    load_failure_log, save_failure_log, record_failure, 
    get_failure_count, smart_deduplicate, calculate_similarity,
    FAILURE_THRESHOLD, MAX_RETRIES
)

import requests
import websocket
import time
from bs4 import BeautifulSoup

# ========== 配置 ==========
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "sites_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "sites_config.json.default")
USER_CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "user_config.json")

CDP_HOST = "localhost"
CDP_PORT = 9222

# ========== 用户反馈模块 ==========

def load_user_config():
    """加载用户配置（优先用户配置目录）"""
    if os.path.exists(USER_CONFIG_FILE):
        try:
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 尝试读取默认配置
    DEFAULT_USER_CONFIG = os.path.join(SCRIPT_DIR, "user_config.json.default")
    if os.path.exists(DEFAULT_USER_CONFIG):
        try:
            with open(DEFAULT_USER_CONFIG, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认用户配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except:
            pass
    
    return {"user_preferences": {}, "default_keywords": {}}

def get_user_keywords():
    config = load_user_config()
    prefs = config.get("user_preferences", {})
    default_kw = config.get("default_keywords", {})
    
    all_keywords = []
    for category, kws in default_kw.items():
        all_keywords.extend(kws)
    
    custom = prefs.get("custom_keywords", [])
    liked = prefs.get("liked_keywords", [])
    excluded = prefs.get("disliked_keywords", [])
    
    final = list(set(all_keywords + custom + liked))
    return [k for k in final if k not in excluded]

def get_excluded_sources():
    config = load_user_config()
    prefs = config.get("user_preferences", {})
    return prefs.get("disliked_sources", [])

def verify_credibility(source_name, title, content):
    """验证内容可信度"""
    config = load_user_config()
    source_cred = config.get("source_credibility", {})
    
    source_info = source_cred.get(source_name, {})
    level = source_info.get("level", "C")
    level_scores = {"A": 90, "B": 70, "C": 50, "D": 30}
    score = level_scores.get(level, 50)
    
    reasons = []
    if score >= 70:
        reasons.append(f"权威来源")
    else:
        reasons.append(f"一般来源")
    
    if len(content) > 200:
        score += 10
        reasons.append("内容详细")
    
    suspicious = ["谣言", "假的", "突发", "刚刚", "震惊"]
    found = [w for w in suspicious if w in title]
    if found:
        score -= 15
        reasons.append("含敏感词")
    
    score = max(0, min(100, score))
    
    if score >= 85:
        level = "A"
    elif score >= 70:
        level = "B"
    elif score >= 50:
        level = "C"
    else:
        level = "D"
    
    return {"score": score, "level": level, "reasons": reasons}

# ========== 网站配置模块 ==========

def load_config():
    """加载网站配置（优先用户配置）"""
    # 优先读取用户配置目录
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认网站配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
            return None
    
    return None

def save_config(config):
    """保存配置到用户配置目录"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] 保存配置失败: {e}")

def update_site_status(site_key, method, status):
    config = load_config()
    if not config or 'sites' not in config:
        return
    if site_key in config['sites']:
        config['sites'][site_key]['status'][method] = status
        config['sites'][site_key]['last_test'] = datetime.now().strftime("%Y-%m-%d")
        save_config(config)

def get_best_method(config, site_key):
    if not config or site_key not in config.get('sites', {}):
        return 'chrome'
    site = config['sites'][site_key]
    priority = site.get('priority', ['chrome'])
    status = site.get('status', {})
    for method in priority:
        if status.get(method) == 'working':
            return method
    return 'chrome'

# ========== 摘要增强模块 ==========

def generate_summary_from_content(title, description, url, source):
    """生成更好的摘要"""
    summary = ""
    
    # 1. 优先使用meta描述
    if description and len(description) > 20:
        summary = description.strip()
        import re
        summary = re.sub(r'<[^>]+>', '', summary)
        summary = summary.strip()
    
    # 2. 如果没有描述，使用标题
    if not summary or len(summary) < 30:
        summary = title
    
    # 3. 清理
    import re
    summary = re.sub(r'\s+', ' ', summary)
    return summary[:350]


def extract_key_points(title, content):
    """提取关键点"""
    if not content:
        return []
    
    import re
    
    text = title + " " + content
    
    patterns = [
        r'(\d+[亿万千百])',
        r'(发布|推出|上线|公布|宣布)',
        r'(首次|首个|第一)',
        r'(增长|下降|突破|超过)',
        r'(融资|投资|收购|上市)',
        r'(新模型|新产品|新功能)',
    ]
    
    key_points = []
    sentences = re.split(r'[。！？\n\r]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 15 or len(sentence) > 150:
            continue
        
        has_number = any(p in sentence for p in ['亿', '万', '千', '%', '年', '月', '日'])
        is_important = any(re.search(p, sentence) for p in patterns)
        
        if has_number or is_important:
            if sentence not in key_points:
                key_points.append(sentence)
        
        if len(key_points) >= 4:
            break
    
    return key_points[:3]


def enhance_article(article):
    """增强单篇文章的摘要"""
    title = article.get('title', '')
    url = article.get('url', '')
    source = article.get('source', '')
    original_summary = article.get('summary', '')
    
    # 生成更好的摘要
    better_summary = generate_summary_from_content(
        title, 
        original_summary, 
        url, 
        source
    )
    
    # 提取关键点
    key_points = extract_key_points(title, original_summary)
    
    article['summary'] = better_summary
    article['key_points'] = key_points
    
    return article


# ========== 抓取方法 ==========

def fetch_via_rss(url, source_name):
    results = []
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        resp = session.get(url, timeout=20)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'xml')
        items = soup.find_all('item')
        for item in items[:20]:
            title = item.find('title')
            link = item.find('link')
            desc = item.find('description')
            title_text = title.get_text(strip=True) if title else ""
            link_text = link.get_text(strip=True) if link else ""
            if len(title_text) > 8:
                results.append({
                    'title': title_text[:150],
                    'url': link_text[:300] if link_text else '',
                    'source': source_name,
                    'method': 'rss'
                })
    except:
        pass
    return results

def fetch_via_http(url, source_name):
    results = []
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        resp = session.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for s in soup(['script', 'style']):
            s.decompose()
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a.get('href', '')
            if 10 < len(text) < 100:
                if href.startswith('//'):
                    href = 'https:' + href
                elif href.startswith('/'):
                    try:
                        base = '/'.join(url.split('/')[:3])
                        href = base + href
                    except:
                        continue
                elif not href.startswith('http'):
                    continue
                if href.startswith('http') and len(href) < 300:
                    results.append({
                        'title': text[:150],
                        'url': href,
                        'source': source_name,
                        'method': 'http'
                    })
    except:
        pass
    return results

def fetch_via_chrome(ws, url, source_name):
    results = []
    try:
        msg = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}})
        ws.send(msg)
        time.sleep(3)
        script = """
        (function() {
            var links = document.querySelectorAll('a[href]');
            var data = [];
            for (var i = 0; i < links.length; i++) {
                var t = links[i].innerText.trim();
                var h = links[i].href;
                if (t.length > 10 && t.length < 100 && h && h.startsWith('http')) {
                    data.push({title: t, url: h});
                }
            }
            return JSON.stringify(data.slice(0, 30));
        })();
        """
        msg = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": script}})
        ws.send(msg)
        try:
            response = ws.recv()
            data = json.loads(response)
            if 'result' in data and 'result' in data.get('result', {}):
                content = data['result']['result']['value']
                links = json.loads(content)
                for link in links:
                    results.append({
                        'title': link.get('title', '')[:150],
                        'url': link.get('url', '')[:300],
                        'source': source_name,
                        'method': 'chrome'
                    })
        except:
            pass
    except:
        pass
    return results

def fetch_article_chrome(ws, url, retry_count=0, max_retries=2):
    """
    获取文章摘要 - 智能提取文章正文
    带重试机制，如果获取内容 < 30字，会换方式重新获取
    """
    try:
        msg = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}})
        ws.send(msg)
        time.sleep(2)
        
        # 智能提取文章正文的脚本
        script = """
        (function() {
            // 1. 先尝试获取 meta description
            var metaDesc = '';
            var metaDescEl = document.querySelector('meta[name="description"]') 
                          || document.querySelector('meta[property="og:description"]');
            if (metaDescEl) {
                metaDesc = metaDescEl.content || '';
            }
            
            // 2. 智能查找文章正文区域
            var articleText = '';
            
            // 优先查找常见的文章内容容器
            var selectors = [
                'article', 
                'main', 
                '[role="main"]',
                '.article-content',
                '.article-body', 
                '.post-content',
                '.post-body',
                '.content-body',
                '.entry-content',
                '.article-text',
                '.news-content',
                '.detail-content',
                '#article',
                '#content',
                '#main-content',
                '.main-text'
            ];
            
            for (var i = 0; i < selectors.length; i++) {
                var el = document.querySelector(selectors[i]);
                if (el) {
                    articleText = el.innerText || '';
                    if (articleText.length > 100) break;
                }
            }
            
            // 3. 如果没找到合适的容器，尝试从 body 中提取
            if (!articleText || articleText.length < 100) {
                var body = document.body;
                // 移除脚本、样式、导航、页脚等噪音元素
                var noiseTags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript'];
                noiseTags.forEach(function(tag) {
                    var elements = body.querySelectorAll(tag);
                    elements.forEach(function(e) { e.remove(); });
                });
                
                // 移除常见的噪音类名
                var noiseClasses = ['nav', 'menu', 'sidebar', 'footer', 'header', 'advertisement', 
                                    'ad-', 'comment', 'share', 'social', 'related', 'recommend',
                                    'copyright', 'breadcrumb', 'pagination', 'toolbar'];
                noiseClasses.forEach(function(cls) {
                    var elements = body.querySelectorAll('[class*="' + cls + '"]');
                    elements.forEach(function(e) { e.remove(); });
                });
                
                articleText = body.innerText || '';
            }
            
            // 4. 清理文本
            articleText = articleText.replace(/\\s+/g, ' ').trim();
            
            // 5. 选择最佳内容
            var bestContent = '';
            if (metaDesc && metaDesc.length > 20) {
                bestContent = metaDesc;
            }
            if (!bestContent || (articleText.length > bestContent.length && articleText.length > 50)) {
                bestContent = articleText;
            }
            
            return JSON.stringify({
                text: bestContent.substring(0, 3000),
                desc: metaDesc,
                hasContent: bestContent.length > 50
            });
        })();
        """
        
        msg = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": script}})
        ws.send(msg)
        try:
            response = ws.recv()
            data = json.loads(response)
            if 'result' in data:
                content = json.loads(data['result']['result']['value'])
                text = content.get('text', '')
                desc = content.get('desc', '')
                has_content = content.get('hasContent', False)
                
                # 检查是否有有效内容
                raw_text = text.strip() if text else ''
                desc_text = desc.strip() if desc else ''
                
                # 选择更长的内容
                best_content = desc_text if len(desc_text) > len(raw_text) else raw_text
                best_content = ' '.join(best_content.split())  # 清理空白
                
                # 如果内容 < 30字，且还有重试次数，返回需要重新获取的标记
                if len(best_content) < 30 and retry_count < max_retries:
                    return "NEED_RETRY"  # 标记需要重试
                elif len(best_content) < 30:
                    return "获取摘要失败"  # 重试次数用完
                
                # 截取到合适长度
                return best_content[:350] if best_content else "暂无摘要"
        except Exception as e:
            print(f"    [DEBUG] 解析内容出错: {e}")
            pass
    except Exception as e:
        print(f"    [DEBUG] 获取摘要出错: {e}")
        pass
    
    return "获取摘要失败"

# ========== Chrome 连接 ==========

def get_or_start_chrome():
    try:
        resp = requests.get(f"http://{CDP_HOST}:{CDP_PORT}/json/list", timeout=5)
        pages = resp.json()
        for p in pages:
            if p['type'] == 'page':
                return p
    except:
        pass
    if sys.platform == 'win32':
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        user_data = os.path.expanduser(r"~\AppData\Local\Temp\openclaw-chrome")
    else:
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data = "/tmp/openclaw-chrome"
    os.makedirs(user_data, exist_ok=True)
    import subprocess
    subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={CDP_PORT}",
        "--remote-allow-origins=*",
        "--no-first-run",
        f"--user-data-dir={user_data}"
    ], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    for _ in range(10):
        time.sleep(1)
        try:
            resp = requests.get(f"http://{CDP_HOST}:{CDP_PORT}/json/list", timeout=5)
            pages = resp.json()
            for p in pages:
                if p['type'] == 'page':
                    return p
        except:
            continue
    raise Exception("无法启动 Chrome")

def cdp_connect(ws_url):
    ws = websocket.WebSocket()
    ws.settimeout(20)
    ws.connect(ws_url)
    return ws

# ========== 供外部调用的函数 ==========

def fetch_all_news(days=1, min_credibility='D', min_score=0):
    """
    供 auto_run.py 调用的主函数
    返回: articles 列表
    """
    yesterday = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    print(f"正在抓取 {yesterday} 的 AI/算力/GPU 资讯...")
    print(f"可信度要求: >= {min_credibility}, 分数 >= {min_score}")
    
    # 获取用户关键词
    user_keywords = get_user_keywords()
    excluded_sources = get_excluded_sources()
    print(f"关键词数量: {len(user_keywords)}")
    print(f"排除来源: {excluded_sources if excluded_sources else '无'}")
    
    config = load_config()
    
    print("正在连接 Chrome...")
    page_info = get_or_start_chrome()
    chrome_ws = cdp_connect(page_info['webSocketDebuggerUrl'])
    print(f"已连接")
    
    all_results = []
    
    if config:
        for site_key, site in config.get('sites', {}).items():
            name = site.get('name', site_key)
            
            if excluded_sources and any(s in name for s in excluded_sources):
                print(f"\n[{name}] 已排除，跳过")
                continue
            
            best_method = get_best_method(config, site_key)
            print(f"\n[{name}] 使用 {best_method} 方式")
            
            results = []
            url = site.get(best_method, site.get('url'))
            
            if not url:
                continue
            
            try:
                if best_method == 'rss':
                    results = fetch_via_rss(url, name)
                elif best_method == 'http':
                    results = fetch_via_http(url, name)
                elif best_method == 'chrome':
                    results = fetch_via_chrome(chrome_ws, url, name)
                
                if results:
                    update_site_status(site_key, best_method, 'working')
            except:
                update_site_status(site_key, best_method, 'failed')
            
            for r in results:
                title_lower = r['title'].lower()
                if any(kw in title_lower for kw in user_keywords):
                    cred = verify_credibility(r['source'], r['title'], r.get('summary', ''))
                    r['credibility'] = cred
                    all_results.append(r)
            
            print(f"  -> 找到 {len([r for r in results if any(kw in r['title'].lower() for kw in user_keywords)])} 条")
    
    chrome_ws.close()
    
    # 去重
    seen = set()
    unique_results = []
    for r in all_results:
        key = r['title'][:25]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    # 智能去重
    print("\n正在进行智能去重...")
    from smart_retry import smart_deduplicate
    unique_results = smart_deduplicate(unique_results, similarity_threshold=0.6)
    
    # 热点排序
    print("\n正在进行热点排序...")
    keyword_weights = {
        'gpu': 15, 'nvidia': 15, 'amd': 15, 'cuda': 15,
        'h100': 15, 'h200': 15, 'a100': 15, 'b100': 15,
        '4090': 15, '5080': 15, '5090': 15, 'blackwell': 15, 'rubin': 15,
        '显卡': 15, '显存': 12, 'RTX': 15, 'geforce': 15,
        '内存': 15, 'ddr5': 15, 'ddr4': 15, 'ddr6': 15,
        'hbm': 15, 'hbm3': 15, 'hbm3e': 15, 'gddr': 15,
        'dram': 15, 'sram': 12, 'rom': 8,
        '存储': 10, '固态': 10, 'ssd': 10, '硬盘': 8,
        '三星': 10, '海力士': 10, '美光': 10, 'sk hynix': 15,
        '颗粒': 10, '芯片颗粒': 15,
        'ai': 10, '人工智能': 10, '大模型': 12, 'llm': 12,
        'gpt': 10, 'chatgpt': 10, 'openai': 10,
        'claude': 10, 'gemini': 10, 'deepseek': 10,
        '模型': 8, '训练': 8, '推理': 8, 'moE': 10,
        '算力': 10, '芯片': 10, '半导体': 10, '处理器': 8,
        'cpu': 8, 'npu': 10, 'tpu': 10, '华为': 8, '昇腾': 10,
        '阿里': 8, '百度': 8, '腾讯': 8, '字节': 8,
        '自动驾驶': 8, '智驾': 8, '特斯拉': 8, 'fsd': 8,
    }
    
    def calc_hot_score(article):
        score = 0
        title = article.get('title', '').lower()
        cred = article.get('credibility', {})
        level = cred.get('level', 'D')
        
        for kw, w in keyword_weights.items():
            if kw in title:
                score += w
        
        if level == 'A':
            score += 10
        elif level == 'B':
            score += 8
        
        if len(article.get('summary', '')) > 100:
            score += 3
        
        if len(article.get('key_points', [])) > 2:
            score += 2
        
        return score
    
    for r in unique_results:
        r['hot_score'] = calc_hot_score(r)
    
    unique_results.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
    
    print("\n🔥 TOP 5 热点资讯:")
    for i, r in enumerate(unique_results[:5], 1):
        print(f"  {i}. [{r.get('hot_score', 0)}分] {r['title'][:40]}...")
    
    print(f"\n共抓取 {len(unique_results)} 条资讯 (按热度排序)")
    
    # 获取摘要 - 带重试和备用方案
    print("正在获取文章摘要...")
    page_info = get_or_start_chrome()
    chrome_ws = cdp_connect(page_info['webSocketDebuggerUrl'])
    
    # 添加 HTTP 备用获取函数
    def fetch_article_http(url):
        """通过 HTTP 直接请求获取文章摘要"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            resp = session.get(url, timeout=15)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 移除噪音元素
            for s in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                s.decompose()
            
            # 查找文章正文
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and ('content' in x or 'article' in x or 'post' in x))
            
            if article:
                text = article.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())  # 清理空白
                return text[:500] if text else ""
            
            # 如果没找到，返回 body 文本
            body = soup.find('body')
            if body:
                text = body.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                return text[:500] if text else ""
                
        except Exception as e:
            print(f"      [HTTP备用] 获取失败: {e}")
        return ""
    
    final_results = []
    failed_urls = []
    
    for i, r in enumerate(unique_results[:15]):
        print(f"  处理 {i+1}/15: {r['source']} - {r['title'][:30]}...")
        
        # 第一次尝试 - Chrome
        summary = fetch_article_chrome(chrome_ws, r['url'], retry_count=0, max_retries=2)
        
        # 如果失败，进行重试（最多2次）
        retry_count = 0
        while summary == "NEED_RETRY" and retry_count < 2:
            retry_count += 1
            print(f"      重试 {retry_count}/2...")
            time.sleep(1)
            summary = fetch_article_chrome(chrome_ws, r['url'], retry_count=retry_count, max_retries=2)
        
        # 如果仍然失败，尝试 HTTP 备用方案
        if summary == "获取摘要失败" or summary == "NEED_RETRY":
            print(f"      [备用] 尝试HTTP方式...")
            summary = fetch_article_http(r['url'])
            if not summary:
                summary = "获取摘要失败"
                failed_urls.append(r['url'])
        
        r['summary'] = summary[:400]
        
        key_points = extract_key_points(r['title'], summary)
        r['key_points'] = key_points
        
        cred = verify_credibility(r['source'], r['title'], summary)
        r['credibility'] = cred
        
        final_results.append(r)
        
        # 每次处理后稍作休息，避免被限流
        time.sleep(0.5)
    
    chrome_ws.close()
    
    # 打印失败列表
    if failed_urls:
        print(f"\n⚠️  有 {len(failed_urls)} 篇文章获取失败:")
        for url in failed_urls[:5]:
            print(f"    - {url[:60]}...")
    
    level_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for r in final_results:
        lv = r.get('credibility', {}).get('level', 'D')
        level_counts[lv] = level_counts.get(lv, 0) + 1
    
    print(f"\n可信度分布: A级={level_counts['A']}, B级={level_counts['B']}, C级={level_counts['C']}, D级={level_counts['D']}")
    
    return final_results


# ========== 主函数（CLI用） ==========

def main():
    import argparse
    parser = argparse.ArgumentParser(description='AI资讯抓取 v3')
    parser.add_argument('--days', type=int, default=1)
    parser.add_argument('--min-credibility', default='D', choices=['A', 'B', 'C', 'D'])
    parser.add_argument('--min-score', type=int, default=0)
    args = parser.parse_args()
    
    yesterday = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    print(f"正在抓取 {yesterday} 的 AI/算力/GPU 资讯...")
    print(f"可信度要求: >= {args.min_credibility}, 分数 >= {args.min_score}")
    
    # 获取用户关键词
    user_keywords = get_user_keywords()
    excluded_sources = get_excluded_sources()
    print(f"关键词数量: {len(user_keywords)}")
    print(f"排除来源: {excluded_sources if excluded_sources else '无'}")
    
    config = load_config()
    needs_chrome = True
    
    print("正在连接 Chrome...")
    page_info = get_or_start_chrome()
    chrome_ws = cdp_connect(page_info['webSocketDebuggerUrl'])
    print(f"已连接")
    
    all_results = []
    
    if config:
        for site_key, site in config.get('sites', {}).items():
            name = site.get('name', site_key)
            
            # 跳过排除的来源
            if excluded_sources and any(s in name for s in excluded_sources):
                print(f"\n[{name}] 已排除，跳过")
                continue
            
            best_method = get_best_method(config, site_key)
            print(f"\n[{name}] 使用 {best_method} 方式")
            
            results = []
            url = site.get(best_method, site.get('url'))
            
            if not url:
                continue
            
            try:
                if best_method == 'rss':
                    results = fetch_via_rss(url, name)
                elif best_method == 'http':
                    results = fetch_via_http(url, name)
                elif best_method == 'chrome':
                    results = fetch_via_chrome(chrome_ws, url, name)
                
                if results:
                    update_site_status(site_key, best_method, 'working')
                else:
                    update_site_status(site_key, best_method, 'failed')
            except:
                update_site_status(site_key, best_method, 'failed')
            
            # 过滤关键词
            for r in results:
                title_lower = r['title'].lower()
                if any(kw in title_lower for kw in user_keywords):
                    # 验证可信度
                    cred = verify_credibility(r['source'], r['title'], r.get('summary', ''))
                    r['credibility'] = cred
                    all_results.append(r)
            
            print(f"  -> 找到 {len([r for r in results if any(kw in r['title'].lower() for kw in user_keywords)])} 条")
    
    chrome_ws.close()
    
    # 去重
    seen = set()
    unique_results = []
    for r in all_results:
        key = r['title'][:25]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    # ===== 智能去重 (新增) =====
    print("\n正在进行智能去重...")
    unique_results = smart_deduplicate(unique_results, similarity_threshold=0.6)
    
    # ===== 热点排序 =====
    print("\n正在进行热点排序...")
    
    # 关键词热度权重（数字越大越热）
    keyword_weights = {
        # GPU/显卡 - 最高权重
        'gpu': 15, 'nvidia': 15, 'amd': 15, 'cuda': 15,
        'h100': 15, 'h200': 15, 'a100': 15, 'b100': 15,
        '4090': 15, '5080': 15, '5090': 15, 'blackwell': 15, 'rubin': 15,
        '显卡': 15, '显存': 12, 'RTX': 15, 'geforce': 15,
        
        # 内存 - 最高权重 (新增)
        '内存': 15, 'ddr5': 15, 'ddr4': 15, 'ddr6': 15,
        'hbm': 15, 'hbm3': 15, 'hbm3e': 15, 'gddr': 15,
        'dram': 15, 'sram': 12, 'rom': 8,
        '存储': 10, '固态': 10, 'ssd': 10, '硬盘': 8,
        '三星': 10, '海力士': 10, '美光': 10, 'sk hynix': 15,
        '颗粒': 10, '芯片颗粒': 15,
        
        # AI/大模型 - 次高权重
        'ai': 10, '人工智能': 10, '大模型': 12, 'llm': 12,
        'gpt': 10, 'chatgpt': 10, 'openai': 10,
        'claude': 10, 'gemini': 10, 'deepseek': 10,
        '模型': 8, '训练': 8, '推理': 8, 'moE': 10,
        
        # 芯片/算力
        '算力': 10, '芯片': 10, '半导体': 10, '处理器': 8,
        'cpu': 8, 'npu': 10, 'tpu': 10, '华为': 8, '昇腾': 10,
        
        # 自动驾驶
        '自动驾驶': 8, '智驾': 8, '特斯拉': 8, 'fsd': 8,
        
        # 新鲜度权重（最近24小时内的）
        '今天': 5, '昨日': 4, '刚刚': 5, '最新': 5,
    }
    
    def calculate_hot_score(article):
        """计算热点分数"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        text = title + ' ' + summary
        
        score = 0
        
        # 1. 关键词热度得分
        for kw, weight in keyword_weights.items():
            if kw in text:
                score += weight
        
        # 2. 来源可信度得分
        level = article.get('credibility', {}).get('level', 'D')
        level_scores = {'A': 10, 'B': 8, 'C': 5, 'D': 2}
        score += level_scores.get(level, 0)
        
        # 3. 内容详细度加分
        if len(article.get('summary', '')) > 100:
            score += 3
        
        # 4. 关键点数量加分
        key_points = article.get('key_points', [])
        if len(key_points) >= 2:
            score += 2
        
        return score
    
    # 计算每篇文章的热度分数
    for r in unique_results:
        r['hot_score'] = calculate_hot_score(r)
    
    # 按热度分数排序
    unique_results.sort(key=lambda x: x.get('hot_score', 0), reverse=True)
    
    # 显示热度排名
    print("热度TOP 5:")
    for i, r in enumerate(unique_results[:5], 1):
        print(f"  {i}. [{r.get('hot_score', 0)}分] {r['title'][:40]}...")
    
    # 原来的可信度排序已替换为热度排序
    # level_order = {"A": 4, "B": 3, "C": 2, "D": 1}
    # unique_results.sort(key=lambda x: (level_order.get(x.get('credibility', {}).get('level', 'D'), 0), x.get('credibility', {}).get('score', 0)), reverse=True)
    
    print(f"\n共抓取 {len(unique_results)} 条资讯 (按热度排序)")
    
    # 获取摘要
    print("正在获取文章摘要...")
    # 添加 HTTP 备用获取函数
    def fetch_article_http(url):
        """通过 HTTP 直接请求获取文章摘要"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            resp = session.get(url, timeout=15)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 移除噪音元素
            for s in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                s.decompose()
            
            # 查找文章正文
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and ('content' in x or 'article' in x or 'post' in x))
            
            if article:
                text = article.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                return text[:500] if text else ""
            
            body = soup.find('body')
            if body:
                text = body.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                return text[:500] if text else ""
                
        except Exception as e:
            print(f"      [HTTP备用] 获取失败: {e}")
        return ""
    
    page_info = get_or_start_chrome()
    chrome_ws = cdp_connect(page_info['webSocketDebuggerUrl'])
    
    final_results = []
    failed_urls = []
    
    for i, r in enumerate(unique_results[:15]):
        print(f"  处理 {i+1}/15: {r['source']} - {r['title'][:30]}...")
        
        # 第一次尝试 - Chrome
        summary = fetch_article_chrome(chrome_ws, r['url'], retry_count=0, max_retries=2)
        
        # 如果失败，进行重试（最多2次）
        retry_count = 0
        while summary == "NEED_RETRY" and retry_count < 2:
            retry_count += 1
            print(f"      重试 {retry_count}/2...")
            time.sleep(1)
            summary = fetch_article_chrome(chrome_ws, r['url'], retry_count=retry_count, max_retries=2)
        
        # 如果仍然失败，尝试 HTTP 备用方案
        if summary == "获取摘要失败" or summary == "NEED_RETRY":
            print(f"      [备用] 尝试HTTP方式...")
            summary = fetch_article_http(r['url'])
            if not summary:
                summary = "获取摘要失败"
                failed_urls.append(r['url'])
        
        r['summary'] = summary[:400]
        
        # 增强摘要 - 提取关键点
        key_points = extract_key_points(r['title'], summary)
        r['key_points'] = key_points
        
        # 重新验证可信度
        cred = verify_credibility(r['source'], r['title'], summary)
        r['credibility'] = cred
        
        final_results.append(r)
        
        # 每次处理后稍作休息
        time.sleep(0.5)
    
    chrome_ws.close()
    
    # 打印失败列表
    if failed_urls:
        print(f"\n⚠️  有 {len(failed_urls)} 篇文章获取失败:")
        for url in failed_urls[:5]:
            print(f"    - {url[:60]}...")
    
    # 统计可信度分布
    level_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for r in final_results:
        lv = r.get('credibility', {}).get('level', 'D')
        level_counts[lv] = level_counts.get(lv, 0) + 1
    
    print(f"\n可信度分布: A级={level_counts['A']}, B级={level_counts['B']}, C级={level_counts['C']}, D级={level_counts['D']}")
    
    # 输出
    output = {
        "query_date": datetime.now().strftime("%Y-%m-%d"),
        "date_range": yesterday,
        "total": len(final_results),
        "credibility_stats": level_counts,
        "results": final_results
    }
    
    print("\n" + "="*60)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()