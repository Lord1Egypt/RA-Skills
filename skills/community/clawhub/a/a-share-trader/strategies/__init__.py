"""
A股选股策略模块
整合12种选股策略
"""

from .base_strategy import BaseStrategy, Signal

# 基本面策略
try:
    from .fundamental import FundamentalStrategy
except ImportError:
    FundamentalStrategy = None

# 防御策略
try:
    from .defensive import DefensiveStrategy
except ImportError:
    DefensiveStrategy = None

# 震荡选股策略（KDJ）
try:
    from .swing_trading import SwingTradingStrategy
except ImportError:
    SwingTradingStrategy = None

# 小市值策略
try:
    from .small_cap import SmallCapStrategy
except ImportError:
    SmallCapStrategy = None

# 营收利润双增策略
try:
    from .revenue_profit import RevenueProfitStrategy
except ImportError:
    RevenueProfitStrategy = None

# 社保重仓策略
try:
    from .social_security import SocialSecurityStrategy
except ImportError:
    SocialSecurityStrategy = None

# 超跌反弹策略
try:
    from .oversold_rebound import OversoldReboundStrategy
except ImportError:
    OversoldReboundStrategy = None

# 时空共振策略
try:
    from .resonance import ResonanceStrategy
except ImportError:
    ResonanceStrategy = None

# 基本面加小市值策略
try:
    from .quality_small_cap import QualitySmallCapStrategy
except ImportError:
    QualitySmallCapStrategy = None

# 小市值成长策略
try:
    from .small_cap_growth import SmallCapGrowthStrategy
except ImportError:
    SmallCapGrowthStrategy = None

# 控盘策略
try:
    from .chip_concentration import ChipConcentrationStrategy
except ImportError:
    ChipConcentrationStrategy = None

# 导出所有策略类
__all__ = [
    'BaseStrategy',
    'Signal',
    'FundamentalStrategy',
    'DefensiveStrategy',
    'SwingTradingStrategy',
    'SmallCapStrategy',
    'QualitySmallCapStrategy',
    'SmallCapGrowthStrategy',
    'RevenueProfitStrategy',
    'ChipConcentrationStrategy',
    'SocialSecurityStrategy',
    'OversoldReboundStrategy',
    'ResonanceStrategy'
]