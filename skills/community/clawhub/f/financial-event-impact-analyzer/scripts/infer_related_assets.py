#!/usr/bin/env python3
"""
Infer related assets based on causal relationships, supply chain, substitution effects.
Maps events to potentially affected asset classes and provides indicator IDs for analysis.
"""

import argparse
import json
from typing import Dict, List, Tuple

# Event-to-asset causal mapping
# Based on economic theory: supply chain, substitution, complementary, financial linkages
# ⭐ 核心改动：多经济体全维度分析框架 (中国、日本、韩国、欧洲)
# ⭐ 核心改动：不仅限于可交易金融资产，包括宏观经济指标、利率、货币发行量、汇率

EVENT_ASSET_MAPPING = {
    'oil_price_increase': {
        'benefited': [
            # Direct beneficiaries: oil producers (US)
            {'category': 'energy_producers', 'indicator': 'xle', 'relation': 'upstream', 'reason': '油价上涨增加能源公司收入', 'economy': 'US'},
            {'category': 'oil_services', 'indicator': 'oef', 'relation': 'upstream', 'reason': '钻井活动增加', 'economy': 'US'},
            {'category': 'commodities', 'indicator': 'natural_gas', 'relation': 'substitution', 'reason': '天然气作为替代能源', 'economy': 'Global'},
            
            # Inflation hedges
            {'category': 'precious_metals', 'indicator': 'gold', 'relation': 'inflation_hedge', 'reason': '油价推升通胀预期', 'economy': 'Global'},
            {'category': 'precious_metals', 'indicator': 'silver', 'relation': 'inflation_hedge', 'reason': '商品通胀代理', 'economy': 'Global'},
            
            # ⭐ 多经济体股市受益资产
            {'category': 'china_energy', 'indicator': '159930', 'relation': 'direct', 'reason': '中国能源ETF受益', 'economy': 'China'},
            {'category': 'china_oil_stock', 'indicator': '600938', 'relation': 'direct', 'reason': '中国海油受益油价上涨', 'economy': 'China'},
            {'category': 'china_oil_stock', 'indicator': '601857', 'relation': 'direct', 'reason': '中国石油受益油价上涨', 'economy': 'China'},
            {'category': 'china_oil_stock', 'indicator': '601088', 'relation': 'direct', 'reason': '中国神华能源溢价', 'economy': 'China'},
            {'category': 'hk_energy', 'indicator': 'hsi', 'relation': 'sector', 'reason': '港股能源股受益', 'economy': 'HK'},
            
            {'category': 'japan_energy', 'indicator': 'nikkei225', 'relation': 'sector', 'reason': '日本能源股受益', 'economy': 'Japan'},
            {'category': 'japan_export', 'indicator': 'nikkei225', 'relation': 'currency', 'reason': '日元贬值利好出口', 'economy': 'Japan'},
            
            {'category': 'europe_energy', 'indicator': 'dax', 'relation': 'sector', 'reason': '德国能源股受益', 'economy': 'Europe'},
            {'category': 'europe_energy', 'indicator': 'cac40', 'relation': 'sector', 'reason': '法国能源股受益', 'economy': 'Europe'},
            
            {'category': 'korea_export', 'indicator': 'kospi', 'relation': 'currency', 'reason': '韩元贬值利好出口', 'economy': 'Korea'},
        ],
        'harmed': [
            # Direct sufferers: fuel consumers (US)
            {'category': 'airlines', 'indicator': 'jets', 'relation': 'fuel_cost', 'reason': '燃油是主要运营成本', 'economy': 'US'},
            {'category': 'transportation', 'indicator': 'xli', 'relation': 'fuel_cost', 'reason': '物流成本上升', 'economy': 'US'},
            {'category': 'consumer_discretionary', 'indicator': 'xly', 'relation': 'demand_shift', 'reason': '能源成本上升减少可支配消费', 'economy': 'US'},
            {'category': 'chemicals', 'indicator': 'dow', 'relation': 'input_cost', 'reason': '石油基原料成本上升', 'economy': 'US'},
            
            # ⭐ 多经济体股市受损资产
            {'category': 'china_airline', 'indicator': '601111', 'relation': 'fuel_cost', 'reason': '中国国航燃油成本上升', 'economy': 'China'},
            {'category': 'china_chemical', 'indicator': 'csi300', 'relation': 'input_cost', 'reason': '中国化工板块成本压力', 'economy': 'China'},
            {'category': 'china_transport', 'indicator': 'chinext', 'relation': 'cost', 'reason': '中国运输板块成本上升', 'economy': 'China'},
            
            {'category': 'japan_auto', 'indicator': 'nikkei225', 'relation': 'input_cost', 'reason': '日本汽车股成本上升', 'economy': 'Japan'},
            {'category': 'japan_chemical', 'indicator': 'topix', 'relation': 'input_cost', 'reason': '日本化工股成本压力', 'economy': 'Japan'},
            
            {'category': 'korea_chemical', 'indicator': 'kospi', 'relation': 'input_cost', 'reason': '韩国化工股成本压力', 'economy': 'Korea'},
            {'category': 'korea_airline', 'indicator': 'kospi', 'relation': 'fuel_cost', 'reason': '韩国航空股燃油成本上升', 'economy': 'Korea'},
            
            {'category': 'europe_auto', 'indicator': 'dax', 'relation': 'input_cost', 'reason': '德国汽车股成本上升', 'economy': 'Europe'},
            {'category': 'europe_airline', 'indicator': 'cac40', 'relation': 'fuel_cost', 'reason': '法航燃油成本上升', 'economy': 'Europe'},
            {'category': 'europe_chemical', 'indicator': 'dax', 'relation': 'input_cost', 'reason': '德国化工股成本压力', 'economy': 'Europe'},
            {'category': 'uk_auto', 'indicator': 'ftse100', 'relation': 'input_cost', 'reason': '英国汽车股成本上升', 'economy': 'Europe'},
            
            {'category': 'india_airline', 'indicator': 'sgx_nifty', 'relation': 'fuel_cost', 'reason': '印度航空股燃油成本上升', 'economy': 'India'},
        ],
        'macro_indicators': [
            # ⭐ 美国宏观指标（必须覆盖）
            {'category': 'inflation', 'indicator': 'cpi_us', 'relation': 'cost_push', 'reason': '油价上涨推升美国CPI', 'economy': 'US'},
            {'category': 'inflation', 'indicator': 'ppi_us', 'relation': 'cost_push', 'reason': '油价上涨推升美国PPI', 'economy': 'US'},
            {'category': 'rate', 'indicator': 'fed_funds_rate', 'relation': 'policy_response', 'reason': '通胀压力可能触发加息', 'economy': 'US'},
            {'category': 'rate', 'indicator': 'us_10y_treasury', 'relation': 'inflation_expectation', 'reason': '通胀预期推升美债收益率', 'economy': 'US'},
            {'category': 'money', 'indicator': 'm2_us', 'relation': 'policy', 'reason': '美联储可能收紧货币', 'economy': 'US'},
            
            # ⭐ 中国宏观指标（必须覆盖）
            {'category': 'inflation', 'indicator': 'cpi_china', 'relation': 'cost_push', 'reason': '油价上涨推升中国CPI', 'economy': 'China'},
            {'category': 'inflation', 'indicator': 'ppi_china', 'relation': 'cost_push', 'reason': '油价上涨推升中国PPI', 'economy': 'China'},
            {'category': 'growth', 'indicator': 'gdp_china', 'relation': 'input_cost', 'reason': '油价上涨增加进口成本', 'economy': 'China'},
            {'category': 'activity', 'indicator': 'pmi_china', 'relation': 'cost', 'reason': '油价上涨影响制造业PMI', 'economy': 'China'},
            {'category': 'rate', 'indicator': 'loan_rate_china', 'relation': 'policy', 'reason': '通胀压力可能影响LPR', 'economy': 'China'},
            {'category': 'rate', 'indicator': 'bond_10y_china', 'relation': 'inflation', 'reason': '通胀预期推升国债收益率', 'economy': 'China'},
            {'category': 'money', 'indicator': 'm2_china', 'relation': 'policy', 'reason': '央行可能收紧货币', 'economy': 'China'},
            {'category': 'money', 'indicator': 'm1_china', 'relation': 'policy', 'reason': '货币供应量变化', 'economy': 'China'},
            {'category': 'credit', 'indicator': 'social_financing', 'relation': 'credit', 'reason': '社融规模可能调整', 'economy': 'China'},
            
            # ⭐ 日本宏观指标（必须覆盖）
            {'category': 'inflation', 'indicator': 'cpi_japan', 'relation': 'cost_push', 'reason': '油价上涨推升日本CPI', 'economy': 'Japan'},
            {'category': 'growth', 'indicator': 'gdp_japan', 'relation': 'import_cost', 'reason': '油价上涨增加进口成本', 'economy': 'Japan'},
            {'category': 'rate', 'indicator': 'japan_10y_bond', 'relation': 'policy', 'reason': '日本央行政策调整', 'economy': 'Japan'},
            {'category': 'money', 'indicator': 'm2_japan', 'relation': 'policy', 'reason': '日本央行货币政策', 'economy': 'Japan'},
            
            # ⭐ 韩国宏观指标（必须覆盖）
            {'category': 'inflation', 'indicator': 'cpi_korea', 'relation': 'cost_push', 'reason': '油价上涨推升韩国CPI', 'economy': 'Korea'},
            {'category': 'growth', 'indicator': 'gdp_korea', 'relation': 'import_cost', 'reason': '油价上涨增加进口成本', 'economy': 'Korea'},
            
            # ⭐ 欧洲宏观指标（必须覆盖）
            {'category': 'inflation', 'indicator': 'cpi_eurozone', 'relation': 'cost_push', 'reason': '油价上涨推升欧元区CPI', 'economy': 'Europe'},
            {'category': 'growth', 'indicator': 'gdp_eurozone', 'relation': 'import_cost', 'reason': '油价上涨增加进口成本', 'economy': 'Europe'},
            {'category': 'rate', 'indicator': 'euro_10y_bond', 'relation': 'policy', 'reason': '欧央行政策调整', 'economy': 'Europe'},
            {'category': 'money', 'indicator': 'm2_eurozone', 'relation': 'policy', 'reason': '欧央行货币政策', 'economy': 'Europe'},
            
            # ⭐ 汇率指标（必须覆盖）
            {'category': 'currency', 'indicator': 'usd_cny', 'relation': 'import_cost', 'reason': '油价上涨→中国进口成本→人民币压力', 'economy': 'China'},
            {'category': 'currency', 'indicator': 'usd_jpy', 'relation': 'import_cost', 'reason': '油价上涨→日本进口成本→日元贬值', 'economy': 'Japan'},
            {'category': 'currency', 'indicator': 'usd_krw', 'relation': 'import_cost', 'reason': '油价上涨→韩国进口成本→韩元贬值', 'economy': 'Korea'},
            {'category': 'currency', 'indicator': 'eur_usd', 'relation': 'import_cost', 'reason': '油价上涨→欧洲进口成本→欧元压力', 'economy': 'Europe'},
            {'category': 'currency', 'indicator': 'gbp_usd', 'relation': 'import_cost', 'reason': '油价上涨→英国进口成本→英镑压力', 'economy': 'Europe'},
            {'category': 'currency', 'indicator': 'usd_index', 'relation': 'capital_flow', 'reason': '油价上涨→美元需求', 'economy': 'US'},
        ],
        'neutral_uncertain': [
            {'category': 'financials', 'indicator': 'xlf', 'relation': 'mixed', 'reason': '能源贷款受益，但通胀压制估值', 'economy': 'US'},
            {'category': 'technology', 'indicator': 'xlk', 'relation': 'mixed', 'reason': '能源成本压力，但需求可能转移', 'economy': 'US'},
            {'category': 'china_financials', 'indicator': 'sse50', 'relation': 'mixed', 'reason': '银行股不确定性', 'economy': 'China'},
        ]
    },
    
    'oil_price_decrease': {
        'benefited': [
            {'category': 'airlines', 'indicator': 'jets', 'relation': 'fuel_cost', 'reason': 'Lower fuel costs boost margins'},
            {'category': 'transportation', 'indicator': 'xli', 'relation': 'fuel_cost', 'reason': 'Logistics cost reduction'},
            {'category': 'consumer_discretionary', 'indicator': 'xly', 'relation': 'demand_shift', 'reason': 'Lower energy costs boost spending'},
            {'category': 'chemicals', 'indicator': 'dow', 'relation': 'input_cost', 'reason': 'Lower feedstock costs'},
            {'category': 'asia_equity', 'indicator': 'csi300', 'relation': 'trade_flow', 'reason': 'Import costs reduced'},
        ],
        'harmed': [
            {'category': 'energy_producers', 'indicator': 'xle', 'relation': 'upstream', 'reason': 'Lower revenue'},
            {'category': 'oil_services', 'indicator': 'oef', 'relation': 'upstream', 'reason': 'Reduced drilling activity'},
            {'category': 'precious_metals', 'indicator': 'gold', 'relation': 'inflation', 'reason': 'Inflation expectations decline'},
        ],
    },
    
    'gold_price_increase': {
        'benefited': [
            {'category': 'gold_miners', 'indicator': 'gdx', 'relation': 'direct', 'reason': 'Higher gold prices boost miner revenue'},
            {'category': 'precious_metals', 'indicator': 'silver', 'relation': 'complementary', 'reason': 'Silver often follows gold'},
        ],
        'harmed': [
            {'category': 'equities', 'indicator': 'sp500', 'relation': 'risk_off', 'reason': 'Gold rise signals risk aversion'},
            {'category': 'financials', 'indicator': 'xlf', 'relation': 'inflation', 'reason': 'Lower inflation expectations'},
        ],
        'neutral': [
            {'category': 'commodities', 'indicator': 'copper', 'relation': 'mixed', 'reason': 'Industrial vs precious divergence'},
        ]
    },
    
    'interest_rate_increase': {
        'benefited': [
            {'category': 'financials', 'indicator': 'xlf', 'relation': 'spread', 'reason': 'Higher net interest margin'},
            {'category': 'dollar', 'indicator': 'usd_index', 'relation': 'capital_flow', 'reason': 'Higher yields attract foreign capital'},
        ],
        'harmed': [
            {'category': 'bonds', 'indicator': 'tlt', 'relation': 'price_inverse', 'reason': 'Bond prices fall when rates rise'},
            {'category': 'real_estate', 'indicator': 'iyr', 'relation': 'financing', 'reason': 'Higher mortgage rates'},
            {'category': 'growth_equity', 'indicator': 'nasdaq', 'relation': 'valuation', 'reason': 'Higher discount rate hurts growth stocks'},
            {'category': 'utilities', 'indicator': 'xlu', 'relation': 'financing', 'reason': 'Capital-intensive, debt-heavy'},
        ],
    },
    
    'vix_increase': {
        'benefited': [
            {'category': 'volatility_products', 'indicator': 'vix', 'relation': 'direct', 'reason': 'Direct VIX exposure'},
            {'category': 'defensive', 'indicator': 'xlp', 'relation': 'flight_to_safety', 'reason': 'Consumer staples are defensive'},
            {'category': 'precious_metals', 'indicator': 'gold', 'relation': 'safe_haven', 'reason': 'Traditional safe haven'},
        ],
        'harmed': [
            {'category': 'equities', 'indicator': 'sp500', 'relation': 'risk_off', 'reason': 'Higher volatility = lower risk appetite'},
            {'category': 'growth_equity', 'indicator': 'nasdaq', 'relation': 'risk_off', 'reason': 'Growth stocks more volatility-sensitive'},
            {'category': 'financials', 'indicator': 'xlf', 'relation': 'risk', 'reason': 'Market stress hurts financials'},
        ],
    },
    
    'dollar_strength': {
        'benefited': [
            {'category': 'us_equity', 'indicator': 'sp500', 'relation': 'capital_flow', 'reason': 'Foreign capital inflows'},
            {'category': 'us_bonds', 'indicator': 'tlt', 'relation': 'capital_flow', 'reason': 'Foreign demand for US assets'},
        ],
        'harmed': [
            {'category': 'emerging_equity', 'indicator': 'csi300', 'relation': 'currency_pressure', 'reason': 'EM currencies weaken'},
            {'category': 'commodities', 'indicator': 'gold', 'relation': 'inverse', 'reason': 'Gold priced in USD'},
            {'category': 'commodities', 'indicator': 'brent_crude', 'relation': 'inverse', 'reason': 'Oil priced in USD'},
            {'category': 'exporters', 'indicator': 'xli', 'relation': 'competitive', 'reason': 'US exports less competitive'},
        ],
    },
    
    'inflation_increase': {
        'benefited': [
            {'category': 'commodities', 'indicator': 'gold', 'relation': 'inflation_hedge', 'reason': 'Traditional inflation hedge'},
            {'category': 'commodities', 'indicator': 'silver', 'relation': 'inflation_hedge', 'reason': 'Commodity inflation proxy'},
            {'category': 'energy', 'indicator': 'xle', 'relation': 'commodity', 'reason': 'Energy prices drive inflation'},
            {'category': 'real_assets', 'indicator': 'iyr', 'relation': 'real_asset', 'reason': 'Real estate appreciates with inflation'},
        ],
        'harmed': [
            {'category': 'bonds', 'indicator': 'tlt', 'relation': 'inflation', 'reason': 'Fixed income loses purchasing power'},
            {'category': 'consumer_staples', 'indicator': 'xlp', 'relation': 'margin_pressure', 'reason': 'Input cost pressure'},
            {'category': 'growth_equity', 'indicator': 'nasdaq', 'relation': 'valuation', 'reason': 'Higher discount rate'},
        ],
    },
    
    'recession_signal': {
        'benefited': [
            {'category': 'defensive', 'indicator': 'xlp', 'relation': 'essential', 'reason': 'Staples demand stable'},
            {'category': 'healthcare', 'indicator': 'xlv', 'relation': 'essential', 'reason': 'Healthcare demand stable'},
            {'category': 'utilities', 'indicator': 'xlu', 'relation': 'essential', 'reason': 'Utilities demand stable'},
            {'category': 'precious_metals', 'indicator': 'gold', 'relation': 'safe_haven', 'reason': 'Flight to safety'},
            {'category': 'bonds', 'indicator': 'tlt', 'relation': 'flight_to_quality', 'reason': 'Safe asset demand'},
        ],
        'harmed': [
            {'category': 'consumer_discretionary', 'indicator': 'xly', 'relation': 'cyclical', 'reason': ' discretionary spending falls'},
            {'category': 'industrials', 'indicator': 'xli', 'relation': 'cyclical', 'reason': 'Industrial demand weakens'},
            {'category': 'financials', 'indicator': 'xlf', 'relation': 'credit_risk', 'reason': 'Loan defaults increase'},
            {'category': 'technology', 'indicator': 'xlk', 'relation': 'growth', 'reason': 'Growth stocks hurt in recession'},
        ],
    },
}


# Primary indicator to event type mapping
INDICATOR_EVENT_TYPE = {
    'brent_crude': {'increase': 'oil_price_increase', 'decrease': 'oil_price_decrease'},
    'wti_crude': {'increase': 'oil_price_increase', 'decrease': 'oil_price_decrease'},
    'gold': {'increase': 'gold_price_increase', 'decrease': 'gold_price_decrease'},
    'silver': {'increase': 'precious_metals_increase', 'decrease': 'precious_metals_decrease'},
    'vix': {'increase': 'vix_increase', 'decrease': 'vix_decrease'},
    'usd_index': {'increase': 'dollar_strength', 'decrease': 'dollar_weakness'},
    'us_10y_treasury': {'increase': 'interest_rate_increase', 'decrease': 'interest_rate_decrease'},
    'fed_funds_rate': {'increase': 'interest_rate_increase', 'decrease': 'interest_rate_decrease'},
    'cpi_us': {'increase': 'inflation_increase', 'decrease': 'inflation_decrease'},
    'unemployment_us': {'increase': 'recession_signal', 'decrease': 'recovery_signal'},
}


def infer_related_assets(primary_indicator: str, direction: str) -> Dict:
    """
    Infer related assets based on primary indicator and direction.
    
    Args:
        primary_indicator: The main indicator ID (e.g., 'brent_crude')
        direction: 'increase' or 'decrease'
    
    Returns:
        Dictionary with benefited, harmed, and neutral asset lists
    """
    # Determine event type
    if primary_indicator in INDICATOR_EVENT_TYPE:
        event_type = INDICATOR_EVENT_TYPE[primary_indicator].get(direction, 'unknown')
    else:
        # Try to infer from indicator name patterns
        if 'crude' in primary_indicator or 'oil' in primary_indicator:
            event_type = f"oil_price_{direction}"
        elif 'gold' in primary_indicator or 'silver' in primary_indicator:
            event_type = f"precious_metals_{direction}"
        elif 'vix' in primary_indicator:
            event_type = f"vix_{direction}"
        else:
            event_type = f"generic_price_{direction}"
    
    # Get mapping for event type
    if event_type in EVENT_ASSET_MAPPING:
        mapping = EVENT_ASSET_MAPPING[event_type]
    else:
        # Default mapping for unknown events
        mapping = {
            'benefited': [],
            'harmed': [],
            'neutral_uncertain': []
        }
    
    result = {
        'event_type': event_type,
        'primary_indicator': primary_indicator,
        'direction': direction,
        'benefited': mapping.get('benefited', []),
        'harmed': mapping.get('harmed', []),
        'neutral_uncertain': mapping.get('neutral_uncertain', [])
    }
    
    return result


def get_all_related_indicators(result: Dict) -> List[str]:
    """
    Extract all indicator IDs from the result.
    ⭐ 核心改动：确保每一项都会生成图表
    """
    indicators = set()
    
    # 遍历所有类别（包括 macro_indicators）
    for category in ['benefited', 'harmed', 'neutral_uncertain', 'macro_indicators']:
        for asset in result.get(category, []):
            if 'indicator' in asset:
                indicators.add(asset['indicator'])
    
    return sorted(list(indicators))


def get_multi_economy_summary(result: Dict) -> Dict:
    """
    ⭐ 核心新增：生成多经济体分析摘要
    
    Returns:
        各经济体受影响指标数量统计
    """
    economy_stats = {
        'US': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'China': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'Japan': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'Korea': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'Europe': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'Global': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'HK': {'benefited': 0, 'harmed': 0, 'macro': 0},
        'India': {'benefited': 0, 'harmed': 0, 'macro': 0},
    }
    
    for category in ['benefited', 'harmed', 'neutral_uncertain']:
        for asset in result.get(category, []):
            economy = asset.get('economy', 'Global')
            if economy in economy_stats:
                if category == 'benefited':
                    economy_stats[economy]['benefited'] += 1
                elif category == 'harmed':
                    economy_stats[economy]['harmed'] += 1
    
    for asset in result.get('macro_indicators', []):
        economy = asset.get('economy', 'Global')
        if economy in economy_stats:
            economy_stats[economy]['macro'] += 1
    
    return economy_stats


def list_event_types():
    """List all supported event types."""
    print("\nSupported Event Types:")
    print("=" * 60)
    for event_type in sorted(EVENT_ASSET_MAPPING.keys()):
        mapping = EVENT_ASSET_MAPPING[event_type]
        print(f"\n{event_type}:")
        print(f"  Benefited: {len(mapping.get('benefited', []))} assets")
        print(f"  Harmed: {len(mapping.get('harmed', []))} assets")
        print(f"  Neutral: {len(mapping.get('neutral_uncertain', []))} assets")


def main():
    parser = argparse.ArgumentParser(description='Infer related assets for an event (Multi-Economy Analysis)')
    parser.add_argument('--indicator', required=True, help='Primary indicator ID')
    parser.add_argument('--direction', choices=['increase', 'decrease'], required=True, help='Price direction')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--multi-economy', action='store_true', help='Enable multi-economy analysis (default: True)')
    parser.add_argument('--list-events', action='store_true', help='List all event types')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.list_events:
        list_event_types()
        return
    
    result = infer_related_assets(args.indicator, args.direction)
    
    # ⭐ 添加多经济体摘要
    economy_summary = get_multi_economy_summary(result)
    result['economy_summary'] = economy_summary
    
    print(f"\n=== {result['event_type']} 多经济体分析 ===")
    print(f"Primary Indicator: {result['primary_indicator']} ({result['direction']})")
    
    # ⭐ 输出多经济体统计
    print(f"\n📊 多经济体影响统计:")
    for economy, stats in economy_summary.items():
        total = stats['benefited'] + stats['harmed'] + stats['macro']
        if total > 0:
            print(f"  {economy}: 受益{stats['benefited']}项 / 受损{stats['harmed']}项 / 宏观{stats['macro']}项")
    
    print(f"\n📈 受益资产 ({len(result['benefited'])}):")
    for asset in result['benefited']:
        economy_tag = f"[{asset.get('economy', 'Global')}]"
        print(f"  - {economy_tag} {asset['category']}: {asset['indicator']}")
        print(f"    Reason: {asset['reason']}")
    
    print(f"\n📉 受损资产 ({len(result['harmed'])}):")
    for asset in result['harmed']:
        economy_tag = f"[{asset.get('economy', 'Global')}]"
        print(f"  - {economy_tag} {asset['category']}: {asset['indicator']}")
        print(f"    Reason: {asset['reason']}")
    
    # ⭐ 输出宏观指标（新增）
    macro_indicators = result.get('macro_indicators', [])
    if macro_indicators:
        print(f"\n📊 宏观指标 ({len(macro_indicators)}):")
        for asset in macro_indicators:
            economy_tag = f"[{asset.get('economy', 'Global')}]"
            print(f"  - {economy_tag} {asset['category']}: {asset['indicator']}")
            print(f"    Reason: {asset['reason']}")
    
    print(f"\n📋 所有相关指标（将生成单独图表）: {get_all_related_indicators(result)}")
    print(f"   总计: {len(get_all_related_indicators(result))} 项")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✓ 已保存: {args.output}")
    else:
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()