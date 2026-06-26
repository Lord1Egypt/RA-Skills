#!/usr/bin/env python3
"""
条件单投资助手 - 核心分析引擎
根据代码识别品种类型，推荐条件单策略，生成具体参数
"""

import json
import sys
import os
import urllib.request
import urllib.parse

# 导入价格获取
sys.path.insert(0, os.path.dirname(__file__))
from fetch_price import fetch_east_money_price, fetch_qdii_premium


# ============ 品种数据库 ============

# ETF 代码 → 类型映射
ETF_DATABASE = {
    # ===== 国债/政金债 ETF =====
    '511260': {'name': '国债 ETF', 'type': 'bond_long', 'category': '债券', 'fee': 0.15},
    '511520': {'name': '政金债 10Y', 'type': 'bond_long', 'category': '债券', 'fee': 0.15},
    '511010': {'name': '国债 ETF 短', 'type': 'bond_short', 'category': '债券', 'fee': 0.15},
    '511180': {'name': '十年国债', 'type': 'bond_long', 'category': '债券', 'fee': 0.15},

    # ===== 宽基 ETF =====
    '510300': {'name': '沪深 300ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '510050': {'name': '上证 50ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '510500': {'name': '中证 500ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '159919': {'name': '沪深 300ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '159901': {'name': '深成 ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '159915': {'name': '创业板 ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '513100': {'name': '纳指 100ETF', 'type': 'cross_border', 'category': '跨境宽基', 'fee': 0.30},
    '513180': {'name': '纳指 100ETF', 'type': 'cross_border', 'category': '跨境宽基', 'fee': 0.30},
    '159941': {'name': '恒生 ETF', 'type': 'cross_border', 'category': '跨境宽基', 'fee': 0.50},
    '513330': {'name': '恒生 ETF', 'type': 'cross_border', 'category': '跨境宽基', 'fee': 0.50},
    '513010': {'name': '恒生科技 ETF', 'type': 'cross_border', 'category': '跨境科技', 'fee': 0.50},
    '513500': {'name': '标普 500ETF', 'type': 'cross_border', 'category': '跨境宽基', 'fee': 0.50},
    '513050': {'name': '中概互联 ETF', 'type': 'cross_border', 'category': '跨境科技', 'fee': 0.50},
    '159509': {'name': '纳指科技 ETF', 'type': 'cross_border', 'category': '跨境科技', 'fee': 0.50},

    # ===== 行业/主题 ETF =====
    '512000': {'name': '券商 ETF', 'type': 'industry', 'category': '金融', 'fee': 0.15},
    '512880': {'name': '券商 ETF', 'type': 'industry', 'category': '金融', 'fee': 0.15},
    '512660': {'name': '军工 ETF', 'type': 'industry', 'category': '军工', 'fee': 0.15},
    '512480': {'name': '军工 ETF', 'type': 'industry', 'category': '军工', 'fee': 0.15},
    '512500': {'name': '中证 500 医药', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '512010': {'name': '医药 ETF', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '159938': {'name': '医药 ETF', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '159992': {'name': '创新药 ETF', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '588250': {'name': '科创医药 ETF', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '159286': {'name': '港股创新药 ETF', 'type': 'cross_border', 'category': '跨境医药', 'fee': 0.50},
    '159928': {'name': '消费 ETF', 'type': 'industry', 'category': '消费', 'fee': 0.15},
    '512600': {'name': '主要消费 ETF', 'type': 'industry', 'category': '消费', 'fee': 0.15},
    '515030': {'name': '新能源车 ETF', 'type': 'industry', 'category': '新能源', 'fee': 0.15},
    '515700': {'name': '新能源 ETF', 'type': 'industry', 'category': '新能源', 'fee': 0.15},
    '515880': {'name': '5G ETF', 'type': 'industry', 'category': '科技', 'fee': 0.15},
    '515050': {'name': '中证 500 信息技术', 'type': 'industry', 'category': '科技', 'fee': 0.15},
    '159813': {'name': '半导体 ETF', 'type': 'industry', 'category': '科技', 'fee': 0.15},
    '512480': {'name': '芯片 ETF', 'type': 'industry', 'category': '科技', 'fee': 0.15},
    '515980': {'name': '人工智能 ETF', 'type': 'industry', 'category': '科技/AI', 'fee': 0.15},
    '515070': {'name': '红利 ETF', 'type': 'dividend', 'category': '高股息', 'fee': 0.15},
    '510880': {'name': '红利 ETF', 'type': 'dividend', 'category': '高股息', 'fee': 0.15},
    '515180': {'name': '中证红利 ETF', 'type': 'dividend', 'category': '高股息', 'fee': 0.15},
    '563020': {'name': '红利低波 ETF', 'type': 'dividend', 'category': '高股息', 'fee': 0.15},
    '159207': {'name': '高股息 ETF', 'type': 'dividend', 'category': '高股息', 'fee': 0.15},
    '562060': {'name': '标普红利 ETF', 'type': 'cross_border', 'category': '跨境高股息', 'fee': 0.50},

    # ===== 商品 ETF =====
    '518880': {'name': '黄金 ETF', 'type': 'gold', 'category': '黄金', 'fee': 0.20},
    '159934': {'name': '黄金 ETF', 'type': 'gold', 'category': '黄金', 'fee': 0.20},
    '159937': {'name': '博时黄金 ETF', 'type': 'gold', 'category': '黄金', 'fee': 0.20},
    '159830': {'name': '黄金 ETF 基金', 'type': 'gold', 'category': '黄金', 'fee': 0.20},
    '518800': {'name': '黄金股 ETF', 'type': 'gold_stock', 'category': '黄金股', 'fee': 0.15},
    '561360': {'name': '石油 ETF', 'type': 'commodity', 'category': '石油', 'fee': 0.15},
    '563150': {'name': '油气 ETF', 'type': 'commodity', 'category': '石油', 'fee': 0.15},
    '512400': {'name': '资源 ETF', 'type': 'commodity', 'category': '资源', 'fee': 0.15},
    '159980': {'name': '有色期货 ETF', 'type': 'commodity', 'category': '资源', 'fee': 0.15},
    '510410': {'name': '资源 ETF', 'type': 'commodity', 'category': '资源', 'fee': 0.15},

    # ===== 科创/创业板 =====
    '588000': {'name': '科创 50ETF', 'type': 'star', 'category': '科创', 'fee': 0.15},
    '588090': {'name': '科创 AI ETF', 'type': 'star', 'category': '科创/AI', 'fee': 0.15},
    '588080': {'name': '科创芯片 ETF', 'type': 'star', 'category': '科创/科技', 'fee': 0.15},
    '588200': {'name': '科创芯片 ETF', 'type': 'star', 'category': '科创/科技', 'fee': 0.15},
    '159363': {'name': '创业板 AI ETF', 'type': 'growth', 'category': '创业板/AI', 'fee': 0.15},
    '513780': {'name': '港股创新药 ETF', 'type': 'cross_border', 'category': '跨境医药', 'fee': 0.50},
    '159858': {'name': '创新药 ETF', 'type': 'industry', 'category': '医药', 'fee': 0.15},
    '510160': {'name': '创业板 ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
    '510030': {'name': '医药 50ETF', 'type': 'broad', 'category': '宽基', 'fee': 0.15},
}

# 股票类型判断规则
STOCK_RULES = {
    'high_dividend': {
        'codes': ['601088', '600900', '601225', '601328', '601398', '600036', '601166', '600887'],
        'names': ['中国神华', '长江电力', '陕西煤业', '交通银行', '工商银行', '招商银行', '兴业银行', '伊利股份'],
        'desc': '高股息蓝筹',
    },
    'tech_ai': {
        'patterns': ['科技', 'AI', '人工智能', '半导体', '芯片', '算力', '光模块'],
        'desc': '科技/AI',
    },
    'consumer': {
        'patterns': ['消费', '白酒', '食品', '家电', '乳业', '茅台', '五粮液', '海天'],
        'desc': '消费',
    },
    'medical': {
        'patterns': ['医药', '生物', '医疗', '创新药', '中药'],
        'desc': '医药',
    },
}


def identify_code(code: str) -> dict:
    """识别代码类型"""
    code = code.strip()

    # ETF 数据库查询
    if code in ETF_DATABASE:
        info = ETF_DATABASE[code].copy()
        info['code'] = code
        info['is_etf'] = True
        info['is_stock'] = False
        return info

    # 判断是否可能是 ETF（51/15/56/16 开头）
    if code.startswith(('51', '15', '56', '16')):
        return {
            'code': code,
            'type': 'unknown_etf',
            'category': '未知 ETF',
            'is_etf': True,
            'is_stock': False,
            'name': '未知 ETF',
        }

    # 判断是否可能是股票（60/00/30 开头）
    if code.startswith(('60', '00', '30')):
        return {
            'code': code,
            'type': 'stock',
            'category': '股票',
            'is_etf': False,
            'is_stock': True,
            'name': '未知股票',
        }

    return {
        'code': code,
        'type': 'unknown',
        'category': '未知',
        'is_etf': False,
        'is_stock': False,
        'name': '未知品种',
    }


def get_strategy_recommendation(info: dict, capital: float = 0, risk_preference: str = 'balanced') -> dict:
    """
    根据品种类型推荐策略
    risk_preference: conservative/balanced/aggressive
    """
    etf_type = info.get('type', '')
    is_stock = info.get('is_stock', False)

    strategies = []

    if etf_type == 'bond_long' or etf_type == 'bond_short':
        # 债券 ETF：网格交易最优
        strategies = [
            {'name': '网格交易', 'priority': '⭐⭐⭐⭐⭐', 'desc': '震荡市高抛低吸，债 ETF 最稳'},
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐', 'desc': '大跌时低吸加仓'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐', 'desc': '急涨后止盈'},
        ]
        grid_spacing = '0.003~0.005'
        grid_range_pct = '±1%'
        not_suitable = ['定价卖出止损', '定期定投']

    elif etf_type == 'broad':
        # 宽基 ETF：定投 + 波段
        strategies = [
            {'name': '定期定投', 'priority': '⭐⭐⭐⭐⭐', 'desc': '长期国运，宽基最优'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '涨多了自动止盈'},
            {'name': '定价买入', 'priority': '⭐⭐⭐', 'desc': '大跌时加仓'},
        ]
        grid_spacing = '1%~1.5%'
        grid_range_pct = '±5%'
        not_suitable = ['网格交易（波动不够）']

    elif etf_type == 'cross_border':
        # 跨境 ETF：波段 + 溢价监控
        strategies = [
            {'name': '反弹买入', 'priority': '⭐⭐⭐⭐', 'desc': '右侧企稳再进'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '涨多了自动止盈'},
            {'name': '定价买入', 'priority': '⭐⭐⭐', 'desc': '回调到支撑位'},
        ]
        grid_spacing = '1.5%~2%'
        grid_range_pct = '±5%'
        not_suitable = ['网格交易（溢价风险）', '定投（汇率风险）']

    elif etf_type == 'gold':
        # 黄金 ETF：网格 + 低吸
        strategies = [
            {'name': '网格交易', 'priority': '⭐⭐⭐⭐⭐', 'desc': '震荡收割，黄金波动适中'},
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐', 'desc': '回调时分档加仓'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐', 'desc': '急涨后锁利'},
        ]
        grid_spacing = '0.5%~0.8%'
        grid_range_pct = '±4%'
        not_suitable = ['定价卖出止损（黄金不止损）']

    elif etf_type == 'gold_stock':
        # 黄金股 ETF：高波动波段
        strategies = [
            {'name': '反弹买入', 'priority': '⭐⭐⭐⭐', 'desc': '右侧企稳'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '高位止盈'},
            {'name': '定价卖出止损', 'priority': '⭐⭐⭐⭐⭐', 'desc': '必设！-6% 止损'},
        ]
        grid_spacing = '1.5%~2%'
        grid_range_pct = '±6%'
        not_suitable = ['网格交易（波动太大）', '定投']

    elif etf_type == 'commodity':
        # 商品 ETF（石油/资源）：分批买卖
        strategies = [
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐⭐', 'desc': '大跌分批买'},
            {'name': '定价卖出', 'priority': '⭐⭐⭐⭐⭐', 'desc': '大涨分批卖 + 止损'},
            {'name': '反弹买入', 'priority': '⭐⭐⭐', 'desc': '企稳再进'},
        ]
        grid_spacing = '不适用'
        grid_range_pct = '不适用'
        not_suitable = ['网格交易（单边行情会打穿）', '定投']

    elif etf_type == 'industry':
        # 行业 ETF：波段交易
        strategies = [
            {'name': '反弹买入', 'priority': '⭐⭐⭐⭐', 'desc': '右侧企稳再进'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '涨多了自动止盈'},
            {'name': '定价卖出止损', 'priority': '⭐⭐⭐⭐⭐', 'desc': '-6%~-8% 止损'},
        ]
        grid_spacing = '1.5%~2%'
        grid_range_pct = '±6%'
        not_suitable = ['定期定投（行业有风险）', '网格（可能单边）']

    elif etf_type in ('star', 'growth'):
        # 科创/创业板：高波动波段
        strategies = [
            {'name': '反弹买入', 'priority': '⭐⭐⭐⭐', 'desc': '从低点反弹 2%~3% 再进'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '涨 15%+ 后回落 2% 止盈'},
            {'name': '定价卖出止损', 'priority': '⭐⭐⭐⭐⭐', 'desc': '-7% 坚决走'},
        ]
        grid_spacing = '2%~3%'
        grid_range_pct = '±8%'
        not_suitable = ['定投（波动太大）', '网格（单边风险）']

    elif etf_type == 'dividend':
        # 高股息 ETF：收息 + 小波段
        strategies = [
            {'name': '定期定投', 'priority': '⭐⭐⭐⭐', 'desc': '长期吃息'},
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐', 'desc': '回调 3%~5% 加仓'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐', 'desc': '涨 8%~10% 后止盈'},
        ]
        grid_spacing = '0.8%~1.2%'
        grid_range_pct = '±4%'
        not_suitable = ['止损（高股息不止损）']

    elif is_stock:
        # 股票：风控第一
        strategies = [
            {'name': '定价卖出止损', 'priority': '⭐⭐⭐⭐⭐', 'desc': '必设！股票必须止损'},
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐', 'desc': '支撑位低吸'},
            {'name': '回落卖出', 'priority': '⭐⭐⭐⭐', 'desc': '波段止盈'},
        ]
        grid_spacing = '不建议'
        grid_range_pct = '不建议'
        not_suitable = ['网格交易（个股风险大）', '定期定投（除非超高股息）']

    else:
        # 未知类型
        strategies = [
            {'name': '定价买入', 'priority': '⭐⭐⭐⭐', 'desc': '先了解品种再决定'},
            {'name': '定价卖出止损', 'priority': '⭐⭐⭐⭐⭐', 'desc': '无论什么品种都设止损'},
        ]
        grid_spacing = '待确认'
        grid_range_pct = '待确认'
        not_suitable = []

    return {
        'strategies': strategies,
        'grid_spacing': grid_spacing,
        'grid_range_pct': grid_range_pct,
        'not_suitable': not_suitable,
    }


def generate_parameters(info: dict, price_data: dict, capital: float, strategies: dict) -> list:
    """
    生成具体参数设置
    """
    code = info['code']
    price = price_data.get('price')
    name = info.get('name', price_data.get('name', ''))
    etf_type = info.get('type', '')
    is_stock = info.get('is_stock', False)

    if not price or price <= 0:
        # 价格获取失败，使用参考值生成参数
        reference_prices = {
            'bond_long': 1.000,
            'bond_short': 1.050,
            'broad': 4.000,
            'gold': 6.000,
            'commodity': 1.200,
            'industry': 1.500,
            'cross_border': 1.800,
            'dividend': 1.200,
            'star': 1.000,
            'growth': 1.500,
        }
        price = reference_prices.get(etf_type, 1.000)
        note_suffix = '（注：当前价格获取失败，以下为参考参数，请手动查询实际价格后调整）'
    else:
        note_suffix = ''

    params = []

    # 根据类型生成具体参数
    if etf_type in ('bond_long', 'bond_short'):
        # 债券网格
        spacing = 0.004
        params.append({
            'strategy': '网格交易',
            'price_range': f'{price - 0.01:.3f} ~ {price + 0.01:.3f}',
            'spacing': f'{spacing:.3f}',
            'per_trade': f'{max(1000, int(capital * 0.05 / price / 100) * 100)} 份',
            'total_capital': f'{capital:.0f} 元',
            'note': '债 ETF 网格最稳，自动高抛低吸',
        })

    elif etf_type == 'gold':
        # 黄金：网格 + 定价买入
        params.append({
            'strategy': '网格交易',
            'price_range': f'{price * 0.96:.2f} ~ {price * 1.04:.2f}',
            'spacing': '0.5%~0.8%',
            'per_trade': f'{max(100, int(capital * 0.03 / price / 100) * 100)} 份',
            'total_capital': f'{capital:.0f} 元',
            'note': '黄金震荡收割，长期底仓不动',
        })
        params.append({
            'strategy': '定价买入（分档）',
            'trigger_price_1': f'≤ {price * 0.97:.2f}（小跌）',
            'trigger_price_2': f'≤ {price * 0.94:.2f}（大跌）',
            'amount_1': f'{int(capital * 0.4):.0f} 元',
            'amount_2': f'{int(capital * 0.6):.0f} 元',
            'note': '分两档买入，避免一把梭',
        })

    elif etf_type == 'commodity':
        # 商品：定价买卖，不做网格
        params.append({
            'strategy': '定价买入（分批）',
            'trigger_1': f'跌 5% → {price * 0.95:.2f}，买 {int(capital * 0.4):.0f} 元',
            'trigger_2': f'跌 8% → {price * 0.92:.2f}，买 {int(capital * 0.6):.0f} 元',
            'note': '商品波动大，分两批买',
        })
        params.append({
            'strategy': '定价卖出（止盈 + 止损）',
            'take_profit': f'涨 12%~18% → {price * 1.12:.2f}~{price * 1.18:.2f}',
            'stop_loss': f'-6% → {price * 0.94:.2f}（必须设！）',
            'note': '商品不做网格，只做分批买卖',
        })

    elif etf_type == 'broad':
        # 宽基：定投 + 波段
        if capital >= 10000:
            weekly_amount = max(500, int(capital * 0.02))
            params.append({
                'strategy': '定期定投',
                'frequency': '每周',
                'amount': f'{weekly_amount} 元',
                'target': f'{code} {name}',
                'note': '宽基定投，长期国运，无视波动',
            })
        params.append({
            'strategy': '回落卖出（止盈）',
            'monitor_gain': '涨幅 ≥ 8%',
            'pullback_sell': '从高点回落 1.5% 自动卖',
            'sell_pct': '总仓位的 20%~30%',
            'note': '涨多了自动止盈，不贪最后一口',
        })

    elif etf_type == 'cross_border':
        # 跨境：波段 + 溢价监控
        params.append({
            'strategy': '反弹买入 + 回落卖出',
            'rebound_buy': '从低点反弹 2% 再进',
            'pullback_sell': '涨 15%+ 后回落 2% 止盈',
            'note': '⚠️ 溢价 >5% 绝对不买！',
        })
        params.append({
            'strategy': '定价卖出止损',
            'stop_loss': '-7%（必须设）',
            'note': '跨境 ETF 有汇率风险，必须止损',
        })

    elif etf_type in ('industry', 'star', 'growth'):
        # 行业/科创：波段 + 止损
        params.append({
            'strategy': '反弹买入',
            'rebound_buy': f'从低点反弹 2%~3% 再进',
            'note': '右侧交易，不抄半山腰',
        })
        params.append({
            'strategy': '回落卖出',
            'monitor_gain': '涨幅 ≥ 10%~15%',
            'pullback_sell': '从高点回落 1.5%~2% 自动卖',
            'note': '行业 ETF 波动大，止盈要果断',
        })
        params.append({
            'strategy': '定价卖出止损',
            'stop_loss': f'-6%~-8%（必须设！）',
            'note': '行业 ETF 可能单边下跌，止损保命',
        })

    elif etf_type == 'dividend':
        # 高股息：定投 + 低吸
        if capital >= 5000:
            weekly_amount = max(300, int(capital * 0.025))
            params.append({
                'strategy': '定期定投',
                'frequency': '每周',
                'amount': f'{weekly_amount} 元',
                'note': '高股息定投，长期吃息',
            })
        params.append({
            'strategy': '定价买入（回调加仓）',
            'trigger': f'跌 3%~5% → {price * 0.95:.2f}~{price * 0.97:.2f}',
            'amount': f'{int(capital * 0.3):.0f} 元/次',
            'note': '高股息不怕跌，越跌越买',
        })

    elif is_stock:
        # 股票：风控第一
        params.append({
            'strategy': '定价卖出止损（必设！）',
            'stop_loss': f'-6%~-8% → {price * 0.92:.2f}~{price * 0.94:.2f}',
            'note': '⚠️ 股票必须设止损，ETF 可以不设，股票必须设！',
        })
        params.append({
            'strategy': '定价买入（低吸）',
            'trigger': f'回调 3%~5% → {price * 0.95:.2f}~{price * 0.97:.2f}',
            'amount': f'{int(capital * 0.3):.0f} 元/次，最多 3 次',
            'note': '支撑位低吸，不追高',
        })
        params.append({
            'strategy': '回落卖出（止盈）',
            'monitor_gain': '涨幅 ≥ 8%~12%',
            'pullback_sell': '从高点回落 1.5%~2.5% 自动卖',
            'note': '股票止盈要果断，不贪',
        })

    else:
        params.append({
            'strategy': '请先确认品种类型',
            'note': f'代码 {code} 未在数据库中，请先确认是 ETF 还是股票，再决定策略',
        })

    return params


def generate_full_report(code: str, capital: float = 0, risk_preference: str = 'balanced') -> dict:
    """
    生成完整分析报告
    """
    # 1. 识别品种
    info = identify_code(code)

    # 2. 获取实时价格
    price_data = fetch_east_money_price(code)

    # 3. 更新名称
    if price_data.get('name') and info.get('name') == '未知':
        info['name'] = price_data['name']

    # 4. 如果是跨境 ETF，获取溢价率
    premium_data = None
    if info.get('type') == 'cross_border':
        premium_data = fetch_qdii_premium(code)

    # 5. 推荐策略
    strategies = get_strategy_recommendation(info, capital, risk_preference)

    # 6. 生成参数（即使没有价格也生成参考参数）
    params = generate_parameters(info, price_data, capital, strategies)
    
    # 如果没有价格，添加提示
    if not price_data.get('price'):
        params.insert(0, {
            'strategy': '⚠️ 价格获取提示',
            'note': '当前无法获取实时价格，以下参数基于参考值生成。请手动查询实际价格后调整。',
        })

    # 7. 组装报告
    report = {
        'code': code,
        'name': info.get('name', price_data.get('name', '未知')),
        'category': info.get('category', '未知'),
        'type': info.get('type', 'unknown'),
        'is_etf': info.get('is_etf', False),
        'is_stock': info.get('is_stock', False),
        'current_price': price_data.get('price'),
        'change_pct': price_data.get('change_pct'),
        'capital': capital,
        'risk_preference': risk_preference,
        'strategies': strategies['strategies'],
        'not_suitable': strategies['not_suitable'],
        'parameters': params,
        'premium': premium_data,
        'disclaimer': '本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。请独立判断并自行承担风险。',
    }

    return report


def format_report_text(report: dict) -> str:
    """格式化为可读文本"""
    lines = []
    lines.append(f"📊 **{report['name']}**（{report['code']}）条件单分析报告")
    lines.append(f"类型：{report['category']} | {'ETF' if report['is_etf'] else '股票'}")

    if report.get('current_price'):
        lines.append(f"当前价格：{report['current_price']:.3f} 元" if report['current_price'] < 100 else f"当前价格：{report['current_price']:.2f} 元")
        if report.get('change_pct'):
            lines.append(f"今日涨跌：{report['change_pct']:+.2f}%")

    if report.get('premium') and report['premium'].get('premium_pct') is not None:
        p = report['premium']['premium_pct']
        warn = ' ⚠️ 溢价过高，不建议买入！' if p > 5 else ''
        lines.append(f"溢价率：{p:+.2f}%{warn}")

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 🎯 推荐策略（按优先级）')

    for i, s in enumerate(report['strategies'], 1):
        lines.append(f"{i}. **{s['name']}** {s['priority']}")
        lines.append(f"   {s['desc']}")

    if report.get('not_suitable'):
        lines.append('')
        lines.append('## ❌ 不适合的策略')
        for ns in report['not_suitable']:
            lines.append(f"- {ns}")

    if report.get('parameters'):
        lines.append('')
        lines.append('---')
        lines.append('')
        lines.append('## ⚙️ 具体参数设置')

        for i, p in enumerate(report['parameters'], 1):
            lines.append(f"\n**{p['strategy']}**")
            for k, v in p.items():
                if k not in ('strategy', 'note'):
                    lines.append(f"  - {k}: {v}")
            if p.get('note'):
                lines.append(f"  💡 {p['note']}")

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append(f"> {report['disclaimer']}")

    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供代码，如: python3 conditional_order.py 518880'}, ensure_ascii=False))
        sys.exit(1)

    code = sys.argv[1]
    capital = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    risk = sys.argv[3] if len(sys.argv) > 3 else 'balanced'

    report = generate_full_report(code, capital, risk)

    # 输出 JSON 和文本
    if '--text' in sys.argv:
        print(format_report_text(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
