#!/usr/bin/env python3
"""
宏观经济分析脚本
===========================
获取宏观经济数据并进行经济周期评估，为个股分析提供宏观背景。

数据源：AkShare（免费，无需 API Key） + web_search 补充 + fetch_trending.py 时政热点

功能模块：
  1. 利率数据：LPR、Shibor
  2. 通胀数据：CPI、PPI
  3. PMI 数据：制造业 / 非制造业
  4. 社融与货币：社融规模、M2 增速
  5. 经济周期判断：基于多指标综合评分
  6. 宏观仪表盘：一键获取全部关键指标
  7. 全网时政热点分类：广覆盖分类 + 时效性过滤
  8. 日期感知与时效过滤：结合对话实时日期过滤旧新闻
  9. 内容时效性深度判断：识别财报/季报/年报所属时期
  10. 严格时效性过滤：基于"当前应关注的财务时期"精确过滤，
      杜绝过期财报；扩大数据关键词覆盖范围；增加独立年份引用检测
  11. 预测类内容排除 + 季报精细化：
      识别预测/展望/预期类文章，其引用的未来时间不作为有效数据；
      财报匹配精细化（半年报/中报/全年业绩等更多表述）
  12. 热点关键词提取 + 动态搜索建议：
      从分类热点中提取高频实体关键词（地名/事件/人名/组织等），
      自动生成"热点驱动的动态搜索建议"，弥补静态搜索词的覆盖盲区；
      新增事件→行业→个股影响传导链分析框架
  13. 新闻去重 + 结构化保存：
      classify_trending 新增标题相似度去重（Jaccard + 核心实体匹配），
      避免多条新闻描述同一事件被重复分析；
      新增 export_news_json() 将结构化新闻保存为独立 JSON 文件
  14. 去重增强 + 新闻结构化改进：
      三层去重策略（Jaccard 2-gram / 核心实体重叠 / 短标题包含）；
      export_news_json 字段完善（time 优先取 item 自身时间）；
      核心实体关键词表扩充
  15. 严格时效性过滤：
      年报最多保留最近1个完整年度；半年报/季报只保留当前应关注的1个周期；
      财务关键词日期窗口缩短至约1年；独立年份引用过滤缩短至1年
  16. 财报匹配增强：
      report_period_patterns 增加"财报"关键词匹配（"YYYY年财报"视为年报）

用法：
    python macro_analysis.py --dashboard --output macro.json
    python macro_analysis.py --dashboard --trending-json trending.json --output macro.json
    python macro_analysis.py --dashboard --reference-date 2026-03-03 --news-max-age-days 30 --output macro.json
    python macro_analysis.py --rates --output rates.json
    python macro_analysis.py --cycle --output cycle.json
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _safe_float(val):
    """安全转换为 float"""
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _direction(values, lookback=6):
    """判断趋势方向：rising / falling / stable"""
    valid = [v for v in values if v is not None]
    if len(valid) < 2:
        return 'insufficient_data'
    recent = valid[-lookback:]
    if len(recent) < 2:
        return 'insufficient_data'
    change = (recent[-1] - recent[0]) / abs(recent[0]) if recent[0] != 0 else 0
    if change > 0.03:
        return 'rising'
    elif change < -0.03:
        return 'falling'
    return 'stable'


def _output_json(data, output_path=None):
    """输出 JSON 数据"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if output_path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json_str, encoding='utf-8')
        logger.info(f'✅ 数据已保存: {output_path}')
    print(json_str)


# ---------------------------------------------------------------------------
# 利率数据
# ---------------------------------------------------------------------------

def fetch_rates():
    """获取中国利率数据（LPR、Shibor）"""
    import akshare as ak

    result = {}

    # LPR
    try:
        df = ak.macro_china_lpr()
        if df is not None and not df.empty:
            recent = df.tail(12)
            lpr_1y = []
            lpr_5y = []
            for _, row in recent.iterrows():
                lpr_1y.append({
                    'date': str(row.get('TRADE_DATE', '')),
                    'value': _safe_float(row.get('LPR1Y')),
                })
                lpr_5y.append({
                    'date': str(row.get('TRADE_DATE', '')),
                    'value': _safe_float(row.get('LPR5Y')),
                })
            result['lpr_1y'] = {
                'latest': lpr_1y[-1]['value'] if lpr_1y else None,
                'direction': _direction([e['value'] for e in lpr_1y]),
                'series': lpr_1y,
                'interpretation': '1年期LPR影响短期贷款和消费信贷成本',
            }
            result['lpr_5y'] = {
                'latest': lpr_5y[-1]['value'] if lpr_5y else None,
                'direction': _direction([e['value'] for e in lpr_5y]),
                'series': lpr_5y,
                'interpretation': '5年期LPR影响房贷利率和长期融资成本',
            }
    except Exception as e:
        result['lpr'] = {'error': str(e)}

    # Shibor
    try:
        df = ak.rate_interbank(
            market='上海银行间同业拆放利率(Shibor)',
            symbol='隔夜',
            indicator='利率'
        )
        if df is not None and not df.empty:
            recent = df.tail(30)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]) if len(row) > 0 else '',
                    'value': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            result['shibor_overnight'] = {
                'latest': records[-1]['value'] if records else None,
                'direction': _direction([e['value'] for e in records]),
                'interpretation': '隔夜Shibor反映银行间流动性松紧',
            }
    except Exception:
        result['shibor_overnight'] = {'note': '数据暂不可用'}

    return result


# ---------------------------------------------------------------------------
# 通胀数据
# ---------------------------------------------------------------------------

def fetch_inflation():
    """获取中国通胀数据（CPI、PPI）"""
    import akshare as ak

    result = {}

    # CPI
    try:
        df = ak.macro_china_cpi_monthly()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]),
                    'cpi_yoy': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            latest = records[-1]['cpi_yoy'] if records else None
            result['cpi'] = {
                'latest': latest,
                'direction': _direction([e['cpi_yoy'] for e in records]),
                'series': records,
                'interpretation': (
                    'CPI同比上涨，通胀压力增加' if latest and latest > 3
                    else 'CPI温和，通胀可控' if latest and latest > 0
                    else 'CPI为负，存在通缩风险' if latest and latest < 0
                    else 'CPI数据正常'
                ),
            }
    except Exception as e:
        result['cpi'] = {'error': str(e)}

    # PPI
    try:
        df = ak.macro_china_ppi_monthly()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]),
                    'ppi_yoy': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            latest = records[-1]['ppi_yoy'] if records else None
            result['ppi'] = {
                'latest': latest,
                'direction': _direction([e['ppi_yoy'] for e in records]),
                'series': records,
                'interpretation': (
                    '工业品出厂价格上涨，上游成本压力传导' if latest and latest > 3
                    else 'PPI温和上涨' if latest and latest > 0
                    else 'PPI通缩，上游需求疲弱' if latest and latest < 0
                    else 'PPI数据正常'
                ),
            }
    except Exception as e:
        result['ppi'] = {'error': str(e)}

    return result


# ---------------------------------------------------------------------------
# PMI 数据
# ---------------------------------------------------------------------------

def fetch_pmi():
    """获取中国 PMI 数据"""
    import akshare as ak

    result = {}

    try:
        df = ak.macro_china_pmi()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]),
                    'manufacturing_pmi': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                    'non_manufacturing_pmi': _safe_float(row.iloc[2]) if len(row) > 2 else None,
                })
            mfg = records[-1]['manufacturing_pmi'] if records else None
            non_mfg = records[-1]['non_manufacturing_pmi'] if records else None
            result['manufacturing_pmi'] = {
                'latest': mfg,
                'direction': _direction([e['manufacturing_pmi'] for e in records]),
                'above_50': mfg > 50 if mfg else None,
                'interpretation': (
                    f'制造业PMI={mfg}，' + ('处于扩张区间，制造业景气' if mfg and mfg > 50 else '低于荣枯线，制造业收缩')
                ) if mfg else '数据不可用',
                'series': records,
            }
            if non_mfg:
                result['non_manufacturing_pmi'] = {
                    'latest': non_mfg,
                    'above_50': non_mfg > 50,
                    'interpretation': (
                        f'非制造业PMI={non_mfg}，' + ('服务业景气' if non_mfg > 50 else '服务业走弱')
                    ),
                }
    except Exception as e:
        result['manufacturing_pmi'] = {'error': str(e)}

    return result


# ---------------------------------------------------------------------------
# 社融与货币供应
# ---------------------------------------------------------------------------

def fetch_social_financing():
    """获取社融规模与 M2 增速"""
    import akshare as ak

    result = {}

    # 社融
    try:
        df = ak.macro_china_shrzgm()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]),
                    'value': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            result['social_financing'] = {
                'latest': records[-1]['value'] if records else None,
                'direction': _direction([e['value'] for e in records]),
                'series': records,
                'interpretation': '社融增速上升代表信用扩张、流动性宽松；下降则信用收紧',
            }
    except Exception as e:
        result['social_financing'] = {'error': str(e)}

    # M2
    try:
        df = ak.macro_china_m2_monthly()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    'date': str(row.iloc[0]),
                    'm2_yoy': _safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            result['m2_growth'] = {
                'latest': records[-1]['m2_yoy'] if records else None,
                'direction': _direction([e['m2_yoy'] for e in records]),
                'series': records,
                'interpretation': 'M2增速反映货币供应量变化，上升表示流动性宽松',
            }
    except Exception as e:
        result['m2_growth'] = {'error': str(e)}

    return result


# ---------------------------------------------------------------------------
# 经济周期评估
# ---------------------------------------------------------------------------

def assess_business_cycle():
    """
    综合评估当前中国经济周期阶段。

    阶段定义：
      - recovery（复苏期）：PMI回升>50，信用扩张，政策宽松
      - expansion（扩张期）：PMI高位，增长稳定
      - contraction（收缩期）：PMI<50，PPI通缩
      - transition（过渡期）：信号混合
    """
    logger.info('正在评估经济周期...')

    inflation = fetch_inflation()
    pmi_data = fetch_pmi()
    financing = fetch_social_financing()

    signals = {}

    # PMI 信号
    mfg_pmi = pmi_data.get('manufacturing_pmi', {})
    pmi_latest = mfg_pmi.get('latest')
    pmi_dir = mfg_pmi.get('direction', 'stable')
    signals['pmi'] = {
        'value': pmi_latest,
        'direction': pmi_dir,
        'expanding': pmi_latest > 50 if pmi_latest else None,
    }

    # 通胀信号
    cpi_latest = inflation.get('cpi', {}).get('latest')
    ppi_latest = inflation.get('ppi', {}).get('latest')
    signals['cpi'] = {'value': cpi_latest, 'direction': inflation.get('cpi', {}).get('direction')}
    signals['ppi'] = {'value': ppi_latest, 'direction': inflation.get('ppi', {}).get('direction')}

    # 信用信号
    sf = financing.get('social_financing', {})
    sf_dir = sf.get('direction', 'stable')
    m2 = financing.get('m2_growth', {})
    m2_dir = m2.get('direction', 'stable')
    signals['credit'] = {'social_financing_direction': sf_dir, 'm2_direction': m2_dir}

    # 阶段判定
    pmi_expanding = pmi_latest and pmi_latest > 50
    pmi_rising = pmi_dir == 'rising'
    credit_expanding = sf_dir == 'rising' or m2_dir == 'rising'

    if pmi_expanding and pmi_rising and credit_expanding:
        phase = 'recovery'
        description = '经济复苏期：PMI回升，信用扩张，政策宽松'
        favored = ['消费', '科技', '金融', '地产']
        disfavored = ['公用事业', '防御板块']
        market_impact = '复苏期通常有利于风险资产，成长股和周期股表现较好'
    elif pmi_expanding and not pmi_rising:
        phase = 'expansion'
        description = '经济扩张期：PMI维持高位，增长稳定'
        favored = ['制造业', '周期股', '金融', '材料']
        disfavored = ['防御板块', '公用事业']
        market_impact = '扩张期盈利增长强劲，关注估值合理的龙头'
    elif not pmi_expanding and ppi_latest and ppi_latest < 0:
        phase = 'contraction'
        description = '经济收缩期：PMI低于50，PPI通缩'
        favored = ['消费防御', '公用事业', '高股息', '医药']
        disfavored = ['周期股', '地产', '材料']
        market_impact = '收缩期应以防御为主，关注高股息和必选消费'
    else:
        phase = 'transition'
        description = '过渡期：经济信号混合，方向不明确'
        favored = ['均衡配置']
        disfavored = []
        market_impact = '信号混合时应降低仓位、分散配置，等待趋势明朗'

    return {
        'phase': phase,
        'description': description,
        'signals': signals,
        'sector_implications': {
            'favored': favored,
            'disfavored': disfavored,
        },
        'market_impact': market_impact,
        'factor_implications': {
            'recovery': '小盘、动量因子占优',
            'expansion': '质量、成长因子占优',
            'contraction': '低波动、红利因子占优',
            'transition': '均衡配置各因子',
        }.get(phase, ''),
        'policy_direction': (
            '宽松（降息降准预期）' if phase in ('contraction', 'recovery')
            else '中性偏紧' if phase == 'expansion'
            else '不确定'
        ),
    }


# ---------------------------------------------------------------------------
# 国际市场概览（通过 web_search 指令生成）
# ---------------------------------------------------------------------------

def generate_global_search_queries(stock_name='', industry=''):
    """
    生成宏观与国际事件相关的 web_search 搜索指令。
    Agent 应依次执行这些搜索，将结果整合到分析中。

    Returns:
        list of dict: 每个包含 dimension, query, explanation
    """
    current_year = datetime.now().year
    queries = [
        {
            'dimension': '宏观经济政策',
            'query': f'中国 宏观经济 政策 {current_year}',
            'explanation': '了解当前宏观经济政策方向（货币政策、财政政策）',
        },
        {
            'dimension': '央行动态',
            'query': f'中国人民银行 利率 降准 降息 {current_year}',
            'explanation': '获取央行最新货币政策操作',
        },
        {
            'dimension': '国际局势',
            'query': f'国际局势 地缘政治 贸易摩擦 {current_year}',
            'explanation': '了解影响市场的国际地缘政治事件',
        },
        {
            'dimension': '全球市场联动',
            'query': f'美股 欧股 全球市场 走势 {current_year}',
            'explanation': '了解全球主要市场走势及联动效应',
        },
        {
            'dimension': '大宗商品',
            'query': f'原油 黄金 铜 大宗商品 价格 {current_year}',
            'explanation': '了解大宗商品价格变化及对相关行业的影响',
        },
        {
            'dimension': '汇率与资金流向',
            'query': f'人民币汇率 北向资金 外资流向 {current_year}',
            'explanation': '了解汇率变化和外资流向对A股的影响',
        },
    ]

    # 如果有具体行业，增加行业政策搜索
    if industry:
        queries.append({
            'dimension': '行业政策',
            'query': f'{industry} 产业政策 补贴 监管 {current_year}',
            'explanation': f'了解{industry}行业最新政策和监管动态',
        })

    # 如果有具体公司，增加公司国际化相关搜索
    if stock_name:
        queries.append({
            'dimension': '公司国际化',
            'query': f'{stock_name} 海外业务 出口 国际化 制裁',
            'explanation': f'了解{stock_name}的国际化布局和潜在的地缘政治风险',
        })

    return queries


# ---------------------------------------------------------------------------
# 时政热点分类与筛选（广覆盖 + 时效性过滤）
# ---------------------------------------------------------------------------

def load_trending_data(trending_json_path):
    """
    加载 fetch_trending.py 脚本采集的时政热点数据。

    Agent 通过 fetch_trending.py 脚本（直接从各平台公开接口采集热榜数据）
    获取热点后，将结果通过 --trending-json 传入。

    Expected JSON format:
    {
        "sources": [
            {
                "source": "xueqiu",
                "source_name": "雪球财经",
                "items": [
                    {"title": "标题", "url": "链接", "hot": 12345},
                    ...
                ]
            },
            {
                "source": "toutiao",
                "source_name": "今日头条",
                "items": [...]
            }
        ],
        "fetch_time": "2026-03-02T10:30:00"
    }
    """
    if not trending_json_path:
        return None
    p = Path(trending_json_path)
    if not p.exists():
        logger.warning(f'时政热点文件不存在: {trending_json_path}')
        return None
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        logger.info(f'已加载时政热点数据: {trending_json_path}')
        return data
    except Exception as e:
        logger.warning(f'加载时政热点数据失败: {e}')
        return None


def _check_freshness(trending_data, max_age_hours=48, reference_date=None):
    """
    检查热点数据的时效性。

    Args:
        trending_data: 热点数据
        max_age_hours: 最大时效（小时），超过此时间的数据会标记为过期
        reference_date: 参考日期（datetime），用于计算时效。默认为当前时间。

    Returns:
        tuple: (is_fresh, age_hours, fetch_time_str)
    """
    now = reference_date if reference_date else datetime.now()
    fetch_time_str = trending_data.get('fetch_time', trending_data.get('fetched_at', ''))
    if not fetch_time_str:
        return True, 0, ''

    try:
        for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S'):
            try:
                fetch_time = datetime.strptime(fetch_time_str, fmt)
                break
            except ValueError:
                continue
        else:
            return True, 0, fetch_time_str

        age = now - fetch_time
        age_hours = age.total_seconds() / 3600
        return age_hours <= max_age_hours, age_hours, fetch_time_str
    except Exception:
        return True, 0, fetch_time_str


def _compute_relevant_fiscal_period(reference_date=None):
    """
    根据参考日期计算当前应关注的财务时期（供时效性过滤使用）。

    严格版：
    - 年报最多只保留最近1个完整年度（不再接受更早的年报）
    - 半年报/季报只保留当前应关注的那1个季度，不接受更早的季报
    - 返回 (最新相关年份, 最新相关季度结束月份) 的列表

    逻辑：
    - 1-4月：关注 上一年年报（Y-1 Q4）+ 当年Q1预期
    - 5-8月：关注 当年Q1（Y Q1）+ 当年半年报
    - 9-10月：关注 当年半年报（Y Q2）+ 三季报
    - 11-12月：关注 当年三季报（Y Q3）+ 全年预期

    注意：对于 1-4月场景，上一年的 Q1/Q2/Q3 数据虽然年份 = Y-1，
    但它们不在 relevant_periods 中，只有 (Y-1, 12) 即年报才有效。
    """
    now = reference_date if reference_date else datetime.now()
    y = now.year
    m = now.month

    if m <= 4:
        # 1-4月：最新有效数据 = 上一年年报(Q4) + 当年Q1
        return [(y - 1, 12), (y, 3)]
    elif m <= 8:
        # 5-8月：最新有效数据 = 当年Q1 + 当年半年报
        return [(y, 3), (y, 6)]
    elif m <= 10:
        # 9-10月：最新有效数据 = 当年半年报 + 三季报
        return [(y, 6), (y, 9)]
    else:
        # 11-12月：最新有效数据 = 当年三季报 + 全年预期
        return [(y, 9), (y, 12)]


def _max_fiscal_age_for_period(report_quarter_end):
    """根据财报类型返回最大允许的时间跨度。

    - 年报（Q4, month=12）：最多保留1个完整年度的年报
    - 半年报（Q2, month=6）：最多保留1个半年报周期
    - 季报（Q1/Q3, month=3/9）：最多保留1个季度周期

    Returns:
        int: 该类型财报允许的最大回看期数（以季度为单位，1=只看当期）
    """
    if report_quarter_end == 12:
        return 1  # 年报：只看最近1个年报
    elif report_quarter_end == 6:
        return 1  # 半年报：只看最近1个半年报
    else:
        return 1  # 季报：只看最近1个季报


def _is_news_within_period(title, max_age_days=30, reference_date=None):
    """
    根据新闻标题中的日期和内容时期线索判断是否在有效期内。

    不仅检查标题中的日期模式，还识别内容所属的财务/经济时期。

    改进（预测类排除 + 季报精细化）：
    - 新增：识别预测/展望/预期类内容，其中提及的**未来时间点不作为有效数据引用**
      （如"预计2027年营收"、"展望2030年行业规模"等属于预测，不等于已发布的真实数据）
    - 财报匹配精细化：半年报、中报与 Q2 合并；前三季度与 Q3 合并；
      识别"YYYY年全年业绩"等年度表述
    - 年度数据同理：只有最近1-2个完整年度的数据才有效
    - 显式日期匹配更严格：超过 max_age_days 即过滤
    - 独立年份引用过滤：距今超过2年的旧数据直接过滤

    判断逻辑：
    1. 预测/展望类内容检测：含预测关键词 + 未来年份 → 标记为预测，不作为真实数据
    2. 显式日期匹配：标题中的 "YYYY年MM月" / "YYYY-MM-DD" 等
    3. 财报时期匹配：识别 "YYYY年Q1/半年报/三季报/年报" 等，
       与当前应关注的财务时期对比
    4. 纯年份数据匹配：识别 "YYYY年" + 数据关键词
    5. 纯年份引用匹配：识别标题中独立出现的年份数字

    Args:
        title: 新闻标题
        max_age_days: 最大有效天数（发布日期维度）
        reference_date: 参考日期

    Returns:
        bool: True 表示新闻有效（在有效期内或无法判断），False 表示明显过时
    """
    import re

    now = reference_date if reference_date else datetime.now()
    cutoff = now - timedelta(days=max_age_days)

    # 计算当前应关注的最新财务时期
    relevant_periods = _compute_relevant_fiscal_period(now)
    # relevant_periods 形如 [(2025, 12), (2026, 3)]，表示最新相关季度

    # 允许的最老数据年份（当前年 - 1 年的数据仍可能有效，再往前就过时了）
    min_relevant_year = now.year - 1

    # ---- 第零层：预测/展望类内容检测 ----
    # 含预测关键词且引用的是未来年份时，其时间点不能作为有效数据参考。
    # 例如："预计2027年营收突破千亿" → 2027年是预测，不是已发布数据
    # 但"预计2025年年报将于3月发布" → 这是对即将发布数据的预告，仍有参考价值
    forecast_keywords = re.compile(
        r'预计|预测|预期|展望|前瞻|预判|目标|规划|愿景|远景|'
        r'有望|或将|将会|料将|可能达到|力争|计划|拟|瞄准'
    )
    if forecast_keywords.search(title):
        # 检查标题中是否引用了未来年份（> 当前年份）
        future_year_pattern = r'(\d{4})\s*年'
        for match in re.finditer(future_year_pattern, title):
            try:
                mentioned_year = int(match.group(1))
                if mentioned_year > now.year:
                    # 标题中含预测关键词 + 引用了未来年份
                    # 这类内容的年份数据是预测值，不能作为已发布真实数据引用
                    # 但文章本身可能仍有参考意义（如行业趋势），不做过滤
                    # 只需确保后续层不会误将预测年份当作有效数据年份
                    pass
            except (ValueError, OverflowError):
                continue

        # 如果预测内容引用的数据年份是过去的（如"预计2024年盈利增长"在2026年看），
        # 则该预测本身已过时，直接过滤
        for match in re.finditer(future_year_pattern, title):
            try:
                mentioned_year = int(match.group(1))
                if mentioned_year < now.year - 1 and mentioned_year > 2000:
                    # 对过去年份的预测/预期，在当前时间点已是旧信息
                    context_start = max(0, match.start() - 10)
                    context_end = min(len(title), match.end() + 20)
                    context = title[context_start:context_end]
                    if forecast_keywords.search(context):
                        return False
            except (ValueError, OverflowError):
                continue

    # ---- 第一层：显式日期匹配 ----
    # 注意：对于包含财务数据关键词的标题，跳过此层的日期过滤，
    # 让第二/三层更精确的财务时期判断来处理
    financial_keywords = re.compile(
        r'财报|年报|季报|半年报|中报|业绩|营收|净利|利润|分红|派息|GDP|'
        r'ROE|ROA|毛利|净资产|经济数据|统计|产值|销量'
    )
    has_financial_context = bool(financial_keywords.search(title))

    date_patterns = [
        (r'(\d{4})年(\d{1,2})月(\d{1,2})[日号]', lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (r'(\d{4})年(\d{1,2})月', lambda m: datetime(int(m.group(1)), int(m.group(2)), 1)),
        (r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})', lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
        (r'(\d{4})[.\-/](\d{1,2})', lambda m: datetime(int(m.group(1)), int(m.group(2)), 1)),
    ]

    if not has_financial_context:
        for pattern, parser in date_patterns:
            match = re.search(pattern, title)
            if match:
                try:
                    news_date = parser(match)
                    if news_date < cutoff:
                        return False
                except (ValueError, OverflowError):
                    continue
    else:
        # 严格化：含财务关键词时，过滤超过1年的日期（从730天缩短为400天）
        for pattern, parser in date_patterns:
            match = re.search(pattern, title)
            if match:
                try:
                    news_date = parser(match)
                    financial_cutoff = now - timedelta(days=400)
                    if news_date < financial_cutoff:
                        return False
                except (ValueError, OverflowError):
                    continue

    # ---- 第二层：财报/经济数据时期匹配（严格版）----
    # 不再用简单的 grace_days，而是精确判断：
    # 该财报时期是否属于 "当前应关注的财务时期" 之一。
    # 如果比最老的相关时期还早，则视为过时。
    report_period_patterns = [
        # Q1 / 一季度 / 一季报 / 第一季度 / 一季度营收 / 一季度业绩
        (r'(\d{4})\s*年?\s*(?:Q1|一季[度报]|第一季[度报]|1季[度报]|第1季[度报])',
         lambda y: (y, 3)),
        # "YYYY年一季度" 后跟数据关键词（匹配"2025年一季度营收"等变体）
        (r'(\d{4})\s*年\s*(?:第?一季度|Q1|1季度)\s*(?:营收|净利|利润|业绩|收入|财报|报告)',
         lambda y: (y, 3)),
        # Q2 / 二季度 / 半年报 / 中报 / 上半年
        (r'(\d{4})\s*年?\s*(?:Q2|二季[度报]|第二季[度报]|2季[度报]|第2季[度报]|半年[报度]|中报|上半年)',
         lambda y: (y, 6)),
        (r'(\d{4})\s*年\s*(?:第?二季度|Q2|2季度|上半年|半年报|中报)\s*(?:营收|净利|利润|业绩|收入|财报|报告)',
         lambda y: (y, 6)),
        # Q3 / 三季度 / 三季报 / 前三季度
        (r'(\d{4})\s*年?\s*(?:Q3|三季[度报]|第三季[度报]|3季[度报]|第3季[度报]|前三季[度报]|前3季[度报])',
         lambda y: (y, 9)),
        (r'(\d{4})\s*年\s*(?:第?三季度|Q3|3季度|前三季度)\s*(?:营收|净利|利润|业绩|收入|财报|报告)',
         lambda y: (y, 9)),
        # Q4 / 四季度 / 年报 / 财报 / 年度 / 全年 / 第四季度 / 全年业绩 / 下半年
        # 新增"财报"匹配——"YYYY年财报"视为年报(Q4)，因为"XX年财报"通常指全年财报
        (r'(\d{4})\s*年?\s*(?:Q4|四季[度报]|第四季[度报]|4季[度报]|第4季[度报]|年报|财报|年度报告|全年业绩|全年营收|全年净利|下半年)',
         lambda y: (y, 12)),
    ]

    matched_fiscal_period = False
    for pattern, period_fn in report_period_patterns:
        match = re.search(pattern, title)
        if match:
            try:
                year = int(match.group(1))
                report_year, report_quarter_end = period_fn(year)

                # 如果标题含预测关键词，且财报时期在未来，则这是预测不是已发布数据
                if forecast_keywords.search(title) and (report_year, report_quarter_end) > relevant_periods[-1]:
                    # 未来财报的预测，不过滤文章，但不应作为已发布数据引用
                    # 由 AI 分析时区分处理，此处放行
                    continue

                matched_fiscal_period = True

                # 核心判断：该财报时期是否比当前最老的相关时期还早？
                oldest_relevant = min(relevant_periods, key=lambda p: (p[0], p[1]))
                # 如果财报时期 < 最老相关时期，则过时
                if (report_year, report_quarter_end) < oldest_relevant:
                    return False
            except (ValueError, OverflowError):
                continue

    # ---- 第三层：纯年份 + 数据关键词匹配（严格版）----
    # "2024年GDP"、"2023年营收" 等 — 只有 min_relevant_year 及之后的年度数据有效
    # 关键修复：对于 min_relevant_year 年份的数据，如果第二层未匹配到具体季度，
    # 需要进一步检查是否隐含了过时的季度数据（如"2025年一季度营收"写成"2025年营收"
    # 但上下文包含季度关键词时）
    yearly_data_keywords = (
        r'(?:GDP|营收|净利|利润|业绩|收入|增长|数据|统计|报告|回顾|总结|盘点|'
        r'财报|年报|营业|毛利|净资产|分红|派息|股息|ROE|ROA|经济|产值|'
        r'出口|进口|贸易|销售|销量|产量|市场规模|行业规模)'
    )
    yearly_data_pattern = rf'(\d{{4}})\s*年\s*{yearly_data_keywords}'
    yearly_match = re.search(yearly_data_pattern, title)
    if yearly_match:
        try:
            data_year = int(yearly_match.group(1))
            # 排除未来年份 + 预测关键词的情况（那是预测，不应作为真实数据过滤依据）
            if data_year > now.year and forecast_keywords.search(title):
                pass  # 预测类内容，不过滤
            elif data_year < min_relevant_year:
                return False
            elif data_year == min_relevant_year and not matched_fiscal_period:
                # 增强：对于 min_relevant_year（如2025年），如果第二层未精确
                # 匹配到具体季度，检查标题中是否隐含了季度信息
                # 例如"2025年营收增长"如果不含季度关键词，则视为年度汇总数据，放行
                # 但如果含季度关键词（如"Q1""一季""上半年"等），说明是过时季度数据
                quarter_hint = re.search(
                    r'Q[123]|一季|二季|三季|第[一二三]季|[123]季|上半年|半年报|中报|前三季',
                    title
                )
                if quarter_hint:
                    # 隐含季度信息但第二层未匹配（可能是变体表述）
                    # 需要判断该季度是否在有效期内
                    q_map = {
                        'Q1': 3, '一季': 3, '第一季': 3, '1季': 3,
                        'Q2': 6, '二季': 6, '第二季': 6, '2季': 6, '上半年': 6, '半年报': 6, '中报': 6,
                        'Q3': 9, '三季': 9, '第三季': 9, '3季': 9, '前三季': 9,
                    }
                    hint_text = quarter_hint.group(0)
                    implied_q = None
                    for key, q_end in q_map.items():
                        if key in hint_text:
                            implied_q = q_end
                            break
                    if implied_q:
                        oldest_relevant = min(relevant_periods, key=lambda p: (p[0], p[1]))
                        if (data_year, implied_q) < oldest_relevant:
                            return False
        except (ValueError, OverflowError):
            pass

    # ---- 第四层：独立年份引用过滤（严格化）----
    # 年份距今超过1个自然年（而非原来的2年）就过滤含数据关键词的旧新闻
    # 匹配 "YYYY年" 但排除未来年份和当前/去年
    standalone_year_pattern = r'(\d{4})\s*年'
    for match in re.finditer(standalone_year_pattern, title):
        try:
            mentioned_year = int(match.group(1))
            # 过滤距今超过1个自然年的年份（原为2年）
            if mentioned_year < now.year - 1 and mentioned_year > 2000:
                # 检查该年份是否与财报相关关键词搭配
                context_start = max(0, match.start() - 5)
                context_end = min(len(title), match.end() + 30)
                context = title[context_start:context_end]
                # 如果上下文含财报/数据关键词，过滤掉
                if re.search(r'财报|年报|季报|业绩|营收|利润|净利|GDP|数据|统计|分析|增长|下滑|回顾', context):
                    return False
        except (ValueError, OverflowError):
            continue

    return True


def _title_tokens(title):
    """将标题分词为 token 集合（用于 Jaccard 相似度）。
    使用字符级 2-gram 作为简单分词，适合中文标题。"""
    import re as _re
    # 去除标点、空白、特殊符号
    clean = _re.sub(r'[^\u4e00-\u9fff\w]', '', title)
    if len(clean) < 2:
        return set(clean)
    return {clean[i:i + 2] for i in range(len(clean) - 1)}


# 核心实体关键词列表（用于去重时的实体匹配）
_CORE_ENTITIES = [
    # 地缘
    '伊朗', '以色列', '俄罗斯', '乌克兰', '台海', '台湾', '朝鲜', '红海', '胡塞',
    '中东', '巴以', '南海', '叙利亚', '也门', '缅甸', '阿富汗',
    # 国际组织/国家
    '美国', '中国', '日本', '韩国', '印度', '欧盟', '北约', '金砖', '东盟',
    # 公司/品牌
    '华为', '苹果', '特斯拉', '英伟达', '台积电', '三星', '比亚迪', '宁德时代',
    # 政策/机构
    '央行', '美联储', '国务院', '证监会', '发改委', '工信部',
    # 大宗
    '原油', '黄金', '锂', '芯片', '半导体',
]

# 去重时需要排除的常见停用词
_STOP_WORDS = {
    '最新', '突发', '重磅', '今天', '今日', '昨日', '刚刚', '速看', '关注',
    '消息', '新闻', '快讯', '热点', '话题', '讨论', '分析', '解读', '评论',
    '什么', '为什么', '如何', '怎么', '哪些', '多少', '是否',
}


def _extract_core_entities(title):
    """从标题中提取核心实体关键词集合（用于去重时的实体匹配）。"""
    import re as _re
    entities = set()
    for entity in _CORE_ENTITIES:
        if entity in title:
            entities.add(entity)
    # 提取数字+单位组合（如"3000亿"、"50%"）作为特征
    for m in _re.finditer(r'\d+[\.\d]*[%％亿万元美元]', title):
        entities.add(m.group())
    return entities


def _is_duplicate(title, existing_titles, threshold=0.55):
    """检测标题是否与已有标题高度相似（增强版去重）。

    三层去重策略：
    1. Jaccard 2-gram 相似度（threshold=0.55）
    2. 核心实体匹配：两条标题的核心实体集合高度重叠（≥80%）视为重复
    3. 短标题包含：一条标题完全包含另一条的核心内容

    避免多条新闻说的是同一事件（如"伊朗遭袭"和"伊朗被攻击最新消息"）被重复分析。
    """
    import re as _re
    tokens_new = _title_tokens(title)
    if not tokens_new:
        return False

    entities_new = _extract_core_entities(title)
    # 去除停用词后的标题核心（用于短标题包含检测）
    clean_new = _re.sub(r'[^\u4e00-\u9fff\w]', '', title)
    for sw in _STOP_WORDS:
        clean_new = clean_new.replace(sw, '')

    for existing in existing_titles:
        tokens_existing = _title_tokens(existing)
        if not tokens_existing:
            continue

        # 策略1: Jaccard 相似度
        intersection = tokens_new & tokens_existing
        union = tokens_new | tokens_existing
        similarity = len(intersection) / len(union) if union else 0
        if similarity >= threshold:
            return True

        # 策略2: 核心实体匹配（至少有2个实体且重叠度≥80%）
        if len(entities_new) >= 2:
            entities_existing = _extract_core_entities(existing)
            if len(entities_existing) >= 2:
                entity_overlap = entities_new & entities_existing
                entity_union = entities_new | entities_existing
                if len(entity_overlap) / len(entity_union) >= 0.8:
                    return True

        # 策略3: 短标题包含（去除停用词后，一条完全包含另一条）
        clean_existing = _re.sub(r'[^\u4e00-\u9fff\w]', '', existing)
        for sw in _STOP_WORDS:
            clean_existing = clean_existing.replace(sw, '')
        if len(clean_new) >= 4 and len(clean_existing) >= 4:
            if clean_new in clean_existing or clean_existing in clean_new:
                return True

    return False


def classify_trending(trending_data, stock_name='', industry='',
                      max_age_hours=48, news_max_age_days=30, reference_date=None):
    """
    对全网热点进行广覆盖分类（严格时效版 + 预测排除 + 去重）。

    增强功能：
    - 新增标题相似度去重（Jaccard 2-gram），避免多条新闻说的是同一件事被重复分析
    - 同一事件在多个平台出现时，只保留热度最高的那条

    时效过滤增强：
    - 预测/展望类内容识别：含预测关键词且引用未来年份的内容，
      其时间点不作为有效数据引用（如"预计2027年营收"属于预测而非已发布数据）
    - 严格时效性过滤：基于"当前应关注的财务时期"精确判断财报数据是否过时
    - 财报匹配精细化：半年报/中报/全年业绩等更多表述
    - 扩大数据关键词匹配范围（覆盖财报、分红、ROE、产值、销量等）
    - 独立年份引用检测：标题中含旧年份+数据关键词的自动过滤
    - 杜绝"2024年财报出现在2026年3月分析"等问题

    Args:
        trending_data: fetch_trending.py 采集的热点数据
        stock_name: 目标股票名称（可选）
        industry: 目标行业（可选）
        max_age_hours: 数据采集时效（小时），超过此时间的数据会标记为过期
        news_max_age_days: 新闻有效期（天），标题中日期超过此天数的新闻被过滤
        reference_date: 参考日期（datetime），用于时效性计算。默认为当前时间。

    Returns:
        dict: 分类后的热点数据，含时效性信息
    """
    if not trending_data:
        return None

    now = reference_date if reference_date else datetime.now()

    # 时效性检查
    is_fresh, age_hours, fetch_time_str = _check_freshness(
        trending_data, max_age_hours, reference_date=now
    )

    # 分类关键词映射（宽泛匹配，不做严格筛选）
    category_keywords = {
        'geopolitical': [
            '地缘', '冲突', '战争', '军事', '台海', '台湾', '南海',
            '俄乌', '俄罗斯', '乌克兰', '中东', '巴以', '以色列', '伊朗',
            '朝鲜', '北约', '制裁', '封锁', '武装', '导弹', '核',
            '国际关系', '外交', '领土', '主权',
        ],
        'us_china': [
            '中美', '美中', '中国美国', '贸易战', '贸易摩擦', '关税',
            '芯片禁令', '出口管制', '实体清单', '科技战', '脱钩',
            '中美关系', '美国制裁', '华为', 'TikTok',
        ],
        'national_policy': [
            '国务院', '中央', '政治局', '两会', '人大', '政协',
            '总书记', '总理', '国家主席', '政府工作报告',
            '改革', '规划', '战略', '新质生产力',
            '产业政策', '补贴', '税收', '减税', '社保',
            '环保', '碳中和', '碳达峰', '双碳',
            '医保', '教育', '住房', '民生', '就业',
            '反腐', '纪委', '监察',
        ],
        'central_bank': [
            '央行', '人民银行', 'PBOC', '降息', '降准', '加息',
            'LPR', 'MLF', '逆回购', '公开市场', '货币政策',
            '美联储', 'Fed', '欧央行', 'ECB', '日央行', 'BOJ',
            '英央行', 'BOE', '利率决议',
            '量化宽松', 'QE', '缩表',
        ],
        'banking_finance': [
            '银行', '工商银行', '建设银行', '农业银行', '中国银行', '交通银行',
            '招商银行', '兴业银行', '中信银行', '浦发银行', '民生银行',
            '商业银行', '信贷', '贷款', '存款', '理财', '信托',
            '券商', '证券', '基金', '公募', '私募', '保险',
            '社保基金', '养老金', '险资', '外资', '北向资金', '南向资金',
            'QFII', 'RQFII', '期货', '债券',
            '上交所', '深交所', '港交所', '纳斯达克', 'NYSE',
            '证监会', '银保监', '金融监管', 'IPO', '退市',
        ],
        'macro_economy': [
            'GDP', 'CPI', 'PPI', 'PMI', '通胀', '通缩', '滞胀',
            '社融', 'M2', '货币供应', '财政赤字', '国债',
            '失业率', '就业', '消费', '零售', '投资',
            '进出口', '贸易顺差', '贸易逆差', '外汇储备',
            '经济增长', '经济下行', '经济复苏', '衰退', '萧条',
            '房地产', '楼市', '房价', '土地市场',
        ],
        'stock_market': [
            'A股', '港股', '美股', '股市', '大盘', '指数',
            '上证', '深证', '创业板', '科创板', '北交所', '恒指', '纳指', '道指',
            '涨停', '跌停', '暴涨', '暴跌', '牛市', '熊市',
            '板块', '龙头', '概念股', '题材',
            '融资', '融券', '杠杆', '爆仓',
            '大宗交易', '股东', '减持', '增持', '回购',
        ],
        'commodities_forex': [
            '原油', '石油', 'OPEC', '黄金', '白银', '贵金属',
            '铜', '铝', '锂', '钴', '铁矿石', '钢材', '煤炭',
            '天然气', '粮食', '大豆', '玉米', '猪肉',
            '碳酸锂', '稀土',
            '汇率', '人民币', '美元', '欧元', '日元', '英镑',
            '外汇', '货币', '数字货币', '比特币', '加密',
        ],
        'industry_tech': [
            '半导体', '芯片', 'AI', '人工智能', '大模型', 'GPT', 'ChatGPT',
            '机器人', '自动驾驶', '新能源', '光伏', '风电', '储能',
            '电动车', '锂电池', '充电桩', '氢能',
            '5G', '6G', '量子', '卫星', '航天', '航空',
            '生物医药', '创新药', '医疗器械', '基因',
            '元宇宙', 'VR', 'AR', '区块链', 'Web3',
            '云计算', '数据中心', '算力', '芯片制造',
        ],
        'global_events': [
            '联合国', 'G7', 'G20', 'APEC', '金砖', '上合',
            '气候', '自然灾害', '地震', '台风', '洪水', '疫情',
            '恐怖', '难民', '移民', '选举', '大选',
            '能源危机', '粮食危机', '供应链',
            '英国', '法国', '德国', '日本', '韩国', '印度', '巴西',
            '欧盟', '东盟', '非洲', '拉美',
        ],
    }

    result = {
        'classified_time': now.isoformat(),
        'reference_date': now.strftime('%Y-%m-%d'),
        'fetch_time': fetch_time_str,
        'data_age_hours': round(age_hours, 1),
        'is_fresh': is_fresh,
        'freshness_warning': '' if is_fresh else f'⚠️ 热点数据已过期（{age_hours:.0f}小时前获取），建议重新采集',
        'news_max_age_days': news_max_age_days,
        'news_cutoff_date': (now - timedelta(days=news_max_age_days)).strftime('%Y-%m-%d'),
        'stock_name': stock_name,
        'industry': industry,
        'categories': {
            'company_related': [],
            'industry_related': [],
            'geopolitical': [],
            'us_china': [],
            'national_policy': [],
            'central_bank': [],
            'banking_finance': [],
            'macro_economy': [],
            'stock_market': [],
            'commodities_forex': [],
            'industry_tech': [],
            'global_events': [],
            'general': [],
        },
        'all_items': [],
        'filtered_out_count': 0,
    }

    sources = trending_data.get('sources', [])
    filtered_out = 0
    dedup_count = 0
    seen_titles = []  # 保存已接受的标题，用于去重

    # 先按热度排序所有 items，确保同一事件保留热度最高的那条
    all_source_items = []
    for source_data in sources:
        source_name = source_data.get('source_name', source_data.get('source', 'unknown'))
        for item in source_data.get('items', []):
            all_source_items.append({**item, '_source_name': source_name})
    all_source_items.sort(key=lambda x: x.get('hot', 0), reverse=True)

    for item in all_source_items:
        source_name = item.get('_source_name', 'unknown')
        title = item.get('title', '')
        if not title:
            continue

        # 过滤标题中明确标注旧日期的新闻
        if not _is_news_within_period(title, news_max_age_days, reference_date=now):
            filtered_out += 1
            continue

        # 标题去重 — 与已接受的标题做相似度检测
        if _is_duplicate(title, seen_titles):
            dedup_count += 1
            continue

        seen_titles.append(title)

        entry = {
            'title': title,
            'source': source_name,
            'url': item.get('url', ''),
            'hot': item.get('hot', 0),
            'categories': [],
        }

        # 公司直接相关（最高优先级）
        if stock_name and stock_name in title:
            entry['categories'].append('company_related')

        # 行业直接相关
        if industry and industry in title:
            entry['categories'].append('industry_related')

        # 按关键词匹配分类
        for cat, keywords in category_keywords.items():
            for kw in keywords:
                if kw in title:
                    if cat not in entry['categories']:
                        entry['categories'].append(cat)
                    break  # 该分类已匹配，不再检查该分类的其他关键词

        # 未匹配任何分类的归入 general
        if not entry['categories']:
            entry['categories'].append('general')

        result['all_items'].append(entry)
        for cat in entry['categories']:
            if cat in result['categories']:
                result['categories'][cat].append(entry)

    # 按热度排序
    result['all_items'].sort(key=lambda x: x.get('hot', 0), reverse=True)
    for cat in result['categories']:
        result['categories'][cat].sort(key=lambda x: x.get('hot', 0), reverse=True)

    # 统计
    result['total_items'] = len(result['all_items'])
    result['filtered_out_count'] = filtered_out
    result['dedup_count'] = dedup_count
    result['category_counts'] = {cat: len(items) for cat, items in result['categories'].items() if items}

    logger.info(
        f'热点分类完成: 共 {result["total_items"]} 条（过滤掉 {filtered_out} 条过时新闻，去重 {dedup_count} 条），'
        f'分布: {result["category_counts"]}'
    )
    if not is_fresh:
        logger.warning(result['freshness_warning'])
    return result


def export_news_json(classified_data, output_path):
    """将分类后的新闻结构化保存为独立 JSON 文件。

    每条新闻包含：标题、时间、链接、来源平台、所属分类、热度。
    - time 字段优先使用 item 自身的时间（如有），否则使用采集时间
    - url 字段保证存在（即使为空字符串）
    文件保存到 financial_data 同目录，方便追溯和二次利用。

    Args:
        classified_data: classify_trending() 返回的分类数据
        output_path: 输出 JSON 文件路径
    """
    if not classified_data:
        return

    category_label_map = {
        'company_related': '公司相关',
        'industry_related': '行业相关',
        'geopolitical': '地缘政治',
        'us_china': '中美关系',
        'national_policy': '国家政策',
        'central_bank': '央行与货币',
        'banking_finance': '银行与金融',
        'macro_economy': '宏观经济',
        'stock_market': '股市行情',
        'commodities_forex': '大宗商品与汇率',
        'industry_tech': '行业科技',
        'global_events': '全球时事',
        'general': '其他',
    }

    news_items = []
    fetch_time = classified_data.get('fetch_time', '')
    reference_date = classified_data.get('reference_date', '')

    for item in classified_data.get('all_items', []):
        # 优先使用 item 自身的时间字段，否则使用统一的采集时间
        item_time = item.get('time', '') or item.get('publish_time', '') or fetch_time
        news_items.append({
            'title': item.get('title', ''),
            'time': item_time,
            'url': item.get('url', ''),
            'source': item.get('source', ''),
            'hot': item.get('hot', 0),
            'categories': [category_label_map.get(c, c) for c in item.get('categories', [])],
        })

    output = {
        'generated_at': datetime.now().isoformat(),
        'reference_date': reference_date,
        'fetch_time': fetch_time,
        'total_count': len(news_items),
        'filtered_out_count': classified_data.get('filtered_out_count', 0),
        'dedup_count': classified_data.get('dedup_count', 0),
        'stock_name': classified_data.get('stock_name', ''),
        'industry': classified_data.get('industry', ''),
        'items': news_items,
    }

    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    logger.info(f'✅ 结构化新闻已保存: {output_path}（共 {len(news_items)} 条）')


# ---------------------------------------------------------------------------
# 热点关键词提取与动态搜索建议
# ---------------------------------------------------------------------------

# 事件→行业影响传导映射（用于将地缘/宏观事件关联到具体行业和个股）
EVENT_IMPACT_CHAINS = {
    # 地缘冲突 → 影响行业/资产
    '伊朗': ['原油', '能源', '航运', '黄金', '军工', '避险资产'],
    '中东': ['原油', '能源', '航运', '黄金', '军工', '避险资产'],
    '俄乌': ['天然气', '能源', '粮食', '化肥', '军工', '稀有金属'],
    '台海': ['半导体', '芯片', '电子', '科技', '军工', '航运'],
    '朝鲜': ['军工', '避险资产', '黄金'],
    '红海': ['航运', '物流', '贸易', '原油'],
    '胡塞': ['航运', '物流', '原油', '能源'],
    '南海': ['航运', '军工', '渔业'],
    # 中美博弈 → 影响行业
    '芯片禁令': ['半导体', '芯片', '科技', 'AI', '国产替代'],
    '出口管制': ['半导体', '科技', '军工', '高端制造'],
    '关税': ['贸易', '出口', '制造业', '消费品'],
    '制裁': ['金融', '科技', '能源', '芯片'],
    # 政策 → 影响行业
    '降息': ['地产', '银行', '消费', '成长股'],
    '降准': ['银行', '地产', '基建', '流动性'],
    '碳中和': ['新能源', '光伏', '风电', '储能'],
    '消费券': ['消费', '零售', '餐饮', '旅游'],
    # 大宗/汇率
    '原油': ['能源', '化工', '航空', '物流'],
    '黄金': ['贵金属', '避险', '珠宝'],
    '人民币': ['出口', '进口', '外贸', '航空'],
}


def extract_hot_keywords(classified_data, stock_name='', industry=''):
    """
    从分类后的热点数据中提取高频实体关键词和动态搜索建议。

    解决的核心问题：
    - 静态搜索词（如"台海 中东 俄乌"）无法覆盖当前实际热点（如"伊朗局势"）
    - 热点采集和搜索是两条平行管线，互不通信
    - 地缘事件到个股影响缺乏自动化传导分析

    工作原理：
    1. 从 classified 热点的 geopolitical/us_china/global_events 等分类中提取标题
    2. 识别高频出现的实体（地名/国名/组织/事件名）
    3. 基于 EVENT_IMPACT_CHAINS 推导该事件对行业/资产类别的影响
    4. 生成"动态搜索建议"供 AI Agent 在 web_search 阶段使用

    Args:
        classified_data: classify_trending() 的输出
        stock_name: 分析标的公司名称
        industry: 分析标的所在行业

    Returns:
        dict: {
            'hot_entities': [...],           # 高频实体关键词列表
            'dynamic_search_queries': [...], # 动态搜索建议（补充 search_service 的固定查询）
            'impact_chains': [...],          # 事件→行业→个股 传导链
            'coverage_gaps': [...],          # 识别到的搜索覆盖盲区
        }
    """
    import re
    from collections import Counter

    if not classified_data:
        return {
            'hot_entities': [],
            'dynamic_search_queries': [],
            'impact_chains': [],
            'coverage_gaps': [],
        }

    categories = classified_data.get('categories', {})

    # 第一步：从高优先级分类中收集所有标题
    high_priority_cats = [
        'geopolitical', 'us_china', 'global_events',
        'national_policy', 'central_bank', 'macro_economy',
        'commodities_forex', 'industry_tech',
    ]
    all_titles = []
    for cat in high_priority_cats:
        for item in categories.get(cat, []):
            all_titles.append(item.get('title', ''))

    if not all_titles:
        return {
            'hot_entities': [],
            'dynamic_search_queries': [],
            'impact_chains': [],
            'coverage_gaps': [],
        }

    # 第二步：提取实体关键词（地名/国名/组织/事件名等）
    # 使用一个较全面的实体词典做匹配
    entity_patterns = {
        # 国家/地区
        '国家地区': [
            '伊朗', '以色列', '巴勒斯坦', '加沙', '黎巴嫩', '叙利亚', '也门',
            '沙特', '伊拉克', '阿富汗', '土耳其', '埃及',
            '俄罗斯', '乌克兰', '白俄罗斯', '格鲁吉亚',
            '台湾', '朝鲜', '韩国', '日本', '印度', '巴基斯坦',
            '缅甸', '菲律宾', '越南',
            '美国', '英国', '法国', '德国', '意大利', '加拿大', '澳大利亚',
            '巴西', '阿根廷', '墨西哥', '南非', '尼日利亚',
        ],
        # 国际组织/军事
        '组织军事': [
            'NATO', '北约', '联合国', '欧盟', 'G7', 'G20', '金砖',
            '东盟', 'OPEC', '上合', 'AUKUS',
            '胡塞', '哈马斯', '真主党', '塔利班',
            '五角大楼', '国防部', '中央军委',
        ],
        # 地理热点
        '地理热点': [
            '台海', '南海', '红海', '霍尔木兹', '苏伊士', '马六甲',
            '克里米亚', '顿巴斯', '戈兰高地',
            '钓鱼岛', '仁爱礁',
        ],
        # 关键事件/话题
        '关键事件': [
            '核武', '核试验', '导弹', '无人机', '空袭', '轰炸',
            '停火', '谈判', '斡旋', '和谈',
            '选举', '大选', '弹劾', '政变',
            '关税', '制裁', '禁令', '封锁', '脱钩',
            '降息', '加息', '降准', '缩表', '量化宽松',
        ],
    }

    entity_counter = Counter()
    entity_category_map = {}

    for title in all_titles:
        for etype, entities in entity_patterns.items():
            for entity in entities:
                if entity in title:
                    entity_counter[entity] += 1
                    if entity not in entity_category_map:
                        entity_category_map[entity] = etype

    # 按出现频次排序，取 top 20
    hot_entities = [
        {
            'keyword': kw,
            'count': cnt,
            'type': entity_category_map.get(kw, 'unknown'),
        }
        for kw, cnt in entity_counter.most_common(20)
    ]

    # 第三步：基于 EVENT_IMPACT_CHAINS 推导影响传导链
    impact_chains = []
    for entity_info in hot_entities:
        kw = entity_info['keyword']
        if kw in EVENT_IMPACT_CHAINS:
            affected = EVENT_IMPACT_CHAINS[kw]
            chain = {
                'trigger_event': kw,
                'trigger_count': entity_info['count'],
                'affected_sectors': affected,
                'relevance_to_target': 'unknown',
            }
            # 判断与分析标的的关联度
            if stock_name or industry:
                target = f'{stock_name} {industry}'.lower()
                matches = [s for s in affected if s.lower() in target or target in s.lower()]
                if matches:
                    chain['relevance_to_target'] = 'high'
                    chain['matched_sectors'] = matches
                else:
                    chain['relevance_to_target'] = 'indirect'
            impact_chains.append(chain)

    # 第四步：生成动态搜索建议
    current_year = classified_data.get('reference_date', str(datetime.now().year))[:4]
    dynamic_queries = []

    for entity_info in hot_entities[:10]:
        kw = entity_info['keyword']
        cnt = entity_info['count']
        etype = entity_info['type']

        if cnt < 2 and etype not in ('国家地区', '地理热点'):
            continue

        # 基础查询：该热点的最新动态
        dynamic_queries.append({
            'keyword': kw,
            'query': f'{kw} 最新 局势 影响 {current_year}',
            'explanation': f'热点关键词"{kw}"在 {cnt} 条热搜中出现，需深入了解最新动态',
            'priority': 'high' if cnt >= 3 else 'medium',
            'type': 'hotspot_tracking',
        })

        # 如果有分析标的，生成关联查询
        if stock_name or industry:
            target = stock_name or industry
            # 如果在影响传导链中有匹配
            chain_match = [c for c in impact_chains if c['trigger_event'] == kw]
            if chain_match and chain_match[0].get('relevance_to_target') in ('high', 'indirect'):
                sectors = chain_match[0]['affected_sectors']
                dynamic_queries.append({
                    'keyword': kw,
                    'query': f'{kw} {target} 影响 {" ".join(sectors[:2])} {current_year}',
                    'explanation': f'评估"{kw}"事件通过{"/".join(sectors[:3])}链条对{target}的具体影响',
                    'priority': 'high',
                    'type': 'impact_analysis',
                })
            else:
                dynamic_queries.append({
                    'keyword': kw,
                    'query': f'{kw} 对 {target} 股价 影响 {current_year}',
                    'explanation': f'评估热点事件"{kw}"对{target}的潜在影响',
                    'priority': 'medium',
                    'type': 'impact_analysis',
                })

    # 第五步：识别搜索覆盖盲区
    # 对比热点实体与 search_service.py 的固定搜索词，找出未被覆盖的
    static_search_keywords = {
        '台海', '中东', '俄乌', '中美', '关税', '科技制裁',
        '降息', '降准', '美联储', '原油', '黄金',
    }
    coverage_gaps = []
    for entity_info in hot_entities[:15]:
        kw = entity_info['keyword']
        if kw not in static_search_keywords and entity_info['count'] >= 2:
            coverage_gaps.append({
                'keyword': kw,
                'count': entity_info['count'],
                'note': f'热点关键词"{kw}"未被 search_service 静态搜索词覆盖，需通过动态搜索补充',
            })

    result = {
        'hot_entities': hot_entities,
        'dynamic_search_queries': dynamic_queries,
        'impact_chains': impact_chains,
        'coverage_gaps': coverage_gaps,
        'total_titles_analyzed': len(all_titles),
    }

    logger.info(
        f'热点关键词提取完成: {len(hot_entities)} 个实体, '
        f'{len(dynamic_queries)} 条动态搜索建议, '
        f'{len(impact_chains)} 条影响传导链, '
        f'{len(coverage_gaps)} 个覆盖盲区'
    )

    return result


# ---------------------------------------------------------------------------
# 宏观仪表盘
# ---------------------------------------------------------------------------

def macro_dashboard(trending_json_path='', stock_name='', industry='',
                    reference_date=None, news_max_age_days=30,
                    news_json_output=''):
    """一键获取全部关键宏观指标，可选合并时政热点。

    Args:
        news_json_output: 结构化新闻 JSON 输出路径（可选，保存到 financial_data 同目录）
    """
    logger.info('正在构建宏观经济仪表盘...')

    now = reference_date if reference_date else datetime.now()

    result = {
        'timestamp': now.isoformat(),
        'reference_date': now.strftime('%Y-%m-%d'),
        'news_max_age_days': news_max_age_days,
        'rates': {},
        'inflation': {},
        'pmi': {},
        'social_financing': {},
        'business_cycle': {},
        'global_search_queries': generate_global_search_queries(),
    }

    try:
        result['rates'] = fetch_rates()
    except Exception as e:
        result['rates'] = {'error': str(e)}
        logger.warning(f'利率数据获取失败: {e}')

    try:
        result['inflation'] = fetch_inflation()
    except Exception as e:
        result['inflation'] = {'error': str(e)}
        logger.warning(f'通胀数据获取失败: {e}')

    try:
        result['pmi'] = fetch_pmi()
    except Exception as e:
        result['pmi'] = {'error': str(e)}
        logger.warning(f'PMI数据获取失败: {e}')

    try:
        result['social_financing'] = fetch_social_financing()
    except Exception as e:
        result['social_financing'] = {'error': str(e)}
        logger.warning(f'社融数据获取失败: {e}')

    try:
        result['business_cycle'] = assess_business_cycle()
    except Exception as e:
        result['business_cycle'] = {'error': str(e)}
        logger.warning(f'经济周期评估失败: {e}')

    # 时政热点（日期感知 + 旧新闻过滤）
    if trending_json_path:
        trending_data = load_trending_data(trending_json_path)
        if trending_data:
            result['trending_raw'] = trending_data
            result['trending_classified'] = classify_trending(
                trending_data, stock_name=stock_name, industry=industry,
                news_max_age_days=news_max_age_days, reference_date=now,
            )
            # 保留旧字段名兼容（指向同一数据）
            result['trending_filtered'] = result['trending_classified']
            logger.info('时政热点数据已分类并合并到仪表盘')

            # 结构化新闻保存为独立 JSON
            if news_json_output:
                export_news_json(result['trending_classified'], news_json_output)
            else:
                # 若未指定输出路径，自动保存到 trending_json 同目录
                auto_path = str(Path(trending_json_path).parent / 'news_structured.json')
                export_news_json(result['trending_classified'], auto_path)

            # 从热点中提取关键词，生成动态搜索建议
            result['hot_keywords'] = extract_hot_keywords(
                result['trending_classified'],
                stock_name=stock_name,
                industry=industry,
            )
            if result['hot_keywords']['dynamic_search_queries']:
                logger.info(
                    f'已生成 {len(result["hot_keywords"]["dynamic_search_queries"])} 条'
                    f'动态搜索建议（基于热点关键词）'
                )
            if result['hot_keywords']['coverage_gaps']:
                logger.warning(
                    f'发现 {len(result["hot_keywords"]["coverage_gaps"])} 个搜索覆盖盲区: '
                    f'{", ".join(g["keyword"] for g in result["hot_keywords"]["coverage_gaps"][:5])}'
                )

    logger.info('宏观经济仪表盘构建完成')
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='中国宏观经济数据分析工具（基于 AkShare，无需 API Key）',
        epilog='示例: python macro_analysis.py --dashboard --output macro_dashboard.json'
    )
    parser.add_argument('--dashboard', action='store_true', help='完整宏观仪表盘')
    parser.add_argument('--rates', action='store_true', help='利率数据（LPR、Shibor）')
    parser.add_argument('--inflation', action='store_true', help='通胀数据（CPI、PPI）')
    parser.add_argument('--pmi', action='store_true', help='PMI数据')
    parser.add_argument('--social-financing', action='store_true', help='社融与M2')
    parser.add_argument('--cycle', action='store_true', help='经济周期评估')
    parser.add_argument('--global-queries', action='store_true', help='生成国际事件搜索指令')
    parser.add_argument('--trending-json', default='', help='fetch_trending.py 采集的时政热点 JSON 路径（可选，合并到仪表盘）')
    parser.add_argument('--stock-name', default='', help='关联的股票名称（用于定制搜索和热点筛选）')
    parser.add_argument('--industry', default='', help='关联的行业（用于定制搜索）')
    parser.add_argument('--output', default='', help='输出 JSON 文件路径')
    parser.add_argument('--reference-date', default='',
                        help='参考日期（YYYY-MM-DD），用于时效性过滤，默认为当前日期。'
                             '应传入对话的实时日期以确保时效性准确。')
    parser.add_argument('--news-max-age-days', type=int, default=30,
                        help='新闻有效期（天），超过此天数的新闻将被过滤（默认30天）')
    parser.add_argument('--news-json-output', default='',
                        help='结构化新闻 JSON 输出路径（含标题/时间/链接/来源/分类），'
                             '默认自动保存到 trending-json 同目录下的 news_structured.json')
    args = parser.parse_args()

    # 解析参考日期
    ref_date = None
    if args.reference_date:
        try:
            ref_date = datetime.strptime(args.reference_date, '%Y-%m-%d')
        except ValueError:
            logger.warning(f'无法解析参考日期: {args.reference_date}，使用当前日期')

    try:
        if args.rates:
            data = fetch_rates()
        elif args.inflation:
            data = fetch_inflation()
        elif args.pmi:
            data = fetch_pmi()
        elif args.social_financing:
            data = fetch_social_financing()
        elif args.cycle:
            data = assess_business_cycle()
        elif args.global_queries:
            data = generate_global_search_queries(
                stock_name=args.stock_name,
                industry=args.industry
            )
        else:
            data = macro_dashboard(
                trending_json_path=args.trending_json,
                stock_name=args.stock_name,
                industry=args.industry,
                reference_date=ref_date,
                news_max_age_days=args.news_max_age_days,
                news_json_output=args.news_json_output,
            )

        _output_json(data, args.output if args.output else None)

    except ImportError:
        print('错误：需要安装 akshare。请运行: pip install akshare', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
