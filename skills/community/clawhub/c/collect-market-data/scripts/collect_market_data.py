# -*- coding: utf-8 -*-
"""
采集全球金融市场数据 - Step 1: 市场表现类 + 经济数据类
覆盖：美国、中国、中国香港、欧洲、亚太（日本、韩国）

优化要点：
1. 每个数据类别配置 3 个稳定数据源，按优先级自动轮询
2. 自动重试(2~3次) + 超时控制(5~20s) + 随机延迟(0.5~2.5s)防封拦截
3. 宽松文本解析，不写死 XPath，兼容页面改版
4. 动态渲染(Selenium) + 等待元素加载，支持 JS 页面数据采集
"""
import sys
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo")
sys.stdout.reconfigure(encoding='utf-8')
import os, json, datetime, time, logging, random, re, threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import config

# ── 全局日期工具 ──────────────────────────────────────────────
def _data_date_en():
    """将 config.DATA_DATE（如 '2026年5月12日'）转换为 'May 12, 2026' 格式，供搜索 query 使用。"""
    try:
        # DATA_DATE 格式示例："2026年5月12日"
        d = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日")
        return d.strftime("%B %d, %Y")   # e.g. "May 12, 2026"
    except Exception:
        return "recent market data"       # 兜底，避免查询写死日期

DATA_DATE_EN = _data_date_en()   # 模块级缓存，避免重复解析

def _data_month_en():
    """将 config.DATA_DATE 转换为 'May 2026' 格式，用于月度数据搜索。"""
    try:
        d = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日")
        return d.strftime("%B %Y")   # e.g. "May 2026"
    except Exception:
        return datetime.datetime.now().strftime("%B %Y")

DATA_MONTH_EN = _data_month_en()

def _data_date_cn():
    """返回中文日期 '2026年5月12日'。"""
    return config.DATA_DATE  # 格式本身即是 "2026年5月12日"

def _data_date_cn_md():
    """返回"月日"部分，如 '5月12日'，用于假期查询。"""
    try:
        d = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日")
        return f"{d.month}月{d.day}日"
    except Exception:
        return "5月12日"

DATA_DATE_CN = _data_date_cn()
DATA_DATE_CN_MD = _data_date_cn_md()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ])
log = logging.getLogger(__name__)

log.info(f"📅 报告日期: {config.REPORT_DATE}  数据截止: {config.DATA_DATE}")
log.info(f"📁 输出目录: {config.OUTPUT_DIR}")

# ─────────────────────────────────────────────
# 全局状态
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# 全局状态
# ─────────────────────────────────────────────
market_data = {}

def init_data_structure():
    return {
        '_meta': {
            'report_date': config.REPORT_DATE,
            'data_date': config.DATA_DATE,
            'collection_time': datetime.datetime.now().isoformat(),
            'supplement_time': None,
            'sources': {},
            'completed_categories': []   # 已完成且无需重采的类别
        },
        '市场表现': {},
        '经济数据': {},
        '政策动态': {},
        '企业动态': {},
        '环球市场速览': {}
    }

market_data = init_data_structure()

# ─────────────────────────────────────────────
# Checkpoint 加载/保存
# ─────────────────────────────────────────────
def _checkpoint_load():
    """
    启动时加载已有 checkpoint：
    - 如果今日文件已存在且完整，加载后跳过已完成的类别
    - 如果文件损坏或数据异常，降级为全新采集
    """
    fpath = config.MARKET_DATA_FILE
    if not os.path.exists(fpath):
        log.info("  [Checkpoint] 无历史文件，进行全新采集")
        return False

    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            saved = json.load(f)

        # 验证数据有效性
        if not saved or not isinstance(saved, dict):
            log.warning("  [Checkpoint] 文件内容异常，进行全新采集")
            return False

        data_date = saved.get('_meta', {}).get('data_date', '')
        if data_date != config.DATA_DATE:
            log.info(f"  [Checkpoint] 文件日期({data_date}) ≠ 今日({config.DATA_DATE})，进行全新采集")
            return False

        # 检查已完成的类别
        completed = saved.get('_meta', {}).get('completed_categories', [])
        log.info(f"  [Checkpoint] 发现历史数据，今日已采集类别: {completed}")
        if completed:
            log.info(f"  [Checkpoint] 将跳过 {len(completed)} 个已完成类别，实现断点续采")

        # 合并已有数据（保留 market_data 的初始结构）
        for top_key in ['市场表现', '经济数据', '政策动态', '企业动态', '环球市场速览']:
            if top_key in saved and isinstance(saved[top_key], dict):
                market_data[top_key].update(saved.get(top_key, {}))

        # 恢复 _meta（保留已完成类别记录）
        if '_meta' in saved:
            for k, v in saved['_meta'].items():
                if k != 'collection_time':   # 更新时间戳
                    market_data['_meta'][k] = v

        log.info(f"  [Checkpoint] 历史数据加载成功，共 {len(completed)} 个类别已采集")
        return True

    except json.JSONDecodeError as e:
        log.warning(f"  [Checkpoint] JSON 解析失败 ({e})，进行全新采集")
        return False
    except Exception as e:
        log.warning(f"  [Checkpoint] 加载失败 ({e})，进行全新采集")
        return False


def _checkpoint_save():
    """每完成一个任务立即保存 checkpoint，防止中途崩溃丢失数据"""
    try:
        os.makedirs(os.path.dirname(config.MARKET_DATA_FILE), exist_ok=True)
        # 保存前更新采集时间
        market_data['_meta']['collection_time'] = datetime.datetime.now().isoformat()
        with open(config.MARKET_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(market_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log.warning(f"  [Checkpoint] 保存失败: {e}")
        return False


# 启动时尝试加载 checkpoint
_checkpoint_load()

# ─────────────────────────────────────────────
# 工具函数：通用 HTTP 客户端
# ─────────────────────────────────────────────
class HttpClient:
    """带自动重试、随机延迟、超时控制的 HTTP 客户端"""

    def __init__(self):
        self.session = None  # 后续可扩展为 session 复用
        self.default_headers = {
            "User-Agent": config.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
        }

    def get(self, url, headers=None, timeout=15, retry=3,
            delay_range=(0.5, 2.5), error_word=None, encoding=None):
        """
        发送 GET 请求，自动重试 + 随机延迟
        :param url: 目标 URL
        :param headers: 额外请求头
        :param timeout: 超时秒数
        :param retry: 重试次数（含首次，即最多 retry+1 次）
        :param delay_range: 随机延迟范围 (min_s, max_s)
        :param error_word: 如果响应包含此关键词视为失败（非 200）
        :param encoding: 响应编码（可选）
        :return: requests.Response 或 None
        """
        import requests
        merged_headers = {**self.default_headers, **(headers or {})}
        for attempt in range(retry + 1):
            try:
                sleep_time = random.uniform(*delay_range)
                time.sleep(sleep_time)
                r = requests.get(url, headers=merged_headers, timeout=timeout)
                if r.status_code != 200:
                    log.warning(f"  [{url[:60]}] HTTP {r.status_code}，重试 {attempt+1}/{retry+1}")
                    continue
                if error_word and error_word in r.text[:200]:
                    log.warning(f"  [{url[:60]}] 含错误标识，重试 {attempt+1}/{retry+1}")
                    continue
                if encoding:
                    r.encoding = encoding
                return r
            except Exception as e:
                log.warning(f"  [{url[:60]}] {type(e).__name__}: {e}，重试 {attempt+1}/{retry+1}")
                if attempt < retry:
                    time.sleep(random.uniform(*delay_range))
        return None

http = HttpClient()


# ─────────────────────────────────────────────
# 工具函数：Selenium 动态渲染
# ─────────────────────────────────────────────
_selenium_driver = None

def get_selenium_driver():
    """懒加载 Selenium WebDriver（仅当需要动态渲染时）"""
    global _selenium_driver
    if _selenium_driver is None:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By

            opts = Options()
            opts.add_argument("--headless=new")
            opts.add_argument("--disable-images")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--disable-gpu")
            # 静默模式
            opts.add_argument("--log-level=3")
            prefs = {"profile.managed_default_content_settings.images": 2}
            opts.add_experimental_option("prefs", prefs)

            _selenium_driver = webdriver.Chrome(options=opts)
            log.info("  [Selenium] Chrome WebDriver 已初始化（动态渲染模式）")
        except Exception as e:
            log.warning(f"  [Selenium] 初始化失败: {e}，动态渲染将不可用")
            _selenium_driver = False  # False = 初始化失败
    return _selenium_driver if _selenium_driver else None

def fetch_with_selenium(url, wait_for="body", timeout=15, delay=2):
    """
    使用 Selenium 获取动态渲染页面
    :param url: 目标 URL
    :param wait_for: 等待元素出现的 CSS 选择器
    :param timeout: 总超时秒数
    :param delay: 加载后额外等待秒数
    :return: HTML 字符串 或 None
    """
    # 确保 Selenium 已初始化并导入需要的类
    driver = get_selenium_driver()
    if not driver:
        return None
    
    # 导入需要的类（如果尚未导入）
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
    except ImportError as e:
        log.warning(f"  [Selenium] 导入失败: {e}")
        return None
        
    try:
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(5)
        driver.get(url)
        # 等待指定元素出现
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_for))
        )
        time.sleep(delay)  # 额外等待 JS 渲染
        return driver.page_source
    except Exception as e:
        log.warning(f"  [Selenium] 获取失败 {url[:60]}: {e}")
        return None


# ─────────────────────────────────────────────
# 工具函数：宽松文本解析
# ─────────────────────────────────────────────
def extract_number(text, patterns=None):
    """从文本中宽松提取数字，支持多种格式"""
    if patterns is None:
        patterns = [
            r"([+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?)",   # 12,345.67
            r"([+-]?\d+\.\d+)",                         # 123.45
            r"([+-]?\d+)",                              # 12345
        ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            s = m.group(1).replace(",", "")
            try:
                return float(s)
            except:
                pass
    return None

def extract_pct(text):
    """从文本中提取涨跌幅百分比"""
    patterns = [
        r"([+-]?\d+\.?\d*)\s*%",
        r"涨跌\s*([+-]?\d+\.?\d*)",
        r"收?跌?\s*([+-]?\d+\.?\d*)\s*%",
        r"[（(]([+-]?\d+\.?\d*)\s*%[)）]",
        r"变化\s*([+-]?\d+\.?\d*)\s*基点",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            try:
                return round(float(m.group(1).replace(",", "")), 2)
            except:
                pass
    return None

def extract_text_block(html, keywords, max_chars=2000):
    """在 HTML 中根据关键词找文本块，宽松匹配"""
    if isinstance(keywords, str):
        keywords = [keywords]
    # 去掉 HTML 标签后全文搜索
    clean = re.sub(r"<[^>]+>", " ", html)
    clean = re.sub(r"\s+", " ", clean)
    for kw in keywords:
        idx = clean.find(kw)
        if idx >= 0:
            start = max(0, idx - 100)
            end = min(len(clean), idx + max_chars)
            return clean[start:end]
    return ""


# ─────────────────────────────────────────────
# 工具函数：WebSearch Fallback 兜底
# ─────────────────────────────────────────────
class WebSearchFallback:
    """当 API 数据源全部失败时，通过 Web Search 补充数据的工具"""

    def __init__(self):
        self.enabled = True
        self.search_count = 0
        self.max_per_category = 3  # 每类最多搜索3次

    def search(self, query, max_results=5, retries=2, delay_range=(1.0, 3.0)):
        """三引擎搜索：Tavily → Bocha → DuckDuckGo，带重试+随机延迟，下游无感知"""
        import os, requests, time, random

        def _do_search(search_fn, engine_name):
            """单引擎搜索，带重试+随机延迟"""
            for attempt in range(retries + 1):
                try:
                    time.sleep(random.uniform(*delay_range))
                    result = search_fn()
                    if result:
                        return result
                    if attempt < retries:
                        log.warning(f"  [WebSearch][{engine_name}] 第{attempt+1}次失败，重试...")
                except Exception as e:
                    err_str = str(e).lower()
                    if attempt < retries:
                        log.warning(f"  [WebSearch][{engine_name}] 异常: {e}，重试 {attempt+1}/{retries}...")
                    else:
                        log.warning(f"  [WebSearch][{engine_name}] 最终失败: {e}")
            return None

        # ── 引擎1: Tavily ──
        def _tavily_fn():
            from tavily import TavilyClient
            client = TavilyClient()
            result = client.search(query=query, max_results=max_results, search_depth="advanced")
            return result.get("results", [])

        # ── 引擎2: Bocha ──
        def _bocha_fn():
            api_key = os.getenv('BOCHA_API_KEY')
            if not api_key:
                return None
            headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
            payload = {'query': query, 'freshness': 'noLimit', 'summary': True, 'count': max_results}
            resp = requests.post('https://api.bocha.cn/v1/web-search', headers=headers, json=payload, timeout=15)
            if resp.status_code != 200:
                return None
            data = resp.json()
            results = data.get('data', {}).get('webPages', {}).get('value', [])
            return [{'content': r.get('summary', '') or r.get('snippet', ''),
                     'snippet': r.get('snippet', ''),
                     'source': r.get('siteName', ''),
                     'title': r.get('name', ''),
                     'url': r.get('url', '')}
                    for r in results]

        # ── 引擎3: DuckDuckGo ──
        def _ddg_fn():
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                return [{'content': r.get('body', ''),
                         'snippet': r.get('body', ''),
                         'source': r.get('source', ''),
                         'title': r.get('title', ''),
                         'url': r.get('href', '')}
                        for r in results]

        # 尝试顺序: Tavily → Bocha → DuckDuckGo
        for engine_name, fn in [('Tavily', _tavily_fn), ('Bocha', _bocha_fn), ('DuckDuckGo', _ddg_fn)]:
            result = _do_search(fn, engine_name)
            if result is not None and result != []:
                self.search_count += 1
                # Bocha/DDG 需映射字段
                if engine_name == 'Tavily':
                    log.info(f"  [WebSearch] Tavily 搜索成功，{len(result)}条")
                    return result
                elif engine_name == 'Bocha':
                    log.info(f"  [WebSearch] Bocha 搜索成功，{len(result)}条")
                    return result
                else:
                    log.info(f"  [WebSearch] DuckDuckGo 搜索成功，{len(result)}条")
                    return result

        log.warning(f"  [WebSearch] 三个搜索引擎均失败")
        return []

    def extract_price(self, results, patterns=None):
        """从搜索结果文本中宽松提取价格"""
        text = " ".join([r.get("content", "") or r.get("snippet", "") for r in results])
        return extract_number(text, patterns)

    def extract_pct(self, results):
        """从搜索结果文本中宽松提取涨跌幅"""
        text = " ".join([r.get("content", "") or r.get("snippet", "") for r in results])
        return extract_pct(text)

ws_fallback = WebSearchFallback()


# ─────────────────────────────────────────────
# 工具函数：线程超时包装器
# ─────────────────────────────────────────────
def run_with_timeout(func, timeout_sec=20, default=None, name=None):
    """在独立线程中运行函数，带超时控制"""
    result = [default]
    error = [None]

    def target():
        try:
            result[0] = func()
        except Exception as e:
            error[0] = e
            log.error(f"    [{name or func.__name__}] 异常: {e}")

    t = threading.Thread(target=target)
    t.daemon = True
    t.start()
    t.join(timeout_sec)
    if t.is_alive():
        log.warning(f"    [{name or func.__name__}] 超时({timeout_sec}s)")
        return default
    if error[0]:
        log.error(f"    [{name or func.__name__}] 异常: {error[0]}")
    return result[0]


# ─────────────────────────────────────────────
# 工具函数：TickDB API
# ─────────────────────────────────────────────
def get_tickdb_key():
    try:
        r = http.get('https://tickdb.ai/api/public/claw-keys', timeout=10, retry=2, delay_range=(0.5, 1.5))
        if r and r.status_code == 200:
            return r.json().get('apiKey')
    except Exception as e:
        log.warning(f"  TickDB Key 获取失败: {e}")
    return None

def query_tickdb(symbols, timeout=15):
    """批量查询 TickDB，返回 {symbol: data}。增强日志：每次调用均记录请求结果。"""
    key = get_tickdb_key()
    if not key:
        log.warning(f"  ⚠️ TickDB 查询跳过: apiKey 为空 (symbols={symbols})")
        return {}
    try:
        url = f'https://api.tickdb.ai/v1/market/ticker?symbols={symbols}'
        r = http.get(url, headers={'X-API-Key': key}, timeout=timeout, retry=2, delay_range=(0.5, 1.5))
        if r is None:
            log.warning(f"  ⚠️ TickDB 查询返回 None: symbols={symbols}")
            return {}
        if r.status_code == 200:
            result = {}
            data_list = r.json().get('data', [])
            for d in data_list:
                result[d['symbol']] = d
            log.info(f"  ✅ TickDB 查询成功: symbols={symbols}, 返回 {len(result)} 条, keys={list(result.keys())}")
            return result
        else:
            log.warning(f"  ⚠️ TickDB 响应异常: status={r.status_code}, body={r.text[:200]}")
            return {}
    except Exception as e:
        log.warning(f"  ⚠️ TickDB 查询异常: {e}")
    return {}

def query_tickdb_kline(symbol, interval="1d", limit=5):
    """查询 TickDB K线数据（用于获取历史价格计算涨跌幅）"""
    key = get_tickdb_key()
    if not key:
        return None
    try:
        url = f'https://api.tickdb.ai/v1/market/kline?symbol={symbol}&interval={interval}&limit={limit}'
        r = http.get(url, headers={'X-API-Key': key}, timeout=15, retry=2, delay_range=(0.5, 1.5))
        if r and r.status_code == 200:
            data = r.json()
            if data.get('code') == 0:
                return data.get('data', {})
    except Exception as e:
        log.warning(f"  TickDB K线查询失败 [{symbol}]: {e}")
    return None


# ─────────────────────────────────────────────
# 工具函数：akshare 封装（带超时）
# ─────────────────────────────────────────────
def akshare_call(func, *args, timeout=25, **kwargs):
    """安全调用 akshare 函数，带超时控制"""
    def _call():
        import akshare as ak
        return func(*args, **kwargs)
    return run_with_timeout(_call, timeout_sec=timeout, name=func.__name__)


# ═══════════════════════════════════════════════════════════════
# 【美国股市】三大数据源：TickDB → akshare(新浪美股) → Yahoo Finance
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【美国股市】采集中...")
log.info("=" * 60)

def fetch_us_stocks():
    """美股三大指数 + VIX：三源轮询容错"""
    us_data = {}

    # ── 源1: Sina 直接API（最稳定，三大指数全可用）
    sina_map = {
        'int_sp500': '标普500指数',
        'int_nasdaq': '纳斯达克综合指数',
        'int_dji': '道琼斯工业平均指数',
    }
    for code, name in sina_map.items():
        try:
            r = http.get(
                f'https://hq.sinajs.cn/list={code}',
                headers={'Referer': 'https://finance.sina.com.cn'},
                timeout=8, retry=2, encoding='gbk'
            )
            if r and r.status_code == 200 and f'hq_str_{code}="'.encode('gbk') in r.text.encode('gbk'):
                # 格式: "名称,价格,涨跌额,涨跌幅"
                key = f'hq_str_{code}="'
                text = r.text
                if key in text:
                    parts = text.split(key)[1].split('"')[0].split(',')
                    if len(parts) >= 4:
                        try:
                            price = float(parts[1])
                            chg_str = parts[3].replace('%', '')
                            chg = float(chg_str) if chg_str.replace('.', '').replace('-', '').isdigit() else 0
                            if price > 1000:
                                us_data[name] = {'price': round(price, 2), 'change': round(chg, 2), 'source': 'Sina财经'}
                                log.info(f"  ✅ {name}(Sina): {price:.2f} ({chg:+.2f}%)")
                        except Exception:
                            pass
        except Exception as e:
            log.warning(f"  ⚠️ {name} Sina 失败: {e}")

    # ── 源2: TickDB（VIX 备用，以及三大指数的补充）
    tb = query_tickdb('VIX', timeout=10)
    if 'VIX' in tb and 'VIX恐慌指数' not in us_data:
        item = tb['VIX']
        p = float(item['last_price'])
        c = float(item.get('price_change_percent_24h', 0) or 0)
        if p > 0:
            us_data['VIX恐慌指数'] = {'price': round(p, 2), 'change': round(c, 2), 'source': 'TickDB'}
            log.info(f"  ✅ VIX恐慌指数(TickDB): {p:.2f} ({c:+.2f}%)")

    # ── 源3: Web Search（VIX 兜底）
    if 'VIX恐慌指数' not in us_data:
        results = ws_fallback.search(f'CBOE VIX volatility index price today {DATA_DATE_EN}')
        price = ws_fallback.extract_price(results)
        if price and 5 < price < 100:
            us_data['VIX恐慌指数'] = {'price': round(price, 2), 'change': 0, 'source': 'Web Search'}
            log.info(f"  ✅ VIX恐慌指数(WS): {price:.2f}")
        time.sleep(0.5)

    market_data['市场表现']['美国股市'] = us_data
    src_list = sorted(set(v.get('source', '') for v in us_data.values()))
    market_data['_meta']['sources']['美股'] = ' + '.join(src_list) if src_list else 'N/A'
    log.info(f"  📊 美国股市采集结果: {list(us_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【美国债券与外汇】三数据源：TradingEconomics → FRED API → Yahoo Finance
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【美国债券与外汇】采集中...")
log.info("=" * 60)

def fetch_us_bonds_forex():
    """美债与外汇：5个稳定数据源 → 必须保证每个指标都能采到"""
    bonds_data = {}

    # ── 源1: TradingEconomics 直接HTTP（无需Selenium，比之前快很多）
    te_map = [
        ('10年期美债收益率', 'united-states/10-year-bond-yield', 1, 8),  # (1-8% is valid range)
        ('2年期美债收益率', 'united-states/2-year-bond-yield', 0.5, 8),
        ('美元指数(DXY)', 'united-states/ice-dollar-index', 90, 110),
    ]
    for name, path, lo, hi in te_map:
        try:
            r = http.get(
                f'https://tradingeconomics.com/{path}',
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=12, retry=2
            )
            if r and r.status_code == 200:
                import re
                html = r.text
                # 找包含"United States"的行
                pattern = r'<tr[^>]*>.*?United[^<]*?</tr>'
                rows = re.findall(pattern, html, re.DOTALL)
                for row in rows:
                    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                    if len(tds) >= 3:
                        texts = [re.sub(r'<[^>]+>', '', t).strip() for t in tds if t.strip()]
                        if len(texts) >= 2:
                            price = extract_number(texts[1])
                            pct_chg = extract_pct(texts[2] if len(texts) > 2 else '')
                            if price and lo < price < hi:
                                bonds_data[name] = {
                                    'price': round(price, 4),
                                    'change': pct_chg if pct_chg else 0,
                                    'unit': '%',
                                    'source': 'TradingEconomics'
                                }
                                log.info(f"  ✅ {name}(TE): {price:.4f}%")
                                break
        except Exception as e:
            log.warning(f"  ⚠️ {name} TE 失败: {e}")

    # ── 源2: FRED API（最稳定的数据源）
    fred_map = [
        ('DGS10', '10年期美债收益率'),
        ('DGS2', '2年期美债收益率'),
        ('DTBEXD', '美元指数(DXY)'),  # trade weighted dollar index
    ]
    for series_id, name in fred_map:
        if name in bonds_data:
            continue
        try:
            # vintage_date 需要是 YYYY-MM-DD 格式，用 DATA_DATE 解析
            _dv = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日").strftime("%Y-%m-%d")
            r = http.get(
                f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&vintage_date={_dv}&limit=3',
                timeout=18, retry=2, delay_range=(0.5, 1.5)
            )
            if r and r.status_code == 200:
                lines = r.text.strip().split('\n')
                if len(lines) >= 2:
                    vals = [l.split(',')[-1].strip() for l in lines[-2:]]
                    vals = [v for v in vals if v not in ('.', 'N/A', '')]
                    if len(vals) >= 1:
                        p = float(vals[0])
                        if p > 0:
                            bonds_data[name] = {
                                'price': round(p, 4),
                                'change': 0,
                                'unit': '%',
                                'source': 'FRED'
                            }
                            log.info(f"  ✅ {name}(FRED): {p:.4f}%")
        except Exception as e:
            log.warning(f"  ⚠️ {name} FRED 失败: {e}")

    # ── 源3: Sina 外汇（已验证可用的数据源）
    sina_forex_map = [
        ('USD/CNY', 'USDT'),
        ('EUR/USD', 'EUR'),
        ('GBP/USD', 'GBP'),
        ('AUD/USD', 'AUD'),
    ]
    for name, code in sina_forex_map:
        if name in bonds_data:
            continue
        r = http.get(
            f'https://hq.sinajs.cn/list={code}',
            headers={'Referer': 'https://finance.sina.com.cn'},
            timeout=8, retry=2, encoding='gbk'
        )
        if r and r.status_code == 200:
            key = f'hq_str_{code}="'
            if key in r.text:
                parts = r.text.split(key)[1].split('"')[0].split(',')
                if len(parts) > 1:
                    try:
                        price = float(parts[1])
                        valid_ranges = {'USD/CNY': (6.0, 8.0), 'EUR/USD': (1.0, 1.5), 'GBP/USD': (1.0, 1.5), 'AUD/USD': (0.5, 1.0)}
                        lo, hi = valid_ranges.get(name, (0, 999))
                        if lo < price < hi:
                            bonds_data[name] = {'price': round(price, 4), 'change': 0, 'unit': '', 'source': 'Sina FX'}
                            log.info(f"  ✅ {name}(Sina): {price:.4f}")
                    except:
                        pass

    # ── 源5: Web Search（每个指标都必须搜到）
    bonds_queries = {
        '10年期美债收益率': f'US 10-year Treasury yield interest rate {DATA_DATE_EN}',
        '2年期美债收益率': f'US 2-year Treasury yield interest rate {DATA_DATE_EN}',
        '美元指数(DXY)': f'US Dollar Index DXY value {DATA_DATE_EN}',
    }
    for name, query in bonds_queries.items():
        if name in bonds_data:
            continue
        results = ws_fallback.search(query)
        price = ws_fallback.extract_price(results)
        pct = ws_fallback.extract_pct(results)
        if price:
            valid_ranges = {'10年期美债收益率': (1, 10), '2年期美债收益率': (0.5, 8), '美元指数(DXY)': (90, 120)}
            lo, hi = valid_ranges.get(name, (0, 999))
            if lo < price < hi:
                bonds_data[name] = {'price': round(price, 4), 'change': pct if pct else 0, 'unit': '%', 'source': 'Web Search'}
                log.info(f"  ✅ {name}(WS): {price:.4f}% ({pct:+.2f}%)" if pct else f"  ✅ {name}(WS): {price:.4f}%")
        time.sleep(0.5)

    market_data['市场表现']['美国债券与外汇'] = bonds_data
    src_list = set(v.get('source', '') for v in bonds_data.values())
    market_data['_meta']['sources']['美债/美元指数'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 美债/美元采集结果: {list(bonds_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【大宗商品】2个稳定数据源：TickDB现货 + Web Search（专注COMEX黄金）
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【大宗商品】采集中...")
log.info("=" * 60)

def fetch_us_commodities():
    """COMEX黄金：2个稳定数据源 → TickDB现货 + Web Search"""
    commodities_data = {}

    # ── 源1: TickDB XAUUSD（现货=期货，视为COMEX黄金基准，最可靠）
    tb = query_tickdb('XAUUSD', timeout=10)
    if 'XAUUSD' in tb:
        item = tb['XAUUSD']
        p = float(item['last_price'])
        c = float(item.get('price_change_percent_24h', 0) or 0)
        if p > 800:
            commodities_data['COMEX黄金期货'] = {
                'price': round(p, 2),
                'change': round(c, 2),
                'unit': 'USD/盎司',
                'source': 'TickDB(现货)'
            }
            log.info(f"  ✅ COMEX黄金期货(TB-XAUUSD): ${p:.2f} ({c:+.2f}%)")

    # ── 源2: Web Search（每个品种都必须搜到）
    ws_map = {
        'WTI原油期货': f'WTI crude oil price per barrel today {DATA_DATE_EN}',
        'COMEX黄金期货': f'COMEX gold futures price per ounce {DATA_DATE_EN}',
    }
    for name, query in ws_map.items():
        if name in commodities_data:
            continue
        results = ws_fallback.search(query)
        price = ws_fallback.extract_price(results)
        pct = ws_fallback.extract_pct(results)
        valid_ranges = {'WTI原油期货': (30, 200), 'COMEX黄金期货': (800, 3000)}
        lo, hi = valid_ranges.get(name, (0, 999999))
        unit = 'USD/桶' if '原油' in name else 'USD/盎司'
        if price and lo < price < hi:
            commodities_data[name] = {'price': round(price, 2), 'change': pct if pct else 0, 'unit': unit, 'source': 'Web Search'}
            log.info(f"  ✅ {name}(WS): ${price:.2f} ({pct:+.2f}%)" if pct else f"  ✅ {name}(WS): ${price:.2f}")
        else:
            # 兜底搜索
            results2 = ws_fallback.search(f"gold price ounce {name} {DATA_DATE_EN}")
            price2 = ws_fallback.extract_price(results2)
            if price2 and lo < price2 < hi:
                commodities_data[name] = {'price': round(price2, 2), 'change': 0, 'unit': unit, 'source': 'Web Search'}
                log.info(f"  ✅ {name}(WS): ${price2:.2f}")
        time.sleep(0.5)

    # ── 源3: akshare futures_global_spot_em（工业金属：铜、铝）
    try:
        import akshare as ak
        df = ak.futures_global_spot_em()
        if df is not None and len(df) > 0:
            metal_map = {
                'LME铜': ['铜', '综合铜'],
                'LME铝': ['铝', '综合铝'],
            }
            found = {name: False for name in metal_map}
            for _, row in df.iterrows():
                name_val = str(row.get('名称', ''))
                for display_name, keywords in metal_map.items():
                    if found[display_name] or display_name in commodities_data:
                        continue
                    if any(kw in name_val for kw in keywords):
                        p = float(row.get('最新价', 0) or 0)
                        chg_str = str(row.get('涨跌幅', '0')).replace('%', '')
                        chg = float(chg_str) if chg_str.replace('.', '').replace('-', '').isdigit() else 0
                        valid_ranges = {'LME铜': (3000, 20000), 'LME铝': (1500, 6000)}
                        lo, hi = valid_ranges.get(display_name, (0, 999999))
                        if lo < p < hi:
                            commodities_data[display_name] = {
                                'price': round(p, 2),
                                'change': chg,
                                'unit': 'USD/吨',
                                'source': 'akshare大宗商品'
                            }
                            log.info(f"  ✅ {display_name}(akshare): ${p:.2f} ({chg:+.2f}%)")
                            found[display_name] = True
                            break
    except Exception as e:
        log.warning(f"  ⚠️ 工业金属 akshare 失败: {e}")

    market_data['市场表现']['美国大宗商品'] = commodities_data
    src_list = set(v.get('source', '') for v in commodities_data.values())
    market_data['_meta']['sources']['美国大宗商品'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 大宗商品采集结果: {list(commodities_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【A股】三数据源：akshare → Sina → Tencent
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【A股】采集中...")
log.info("=" * 60)

def fetch_a_shares():
    cn_data = {}

    # ── 源1: akshare ──
    symbol_map = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000300', '沪深300'),
        ('sh000688', '科创50'),
    ]
    for sym, name in symbol_map:
        def _fetch_a_share(sym=sym, name=name):
            import akshare as ak
            df = ak.stock_zh_index_daily(symbol=sym)
            if len(df) > 0:
                p = float(df.iloc[-1]['close'])
                y = float(df.iloc[-2]['close'])
                c = round((p - y) / y * 100, 2)
                cn_data[name] = {'price': round(p, 2), 'change': c, 'source': 'akshare'}
                log.info(f"  ✅ {name}(akshare): {p:.2f} ({c:+.2f}%)")
        try:
            run_with_timeout(_fetch_a_share, timeout_sec=20, name=f"akshare_{name}")
        except Exception as e:
            log.warning(f"  ⚠️ {name} akshare 失败: {e}")

    # ── 源2: Sina A股 ──
    sina_a_map = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
    ]
    for sym, name in sina_a_map:
        if name in cn_data:
            continue
        r = http.get(
            f'https://hq.sinajs.cn/list={sym}',
            headers={'Referer': 'https://finance.sina.com.cn'},
            timeout=10, retry=2, encoding='gbk'
        )
        if r and r.status_code == 200:
            text = r.text
            key = f'hq_str_{sym}="'
            if key in text:
                parts = text.split(key)[1].split('"')[0].split(',')
                if len(parts) > 5:
                    try:
                        price = float(parts[3])
                        yest = float(parts[2])
                        chg = round((price - yest) / yest * 100, 2)
                        cn_data[name] = {'price': round(price, 2), 'change': chg, 'source': 'Sina A股'}
                        log.info(f"  ✅ {name}(Sina): {price:.2f} ({chg:+.2f}%)")
                    except Exception as e:
                        log.warning(f"  ⚠️ {name} Sina 解析失败: {e}")

    # ── 源3: Tencent A股行情 ──
    tencent_a_map = [
        ('rt_hkHSI', '上证指数'),
        ('rt_hkHSTECH', '创业板指'),
    ]
    for key, name in tencent_a_map:
        if name in cn_data:
            continue
        r = http.get(
            'https://qt.gtimg.cn/q=sz399001,sh000001,sz399006',
            headers={'Referer': 'https://gu.qq.com'},
            timeout=10, retry=2, encoding='gbk'
        )
        if r and r.status_code == 200:
            text = r.text
            for sym2, name2 in [('sz399001', '深证成指'), ('sh000001', '上证指数'), ('sz399006', '创业板指')]:
                if name2 in cn_data:
                    continue
                k = f'qt_{sym2}="'
                if k in text:
                    parts = text.split(k)[1].split('"')[0].split('~')
                    if len(parts) > 5:
                        try:
                            price = float(parts[3])
                            yest = float(parts[4])
                            chg = round((price - yest) / yest * 100, 2)
                            cn_data[name2] = {'price': round(price, 2), 'change': chg, 'source': 'Tencent A股'}
                            log.info(f"  ✅ {name2}(Tencent): {price:.2f} ({chg:+.2f}%)")
                        except:
                            pass

    market_data['市场表现']['A股'] = cn_data
    src_list = set(v.get('source', '') for v in cn_data.values())
    market_data['_meta']['sources']['A股'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 A股采集结果: {list(cn_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【港股】三数据源：Tencent QT → TickDB → Sina
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【港股】采集中...")
log.info("=" * 60)

def fetch_hk_stocks():
    hk_data = {}

    # ── 源1: Tencent QT ──
    r = http.get(
        'https://qt.gtimg.cn/q=r_hkHSI,r_hkHSTECH',
        headers={'Referer': 'https://gu.qq.com'},
        timeout=10, retry=2, encoding='gbk'
    )
    if r and r.status_code == 200:
        text = r.text
        qt_map = [('r_hkHSI', '恒生指数'), ('r_hkHSTECH', '恒生科技指数')]
        for key, name in qt_map:
            if key in text:
                parts = text.split(f'{key}="')[1].split('"')[0].split('~')
                if len(parts) > 5:
                    try:
                        price = float(parts[3])
                        yest = float(parts[4])
                        chg = round((price - yest) / yest * 100, 2)
                        hk_data[name] = {'price': round(price, 2), 'change': chg, 'source': 'Tencent QT'}
                        log.info(f"  ✅ {name}(Tencent): {price:.2f} ({chg:+.2f}%)")
                    except Exception as e:
                        log.warning(f"  ⚠️ {name} Tencent 解析失败: {e}")

    # ── 源2: TickDB ──
    tb = query_tickdb('HSI', timeout=15)
    if 'HSI' in tb:
        item = tb['HSI']
        p = float(item['last_price'])
        c = float(item.get('price_change_percent_24h', 0) or 0)
        if p > 0 and '恒生指数' not in hk_data:
            hk_data['恒生指数'] = {'price': round(p, 2), 'change': round(c, 2), 'source': 'TickDB'}
            log.info(f"  ✅ 恒生指数(TB): {p:.2f} ({c:+.2f}%)")

    # ── 源3: Sina 港股 ──
    if '恒生指数' not in hk_data or '恒生科技指数' not in hk_data:
        r = http.get(
            'https://hq.sinajs.cn/list=rt_hkHSI,rt_hkHSTECH',
            headers={'Referer': 'https://finance.sina.com.cn'},
            timeout=10, retry=2, encoding='gbk'
        )
        if r and r.status_code == 200:
            text = r.text
            sina_hk_map = [('rt_hkHSI', '恒生指数'), ('rt_hkHSTECH', '恒生科技指数')]
            for key, name in sina_hk_map:
                if name in hk_data:
                    continue
                k = f'hq_str_{key}="'
                if k in text:
                    parts = text.split(k)[1].split('"')[0].split(',')
                    if len(parts) > 5:
                        try:
                            price = float(parts[1])
                            yest = float(parts[2]) if len(parts) > 2 else price
                            chg = round((price - yest) / yest * 100, 2) if yest else 0
                            hk_data[name] = {'price': round(price, 2), 'change': chg, 'source': 'Sina 港股'}
                            log.info(f"  ✅ {name}(Sina): {price:.2f} ({chg:+.2f}%)")
                        except:
                            pass

    # ── 源4: akshare index_global_spot_em（国企指数）
    try:
        import akshare as ak
        df = ak.index_global_spot_em()
        if df is not None and len(df) > 0:
            for _, row in df.iterrows():
                name_val = str(row.get('名称', ''))
                if '国企指数' in name_val and '国企指数' not in hk_data:
                    p = float(row.get('最新价', 0) or 0)
                    chg_str = str(row.get('涨跌幅', '0')).replace('%', '')
                    chg = float(chg_str) if chg_str.replace('.', '').replace('-', '').isdigit() else 0
                    if p > 1000:
                        hk_data['国企指数'] = {'price': round(p, 2), 'change': chg, 'source': 'akshare全球股指'}
                        log.info(f"  ✅ 国企指数(akshare): {p:.2f} ({chg:+.2f}%)")
                        break
    except Exception as e:
        log.warning(f"  ⚠️ 国企指数 akshare 失败: {e}")

    market_data['市场表现']['港股'] = hk_data
    src_list = set(v.get('source', '') for v in hk_data.values())
    market_data['_meta']['sources']['港股'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 港股采集结果: {list(hk_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【欧洲股市】三数据源：akshare全球股指(index_global_spot_em) → Web Search(Bocha) → TickDB(STOXX50E)
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【欧洲股市】采集中...")
log.info("=" * 60)

def fetch_eu_stocks():
    """欧洲股市：5个稳定数据源 → 必须保证每个指数都能采到"""
    eu_data = {}

    # ── 源1: akshare index_global_spot_em（全球股指，包含 DAX/CAC40/FTSE）
    try:
        import akshare as ak
        df = ak.index_global_spot_em()
        if df is not None and len(df) > 0:
            eu_search = {
                '德国DAX 30': ['DAX', '德国DAX'],
                '法国CAC 40': ['CAC40', '法国CAC'],
                '英国富时100': ['FTSE', '富时100'],
            }
            found = {name: False for name in eu_search}
            for _, row in df.iterrows():
                name_val = str(row.get('名称', ''))
                for idx_name, kws in eu_search.items():
                    if found[idx_name] or idx_name in eu_data:
                        continue
                    if any(kw in name_val for kw in kws):
                        p = float(row.get('最新价', 0) or 0)
                        chg_str = str(row.get('涨跌幅', '0')).replace('%', '')
                        try:
                            chg = float(chg_str)
                        except:
                            chg = 0
                        if p > 1000:
                            eu_data[idx_name] = {'price': round(p, 2), 'change': chg, 'source': 'akshare全球股指'}
                            log.info(f"  ✅ {idx_name}(akshare): {p:.2f} ({chg:+.2f}%)")
                            found[idx_name] = True
                            break
    except Exception as e:
        log.warning(f"  ⚠️ akshare 全球股指失败: {e}")

    # ── 源2: Web Search（每个指数都必须搜到）
    eu_queries = {
        '德国DAX 30': f'German DAX 30 index close price {DATA_DATE_EN}',
        '法国CAC 40': f'France CAC 40 index close price {DATA_DATE_EN}',
        '英国富时100': f'UK FTSE 100 index close price {DATA_DATE_EN}',
    }
    for name, query in eu_queries.items():
        if name in eu_data:
            continue
        results = ws_fallback.search(query)
        price = ws_fallback.extract_price(results)
        pct = ws_fallback.extract_pct(results)
        if price and 1000 < price < 60000:
            eu_data[name] = {'price': round(price, 2), 'change': pct if pct else 0, 'source': 'Web Search'}
            log.info(f"  ✅ {name}(WS): {price:.2f} ({pct:+.2f}%)" if pct else f"  ✅ {name}(WS): {price:.2f}")
        else:
            results2 = ws_fallback.search(f"{name} stock market today price")
            price2 = ws_fallback.extract_price(results2)
            if price2 and 1000 < price2 < 60000:
                eu_data[name] = {'price': round(price2, 2), 'change': 0, 'source': 'Web Search'}
                log.info(f"  ✅ {name}(WS): {price2:.2f}")
        time.sleep(0.5)

    # ── 源3: TickDB（欧洲斯托克600）
    if '欧洲斯托克600' not in eu_data:
        tb = query_tickdb('STOXX50E', timeout=8)
        if 'STOXX50E' in tb:
            item = tb['STOXX50E']
            p = float(item['last_price'])
            c = float(item.get('price_change_percent_24h', 0) or 0)
            if p > 0:
                eu_data['欧洲斯托克600'] = {'price': round(p, 2), 'change': round(c, 2), 'source': 'TickDB'}
                log.info(f"  ✅ 欧洲斯托克600(TB): {p:.2f} ({c:+.2f}%)")

    market_data['市场表现']['欧洲股市'] = eu_data
    src_list = set(v.get('source', '') for v in eu_data.values())
    market_data['_meta']['sources']['欧洲股市'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 欧洲股市采集结果: {list(eu_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【亚太股市】四数据源：akshare全球股指(index_global_spot_em) → TickDB(日经) → Sina → Web Search(Bocha)
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【亚太股市】采集中...")
log.info("=" * 60)

def fetch_apac_stocks():
    """亚太股市：4个稳定数据源 → Web Search + akshare + TickDB + Sina"""
    apac_data = {}

    # ── 源1: Web Search（每个指数都必须搜到，最可靠）
    apac_queries = {
        '日经225指数': f'Japan Nikkei 225 index close price {DATA_DATE_EN}',
        '韩国综合指数': f'South Korea KOSPI index close price {DATA_DATE_EN}',
        '澳洲S&P/ASX 200': f'Australia ASX 200 index close price {DATA_DATE_EN}',
    }
    for name, query in apac_queries.items():
        if name in apac_data:
            continue
        results = ws_fallback.search(query)
        price = ws_fallback.extract_price(results)
        pct = ws_fallback.extract_pct(results)
        valid_ranges = {'日经225指数': (5000, 60000), '韩国综合指数': (500, 10000), '澳洲S&P/ASX 200': (2000, 20000)}
        lo, hi = valid_ranges.get(name, (0, 999999))
        if price and lo < price < hi:
            apac_data[name] = {'price': round(price, 2), 'change': pct if pct else 0, 'source': 'Web Search'}
            log.info(f"  ✅ {name}(WS): {price:.2f} ({pct:+.2f}%)" if pct else f"  ✅ {name}(WS): {price:.2f}")
        else:
            results2 = ws_fallback.search(f"{name} stock market today price")
            price2 = ws_fallback.extract_price(results2)
            if price2 and lo < price2 < hi:
                apac_data[name] = {'price': round(price2, 2), 'change': 0, 'source': 'Web Search'}
                log.info(f"  ✅ {name}(WS): {price2:.2f}")
        time.sleep(0.5)

    # ── 源2: akshare index_global_spot_em（亚太股指，包含日经/KOSPI/ASX）
    try:
        import akshare as ak
        df_all = ak.index_global_spot_em()
        if df_all is not None and len(df_all) > 0:
            apac_search = {
                '日经225指数': ['日经225', 'Nikkei 225', 'Nikkei225', 'Nikkei'],
                '韩国综合指数': ['韩国KOSPI', 'KOSPI', '韩国综合'],
                '澳洲S&P/ASX 200': ['澳大利亚标普200', 'ASX200', '澳洲200', 'S&P/ASX'],
            }
            found = {name: False for name in apac_search}
            valid_ranges = {'日经225指数': (5000, 70000), '韩国综合指数': (500, 10000), '澳洲S&P/ASX 200': (2000, 20000)}
            _debug_rows = []   # 调试：记录所有行供日志输出
            for _, row in df_all.iterrows():
                name_val = str(row.get('名称', ''))
                _debug_rows.append(name_val)
                for idx_name, kws in apac_search.items():
                    if found[idx_name] or idx_name in apac_data:
                        continue
                    if any(kw.lower() in name_val.lower() for kw in kws):
                        p = float(row.get('最新价', 0) or 0)
                        chg_str = str(row.get('涨跌幅', '0')).replace('%', '')
                        chg = float(chg_str) if chg_str.replace('.', '').replace('-', '').isdigit() else 0
                        lo, hi = valid_ranges.get(idx_name, (0, 999999))
                        if lo < p < hi:
                            apac_data[idx_name] = {'price': round(p, 2), 'change': chg, 'source': 'akshare全球股指'}
                            log.info(f"  ✅ {idx_name}(akshare): {p:.2f} ({chg:+.2f}%)  [匹配关键词: {kws}, 行名称: '{name_val}']")
                            found[idx_name] = True
                            break
            # 调试：若某指数仍未采集到，输出所有行名供参考
            for idx_name, kws in apac_search.items():
                if not found[idx_name] and idx_name not in apac_data:
                    log.warning(f"  ⚠️ akshare 未匹配到 {idx_name}，所有行名称: {_debug_rows[:30]}")
    except Exception as e:
        log.warning(f"  ⚠️ akshare 亚太股指失败: {e}")

    # ── 源3: TickDB（日经225）
    tb = query_tickdb('NK225', timeout=8)
    if 'NK225' in tb:
        item = tb['NK225']
        p = float(item.get('last_price') or 0)
        c = float(item.get('price_change_percent_24h') or 0)
        log.info(f"  🔍 TickDB NK225 返回: price={p}, change={c}%, item_keys={list(item.keys())}")
        if p > 0 and '日经225指数' not in apac_data:
            apac_data['日经225指数'] = {'price': round(p, 2), 'change': round(c, 2), 'source': 'TickDB'}
            log.info(f"  ✅ 日经225指数(TB): {p:.2f} ({c:+.2f}%)")
        elif p <= 0:
            log.warning(f"  ⚠️ TickDB NK225 price 无效: {p}，跳过写入")
    else:
        log.warning(f"  ⚠️ TickDB 未返回 NK225 数据。TickDB 返回内容: {tb}")

    # ── 源4: Sina 亚太指数
    sina_apac_map = [
        ('int_nikkei225', '日经225指数'),
        ('int_kospi', '韩国综合指数'),
        ('int_asx200', '澳洲S&P/ASX 200'),
    ]
    for code, name in sina_apac_map:
        if name in apac_data:
            continue
        r = http.get(
            f'https://hq.sinajs.cn/list={code}',
            headers={'Referer': 'https://finance.sina.com.cn'},
            timeout=8, retry=2, encoding='gbk'
        )
        if r and r.status_code == 200:
            key = f'hq_str_{code}="'
            if key in r.text:
                parts = r.text.split(key)[1].split('"')[0].split(',')
                if len(parts) > 2:
                    try:
                        price = float(parts[1])
                        chg = float(parts[2]) if len(parts) > 2 else 0
                        lo, hi = valid_ranges.get(name, (0, 999999))
                        if lo < price < hi:
                            apac_data[name] = {'price': round(price, 2), 'change': round(chg, 2), 'source': 'Sina 亚太'}
                            log.info(f"  ✅ {name}(Sina): {price:.2f} ({chg:+.2f}%)")
                    except:
                        pass

    market_data['市场表现']['亚太股市'] = apac_data
    src_list = set(v.get('source', '') for v in apac_data.values())
    market_data['_meta']['sources']['亚太股市'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 亚太股市采集结果: {list(apac_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【中国外汇与贵金属】三数据源：Sina API → TickDB → Yahoo Finance
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【中国外汇与贵金属】采集中...")
log.info("=" * 60)

def fetch_cn_forex_metals():
    cn_fm_data = {}

    # ── 源1: Sina Finance API ──
    r = http.get(
        'https://hq.sinajs.cn/list=USDCNY,EURUSD,GBPUSD,AUDUSD',
        headers={'Referer': 'https://finance.sina.com.cn'},
        timeout=10, retry=2, encoding='gbk'
    )
    if r and r.status_code == 200:
        text = r.text
        sina_fx_map = [
            ('hq_str_USDCNY="', 'USD/CNY'),
            ('hq_str_EURUSD="', 'EUR/USD'),
            ('hq_str_GBPUSD="', 'GBP/USD'),
            ('hq_str_AUDUSD="', 'AUD/USD'),
        ]
        for key, name in sina_fx_map:
            if key in text:
                parts = text.split(key)[1].split('"')[0].split(',')
                if len(parts) > 1:
                    try:
                        price = float(parts[1])
                        if price > 0:
                            cn_fm_data[name] = {'price': round(price, 5 if 'USD' not in name else 4), 'change': 0, 'source': 'Sina FX'}
                            log.info(f"  ✅ {name}(Sina): {price}")
                    except:
                        pass

    # ── 源2: TickDB ──
    tb = query_tickdb('EURUSD,GBPUSD,AUDUSD,XAUUSD,XAGUSD', timeout=15)
    tb_fm_map = {
        'EURUSD': 'EUR/USD', 'GBPUSD': 'GBP/USD', 'AUDUSD': 'AUD/USD',
        'XAUUSD': '现货黄金(XAUUSD)', 'XAGUSD': '现货白银(XAGUSD)'
    }
    for sym, name in tb_fm_map.items():
        if sym in tb and name not in cn_fm_data:
            item = tb[sym]
            p = float(item['last_price'])
            c = float(item.get('price_change_percent_24h', 0) or 0)
            if p > 0:
                unit = 'USD/盎司' if '金' in name or '银' in name else ''
                cn_fm_data[name] = {'price': round(p, 5 if unit else 4), 'change': round(c, 2), 'unit': unit, 'source': 'TickDB'}
                log.info(f"  ✅ {name}(TB): {p} ({c:+.2f}%)")

    # ── 源3: Yahoo Finance ──
    try:
        import yfinance as yf
        yf_fx_map = {
            'CNY=X': ('USD/CNY', 4),
            'EURUSD=X': ('EUR/USD', 5),
            'GC=F': ('COMEX黄金期货', 2),
            'SI=F': ('COMEX白银期货', 2),
        }
        for sym, (name, dp) in yf_fx_map.items():
            if name in cn_fm_data:
                continue
            for attempt in range(3):
                try:
                    ticker = yf.Ticker(sym)
                    info = ticker.fast_info
                    p = info.last_price
                    if p and p > 0:
                        cn_fm_data[name] = {'price': round(float(p), dp), 'change': 0, 'source': 'Yahoo Finance'}
                        log.info(f"  ✅ {name}(YF): {p}")
                        break
                except Exception:
                    if attempt < 2:
                        time.sleep(random.uniform(1, 2.5))
                break
    except Exception as e:
        log.warning(f"  ⚠️ Yahoo Finance 外汇/贵金属失败: {e}")

    market_data['市场表现']['中国外汇与贵金属'] = cn_fm_data
    src_list = set(v.get('source', '') for v in cn_fm_data.values())
    market_data['_meta']['sources']['中国外汇与贵金属'] = ' + '.join(sorted(src_list)) if src_list else 'N/A'
    log.info(f"  📊 外汇与贵金属采集结果: {list(cn_fm_data.keys())}")


# ═══════════════════════════════════════════════════════════════
# 【中国经济数据】三数据源：akshare → Sina宏观 → Web Search
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【中国经济数据】采集中...")
log.info("=" * 60)

# -*- coding: utf-8 -*-
# 新的经济数据采集函数（完整替换 fetch_cn_economic + fetch_us_economic）
# 包含：中美欧日韩全维度经济指标采集



# ===== NEW ECONOMIC FUNCTIONS (Added for expanded data collection) =====

def fetch_cn_economic():
    """中国经济数据：PMI/CPI/PPI/GDP/社融/贸易差额/工业增加值/零售销售/失业率"""
    cn_econ = {}
    market_data['经济数据']['中国'] = cn_econ
    
    def _add(name, val, period='', unit='%', dp=1):
        if val is None: return
        try:
            num = float(val)
            cn_econ[name] = {'数值': num, '展示': f"{num:.{dp}f}{unit}", '单位': unit, '期间': str(period), 'source': 'akshare'}
            log.info(f"  ✅ 中国{name}: {num:.{dp}f}{unit}")
        except: pass
    
    try:
        import akshare as ak
        try:
            df = ak.macro_china_pmi()
            if df is not None and len(df) > 0:
                latest = df.iloc[0]
                period = str(latest.get('月份', ''))
                for key, label in [('制造业PMI','制造业PMI'), ('非制造业PMI','非制造业PMI')]:
                    v = latest.get(key, None)
                    if v:
                        try: _add(label, float(v), period, '', 1)
                        except: pass
        except Exception as e: log.warning(f"  ⚠️ PMI失败: {e}")
        
        try:
            df = ak.macro_china_cpi()
            if df is not None and len(df) > 0:
                v = df.iloc[0].get('全国-当月', None)
                if v: _add('CPI', float(v), str(df.iloc[0].get('月份', '')), '%', 1)
        except: pass
        
        try:
            df = ak.macro_china_ppi()
            if df is not None and len(df) > 0:
                v = df.iloc[0].get('当月', None)
                if v: _add('PPI', float(v), str(df.iloc[0].get('月份', '')), '%', 1)
        except: pass
        
        try:
            df = ak.macro_china_gdp()
            if df is not None and len(df) > 0:
                v = df.iloc[0].get('国内生产总值-同比增长', None)
                if v: _add('GDP', float(v), str(df.iloc[0].get('季度', '')), '%', 1)
        except: pass
        
        # ── 北向/南向资金
        try:
            df = ak.stock_hsgt_fund_flow_summary_em()
            if df is not None and len(df) > 0:
                north = df[df['资金方向'] == '北向']['资金净流入'].sum()
                south = df[df['资金方向'] == '南向']['资金净流入'].sum()
                today_str = str(df.iloc[0]['交易日']) if len(df) > 0 else ''
                if north != 0 or len(df) > 0:
                    # 单位是元，转换为亿
                    north_yi = round(north / 1e8, 2) if north else 0
                    south_yi = round(south / 1e8, 2) if south else 0
                    cn_econ['北向资金'] = {'数值': north_yi, '展示': f"{north_yi:.2f}亿", '单位': '亿', '期间': today_str, 'source': 'akshare'}
                    cn_econ['南向资金'] = {'数值': south_yi, '展示': f"{south_yi:.2f}亿", '单位': '亿', '期间': today_str, 'source': 'akshare'}
                    log.info(f"  ✅ 北向资金(akshare): {north_yi:.2f}亿")
                    log.info(f"  ✅ 南向资金(akshare): {south_yi:.2f}亿")
        except Exception as e:
            log.warning(f"  ⚠️ 北向/南向资金失败: {e}")
        
        # ── 中国10年国债收益率（国债指数）
        try:
            from datetime import date, timedelta
            today = date.today()
            start = (today - timedelta(days=30)).strftime('%Y%m%d')
            end = today.strftime('%Y%m%d')
            df = ak.bond_china_yield(start_date=start, end_date=end)
            if df is not None and len(df) > 0:
                # 取最新一条国债收益率曲线
                gov = df[df['曲线名称'].str.contains('国债', na=False)]
                if len(gov) > 0:
                    latest = gov.iloc[-1]
                    val_10y = latest.get('10年', None)
                    period = str(latest.get('日期', ''))
                    if val_10y is not None and val_10y not in ('', None):
                        cn_econ['10年国债收益率'] = {
                            '数值': float(val_10y), '展示': f"{float(val_10y):.4f}%",
                            '单位': '%', '期间': period, 'source': '中国债券信息网'
                        }
                        log.info(f"  ✅ 10年国债收益率(akshare): {val_10y}%")
        except Exception as e:
            log.warning(f"  ⚠️ 10年国债收益率失败: {e}")
        
    except Exception as e: log.warning(f"  ⚠️ akshare中国经济失败: {e}")
    
    log.info(f"  📊 中国经济数据: {list(cn_econ.keys())}")


def fetch_us_economic():
    """美国经济数据：失业率/初请/PPI/零售/工业产出"""
    us_econ = {}
    market_data['经济数据']['美国'] = us_econ
    
    def _fred(sid, name, dp=2, retries=2):
        import time as _t, random as _r
        for attempt in range(retries + 1):
            try:
                _t.sleep(_r.uniform(1.0, 2.5))
                url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit=3'
                r = requests.get(url, timeout=15)
                if r.status_code != 200:
                    if attempt < retries: continue
                    return None
                vals = [l.split(',')[-1].strip() for l in r.text.strip().split('\n')[-3:] if l.split(',')[-1].strip() not in ('.', 'N/A', '')]
                if not vals:
                    if attempt < retries: continue
                    return None
                return round(float(vals[-1]), dp) if vals else None
            except:
                if attempt < retries: _t.sleep(_r.uniform(1.0, 2.5))
                elif attempt == retries: return None
        return None
    
    _econ_month = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日").strftime("%Y-%m")
    for sid, name, dp in [('UNRATE','失业率',1), ('PPIACO','PPI',1), ('RSXFS','零售销售',1), ('INDPRO','工业产出',1)]:
        v = _fred(sid, name, dp)
        if v is not None:
            us_econ[name] = {'数值': v, '展示': f"{v:.1f}%", '单位': '%', '期间': _econ_month, 'source': 'FRED'}
            log.info(f"  ✅ 美国{name}: {v:.1f}%")
    
    log.info(f"  📊 美国经济数据: {list(us_econ.keys())}")


def fetch_eu_economic():
    """欧洲经济数据：CPI/失业率"""
    eu_econ = {}
    market_data['经济数据']['欧洲'] = eu_econ
    log.info(f"  📊 欧洲经济数据: (待实现)")


def fetch_apac_economic():
    """亚太经济数据：日本CPI/韩国PMI"""
    apac_econ = {}
    market_data['经济数据']['亚太'] = apac_econ
    log.info(f"  📊 亚太经济数据: (待实现)")


# ═══════════════════════════════════════════════════════════════
# 【美国就业市场】专项：初请/续请/Challenger裁员/非农前瞻
# 数据源：金投网财经日历、Challenger官方月度报告、华尔街见闻、美国劳工部官网、FRED
# ═══════════════════════════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【美国就业市场】采集中...")
log.info("=" * 60)

def fetch_us_employment():
    """美国就业市场专项数据 - 五维完整精确版
    采集指标：
      1. 当周初请失业金人数 (ICSA)     → 当期值、预期值、前值(修正后)、前值(修正前)
      2. 初请四周均值 (IC4WSA)        → 当期值、前值(修正后)、边际变化
      3. 续请失业金人数 (CCSA)       → 当期值、预期值、前值(修正后)、前值(修正前)
      4. Challenger企业裁员           → 当期值、前值、核心诱因及分项占比
      5. 非农前瞻预测                 → 新增就业预期区间、失业率一致预期
    严格区分当期值、预期值、前值(修正后)、前值(修正前)
    禁止编造：无数据标注「暂未披露」
    """
    import requests, re, time, random, datetime
    log = logging.getLogger('collector')

    employment = {}

    # ─── 工具函数 ────────────────────────────────────────────

    def _fred(sid, limit=30):
        """从FRED CSV拉数据，返回[(date, val), ...]，按日期升序"""
        for attempt in range(3):
            try:
                time.sleep(random.uniform(1.0, 2.5))
                url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit={limit}'
                r = requests.get(url, timeout=20)
                if r.status_code != 200:
                    continue
                lines = r.text.strip().split('\n')
                data = []
                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        date = parts[0].strip()
                        raw = parts[-1].strip()
                        if raw not in ('.', 'N/A', '', 'nan', 'None') and raw.replace('.', '').replace('-', '').replace('+', '').replace('e', '').replace('E', '').replace(' ', '').isdigit():
                            try:
                                val = float(raw)
                                data.append((date, val))
                            except:
                                pass
                data.sort(key=lambda x: x[0])
                return data
            except Exception as e:
                log.warning(f'  [FRED] {sid} 异常: {e}')
                time.sleep(random.uniform(2, 4))
        return []

    def _ws(query, max_results=8):
        """Web Search，回退逻辑"""
        try:
            results = ws_fallback.search(query, max_results=max_results)
            return ' '.join([r.get('content', '') or r.get('snippet', '') for r in results])
        except Exception as e:
            log.warning(f'  [WS] search failed: {e}')
            return ''

    def _ws_multi(queries):
        """多引擎合并搜索（避免单引擎结果贫乏）"""
        merged = []
        for q in queries:
            r = _ws(q, max_results=6)
            merged.append(r)
        return ' || '.join([r for r in merged if r])

    # ══════════════════════════════════════════════════════════
    # 指标1：当周初请失业金人数 (ICSA)
    # 取数平台：FRED(ICSA) + 金投网 + 华尔街见闻
    # 目标字段：当期值、预期值、前值(修正后)、前值(修正前)
    # ══════════════════════════════════════════════════════════

    # FRED ICSA：取最新6条数据，找到当前和前4周的前值（用于检测修订）
    ic_data = _fred('ICSA', limit=30)
    val_cur  = None; date_cur  = None
    val_prev = None; date_prev = None  # 修正后的前值
    val_prev_orig = None; date_prev_orig = None  # 修正前的原始前值

    if len(ic_data) >= 2:
        date_cur,  val_cur  = ic_data[-1]
        date_prev, val_prev = ic_data[-2]
    if len(ic_data) >= 5:
        # 原始前值 = 4周前的报告值（修订前的数据）
        date_prev_orig, val_prev_orig = ic_data[-5]

    # 预期值：从金投网和华尔街见闻抓取
    ws_ic_q = _ws_multi([
        f'当周初请失业金 预期值 {DATA_MONTH_EN}',
        f'initial jobless claims forecast consensus estimate {DATA_MONTH_EN}',
        '美国初请失业金人数 市场预期 万人',
    ])
    val_consensus = None
    if ws_ic_q:
        for pat in [
            r'预期[为:：]?\s*(\d+\.?\d*)\s*(?:万|千人)',
            r'(\d+\.?\d*)\s*万\s*(?:预期)?',
            r'estimate[:\s]*(\d+\.?\d*)\s*K',
            r'consensus[:\s]*(\d+\.?\d*)\s*(?:万|K)',
        ]:
            for m in re.finditer(pat, ws_ic_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    val_consensus = round(v / 1000, 1) if 100 <= v <= 500 else round(v, 1) if 0.1 <= v <= 50 else None
                    if val_consensus:
                        break
                except:
                    pass
            if val_consensus:
                break

    if val_cur is not None:
        entry = {
            '当期值': round(val_cur),
            '预期值': val_consensus,
            '前值(修正后)': round(val_prev) if val_prev is not None else None,
            '前值(修正前)': round(val_prev_orig) if val_prev_orig is not None else None,
            '前值期间': date_prev,
            '单位': '万人',
            '期间': date_cur,
            'source': 'FRED(ICSA)+Web Search',
        }
        # 若修正前后有差异，标注
        if val_prev_orig is not None and abs(val_prev_orig - val_prev) > 0.3:
            entry['修正标注'] = f'前值自{round(val_prev_orig)}万修正至{round(val_prev)}万'
        employment['当周初请失业金'] = entry
        cons_str = f" | 预期{val_consensus}万" if val_consensus else ""
        log.info(f'  ✅ 当周初请: {round(val_cur)}万({date_cur}){cons_str} | 前值(修正后){round(val_prev) if val_prev else "N/A"}万 | 前值(修正前){round(val_prev_orig) if val_prev_orig else "N/A"}万')
    else:
        employment['当周初请失业金'] = {
            '当期值': '暂未披露', '预期值': val_consensus,
            '前值(修正后)': '暂未披露', '前值(修正前)': '暂未披露',
            '单位': '万人', 'source': 'FRED(ICSA)+Web Search',
        }
        log.warning('  ⚠️ 当周初请: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标2：初请四周均值 (IC4WSA)
    # 取数平台：FRED(IC4WSA) + 金投网
    # 目标字段：当期值、前值(修正后)、边际变化（自动计算）
    # ══════════════════════════════════════════════════════════

    ic4_data = _fred('IC4WSA', limit=30)
    val_ic4 = None; date_ic4 = None
    val_ic4_prev = None; date_ic4_prev = None

    if len(ic4_data) >= 2:
        date_ic4, val_ic4 = ic4_data[-1]
        date_ic4_prev, val_ic4_prev = ic4_data[-2]

    # 边际变化自动计算
    change = None
    if val_ic4 is not None and val_ic4_prev is not None:
        change = round(val_ic4 - val_ic4_prev, 1)
        change_str = f'+{change}' if change > 0 else str(change)
    else:
        change_str = '暂无法计算'

    if val_ic4 is not None:
        entry = {
            '当期值': round(val_ic4),
            '前值': round(val_ic4_prev) if val_ic4_prev is not None else None,
            '前值期间': date_ic4_prev,
            '边际变化': change_str,
            '边际变化数值': change,  # 纯数字，用于计算
            '单位': '万人',
            '期间': date_ic4,
            'source': 'FRED(IC4WSA)',
            '备注': '四周均值不含当周单周数据',
        }
        employment['初请四周均值'] = entry
        log.info(f'  ✅ 初请四周均值: {round(val_ic4)}万({date_ic4}) | 前值{date_ic4_prev}为{round(val_ic4_prev) if val_ic4_prev else "N/A"}万 | 边际变化{change_str}万人')
    else:
        employment['初请四周均值'] = {
            '当期值': '暂未披露', '前值': '暂未披露', '边际变化': '暂无法计算',
            '单位': '万人', 'source': 'FRED(IC4WSA)',
        }
        log.warning('  ⚠️ 初请四周均值: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标3：续请失业金人数 (CCSA)
    # 取数平台：FRED(CCSA) + 金投网 + 华尔街见闻
    # 目标字段：当期值、预期值、前值(修正后)、前值(修正前)
    # ══════════════════════════════════════════════════════════

    ccsa_data = _fred('CCSA', limit=30)
    val_ccsa = None; date_ccsa = None
    val_ccsa_prev = None; date_ccsa_prev = None
    val_ccsa_prev_orig = None; date_ccsa_prev_orig = None

    if len(ccsa_data) >= 2:
        date_ccsa, val_ccsa = ccsa_data[-1]
        date_ccsa_prev, val_ccsa_prev = ccsa_data[-2]
    if len(ccsa_data) >= 5:
        date_ccsa_prev_orig, val_ccsa_prev_orig = ccsa_data[-5]

    # 预期值
    ws_ccsa_q = _ws_multi([
        f'续请失业金 预期值 {DATA_MONTH_EN}',
        f'continued jobless claims forecast consensus {DATA_MONTH_EN}',
        '美国续请失业金人数 市场预期 万人',
    ])
    val_ccsa_consensus = None
    if ws_ccsa_q:
        for pat in [
            r'预期[为:：]?\s*(\d+\.?\d*)\s*(?:万|千人)',
            r'(\d+\.?\d*)\s*万\s*(?:预期)?',
            r'consensus[:\s]*(\d+\.?\d*)\s*(?:万|K)',
        ]:
            for m in re.finditer(pat, ws_ccsa_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    val_ccsa_consensus = round(v / 1000, 1) if 1000 <= v <= 5000 else round(v, 1) if 100 <= v <= 300 else None
                    if val_ccsa_consensus:
                        break
                except:
                    pass
            if val_ccsa_consensus:
                break

    if val_ccsa is not None:
        entry = {
            '当期值': round(val_ccsa),
            '预期值': val_ccsa_consensus,
            '前值(修正后)': round(val_ccsa_prev) if val_ccsa_prev is not None else None,
            '前值(修正前)': round(val_ccsa_prev_orig) if val_ccsa_prev_orig is not None else None,
            '前值期间': date_ccsa_prev,
            '单位': '万人',
            '期间': date_ccsa,
            'source': 'FRED(CCSA)+Web Search',
            '备注': 'seasonally adjusted',
        }
        if val_ccsa_prev_orig is not None and abs(val_ccsa_prev_orig - val_ccsa_prev) > 0.3:
            entry['修正标注'] = f'前值自{round(val_ccsa_prev_orig)}万修正至{round(val_ccsa_prev)}万'
        employment['续请失业金'] = entry
        cons_str = f" | 预期{val_ccsa_consensus}万" if val_ccsa_consensus else ""
        rev_str = f" | {entry.get('修正标注', '')}" if entry.get('修正标注') else ""
        log.info(f'  ✅ 续请失业金: {round(val_ccsa)}万({date_ccsa}){cons_str} | 前值(修正后){round(val_ccsa_prev) if val_ccsa_prev else "N/A"}万 | 前值(修正前){round(val_ccsa_prev_orig) if val_ccsa_prev_orig else "N/A"}万{rev_str}')
    else:
        employment['续请失业金'] = {
            '当期值': '暂未披露', '预期值': val_ccsa_consensus,
            '前值(修正后)': '暂未披露', '前值(修正前)': '暂未披露',
            '单位': '万人', 'source': 'FRED(CCSA)+Web Search',
        }
        log.warning('  ⚠️ 续请失业金: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标4：Challenger企业裁员人数 + 分项诱因
    # 取数平台：金投网财经日历、Challenger官方月度报告、华尔街见闻
    # 目标字段：当期值、前值、核心诱因及分项占比
    # ══════════════════════════════════════════════════════════

    today = datetime.date.today()
    month_names_cn = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
    month_names_en = ['January','February','March','April','May','June','July','August','September','October','November','December']
    cur_month_cn = month_names_cn[today.month - 1]
    cur_month_en = month_names_en[today.month - 1]

    # 搜索 Challenger 官方报告 + 金投网 + 华尔街见闻
    ws_ch_q = _ws_multi([
        f'Challenger job cuts {cur_month_en} {today.year} official report',
        f'挑战者企业裁员 {today.year}年{cur_month_cn} 官方报告',
        f'Challenger裁员 {today.year}年{cur_month_cn} 人数',
        f'美国挑战者企业裁员 {cur_month_cn} 公布值',
    ])

    val_ch = None; val_ch_prev = None
    reasons = {}

    if ws_ch_q:
        # ── 提取裁员总人数 ──
        for pat in [
            r'(\d{1,3}\,\d{3}\,\d{3})\s*(?:人|layoffs?)',
            r'(\d{1,3}\,\d{3})\s*(?:万)?\s*(?:人|layoffs?)(?:\s|$)',
            r'裁员\s*(\d{1,3}\,\d{3})\s*(?:人|人)?',
            r'(\d+\.?\d*)\s*万\s*(?:裁员|layoff)?',
        ]:
            if val_ch is not None:
                break
            for m in re.finditer(pat, ws_ch_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if v > 1000000:
                        v = v / 10000  # 人→万
                    val_ch = round(v, 1)
                    break
                except:
                    pass

        # ── 提取前值 ──
        for pat in [
            r'(?:上月|前月|前值)[:\s]*(\d+\.?\d*)\s*(?:万)?',
            r'(\d+\.?\d*)\s*万?\s*(?:上月|前月)(?:\s|。)',
            r'前值\s*(\d+\.?\d*)\s*(?:万)?',
        ]:
            if val_ch_prev is not None:
                break
            for m in re.finditer(pat, ws_ch_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if v > 10000:
                        v = v / 10000
                    val_ch_prev = round(v, 1)
                    if val_ch_prev > 0:
                        break
                except:
                    pass

        # ── 提取裁员诱因及占比 ──
        # AI替代/自动化
        for pat in [
            r'AI.{0,6}替代.{0,20}(\d+\.?\d*)\s*%',
            r'(?:artificial\s*)?AI.{0,20}(\d+\.?\d*)\s*%',
            r'自动化.{0,20}(\d+\.?\d*)\s*%',
            r'technology.{0,15}(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:AI|自动化|技术替代)',
        ]:
            for m in re.finditer(pat, ws_ch_q, re.IGNORECASE):
                try:
                    pct = float(m.group(1))
                    if 0 < pct <= 100:
                        reasons['AI替代/自动化'] = f'{pct:.1f}%'
                        break
                except:
                    pass
            if 'AI替代/自动化' in reasons:
                break

        # 企业重组/成本削减
        for pat in [
            r'(?:企业\s*)?重组.{0,20}(\d+\.?\d*)\s*%',
            r'restructur.{0,20}(\d+\.?\d*)\s*%',
            r'(?:成本|降本).{0,20}(\d+\.?\d*)\s*%',
            r'cost\s*cut.{0,20}(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:企业\s*)?(?:重组|cost)',
        ]:
            for m in re.finditer(pat, ws_ch_q, re.IGNORECASE):
                try:
                    pct = float(m.group(1))
                    if 0 < pct <= 100:
                        reasons['企业重组'] = f'{pct:.1f}%'
                        break
                except:
                    pass
            if '企业重组' in reasons:
                break

        # 行业拖累/需求疲软
        for pat in [
            r'(?:行业|需求).{0,20}(\d+\.?\d*)\s*%',
            r'(?:soft|weak).{0,20}(?:demand|market).{0,20}(\d+\.?\d*)\s*%',
            r'market.{0,15}(?:weak|soft).{0,20}(\d+\.?\d*)\s*%',
        ]:
            for m in re.finditer(pat, ws_ch_q, re.IGNORECASE):
                try:
                    pct = float(m.group(1))
                    if 0 < pct <= 100:
                        reasons['行业拖累/需求疲软'] = f'{pct:.1f}%'
                        break
                except:
                    pass
            if '行业拖累/需求疲软' in reasons:
                break

        # 关税/贸易摩擦
        for pat in [
            r'关税.{0,20}(\d+\.?\d*)\s*%',
            r'tariff.{0,20}(\d+\.?\d*)\s*%',
            r'贸易.{0,10}(?:摩擦|战).{0,20}(\d+\.?\d*)\s*%',
        ]:
            for m in re.finditer(pat, ws_ch_q, re.IGNORECASE):
                try:
                    pct = float(m.group(1))
                    if 0 < pct <= 100:
                        reasons['关税/贸易摩擦'] = f'{pct:.1f}%'
                        break
                except:
                    pass
            if '关税/贸易摩擦' in reasons:
                break

    if val_ch is not None:
        entry = {
            '当期值': val_ch,
            '前值': val_ch_prev if val_ch_prev else '暂未披露',
            '单位': '万人',
            '期间': f'{today.year}年{today.month}月',
            'source': 'Web Search(Challenger+金投网+华尔街见闻)',
        }
        if reasons:
            entry['核心诱因及占比'] = reasons
        employment['Challenger裁员'] = entry
        log.info(f'  ✅ Challenger裁员: 当期{val_ch}万 | 前值{val_ch_prev if val_ch_prev else "N/A"}万 | 诱因: {reasons if reasons else "未披露分项"}')
    else:
        employment['Challenger裁员'] = {
            '当期值': '暂未披露', '前值': '暂未披露',
            '单位': '万人', 'source': 'Web Search(Challenger)',
        }
        log.warning('  ⚠️ Challenger裁员: 未解析到有效数据')

    # ══════════════════════════════════════════════════════════
    # 指标5：非农前瞻预测
    # 取数平台：华尔街见闻前瞻专题、金投网宏观预期汇总、主流财经快讯
    # 目标字段：新增就业预期区间（含市场普遍预期）、失业率一致预期
    # ══════════════════════════════════════════════════════════

    ws_nfp_q = _ws_multi([
        f'非农前瞻预测 {today.year}年{today.month}月 市场预期',
        f'NFP nonfarm payroll analyst estimate {cur_month_en} {today.year}',
        f'美国非农就业新增预期 失业率一致预期 {cur_month_en}',
        f'nonfarm payrolls consensus estimate {today.year} forecast',
    ])

    if ws_nfp_q:
        payroll_vals = []; ur_vals = []

        # ── 新增就业：提取数字（多种模式） ──
        for pat in [
            r'新增就业[为:：]?\s*(\d+\.?\d*)\s*(?:万|人)?',
            r'预计新增\s*(\d+\.?\d*)\s*(?:万)?',
            r'(\d+\.?\d*)\s*万\s*(?:新增)?\s*(?:就业)?',
            r'payrolls?\s*(?:estimate|forecast)?[:\s]*(\d+\.?\d*)\s*(?:万)?',
            r'average\s*estimate[:\s]*(\d+\.?\d*)\s*(?:万)?',
            r'(\d+\.?\d*)\s*至\s*(\d+\.?\d*)\s*万',
        ]:
            for m in re.finditer(pat, ws_nfp_q, re.IGNORECASE):
                try:
                    if len(m.groups()) >= 2 and m.group(2):
                        # 区间格式：X至Y万
                        low = float(m.group(1).replace(',',''))
                        high = float(m.group(2).replace(',',''))
                        if 0 < low < 500 and 0 < high < 500:
                            payroll_vals.extend([low, high])
                    else:
                        raw = m.group(1).replace(',', '')
                        v = float(raw)
                        if 0 < v < 500:
                            payroll_vals.append(v)
                        elif 1000 <= v <= 5000:
                            payroll_vals.append(v / 10000)
                except:
                    pass

        # ── 失业率：提取数字 ──
        for pat in [
            r'失业率[为:：]?\s*(\d+\.?\d*)\s*%',
            r'unemployment\s*(?:rate)?[:\s]*(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:失业率|unemployment)',
            r'失业率一致预期[为:：]?\s*(\d+\.?\d*)\s*%',
        ]:
            for m in re.finditer(pat, ws_nfp_q):
                try:
                    v = float(m.group(1))
                    if 0 < v < 20:
                        ur_vals.append(v)
                except:
                    pass

        # ── 聚合同值（±0.3范围取平均） ──
        def cluster(vals, tol=0.5):
            if not vals: return []
            vals = sorted(set([round(v, 1) for v in vals]))
            groups = []; cur = [vals[0]]
            for x in vals[1:]:
                if abs(x - cur[-1]) <= tol:
                    cur.append(x)
                else:
                    groups.append(round(sum(cur) / len(cur), 1))
                    cur = [x]
            groups.append(round(sum(cur) / len(cur), 1))
            return groups

        payroll_ests = cluster(payroll_vals, 3.0)
        ur_ests = cluster(ur_vals, 0.2)

        nfp_entry = {'source': 'Web Search(华尔街见闻+金投网+主流财经)'}
        if payroll_ests:
            nfp_entry['新增就业预期'] = round(sum(payroll_ests) / len(payroll_ests), 1)
            if len(payroll_ests) >= 2:
                mn = min(payroll_ests); mx = max(payroll_ests)
                nfp_entry['新增就业预期区间'] = f'{mn:.0f}~{mx:.0f}'
            nfp_entry['单位'] = '万人'
        if ur_ests:
            nfp_entry['失业率预期'] = round(sum(ur_ests) / len(ur_ests), 2)
            if len(ur_ests) >= 2:
                mn = min(ur_ests); mx = max(ur_ests)
                nfp_entry['失业率预期区间'] = f'{mn:.1f}~{mx:.1f}'
            nfp_entry['失业率单位'] = '%'
        nfp_entry['期间'] = f'{today.year}年{today.month}月'
        employment['非农前瞻预测'] = nfp_entry
        log.info(f'  ✅ 非农前瞻: 新增={nfp_entry.get("新增就业预期","N/A")}万{nfp_entry.get("新增就业预期区间","")} | 失业率={nfp_entry.get("失业率预期","N/A")}%{nfp_entry.get("失业率预期区间","")}')
    else:
        employment['非农前瞻预测'] = {
            '新增就业预期': '暂未披露',
            '失业率预期': '暂未披露',
            'source': 'Web Search(华尔街见闻+金投网)',
        }
        log.warning('  ⚠️ 非农前瞻: Web Search 无结果')

    market_data['美国就业市场'] = employment
    log.info(f'  📊 美国就业市场采集完成: {list(employment.keys())}')

def fetch_us_employment():
    """美国就业市场专项数据 - 优化增强版
    采集：当周初请、续请、四周均值、Challenger裁员、非农前瞻
    数据源：FRED（初请/续请/均值）+ Web Search（Challenger/非农前瞻）
    严格区分：当期值、预期值、前值（修正前后）
    """
    import requests, re, time, random
    import logging
    log = logging.getLogger('collector')

    employment = {}

    # ─── FRED 封装 ───────────────────────────────────────────
    def _fred(sid, limit=15):
        """从FRED CSV拉数据，返回[(date, val), ...]"""
        for attempt in range(3):
            try:
                time.sleep(random.uniform(1.0, 2.5))
                url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit={limit}'
                r = requests.get(url, timeout=15)
                if r.status_code != 200:
                    continue
                lines = r.text.strip().split('\n')
                data = []
                for line in lines[1:]:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        date = parts[0].strip()
                        raw = parts[-1].strip()
                        if raw not in ('.', 'N/A', '', 'nan', 'None') and raw.replace('.', '').replace('-', '').isdigit():
                            try:
                                val = float(raw)
                                data.append((date, val))
                            except:
                                pass
                return data
            except Exception as e:
                log.warning(f'  [FRED] {sid} 异常: {e}')
                time.sleep(random.uniform(2, 4))
        return []

    def _fred_latest(sid, limit=15):
        """返回 (当期date, 当期val, 前值date, 前值val)"""
        data = _fred(sid, limit)
        if not data or len(data) < 2:
            return None, None, None, None
        # data: oldest→newest
        latest_date, latest_val = data[-1]
        prev_date, prev_val = data[-2]
        return latest_date, latest_val, prev_date, prev_val

    # ─── Web Search 封装 ─────────────────────────────────────
    def _ws(query, max_results=5):
        """Web Search，回退逻辑"""
        try:
            results = ws_fallback.search(query, max_results=max_results)
            return ' '.join([r.get('content', '') or r.get('snippet', '') for r in results])
        except Exception as e:
            log.warning(f'  [WS] search failed: {e}')
            return ''

    # ══════════════════════════════════════════════════════════
    # 指标1：当周初请失业金人数 (ICSA)
    # FRED序列：ICSA = Initial Claims Seasonally Adjusted
    # 数据字段：当期值、当期期间、前值、前值期间、预期值(市场一致预期)、source
    # ══════════════════════════════════════════════════════════
    date_cur, val_cur, date_prev, val_prev = _fred_latest('ICSA', limit=15)

    # ── 获取市场预期值：搜"当周初请失业金 预期" ──
    ws_initial_q = _ws(f'initial jobless claims forecast this week {DATA_DATE_EN} consensus estimate', max_results=8)
    val_consensus = None
    if ws_initial_q:
        est_patterns = [
            r'(?:预期|estimate|consensus|forecast)[:\s]*(\d+\.?\d*)\s*(?:万|thousand|K)?',
            r'(\d+\.?\d*)\s*(?:万)?\s*(?:初请)?\s*(?:预期)?',
            r'(\d+\.?\d*)\s*K\s*(?:initial)?\s*(?:claims)?',
        ]
        for pat in est_patterns:
            m = re.search(pat, ws_initial_q, re.IGNORECASE)
            if m:
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if 100 <= v <= 500:  # 千人单位，转万人
                        val_consensus = round(v / 1000, 1)
                    elif 0.1 <= v <= 100:
                        val_consensus = round(v, 1)
                    if val_consensus:
                        break
                except:
                    pass

    if val_cur is not None:
        emp_entry = {
            '当期值': round(val_cur),
            '前值': round(val_prev) if val_prev is not None else None,
            '前值期间': date_prev,
            '单位': '万人',
            '期间': date_cur,
            'source': 'FRED(ICSA)',
            '备注': 'seasonally adjusted',
        }
        if val_consensus is not None:
            emp_entry['预期值'] = val_consensus
        employment['当周初请失业金'] = emp_entry
        cons_str = f" 预期{val_consensus}万" if val_consensus else ""
        log.info(f'  ✅ 当周初请: {round(val_cur)}万({date_cur}){cons_str}, 前值: {round(val_prev) if val_prev else "N/A"}万({date_prev})')
    else:
        employment['当周初请失业金'] = {
            '当期值': None, '前值': None, '预期值': val_consensus,
            '单位': '万人', 'source': 'FRED',
        }
        log.warning('  ⚠️ 当周初请: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标2：初请四周均值 (IC4WSA)
    # FRED序列：IC4WSA = 4-week moving average of initial claims
    # 数据字段：当期值、前值(修正后)、前值期间(修正前)、边际变化、source
    # 修正值：FRED ICSA 的 revision = 当期值 vs 前值
    # ══════════════════════════════════════════════════════════
    date_ic4, val_ic4, date_ic4_prev, val_ic4_prev = _fred_latest('IC4WSA', limit=15)

    # ── 修正值：取更多历史数据看修订幅度 ──
    ic4_data_full = _fred('IC4WSA', limit=20)
    revision_note = None
    if len(ic4_data_full) >= 4:
        # 上上周均值 vs 当时的报告值
        prev2_date, prev2_val = ic4_data_full[-3] if len(ic4_data_full) >= 3 else (None, None)
        if prev2_val is not None:
            revision_note = f"前值自{round(prev2_val)}万修正至{round(val_ic4_prev) if val_ic4_prev else 'N/A'}万"

    change = None
    if val_ic4_prev is not None:
        change = round(val_ic4 - val_ic4_prev)
    if val_ic4 is not None:
        emp_ic4 = {
            '当期值': round(val_ic4),
            '前值': round(val_ic4_prev) if val_ic4_prev is not None else None,
            '前值期间': date_ic4_prev,
            '边际变化': f'+{change}' if change and change > 0 else str(change) if change else None,
            '单位': '万人',
            '期间': date_ic4,
            'source': 'FRED(IC4WSA)',
            '备注': '四周均值不含当周单周数据',
        }
        if revision_note:
            emp_ic4['修正值'] = revision_note
        employment['初请四周均值'] = emp_ic4
        rev_str = f" | {revision_note}" if revision_note else ""
        log.info(f'  ✅ 初请四周均值: {round(val_ic4)}万({date_ic4}), 前值: {round(val_ic4_prev) if val_ic4_prev else "N/A"}万, 边际: {change}{rev_str}')
    else:
        employment['初请四周均值'] = {
            '当期值': None, '前值': None, '边际变化': None,
            '单位': '万人', 'source': 'FRED(IC4WSA)',
        }
        log.warning('  ⚠️ 初请四周均值: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标3：续请失业金人数 (CCSA)
    # FRED序列：CCSA = Continued Claims Seasonally Adjusted
    # 数据字段：当期值、前值(修正后)、前值期间、预期值(市场一致预期)、source
    # ══════════════════════════════════════════════════════════
    date_ccsa, val_ccsa, date_ccsa_prev, val_ccsa_prev = _fred_latest('CCSA', limit=15)

    # ── 获取市场预期值：搜"续请失业金 预期" ──
    ws_continuing_q = _ws(f'continued jobless claims forecast {DATA_DATE_EN} consensus estimate', max_results=8)
    val_ccsa_consensus = None
    if ws_continuing_q:
        est_patterns = [
            r'(?:预期|estimate|consensus)[:\s]*(\d+\.?\d*)\s*(?:万|thousand|K)',
            r'(\d+\.?\d*)\s*(?:万)?\s*(?:续请|continued)?\s*(?:预期)?',
        ]
        for pat in est_patterns:
            m = re.search(pat, ws_continuing_q, re.IGNORECASE)
            if m:
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if 1000 <= v <= 5000:  # 千人单位，转万人
                        val_ccsa_consensus = round(v / 1000, 1)
                    elif 0.1 <= v <= 100:
                        val_ccsa_consensus = round(v, 1)
                    if val_ccsa_consensus:
                        break
                except:
                    pass

    # ── 修正值：获取更多历史数据看修订幅度 ──
    ccsa_full = _fred('CCSA', limit=20)
    ccsa_rev_note = None
    if len(ccsa_full) >= 4 and val_ccsa_prev is not None:
        # 取第4新的数据作为"前值"（已被修订）
        older_date, older_val = ccsa_full[-3] if len(ccsa_full) >= 3 else (None, None)
        if older_val is not None and abs(older_val - val_ccsa_prev) > 0.5:
            ccsa_rev_note = f"前值自{round(older_val)}万修正至{round(val_ccsa_prev)}万"

    if val_ccsa is not None:
        emp_ccsa = {
            '当期值': round(val_ccsa),
            '前值': round(val_ccsa_prev) if val_ccsa_prev is not None else None,
            '前值期间': date_ccsa_prev,
            '单位': '万人',
            '期间': date_ccsa,
            'source': 'FRED(CCSA)',
            '备注': 'seasonally adjusted',
        }
        if val_ccsa_consensus is not None:
            emp_ccsa['预期值'] = val_ccsa_consensus
        if ccsa_rev_note:
            emp_ccsa['修正值'] = ccsa_rev_note
        employment['续请失业金'] = emp_ccsa
        cons_str = f" 预期{val_ccsa_consensus}万" if val_ccsa_consensus else ""
        rev_str = f" | {ccsa_rev_note}" if ccsa_rev_note else ""
        log.info(f'  ✅ 续请失业金: {round(val_ccsa)}万({date_ccsa}){cons_str}, 前值: {round(val_ccsa_prev) if val_ccsa_prev else "N/A"}万({date_ccsa_prev}){rev_str}')
    else:
        employment['续请失业金'] = {
            '当期值': None, '前值': None, '预期值': val_ccsa_consensus,
            '单位': '万人', 'source': 'FRED(CCSA)',
        }
        log.warning('  ⚠️ 续请失业金: 数据获取失败')

    # ══════════════════════════════════════════════════════════
    # 指标4：Challenger企业裁员人数 + 分项诱因
    # 数据源：Web Search（三引擎轮搜）
    # 字段：公布值、前值、裁员核心诱因及分项占比
    # 重点：AI替代、企业重组、行业拖累等核心因素
    # ══════════════════════════════════════════════════════════
    challenger_q = _ws('Challenger job cuts monthly report current month', max_results=8)
    if challenger_q:
        # 提取裁员总人数
        # Pattern: "X,YZZ" or "X.XX万" or "X,XXX,XXX" style numbers
        raw_patterns = [
            r'(\d{1,3}\,\d{3}\,\d{3})\s*(?:人|人裁员|layoff)',
            r'(\d{1,3}\,\d{3})\s*(?:万)?\s*(?:人|裁员|layoff)',
            r'(\d+\.?\d*)\s*(?:万)?\s*(?:layoff|job\s*cuts|裁员)',
            r'裁员\s*(\d+\.?\d*)\s*(?:万)?\s*(?:人)',
            r'(\d+\.?\d*)\s*(?:万)\s*(?:人)',
        ]
        val_ch = None
        for pat in raw_patterns:
            m = re.search(pat, challenger_q)
            if m:
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    # 判断单位：>10000视为人，转万人；<1000视为万
                    if v > 100000:
                        v = v / 10000
                    val_ch = round(v, 2)
                    break
                except:
                    pass

        # 提取前值
        prev_patterns = [
            r'(?:上月|前月|上月为|上月为)\s*(\d+\.?\d*)\s*(?:万)?',
            r'(?:前值|上期)[:\s]*(\d+\.?\d*)\s*(?:万)?',
            r'(\d+\.?\d*)\s*(?:万)\s*(?:人)?.{0,10}?(?:上月|前月)',
        ]
        val_ch_prev = None
        for pat in prev_patterns:
            m = re.search(pat, challenger_q)
            if m:
                try:
                    raw = m.group(1).replace(',', '')
                    v = float(raw)
                    if v > 10000:
                        v = v / 10000
                    val_ch_prev = round(v, 2)
                    break
                except:
                    pass

        # 提取AI替代、企业重组等行业分类占比
        reasons = {}
        reason_patterns = {
            'AI替代/自动化': [r'AI(?:替代|取代|自动化|机器)', r'(?:artificial|AI)\s*(?:replacement|automation)', r'自动化.{0,8}替代', r'机器.{0,8}替代'],
            '企业重组': [r'企业\s*重组', r'公司\s*重组', r'restructur', r'cost\s*cut', r'降本'],
            '行业拖累/需求疲软': [r'行业\s*拖累', r'需求\s*疲软', r'market\s*(?:weak|soft|demand)', r'行业.{0,6}下滑', r'demand.{0,8}(?:soft|weak)'],
            '关税/贸易摩擦': [r'关税', r'tariff', r'贸易.{0,6}摩擦', r'trade\s*war'],
        }
        for reason_name, patterns in reason_patterns.items():
            for pat in patterns:
                if re.search(pat, challenger_q, re.IGNORECASE):
                    reasons[reason_name] = '提及'
                    break

        if val_ch is not None:
            entry = {
                '当期值': val_ch,
                '前值': val_ch_prev if val_ch_prev else '暂未披露',
                '单位': '万人',
                'source': 'Web Search(Challenger)',
            }
            if reasons:
                entry['核心诱因'] = reasons
            employment['Challenger裁员'] = entry
            log.info(f'  ✅ Challenger裁员: {val_ch}万, 前值: {val_ch_prev}, 诱因: {list(reasons.keys()) if reasons else "未明确"}')
        else:
            log.warning('  ⚠️ Challenger裁员: 未解析到有效数据')
    else:
        log.warning('  ⚠️ Challenger裁员: Web Search 无结果')

    # ══════════════════════════════════════════════════════════
    # 指标5：最新非农就业前瞻预测
    # 数据源：Web Search（三引擎）
    # 字段：市场普遍新增就业预期区间、失业率预期数值
    # ══════════════════════════════════════════════════════════
    # 自动判断当前月份（距上次非农发布后的第几周）
    import datetime
    today = datetime.date.today()
    # 每月第一个周五发布非农数据，估算当前所处月份
    # 非农发布后一周内为"当月已发布"，之后为"下月预测"
    # 简单策略：搜"非农就业预测 YYYY年MM月" 或 "NFP forecast month"
    month_names = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    cur_month_name = month_names[today.month - 1]
    prev_month_name = month_names[(today.month - 2) % 12]
    # 尝试两个版本：上月实际 vs 本月预测
    nfp_q = _ws(f'NFP nonfarm payroll forecast {cur_month_name} {today.year} analyst estimate', max_results=8)
    if not nfp_q or len(nfp_q) < 50:
        nfp_q2 = _ws(f'美国非农就业预测 {today.year}年{today.month}月 市场预期', max_results=8)
        nfp_q = nfp_q + ' ' + nfp_q2

    if nfp_q:
        payroll_vals = []
        ur_vals = []

        # 提取新增就业人数（多种模式）
        payroll_patterns = [
            r'(?:新增|预计|预期|估计)\s*(\d+\.?\d*)\s*(?:万)?\s*(?:人|jobs?)',
            r'(\d+\.?\d*)\s*万\s*(?:新增)?\s*(?:就业)?',
            r'(?:新增|increase)\s*(?:of\s*)?(\d+\.?\d*)\s*(?:万)?\s*(?:jobs?|人)',
            r'payroll[s]?\s*(?:estimate|forecast|预期)?[:\s]*(\d+\.?\d*)',
            r'average\s*estimate[:\s]*(\d+\.?\d*)\s*(?:万)?',
        ]
        for pat in payroll_patterns:
            for m in re.finditer(pat, nfp_q):
                raw = m.group(1).replace(',', '')
                try:
                    v = float(raw)
                    if 0 < v < 1000:  # 万人
                        payroll_vals.append(v)
                    elif 1000 <= v <= 5000:
                        payroll_vals.append(v / 10000)
                except:
                    pass

        # 提取失业率
        ur_patterns = [
            r'失业率\s*(\d+\.?\d*)\s*%',
            r'unemployment\s*(?:rate)?\s*(?:预期)?[:\s]*(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*%\s*(?:失业率|unemployment)',
        ]
        for pat in ur_patterns:
            for m in re.finditer(pat, nfp_q):
                try:
                    v = float(m.group(1))
                    if 0 < v < 20:
                        ur_vals.append(v)
                except:
                    pass

        # 合并去重（同值±0.5取平均）
        def cluster(vals, tol=0.5):
            if not vals:
                return []
            vals = sorted(set(vals))
            clusters = []
            cur = [vals[0]]
            for x in vals[1:]:
                if abs(x - cur[-1]) <= tol:
                    cur.append(x)
                else:
                    clusters.append(sum(cur) / len(cur))
                    cur = [x]
            clusters.append(sum(cur) / len(cur))
            return [round(v, 1) for v in clusters]

        payroll_ests = cluster(payroll_vals, 3.0)
        ur_ests = cluster(ur_vals, 0.2)

        nfp_entry = {
            'source': 'Web Search(NFP前瞻)',
        }
        if payroll_ests:
            if len(payroll_ests) == 1:
                nfp_entry['新增就业预期'] = payroll_ests[0]
            else:
                nfp_entry['新增就业预期区间'] = f'{min(payroll_ests):.0f}~{max(payroll_ests):.0f}'
                nfp_entry['新增就业预期'] = round(sum(payroll_ests) / len(payroll_ests), 1)
            nfp_entry['单位'] = '万人'
        if ur_ests:
            if len(ur_ests) == 1:
                nfp_entry['失业率预期'] = ur_ests[0]
            else:
                nfp_entry['失业率预期区间'] = f'{min(ur_ests):.1f}~{max(ur_ests):.1f}'
                nfp_entry['失业率预期'] = round(sum(ur_ests) / len(ur_ests), 2)
            nfp_entry['失业率单位'] = '%'
        nfp_entry['期间'] = f'{today.year}年{today.month}月'

        employment['非农前瞻预测'] = nfp_entry
        log.info(f'  ✅ 非农前瞻: 新增={nfp_entry.get("新增就业预期","N/A")}万 失业率={nfp_entry.get("失业率预期","N/A")}% 区间={nfp_entry.get("新增就业预期区间","N/A")}')
    else:
        employment['非农前瞻预测'] = {
            '新增就业预期': '暂未披露',
            '失业率预期': '暂未披露',
            'source': 'Web Search(NFP前瞻)',
        }
        log.warning('  ⚠️ 非农前瞻: Web Search 无结果')

    market_data['美国就业市场'] = employment
    log.info(f'  📊 美国就业市场采集完成: {list(employment.keys())}')
def fetch_market_holidays():
    """采集当日全球金融市场休市安排。
    
    优先级：API 查询优先 → Web Search 兜底。
    A股/港股：通过 akshare 交易日历确认（有实际行情数据则必定为交易日）。
    美股/欧股：优先用 akshare 节假日接口，Web Search 辅助。
    """
    holiday_data = {}

    # ─────────────────────────────────────────────
    # 工具：API 查是否交易日
    # ─────────────────────────────────────────────
    def _is_cn_trading_day(target_date):
        """用 akshare stock_zh_index_daily 验证目标日期是否有实际行情。
        有行情数据 = 必定为交易日（最可靠的事实判断）。
        注意：akshare 的 tool_trade_date_hist_sina 日历数据可能滞后，
        以实际行情数据为准。
        """
        try:
            df = ak.stock_zh_index_daily(symbol='sh000001')
            return target_date in df['date'].astype(str).values
        except Exception as e:
            log.warning(f"  akshare 行情数据查询失败: {e}")
            return None  # 不确定

    target = datetime.datetime.strptime(config.DATA_DATE, "%Y年%m月%d日").strftime("%Y-%m-%d")

    # ════════════════════════════════════════════
    # 【中国 A 股】akshare 优先：直接查交易日历
    # ════════════════════════════════════════════
    cn_is_trading = _is_cn_trading_day(target)
    if cn_is_trading is True:
        cn_status = '正常交易'
        cn_src = 'akshare(交易日历)'
    elif cn_is_trading is False:
        cn_status = '全日休市'
        cn_src = 'akshare(交易日历)'
    else:
        # akshare 查不到，用 Web Search 兜底
        cn_status = None
        cn_src = 'Web Search'

    # 若 akshare 判断为交易日，直接采信；否则 Web Search 兜底
    if cn_is_trading is False:
        pass  # 已确认休市
    else:
        # 用 Web Search 辅助确认（或兜底）
        ws_q = f"中国A股 {DATA_DATE_CN_MD} 休市"
        ws_r = ws_fallback.search(ws_q)
        ws_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in ws_r])
        if any(kw in ws_text for kw in ['A股休市', '沪深交易所休市', '内地股市休市']):
            cn_status = '全日休市'
        else:
            cn_status = '正常交易'

    # 港股同步（与 A 股共用同一交易日历，港股通规则相同）
    holiday_data['中国股市'] = {'状态': cn_status, 'source': cn_src}
    holiday_data['港股']     = {'状态': cn_status, 'source': cn_src}

    # ════════════════════════════════════════════
    # 【美国股市】akshare 节假日接口 + Web Search 兜底
    # ════════════════════════════════════════════
    us_q = f"US stock market closed {DATA_DATE_CN_MD} holiday"
    us_r = ws_fallback.search(us_q)
    us_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in us_r])
    us_closed = any(kw in us_text.lower() for kw in [
        'us market closed', 'us exchanges closed', 'nyse closed', 'nasdaq closed',
        '阵亡将士纪念日', 'memorial day', 'independence day', '美国股市休市'
    ])
    us_half = any(kw in us_text for kw in ['美股提前收盘', 'early close', '半日交易'])
    holiday_data['美国股市'] = {
        '状态': '全日休市' if us_closed else ('半日休市' if us_half else '正常交易'),
        'source': 'Web Search'
    }

    # ════════════════════════════════════════════
    # 【欧洲股市】Web Search 兜底
    # ════════════════════════════════════════════
    eu_q = f"European stock market closed {DATA_MONTH_EN.split()[0]} holiday"
    eu_r = ws_fallback.search(eu_q)
    eu_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in eu_r])
    eu_closed = any(kw in eu_text.lower() for kw in [
        'european market closed', 'london stock exchange closed',
        '法兰克福休市', '巴黎证交所休市', '复活节假期', 'easter holiday'
    ])
    eu_half = any(kw in eu_text for kw in ['欧洲提前收盘', '半日交易'])
    holiday_data['欧洲股市'] = {
        '状态': '全日休市' if eu_closed else ('半日休市' if eu_half else '正常交易'),
        'source': 'Web Search'
    }

    # ════════════════════════════════════════════
    # 【澳大利亚股市】Web Search 兜底
    # ════════════════════════════════════════════
    au_q = f"Australia ASX market closed {DATA_MONTH_EN.split()[0]} holiday"
    au_r = ws_fallback.search(au_q)
    au_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in au_r])
    au_closed = any(kw in au_text.lower() for kw in [
        'asx closed', '澳大利亚休市', '澳洲股市休市',
        'anzac day', '澳新军团日'
    ])
    holiday_data['澳大利亚股市'] = {
        '状态': '全日休市' if au_closed else '正常交易',
        'source': 'Web Search'
    }

    # ════════════════════════════════════════════
    # 【CME 贵金属/美油期货】Web Search 兜底
    # ════════════════════════════════════════════
    cme_q = f"CME metals crude oil holiday schedule {DATA_MONTH_EN.split()[0]}"
    cme_r = ws_fallback.search(cme_q)
    cme_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in cme_r])
    cme_closed = any(kw in cme_text.lower() for kw in [
        'cme closed', 'comex closed', 'nymex closed', 'cme全日休市'
    ])
    cme_half = any(kw in cme_text for kw in ['CME提前收盘', '半日交易'])
    holiday_data['CME贵金属/美油'] = {
        '状态': '全日休市' if cme_closed else ('半日休市' if cme_half else '正常交易'),
        'source': 'Web Search'
    }

    # ════════════════════════════════════════════
    # 【ICE 布油期货】Web Search 兜底
    # ════════════════════════════════════════════
    ice_q = f"ICE Brent crude oil holiday schedule {DATA_MONTH_EN.split()[0]}"
    ice_r = ws_fallback.search(ice_q)
    ice_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in ice_r])
    ice_closed = any(kw in ice_text.lower() for kw in [
        'ice closed', 'ice futures closed', '布油期货休市'
    ])
    holiday_data['ICE布油'] = {
        '状态': '全日休市' if ice_closed else '正常交易',
        'source': 'Web Search'
    }

    # ════════════════════════════════════════════
    # 【国内期货夜盘】Web Search 兜底
    # ════════════════════════════════════════════
    dom_q = f"上海期货交易所 夜盘交易时间 {DATA_DATE_CN_MD}"
    dom_r = ws_fallback.search(dom_q)
    dom_text = ' '.join([r.get('content', '') or r.get('snippet', '') for r in dom_r])
    domestic_night = '夜盘交易' in dom_text
    domestic_closed = any(kw in dom_text for kw in [
        '上期所休市', '郑商所休市', '大商所休市', '上金所休市',
        '国内期货休市', '期货交易所休市'
    ])
    holiday_data['国内期货夜盘'] = {
        '状态': '休市' if domestic_closed else ('正常交易' if domestic_night else '待确认'),
        'source': 'Web Search'
    }

    market_data['休市情况'] = holiday_data
    for name, info in holiday_data.items():
        log.info(f"  ✅ {name}: {info['状态']}")


def _get_func(name):
    """Lazy lookup - resolves function name at call time"""
    fn = globals().get(name)
    if fn is None:
        log.warning(f'  Function {name} not found in globals')
    return fn

def _call_task(name):
    """Call a task by name using lazy lookup. Always use try/except - never swallow exceptions silently."""
    fn = _get_func(name)
    if fn is None:
        log.warning(f'  [SKIP] Function {name} not found in globals')
        return False
    try:
        fn()
        log.info(f"  [OK]   {name} completed")
        return True
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] {name}")
        log.error(f"         Exception: {type(e).__name__}: {e}")
        log.error(f"         Traceback: {traceback.format_exc().strip()}")
        return False


tasks = [
    ('fetch_us_stocks',      240),
    ('fetch_us_bonds_forex', 240),
    ('fetch_us_commodities', 240),
    ('fetch_a_shares',       240),
    ('fetch_hk_stocks',      240),
    ('fetch_eu_stocks',      240),
    ('fetch_apac_stocks',    240),
    ('fetch_cn_forex_metals',240),
    ('fetch_cn_economic',    240),
    ('fetch_us_economic',    240),
    ('fetch_us_employment',  240),
    ('fetch_eu_economic',    240),
    ('fetch_apac_economic',  240),
    ('fetch_market_holidays',240),
]

# ── Run all tasks and collect per-task results ──────────────────────
task_results = {}   # {name: True/False/None}
ok_count = fail_count = skip_count = 0

for name, timeout_sec in tasks:
    # ── 断点续采：跳过已完成的类别 ────────────────────────────────
    category_map = {
        'fetch_us_stocks':       '美国股市',
        'fetch_us_bonds_forex':  '美国债券与外汇',
        'fetch_us_commodities':  '美国大宗商品',
        'fetch_a_shares':        'A股',
        'fetch_hk_stocks':       '港股',
        'fetch_eu_stocks':       '欧洲股市',
        'fetch_apac_stocks':     '亚太股市',
        'fetch_cn_forex_metals': '中国外汇与贵金属',
        'fetch_cn_economic':     '中国经济数据',
        'fetch_us_economic':     '美国经济数据',
        'fetch_us_employment':   '美国就业市场',
        'fetch_eu_economic':     '欧洲经济数据',
        'fetch_apac_economic':   '亚太经济数据',
        'fetch_market_holidays': '休市情况',
    }
    cat_name = category_map.get(name, '')

    # 已完成的子类别（市场表现/经济数据下的具体指标）从 market_data 读取判断
    # 只有任务名称对应的主类别已全部采集成功才跳过
    if cat_name and cat_name in market_data['_meta'].get('completed_categories', []):
        log.info(f"\n  --- Task: {name} [SKIP - 已完成] ---")
        task_results[name] = None
        skip_count += 1
        continue

    log.info(f"\n  --- Task: {name} ---")
    result = _call_task(name)
    task_results[name] = result
    if result is True:
        ok_count += 1
        # 标记该类别为已完成
        if cat_name and cat_name not in market_data['_meta']['completed_categories']:
            market_data['_meta']['completed_categories'].append(cat_name)
        # 立即保存 checkpoint
        _checkpoint_save()
        log.info(f"  [Checkpoint] 已保存，已完成类别: {market_data['_meta']['completed_categories']}")
    elif result is False:
        fail_count += 1
    else:
        skip_count += 1

# ── Final summary ──────────────────────────────────────────────────
log.info("\n" + "=" * 60)
log.info("📊 【采集任务汇总报告】")
log.info("=" * 60)
for name, result in task_results.items():
    status = {True: "OK", False: "FAIL", None: "SKIP"}[result]
    icon = {"OK": "✅", "FAIL": "❌", "SKIP": "⏭️ "}[status]
    log.info(f"  {icon} {name:<30} {status}")
log.info("-" * 60)
log.info(f"  成功: {ok_count}  |  失败: {fail_count}  |  跳过: {skip_count}")
log.info("=" * 60)


# ===== FINAL SAVE =====
# 与 checkpoint 相同的保存逻辑（更新 collection_time）
if _checkpoint_save():
    log.info("✅ 数据已保存(最终版): " + config.MARKET_DATA_FILE)
else:
    log.warning("❌ 保存失败: " + str(e))
