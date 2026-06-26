from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SearchFilter:
    """Unified search filter for used car searches across all platforms."""

    city: str = "北京"
    brand: str = ""
    series: str = ""
    min_price: Optional[float] = None  # 万元
    max_price: Optional[float] = None
    min_mileage: Optional[float] = None  # 万公里
    max_mileage: Optional[float] = None
    min_year: Optional[int] = None  # e.g. 2020
    max_year: Optional[int] = None
    transmission: str = ""  # auto / manual
    fuel_type: str = ""  # gasoline / diesel / electric / hybrid
    body_type: str = ""  # sedan / suv / mpv
    sort_by: str = "default"  # default, price_asc, price_desc, mileage, date
    page: int = 1
    page_size: int = 20
    keywords: str = ""
    tags: list[str] = field(default_factory=list)
