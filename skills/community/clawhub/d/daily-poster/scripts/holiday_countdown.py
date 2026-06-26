"""Shared holiday countdown helpers for dynamic poster rendering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Iterable

OFFICIAL_SOURCE = {
    "title": "国务院办公厅关于2026年部分节假日安排的通知",
    "document_number": "国办发明电〔2025〕7号",
    "published_date": "2025-11-04",
    "url": "https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html",
}


@dataclass(frozen=True)
class Holiday:
    name: str
    start: date
    end: date
    days_off: int
    makeup_workdays: tuple[date, ...] = ()

    def to_schedule_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "start_date": self.start.isoformat(),
            "end_date": self.end.isoformat(),
            "days_off": self.days_off,
            "makeup_workdays": [day.isoformat() for day in self.makeup_workdays],
        }

    def to_countdown_item(self, base_date: date) -> dict[str, Any]:
        if base_date < self.start:
            days_left = (self.start - base_date).days
            label = f"距离{self.name}"
            value = f"{days_left}天"
            status = "upcoming"
        else:
            day_index = (base_date - self.start).days + 1
            days_left = 0
            label = f"{self.name}中"
            value = "今天" if day_index == 1 else f"第{day_index}天"
            status = "ongoing"
        return {
            "label": label,
            "value": value,
            "holiday": self.name,
            "start_date": self.start.isoformat(),
            "end_date": self.end.isoformat(),
            "days_left": days_left,
            "status": status,
        }


HOLIDAYS_2026 = (
    Holiday("元旦", date(2026, 1, 1), date(2026, 1, 3), 3, (date(2026, 1, 4),)),
    Holiday("春节", date(2026, 2, 15), date(2026, 2, 23), 9, (date(2026, 2, 14), date(2026, 2, 28))),
    Holiday("清明节", date(2026, 4, 4), date(2026, 4, 6), 3),
    Holiday("劳动节", date(2026, 5, 1), date(2026, 5, 5), 5, (date(2026, 5, 9),)),
    Holiday("端午节", date(2026, 6, 19), date(2026, 6, 21), 3),
    Holiday("中秋节", date(2026, 9, 25), date(2026, 9, 27), 3),
    Holiday("国庆节", date(2026, 10, 1), date(2026, 10, 7), 7, (date(2026, 9, 20), date(2026, 10, 10))),
)


def parse_base_date(value: Any = None) -> date:
    text = str(value or "").strip().lower()
    if not text or text in {"today", "auto"}:
        return date.today()
    return date.fromisoformat(text)


def holidays_from_schedule(raw_schedule: Iterable[dict[str, Any]] | None) -> list[Holiday]:
    holidays: list[Holiday] = []
    if not raw_schedule:
        return holidays
    for item in raw_schedule:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        start_text = str(item.get("start_date", "")).strip()
        end_text = str(item.get("end_date", "")).strip()
        if not name or not start_text or not end_text:
            continue
        holidays.append(
            Holiday(
                name=name,
                start=date.fromisoformat(start_text),
                end=date.fromisoformat(end_text),
                days_off=int(item.get("days_off", 0) or 0),
                makeup_workdays=tuple(
                    date.fromisoformat(str(day))
                    for day in item.get("makeup_workdays", [])
                    if str(day).strip()
                ),
            )
        )
    holidays.sort(key=lambda holiday: holiday.start)
    return holidays


def build_countdown_items(holidays: Iterable[Holiday], *, base_date: date, limit: int = 4) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    limit = max(limit, 0)
    if limit == 0:
        return items

    weekday = base_date.weekday()
    weekend_start = base_date + timedelta(days=(5 - weekday if weekday <= 4 else -(weekday - 5)))
    weekend_end = weekend_start + timedelta(days=1)
    if weekday <= 4:
        items.append(
            {
                "label": "距离周末",
                "value": f"{(weekend_start - base_date).days}天",
                "holiday": "周末",
                "start_date": weekend_start.isoformat(),
                "end_date": weekend_end.isoformat(),
                "days_left": (weekend_start - base_date).days,
                "status": "upcoming",
            }
        )
    else:
        day_index = 1 if weekday == 5 else 2
        items.append(
            {
                "label": "周末中",
                "value": "今天" if day_index == 1 else f"第{day_index}天",
                "holiday": "周末",
                "start_date": weekend_start.isoformat(),
                "end_date": weekend_end.isoformat(),
                "days_left": 0,
                "status": "ongoing",
            }
        )

    active_holidays = [holiday for holiday in holidays if holiday.end >= base_date]
    items.extend(holiday.to_countdown_item(base_date) for holiday in active_holidays[: max(limit - 1, 0)])
    return items[:limit]


def build_payload(base_date: date, *, title: str, limit: int) -> dict[str, Any]:
    return {
        "metadata": {
            "base_date_mode": "today",
            "calendar_year": 2026,
            "source": OFFICIAL_SOURCE,
        },
        "holiday_schedule": [holiday.to_schedule_dict() for holiday in HOLIDAYS_2026],
        "countdown": {
            "title": title,
            "auto_update": True,
            "base_date": "today",
            "limit": max(limit, 0),
        },
        "preview": {
            "base_date": base_date.isoformat(),
            "items": build_countdown_items(HOLIDAYS_2026, base_date=base_date, limit=limit),
        },
    }
