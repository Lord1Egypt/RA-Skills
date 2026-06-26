#!/usr/bin/env python3
"""
Web3 行业资本运作周报 — 一键生成脚本
======================================
运行：python3 run_all.py [--week YYYY-MM-DD] [--rwa-url URL] [--output report.md]

参数：
  --week      指定周报起始日期（周一），默认自动计算上周
  --rwa-url   直接指定 PANews RWA 周刊文章 URL，跳过自动搜索
  --output    输出文件路径，默认 report_YYYYMMDD.md

依赖：curl、python3 标准库
所有子模块脚本位于 scripts/ 目录
"""

import subprocess, sys, json, re, os
import urllib.parse
from datetime import datetime, timedelta
from html.parser import HTMLParser
from email.utils import parsedate_to_datetime
from argparse import ArgumentParser


# ══════════════════════════════════════════════════════
#  工具函数
# ══════════════════════════════════════════════════════

def fetch(url: str, timeout: int = 20) -> str:
    r = subprocess.run(
        ['curl', '-s', '-L', f'--max-time', str(timeout),
         '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
         '-H', 'Accept: text/html,application/json',
         '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
         url],
        capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else ''


def log(msg: str) -> None:
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', file=sys.stderr)


def fmt_usd(n: float) -> str:
    if not n: return '未披露'
    if n >= 1e9: return f'约 {n/1e9:.2f} 亿美元'
    if n >= 1e6: return f'约 {n/1e6:.1f}M 美元'
    return f'约 ${n:,.0f}'


def get_week_dates(start: datetime) -> set:
    return {(start + timedelta(days=i)).strftime('%b %-d') for i in range(7)}


# ══════════════════════════════════════════════════════
#  Part.3  监管 / 行业事件（深潮 TechFlow RSS）
# ══════════════════════════════════════════════════════

INCLUDE_KW = [
    '监管', '法案', 'SEC', 'CFTC', 'FDIC', '立法', '合规要求', '禁止',
    '证监会', '金融监管局', '金融局', '金管局', '央行发布', '央行规定',
    'MiCA', 'GENIUS', 'CLARITY', '国会', '议会', '处罚', '执法',
    '牌照', '许可证', 'VASP', 'FATF', '反洗钱', '稳定币立法',
    '虚拟资产条例', '加密法规', '监管框架', '监管政策', '合规框架',
    '拟立法', '拟监管', '拟禁止', '拟要求', '拟出台', '整治',
    '虚拟资产税', '加密税', '数字资产税', '代币化监管', '稳定币监管',
    '加密货币监管', '区块链监管', '数字资产监管', '数字货币监管',
]
EXCLUDE_KW = [
    '价格', '涨幅', '跌幅', '清算', '链上数据', '空投', '回购销毁',
    '行情', '日报', '早报', '研报', '教程', '攻略', '巨鲸',
    '会跌', '会涨', '预测', '分析师', '综述', '市场观察',
    '伊朗', '石油', '黄金', '战争', '军事', '停火', '制裁',
    '凭什么', '背后', '帝国', '赚钱', '暴富', '秘密'
]

# 标题必须命中监管行为动词才纳入（避免只是提到"美国"就被收录）
REGULATORY_ACTION_KW = [
    '拟', '将', '计划', '宣布', '发布', '出台', '通过', '批准', '禁止',
    '要求', '规定', '处罚', '整治', '调查', '起诉', '执法', '提案',
    '草案', '法案', '条例', '框架', '政策', '牌照', '许可', '合规',
    '废除', '修订', '颁布', '实施', '推进', '推动', '开展', '启动',
    '警告', '限制', '强制', '明确', '澄清', '回应',
    'proposes', 'bans', 'approves', 'requires', 'law', 'bill', 'rule'
]

class RSSParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tag = False
        self.tag = ''
        self.items = []
        self.cur = {}
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag == 'item':
            self.cur = {}
        if tag in ('title', 'description', 'pubdate', 'link'):
            self.in_tag = True
            self.tag = tag
            self.buf = []

    def handle_endtag(self, tag):
        if self.in_tag and tag in ('title', 'description', 'pubdate', 'link'):
            self.cur[tag] = ''.join(self.buf).strip()
            self.in_tag = False
        if tag == 'item' and self.cur:
            self.items.append(self.cur)
            self.cur = {}

    def handle_data(self, data):
        if self.in_tag:
            self.buf.append(data)


def fetch_part3(one_week_ago: datetime) -> list:
    log('Part.3 — 抓取深潮 TechFlow RSS...')
    results, seen = [], set()
    for page in range(1, 6):
        xml = fetch(f'https://www.techflowpost.com/api/client/common/rss.xml?page={page}', timeout=15)
        if not xml:
            break
        # 用简单正则解析 XML（比HTMLParser更可靠处理CDATA）
        items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
        hit_old = False
        for item_xml in items:
            title = re.search(r'<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item_xml, re.DOTALL)
            desc  = re.search(r'<description[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', item_xml, re.DOTALL)
            pubdate = re.search(r'<pubDate>(.*?)</pubDate>', item_xml)
            link  = re.search(r'<link>(.*?)</link>', item_xml)

            title = (title.group(1) if title else '').strip()
            desc  = re.sub(r'<[^>]+>', '', (desc.group(1) if desc else '')).strip()
            link  = (link.group(1) if link else '').strip()
            pubdate_str = (pubdate.group(1) if pubdate else '').strip()

            try:
                dt = parsedate_to_datetime(pubdate_str)
            except Exception:
                continue

            if dt < one_week_ago:
                hit_old = True
                continue

            text = title + desc
            relevant = any(k in text for k in INCLUDE_KW)
            noisy    = any(k in title for k in EXCLUDE_KW)
            # 二次校验：标题必须同时出现监管行为词，排除仅提及地区/机构的泛泛文章
            has_action = any(k in title for k in REGULATORY_ACTION_KW)
            if relevant and not noisy and has_action and title not in seen:
                seen.add(title)
                # desc 截取前 120 字，去除多余空白
                desc_short = re.sub(r'\s+', ' ', desc).strip()[:120]
                results.append({
                    'date': dt.strftime('%m/%d'),
                    'title': title,
                    'desc': desc_short,
                    'link': link
                })
        if hit_old:
            break

    log(f'Part.3 — 共 {len(results)} 条监管/行业新闻')
    return results


# ══════════════════════════════════════════════════════
#  Part.4 + Part.6  融资 / 并购（Rootdata）
# ══════════════════════════════════════════════════════

EXCHANGE_MAP = {
    'US':'Nasdaq/NYSE','HK':'HKEX','JP':'TSE','T':'TSE',
    'SW':'SIX','AU':'ASX','CA':'TSX','DE':'Frankfurt',
    'GB':'LSE','KR':'KRX','SG':'SGX','TW':'TWSE','PA':'Euronext Paris',
}
COUNTRY_MAP = {
    'US':'美国','JP':'日本','HK':'香港','CN':'中国','SG':'新加坡',
    'AU':'澳大利亚','CA':'加拿大','GB':'英国','DE':'德国','KR':'韩国',
    'TW':'台湾','CH':'瑞士','FR':'法国','IN':'印度',
}
TOP_INVESTORS = {
    'a16z','Andreessen Horowitz','Paradigm','Coinbase Ventures','Sequoia',
    'Polychain','Dragonfly','YZi Labs','Binance Labs','Animoca Brands',
    'Bain Capital Crypto','Coatue Management','OKX Ventures','Kucoin Ventures',
    'Alibaba','阿里巴巴','Tencent','腾讯'
}


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.cells, self.rows, self.cur = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'td':   self.in_td = True; self.cur = []
        elif tag == 'tr': self.cells = []

    def handle_endtag(self, tag):
        if tag == 'td':
            self.cells.append(' '.join(''.join(self.cur).split()).strip())
            self.in_td = False
        elif tag == 'tr' and len(self.cells) == 7:
            self.rows.append(self.cells[:]); self.cells = []

    def handle_data(self, data):
        if self.in_td: self.cur.append(data)


# 货币符号 → (ISO代码, 中文名)
CURRENCY_MAP = {
    '€': ('EUR', '欧元'),
    '£': ('GBP', '英镑'),
    '¥': ('JPY', '日元'),
    'A$': ('AUD', '澳元'),
    'C$': ('CAD', '加元'),
    'HK$': ('HKD', '港元'),
}

def get_fx_rate(currency_code: str) -> float:
    """从免费 API 获取对美元汇率，失败返回 1（不换算）"""
    if currency_code == 'USD':
        return 1.0
    try:
        raw = fetch(f'https://open.er-api.com/v6/latest/USD', timeout=8)
        data = json.loads(raw)
        return 1.0 / data['rates'].get(currency_code, 1.0)
    except Exception:
        return 1.0


def parse_currency(s: str) -> tuple:
    """
    解析金额字符串，返回 (usd_amount_m, display_str)
    display_str: 若为非美元则附注原始金额，如 '约 $330 万美元（€3M）'
    """
    s = s.strip()
    if not s or s == '--':
        return 0, '--'

    # 识别货币符号（先检查多字符符号）
    currency_sym = '$'
    currency_code = 'USD'
    currency_name = ''
    for sym, (code, name) in CURRENCY_MAP.items():
        if s.startswith(sym):
            currency_sym = sym
            currency_code = code
            currency_name = name
            break

    original = s  # 保留原始字符串
    clean = s.replace(currency_sym, '').replace(',', '').strip()

    try:
        if 'B' in clean:   raw_val = float(clean.replace('B','').strip()) * 1000
        elif 'M' in clean: raw_val = float(clean.replace('M','').strip())
        elif 'K' in clean: raw_val = float(clean.replace('K','').strip()) / 1000
        else:               raw_val = float(clean) / 1e6
    except Exception:
        return 0, s

    if currency_code == 'USD':
        return raw_val, s   # 美元直接返回

    # 非美元：换算
    rate = get_fx_rate(currency_code)
    usd_m = raw_val * rate

    # 格式化显示
    if usd_m >= 100:
        usd_str = f'约 {usd_m/100:.2f} 亿美元'
    elif usd_m >= 1:
        usd_str = f'约 {usd_m:.1f}M 美元'
    else:
        usd_str = f'约 ${usd_m*1e6:,.0f} 美元'

    return usd_m, f'{usd_str}（{original}，按实时汇率换算）'


def parse_m(s: str) -> float:
    """只返回美元百万数值，供排序用"""
    usd_m, _ = parse_currency(s)
    return usd_m


def parse_investors(inv: str):
    """
    解析投资方字符串。
    带 * 的为明确领投方（leads），其余为跟投/未区分（follows）。
    若无任何 * 标记，所有人放 follows（不区分领投），leads 为空。
    """
    inv = re.sub(r'\+\d+', '', inv).strip()
    if not inv or inv == '--': return [], []
    leads = [m.group(1).strip() for m in re.finditer(r'([\w][\w\s&.]*?)\s*\*', inv)]
    rest  = re.sub(r'[\w][\w\s&.]*?\s*\*', '', inv).strip()
    follows = [t.strip() for t in re.split(r'\s{2,}', rest) if len(t.strip()) > 1]
    if not leads and inv != '--':
        # 无 * 标记：全部视为未区分投资方，不假设谁是领投
        parts = re.split(r'\s{2,}', inv)
        follows = [p.strip() for p in parts if p.strip()]
        leads = []   # 明确不设领投
    return leads, follows


def fetch_part4(week_dates: set):
    log('Part.4/6 — 抓取 Rootdata 融资列表...')
    html = fetch('https://www.rootdata.com/Fundraising')
    if not html:
        log('[WARN] Rootdata 抓取失败')
        return [], []

    p = TableParser(); p.feed(html)
    log(f'Part.4/6 — 解析到 {len(p.rows)} 行数据')

    # 同时解析 <a> 标签中的项目名（SSR HTML 中项目名在 <a> 里）
    class NameParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_a = False; self.names = []; self.buf = []
        def handle_starttag(self, tag, attrs):
            if tag == 'a': self.in_a = True; self.buf = []
        def handle_endtag(self, tag):
            if tag == 'a':
                t = ''.join(self.buf).strip()
                if t: self.names.append(t)
                self.in_a = False
        def handle_data(self, data):
            if self.in_a: self.buf.append(data)

    # 提取每个 td[0] 中 <a> 标签的文本作为项目名
    td_names = []
    for row_html in re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
        if len(tds) == 7:
            np = NameParser(); np.feed(tds[0])
            # 取第一个 <a> 文本；若无则取纯文本首行
            if np.names:
                td_names.append(np.names[0].strip())
            else:
                td_names.append(re.sub(r'<[^>]+>', '', tds[0]).split('\n')[0].strip())

    entries = []
    for idx, row in enumerate(p.rows):
        # 用解析出的干净项目名替代 row[0]
        name = td_names[idx] if idx < len(td_names) else row[0].split('\n')[0].strip()
        rnd, amt, val, date, _, inv = [row[i] for i in range(1, 7)]
        if date not in week_dates: continue
        leads, follows = parse_investors(inv)
        entries.append({
            'name': name, 'round': rnd, 'amount': amt, 'valuation': val,
            'date': date, 'leads': leads, 'follows': follows,
            'is_mna': rnd == 'M&A', 'amount_m': parse_m(amt),
            'has_top': any(t in inv for t in TOP_INVESTORS)
        })

    fund = sorted([e for e in entries if not e['is_mna']],
                  key=lambda e: (e['amount_m'], int(e['has_top'])), reverse=True)
    mna  = [e for e in entries if e['is_mna']]
    log(f'Part.4 — {len(fund)} 个融资项目，Part.6 — {len(mna)} 笔并购')
    return fund, mna


# ══════════════════════════════════════════════════════
#  Part.5  DAT 动态（CoinGecko + 本周变动搜索）
# ══════════════════════════════════════════════════════

# 需要追踪的主要 DAT 公司（用于搜索变动）
DAT_WATCHLIST = [
    ('Strategy',    'MSTR',  'bitcoin'),
    ('Metaplanet',  '3350',  'bitcoin'),
    ('MARA Holdings','MARA', 'bitcoin'),
    ('Coinbase',    'COIN',  'bitcoin'),
    ('Tesla',       'TSLA',  'bitcoin'),
    ('XXI',         'XXI',   'bitcoin'),
    ('SharpLink',   'SBET',  'ethereum'),
    ('Bit Digital', 'BTBT',  'ethereum'),
    ('Coinbase',    'COIN',  'ethereum'),
]

# 变动关键词（搜索结果中出现才认为有本周变动）
CHANGE_KW = ['purchase', 'acquire', 'acquires', 'buy', 'buys', 'bought',
             'sold', 'sell', 'sells', 'added', 'adds', 'increase',
             '购入', '增持', '买入', '出售', '减持', '收购', 'BTC', 'ETH']


# CoinGecko 公司详情页 slug 映射（用于直接抓取购买历史，不依赖搜索引擎）
COINGECKO_SLUGS = {
    'Strategy':   'strategy',
    'Metaplanet': 'metaplanet',
    'MARA Holdings': 'mara-holdings',
    'Coinbase':   'coinbase',
    'Tesla':      'tesla',
    'SharpLink':  'sharplink-gaming',
    'Bit Digital': 'bit-digital',
}


def search_dat_changes(week_start: datetime) -> dict:
    """
    直接抓取 CoinGecko 各公司详情页的 Purchase History 表格，
    筛选出本周（week_start 起7天内）有操作的公司。
    不依赖 DuckDuckGo，curl 可直接获取 SSR 页面。
    """
    changes = {}
    week_end = week_start + timedelta(days=7)
    # 格式化用于匹配：Mar 19, 2026 / March 19, 2026 等
    week_months = {week_start.strftime('%b'), week_start.strftime('%B'),
                   week_end.strftime('%b'), week_end.strftime('%B')}
    week_year = str(week_start.year)

    for name, slug in COINGECKO_SLUGS.items():
        url = f'https://www.coingecko.com/en/treasuries/companies/{slug}'
        html = fetch(url, timeout=20)
        if not html or len(html) < 200:
            log(f'[WARN] Part.5 — {name} CoinGecko 详情页抓取失败')
            continue

        # 从 Purchase History 表格提取购买记录
        # CoinGecko 表格格式：日期 | 数量 | 价格 | 来源
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
        this_week_rows = []
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            if not cells:
                continue
            # 检查第一列（日期）是否在本周范围内
            date_cell = cells[0] if cells else ''
            # 匹配 "Mar 19, 2026" 或 "2026-03-19" 格式
            in_week = False
            m = re.search(r'(\w{3,9})\s+(\d{1,2}),?\s+(\d{4})', date_cell)
            if m:
                try:
                    from datetime import datetime as dt
                    parsed = dt.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", '%B %d %Y')
                except:
                    try:
                        parsed = dt.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", '%b %d %Y')
                    except:
                        parsed = None
                if parsed and week_start <= parsed < week_end:
                    in_week = True
            # 也匹配 ISO 格式
            m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_cell)
            if m2:
                try:
                    from datetime import datetime as dt
                    parsed = dt.strptime(date_cell[:10], '%Y-%m-%d')
                    if week_start <= parsed < week_end:
                        in_week = True
                except:
                    pass
            if in_week and len(cells) >= 2:
                this_week_rows.append(cells)

        if this_week_rows:
            # 汇总本周操作
            summary_parts = []
            for row in this_week_rows[:3]:
                summary_parts.append(' | '.join(row[:4]))
            changes[name] = '；'.join(summary_parts)
            log(f'Part.5 — {name} 本周有 {len(this_week_rows)} 条操作记录')
        else:
            log(f'Part.5 — {name} 本周无操作记录')

    # 若所有 CoinGecko 详情页都抓取失败（无网络），降级：展示全部持仓快照
    if not changes and all(
        not fetch(f'https://www.coingecko.com/en/treasuries/companies/{slug}', timeout=8)
        for slug in list(COINGECKO_SLUGS.values())[:1]
    ):
        log('[WARN] Part.5 — CoinGecko 详情页无法访问，将展示全部持仓快照')
        return {'__show_all__': True}

    log(f'Part.5 — 共找到 {len(changes)} 家公司本周变动')
    return changes


def fetch_part5(week_start: datetime = None):
    log('Part.5 — 抓取 CoinGecko DAT 数据...')
    result = {}
    for coin_id, asset in [('bitcoin', 'BTC'), ('ethereum', 'ETH')]:
        raw = fetch(f'https://api.coingecko.com/api/v3/companies/public_treasury/{coin_id}')
        if not raw:
            log(f'[WARN] {asset} 数据获取失败')
            continue
        try:
            data = json.loads(raw)
            companies  = data.get('companies', [])
            total_value = data.get('total_value_usd', 1) or 1
            # 合理性校验：单家市值不超过全网机构总持仓市值 70%
            # Strategy 持 BTC 64% 是真实情况；BitMine 持 ETH 70% 是数据异常
            valid = [c for c in companies
                     if c.get('total_current_value_usd', 0) / total_value <= 0.70]
            if len(valid) < len(companies):
                log(f'[WARN] {asset} 过滤了 {len(companies)-len(valid)} 条异常持仓数据')
            result[asset] = {
                'total_holdings': data.get('total_holdings', 0),
                'total_value_usd': data.get('total_value_usd', 0),
                'companies': valid[:20]
            }
            log(f'Part.5 — {asset}: {len(valid)} 家有效机构')
        except Exception as e:
            log(f'[WARN] {asset} JSON 解析失败: {e}')

    # 搜索本周变动（S5：只展示有变动的）
    if week_start:
        changes = search_dat_changes(week_start)
        result['changes'] = changes
    else:
        result['changes'] = {}

    return result


# ══════════════════════════════════════════════════════
#  Part.7  RWA 项目动态（PANews）
# ══════════════════════════════════════════════════════

STABLECOIN_KW = ['稳定币', 'stablecoin', 'USDT', 'USDC', 'USDE', 'FDUSD', 'USD1', 'DAI', 'FRAX']

# PANews 英文版章节标题（比中文版更稳定，curl 可直接获取，无需浏览器）
RWA_SECTION_KW = [
    'Institutional & Project Activity', 'Project Activity', 'Project Update',
    'Project Developments', 'Industry Highlights', '项目进展', '项目动态',
]
RWA_END_KW = [
    'Regulatory', 'Data Perspective', 'Market', 'Summary', 'Stablecoin Market',
    'Data Overview', '监管', '数据', '总结',
]


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tag = False
        self.tag_name = ''
        self.paragraphs = []
        self.headings = []   # (index, text)
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li'):
            self.in_tag = True
            self.tag_name = tag
            self.cur = []

    def handle_endtag(self, tag):
        if self.in_tag and tag in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li'):
            text = re.sub(r'\s+', ' ', ''.join(self.cur)).strip()
            if text and len(text) > 3:
                self.paragraphs.append(text)
                if tag in ('h1', 'h2', 'h3', 'h4'):
                    self.headings.append((len(self.paragraphs) - 1, text))
            self.in_tag = False

    def handle_data(self, data):
        if self.in_tag:
            self.cur.append(data)


def find_rwa_article() -> str:
    """
    不依赖 DuckDuckGo，直接抓 PANews RWA 周刊专栏页取最新文章。
    先抓英文版专栏（更易解析），失败则抓中文版。
    """
    # PANews RWA 周刊专栏页（按时间排列，第一条即最新）
    for col_url in [
        'https://www.panewslab.com/en/columns/019888d2-9a04-7e7b-97b5-5a1eac76759a',
        'https://www.panewslab.com/zh/columns/019888d2-9a04-7e7b-97b5-5a1eac76759a',
    ]:
        html = fetch(col_url, timeout=20)
        if not html:
            continue
        # 从专栏页提取文章链接（UUID 格式）
        urls = re.findall(
            r'https?://www\.panewslab\.com/(?:zh|en)/articles/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
            html
        )
        # 专栏页也可能是短 ID 格式
        if not urls:
            urls = re.findall(
                r'href=["\'](?:https?://www\.panewslab\.com)?/(?:zh|en)/articles/([0-9a-zA-Z\-]{10,})["\']',
                html
            )
        seen = set()
        for uid in urls:
            if uid not in seen:
                seen.add(uid)
                full = f'https://www.panewslab.com/en/articles/{uid}'
                log(f'Part.7 - found article from column: {full}')
                return full

    # 降级：尝试已知近期文章（按周更新，作为兜底）
    fallback_urls = [
        'https://www.panewslab.com/en/articles/019ce690-dcd7-7009-9070-43334d068045',  # 3/13
        'https://www.panewslab.com/en/articles/019c55f3-6562-7601-98c9-fc5f1ba41f55',  # 2/13
    ]
    for u in fallback_urls:
        html = fetch(u, timeout=15)
        if html and len(html) > 5000:
            log(f'Part.7 - using fallback URL: {u}')
            return u
    return ''


def extract_project_section(parser) -> list:
    paragraphs = parser.paragraphs

    # 方法1：找章节标题行
    section_start = -1
    section_end   = len(paragraphs)
    for idx, text in parser.headings:
        if any(kw.lower() in text.lower() for kw in RWA_SECTION_KW):
            section_start = idx + 1
        elif section_start >= 0 and any(kw.lower() in text.lower() for kw in RWA_END_KW):
            section_end = idx
            break

    if section_start >= 0:
        section = paragraphs[section_start:section_end]
        log(f'Part.7 - found section via heading, {len(section)} paras')
        return section

    # 方法2：关键词定位非标题行
    for i, para in enumerate(paragraphs):
        if any(kw in para for kw in RWA_SECTION_KW) and len(para) < 40:
            end = next(
                (j for j in range(i + 1, len(paragraphs))
                 if len(paragraphs[j]) < 30 and any(kw in paragraphs[j] for kw in RWA_END_KW)),
                len(paragraphs)
            )
            section = paragraphs[i + 1:end]
            log(f'Part.7 - found section via keyword, {len(section)} paras')
            return section

    # 方法3：降级取中间 60%
    log('[WARN] Part.7 - no section found, using article middle')
    start = len(paragraphs) // 5
    end   = len(paragraphs) * 4 // 5
    return [
        p for p in paragraphs[start:end]
        if len(p) > 30 and not any(k in p for k in STABLECOIN_KW)
    ]


def parse_rwa_projects(section: list) -> list:
    projects = []
    cur_name, cur_details = None, []

    for para in section:
        if any(k in para for k in STABLECOIN_KW):
            continue

        # 英文版: **Bold** 标题；中文版: 短行
        is_bold  = para.startswith('**') and para.count('**') >= 2 and len(para) < 80
        is_short = (
            len(para) < 40 and
            '。' not in para and
            not para.startswith(('According', 'The ', 'In ', 'A ', 'As ', '根据', '据', '此前'))
        )

        if is_bold or is_short:
            if cur_name and cur_details and not any(k in cur_name for k in STABLECOIN_KW):
                projects.append({'name': cur_name.strip('*').strip(), 'detail': ' '.join(cur_details[:3])})
            cur_name = para.strip('*').strip()
            cur_details = []
        elif cur_name:
            cur_details.append(para)

    if cur_name and cur_details and not any(k in cur_name for k in STABLECOIN_KW):
        projects.append({'name': cur_name.strip('*').strip(), 'detail': ' '.join(cur_details[:3])})

    return projects


def fetch_part7(rwa_url: str = '') -> tuple:
    log('Part.7 - searching PANews RWA Weekly...')
    if not rwa_url:
        rwa_url = find_rwa_article()
    if not rwa_url:
        log('[WARN] Part.7 - could not find article URL')
        return [], ''

    log(f'Part.7 - fetching: {rwa_url}')
    html = fetch(rwa_url)
    if not html:
        log('[WARN] Part.7 - fetch failed')
        return [], rwa_url

    parser = ArticleParser()
    parser.feed(html)

    if len(parser.paragraphs) < 5:
        raw = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        for p in raw:
            text = re.sub(r'<[^>]+>', '', p).strip()
            if text and len(text) > 3:
                parser.paragraphs.append(text)

    log(f'Part.7 - {len(parser.paragraphs)} paras, {len(parser.headings)} headings')

    section  = extract_project_section(parser)
    projects = parse_rwa_projects(section)
    log(f'Part.7 - {len(projects)} RWA projects parsed')
    return projects, rwa_url




# ══════════════════════════════════════════════════════
#  报告生成
# ══════════════════════════════════════════════════════

def format_date_range(start: datetime) -> str:
    end = start + timedelta(days=6)
    return f'{start.year}年{start.month}月{start.day}日至{end.month}月{end.day}日'


def build_report(week_start: datetime, part3, fund, mna, part5, rwa_projects, rwa_url) -> str:
    lines = []
    dr = format_date_range(week_start)
    total_m = sum(e['amount_m'] for e in fund)
    total_unit = f'{total_m/100:.2f} 亿' if total_m >= 100 else f'{total_m:.1f}M'

    def inv_str(e):
        leads, follows = e['leads'], e['follows'][:5]
        if leads:
            # 有 * 明确标注的领投方
            ls = '、'.join(leads) + ' 领投'
            fs = '、'.join(follows) + ' 参投' if follows else ''
            return '；'.join(filter(None, [ls, fs]))
        elif follows:
            # 无 * 标注：只列名称，不加"领投/参投"标签
            return '、'.join(follows)
        return '未披露'

    # 轮次中英文映射
    ROUND_ZH = {
        'Seed': 'Seed 轮', 'Pre-Seed': 'Pre-Seed 轮', 'Angel': '天使轮',
        'Series A': 'A 轮', 'Series B': 'B 轮', 'Series C': 'C 轮',
        'Series D': 'D 轮', 'Series E': 'E 轮', 'Series F': 'F 轮',
        'Pre-A': 'Pre-A 轮', 'Pre-B': 'Pre-B 轮',
        'Strategic': '战略融资', 'Private': '私募融资',
        'Debt Financing': '债务融资', 'Post-IPO': '上市后融资',
        'M&A': '并购', '--': '',
    }

    def fmt_round_amt(e):
        """格式化 '轮次与金额' 字段，处理未披露/非美元/未知轮次"""
        rnd = e['round']
        rnd_zh = ROUND_ZH.get(rnd, rnd)  # 未知轮次保留原文
        amt_raw = e['amount']

        if amt_raw == '--' or not amt_raw:
            # 金额未披露
            if rnd_zh:
                return f'未披露具体金额的{rnd_zh}'
            else:
                return '未披露具体金额'
        else:
            # 货币换算（非美元附注）
            _, amt_display = parse_currency(amt_raw)
            val_s = f'，估值 {e["valuation"]}' if e['valuation'] not in ('--', '') else ''
            if rnd_zh:
                return f'{amt_display} {rnd_zh}{val_s}'
            else:
                return f'{amt_display}{val_s}'

    # ── Part.1 近期概览（占位，待 AI 生成）──
    lines += [
        '# Part.1 近期概览',
        '',
        f'> ⚠️ 本部分由 AI 根据 Part.3–Part.6 内容汇总生成，请在所有模块确认后填入。',
        '',
        f'{dr}期间，共录得 Web3 行业 **{len(fund)} 个**项目完成融资，',
        f'总融资金额超 **{total_unit} 美元**（已披露部分）。',
        '',
        '【AI 待补充：大额项目点名、DAT 趋势概括、并购总结、监管重点】',
        '',
    ]

    # ── Part.2 关键数据速览 ──
    changes = part5.get('changes', {}) if part5 else {}
    dat_summary = f'{len(changes)} 家机构有变动' if changes else '本周暂无检测到变动'
    lines += [
        '# Part.2 关键数据速览',
        '',
        '| 指标 | 数值 |',
        '|------|------|',
        f'| 融资项目数 | {len(fund)} 件 |',
        f'| 总融资额 | {total_unit} 美元（已披露） |',
        f'| 并购交易 | {len(mna)} 起 |',
        f'| DAT 变动 | {dat_summary} |',
        '',
    ]

    # ── Part.3 监管 / 行业事件 ──
    lines.append('# Part.3 近期监管/行业事件')
    lines.append('')
    if part3:
        cn_kw    = ['中国', '香港', '海南', '证监', '金融局']
        us_kw    = ['美国', 'SEC', 'CFTC', 'GENIUS', 'CLARITY', '国会', '联邦']
        eu_kw    = ['欧洲', 'MiCA', '英国', '德国', '法国']
        other_kw = ['韩国', '日本', '俄罗斯', '新加坡', '澳大利亚']

        groups = {'中国大陆': [], '香港': [], '美国': [], '欧洲': [], '其他地区': [], '行业/RWA': []}
        for item in part3:
            t = item['title']
            if '香港' in t:                       groups['香港'].append(item)
            elif any(k in t for k in cn_kw):      groups['中国大陆'].append(item)
            elif any(k in t for k in us_kw):      groups['美国'].append(item)
            elif any(k in t for k in eu_kw):      groups['欧洲'].append(item)
            elif any(k in t for k in other_kw):   groups['其他地区'].append(item)
            else:                                  groups['行业/RWA'].append(item)

        count = 0
        for region, items in groups.items():
            for item in items:
                if count >= 12: break
                # 标题 + 摘要（如有）+ 原文链接
                title = item['title']
                desc  = item.get('desc', '')
                link  = item['link']
                lines.append(f'- **[{region}]** {title}')
                if desc:
                    lines.append(f'  > {desc}')
                lines.append(f'  > 原文：{link}')
                lines.append(f'  > ⚠️ AI 润色：（根据上述标题和摘要，改写为一句周报体简讯）')
                lines.append('')
                count += 1

        lines.append(f'> 共 {len(part3)} 条，已按地区分组展示前 {min(len(part3), 12)} 条。')
        lines.append('> ⚠️ 如有来自世链大宗等国内公众号的补充内容，请粘贴后由 AI 插入。')
    else:
        lines.append('> ⚠️ 自动抓取失败，请手动补充。')
    lines.append('')

    # ── Part.4 主要融资事件 ──
    lines.append('# Part.4 主要融资事件')
    lines.append('')
    if fund:
        n = 5 if len(fund) <= 15 else 10
        top_n = fund[:n] + [e for e in fund[n:] if e['has_top']][:2]
        for e in top_n:
            lines += [
                f'## {e["name"]}',
                f'**定位：** （⚠️ AI 搜索补充）',
                f'**轮次与金额：** {fmt_round_amt(e)}',
                f'**投资方：** {inv_str(e)}',
                f'**点评：** （⚠️ AI 根据项目信息生成）',
                '',
            ]
        lines.append(f'> 本周共 {len(fund)} 个融资项目，展示前 {len(top_n)} 个。')
        if len(fund) > 30:
            lines.append('> ⚠️ Rootdata 每页仅 30 条，可能有遗漏，建议访问 https://www.rootdata.com/Fundraising 核对。')
    else:
        lines.append('> ⚠️ 自动抓取失败，请手动补充。')
    lines.append('')

    # ── Part.5 DAT 动态 ──
    lines.append('# Part.5 上市公司 DAT 动态')
    lines.append('')
    if part5:
        changes = part5.get('changes', {})
        show_all = changes.get('__show_all__', False)
        if show_all:
            changes = {}  # 降级时不过滤，下面走 show_all 分支
        assets_data = {k: v for k, v in part5.items() if k in ('BTC', 'ETH')}

        # 构建公司名 → 持仓信息的快查表
        company_lookup = {}
        for asset, data in assets_data.items():
            for c in data.get('companies', []):
                company_lookup[c['name']] = (c, asset)

        if changes:
            lines.append(f'> 本周共 {len(changes)} 家机构有持仓变动：')
            lines.append('')
            for company_name, change_text in changes.items():
                c, asset = company_lookup.get(company_name, ({}, ''))
                if c:
                    code     = c['symbol'].split('.')[0]
                    suffix   = c['symbol'].split('.')[-1] if '.' in c['symbol'] else ''
                    exchange = EXCHANGE_MAP.get(suffix, suffix)
                    country  = COUNTRY_MAP.get(c.get('country', ''), c.get('country', ''))
                    holdings = f'{c.get("total_holdings", 0):,.0f}'
                    cur_val  = c.get('total_current_value_usd', 0)
                    entry_val = c.get('total_entry_value_usd', 0)
                    pnl = ''
                    if entry_val and entry_val > 0 and cur_val:
                        p    = cur_val - entry_val
                        sign = '+' if p >= 0 else ''
                        pnl  = f'，未实现盈亏 {sign}{fmt_usd(abs(p))}（{sign}{p/entry_val*100:.1f}%）'
                    lines += [
                        f'**{company_name}**（{country}）',
                        f'- 股票代号：{code}（{exchange}）',
                        f'- 动作：⚠️ AI 根据以下摘要生成——{change_text}',
                        f'- 总持仓：{holdings} {asset}（当前市值 {fmt_usd(cur_val)}）{pnl}',
                        f'- 点评：（⚠️ AI 根据公司特征与动作生成）',
                        '',
                    ]
                else:
                    lines += [
                        f'**{company_name}**',
                        f'- 动作：⚠️ AI 根据以下摘要生成——{change_text}',
                        f'- 点评：（⚠️ AI 根据公司特征与动作生成）',
                        '',
                    ]
            lines.append('> 参考：https://www.coingecko.com/en/treasuries/bitcoin')
        elif show_all:
            # 降级：CoinGecko 详情页无法访问，展示全部持仓快照供 AI 补全
            lines.append('> ⚠️ 本周变动数据暂无法自动检测，以下为当前持仓快照，请 AI 根据公开信息补全动作字段：')
            lines.append('')
            for asset, data in assets_data.items():
                ttl = f'{data["total_holdings"]:,.0f}'
                val = fmt_usd(data['total_value_usd'])
                lines.append(f'**{asset} 持仓（共 {len(data["companies"])} 家，合计 {ttl} {asset} / {val}）**')
                lines.append('')
                for c in data['companies'][:10]:
                    code     = c['symbol'].split('.')[0]
                    suffix   = c['symbol'].split('.')[-1] if '.' in c['symbol'] else ''
                    exchange = EXCHANGE_MAP.get(suffix, suffix)
                    country  = COUNTRY_MAP.get(c.get('country', ''), c.get('country', ''))
                    holdings = f'{c.get("total_holdings", 0):,.0f}'
                    cur_val  = c.get('total_current_value_usd', 0)
                    entry_val = c.get('total_entry_value_usd', 0)
                    pnl = ''
                    if entry_val and entry_val > 0 and cur_val:
                        p    = cur_val - entry_val
                        sign = '+' if p >= 0 else ''
                        pnl  = f'，未实现盈亏 {sign}{fmt_usd(abs(p))}（{sign}{p/entry_val*100:.1f}%）'
                    lines += [
                        f'**{c["name"]}**（{country}）',
                        f'- 股票代号：{code}（{exchange}）',
                        f'- 动作：⚠️ 待补充',
                        f'- 总持仓：{holdings} {asset}（当前市值 {fmt_usd(cur_val)}）{pnl}',
                        f'- 点评：（⚠️ AI 根据公司特征与动作生成）',
                        '',
                    ]
            lines.append('> 参考：https://www.coingecko.com/en/treasuries/bitcoin')
        else:
            lines.append('> 本周未检测到主要机构持仓变动，如有遗漏请手动补充。')
            lines.append('> 参考：https://www.coingecko.com/en/treasuries/bitcoin')
    else:
        lines.append('> ⚠️ CoinGecko 数据获取失败，请手动补充。')
    lines.append('')

    # ── Part.6 并购 ──
    lines.append('# Part.6 并购交易情况')
    lines.append('')
    if mna:
        for e in mna:
            acq = e['leads'][0] if e['leads'] else (e['follows'][0] if e['follows'] else '未披露')
            if e['amount'] != '--':
                _, amt_display = parse_currency(e['amount'])
                amt_s = f'，金额 {amt_display}'
            else:
                amt_s = ''
            lines += [
                f'## {acq} 收购 {e["name"]}',
                f'- **收购方：** {acq}（⚠️ AI 补充）',
                f'- **标的：** {e["name"]}（⚠️ AI 补充）{amt_s}',
                f'- **分析：** （⚠️ AI 生成）',
                '',
            ]
    else:
        lines.append('> 本周暂无并购交易记录。')
    lines.append('')

    # ── Part.7 RWA ──
    lines.append('# Part.7 RWA 项目动态')
    if rwa_url:
        lines.append(f'> 数据来源：[PANews RWA周刊]({rwa_url})')
    lines.append('')
    if rwa_projects:
        for p in rwa_projects:
            lines += [
                f'## {p["name"]}',
                f'**详情：** {p["detail"][:200]}',
                '',
            ]
        lines.append(f'> 共 {len(rwa_projects)} 个项目（稳定币相关已过滤）。')
        lines.append('> ⚠️ 建议与原文对照核实。')
    else:
        lines.append('> ⚠️ 自动解析未能识别项目标题，以下为文章原始段落，请人工确认后补充：')
        lines.append('')
        # 把 section 段落原文输出，供 AI 在后续对话中整理
        if rwa_url:
            lines.append(f'> 原文链接：{rwa_url}')
        lines.append('')
        lines.append('```')
        # 输出全部段落（最多30段），便于粘贴给AI整理
        for seg in (rwa_projects or [])[:30]:
            lines.append(seg.get('detail', str(seg)))
        lines.append('```')
    lines.append('')

    # ── 元信息 ──
    lines += [
        '---',
        f'> 报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'> 周报周期：{dr}',
        '> ⚠️ 标注 AI 待补充的字段需人工确认后完成，建议将整份报告粘贴给 AI 一次性补全。',
    ]

    return '\n'.join(lines)


# ══════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════

def main():
    parser = ArgumentParser(description='Web3 行业资本运作周报一键生成')
    parser.add_argument('--week', help='周报起始日期 YYYY-MM-DD（默认：上周一）')
    parser.add_argument('--rwa-url', help='PANews RWA 周刊文章 URL（跳过自动搜索）', default='')
    parser.add_argument('--output', help='输出文件路径', default='')
    args = parser.parse_args()

    # 计算周报时间范围
    if args.week:
        week_start = datetime.strptime(args.week, '%Y-%m-%d')
    else:
        today = datetime.today()
        week_start = today - timedelta(days=today.weekday() + 7)

    week_dates = get_week_dates(week_start)
    one_week_ago = datetime.now().astimezone() - timedelta(days=7)

    output_path = args.output or f'report_{week_start.strftime("%Y%m%d")}.md'

    print(f'\n{"="*55}')
    print(f'  Web3 行业资本运作周报生成器')
    print(f'  周期：{format_date_range(week_start)}')
    print(f'{"="*55}\n', flush=True)

    # 并行（顺序执行）抓取各模块
    part3         = fetch_part3(one_week_ago)
    fund, mna     = fetch_part4(week_dates)
    part5         = fetch_part5(week_start)
    rwa_projects, rwa_url = fetch_part7(args.rwa_url)

    # 生成报告
    log('生成报告...')
    report = build_report(week_start, part3, fund, mna, part5, rwa_projects, rwa_url)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'\n{"="*55}')
    print(f'  ✅ 报告已生成：{output_path}')
    print(f'  融资项目：{len(fund)} 个 | 并购：{len(mna)} 起')
    print(f'  监管新闻：{len(part3)} 条 | RWA 项目：{len(rwa_projects)} 个')
    print(f'{"="*55}')
    print()
    print('下一步：将生成的 .md 文件粘贴给 AI，补全所有 ⚠️ 标注字段。')


if __name__ == '__main__':
    main()
