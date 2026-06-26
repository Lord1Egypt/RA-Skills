"""
金甲龙虾 (AegisClaw) 配置文件
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

# 加载 .env 文件
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

@dataclass
class BinanceConfig:
    """币安 API 配置"""
    api_key: str = os.getenv("BINANCE_API_KEY", "")
    api_secret: str = os.getenv("BINANCE_API_SECRET", "")
    testnet: bool = False
    # 安全配置
    max_daily_trades: int = 10
    max_price_slippage: float = 0.01  # 1%
    allowed_ip_whitelist: List[str] = field(default_factory=list)
    # 禁用的危险权限
    forbidden_permissions: List[str] = field(default_factory=lambda: ["ENABLE_WITHDRAWALS", "PERMIT_UNIVERSAL_TRANSFER"])

@dataclass
class StrategyConfig:
    """策略配置"""
    # 资金费率套利阈值
    funding_rate_threshold: float = 0.0001  # 0.01%
    min_arbitrage_profit: float = 0.001  # 0.1%
    # Launchpool 最小参与金额
    min_launchpool_amount: float = 10.0  # USDT
    # Dust Sweeper 最小兑换阈值
    min_dust_threshold: float = 10.0  # USDT 等值

@dataclass
class DatabaseConfig:
    """数据库配置"""
    path: str = "db/aegisclaw.db"

@dataclass
class TelegramConfig:
    """Telegram 配置"""
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

class Config:
    """主配置类"""
    binance = BinanceConfig()
    strategy = StrategyConfig()
    database = DatabaseConfig()
    telegram = TelegramConfig()

    @classmethod
    def validate(cls) -> bool:
        """验证必要配置"""
        if not cls.binance.api_key or not cls.binance.api_secret:
            return False
        return True

# 默认配置
config = Config()
