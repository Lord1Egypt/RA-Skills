# -*- coding: utf-8 -*-
"""
===================================
多数据源管理器 - V2.2
===================================

设计参考: daily_stock_analysis的DataFetcherManager

核心功能:
1. 主数据源: AKShare
2. 备用数据源: Efinance（可选）
3. 自动故障切换
4. 熔断机制
5. 数据质量校验
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============================================
# 异常定义
# ============================================

class DataFetchError(Exception):
    """数据获取异常基类"""
    pass


class DataSourceUnavailableError(DataFetchError):
    """数据源不可用异常"""
    pass


# ============================================
# 熔断器
# ============================================

class CircuitBreaker:
    """
    熔断器 - 管理数据源的熔断/冷却状态

    策略：
    - 连续失败 N 次后进入熔断状态
    - 熔断期间跳过该数据源
    - 冷却时间后自动恢复
    """

    CLOSED = "closed"      # 正常状态
    OPEN = "open"          # 熔断状态
    HALF_OPEN = "half_open"  # 半开状态

    def __init__(
        self,
        failure_threshold: int = 3,
        cooldown_seconds: float = 300.0,
    ):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self._states: Dict[str, Dict[str, Any]] = {}

    def _get_state(self, source: str) -> Dict[str, Any]:
        """获取或初始化数据源状态"""
        if source not in self._states:
            self._states[source] = {
                'state': self.CLOSED,
                'failures': 0,
                'last_failure_time': 0.0,
            }
        return self._states[source]

    def is_available(self, source: str) -> bool:
        """检查数据源是否可用"""
        state = self._get_state(source)
        current_time = time.time()

        if state['state'] == self.CLOSED:
            return True

        if state['state'] == self.OPEN:
            # 检查冷却时间
            time_since_failure = current_time - state['last_failure_time']
            if time_since_failure >= self.cooldown_seconds:
                state['state'] = self.HALF_OPEN
                logger.info(f"[熔断器] {source} 冷却完成，进入半开状态")
                return True
            else:
                return False

        if state['state'] == self.HALF_OPEN:
            return True

        return True

    def record_success(self, source: str) -> None:
        """记录成功请求"""
        state = self._get_state(source)
        state['state'] = self.CLOSED
        state['failures'] = 0

    def record_failure(self, source: str, error: Optional[str] = None) -> None:
        """记录失败请求"""
        state = self._get_state(source)
        current_time = time.time()

        state['failures'] += 1
        state['last_failure_time'] = current_time

        if state['failures'] >= self.failure_threshold:
            state['state'] = self.OPEN
            logger.warning(f"[熔断器] {source} 连续失败 {state['failures']} 次，进入熔断状态 "
                          f"(冷却 {self.cooldown_seconds}s)")
            if error:
                logger.warning(f"[熔断器] 最后错误: {error}")


# ============================================
# 实时行情数据结构
# ============================================

@dataclass
class RealtimeQuote:
    """统一实时行情数据结构"""
    code: str
    name: str = ""
    price: Optional[float] = None
    volume_ratio: Optional[float] = None      # 量比
    turnover_rate: Optional[float] = None     # 换手率(%)
    volume: Optional[int] = None              # 成交量（手）
    amount: Optional[float] = None            # 成交额
    change_pct: Optional[float] = None        # 涨跌幅(%)
    source: str = "unknown"

    def has_volume_data(self) -> bool:
        """检查是否有量价数据"""
        return self.volume_ratio is not None or self.turnover_rate is not None


# ============================================
# 筹码分布数据结构
# ============================================

@dataclass
class ChipDistribution:
    """筹码分布数据"""
    code: str
    date: str = ""
    profit_ratio: float = 0.0              # 获利盘比例(0-1)
    avg_cost: float = 0.0                  # 平均成本
    concentration_90: float = 0.0          # 90%筹码集中度
    concentration_70: float = 0.0          # 70%筹码集中度


# ============================================
# 数据源抽象基类
# ============================================

class BaseFetcher(ABC):
    """数据源抽象基类"""

    name: str = "BaseFetcher"
    priority: int = 99

    @abstractmethod
    def get_daily_data(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """获取日线数据"""
        pass

    @abstractmethod
    def get_realtime_quote(self, stock_code: str) -> Optional[RealtimeQuote]:
        """获取实时行情"""
        pass

    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化DataFrame列名"""
        # 标准列名
        column_map = {
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'amount': 'amount',
            'pct_chg': 'pct_chg',
        }

        # 重命名列
        df = df.rename(columns=column_map)

        # 确保必需列存在
        required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"缺少必需列: {col}")

        return df


# ============================================
# AKShare数据源
# ============================================

class AkshareFetcher(BaseFetcher):
    """AKShare数据源适配器"""

    name = "Akshare"
    priority = 1

    def get_daily_data(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """获取日线数据"""
        try:
            import akshare as ak

            # akshare获取股票历史数据
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                adjust="qfq"  # 前复权
            )

            if df is None or df.empty:
                raise DataFetchError(f"AKShare未获取到{stock_code}的数据")

            # 标准化列名
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume',
                '成交额': 'amount',
                '涨跌幅': 'pct_chg',
            })

            # 确保日期格式
            df['date'] = pd.to_datetime(df['date'])

            return self.normalize_dataframe(df)

        except ImportError:
            raise DataFetchError("AKShare库未安装，请执行: pip install akshare")
        except Exception as e:
            raise DataFetchError(f"AKShare获取失败: {str(e)}")

    def get_realtime_quote(self, stock_code: str) -> Optional[RealtimeQuote]:
        """获取实时行情"""
        try:
            import akshare as ak

            # 获取实时行情
            df = ak.stock_zh_a_spot_em()

            # 查找目标股票
            row = df[df['代码'] == stock_code]

            if row.empty:
                logger.warning(f"AKShare未找到{stock_code}的实时行情")
                return None

            row = row.iloc[0]

            return RealtimeQuote(
                code=stock_code,
                name=row.get('名称', ''),
                price=row.get('最新价', 0),
                volume_ratio=row.get('量比', 0),
                turnover_rate=row.get('换手率', 0),
                volume=row.get('成交量', 0),
                amount=row.get('成交额', 0),
                change_pct=row.get('涨跌幅', 0),
                source="akshare"
            )

        except Exception as e:
            logger.warning(f"AKShare获取实时行情失败: {str(e)}")
            return None


# ============================================
# Efinance数据源（可选）
# ============================================

class EfinanceFetcher(BaseFetcher):
    """Efinance数据源适配器"""

    name = "Efinance"
    priority = 0  # 最高优先级

    def get_daily_data(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """获取日线数据"""
        try:
            import efinance as ef

            # efinance获取股票历史数据
            df = ef.stock.get_quote_history(
                stock_code,
                beg=start_date,
                end=end_date
            )

            if df is None or df.empty:
                raise DataFetchError(f"Efinance未获取到{stock_code}的数据")

            # 标准化列名
            df = df.rename(columns={
                '行情日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low',
                '收盘': 'close',
                '成交量': 'volume',
                '成交额': 'amount',
                '涨跌幅': 'pct_chg',
            })

            # 确保日期格式
            df['date'] = pd.to_datetime(df['date'])

            return self.normalize_dataframe(df)

        except ImportError:
            raise DataFetchError("Efinance库未安装，请执行: pip install efinance")
        except Exception as e:
            raise DataFetchError(f"Efinance获取失败: {str(e)}")

    def get_realtime_quote(self, stock_code: str) -> Optional[RealtimeQuote]:
        """获取实时行情"""
        try:
            import efinance as ef

            # 获取实时行情
            df = ef.stock.get_realtime_quotes()

            # 查找目标股票
            row = df[df['股票代码'] == stock_code]

            if row.empty:
                logger.warning(f"Efinance未找到{stock_code}的实时行情")
                return None

            row = row.iloc[0]

            return RealtimeQuote(
                code=stock_code,
                name=row.get('股票名称', ''),
                price=row.get('最新价', 0),
                volume_ratio=row.get('量比', 0),
                turnover_rate=row.get('换手率', 0),
                volume=row.get('成交量', 0),
                amount=row.get('成交额', 0),
                change_pct=row.get('涨跌幅', 0),
                source="efinance"
            )

        except Exception as e:
            logger.warning(f"Efinance获取实时行情失败: {str(e)}")
            return None


# ============================================
# 多数据源管理器
# ============================================

class DataFetcherManager:
    """
    多数据源管理器

    功能：
    1. 管理多个数据源
    2. 自动故障切换
    3. 熔断机制
    4. 数据质量校验
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化管理器

        Args:
            config: 配置字典，如:
                {
                    'primary': 'akshare',
                    'fallback': ['efinance'],
                    'circuit_breaker': {
                        'failure_threshold': 3,
                        'cooldown_seconds': 300
                    }
                }
        """
        self.config = config or {}

        # 初始化熔断器
        cb_config = self.config.get('circuit_breaker', {})
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=cb_config.get('failure_threshold', 3),
            cooldown_seconds=cb_config.get('cooldown_seconds', 300),
        )

        # 初始化数据源
        self.fetchers = self._init_fetchers()

        logger.info(f"数据管理器初始化完成，数据源数量: {len(self.fetchers)}")

    def _init_fetchers(self) -> List[BaseFetcher]:
        """初始化数据源列表"""
        fetchers = []

        # 添加AKShare（默认总是启用）
        fetchers.append(AkshareFetcher())

        # 尝试添加Efinance（可选）
        try:
            import efinance
            fetchers.append(EfinanceFetcher())
            logger.info("Efinance数据源已启用")
        except ImportError:
            logger.info("Efinance未安装，仅使用AKShare")

        # 按优先级排序
        fetchers.sort(key=lambda x: x.priority)

        return fetchers

    def get_daily_data(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: int = 30,
    ) -> pd.DataFrame:
        """
        获取日线数据（自动故障切换）

        Args:
            stock_code: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            days: 获取天数（当start_date未指定时使用）

        Returns:
            标准化的DataFrame
        """
        # 计算日期范围
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        if start_date is None:
            start_dt = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days * 2)
            start_date = start_dt.strftime('%Y-%m-%d')

        # 遍历数据源
        for fetcher in self.fetchers:
            # 检查熔断器
            if not self.circuit_breaker.is_available(fetcher.name):
                logger.debug(f"{fetcher.name} 处于熔断状态，跳过")
                continue

            try:
                logger.info(f"尝试使用 {fetcher.name} 获取 {stock_code} 数据...")
                df = fetcher.get_daily_data(stock_code, start_date, end_date)

                # 数据质量校验
                if not self._validate_data(df):
                    raise ValueError("数据质量校验失败")

                # 成功获取
                self.circuit_breaker.record_success(fetcher.name)
                logger.info(f"{fetcher.name} 获取成功，数据量: {len(df)}")
                return df

            except Exception as e:
                # 失败，记录并尝试下一个
                self.circuit_breaker.record_failure(fetcher.name, str(e))
                logger.warning(f"{fetcher.name} 获取失败: {str(e)}，尝试下一个数据源")

        # 所有数据源均失败
        raise DataSourceUnavailableError(
            f"所有数据源均无法获取 {stock_code} 的数据"
        )

    def get_realtime_quote(self, stock_code: str) -> Optional[RealtimeQuote]:
        """
        获取实时行情（自动故障切换）

        Args:
            stock_code: 股票代码

        Returns:
            RealtimeQuote对象，失败返回None
        """
        for fetcher in self.fetchers:
            if not self.circuit_breaker.is_available(fetcher.name):
                continue

            try:
                quote = fetcher.get_realtime_quote(stock_code)
                if quote and quote.has_volume_data():
                    self.circuit_breaker.record_success(fetcher.name)
                    return quote
            except Exception as e:
                self.circuit_breaker.record_failure(fetcher.name, str(e))
                logger.warning(f"{fetcher.name} 获取实时行情失败: {str(e)}")

        return None

    def _validate_data(self, df: pd.DataFrame) -> bool:
        """
        数据质量校验

        检查：
        1. 不为空
        2. 日期升序
        3. 必需列存在
        4. 无异常值
        """
        if df is None or df.empty:
            logger.error("数据为空")
            return False

        # 检查必需列
        required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                logger.error(f"缺少列: {col}")
                return False

        # 检查异常值
        if (df['close'] <= 0).any():
            logger.error("收盘价存在异常值（<=0）")
            return False

        if (df['volume'] < 0).any():
            logger.error("成交量存在负值")
            return False

        return True


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 测试数据管理器
    print("=" * 60)
    print("测试多数据源管理器")
    print("=" * 60)

    # 初始化管理器
    manager = DataFetcherManager()

    # 测试获取日线数据
    print("\n1. 测试获取日线数据...")
    try:
        df = manager.get_daily_data("600519", days=30)
        print(f"✓ 成功获取数据: {len(df)}条")
        print(df.head())
    except Exception as e:
        print(f"✗ 获取失败: {e}")

    # 测试获取实时行情
    print("\n2. 测试获取实时行情...")
    quote = manager.get_realtime_quote("600519")
    if quote:
        print(f"✓ 成功获取实时行情:")
        print(f"  股票: {quote.name}({quote.code})")
        print(f"  价格: {quote.price}")
        print(f"  量比: {quote.volume_ratio}")
        print(f"  换手率: {quote.turnover_rate}%")
    else:
        print("✗ 获取实时行情失败")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
