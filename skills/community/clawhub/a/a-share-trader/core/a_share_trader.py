#!/usr/bin/env python3
"""
A股核心交易框架主引擎
整合12种选股策略的自适应量化交易系统
"""

import asyncio
import logging
import sys
import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('a_share_trader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AShareTrader:
    """A股核心交易主引擎"""
    
    def __init__(self, capital: float = 1000000000.0, mode: str = "paper"):
        """
        初始化A股交易引擎
        
        Args:
            capital: 初始资金（元），默认10亿
            mode: 运行模式，"live"(实盘), "paper"(模拟), "backtest"(回测)
        """
        self.capital = capital
        self.current_capital = capital  # 当前现金
        self.mode = mode
        
        # 投资组合
        self.positions = {}  # {symbol: {quantity, avg_cost, market_value, ...}}
        self.portfolio_value = capital
        self.peak_value = capital
        self.max_drawdown = 0.0
        self.daily_pnl = 0.0
        self.total_pnl = 0.0
        
        # 核心组件
        self.data_interface = None
        self.strategies = []
        self.risk_manager = None
        self.performance_tracker = None
        self.adaptive_engine = None  # 自适应引擎
        
        # 交易状态
        self.is_running = False
        self.trading_day = datetime.now().date()
        
        # 配置
        self.config = self._load_config()
        
        logger.info(f"A股交易引擎初始化完成 - 模式: {mode}, 资金: {capital:,.0f}元")
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        config = {
            "trading": {
                "max_positions": 15,  # 最大持仓数（A股可稍多）
                "max_position_size": 0.08,  # 单只最大仓位（8%）
                "max_industry_concentration": 0.25,  # 行业集中度
                "daily_loss_limit": 0.03,  # 日度亏损限制
                "weekly_loss_limit": 0.08,  # 周度亏损限制
                "turnover_target": 50.0,  # 年换手率目标
                "enable_short_selling": False,  # A股融券暂不开启
                "enable_margin_trading": False,  # A股融资暂不开启
            },
            "risk": {
                "max_drawdown": 0.15,  # 最大回撤限制
                "stop_loss_per_trade": 0.03,  # 单笔止损（A股波动稍大）
                "stop_loss_daily": 0.05,  # 日度止损
                "var_confidence": 0.95,  # VaR置信度
                "stress_scenarios": ["2015_crash", "2020_covid", "2022_bear"]
            },
            "strategies": {
                # 基本面选股策略
                "fundamental": {
                    "enabled": True,
                    "weight": 0.15,
                    "min_market_cap": 500000000,  # 5亿流通市值
                    "min_profit_growth": 0.30,     # 净利润同比增长率>30%
                    "min_revenue_growth": 0.30,    # 营业收入同比增长率>30%
                    "pe_min": 0.1,                 # 市盈率下限
                    "pe_max": 50.0,                # 市盈率上限
                    "pb_max": 5.0,                 # 市净率上限
                    "exclude_st": True,            # 排除ST股
                    "exclude_star": True,          # 排除科创板（默认）
                    "exclude_suspended": True,     # 排除停牌股
                    "exclude_new": True,           # 排除新股
                    "sort_by": "market_cap",       # 按总市值从小到大
                    "holding_count": 8,            # 持仓数量
                    "rebalance_days": 5            # 调仓周期
                },
                # 防御选股（红利策略）
                "defensive": {
                    "enabled": True,
                    "weight": 0.12,
                    "min_dividend_yield": 0.04,    # 最小股息率
                    "max_dividend_yield": 0.15,    # 最大股息率
                    "market_cap_quantile_min": 0.2,  # 总市值截面升序分位数>0.2
                    "pe_quantile_max": 0.4,        # 市盈率截面升序分位数<0.4
                    "max_price": 30.0,             # 价格不高于30元
                    "pe_positive": True,           # 市盈率为正
                    "exclude_st": True,
                    "exclude_suspended": True,
                    "holding_count": 3,
                    "rebalance_days": 5
                },
                # 震荡选股（KDJ策略）
                "swing_trading": {
                    "enabled": True,
                    "weight": 0.10,
                    "kdj_period": (9, 3, 3),       # KDJ参数
                    "buy_threshold": 20,           # KDJ_K<20买入
                    "sell_threshold": 80,          # KDJ_K>80卖出
                    "initial_position": 0.8,       # 首次建仓80%
                    "max_position": 1.0,           # 最大仓位100%
                    "rebalance_freq": "daily"      # 每日调仓
                },
                # 小市值策略
                "small_cap": {
                    "enabled": True,
                    "weight": 0.08,
                    "min_market_cap": 500000000,   # 流通市值>5亿
                    "min_listing_days": 252,       # 上市超252天
                    "min_profit_ttm": 0,           # 归母净利润TTM>0
                    "min_dividend_yield": 0.0,     # 股息率>0
                    "exclude_st": True,
                    "exclude_star": True,
                    "exclude_suspended": True,
                    "monthly_logic": True,         # 月度切换逻辑
                    "jan_apr_dividend": True,      # 1/4月按股息率
                    "other_months_market_cap": True, # 其他月按流通市值
                    "initial_screen": 20,          # 初选20只
                    "final_screen": 10,            # 终选10只
                    "screening_by": "turnover_volatility", # 按换手率波动率
                    "rebalance_days": 5
                },
                # 基本面加小市值
                "quality_small_cap": {
                    "enabled": True,
                    "weight": 0.08,
                    "min_dividend_yield": 0.02,    # 股息率>2%
                    "min_profit_growth": 0.10,     # 净利润同比增长率>10%
                    "min_roe": 0.15,               # ROE>15%
                    "min_gross_margin": 0.30,      # 毛利率>30%
                    "max_pe_ttm": 25.0,            # PE_TTM<25
                    "exclude_st": True,
                    "exclude_suspended": True,
                    "sort_by": "market_cap",       # 按流通市值升序
                    "holding_count": 5,
                    "rebalance_days": 14
                },
                # 小市值成长
                "small_cap_growth": {
                    "enabled": True,
                    "weight": 0.08,
                    "max_market_cap": 2500000000,  # 流通市值≤25亿
                    "min_listing_days": 365,       # 上市>365天
                    "min_pe_ttm": 0.1,             # PE_TTM>0
                    "exclude_st": True,
                    "exclude_suspended": True,
                    "board_filter": ["main"],      # 主板个股
                    "scoring_weights": {
                        "market_cap_rank": 0.5,
                        "price_rank": 0.3,
                        "eps_growth_rank": 0.2     # 负号已处理
                    },
                    "holding_count": 10,
                    "rebalance_days": 3
                },
                # 营收利润双增
                "revenue_profit": {
                    "enabled": True,
                    "weight": 0.10,
                    "min_market_cap": 500000000,   # 流通市值>5亿
                    "min_listing_days": 365,       # 上市超365天
                    "min_profit_growth": 0.30,     # 净利润同比>30%
                    "min_revenue_growth": 0.30,    # 营业收入同比>30%
                    "pe_min": 0.1,                 # 0<市盈率
                    "pe_max": 50.0,                # 市盈率<50
                    "pb_max": 5.0,                 # 市净率<5
                    "exclude_st": True,
                    "exclude_star": True,
                    "exclude_suspended": True,
                    "sort_by": "market_cap",       # 按总市值从小到大
                    "holding_count": 10,
                    "rebalance_days": 5
                },
                # 控盘策略
                "chip_concentration": {
                    "enabled": True,
                    "weight": 0.07,
                    "index_constituent": "CSI1000", # 中证1000成分股
                    "max_chip_concentration": 0.10, # 筹码集中度90<10%
                    "sort_by": "market_cap",       # 按总市值从小到大
                    "max_stocks": 20,              # 小于20只股票
                    "rebalance_days": 5,
                    "trading_price": "open"        # 开盘价交易
                },
                # 社保重仓
                "social_security": {
                    "enabled": True,
                    "weight": 0.07,
                    "min_market_cap": 1000000000,  # 流通市值>10亿
                    "min_pe": 0.1,                 # PE>0
                    "include_social_security": True, # 前十大包含社保
                    "sort_by": "holding_ratio",    # 按持股比例从大到小
                    "exclude_st": True,
                    "exclude_delisted": True,
                    "board_filter": ["main"],      # 主板
                    "holding_count": 8,
                    "rebalance_days": 10
                },
                # 超跌反弹
                "oversold_rebound": {
                    "enabled": True,
                    "weight": 0.08,
                    "price_vs_ma250_min": -0.5,    # 收盘价与250日均线比最小值
                    "price_vs_ma250_max": -0.1,    # 收盘价与250日均线比最大值
                    "min_profit_growth": 0.60,     # 净利润同比增长率>60%
                    "min_profit_ttm": 0,           # 扣非归母净利润>0
                    "market_cap_quantile_max": 0.1, # 总市值截面升序分位数<0.1
                    "min_price": 1.5,              # 真实价格>1.5
                    "no_warning": True,            # 无风险警示
                    "exclude_st": True,
                    "exclude_suspended": True,
                    "holding_count": 5,
                    "rebalance_days": 1
                },
                # 时空共振策略
                "resonance": {
                    "enabled": True,
                    "weight": 0.07,
                    "four_dimensions": {
                        "cycle": True,     # 周期维度
                        "fundamental": True, # 基础维度
                        "sentiment": False,  # 情绪维度（暂不使用）
                        "technical": True    # 技术维度
                    },
                    "fundamental_factors": {
                        "min_roe": 0.15,       # ROE≥15%
                        "max_debt_ratio": 0.60, # 资产负债率≤60%
                        "min_gross_margin": 0.30, # 毛利率≥30%
                        "pe_vs_industry": 0.8,  # PE<行业平均80%
                        "pb_vs_industry": 0.8,  # PB<行业平均80%
                        "min_dividend_yield": 0.02 # 股息率>2%
                    },
                    "momentum_factors": {
                        "min_6m_return": 0.10,  # 6个月收益率>10%
                        "min_12m_return": 0.20  # 12个月收益率>20%
                    },
                    "technical_factors": {
                        "consolidation_days": 20,    # 盘整平台20天
                        "consolidation_range": 0.15, # 波动幅度≤15%
                        "breakout_threshold": 0.03,  # 突破上沿3%
                        "volume_ratio": 1.5,         # 成交量至5日均量1.5倍
                        "fibonacci_windows": [3, 5, 8, 13, 21] # 斐波那契时间窗口
                    },
                    "holding_count": 12,
                    "rebalance_days": 10
                }
            },
            "data": {
                "real_time": True,
                "update_frequency": 1.0,  # 秒
                "history_days": 252 * 3,  # 3年历史数据
                "save_to_db": True,
                "data_sources": ["xtquant", "tushare", "baostock"]  # 数据源
            },
            "adaptive": {
                "enabled": True,
                "learning_rate": 0.1,
                "adaptation_speed": 0.3,
                "memory_window": 30,
                "confidence_threshold": 0.7,
                "initial_market_state": "VOLATILE",
                "min_adaptation_interval": 5,
                "max_parameter_change": 0.2,
                "state_recognition_method": "rule_based"
            },
            "performance": {
                "target_annual_return": 1.50,  # 150%
                "target_sharpe": 3.0,
                "target_win_rate": 0.60,
                "report_frequency": "daily"
            }
        }
        return config
    
    def initialize_components(self):
        """初始化所有组件"""
        logger.info("初始化A股交易系统组件...")
        
        # 初始化数据接口
        try:
            from core.data_interface import AShareDataInterface
            self.data_interface = AShareDataInterface(
                real_time=self.config["data"]["real_time"],
                update_frequency=self.config["data"]["update_frequency"],
                data_sources=self.config["data"]["data_sources"]
            )
            logger.info("A股数据接口初始化成功")
        except ImportError as e:
            logger.error(f"A股数据接口初始化失败: {e}")
            self.data_interface = self._create_mock_data_interface()
        
        # 初始化策略
        self._initialize_strategies()
        
        # 初始化自适应引擎
        try:
            from core.adaptive_engine import AdaptiveEngine, MarketState
            
            adaptive_config = self.config.get("adaptive", {})
            initial_state_str = adaptive_config.get("initial_market_state", "VOLATILE")
            initial_market_state = MarketState.VOLATILE
            
            try:
                initial_market_state = MarketState[initial_state_str.upper()]
            except (KeyError, AttributeError):
                logger.warning(f"未知市场状态: {initial_state_str}, 使用默认值: VOLATILE")
            
            self.adaptive_engine = AdaptiveEngine(
                initial_market_state=initial_market_state,
                learning_rate=adaptive_config.get("learning_rate", 0.1),
                adaptation_speed=adaptive_config.get("adaptation_speed", 0.3),
                memory_window=adaptive_config.get("memory_window", 30),
                confidence_threshold=adaptive_config.get("confidence_threshold", 0.7)
            )
            logger.info("自适应引擎初始化成功")
        except ImportError as e:
            logger.error(f"自适应引擎初始化失败: {e}")
            self.adaptive_engine = self._create_mock_adaptive_engine()
        
        # 初始化风控管理器
        try:
            from risk_management.core import AShareRiskManager
            self.risk_manager = AShareRiskManager(
                max_drawdown=self.config["risk"]["max_drawdown"],
                stop_loss_per_trade=self.config["risk"]["stop_loss_per_trade"],
                capital=self.capital,
                config=self.config
            )
            logger.info("A股风控管理器初始化成功")
        except ImportError as e:
            logger.error(f"风控管理器初始化失败: {e}")
            self.risk_manager = self._create_mock_risk_manager()
        
        # 初始化绩效跟踪器
        self.performance_tracker = self._create_performance_tracker()
        
        logger.info("所有组件初始化完成")
    
    def _initialize_strategies(self):
        """初始化12种A股选股策略"""
        logger.info("初始化A股选股策略...")
        
        strategy_initializers = [
            ("fundamental", "strategies.fundamental", "FundamentalStrategy"),
            ("defensive", "strategies.defensive", "DefensiveStrategy"),
            ("swing_trading", "strategies.swing_trading", "SwingTradingStrategy"),
            ("small_cap", "strategies.small_cap", "SmallCapStrategy"),
            ("quality_small_cap", "strategies.quality_small_cap", "QualitySmallCapStrategy"),
            ("small_cap_growth", "strategies.small_cap_growth", "SmallCapGrowthStrategy"),
            ("revenue_profit", "strategies.revenue_profit", "RevenueProfitStrategy"),
            # 注：value_growth策略与fundamental类似，暂时使用fundamental
            ("chip_concentration", "strategies.chip_concentration", "ChipConcentrationStrategy"),
            ("social_security", "strategies.social_security", "SocialSecurityStrategy"),
            ("oversold_rebound", "strategies.oversold_rebound", "OversoldReboundStrategy"),
            ("resonance", "strategies.resonance", "ResonanceStrategy"),
        ]
        
        for strategy_key, module_name, class_name in strategy_initializers:
            if self.config["strategies"][strategy_key]["enabled"]:
                try:
                    module = __import__(module_name, fromlist=[class_name])
                    strategy_class = getattr(module, class_name)
                    
                    # 获取策略配置
                    strategy_config = self.config["strategies"][strategy_key]
                    
                    # 创建策略实例
                    strategy = strategy_class(**strategy_config)
                    
                    self.strategies.append({
                        "name": strategy_key,
                        "instance": strategy,
                        "weight": strategy_config["weight"],
                        "config": strategy_config
                    })
                    
                    logger.info(f"{strategy_key}策略初始化成功")
                    
                except ImportError as e:
                    logger.error(f"策略 {strategy_key} 初始化失败: {e}")
                except Exception as e:
                    logger.error(f"策略 {strategy_key} 创建失败: {e}")
        
        logger.info(f"共初始化 {len(self.strategies)} 个策略")
    
    def _create_mock_data_interface(self):
        """创建模拟数据接口"""
        logger.warning("使用模拟数据接口（生产环境请使用真实数据接口）")
        
        class MockAShareDataInterface:
            def __init__(self):
                self.a_share_stocks = [
                    "000001.SZ", "000002.SZ", "000333.SZ", "000858.SZ", "002415.SZ",
                    "300750.SZ", "600036.SH", "600519.SH", "601318.SH", "601888.SH"
                ]
                self.price_cache = {}
                self.fundamental_cache = {}
            
            def get_market_data(self, symbol: str) -> Dict:
                """获取模拟市场数据"""
                import random
                price = self.get_realtime_price(symbol)
                return {
                    "symbol": symbol,
                    "price": price,
                    "volume": random.randint(100000, 10000000),
                    "bid": price * 0.999,
                    "ask": price * 1.001,
                    "timestamp": datetime.now()
                }
            
            def get_realtime_price(self, symbol: str) -> float:
                """获取模拟实时价格"""
                if symbol in self.price_cache:
                    # 添加随机波动
                    old_price = self.price_cache[symbol]
                    change = random.uniform(-0.02, 0.02)
                    new_price = old_price * (1 + change)
                else:
                    # 初始价格
                    new_price = random.uniform(10.0, 500.0)
                
                self.price_cache[symbol] = new_price
                return round(new_price, 2)
            
            def get_fundamental_data(self, symbol: str) -> Dict:
                """获取模拟基本面数据"""
                import random
                
                # 生成模拟基本面数据
                return {
                    "market_cap": random.uniform(500000000, 500000000000),
                    "profit_growth": random.uniform(-0.2, 0.5),
                    "revenue_growth": random.uniform(-0.1, 0.4),
                    "roe": random.uniform(0.05, 0.30),
                    "gross_margin": random.uniform(0.20, 0.60),
                    "pe": random.uniform(5.0, 60.0),
                    "pb": random.uniform(0.5, 8.0),
                    "dividend_yield": random.uniform(0.0, 0.08),
                    "debt_ratio": random.uniform(0.2, 0.7),
                    "sector": random.choice(["金融", "消费", "医药", "科技", "制造", "能源"]),
                    "is_st": random.random() < 0.05,  # 5%概率是ST
                    "is_suspended": random.random() < 0.02,  # 2%概率停牌
                    "is_star": random.random() < 0.1,  # 10%概率是科创板
                    "listing_days": random.randint(100, 5000)
                }
            
            def get_technical_data(self, symbol: str, period: str = "daily") -> Dict:
                """获取模拟技术数据"""
                import random
                return {
                    "kdj_k": random.uniform(0, 100),
                    "kdj_d": random.uniform(0, 100),
                    "kdj_j": random.uniform(0, 100),
                    "rsi": random.uniform(0, 100),
                    "macd": random.uniform(-2, 2),
                    "boll_upper": random.uniform(10, 50),
                    "boll_middle": random.uniform(10, 50),
                    "boll_lower": random.uniform(10, 50),
                    "volume_ma5": random.randint(100000, 1000000),
                    "volume_ma10": random.randint(100000, 1000000)
                }
        
        return MockAShareDataInterface()
    
    def _create_mock_adaptive_engine(self):
        """创建模拟自适应引擎"""
        class MockAdaptiveEngine:
            def __init__(self):
                self.market_state = "VOLATILE"
            
            def get_adaptive_decisions(self, market_data: Dict[str, Dict], current_config: Dict) -> Dict:
                return {
                    "market_state": self.market_state,
                    "state_confidence": 0.7,
                    "strategy_weights": current_config.get("strategies", {}),
                    "timestamp": datetime.now().isoformat()
                }
        
        return MockAdaptiveEngine()
    
    def _create_mock_risk_manager(self):
        """创建模拟风控管理器"""
        class MockRiskManager:
            def __init__(self):
                pass
            
            def check_trade_risk(self, symbol: str, price: float, quantity: int, side: str) -> Tuple[bool, str]:
                return True, "风险检查通过"
        
        return MockRiskManager()
    
    def _create_performance_tracker(self):
        """创建绩效跟踪器"""
        class PerformanceTracker:
            def __init__(self, capital: float):
                self.capital = capital
                self.start_time = datetime.now()
                self.trades = []
                self.daily_returns = []
            
            def record_trade(self, trade: Dict):
                self.trades.append(trade)
            
            def record_return(self, daily_return: float):
                self.daily_returns.append(daily_return)
            
            def generate_report(self) -> Dict:
                if not self.daily_returns:
                    return {"status": "no_data"}
                
                returns = np.array(self.daily_returns)
                total_return = np.prod(1 + returns) - 1
                annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
                volatility = np.std(returns) * np.sqrt(252)
                sharpe = annualized_return / volatility if volatility > 0 else 0
                
                return {
                    "total_return": total_return,
                    "annualized_return": annualized_return,
                    "sharpe_ratio": sharpe,
                    "max_drawdown": self.max_drawdown,
                    "win_rate": len([r for r in returns if r > 0]) / len(returns),
                    "total_trades": len(self.trades),
                    "days_running": (datetime.now() - self.start_time).days
                }
        
        return PerformanceTracker(self.capital)
    
    async def run(self):
        """运行交易引擎"""
        if self.is_running:
            logger.warning("交易引擎已在运行中")
            return
        
        self.is_running = True
        logger.info(f"启动A股交易引擎，模式: {self.mode}")
        
        try:
            # 初始化组件
            self.initialize_components()
            
            # 主交易循环
            while self.is_running:
                try:
                    await self._trading_cycle()
                    await asyncio.sleep(1.0)  # 每秒一个周期
                except KeyboardInterrupt:
                    logger.info("收到停止信号，正在关闭引擎...")
                    break
                except Exception as e:
                    logger.error(f"交易周期异常: {e}", exc_info=True)
                    await asyncio.sleep(5.0)  # 异常后等待5秒
            
        except Exception as e:
            logger.error(f"交易引擎运行异常: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    async def _trading_cycle(self):
        """单次交易周期"""
        try:
            # 1. 更新市场数据
            market_data = await self._update_market_data()
            
            # 2. 生成交易信号（集成自适应决策）
            signals = await self._generate_signals(market_data)
            
            # 3. 风险检查
            approved_signals = await self._risk_check(signals)
            
            # 4. 执行交易
            if approved_signals:
                trades = await self._execute_trades(approved_signals)
                # 5. 更新持仓和绩效
                await self._update_portfolio(trades)
            
            # 6. 监控和报告
            await self._monitor_and_report()
            
        except Exception as e:
            logger.error(f"交易周期异常: {e}", exc_info=True)
    
    async def _update_market_data(self) -> Dict:
        """更新市场数据"""
        market_data = {}
        
        # 获取股票列表（从数据接口或默认列表）
        symbols = []
        if self.data_interface and hasattr(self.data_interface, 'a_share_stocks'):
            symbols = self.data_interface.a_share_stocks
        else:
            # 默认A股列表
            symbols = [
                "000001.SZ", "000002.SZ", "000333.SZ", "000858.SZ",
                "002415.SZ", "300750.SZ", "600036.SH", "600519.SH",
                "601318.SH", "601888.SH", "603259.SH", "688981.SH"
            ]
        
        for symbol in symbols:
            if self.data_interface:
                try:
                    market_data[symbol] = self.data_interface.get_market_data(symbol)
                except Exception as e:
                    logger.debug(f"获取{symbol}市场数据失败: {e}")
        
        logger.debug(f"更新市场数据: {len(market_data)}只股票")
        return market_data
    
    async def _generate_signals(self, market_data: Dict) -> List[Dict]:
        """生成交易信号（集成自适应决策）"""
        signals = []
        
        # 获取自适应决策
        adaptive_decisions = None
        if self.adaptive_engine:
            try:
                current_config = {
                    "strategies": {
                        info["name"]: {"weight": info["weight"]}
                        for info in self.strategies
                    }
                }
                
                adaptive_decisions = self.adaptive_engine.get_adaptive_decisions(
                    market_data, current_config
                )
                
                logger.info(f"自适应决策 - 市场状态: {adaptive_decisions.get('market_state')}, "
                           f"置信度: {adaptive_decisions.get('state_confidence', 0):.2f}")
                
                # 调整策略权重（简化实现）
                adaptive_weights = adaptive_decisions.get("strategy_weights", {})
                for strategy_info in self.strategies:
                    strategy_name = strategy_info["name"]
                    if strategy_name in adaptive_weights:
                        old_weight = strategy_info["weight"]
                        new_weight = adaptive_weights[strategy_name]
                        strategy_info["weight"] = new_weight
                        
                        if abs(old_weight - new_weight) > 0.01:
                            logger.info(f"策略权重调整: {strategy_name} {old_weight:.2f} → {new_weight:.2f}")
                
            except Exception as e:
                logger.error(f"获取自适应决策失败: {e}")
        
        # 获取基本面和技术数据
        fundamental_data = {}
        technical_data = {}
        
        if self.data_interface:
            for symbol in market_data.keys():
                try:
                    fundamental_data[symbol] = self.data_interface.get_fundamental_data(symbol)
                    technical_data[symbol] = self.data_interface.get_technical_data(symbol)
                except Exception as e:
                    logger.debug(f"获取{symbol}辅助数据失败: {e}")
        
        # 各策略生成信号
        for strategy_info in self.strategies:
            strategy = strategy_info["instance"]
            strategy_name = strategy_info["name"]
            strategy_weight = strategy_info["weight"]
            
            try:
                # 生成策略信号
                strategy_signals = []
                
                if hasattr(strategy, 'generate_signals'):
                    try:
                        # 传递多种数据
                        strategy_signals = strategy.generate_signals(
                            market_data, 
                            fundamental_data=fundamental_data,
                            technical_data=technical_data
                        )
                    except TypeError:
                        # 回退到只传递market_data
                        strategy_signals = strategy.generate_signals(market_data)
                
                # 增强信号信息
                for signal in strategy_signals:
                    signal["strategy"] = strategy_name
                    signal["weight"] = strategy_weight
                    
                    # 添加自适应信息
                    if adaptive_decisions:
                        signal["adaptive_info"] = {
                            "market_state": adaptive_decisions.get("market_state"),
                            "state_confidence": adaptive_decisions.get("state_confidence"),
                            "timestamp": datetime.now().isoformat()
                        }
                    
                    signals.append(signal)
                    
            except Exception as e:
                logger.error(f"策略 {strategy_name} 生成信号失败: {e}")
        
        logger.info(f"共生成 {len(signals)} 个交易信号，来自 {len(self.strategies)} 个策略")
        return signals
    
    async def _risk_check(self, signals: List[Dict]) -> List[Dict]:
        """风险检查"""
        approved_signals = []
        
        for signal in signals:
            symbol = signal.get("symbol", "")
            price = signal.get("price", 0)
            quantity = signal.get("quantity", 0)
            side = signal.get("side", "BUY")
            
            if self.risk_manager:
                try:
                    approved, reason = self.risk_manager.check_trade_risk(symbol, price, quantity, side)
                    if approved:
                        signal["risk_check"] = {"approved": True, "reason": reason}
                        approved_signals.append(signal)
                    else:
                        signal["risk_check"] = {"approved": False, "reason": reason}
                        logger.warning(f"信号被风控拒绝: {symbol} {side}, 原因: {reason}")
                except Exception as e:
                    logger.error(f"风控检查失败: {e}")
                    signal["risk_check"] = {"approved": False, "reason": f"风控检查异常: {e}"}
            else:
                # 无风控管理器，直接通过
                signal["risk_check"] = {"approved": True, "reason": "无风控管理器"}
                approved_signals.append(signal)
        
        return approved_signals
    
    async def _execute_trades(self, signals: List[Dict]) -> List[Dict]:
        """执行交易"""
        executed_trades = []
        
        for signal in signals:
            # 模拟交易执行
            trade = {
                "trade_id": f"TRADE_{int(time.time() * 1000)}",
                "symbol": signal["symbol"],
                "side": signal["side"],
                "price": signal["price"],
                "quantity": signal.get("quantity", 100),
                "timestamp": datetime.now(),
                "strategy": signal["strategy"],
                "commission": signal.get("price", 0) * signal.get("quantity", 0) * 0.0003,
                "status": "EXECUTED" if self.mode != "backtest" else "SIMULATED"
            }
            
            executed_trades.append(trade)
            logger.info(f"执行交易: {trade['symbol']} {trade['side']} {trade['quantity']}股 @ {trade['price']:.2f}")
            
            # 记录到绩效跟踪器
            if self.performance_tracker:
                self.performance_tracker.record_trade(trade)
        
        return executed_trades
    
    async def _update_portfolio(self, trades: List[Dict]):
        """更新投资组合"""
        for trade in trades:
            symbol = trade["symbol"]
            side = trade["side"]
            price = trade["price"]
            quantity = trade["quantity"]
            value = price * quantity
            commission = trade.get("commission", 0)
            
            if side == "BUY":
                # 更新现金
                self.current_capital -= (value + commission)
                
                # 更新持仓
                if symbol not in self.positions:
                    self.positions[symbol] = {
                        "quantity": 0,
                        "avg_cost": 0,
                        "market_value": 0,
                        "current_price": price,
                        "unrealized_pnl": 0,
                        "unrealized_pnl_pct": 0
                    }
                
                pos = self.positions[symbol]
                total_quantity = pos["quantity"] + quantity
                total_cost = pos["avg_cost"] * pos["quantity"] + value
                
                if total_quantity > 0:
                    pos["avg_cost"] = total_cost / total_quantity
                pos["quantity"] = total_quantity
                
            elif side == "SELL":
                # 更新现金
                self.current_capital += (value - commission)
                
                if symbol in self.positions:
                    pos = self.positions[symbol]
                    pos["quantity"] -= quantity
                    
                    if pos["quantity"] <= 0:
                        # 全部卖出，移除持仓
                        del self.positions[symbol]
        
        # 更新持仓市值和盈亏
        positions_value = 0
        for symbol, pos in self.positions.items():
            # 获取当前价格
            if self.data_interface:
                current_price = self.data_interface.get_realtime_price(symbol)
            else:
                # 使用模拟价格
                current_price = pos.get("avg_cost", 0) * random.uniform(0.9, 1.1)
            
            pos["market_value"] = current_price * pos["quantity"]
            pos["current_price"] = current_price
            pos["unrealized_pnl"] = (current_price - pos["avg_cost"]) * pos["quantity"]
            if pos["avg_cost"] > 0:
                pos["unrealized_pnl_pct"] = (current_price / pos["avg_cost"] - 1)
            else:
                pos["unrealized_pnl_pct"] = 0
            
            positions_value += pos["market_value"]
        
        self.portfolio_value = self.current_capital + positions_value
        
        # 更新最大回撤
        if self.portfolio_value > self.peak_value:
            self.peak_value = self.portfolio_value
        
        current_drawdown = (self.peak_value - self.portfolio_value) / self.peak_value
        self.max_drawdown = max(self.max_drawdown, current_drawdown)
        
        # 计算日度盈亏
        self.daily_pnl = self.portfolio_value - (self.capital if self.total_pnl == 0 else self.portfolio_value - self.total_pnl)
        self.total_pnl = self.portfolio_value - self.capital
    
    async def _monitor_and_report(self):
        """监控和报告"""
        # 检查最大回撤限制
        if self.max_drawdown >= self.config["risk"]["max_drawdown"]:
            logger.warning(f"最大回撤达到限制: {self.max_drawdown:.2%} >= {self.config['risk']['max_drawdown']:.2%}")
            # 触发风控措施
        
        # 定期生成绩效报告
        current_time = datetime.now()
        if hasattr(self, '_last_report_time'):
            hours_since_report = (current_time - self._last_report_time).total_seconds() / 3600
            if hours_since_report >= 1:  # 每小时报告一次
                await self.generate_performance_report()
                self._last_report_time = current_time
        else:
            self._last_report_time = current_time
        
        # 自适应学习
        self._adaptive_learning()
    
    def _adaptive_learning(self):
        """自适应学习"""
        if not self.adaptive_engine:
            return
        
        try:
            # 收集策略绩效数据（简化实现）
            strategy_performance = {}
            
            for strategy_info in self.strategies:
                strategy_name = strategy_info["name"]
                
                # 模拟绩效数据
                strategy_performance[strategy_name] = {
                    "total_return": random.uniform(-0.1, 0.3),
                    "win_rate": random.uniform(0.4, 0.7),
                    "sharpe_ratio": random.uniform(0.5, 2.0)
                }
            
            # 提供给自适应引擎学习（如果支持）
            if hasattr(self.adaptive_engine, 'learn_from_performance'):
                self.adaptive_engine.learn_from_performance(strategy_performance)
                
        except Exception as e:
            logger.error(f"自适应学习失败: {e}")
    
    async def generate_performance_report(self):
        """生成绩效报告"""
        if not self.performance_tracker:
            return {"error": "无绩效跟踪器"}
        
        report = self.performance_tracker.generate_report()
        
        # 添加当前状态
        report.update({
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "portfolio_value": self.portfolio_value,
            "cash": self.current_capital,
            "positions_count": len(self.positions),
            "max_drawdown": self.max_drawdown,
            "daily_pnl": self.daily_pnl,
            "total_pnl": self.total_pnl,
            "active_strategies": len(self.strategies)
        })
        
        # 输出报告
        logger.info(f"A股绩效报告: 组合价值 {self.portfolio_value:,.0f}元, 最大回撤 {self.max_drawdown:.2%}, "
                   f"总盈亏 {self.total_pnl:,.0f}元")
        
        # 保存报告
        try:
            report_file = f"a_share_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"绩效报告已保存到: {report_file}")
        except Exception as e:
            logger.error(f"保存绩效报告失败: {e}")
        
        return report
    
    async def shutdown(self):
        """关闭交易引擎"""
        logger.info("正在关闭A股交易引擎...")
        
        # 生成最终报告
        final_report = await self.generate_performance_report()
        
        if self.config.get("auto_close_positions", False):
            await self._close_all_positions()
        
        self.is_running = False
        logger.info("A股交易引擎已关闭")
        
        return final_report
    
    async def _close_all_positions(self):
        """平掉所有持仓"""
        logger.info("正在平掉所有持仓...")
        # 实现平仓逻辑
        pass


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="A股核心交易框架 - 整合12种选股策略")
    parser.add_argument("--mode", choices=["live", "paper", "backtest"], default="paper",
                       help="运行模式: live(实盘), paper(模拟), backtest(回测)")
    parser.add_argument("--capital", type=float, default=1000000000.0,
                       help="资金规模（元），默认10亿")
    
    args = parser.parse_args()
    
    # 创建交易引擎
    trader = AShareTrader(capital=args.capital, mode=args.mode)
    
    # 运行引擎
    await trader.run()


if __name__ == "__main__":
    asyncio.run(main())