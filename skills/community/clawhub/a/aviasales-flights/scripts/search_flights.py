#!/usr/bin/env python3
"""
Поиск авиабилетов через Travelpayouts API (Aviasales).

Использование:
  python3 search_flights.py --from MOW --to LED --date 2026-04-15
  python3 search_flights.py --from MOW --to LED --date 2026-04-15 --return 2026-04-20
  python3 search_flights.py --from MOW --to LED --month 2026-04
  python3 search_flights.py --from MOW --to AER --latest
  python3 search_flights.py --from MOW --directions
  python3 search_flights.py --lookup "Стамбул"
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# ─── Константы ────────────────────────────────────────────────────────────────

BASE_URL = "https://api.travelpayouts.com"
AUTOCOMPLETE_URL = "https://autocomplete.travelpayouts.com/places2"
AIRLINES_CACHE = "/tmp/airlines_cache.json"
AIRLINES_CACHE_TTL = 86400  # 24 часа

# Встроенный маппинг на случай недоступности API
AIRLINES_FALLBACK = {
    "SU": "Аэрофлот",
    "S7": "S7 Airlines",
    "DP": "Победа",
    "UT": "ЮТэйр",
    "U6": "Уральские авиалинии",
    "5N": "Smartavia",
    "WZ": "Red Wings",
    "N4": "Nordwind",
    "FV": "Россия",
    "IO": "IrAero",
    "GH": "Глобус",
    "SU": "Аэрофлот",
    "EK": "Emirates",
    "TK": "Turkish Airlines",
    "LH": "Lufthansa",
    "AF": "Air France",
    "BA": "British Airways",
    "QR": "Qatar Airways",
    "PC": "Pegasus",
    "FR": "Ryanair",
    "W6": "Wizz Air",
}


# ─── Вспомогательные функции ──────────────────────────────────────────────────

def get_token() -> str:
    token = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
    if not token:
        print(json.dumps({"error": "TRAVELPAYOUTS_TOKEN не задан в окружении"}), file=sys.stderr)
        sys.exit(1)
    return token


def load_airlines(token: str) -> dict:
    """Загружает маппинг авиакомпаний с кэшированием."""
    cache_path = Path(AIRLINES_CACHE)

    # Проверяем кэш
    if cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < AIRLINES_CACHE_TTL:
            try:
                with open(cache_path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    # Загружаем с API
    try:
        url = f"{BASE_URL}/data/ru/airlines.json"
        resp = requests.get(url, params={"token": token}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # data — список объектов [{code, name, ...}]
        mapping = {}
        for item in data:
            code = item.get("code") or item.get("iata")
            name = item.get("name") or item.get("name_translations", {}).get("ru", "")
            if code and name:
                mapping[code] = name
        # Сохраняем кэш
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False)
        return mapping
    except Exception:
        # Возвращаем встроенный маппинг
        return AIRLINES_FALLBACK


def airline_name(code: str, airlines: dict) -> str:
    """Возвращает название авиакомпании по коду."""
    return airlines.get(code, code)


def duration_str(minutes: int) -> str:
    """Форматирует минуты в '2ч 30мин'."""
    if not minutes:
        return "—"
    h = minutes // 60
    m = minutes % 60
    if h and m:
        return f"{h}ч {m}мин"
    elif h:
        return f"{h}ч"
    else:
        return f"{m}мин"


def transfers_str(count: int) -> str:
    """Форматирует количество пересадок."""
    if count == 0:
        return "прямой"
    elif count == 1:
        return "1 пересадка"
    elif 2 <= count <= 4:
        return f"{count} пересадки"
    else:
        return f"{count} пересадок"


def build_link(raw_link: str) -> str:
    """Строит полную ссылку на Aviasales."""
    if not raw_link:
        return ""
    if raw_link.startswith("http"):
        return raw_link
    return "https://aviasales.ru" + raw_link


def format_flight(item: dict, airlines: dict) -> dict:
    """Приводит запись из API к единому формату."""
    airline_code = item.get("airline", "")
    transfers = item.get("transfers", 0)
    dur = item.get("duration") or item.get("flight_time") or 0
    # Некоторые API возвращают duration в секундах, другие в минутах
    if dur > 1440:  # скорее всего секунды
        dur = dur // 60

    return {
        "price": item.get("price", 0),
        "airline": airline_name(airline_code, airlines),
        "airline_code": airline_code,
        "flight": item.get("flight_number", ""),
        "from_airport": item.get("origin", item.get("origin_airport", "")),
        "to_airport": item.get("destination", item.get("destination_airport", "")),
        "departure": item.get("departure_at", item.get("depart_date", "")),
        "return_at": item.get("return_at", ""),
        "duration_min": dur,
        "duration_str": duration_str(dur),
        "transfers": transfers,
        "transfers_str": transfers_str(transfers),
        "link": build_link(item.get("link", "")),
    }


# ─── Команды ──────────────────────────────────────────────────────────────────

def cmd_lookup(term: str):
    """Поиск IATA-кода по названию города."""
    try:
        resp = requests.get(
            AUTOCOMPLETE_URL,
            params={"term": term, "locale": "ru", "types[]": ["city", "airport"]},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data[:10]:
            results.append({
                "code": item.get("code", ""),
                "name": item.get("name", ""),
                "country": item.get("country_name", ""),
                "type": item.get("type", ""),
            })
        print(json.dumps({"query": term, "results": results}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def cmd_search_dates(args, token: str, airlines: dict):
    """Поиск билетов на конкретную дату (prices_for_dates)."""
    params = {
        "origin": args.frm,
        "destination": args.to,
        "token": token,
        "sorting": "price",
        "limit": args.limit,
    }
    if args.date:
        params["departure_at"] = args.date
    if args.ret:
        params["return_at"] = args.ret
    if args.direct:
        params["direct"] = "true"

    try:
        resp = requests.get(
            f"{BASE_URL}/aviasales/v3/prices_for_dates",
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    raw_results = data.get("data", [])
    results = [format_flight(item, airlines) for item in raw_results]

    output = {
        "query": {
            "from": args.frm,
            "to": args.to,
            "date": args.date or "",
            "return": args.ret or "",
            "direct": args.direct,
        },
        "results": results,
        "cheapest": min((r["price"] for r in results), default=None),
        "count": len(results),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_calendar(args, token: str, airlines: dict):
    """Календарь минимальных цен по месяцу (grouped_prices)."""
    params = {
        "origin": args.frm,
        "destination": args.to,
        "token": token,
        "group_by": "departure_at",
    }
    # month в формате YYYY-MM — передаём как фильтр (API не фильтрует напрямую, берём всё)
    try:
        resp = requests.get(
            f"{BASE_URL}/aviasales/v3/grouped_prices",
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    raw_results = data.get("data", {})
    # grouped_prices возвращает dict: {"2026-04-01": {price, airline, ...}, ...}
    if isinstance(raw_results, dict):
        items = []
        for date_key, item in raw_results.items():
            if args.month and not date_key.startswith(args.month):
                continue
            item["depart_date"] = date_key
            items.append(item)
    else:
        items = raw_results

    results = [format_flight(item, airlines) for item in items]
    results.sort(key=lambda x: x["price"])

    output = {
        "query": {
            "from": args.frm,
            "to": args.to,
            "month": args.month,
            "mode": "calendar",
        },
        "results": results,
        "cheapest": min((r["price"] for r in results), default=None),
        "count": len(results),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_latest(args, token: str, airlines: dict):
    """Последние найденные цены (get_latest_prices)."""
    params = {
        "origin": args.frm,
        "token": token,
        "limit": args.limit,
        "period_type": "year",
        "one_way": "true" if args.one_way else "false",
    }
    if args.to:
        params["destination"] = args.to

    try:
        resp = requests.get(
            f"{BASE_URL}/aviasales/v3/get_latest_prices",
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    raw_results = data.get("data", [])
    results = [format_flight(item, airlines) for item in raw_results]

    output = {
        "query": {
            "from": args.frm,
            "to": args.to or "any",
            "mode": "latest",
            "one_way": args.one_way,
        },
        "results": results,
        "cheapest": min((r["price"] for r in results), default=None),
        "count": len(results),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_directions(args, token: str, airlines: dict):
    """Популярные направления из города (city-directions)."""
    params = {
        "origin": args.frm,
        "token": token,
    }
    try:
        resp = requests.get(
            f"{BASE_URL}/v1/city-directions",
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    raw_results = data.get("data", {})
    # city-directions возвращает dict: {"AER": {price, airline, ...}, ...}
    directions = []
    if isinstance(raw_results, dict):
        for dest_code, item in raw_results.items():
            item["destination"] = dest_code
            formatted = format_flight(item, airlines)
            formatted["to_airport"] = dest_code
            directions.append(formatted)
    else:
        directions = [format_flight(item, airlines) for item in raw_results]

    directions.sort(key=lambda x: x["price"])

    output = {
        "query": {"from": args.frm, "mode": "directions"},
        "results": directions,
        "count": len(directions),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ─── Точка входа ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Поиск авиабилетов через Travelpayouts API"
    )
    parser.add_argument("--from", dest="frm", help="Код аэропорта/города отправления (напр. MOW)")
    parser.add_argument("--to", help="Код аэропорта/города назначения (напр. LED)")
    parser.add_argument("--date", help="Дата вылета YYYY-MM-DD")
    parser.add_argument("--return", dest="ret", help="Дата возврата YYYY-MM-DD")
    parser.add_argument("--month", help="Месяц для календаря цен YYYY-MM")
    parser.add_argument("--direct", action="store_true", help="Только прямые рейсы")
    parser.add_argument("--limit", type=int, default=10, help="Максимум результатов (по умолч. 10)")
    parser.add_argument("--latest", action="store_true", help="Режим: последние найденные цены")
    parser.add_argument("--one-way", action="store_true", help="Только билеты в одну сторону")
    parser.add_argument("--directions", action="store_true", help="Популярные направления из города")
    parser.add_argument("--lookup", metavar="CITY", help="Поиск IATA-кода по названию города")

    args = parser.parse_args()

    # Поиск IATA-кода — токен не нужен
    if args.lookup:
        cmd_lookup(args.lookup)
        return

    token = get_token()
    airlines = load_airlines(token)

    if args.directions:
        if not args.frm:
            parser.error("--from обязателен для --directions")
        cmd_directions(args, token, airlines)
    elif args.latest:
        if not args.frm:
            parser.error("--from обязателен для --latest")
        cmd_latest(args, token, airlines)
    elif args.month:
        if not args.frm or not args.to:
            parser.error("--from и --to обязательны для --month")
        cmd_calendar(args, token, airlines)
    else:
        if not args.frm or not args.to:
            parser.error("--from и --to обязательны для поиска по датам")
        cmd_search_dates(args, token, airlines)


if __name__ == "__main__":
    main()
