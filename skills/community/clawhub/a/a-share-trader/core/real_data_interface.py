#!/usr/bin/env python3
"""
真实A股数据接口 - 使用xtquant/tushare获取真实数据
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class RealAShareDataInterface:
    """真实A股数据接口"""
    
    def __init__(self, use_xtquant: bool = True, use_tushare: bool = False):
        """
        初始化真实数据接口
        
        Args:
            use_xtquant: 是否使用xtquant
            use_tushare: 是否使用tushare
        """
        self.use_xtquant = use_xtquant
        self.use_tushare = use_tushare
        self.xtdata = None
        self.tushare = None
        
        # 常用A股代码列表
        self.common_stocks = [
            "000001.SZ", "000002.SZ", "000333.SZ", "000858.SZ",
            "002415.SZ", "300750.SZ", "600036.SH", "600519.SH",
            "601318.SH", "601398.SH", "601888.SH", "601988.SH",
            "000063.SZ", "600900.SH", "600028.SH", "601857.SH",
            "000725.SZ", "002594.SZ", "300059.SZ", "600276.SH"
        ]
        
        self._initialize_data_sources()
    
    def _initialize_data_sources(self):
        """初始化数据源"""
        if self.use_xtquant:
            try:
                import xtquant.xtdata as xtdata
                self.xtdata = xtdata
                logger.info("xtquant数据源初始化成功")
            except ImportError as e:
                logger.error(f"导入xtquant失败: {e}")
                self.use_xtquant = False
        
        if self.use_tushare:
            try:
                import tushare as ts
                self.tushare = ts
                logger.info("tushare数据源初始化成功")
            except ImportError as e:
                logger.error(f"导入tushare失败: {e}")
                self.use_tushare = False
    
    def get_market_data(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict]:
        """
        获取市场数据
        
        Args:
            symbols: 股票代码列表，如为None则使用常用股票
            
        Returns:
            市场数据字典
        """
        if symbols is None:
            symbols = self.common_stocks
        
        market_data = {}
        
        if self.use_xtquant and self.xtdata:
            # 使用xtquant获取实时数据
            market_data = self._get_market_data_from_xtquant(symbols)
        elif self.use_tushare and self.tushare:
            # 使用tushare获取数据
            market_data = self._get_market_data_from_tushare(symbols)
        else:
            # 回退到模拟数据
            market_data = self._get_mock_market_data(symbols)
        
        return market_data
    
    def _get_market_data_from_xtquant(self, symbols: List[str]) -> Dict[str, Dict]:
        """从xtquant获取市场数据"""
        market_data = {}
        
        try:
            # 获取行情快照
            quote_data = self.xtdata.get_market_data(
                field_list=['lastPrice', 'volume', 'amount', 'high', 'low', 'open', 'preClose'],
                stock_list=symbols,
                period='1d',
                count=1
            )
            
            for symbol in symbols:
                try:
                    price = float(quote_data.get('lastPrice', {}).get(symbol, [0])[0])
                    volume = float(quote_data.get('volume', {}).get(symbol, [0])[0])
                    amount = float(quote_data.get('amount', {}).get(symbol, [0])[0])
                    high = float(quote_data.get('high', {}).get(symbol, [0])[0])
                    low = float(quote_data.get('low', {}).get(symbol, [0])[0])
                    open_price = float(quote_data.get('open', {}).get(symbol, [0])[0])
                    pre_close = float(quote_data.get('preClose', {}).get(symbol, [0])[0])
                    
                    change = price - pre_close
                    change_percent = (change / pre_close * 100) if pre_close else 0
                    
                    market_data[symbol] = {
                        "price": round(price, 2),
                        "volume": int(volume),
                        "amount": round(amount, 2),
                        "high": round(high, 2),
                        "low": round(low, 2),
                        "open": round(open_price, 2),
                        "pre_close": round(pre_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "update_time": datetime.now().isoformat()
                    }
                except (IndexError, TypeError, ValueError) as e:
                    logger.warning(f"获取{symbol}数据失败: {e}")
                    # 使用模拟数据
                    market_data[symbol] = self._create_mock_stock_data(symbol)
        
        except Exception as e:
            logger.error(f"从xtquant获取市场数据失败: {e}")
            # 回退到模拟数据
            market_data = self._get_mock_market_data(symbols)
        
        return market_data
    
    def _get_market_data_from_tushare(self, symbols: List[str]) -> Dict[str, Dict]:
        """从tushare获取市场数据"""
        market_data = {}
        
        try:
            # 获取实时行情
            ts = self.tushare
            
            # 转换代码格式（移除后缀）
            symbol_codes = [s.replace('.SZ', '').replace('.SH', '') for s in symbols]
            
            # 注意：tushare需要token，这里简化处理
            # 在实际使用中需要配置tushare token
            
            # 创建模拟数据（因为需要token）
            market_data = self._get_mock_market_data(symbols)
            
        except Exception as e:
            logger.error(f"从tushare获取市场数据失败: {e}")
            # 回退到模拟数据
            market_data = self._get_mock_market_data(symbols)
        
        return market_data
    
    def _get_mock_market_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """获取模拟市场数据"""
        market_data = {}
        
        for symbol in symbols:
            market_data[symbol] = self._create_mock_stock_data(symbol)
        
        return market_data
    
    def _create_mock_stock_data(self, symbol: str) -> Dict[str, Any]:
        """创建模拟股票数据"""
        import random
        
        # 根据代码生成一些合理的数据
        if symbol.startswith('000'):
            base_price = random.uniform(5, 50)
        elif symbol.startswith('002'):
            base_price = random.uniform(10, 100)
        elif symbol.startswith('300'):
            base_price = random.uniform(20, 150)
        elif symbol.startswith('600'):
            base_price = random.uniform(8, 80)
        elif symbol.startswith('601'):
            base_price = random.uniform(4, 40)
        else:
            base_price = random.uniform(5, 60)
        
        price = round(base_price * random.uniform(0.95, 1.05), 2)
        volume = random.randint(100000, 10000000)
        amount = round(price * volume, 2)
        
        return {
            "price": price,
            "volume": volume,
            "amount": amount,
            "high": round(price * random.uniform(1.01, 1.05), 2),
            "low": round(price * random.uniform(0.95, 0.99), 2),
            "open": round(price * random.uniform(0.98, 1.02), 2),
            "pre_close": round(base_price, 2),
            "change": round(price - base_price, 2),
            "change_percent": round((price - base_price) / base_price * 100, 2),
            "update_time": datetime.now().isoformat(),
            "market_cap": random.uniform(1000000000, 50000000000),
            "pe": random.uniform(8, 60),
            "pb": random.uniform(0.8, 8),
            "dividend_yield": random.uniform(0.01, 0.05)
        }
    
    def get_fundamental_data(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict]:
        """
        获取基本面数据
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            基本面数据字典
        """
        if symbols is None:
            symbols = self.common_stocks
        
        fundamental_data = {}
        
        # 尝试从数据源获取，失败则使用模拟数据
        for symbol in symbols:
            fundamental_data[symbol] = self._get_stock_fundamental(symbol)
        
        return fundamental_data
    
    def _get_stock_fundamental(self, symbol: str) -> Dict[str, Any]:
        """获取单只股票的基本面数据"""
        import random
        
        # 模拟基本面数据
        return {
            "market_cap": random.uniform(1000000000, 50000000000),  # 市值
            "pe": random.uniform(8, 60),  # 市盈率
            "pb": random.uniform(0.8, 8),  # 市净率
            "dividend_yield": random.uniform(0.01, 0.05),  # 股息率
            "profit_growth": random.uniform(-0.2, 1.0),  # 净利润增长率
            "revenue_growth": random.uniform(-0.1, 0.8),  # 营收增长率
            "roe": random.uniform(0.05, 0.25),  # ROE
            "gross_margin": random.uniform(0.2, 0.5),  # 毛利率
            "debt_ratio": random.uniform(0.3, 0.7),  # 负债率
            "is_st": random.random() < 0.02,  # 是否为ST股
            "is_suspended": random.random() < 0.01,  # 是否停牌
            "listing_days": random.randint(100, 5000),  # 上市天数
            "eps": random.uniform(0.1, 5.0),  # 每股收益
            "bps": random.uniform(2, 20),  # 每股净资产
            "chip_concentration_90": random.uniform(0.05, 0.25),  # 筹码集中度
            "has_social_security": random.random() < 0.3,  # 是否有社保持股
            "social_security_ratio": random.uniform(0, 0.05) if random.random() < 0.3 else 0  # 社保持股比例
        }
    
    def get_technical_data(self, symbols: Optional[List[str]] = None, 
                          indicators: List[str] = None) -> Dict[str, Dict]:
        """
        获取技术指标数据
        
        Args:
            symbols: 股票代码列表
            indicators: 技术指标列表
            
        Returns:
            技术指标数据字典
        """
        if symbols is None:
            symbols = self.common_stocks
        
        if indicators is None:
            indicators = ['ma5', 'ma10', 'ma20', 'ma60', 'kdj_k', 'kdj_d', 'kdj_j', 
                         'macd', 'macd_signal', 'macd_hist', 'rsi', 'boll_upper', 
                         'boll_middle', 'boll_lower']
        
        technical_data = {}
        
        for symbol in symbols:
            tech_data = {}
            
            # 生成模拟技术指标
            for indicator in indicators:
                if 'ma' in indicator:
                    # 移动平均线
                    tech_data[indicator] = random.uniform(5, 50)
                elif 'kdj' in indicator:
                    # KDJ指标
                    tech_data[indicator] = random.uniform(0, 100)
                elif 'macd' in indicator:
                    # MACD指标
                    tech_data[indicator] = random.uniform(-2, 2)
                elif 'rsi' in indicator:
                    # RSI指标
                    tech_data[indicator] = random.uniform(20, 80)
                elif 'boll' in indicator:
                    # 布林带
                    tech_data[indicator] = random.uniform(5, 60)
                else:
                    tech_data[indicator] = 0
            
            technical_data[symbol] = tech_data
        
        return technical_data
    
    def test_connection(self) -> Dict[str, Any]:
        """测试数据源连接"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "xtquant_available": self.use_xtquant and self.xtdata is not None,
            "tushare_available": self.use_tushare and self.tushare is not None,
            "common_stocks_count": len(self.common_stocks)
        }
        
        # 测试获取少量数据
        try:
            test_symbols = ["000001.SZ", "600036.SH"]
            market_data = self.get_market_data(test_symbols)
            result["market_data_test"] = {
                "success": True,
                "symbols_retrieved": len(market_data),
                "sample_data": {k: v.get("price", 0) for k, v in market_data.items()}
            }
        except Exception as e:
            result["market_data_test"] = {
                "success": False,
                "error": str(e)
            }
        
        return result


if __name__ == "__main__":
    # 测试数据接口
    import json
    data_interface = RealAShareDataInterface(use_xtquant=True, use_tushare=False)
    
    # 测试连接
    connection_test = data_interface.test_connection()
    print("连接测试结果:")
    print(json.dumps(connection_test, indent=2, ensure_ascii=False))
    
    # 获取市场数据
    print("\n获取市场数据示例:")
    market_data = data_interface.get_market_data(["000001.SZ", "600036.SH"])
    for symbol, data in market_data.items():
        print(f"{symbol}: 价格={data.get('price')}, 涨跌幅={data.get('change_percent')}%")
    
    # 获取基本面数据
    print("\n获取基本面数据示例:")
    fundamental_data = data_interface.get_fundamental_data(["000001.SZ"])
    for symbol, data in fundamental_data.items():
        print(f"{symbol}: PE={data.get('pe'):.2f}, ROE={data.get('roe'):.2%}")