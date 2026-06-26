"""
A股数据接口
为A股核心交易框架提供数据支持
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class AShareDataInterface:
    """A股数据接口类"""
    
    def __init__(self, real_time: bool = True, update_frequency: float = 1.0,
                 data_sources: List[str] = None):
        """
        初始化A股数据接口
        
        Args:
            real_time: 是否使用实时数据
            update_frequency: 数据更新频率（秒）
            data_sources: 数据源列表
        """
        self.real_time = real_time
        self.update_frequency = update_frequency
        self.data_sources = data_sources or ["xtquant", "tushare", "baostock"]
        
        # A股股票池（示例）
        self.a_share_stocks = [
            # 大盘蓝筹
            "000001.SZ",  # 平安银行
            "000002.SZ",  # 万科A
            "000333.SZ",  # 美的集团
            "000858.SZ",  # 五粮液
            "002415.SZ",  # 海康威视
            # 成长股
            "300750.SZ",  # 宁德时代
            "300059.SZ",  # 东方财富
            "300124.SZ",  # 汇川技术
            # 上证主板
            "600036.SH",  # 招商银行
            "600519.SH",  # 贵州茅台
            "601318.SH",  # 中国平安
            "601888.SH",  # 中国中免
            # 科创板
            "688981.SH",  # 中芯国际
            "688111.SH",  # 金山办公
            # 中小板
            "002475.SZ",  # 立讯精密
            "002594.SZ",  # 比亚迪
            # 高股息
            "601328.SH",  # 交通银行
            "601398.SH",  # 工商银行
            "601988.SH",  # 中国银行
        ]
        
        # 价格缓存
        self.price_cache = {}
        
        # 基本面数据模板
        self.fundamental_templates = self._create_fundamental_templates()
        
        logger.info(f"A股数据接口初始化完成，股票池: {len(self.a_share_stocks)}只股票")
    
    def _create_fundamental_templates(self) -> Dict[str, Dict]:
        """创建基本面数据模板"""
        templates = {}
        
        # 为每只股票创建基本面模板
        for symbol in self.a_share_stocks:
            # 根据股票类型设置不同的基本面特征
            if "688" in symbol:  # 科创板
                templates[symbol] = {
                    "market_cap": random.uniform(50000000000, 500000000000),
                    "profit_growth": random.uniform(0.20, 0.60),  # 高增长
                    "revenue_growth": random.uniform(0.15, 0.50),
                    "roe": random.uniform(0.10, 0.25),
                    "gross_margin": random.uniform(0.30, 0.70),  # 高毛利
                    "pe": random.uniform(30.0, 80.0),  # 高估值
                    "pb": random.uniform(3.0, 12.0),
                    "dividend_yield": random.uniform(0.0, 0.02),  # 低股息
                    "debt_ratio": random.uniform(0.2, 0.5),
                    "sector": "科技",
                    "is_st": False,
                    "is_suspended": False,
                    "is_star": True,  # 科创板
                    "listing_days": random.randint(200, 1000)
                }
            elif "300" in symbol:  # 创业板
                templates[symbol] = {
                    "market_cap": random.uniform(20000000000, 300000000000),
                    "profit_growth": random.uniform(0.15, 0.50),
                    "revenue_growth": random.uniform(0.10, 0.40),
                    "roe": random.uniform(0.08, 0.20),
                    "gross_margin": random.uniform(0.25, 0.60),
                    "pe": random.uniform(20.0, 60.0),
                    "pb": random.uniform(2.0, 8.0),
                    "dividend_yield": random.uniform(0.0, 0.03),
                    "debt_ratio": random.uniform(0.25, 0.55),
                    "sector": random.choice(["科技", "医药", "新能源"]),
                    "is_st": random.random() < 0.02,
                    "is_suspended": random.random() < 0.01,
                    "is_star": False,
                    "listing_days": random.randint(500, 3000)
                }
            elif "601" in symbol or "600" in symbol:  # 上证主板
                templates[symbol] = {
                    "market_cap": random.uniform(100000000000, 1000000000000),
                    "profit_growth": random.uniform(0.05, 0.25),
                    "revenue_growth": random.uniform(0.03, 0.20),
                    "roe": random.uniform(0.10, 0.20),
                    "gross_margin": random.uniform(0.20, 0.50),
                    "pe": random.uniform(5.0, 25.0),
                    "pb": random.uniform(0.8, 3.0),
                    "dividend_yield": random.uniform(0.02, 0.08),  # 较高股息
                    "debt_ratio": random.uniform(0.4, 0.8),
                    "sector": random.choice(["金融", "消费", "能源", "制造"]),
                    "is_st": random.random() < 0.01,
                    "is_suspended": random.random() < 0.005,
                    "is_star": False,
                    "listing_days": random.randint(1000, 5000)
                }
            else:  # 深证主板/中小板
                templates[symbol] = {
                    "market_cap": random.uniform(5000000000, 200000000000),
                    "profit_growth": random.uniform(0.08, 0.35),
                    "revenue_growth": random.uniform(0.05, 0.30),
                    "roe": random.uniform(0.08, 0.22),
                    "gross_margin": random.uniform(0.20, 0.55),
                    "pe": random.uniform(10.0, 40.0),
                    "pb": random.uniform(1.0, 5.0),
                    "dividend_yield": random.uniform(0.01, 0.05),
                    "debt_ratio": random.uniform(0.3, 0.65),
                    "sector": random.choice(["制造", "消费", "医药", "科技"]),
                    "is_st": random.random() < 0.03,
                    "is_suspended": random.random() < 0.01,
                    "is_star": False,
                    "listing_days": random.randint(800, 4000)
                }
        
        return templates
    
    def get_market_data(self, symbol: str) -> Dict:
        """
        获取市场数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            市场数据字典
        """
        price = self.get_realtime_price(symbol)
        
        return {
            "symbol": symbol,
            "price": price,
            "volume": random.randint(100000, 10000000),
            "bid": price * 0.999,
            "ask": price * 1.001,
            "market_cap": self._get_market_cap(symbol),
            "timestamp": datetime.now()
        }
    
    def get_realtime_price(self, symbol: str) -> float:
        """
        获取实时价格
        
        Args:
            symbol: 股票代码
        
        Returns:
            实时价格
        """
        if symbol in self.price_cache:
            # 添加随机波动
            old_price = self.price_cache[symbol]
            # A股涨跌停限制：±10%（ST股±5%）
            is_st = self.fundamental_templates.get(symbol, {}).get("is_st", False)
            max_change = 0.05 if is_st else 0.10
            change = random.uniform(-max_change, max_change)
            new_price = old_price * (1 + change)
        else:
            # 初始价格（基于股票类型）
            if "688" in symbol:  # 科创板
                new_price = random.uniform(30.0, 200.0)
            elif "300" in symbol:  # 创业板
                new_price = random.uniform(15.0, 100.0)
            elif "601" in symbol or "600" in symbol:  # 上证主板
                new_price = random.uniform(5.0, 80.0)
            else:  # 深证主板/中小板
                new_price = random.uniform(8.0, 60.0)
        
        # A股价格精度：0.01元
        new_price = round(new_price, 2)
        
        # 确保价格为正
        new_price = max(0.01, new_price)
        
        self.price_cache[symbol] = new_price
        return new_price
    
    def _get_market_cap(self, symbol: str) -> float:
        """获取市值"""
        if symbol in self.fundamental_templates:
            return self.fundamental_templates[symbol].get("market_cap", 0)
        return random.uniform(5000000000, 500000000000)
    
    def get_fundamental_data(self, symbol: str) -> Dict:
        """
        获取基本面数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            基本面数据字典
        """
        template = self.fundamental_templates.get(symbol, {})
        if not template:
            # 生成随机基本面数据
            return self._generate_random_fundamental(symbol)
        
        # 在模板基础上添加一些随机波动
        fundamental = template.copy()
        
        # 添加随机波动（模拟数据更新）
        for key in ["profit_growth", "revenue_growth", "roe", "gross_margin", 
                  "dividend_yield", "pe", "pb", "debt_ratio"]:
            if key in fundamental:
                fundamental[key] *= (1 + random.uniform(-0.05, 0.05))
        
        # 确保数据在合理范围内
        if "pe" in fundamental:
            fundamental["pe"] = max(0.1, fundamental["pe"])
        
        if "pb" in fundamental:
            fundamental["pb"] = max(0.1, fundamental["pb"])
        
        if "dividend_yield" in fundamental:
            fundamental["dividend_yield"] = max(0.0, fundamental["dividend_yield"])
        
        return fundamental
    
    def _generate_random_fundamental(self, symbol: str) -> Dict:
        """生成随机基本面数据"""
        return {
            "market_cap": random.uniform(5000000000, 500000000000),
            "profit_growth": random.uniform(-0.2, 0.5),
            "revenue_growth": random.uniform(-0.1, 0.4),
            "roe": random.uniform(0.05, 0.30),
            "gross_margin": random.uniform(0.20, 0.60),
            "pe": random.uniform(5.0, 60.0),
            "pb": random.uniform(0.5, 8.0),
            "dividend_yield": random.uniform(0.0, 0.08),
            "debt_ratio": random.uniform(0.2, 0.7),
            "sector": random.choice(["金融", "消费", "医药", "科技", "制造", "能源"]),
            "is_st": random.random() < 0.03,
            "is_suspended": random.random() < 0.01,
            "is_star": "688" in symbol,
            "listing_days": random.randint(100, 5000)
        }
    
    def get_technical_data(self, symbol: str, period: str = "daily") -> Dict:
        """
        获取技术指标数据
        
        Args:
            symbol: 股票代码
            period: 周期（daily, weekly, monthly）
        
        Returns:
            技术指标数据字典
        """
        # 生成随机技术指标（模拟）
        return {
            "kdj_k": random.uniform(0, 100),
            "kdj_d": random.uniform(0, 100),
            "kdj_j": random.uniform(0, 100),
            "rsi": random.uniform(0, 100),
            "macd": random.uniform(-2, 2),
            "macd_signal": random.uniform(-2, 2),
            "macd_hist": random.uniform(-1, 1),
            "boll_upper": random.uniform(10, 50),
            "boll_middle": random.uniform(10, 50),
            "boll_lower": random.uniform(10, 50),
            "volume_ma5": random.randint(100000, 1000000),
            "volume_ma10": random.randint(100000, 1000000),
            "price_ma5": random.uniform(10, 50),
            "price_ma10": random.uniform(10, 50),
            "price_ma20": random.uniform(10, 50),
            "price_ma60": random.uniform(10, 50),
            "price_ma250": random.uniform(10, 50),
            "period": period,
            "timestamp": datetime.now()
        }
    
    def get_stock_list(self, filter_criteria: Dict = None) -> List[str]:
        """
        获取股票列表（可筛选）
        
        Args:
            filter_criteria: 筛选条件
        
        Returns:
            股票代码列表
        """
        if not filter_criteria:
            return self.a_share_stocks.copy()
        
        filtered = []
        for symbol in self.a_share_stocks:
            # 获取基本面数据
            fund_data = self.get_fundamental_data(symbol)
            
            passed = True
            
            # 应用筛选条件
            for key, (min_val, max_val) in filter_criteria.items():
                if key in fund_data:
                    value = fund_data[key]
                    
                    if min_val is not None and value < min_val:
                        passed = False
                        break
                    
                    if max_val is not None and value > max_val:
                        passed = False
                        break
            
            if passed:
                filtered.append(symbol)
        
        return filtered
    
    def get_batch_data(self, symbols: List[str], data_type: str = "market") -> Dict[str, Dict]:
        """
        批量获取数据
        
        Args:
            symbols: 股票代码列表
            data_type: 数据类型（market, fundamental, technical）
        
        Returns:
            数据字典 {symbol: data}
        """
        result = {}
        
        for symbol in symbols:
            try:
                if data_type == "market":
                    result[symbol] = self.get_market_data(symbol)
                elif data_type == "fundamental":
                    result[symbol] = self.get_fundamental_data(symbol)
                elif data_type == "technical":
                    result[symbol] = self.get_technical_data(symbol)
            except Exception as e:
                logger.error(f"获取{symbol}的{data_type}数据失败: {e}")
        
        return result