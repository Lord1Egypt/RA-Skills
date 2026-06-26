import time

from pydantic import BaseModel, Field


class MarketDataModel(BaseModel):
    last_price: float = Field(..., gt=0, description="最新成交价")
    volume_24h: float = Field(default=0.0, ge=0)
    timestamp: float = Field(default_factory=time.time)


class IntelligenceModel(BaseModel):
    author: str = Field(..., description="研报生成者ID")
    content: str = Field(..., description="研报正文内容")
    ttl_seconds: int = Field(default=1800, description="数据有效时长(秒)，默认30分钟")
    created_at: float = Field(default_factory=time.time)


class RiskAuditModel(BaseModel):
    global_lock: bool = Field(default=False, description="是否触发全局爆仓保护")
    max_position_allowance: float = Field(..., ge=0, description="当前允许的最大下单量")
    current_drawdown: float = Field(default=0.0, description="当前账户回撤比例")
