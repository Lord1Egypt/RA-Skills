#!/usr/bin/env python3
"""
geo-market-impact-mapper - 市场影响映射

负责获取和分析原油、黄金等大宗商品价格数据，为地缘事件提供市场联动分析。
"""

import requests
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

# =============================================================================
# 配置区
# =============================================================================

VERSION = "1.0.0"

# 阈值配置
OIL_HIGH_THRESHOLD = 3.0    # 原油 ±3%
GOLD_HIGH_THRESHOLD = 2.0   # 黄金 ±2%
OIL_WATCH_THRESHOLD = 1.2   # 原油 ±1.2%
GOLD_WATCH_THRESHOLD = 0.8  # 黄金 ±0.8%

# Yahoo Finance API 端点
YAHOO_OIL_SYMBOL = "CL=F"   # WTI 原油期货
YAHOO_GOLD_SYMBOL = "GC=F"  # 黄金期货

# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class MarketImpact:
    """市场影响数据"""
    oil_pct: float = 0.0      # 原油涨跌幅
    gold_pct: float = 0.0     # 黄金涨跌幅
    oil_pulse: float = 0.0    # 15 分钟脉冲
    gold_pulse: float = 0.0   # 15 分钟脉冲
    oil_price: float = 0.0    # 原油当前价格
    gold_price: float = 0.0   # 黄金当前价格
    oil_prev_close: float = 0.0  # 原油前收盘价
    gold_prev_close: float = 0.0 # 黄金前收盘价
    
    def is_high_priority(self) -> bool:
        """是否达到高优先级阈值"""
        return (
            abs(self.oil_pct) >= OIL_HIGH_THRESHOLD or
            abs(self.gold_pct) >= GOLD_HIGH_THRESHOLD
        )
    
    def is_watch_level(self) -> bool:
        """是否达到观察池阈值"""
        return (
            abs(self.oil_pct) >= OIL_WATCH_THRESHOLD or
            abs(self.gold_pct) >= GOLD_WATCH_THRESHOLD
        )
    
    def get_impact_description(self) -> str:
        """生成市场影响描述"""
        parts = []
        
        if abs(self.oil_pct) >= OIL_WATCH_THRESHOLD:
            direction = "大涨" if self.oil_pct > 0 else "大跌"
            parts.append(f"原油{direction}{abs(self.oil_pct):.1f}%")
        
        if abs(self.gold_pct) >= GOLD_WATCH_THRESHOLD:
            direction = "大涨" if self.gold_pct > 0 else "大跌"
            parts.append(f"黄金{direction}{abs(self.gold_pct):.1f}%")
        
        if not parts:
            return "市场平稳"
        
        return "，".join(parts)
    
    def get_sector_impact(self) -> Dict[str, str]:
        """
        获取对各板块的影响
        返回：{板块：影响方向}
        """
        impact = {}
        
        # 原油影响
        if self.oil_pct > 0:
            impact['石油石化'] = '利多'
            impact['油运'] = '利多'
            impact['航空'] = '利空'
            impact['物流'] = '利空'
        elif self.oil_pct < 0:
            impact['石油石化'] = '利空'
            impact['油运'] = '利空'
            impact['航空'] = '利多'
            impact['物流'] = '利多'
        
        # 黄金影响
        if self.gold_pct > 0:
            impact['有色金属'] = '利多'
            impact['黄金股'] = '利多'
        elif self.gold_pct < 0:
            impact['有色金属'] = '利空'
            impact['黄金股'] = '利空'
        
        return impact
    
    def to_dict(self) -> Dict:
        return {
            'oil_pct': self.oil_pct,
            'gold_pct': self.gold_pct,
            'oil_pulse': self.oil_pulse,
            'gold_pulse': self.gold_pulse,
            'oil_price': self.oil_price,
            'gold_price': self.gold_price,
            'oil_prev_close': self.oil_prev_close,
            'gold_prev_close': self.gold_prev_close,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MarketImpact':
        return cls(
            oil_pct=data.get('oil_pct', 0),
            gold_pct=data.get('gold_pct', 0),
            oil_pulse=data.get('oil_pulse', 0),
            gold_pulse=data.get('gold_pulse', 0),
            oil_price=data.get('oil_price', 0),
            gold_price=data.get('gold_price', 0),
            oil_prev_close=data.get('oil_prev_close', 0),
            gold_prev_close=data.get('gold_prev_close', 0),
        )

# =============================================================================
# 数据获取
# =============================================================================

def fetch_yahoo_price(symbol: str) -> Optional[Dict]:
    """
    从 Yahoo Finance 获取价格数据
    
    返回：{
        'price': float,       # 当前价格
        'prev_close': float,  # 前收盘价
        'change_pct': float,  # 涨跌幅
    }
    """
    try:
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        result = data.get('chart', {}).get('result', [])
        if not result:
            return None
        
        meta = result[0].get('meta', {})
        current_price = meta.get('regularMarketPrice', 0)
        previous_close = meta.get('previousClose', 0)
        
        if previous_close > 0 and current_price > 0:
            change_pct = ((current_price - previous_close) / previous_close) * 100
            return {
                'price': current_price,
                'prev_close': previous_close,
                'change_pct': change_pct,
            }
        
        return None
        
    except Exception as e:
        print(f"⚠️  获取 {symbol} 价格失败：{e}")
        return None

def get_market_data() -> MarketImpact:
    """
    获取完整市场数据
    
    返回：MarketImpact 对象
    """
    market = MarketImpact()
    
    # 获取原油价格
    oil_data = fetch_yahoo_price(YAHOO_OIL_SYMBOL)
    if oil_data:
        market.oil_price = oil_data['price']
        market.oil_prev_close = oil_data['prev_close']
        market.oil_pct = oil_data['change_pct']
    
    # 获取黄金价格
    gold_data = fetch_yahoo_price(YAHOO_GOLD_SYMBOL)
    if gold_data:
        market.gold_price = gold_data['price']
        market.gold_prev_close = gold_data['prev_close']
        market.gold_pct = gold_data['change_pct']
    
    # 打印摘要
    oil_sign = "+" if market.oil_pct >= 0 else ""
    gold_sign = "+" if market.gold_pct >= 0 else ""
    print(f"📊 市场数据：原油{oil_sign}{market.oil_pct:.2f}% 黄金{gold_sign}{market.gold_pct:.2f}%")
    
    return market

# =============================================================================
# 影响分析
# =============================================================================

def analyze_market_impact(market: MarketImpact) -> Dict:
    """
    分析市场影响
    
    返回：{
        'level': str,           # high|watch|normal
        'description': str,     # 描述
        'sectors': Dict,        # 板块影响
        'bias': str,            # 市场偏向
    }
    """
    result = {
        'level': 'normal',
        'description': '市场平稳',
        'sectors': {},
        'bias': '中性',
    }
    
    if market.is_high_priority():
        result['level'] = 'high'
    elif market.is_watch_level():
        result['level'] = 'watch'
    
    result['description'] = market.get_impact_description()
    result['sectors'] = market.get_sector_impact()
    
    # 判断市场偏向
    if market.oil_pct > 2 or market.gold_pct > 1.5:
        result['bias'] = '利多避险资产'
    elif market.oil_pct < -2:
        result['bias'] = '利空原油、利多航空'
    elif market.gold_pct < -1.5:
        result['bias'] = '利空黄金'
    
    return result

def get_event_market_bonus(event_type: str, market: MarketImpact) -> Tuple[float, str]:
    """
    根据事件类型和市场数据计算评分加分
    
    返回：(加分值，原因描述)
    """
    bonus = 0
    reason = ""
    
    if not market.is_watch_level():
        return 0, ""
    
    # 地缘/军事事件 + 原油上涨 = 强关联
    if event_type in ['military', 'geopolitics']:
        if market.oil_pct >= 2:
            bonus = 15
            reason = f"地缘事件 + 原油大涨{market.oil_pct:.1f}% (+15)"
        elif market.oil_pct >= 1:
            bonus = 8
            reason = f"地缘事件 + 原油上涨{market.oil_pct:.1f}% (+8)"
        elif market.gold_pct >= 1.5:
            bonus = 10
            reason = f"地缘事件 + 黄金大涨{market.gold_pct:.1f}% (+10)"
    
    # 央行事件 + 黄金波动 = 强关联
    elif event_type == 'central_bank':
        if abs(market.gold_pct) >= 1.5:
            bonus = 12
            reason = f"央行政策 + 黄金波动{market.gold_pct:.1f}% (+12)"
    
    # 商品事件 + 对应商品波动 = 强关联
    elif event_type == 'commodity':
        if abs(market.oil_pct) >= 2 or abs(market.gold_pct) >= 1.5:
            bonus = 10
            reason = f"商品事件 + 市场联动 (+10)"
    
    return bonus, reason

# =============================================================================
# 行业映射
# =============================================================================

# 影响路径映射表
IMPACT_PATHS = {
    "military": {
        "theme": "地缘冲突升级",
        "factors": ["原油供应扰动", "避险升温"],
        "sectors": {
            "石油石化": ["原油", "石油", "油气", "OPEC", "霍尔木兹"],
            "交通运输": ["航运", "海运", "港口", "运价"],
            "有色金属": ["黄金", "贵金属", "避险"],
            "国防军工": ["军工", "国防", "导弹", "战机", "军事"],
        }
    },
    "central_bank": {
        "theme": "利率中枢变化",
        "factors": ["成长估值承压", "美元偏强", "银行息差变化"],
        "sectors": {
            "银行": ["银行", "利率", "息差", "LPR"],
            "券商": ["券商", "证券", "成交量"],
            "科技": ["科技", "芯片", "半导体", "成长"],
        }
    },
    "commodity": {
        "theme": "商品价格波动",
        "factors": ["成本传导", "通胀预期"],
        "sectors": {
            "石油石化": ["原油", "石油", "炼化"],
            "有色金属": ["黄金", "白银", "铜", "铝"],
            "交通运输": ["航空", "燃油成本"],
        }
    },
    "market": {
        "theme": "市场情绪波动",
        "factors": ["风险偏好变化", "资金流向"],
        "sectors": {
            "券商": ["券商", "证券", "成交量"],
            "银行": ["银行", "金融"],
        }
    },
}

# 自选股行业关键词
STOCK_SECTOR_KEYWORDS = {
    "石油石化": ["石油", "石化", "油气", "中海油", "中石油", "中石化"],
    "银行": ["银行"],
    "券商": ["证券", "券商", "信托", "期货"],
    "有色金属": ["黄金", "贵金属", "锌业", "铜业", "铝业", "有色"],
    "交通运输": ["航运", "海运", "港口", "运输", "航空", "物流"],
    "国防军工": ["军工", "国防", "航天", "船舶", "兵器"],
    "科技": ["科技", "芯片", "半导体", "电子", "通信", "软件"],
    "消费": ["食品", "饮料", "白酒", "啤酒", "旅游", "零售"],
    "医药生物": ["医药", "医疗", "药业", "生物", "健康"],
    "汽车": ["汽车", "客车", "卡车", "零部件", "轮胎"],
}

def map_stocks_to_event(event_type: str, stocks: List[Dict]) -> Tuple[List[Dict], str]:
    """
    根据事件类型映射相关股票
    
    返回：(相关股票列表，影响路径描述)
    """
    if event_type not in IMPACT_PATHS:
        return [], ""
    
    path_info = IMPACT_PATHS[event_type]
    theme = path_info['theme']
    factors = path_info['factors']
    sector_keywords = path_info['sectors']
    
    impact_path = f"{theme} → {' / '.join(factors)}"
    
    related_stocks = []
    matched_codes = set()
    
    for sector, keywords in sector_keywords.items():
        sector_stocks = []
        for stock in stocks:
            code = stock.get('code', '')
            name = stock.get('name', '')
            
            if code in matched_codes:
                continue
            
            stock_keywords = STOCK_SECTOR_KEYWORDS.get(sector, [])
            if stock_keywords and any(kw in name for kw in stock_keywords):
                matched_codes.add(code)
                sector_stocks.append({'code': code, 'name': name, 'sector': sector})
        
        related_stocks.extend(sector_stocks)
    
    return related_stocks, impact_path
