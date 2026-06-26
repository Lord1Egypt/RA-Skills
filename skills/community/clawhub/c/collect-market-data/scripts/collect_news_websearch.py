# -*- coding: utf-8 -*-
"""
采集全球金融市场数据 - Step 2: 政策类 + 科技企业动态 + 汇总类
覆盖：美国、中国、中国香港、欧洲、亚太（日本、韩国）
使用 Web Search（三引擎：Tavily → Bocha → DuckDuckGo，自动切换）
"""
import sys
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo")
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo\skills\collect-market-data\scripts")
sys.stdout.reconfigure(encoding='utf-8')
import os, json, datetime, logging
import config
import content_cleaner as cc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(config.LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)])
log = logging.getLogger(__name__)

log.info("=" * 60)
log.info("🔍 开始采集【政策类】【科技企业动态】【汇总类】数据")
log.info("=" * 60)
log.info(f"📅 报告日期: {config.REPORT_DATE}")
log.info(f"📁 输出目录: {config.OUTPUT_DIR}")

# 读取现有数据
market_data_file = os.path.join(config.OUTPUT_DIR, "market_data.json")
if not os.path.exists(market_data_file):
    log.error(f"❌ 未找到基础数据文件: {market_data_file}")
    log.error("   请先运行 collect_market_data.py")
    sys.exit(1)

with open(market_data_file, 'r', encoding='utf-8') as f:
    market_data = json.load(f)

# 获取年月用于搜索
year = config.TODAY.year
month = config.TODAY.month
date_str = f"{year}年{month:02d}月"

# ═══════════════════════════════════════════
# Web Search 工具函数（三引擎自动切换）
# 优先级：Tavily → Bocha → DuckDuckGo（配额/报错时透明切换，下游无感知）
# ═══════════════════════════════════════════
_search_engine = None  # 缓存最终使用的引擎

def _tavily_search(query, max_results):
    """Tavily 搜索"""
    try:
        from tavily import TavilyClient
        client = TavilyClient()
        result = client.search(query=query, max_results=max_results, search_depth="advanced")
        return result.get('results', [])
    except Exception as e:
        err_str = str(e).lower()
        if 'usage limit' in err_str or 'quota' in err_str or 'exceed' in err_str or 'rate limit' in err_str:
            log.warning(f"  Tavily 配额用尽，切换 Bocha")
            return None  # 表示配额问题，需要切换
        log.warning(f"  Tavily 搜索失败: {e}")
        return []  # 其他错误不切换，直接返回空

def _bocha_search(query, max_results):
    """博查 Bocha Web Search API（环境变量 BOCHA_API_KEY）"""
    import os, requests
    api_key = os.getenv('BOCHA_API_KEY')
    if not api_key:
        log.warning(f"  Bocha API Key 未配置（BOCHA_API_KEY）")
        return None  # 未配置也切换
    try:
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {'query': query, 'freshness': 'noLimit', 'summary': True, 'count': max_results}
        resp = requests.post('https://api.bocha.cn/v1/web-search', headers=headers, json=payload, timeout=15)
        if resp.status_code == 401:
            log.warning(f"  Bocha API Key 无效（401）")
            return None
        if resp.status_code == 403:
            log.warning(f"  Bocha API 余额不足（403）")
            return None
        if resp.status_code == 429:
            log.warning(f"  Bocha 请求限流（429）")
            return None
        resp.raise_for_status()
        data = resp.json()
        results = data.get('data', {}).get('webPages', {}).get('value', [])
        return [{'title': r.get('name', ''),
                 'content': r.get('summary', '') or r.get('snippet', ''),
                 'source': r.get('siteName', ''),
                 'url': r.get('url', ''),
                 'published_date': r.get('datePublished', '')}
                for r in results]
    except Exception as e:
        log.warning(f"  Bocha 搜索失败: {e}")
        return None  # 失败不返回空，尝试 DuckDuckGo

def _ddg_search(query, max_results):
    """DuckDuckGo 搜索（无需 API Key，使用新包 ddgs）"""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [{'title': r.get('title', ''),
                    'content': r.get('body', ''),
                    'source': r.get('source', ''),
                    'url': r.get('href', ''),
                    'published_date': r.get('date', '')}
                   for r in results]
    except Exception as e:
        log.warning(f"  DuckDuckGo 搜索失败: {e}")
        return []

def web_search(query, max_results=5, retries=1, delay_range=(0.5, 1.5)):
    """三引擎搜索：Tavily → Bocha → DuckDuckGo，带重试+随机延迟，下游无感知"""
    import time, random
    global _search_engine

    def _try_engine(engine_fn, engine_name):
        """单引擎搜索，带重试+随机延迟"""
        for attempt in range(retries + 1):
            try:
                time.sleep(random.uniform(*delay_range))
                result = engine_fn()
                if result is not None and result != []:
                    return result
                if attempt < retries:
                    log.warning(f"  [{engine_name}] 第{attempt+1}次失败或为空，重试...")
            except Exception as e:
                err_str = str(e).lower()
                if 'usage limit' in err_str or 'quota' in err_str or 'exceed' in err_str or 'rate limit' in err_str:
                    log.warning(f"  [{engine_name}] 配额用尽，不再重试")
                    return None  # 配额问题直接切引擎，不重试
                if attempt < retries:
                    log.warning(f"  [{engine_name}] {e}，重试 {attempt+1}/{retries}...")
                else:
                    log.warning(f"  [{engine_name}] 最终失败: {e}")
        return None

    # 引擎1: Tavily
    tavily_result = _try_engine(lambda: _tavily_search(query, max_results), 'Tavily')
    if tavily_result is not None and tavily_result != []:
        _search_engine = 'Tavily'
        return tavily_result

    # 引擎2: Bocha
    bocha_result = _try_engine(lambda: _bocha_search(query, max_results), 'Bocha')
    if bocha_result is not None:
        _search_engine = 'Bocha'
        log.info(f"  → Bocha 搜索成功，{len(bocha_result)}条结果")
        return bocha_result

    # 引擎3: DuckDuckGo 兜底
    ddg_result = _try_engine(lambda: _ddg_search(query, max_results), 'DuckDuckGo')
    if ddg_result:
        _search_engine = 'DuckDuckGo'
        log.info(f"  → DuckDuckGo 搜索成功，{len(ddg_result)}条结果")
        return ddg_result

    _search_engine = None
    log.warning(f"  三个搜索引擎均失败，返回空列表")
    return []

# ═══════════════════════════════════════════
# 【政策类】数据采集
# 覆盖：货币政策、监管政策、产业财政、地缘经贸
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("[STEP] 采集【政策类】数据")
log.info("=" * 60)

policy_data = {}

# ─────────────────────────────────────────────
# 工具函数：执行政策搜索（通用，避免重复代码）
# ─────────────────────────────────────────────
def _search_policy(queries, region_name):
    """执行一组政策查询，返回去重后的政策列表"""
    policies = []
    seen_titles = set()
    for query in queries:
        try:
            results = web_search(query, max_results=3)
            for r in results:
                title = r.get('title', '')[:100]
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    raw = {
                        '标题': title,
                        '内容': r.get('content', ''),
                        '来源': r.get('source', ''),
                        '链接': r.get('url', ''),
                        '时间': r.get('published_date', '')
                    }
                    c = cc.clean_policy_item(raw)
                    if c:
                        policies.append(c)
            log.info(f"  [OK]   {query[:40]}... -> {len(results)}条")
        except Exception as e:
            import traceback
            log.error(f"  [FAIL] {query[:40]}...")
            log.error(f"         {type(e).__name__}: {e}")
            log.error(f"         {traceback.format_exc().strip()}")
    return policies
    return policies

# ═══════════════════════════════════════════
# 【维度一】货币政策：央行利率/官员讲话/流动性工具
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 货币政策")
monetary = []
try:
    monetary = _search_policy([
        f"美联储 FOMC 利率决议 降息 加息 {date_str}",
        f"美联储主席鲍威尔讲话 货币政策 {date_str}",
        f"美联储量化宽松 QT 缩表 流动性 {date_str}",
        f"美国非农 CPI数据 美联储反应 {date_str}",
        f"欧洲央行 ECB 利率决议 加息 降息 {date_str}",
        f"欧洲央行行长拉加德讲话 货币政策 {date_str}",
        f"英国央行 BOE 利率决议 货币政策 {date_str}",
        f"中国央行 降准 降息 LPR {date_str}",
        f"中国央行行长易纲 郭树清讲话 {date_str}",
        f"日本央行 BOJ 负利率 YCC 收益率曲线控制 {date_str}",
        f"日本央行行长植田和男讲话 货币政策 {date_str}",
        f"韩国央行 BOK 利率决议 韩国经济 {date_str}",
        f"韩国央行行长讲话 货币政策 {date_str}",
    ], "货币政策")
    log.info(f"  [OK]   货币政策 -> {len(monetary)}条")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 货币政策: {type(e).__name__}: {e}")
    log.error(f"         {traceback.format_exc().strip()}")

# ═══════════════════════════════════════════
# 【维度二】监管与资本市场政策
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 监管政策")
regulatory = []
try:
    regulatory = _search_policy([
        f"SEC 美国证券交易委员会 监管新规 {date_str}",
        f"美国中概股监管 PCAOB 审计检查 {date_str}",
        f"美国金融稳定监督委员会 系统性风险 {date_str}",
        f"中国证监会 全面注册制 监管 {date_str}",
        f"中国金融监管总局 资管新规 {date_str}",
        f"中国 A股 IPO 并购重组 审核 {date_str}",
        f"香港证监会 港股通 规则调整 {date_str}",
        f"香港金管局 金融市场稳定 {date_str}",
        f"欧洲证券和市场管理局 ESMA 监管 {date_str}",
        f"欧洲金融监管 资本市场法案 {date_str}",
        f"日本金融厅 FSA 金融监管 {date_str}",
        f"日本虚拟货币 加密资产 监管 {date_str}",
        f"韩国金融委员会 FSC 金融监管 {date_str}",
        f"韩国虚拟资产 加密货币 监管框架 {date_str}",
    ], "监管政策")
    log.info(f"  [OK]   监管政策 -> {len(regulatory)}条")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 监管政策: {type(e).__name__}: {e}")
    log.error(f"         {traceback.format_exc().strip()}")

# ═══════════════════════════════════════════
# 【维度三】产业与财政政策
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 产业财政政策")
industrial = []
try:
    industrial = _search_policy([
        f"美国芯片法案 CHIPS Act 半导体补贴 {date_str}",
        f"美国通胀削减法案 IRA 新能源补贴 {date_str}",
        f"美国基建法案 基础设施投资 {date_str}",
        f"欧洲绿色协议 碳关税 Climate {date_str}",
        f"欧洲芯片法案 半导体产业政策 {date_str}",
        f"欧洲经济刺激计划 财政政策 {date_str}",
        f"中国两会 政府工作报告 经济部署 {date_str}",
        f"中国半导体 芯片 自主可控 政策 {date_str}",
        f"中国新能源汽车 光伏 产业政策 {date_str}",
        f"中国房地产 楼市调控 保障房 {date_str}",
        f"中国医药集采 医保谈判 药品政策 {date_str}",
        f"中国消费刺激 以旧换新 补贴 {date_str}",
        f"中国超长期特别国债 财政刺激 {date_str}",
        f"日本经济产业省 METI 产业政策 {date_str}",
        f"日本半导体 芯片产业 扶持政策 {date_str}",
        f"日本新能源 氢能 能源转型政策 {date_str}",
        f"韩国半导体 芯片产业 政府支持 {date_str}",
        f"韩国新能源 汽车电池 产业政策 {date_str}",
    ], "产业财政政策")
    log.info(f"  [OK]   产业财政政策 -> {len(industrial)}条")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 产业财政政策: {type(e).__name__}: {e}")
    log.error(f"         {traceback.format_exc().strip()}")

# ═══════════════════════════════════════════
# 【维度四】地缘与经贸政策
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 地缘经贸政策")
geopolitical = []
try:
    geopolitical = _search_policy([
        f"中美贸易战 关税 贸易摩擦 {date_str}",
        f"中美关系 经济脱钩 科技战 {date_str}",
        f"中美欧 贸易协定 关税谈判 {date_str}",
        f"WTO 世界贸易组织 贸易争端 {date_str}",
        f"区域全面经济伙伴关系协定 RCEP {date_str}",
        f"全面与进步跨太平洋伙伴关系协定 CPTPP {date_str}",
        f"俄乌冲突 欧洲能源 制裁 {date_str}",
        f"中东局势 油价 地缘风险 {date_str}",
        f"台海局势 南海争端 地缘紧张 {date_str}",
        f"美国关税 贸易保护 进出口 {date_str}",
        f"美国债务上限 财政危机 {date_str}",
        f"美国移民政策 H1B 科技人才 {date_str}",
        f"G20峰会 APEC 经济合作 {date_str}",
        f"达沃斯论坛 WEF 全球经济 {date_str}",
        f"一带一路 国际合作 投资 {date_str}",
        f"美联储 财政部 国际金融政策 {date_str}",
    ], "地缘经贸政策")
    log.info(f"  [OK]   地缘经贸政策 -> {len(geopolitical)}条")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 地缘经贸政策: {type(e).__name__}: {e}")
    log.error(f"         {traceback.format_exc().strip()}")

# ═══════════════════════════════════════════
# 按地区合并政策（货币+监管+产业+地缘）
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 整合政策数据")
try:
    def _region_filter(policies, region_keywords):
        result = []
        for p in policies:
            title = p.get('标题', '')
            content = p.get('内容', '')[:200]
            text = title + content
            if any(kw in text for kw in region_keywords):
                result.append(p)
        return result

    us_keywords = ['美国', '美联储', 'Fed', 'SEC', '美国', '美股', '华尔街', '鲍威尔', 'Powell']
    eu_keywords = ['欧洲', '欧元区', '欧盟', '德国', '法国', '英国', 'ECB', 'BOE', 'ESMA', '拉加德', 'Lagarde', '德法', '斯托克']
    cn_keywords = ['中国', '央行', '证监会', '国务院', '发改委', '财政部', '易纲', '北京', '全国两会', '港股通', 'A股', '央行']
    apac_keywords = ['日本', '韩国', '日经', 'BOJ', 'BOK', 'FSA', '日本央行', '韩国央行', '丰田', '三星', '日元', '韩元', '韩元']

    all_policies = monetary + regulatory + industrial + geopolitical
    policy_data = {}
    policy_data['美国'] = cc.batch_clean_policy(_region_filter(all_policies, us_keywords))
    policy_data['欧洲'] = cc.batch_clean_policy(_region_filter(all_policies, eu_keywords))
    policy_data['中国'] = cc.batch_clean_policy(_region_filter(all_policies, cn_keywords))
    policy_data['亚太日本韩国'] = cc.batch_clean_policy(_region_filter(all_policies, apac_keywords))

    market_data['政策动态'] = policy_data
    if policy_data:
        market_data['_meta']['sources']['政策动态'] = f'Web Search ({_search_engine or "Tavily"})'
        log.info(f"  [OK]   政策整合完成")
        for region, items in policy_data.items():
            log.info(f"         {region}: {len(items)}条")
        total_policy = sum(len(v) for v in policy_data.values())
        log.info(f"         合计: {total_policy}条")

    # 增量保存
    try:
        with open(market_data_file, 'w', encoding='utf-8') as f:
            json.dump(market_data, f, ensure_ascii=False, indent=2)
        log.info(f"  [OK]   政策动态已保存")
    except Exception as e:
        log.error(f"  [FAIL] 政策动态保存失败: {e}")

except Exception as e:
    import traceback
    log.error(f"  [FAIL] 整合政策数据: {type(e).__name__}: {e}")
    log.error(f"         {traceback.format_exc().strip()}")

# ═══════════════════════════════════════════
# ═══════════════════════════════════════════
# 【科技企业动态】数据采集
# 仅聚焦全球科技类企业：AI/芯片/互联网/软件/电子
# 剔除：消费、能源、传统工业、传统金融、地产等非科技主体
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("🔍 开始采集【科技企业动态】")
log.info("=" * 60)

enterprise_data = {}

# ─────────────────────────────────────────────
# 科技企业关键词黑名单（过滤非科技内容）
# ─────────────────────────────────────────────
TECH_EXCLUDE_KEYWORDS = [
    # 传统行业
    '石油', '原油', '天然气', '煤炭', '电价', '加油站',
    '房地产', '楼市', '万科', '恒大', '碧桂园', '房价',
    '银行', '保险', '寿险', '财险', '信贷', '储蓄',
    '汽车整车', '燃油车', '二手车', '4S店',
    '煤炭', '钢铁', '水泥', '铝业', '铜业',
    '零售', '超市', '便利店', '电商消费', '餐饮',
    '酒店', '航空', '机场', '旅游', '电影',
    '医药', '医院', '中药', '医疗器械（除科技类）',
    '农业', '化肥', '种子', '猪肉', '养殖',
    # 传统金融
    '摩根大通', '高盛', '花旗', '汇丰', '渣打', '富国银行',
    '工商银行', '建设银行', '农业银行', '中国银行', '交通银行',
    '招商银行', '浦发银行', '兴业银行', '平安银行',
    '中国人寿', '中国平安', '新华保险', '友邦保险',
    # 能源
    '国家电网', '南方电网', '电力公司', '发电集团',
]

# 科技企业白名单关键词（出现即保留）
TECH_INCLUDE_KEYWORDS = [
    '英伟达', 'NVIDIA', 'Nvidia', 'AMD', '英特尔', 'Intel', '苹果', 'Apple',
    '微软', 'Microsoft', '谷歌', 'Google', 'Meta', '亚马逊', 'Amazon', 'AWS',
    '特斯拉', 'Tesla', 'SpaceX', 'OpenAI', 'ChatGPT', '生成式AI',
    '阿里巴巴', 'Alibaba', '腾讯', 'Tencent', '字节跳动', 'ByteDance',
    'TikTok', '百度', 'Baidu', '华为', 'Huawei', '小米', 'Xiaomi',
    '美团', 'Meituan', '京东', 'JD.com', '拼多多', 'Pinduoduo', 'PDD',
    '比亚迪', 'BYD', '宁德时代', 'CATL', '蔚来', '小鹏', '理想汽车',
    '商汤', 'SenseTime', '旷视', 'Megvii', '依图', '寒武纪', '海光',
    '阿里云', '腾讯云', '华为云', '字节云',
    '中芯国际', 'SMIC', '华虹半导体', '华虹', '长江存储', 'YMTC',
    '三星', 'Samsung', 'SK海力士', 'SK Hynix', 'SKHynix',
    'ASML', 'Arm', 'ARM', 'Qualcomm', '高通', '联发科', 'MediaTek',
    '台积电', 'TSMC', '日月光', 'ASE', '环球晶圆', 'Siltronic',
    '博通', 'Broadcom', '德仪', 'TI', '意法半导体', 'STM',
    '索尼', 'Sony', '松下', 'Panasonic', '村田', 'TDK',
    '软银', 'Softbank', 'LINE', 'Naver', 'Kakao',
    '动视', '暴雪', 'Activision', 'Blizzard', 'Epic', 'Unity',
    'Snowflake', 'Databricks', 'Palantir', 'CrowdStrike', 'Palo Alto',
    'Salesforce', 'ServiceNow', 'SAP', 'Oracle', 'Snowflake',
    'GitHub', 'GitLab', 'Atlassian', 'Slack', 'Zoom', 'Figma',
    '台股', '港股', 'A股', '科创', '创业板', '深交所', '上交所',
    'IPO', '上市', '财报', '业绩', '回购', '并购', '收购',
    'AI', '人工智能', '芯片', '半导体', '晶圆', '光刻', '7nm', '3nm', '5nm',
    'GPU', 'CPU', 'HBM', 'H100', 'B100', 'A100',
    '大模型', 'LLM', '模型', '推理', '训练', '算力',
    '智能驾驶', '自动驾驶', 'FSD', 'NOA', '城市NOA',
    '固态电池', '锂电', '动力电池', '储能',
    '机器人', '人形机器人', '具身智能',
]

def _is_tech_item(title, content, source=''):
    """判断一条新闻是否属于科技企业范畴"""
    text = (title + ' ' + content + ' ' + source).lower()
    # 先排除黑名单
    for kw in TECH_EXCLUDE_KEYWORDS:
        if kw.lower() in text:
            return False
    # 再匹配白名单
    for kw in TECH_INCLUDE_KEYWORDS:
        if kw.lower() in text:
            return True
    return False

# ─────────────────────────────────────────────
# 工具函数：执行科技企业搜索
# ─────────────────────────────────────────────
def _search_tech(query, max_results=5):
    """搜索并过滤，只返回科技企业相关内容"""
    try:
        results = web_search(query, max_results=max_results)
        filtered = []
        for r in results:
            title = r.get('title', '')
            content = r.get('content', '')
            source = r.get('source', '')
            if _is_tech_item(title, content, source):
                filtered.append(r)
        return filtered
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] 搜索 [{query[:30]}...]: {type(e).__name__}: {e}")
        log.error(f"         {traceback.format_exc().strip()}")
        return []

# ═══════════════════════════════════════════
# 【美股科技】AI/互联网/芯片/软件/云
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 美股科技企业")
us_tech_queries = [
    f"英伟达 AMD 高通 微软 Meta 科技股 2026年05月",
    f"苹果 谷歌 亚马逊 OpenAI 动态 2026年05月",
    f"AI公司 OpenAI Anthropic Google DeepMind 动态 2026年05月",
    f"英伟达 AMD 高通 博通 芯片动态 2026年05月",
    f"微软 谷歌 Meta 财报回购 2026年05月",
]
us_tech = []
for query in us_tech_queries:
    try:
        results = _search_tech(query, max_results=5)
        for r in results:
            us_tech.append({
                '公司': r.get('title', '').split(':')[0][:50],
                '事件': r.get('content', ''),
                '时间': r.get('published_date', ''),
                '来源': r.get('source', '')
            })
        if results:
            log.info(f"  [OK]   {query[:40]}... -> {len(results)}条")
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] {query[:40]}...: {type(e).__name__}: {e}")

# 去重
seen_us = set()
us_tech_dedup = []
for item in us_tech:
    key = item['公司'] + item['事件'][:30]
    if key not in seen_us:
        seen_us.add(key)
        us_tech_dedup.append(item)
us_tech = us_tech_dedup

enterprise_data['美股科技'] = cc.batch_clean_enterprise(us_tech)
log.info(f"  [OK]   美股科技企业 -> {len(us_tech)}条")

# ═══════════════════════════════════════════
# 【A+H股科技】国内科技互联网/AI/半导体
# ═══════════════════════════════════════════
log.info("\n  [SECTION] A+H股科技企业")
cn_tech_queries = [
    f"阿里巴巴 腾讯 字节跳动 百度 科技动态 2026年05月",
    f"小米 京东 美团 拼多多 财报 动态 2026年05月",
    f"华为 中芯国际 科大讯飞 商汤 科技动态 2026年05月",
    f"宁德时代 比亚迪 蔚来 小鹏 理想 汽车科技 2026年05月",
    f"科创板 创业板 科技公司 上市 2026年05月",
]
cn_tech = []
for query in cn_tech_queries:
    try:
        results = _search_tech(query, max_results=5)
        for r in results:
            cn_tech.append({
                '公司': r.get('title', '').split(':')[0][:50],
                '事件': r.get('content', ''),
                '时间': r.get('published_date', ''),
                '来源': r.get('source', '')
            })
        if results:
            log.info(f"  [OK]   {query[:40]}... -> {len(results)}条")
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] {query[:40]}...: {type(e).__name__}: {e}")

# 去重
seen_cn = set()
cn_tech_dedup = []
for item in cn_tech:
    key = item['公司'] + item['事件'][:30]
    if key not in seen_cn:
        seen_cn.add(key)
        cn_tech_dedup.append(item)
cn_tech = cn_tech_dedup

enterprise_data['A股科技'] = cc.batch_clean_enterprise(cn_tech)
log.info(f"  [OK]   A股科技企业 -> {len(cn_tech)}条")

# ═══════════════════════════════════════════
# 【港股科技】
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 港股科技企业")
hk_tech_queries = [
    f"腾讯 阿里 美团 小米 京东 百度 港股动态 2026年05月",
    f"港股上市公司 并购 重组 动态 2026年05月",
]
hk_tech = []
for query in hk_tech_queries:
    try:
        results = _search_tech(query, max_results=5)
        for r in results:
            hk_tech.append({
                '公司': r.get('title', '').split(':')[0][:50],
                '事件': r.get('content', ''),
                '时间': r.get('published_date', ''),
                '来源': r.get('source', '')
            })
        if results:
            log.info(f"  [OK]   {query[:40]}... -> {len(results)}条")
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] {query[:40]}...: {type(e).__name__}: {e}")

# 去重
seen_hk = set()
hk_tech_dedup = []
for item in hk_tech:
    key = item['公司'] + item['事件'][:30]
    if key not in seen_hk:
        seen_hk.add(key)
        hk_tech_dedup.append(item)
hk_tech = hk_tech_dedup

enterprise_data['港股科技'] = cc.batch_clean_enterprise(hk_tech)
log.info(f"  [OK]   港股科技企业 -> {len(hk_tech)}条")

# ═══════════════════════════════════════════
# 【欧日韩半导体及电子科技】
# ═══════════════════════════════════════════
log.info("\n  [SECTION] 欧日韩半导体/电子科技")
apac_tech_queries = [
    f"ASML ARM 三星 SK海力士 半导体动态 2026年05月",
    f"索尼 软银 东京电子 科技动态 2026年05月",
]
apac_tech = []
for query in apac_tech_queries:
    try:
        results = _search_tech(query, max_results=5)
        for r in results:
            apac_tech.append({
                '公司': r.get('title', '').split(':')[0][:50],
                '事件': r.get('content', ''),
                '时间': r.get('published_date', ''),
                '来源': r.get('source', '')
            })
        if results:
            log.info(f"  [OK]   {query[:40]}... -> {len(results)}条")
    except Exception as e:
        import traceback
        log.error(f"  [FAIL] {query[:40]}...: {type(e).__name__}: {e}")

# 去重
seen_apac = set()
apac_tech_dedup = []
for item in apac_tech:
    key = item['公司'] + item['事件'][:30]
    if key not in seen_apac:
        seen_apac.add(key)
        apac_tech_dedup.append(item)
apac_tech = apac_tech_dedup

enterprise_data['欧日韩科技'] = cc.batch_clean_enterprise(apac_tech)
log.info(f"  [OK]   欧日韩半导体/电子科技 -> {len(apac_tech)}条")

market_data['科技企业动态'] = enterprise_data
total = sum(len(v) for v in enterprise_data.values())
market_data['_meta']['sources']['科技企业动态'] = f'Web Search ({_search_engine or "Tavily"})'
log.info(f"\n  [OK]   科技企业动态收集完成，共 {total} 条")

# 增量保存
try:
    with open(market_data_file, 'w', encoding='utf-8') as f:
        json.dump(market_data, f, ensure_ascii=False, indent=2)
    log.info(f"  [OK]   科技企业动态已保存（{total}条）")
except Exception as e:
    log.error(f"  [FAIL] 企业动态保存失败: {e}")

# ═══════════════════════════════════════════
# 【重要经济日历】当日全球宏观经济数据发布清单
# 仅采集原始数据条目，不做解读，不做分析
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📅 采集【重要经济日历】...")
log.info("=" * 60)

def _build_calendar_query(region_keywords, date_str):
    """按地区构建财经日历查询"""
    return f"{region_keywords} 财经日历 经济数据发布 {date_str}"

calendar_data = []

# ── 经济日历查询（按地区） ──
calendar_regions = [
    ("中国", "中国 PMI CPI PPI GDP 进出口 零售 工业增加值 固定资产投资 失业率 财经日历"),
    ("美国", "US economic calendar CPI PPI GDP jobs payroll unemployment retail ISM PMI FRED"),
    ("欧元区", "Eurozone economic calendar ECB CPI GDP PMI unemployment industrial production"),
    ("日本", "Japan economic calendar BOJ Tankan CPI trade balance GDP industrial production"),
    ("韩国", "Korea economic calendar BOK CPI trade balance GDP unemployment rate"),
    ("澳大利亚", "Australia economic calendar RBA CPI GDP unemployment trade balance"),
]

seen_cal = set()
for region, query_base in calendar_regions:
    full_query = f"{query_base} {date_str}"
    try:
        results = web_search(full_query, max_results=5)
        for r in results:
            title = r.get('title', '')[:100]
            content = r.get('content', '') or r.get('snippet', '')
            if not content:
                continue
            # 去重
            key = title + content[:50]
            if key in seen_cal:
                continue
            seen_cal.add(key)
            # 提取时间（早/午/晚盘）
            time_kw = []
            for kw in ['08:30', '09:30', '10:00', '14:00', '14:30', '15:00', '16:00', '20:30', '21:00', '22:00', '23:00']:
                if kw in content:
                    time_kw.append(kw)
            item = {
                '地区': region,
                '标题': title,
                '摘要': content[:300],
                '来源': r.get('source', ''),
                '时间': r.get('published_date', ''),
                '发布时间点': time_kw[0] if time_kw else '待确认',
            }
            calendar_data.append(item)
        log.info(f"  ✓ {region}经济日历 -> {len(results)}条原始结果")
    except Exception as e:
        log.warning(f"  ✗ {region}经济日历失败: {e}")

# ── 全局财经日历（一次性抓全部） ──
try:
    global_query = f"global economic calendar today {date_str} all countries released"
    results = web_search(global_query, max_results=8)
    for r in results:
        content = r.get('content', '') or r.get('snippet', '')
        title = r.get('title', '')[:100]
        if not content or len(content) < 20:
            continue
        key = title + content[:50]
        if key in seen_cal:
            continue
        seen_cal.add(key)
        time_kw = []
        for kw in ['08:30', '09:30', '10:00', '14:00', '14:30', '15:00', '16:00', '20:30', '21:00', '22:00', '23:00']:
            if kw in content:
                time_kw.append(kw)
        calendar_data.append({
            '地区': '全球',
            '标题': title,
            '摘要': content[:300],
            '来源': r.get('source', ''),
            '时间': r.get('published_date', ''),
            '发布时间点': time_kw[0] if time_kw else '待确认',
        })
    log.info(f"  ✓ 全球经济日历 -> {len(results)}条")
except Exception as e:
    log.warning(f"  ✗ 全球经济日历失败: {e}")

market_data['重要经济日历'] = calendar_data
log.info(f"\n✅ 重要经济日历: 共{len(calendar_data)}条原始条目")

# ═══════════════════════════════════════════
# 【汇总类】每日环球市场速览
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("🔍 生成【汇总类】每日环球市场速览")
log.info("=" * 60)

def get_change_desc(change, magnitude='普通'):
    """涨跌幅转定性描述"""
    if magnitude == '大幅':
        if change > 3: return "大幅收涨"
        if change > 1.5: return "明显上涨"
        if change > 0: return "小幅上涨"
        if change > -1.5: return "小幅回调"
        if change > -3: return "明显下跌"
        return "大幅收跌"
    else:
        if change > 2: return "大涨"
        if change > 0.5: return "收涨"
        if change > -0.5: return "基本持平"
        if change > -2: return "收跌"
        return "大跌"

def get_market_trend(changes):
    """根据多个涨跌幅判断整体趋势"""
    avg = sum(changes) / len(changes) if changes else 0
    if avg > 1.5: return "全线上涨"
    if avg > 0.5: return "整体收高"
    if avg > -0.5: return "涨跌互现"
    if avg > -1.5: return "整体承压"
    return "全线下跌"

def generate_daily_summary():
    """基于已采集的数据生成每日环球市场速览（总结性言论，至少10句话）"""
    mp = market_data.get('市场表现', {})
    ed = market_data.get('经济数据', {})
    summary = []
    
    # 1. 美国股市整体走势
    us_stocks = mp.get('美国股市', {})
    sp500 = us_stocks.get('标普500指数', {})
    nasdaq = us_stocks.get('纳斯达克综合指数', {})
    dow = us_stocks.get('道琼斯工业平均指数', {})
    vix = us_stocks.get('VIX恐慌指数', {})
    
    if sp500 and nasdaq and dow:
        us_changes = [sp500.get('change', 0), nasdaq.get('change', 0), dow.get('change', 0)]
        us_trend = get_market_trend(us_changes)
        nasdaq_vs_sp = "科技股表现强于大盘" if nasdaq.get('change', 0) > sp500.get('change', 0) else "科技股相对疲软"
        summary.append(f"美股三大指数{us_trend}，{get_change_desc(sp500.get('change', 0))}，{nasdaq_vs_sp}，市场情绪整体{get_change_desc(dow.get('change', 0))}。")
    
    # 2. 美债与美元走势
    us_bonds = mp.get('美国债券与外汇', {})
    us10y = us_bonds.get('10年期美债收益率', {})
    dxy = us_bonds.get('美元指数(DXY)', {})
    
    if us10y:
        bond_desc = "大幅上行" if us10y.get('change', 0) > 0.1 else "小幅走高" if us10y.get('change', 0) > 0 else "小幅回落" if us10y.get('change', 0) < -0.05 else "保持平稳"
        summary.append(f"美债收益率{bond_desc}，反映市场对美联储政策路径的重新定价，长端利率波动加大。")
    
    if dxy:
        dxy_desc = "明显走强" if dxy.get('change', 0) > 0.5 else "小幅上涨" if dxy.get('change', 0) > 0 else "小幅走弱" if dxy.get('change', 0) < 0 else "维持震荡"
        summary.append(f"美元指数{dxy_desc}，显示避险需求{get_change_desc(dxy.get('change', 0), '大幅')}，汇率市场波动加剧。")
    
    # 3. 大宗商品与避险资产
    us_commodities = mp.get('美国大宗商品', {})
    wti = us_commodities.get('WTI原油期货', {})
    gold = us_commodities.get('COMEX黄金期货', {})
    
    if wti:
        oil_desc = "大幅反弹" if wti.get('change', 0) > 3 else "温和上涨" if wti.get('change', 0) > 0 else "明显回调" if wti.get('change', 0) < -2 else "窄幅震荡"
        summary.append(f"原油市场{oil_desc}，地缘政治因素与供需预期博弈加剧，国际油价波动区间扩大。")
    
    if gold:
        gold_desc = "强势上涨" if gold.get('change', 0) > 1 else "温和走高" if gold.get('change', 0) > 0 else "承压回落" if gold.get('change', 0) < -1 else "横盘整理"
        summary.append(f"黄金作为避险资产{gold_desc}，在通胀预期与美元走势交织影响下，贵金属板块表现分化。")
    
    # 4. A股市场整体表现
    cn_stocks = mp.get('A股', {})
    sh = cn_stocks.get('上证指数', {})
    cy = cn_stocks.get('创业板指', {})
    
    if sh and cy:
        cn_trend = get_market_trend([sh.get('change', 0), cy.get('change', 0)])
        growth_vs_main = "成长股领跌" if cy.get('change', 0) < sh.get('change', 0) else "科技股相对抗跌"
        summary.append(f"A股市场{get_change_desc(sh.get('change', 0))}，{cn_trend}，{growth_vs_main}，成交量维持温和水平。")
    
    # 5. 港股市场
    hk_stocks = mp.get('港股', {})
    hsi = hk_stocks.get('恒生指数', {})
    hst = hk_stocks.get('恒生科技指数', {})
    
    if hsi:
        hk_desc = "延续反弹" if hsi.get('change', 0) > 1 else "小幅收涨" if hsi.get('change', 0) > 0 else "承压调整" if hsi.get('change', 0) < -1 else "窄幅震荡"
        tech_desc = "科技股大幅波动" if hst and abs(hst.get('change', 0)) > 2 else "科技股表现相对平稳"
        summary.append(f"港股市场{hk_desc}，外资{get_change_desc(hsi.get('change', 0))}，{tech_desc}，市场流动性有所改善。")
    
    # 6. 欧洲股市
    eu_stocks = mp.get('欧洲股市', {})
    dax = eu_stocks.get('德国DAX 30', {})
    ftse = eu_stocks.get('英国富时100', {})
    
    if dax and ftse:
        eu_changes = [dax.get('change', 0), ftse.get('change', 0)]
        eu_trend = get_market_trend(eu_changes)
        uk_vs_eu = "英国股市相对疲软" if ftse.get('change', 0) < dax.get('change', 0) else "英股表现优于欧陆"
        summary.append(f"欧洲股市{eu_trend}，{uk_vs_eu}，能源板块与金融股分化明显，市场对欧央行政策预期修正。")
    
    # 7. 亚太市场
    apac_stocks = mp.get('亚太股市', {})
    n225 = apac_stocks.get('日经225指数', {})
    ks = apac_stocks.get('韩国综合指数', {})
    
    if n225 and ks:
        jp_desc = "强势上涨" if n225.get('change', 0) > 1 else "温和收涨" if n225.get('change', 0) > 0 else "明显调整"
        kr_desc = "跟随上涨" if ks.get('change', 0) > 0 and n225.get('change', 0) > 0 else "走势分化"
        summary.append(f"亚太市场方面，日股{jp_desc}，韩股{kr_desc}，亚洲新兴市场整体表现优于发达市场。")
    
    # 8. 外汇与汇率
    cn_fm = mp.get('中国外汇与贵金属', {})
    usdcny = cn_fm.get('USD/CNY', {})
    
    if usdcny:
        fx_desc = "小幅升值" if usdcny.get('change', 0) < 0 else "小幅贬值" if usdcny.get('change', 0) > 0 else "维持稳定"
        summary.append(f"人民币汇率{fx_desc}，在美元指数波动与贸易数据影响下，外汇市场整体保持平稳。")
    
    # 9. 宏观经济数据解读
    cn_econ = ed.get('中国', {})
    cn_pmi = cn_econ.get('制造业PMI', {}).get('数值', 50) if cn_econ else 50
    
    if cn_pmi > 50:
        pmi_desc = "扩张势头延续" if cn_pmi > 51 else "温和复苏"
    else:
        pmi_desc = "收缩压力加大" if cn_pmi < 49 else "边际改善"
    summary.append(f"中国制造业PMI显示经济{pmi_desc}，内需修复与外需扰动并存，稳增长政策仍有发力空间。")
    
    # 10. 政策与市场影响
    policy_items = []
    for region, items in market_data.get('政策动态', {}).items():
        for item in items[:1]:
            if item.get('标题'):
                policy_items.append(region)
    
    if policy_items:
        policy_regions = "、".join(policy_items[:3])
        summary.append(f"政策面来看，{policy_regions}等地监管机构发布重要政策指引，市场对这些政策动向反应积极，政策预期成为短期市场波动的重要驱动因素。")
    else:
        summary.append("政策面保持相对平稳，市场聚焦于企业财报季与经济数据发布，政策预期对资产定价的影响趋于中性。")
    
    # 11. 市场情绪与展望
    if vix:
        if vix.get('price', 0) > 25:
            summary.append("市场情绪方面，恐慌指数高位运行显示投资者风险偏好明显下降，短期波动性可能持续，建议关注防御性资产配置。")
        elif vix.get('price', 0) < 15:
            summary.append("市场情绪方面，恐慌指数处于低位表明投资者情绪较为乐观，但需警惕低波动环境下的潜在风险积聚。")
        else:
            summary.append("市场情绪方面，投资者保持相对理性，风险偏好维持在均衡水平，预计短期市场将以结构性行情为主。")
    
    # 12. 全球宏观展望（结论放最前面）
    conclusion = "综合来看，全球主要市场在通胀预期、货币政策与地缘政治等多重因素交织下呈现分化走势，投资者需关注美联储政策路径与中国经济复苏进程的边际变化。"
    
    # 将结论移至最前面，重排句子顺序
    sentences_without_conclusion = [s for s in summary if conclusion not in s]
    final_summary = [conclusion] + sentences_without_conclusion
    
    return {
        '更新时间': datetime.datetime.now().isoformat(),
        '句子数': len(final_summary),
        '段落列表': final_summary,
        '概述': conclusion
    }

log.info(f"\n  [SECTION] 每日环球市场速览")
try:
    summary_data = generate_daily_summary()
    market_data['环球市场速览'] = summary_data
    market_data['_meta']['supplement_time'] = datetime.datetime.now().isoformat()
    log.info(f"  [OK] 速览生成 -> {summary_data.get('句子数', 0)} 句话")
    for i, sentence in enumerate(summary_data.get('段落列表', []), 1):
        log.info(f"      {i}. {sentence[:80]}...")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 每日环球市场速览生成失败: {e}")
    log.error(f"         {traceback.format_exc().strip()}")
    market_data['环球市场速览'] = {}

# ═══════════════════════════════════════════
# 今日经济数据日历
# ═══════════════════════════════════════════
log.info(f"\n  [SECTION] 今日经济数据日历")
try:
    calendar_results = web_search(f"今日经济数据日历 {config.REPORT_DATE}", max_results=5)
    raw_items = []
    for r in calendar_results:
        raw_items.append({
            '时间': r.get('title', ''),
            '事件': r.get('content', '')
        })
    cleaned = cc.batch_clean_calendar(raw_items)
    market_data['经济数据']['今日经济数据日历'] = cleaned
    log.info(f"  [OK] 经济数据日历 -> {len(cleaned)}条")
except Exception as e:
    import traceback
    log.error(f"  [FAIL] 经济数据日历采集失败: {e}")
    log.error(f"         {traceback.format_exc().strip()}")
    market_data['经济数据']['今日经济数据日历'] = []

# ═══════════════════════════════════════════
# 保存完整数据
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("💾 保存完整数据...")
log.info("=" * 60)

try:
    with open(market_data_file, 'w', encoding='utf-8') as f:
        json.dump(market_data, f, ensure_ascii=False, indent=2)
    log.info(f"✅ 完整数据已保存: {market_data_file}")
except Exception as e:
    log.error(f"❌ 保存失败: {e}")
    sys.exit(1)

# ═══════════════════════════════════════════
# 【最终汇总报告】
# ═══════════════════════════════════════════
log.info("\n" + "=" * 60)
log.info("📊 【Step 2 任务汇总报告】")
log.info("=" * 60)

# 各section统计
sections_ok = []
sections_fail = []

for region, data in market_data.get('政策动态', {}).items():
    if data:
        sections_ok.append(f"政策-{region}")
    else:
        sections_fail.append(f"政策-{region}")

total_ent = sum(len(v) for v in market_data.get('科技企业动态', {}).values())
if total_ent > 0:
    sections_ok.append(f"科技企业动态({total_ent}条)")
else:
    sections_fail.append("科技企业动态")

if market_data.get('环球市场速览', {}).get('句子数', 0) > 0:
    sections_ok.append("环球市场速览")
else:
    sections_fail.append("环球市场速览")

if market_data.get('经济数据', {}).get('今日经济数据日历'):
    sections_ok.append("经济日历")
else:
    sections_fail.append("经济日历")

# 输出汇总
log.info("\n  ✅ 成功任务:")
for s in sections_ok:
    log.info(f"     • {s}")

if sections_fail:
    log.info("\n  ❌ 失败/空任务:")
    for s in sections_fail:
        log.info(f"     • {s}")

log.info("\n【数据统计】")
log.info(f"  政策动态: {sum(len(v) for v in market_data.get('政策动态', {}).values())}条")
log.info(f"  科技企业动态: {total_ent}条")
log.info(f"  环球市场速览: {market_data.get('环球市场速览', {}).get('句子数', 0)}句")

log.info("\n" + "=" * 60)
log.info("🎉 Step 2 数据采集完成！")
log.info("=" * 60)
