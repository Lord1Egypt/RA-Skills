"""
万能反爬 Skill - 统一数据模型
所有平台采集的车辆数据统一为此格式，方便 OpenClaw 导入
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import json


@dataclass
class VehicleInfo:
    """统一车辆信息模型"""

    # ─── 基本信息 ──────────────
    source: str = ""          # 来源平台：dasouche / dongchedi / autohome
    source_id: str = ""       # 来源平台的车辆ID
    source_url: str = ""      # 来源详情页URL
    scraped_at: str = ""      # 采集时间

    # ─── 车辆信息 ──────────────
    title: str = ""           # 标题
    brand: str = ""           # 品牌
    series: str = ""          # 车系
    model: str = ""           # 车型（具体配置名）
    year: int = 0             # 年款
    mileage: str = ""         # 里程（带单位）
    mileage_km: float = 0.0  # 里程（公里数）
    color: str = ""           # 颜色
    plate_city: str = ""      # 上牌城市
    plate_date: str = ""      # 上牌日期
    vin: str = ""             # VIN码

    # ─── 价格信息 ──────────────
    price: float = 0.0        # 售价（万元）
    original_price: float = 0.0  # 新车指导价（万元）
    price_currency: str = "CNY"

    # ─── 技术参数 ──────────────
    fuel_type: str = ""       # 燃油类型：汽油/柴油/纯电/混动
    engine: str = ""          # 发动机
    transmission: str = ""    # 变速箱
    drive_type: str = ""      # 驱动方式
    body_type: str = ""       # 车身类型：轿车/SUV/MPV等
    displacement: str = ""    # 排量
    seats: int = 0            # 座位数
    doors: int = 0            # 车门数
    emission_standard: str = ""  # 排放标准

    # ─── 电动车参数 ─────────────
    battery_capacity: str = ""   # 电池容量
    range_km: float = 0.0       # 续航里程
    motor_power: str = ""       # 电机功率

    # ─── 图片和媒体 ─────────────
    images: list[str] = field(default_factory=list)       # 图片URL列表
    thumbnail: str = ""         # 缩略图URL

    # ─── 商家/经销商 ────────────
    dealer_name: str = ""       # 商家名称
    dealer_phone: str = ""      # 商家电话
    dealer_city: str = ""       # 商家城市
    dealer_address: str = ""    # 商家地址

    # ─── 车况描述 ──────────────
    condition_tags: list[str] = field(default_factory=list)  # 车况标签
    highlights: str = ""        # 卖点/亮点
    description: str = ""       # 详细描述

    def to_dict(self) -> dict:
        """转为字典"""
        return {k: v for k, v in self.__dict__.items() if v or v == 0}

    def to_json(self) -> str:
        """转为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "VehicleInfo":
        """从字典创建"""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


@dataclass
class ScrapeResult:
    """单次采集结果"""
    success: bool = True
    vehicles: list[VehicleInfo] = field(default_factory=list)
    total_found: int = 0
    pages_scraped: int = 0
    errors: list[str] = field(default_factory=list)
    source: str = ""
    started_at: str = ""
    finished_at: str = ""

    def summary(self) -> str:
        return (
            f"[{self.source}] 采集完成: "
            f"共{self.total_found}条, 成功{len(self.vehicles)}条, "
            f"翻页{self.pages_scraped}页, 错误{len(self.errors)}条"
        )
