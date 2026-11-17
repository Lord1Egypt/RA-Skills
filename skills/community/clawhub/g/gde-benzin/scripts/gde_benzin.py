#!/usr/bin/env python3
"""Official read-only client for gde-benzin.ru; Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import email.utils
import json
import math
import re
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

VERSION = "1.1.2"
API = "https://gde-benzin.ru/api"
SITE = "https://gde-benzin.ru/"
AUTHOR_URL = "https://www.youtube.com/@d_tylnyi"
TERMS_URL = "https://github.com/tylnyi/Gde-Benzin-Skill/blob/v1.1.0/skills/gde-benzin/references/api-terms.md"
MAX_BODY = 8 * 1024 * 1024
EARTH_KM = 6371.0088
LABELS = {"ai92": "АИ-92", "ai95": "АИ-95", "ai98": "АИ-98", "ai100": "АИ-100", "dt": "ДТ"}
UTM = {"utm_source": "ai_agent", "utm_medium": "referral", "utm_campaign": "official_skill"}


class ApiError(Exception):
    pass


class IncompleteResult(ApiError):
    pass


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if target.scheme != "https" or target.hostname != "gde-benzin.ru" or target.port not in (None, 443):
            raise ApiError("API перенаправил запрос за пределы официального HTTPS-домена")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Client:
    def __init__(self, opener=None, sleep=time.sleep):
        self.opener = opener or build_opener(OfficialRedirects())
        self.sleep = sleep

    def get(self, path, params=None):
        url = API + path + ("?" + urlencode(params) if params else "")
        request = Request(url, headers={"Accept": "application/json", "User-Agent": f"GdeBenzinSkill/{VERSION} (+https://github.com/tylnyi/Gde-Benzin-Skill)"})
        for attempt in range(2):
            try:
                with self.opener.open(request, timeout=15) as response:
                    content_type = response.headers.get("Content-Type", "").lower()
                    if "application/json" not in content_type:
                        raise ApiError("API вернул не JSON; возможно, временная защита или сбой")
                    raw = response.read(MAX_BODY + 1)
                    if len(raw) > MAX_BODY:
                        raise IncompleteResult("Ответ слишком велик; уменьшите радиус")
                    try:
                        return json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
                    except (ValueError, UnicodeError) as exc:
                        raise ApiError("API вернул некорректный JSON") from exc
            except HTTPError as exc:
                delay = retry_delay(exc.headers.get("Retry-After"))
                exc.close()
                if attempt == 0 and exc.code in (429, 502, 503, 504) and delay is not None:
                    self.sleep(delay)
                    continue
                raise ApiError(f"API недоступен (HTTP {exc.code}); повторите позже") from exc
            except (URLError, TimeoutError, socket.timeout, OSError) as exc:
                if attempt == 0:
                    self.sleep(1)
                    continue
                raise ApiError("Не удалось связаться с API; проверьте сеть и повторите позже") from exc
        raise ApiError("Не удалось завершить запрос")


def retry_delay(raw):
    if raw is None:
        return 1
    try:
        delay = float(raw)
    except (ValueError, TypeError):
        try:
            delay = (email.utils.parsedate_to_datetime(raw) - datetime.now(timezone.utc)).total_seconds()
        except (ValueError, TypeError, OverflowError):
            return None
    return max(0, delay) if math.isfinite(delay) and delay <= 5 else None


def number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def text(value, limit=250):
    if not isinstance(value, str):
        return ""
    # Keep API strings as single-line display data; strip terminal controls/bidi.
    return re.sub(r"[\x00-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]", " ", value).strip()[:limit]


def map_url(station_id=None):
    return SITE + "?" + urlencode(UTM) + (f"#station={station_id}" if station_id is not None else "")


def fuel_code(value):
    key = value.strip().lower().replace("аи", "ai").replace("-", "").replace(" ", "")
    if key in ("дт", "дизель", "diesel"):
        key = "dt"
    if key in ("92", "95", "98", "100"):
        key = "ai" + key
    if key not in LABELS:
        raise argparse.ArgumentTypeError("Марка должна быть 92, 95, 98, 100 или ДТ")
    return key


def distance_km(lat, lon, other_lat, other_lon):
    p1, p2 = math.radians(lat), math.radians(other_lat)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(other_lon - lon) / 2) ** 2
    return 2 * EARTH_KM * math.asin(min(1, math.sqrt(max(0, h))))


def bounding_boxes(lat, lon, radius):
    delta = radius / EARTH_KM
    south, north = max(-90, lat - math.degrees(delta)), min(90, lat + math.degrees(delta))
    if south == -90 or north == 90:
        return [(south, -180, north, 180)]
    dlon = math.degrees(math.asin(min(1, math.sin(delta) / math.cos(math.radians(lat)))))
    west, east = lon - dlon, lon + dlon
    if west < -180:
        return [(south, west + 360, north, 180), (south, -180, north, east)]
    if east > 180:
        return [(south, west, north, 180), (south, -180, north, east - 360)]
    return [(south, west, north, east)]


def timestamp_age(value, now):
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            return None
        age = (now - stamp).total_seconds()
        return max(0, age) if age >= -60 else None
    except (ValueError, TypeError, OverflowError):
        return None


def age_seconds(record, now, *, price=False):
    key = "price_freshness_seconds" if price else "freshness_seconds"
    supplied = record.get(key)
    measured = None if price else timestamp_age(record.get("last_report_at"), now)
    if not price and record.get("last_report_at") is not None and measured is None:
        return None
    values = [v for v in (supplied, measured) if number(v) and v >= 0]
    return max(values) if values else None


def normalize_station(raw, now, status_age, price_age, lat=None, lon=None):
    if not isinstance(raw, dict):
        raise ApiError("Некорректная запись АЗС")
    sid, slat, slon = raw.get("id"), raw.get("lat"), raw.get("lon")
    if not isinstance(sid, int) or isinstance(sid, bool) or sid <= 0 or not number(slat) or not number(slon) or not -90 <= slat <= 90 or not -180 <= slon <= 180:
        raise ApiError("API вернул некорректный идентификатор или координаты АЗС")
    fuels, prices = raw.get("fuels"), raw.get("prices")
    if not isinstance(fuels, dict) or not isinstance(prices, dict):
        raise ApiError("Изменился формат сведений о топливе")
    normalized = {}
    for code, label in LABELS.items():
        f = fuels.get(code) or {}
        p = prices.get(code) or {}
        if not isinstance(f, dict) or not isinstance(p, dict):
            raise ApiError("Некорректный формат марки топлива")
        age = age_seconds(f, now)
        expires = f.get("expires_in_seconds")
        fresh = age is not None and age <= status_age and number(expires) and expires > 0
        available = f.get("available") if fresh and isinstance(f.get("available"), bool) else None
        p_age = p.get("freshness_seconds")
        if not number(p_age) or p_age < 0:
            p_age = age_seconds(f, now, price=True)
        value = p.get("price", f.get("price"))
        price = value if number(value) and value > 0 and number(p_age) and 0 <= p_age <= price_age else None
        normalized[code] = {"label": label, "available": available,
                            "availability_age_seconds": round(age) if fresh else None,
                            "price_rub_per_liter": price,
                            "price_age_seconds": round(p_age) if price is not None else None}
    result = {"id": sid, "name": text(raw.get("name")) or "АЗС", "address": text(raw.get("address"), 500),
              "lat": slat, "lon": slon, "fuels": normalized, "map_url": map_url(sid)}
    if lat is not None:
        result["distance_km"] = round(distance_km(lat, lon, slat, slon), 3)
    return result


def envelope():
    return {"schema_version": 1, "provider": "Где бензин", "source_url": map_url(),
            "attribution": {"required": True, "website_url": SITE,
                            "author_name": "Дмитрий Тыльный", "author_url": AUTHOR_URL,
                            "terms_url": TERMS_URL, "terms_version": "1.0"},
            "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def attribution_footer(data):
    return f"Данные: [Где бензин]({data['source_url']}) · [Автор проекта — Дмитрий Тыльный]({AUTHOR_URL})"


def search(client, args):
    now = datetime.now(timezone.utc)
    stations = {}
    for box in bounding_boxes(args.lat, args.lon, args.radius_km):
        payload = client.get("/stations", {"bbox": ",".join(f"{v:.8f}" for v in box)})
        if not isinstance(payload, dict) or not isinstance(payload.get("stations"), list) or payload.get("truncated") is not False or payload.get("count") != len(payload["stations"]):
            raise IncompleteResult("Выдача неполная или формат изменился; уменьшите радиус и повторите поиск")
        for raw in payload["stations"]:
            s = normalize_station(raw, now, args.max_status_age_hours * 3600, args.max_price_age_hours * 3600, args.lat, args.lon)
            # API rounds bbox outwards; apply the exact requested circle locally.
            if distance_km(args.lat, args.lon, s["lat"], s["lon"]) > args.radius_km:
                continue
            if args.fuel and s["fuels"][args.fuel]["available"] is not True:
                continue
            stations[s["id"]] = s
    ordered = sorted(stations.values(), key=lambda s: (s["distance_km"], s["id"]))
    out = envelope()
    out.update(status="ok" if ordered else "no_matches", query={"lat": args.lat, "lon": args.lon, "radius_km": args.radius_km, "fuel": args.fuel},
               matching_count=len(ordered), shown_count=min(args.limit, len(ordered)), stations=ordered[:args.limit],
               note="Расстояние по прямой, не длина маршрута. Наличие и цены уточняйте на АЗС.")
    return out


def locate(client, query):
    data = client.get("/geocode", {"text": query})
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise ApiError("Изменился формат поиска населённых пунктов")
    items = []
    for row in data["items"][:10]:
        if not isinstance(row, dict) or not number(row.get("lat")) or not number(row.get("lon")) or not -90 <= row["lat"] <= 90 or not -180 <= row["lon"] <= 180:
            raise ApiError("Некорректные координаты населённого пункта")
        items.append({"name": text(row.get("n")), "description": text(row.get("full"), 500), "lat": row["lat"], "lon": row["lon"]})
    return {**envelope(), "status": "ok" if items else "no_matches", "places": items,
            "note": "Выберите подходящее место. Центр города не является геопозицией пользователя."}


def markdown(value):
    return re.sub(r"([\\`*_{}\[\]()<>#!|])", r"\\\1", text(value, 500))


def age_label(value):
    if value is None:
        return "нет данных о времени"
    return f"{max(0, int(value) // 60)} мин назад" if value < 3600 else f"{value / 3600:.1f} ч назад"


def render(data, selected_fuel=None):
    lines = ["Где бензин — данные на " + data["checked_at"]]
    if "places" in data:
        for p in data["places"]:
            lines.append(f"- {markdown(p['description'] or p['name'])}: {p['lat']}, {p['lon']}")
    for s in data.get("stations", []):
        distance = f" · {s['distance_km']:.2f} км по прямой" if "distance_km" in s else ""
        lines.append(f"\n**{markdown(s['name'])}**{distance}")
        if s["address"]:
            lines.append(markdown(s["address"]))
        codes = [selected_fuel] if selected_fuel else [code for code in LABELS
                if s["fuels"][code]["available"] is not None or s["fuels"][code]["price_rub_per_liter"] is not None]
        if not codes:
            lines.append("Нет актуальных данных о наличии и ценах по маркам топлива.")
        for code in codes:
            f = s["fuels"][code]
            state = {True: "есть по данным сервиса", False: "отмечено отсутствие", None: "нет актуальных данных"}[f["available"]]
            value = f["label"] + ": " + state
            if f["available"] is not None:
                value += " (" + age_label(f["availability_age_seconds"]) + ")"
            if f["price_rub_per_liter"] is not None:
                value += f"; {f['price_rub_per_liter']:.2f} ₽/л, цена {age_label(f['price_age_seconds'])}"
            lines.append("- " + value)
        lines.append(f"[Открыть АЗС на карте «Где бензин»]({s['map_url']})")
    if data.get("status") == "no_matches":
        lines.append("Подходящих актуальных сведений в этой выборке не найдено. Это не означает отсутствие топлива.")
    if data.get("note"):
        lines.append(data["note"])
    lines.append(attribution_footer(data))
    return "\n".join(lines)


def bounded_float(low, high):
    def parse(value):
        try:
            n = float(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("Ожидается число") from exc
        if not math.isfinite(n) or not low <= n <= high:
            raise argparse.ArgumentTypeError(f"Число должно быть от {low} до {high}")
        return n
    return parse


def bounded_int(low, high):
    def parse(value):
        try:
            n = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError("Ожидается целое число") from exc
        if not low <= n <= high:
            raise argparse.ArgumentTypeError(f"Число должно быть от {low} до {high}")
        return n
    return parse


def parser():
    p = argparse.ArgumentParser(description="Официальный поиск АЗС через gde-benzin.ru (только чтение)")
    p.add_argument("--version", action="version", version=VERSION)
    subs = p.add_subparsers(dest="command", required=True)
    s = subs.add_parser("search", help="АЗС в радиусе, с выбранной маркой или без фильтра")
    s.add_argument("--lat", type=bounded_float(-90, 90), required=True)
    s.add_argument("--lon", type=bounded_float(-180, 180), required=True)
    s.add_argument("--radius-km", type=bounded_float(0.5, 50), default=5)
    s.add_argument("--limit", type=bounded_int(1, 10), default=5)
    s.add_argument("--fuel", type=fuel_code)
    place = subs.add_parser("locate", help="Найти координаты города или места")
    place.add_argument("query")
    one = subs.add_parser("station", help="Прочитать конкретную АЗС")
    one.add_argument("id", type=bounded_int(1, 2**63 - 1))
    for sub in (s, one):
        sub.add_argument("--max-status-age-hours", type=bounded_float(0.01, 6), default=6)
        sub.add_argument("--max-price-age-hours", type=bounded_float(0.01, 336), default=24)
    for sub in (s, place, one):
        sub.add_argument("--format", choices=("text", "json"), default="text")
    return p


def main(argv=None, client=None):
    p = parser()
    args = p.parse_args(argv)
    if args.command == "locate" and not 2 <= len(args.query.strip()) <= 200:
        p.error("Укажите место длиной от 2 до 200 символов")
    try:
        client = client or Client()
        if args.command == "search":
            data = search(client, args)
        elif args.command == "locate":
            data = locate(client, args.query)
        else:
            station = normalize_station(client.get(f"/stations/{args.id}"), datetime.now(timezone.utc), args.max_status_age_hours * 3600, args.max_price_age_hours * 3600)
            data = {**envelope(), "status": "ok", "stations": [station], "note": "Наличие и цены уточняйте на АЗС."}
        print(json.dumps(data, ensure_ascii=False, allow_nan=False) if args.format == "json" else render(data, getattr(args, "fuel", None)))
        return 0
    except ApiError as exc:
        data = {**envelope(), "status": "incomplete" if isinstance(exc, IncompleteResult) else "error", "message": str(exc)}
        print(json.dumps(data, ensure_ascii=False) if args.format == "json" else str(exc) + "\n" + attribution_footer(data))
        return 4 if isinstance(exc, IncompleteResult) else 3


if __name__ == "__main__":
    sys.exit(main())
