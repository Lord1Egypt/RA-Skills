from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Car:
    """Unified used car data model across all platforms."""

    id: str
    platform: str  # dongchedi, guazi, renren
    title: str  # e.g. "2020款 宝马3系 325Li M运动套装"
    price: float  # 万元
    brand: str = ""  # e.g. "宝马"
    series: str = ""  # e.g. "3系"
    model_year: str = ""  # e.g. "2020款"
    mileage: float = 0.0  # 万公里
    first_reg_date: str = ""  # 首次上牌日期
    transmission: str = ""  # 自动/手动
    displacement: str = ""  # e.g. "2.0T"
    city: str = ""
    color: str = ""
    url: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class CarDetail(Car):
    """Extended car detail with additional info."""

    description: str = ""
    emission_standard: str = ""  # e.g. "国六"
    engine_power: str = ""  # e.g. "184马力"
    fuel_type: str = ""  # 汽油/柴油/纯电/混动
    body_type: str = ""  # 轿车/SUV/MPV
    drive_type: str = ""  # 前驱/后驱/四驱
    seats: Optional[int] = None
    license_plate: str = ""  # 车牌所在地
    transfer_count: str = ""  # 过户次数
    annual_inspection: str = ""  # 年检到期
    insurance_expiry: str = ""  # 保险到期
    images: list[str] = field(default_factory=list)
    price_history: list[dict] = field(default_factory=list)
