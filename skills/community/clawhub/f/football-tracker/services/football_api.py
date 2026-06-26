import os
import re
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

BASE_URL = "https://api.football-data.org/v4"
MATCH_BROADCAST_KEYWORDS = [
    "ESPN",
    "ESPN Brasil",
    "SporTV",
    "Sportv",
    "Premiere",
    "Premiere FC",
    "TV Globo",
    "Globo",
    "Record",
    "TNT Sports",
    "Max",
    "Disney+",
    "Prime Video",
    "Paramount+",
    "DAZN",
    "Sky Sports",
    "NBC",
    "CBS",
    "FOX",
]


def _get_json(url, api_key, timeout=20):
    req = Request(url, headers={"X-Auth-Token": api_key})

    with urlopen(req, timeout=timeout) as resp:
        import json

        return json.loads(resp.read().decode("utf-8"))


WEEKDAYS = {
    "pt": [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ],
    "en": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
}


def get_matches(team_id, api_key, locale="pt"):

    url = f"{BASE_URL}/teams/{team_id}/matches"
    try:
        data = _get_json(url, api_key)
    except (HTTPError, URLError, ValueError):
        return {
            "last": "N/A",
            "next": "N/A",
            "competition": "N/A",
            "competition_id": None,
        }

    matches = data.get("matches", [])

    past = []
    future = []

    for m in matches:

        if m["status"] in ["FINISHED"]:

            past.append(m)
        else:
            future.append(m)

    last_game = sorted(
        past,
        key=lambda x: x["utcDate"],
        reverse=True
    )

    next_game = sorted(
        future,
        key=lambda x: x["utcDate"]
    )

    next_match = next_game[0] if future else None

    return {
        "last": format_match(last_game[0]) if past else "N/A",
        "next": format_match(next_match) if next_match else "N/A",
        "next_time": format_kickoff(next_match.get("utcDate"), locale=locale) if next_match else "N/A",
        "next_round": next_match.get("matchday") if next_match else None,
        "broadcasts": get_broadcasts(next_match, api_key) if next_match else [],
        "competition": matches[0]["competition"]["name"] if matches else "N/A",
        "competition_type": matches[0]["competition"].get("type") if matches else None,
        "competition_id": matches[0]["competition"]["id"] if matches else None,
    }


def get_standings(team_id, api_key, competition_id=None, locale="pt"):
    if not competition_id:
        return "standing not available" if locale == "en" else "posição não disponível"

    url = f"{BASE_URL}/competitions/{competition_id}/standings"

    try:
        data = _get_json(url, api_key)
    except (HTTPError, URLError, ValueError):
        return "standing not available" if locale == "en" else "posição não disponível"

    standings = data.get("standings", [])
    for table in standings:
        for row in table.get("table", []):
            team = row.get("team", {})
            if team.get("id") == team_id:
                position = row.get("position")
                points = row.get("points")
                played = row.get("playedGames")
                if locale == "en":
                    return f"{position}th place, {points} points in {played} matches"
                return f"{position}º lugar, {points} pontos em {played} jogos"

    return "standing not available" if locale == "en" else "posição não disponível"


def format_match(match):

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    score = match["score"]["fullTime"]

    if score["home"] is None or score["away"] is None:
        return f"{home} x {away}"

    return f"{home} {score['home']}x{score['away']} {away}"


def format_kickoff(utc_date, locale="pt"):
    if not utc_date:
        return "N/A"

    try:
        dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
    except Exception:
        return utc_date

    local_tz = _local_timezone()
    local_dt = dt.astimezone(local_tz)
    utc_dt = dt.astimezone(timezone.utc)
    local_day = _weekday_name(local_dt.weekday(), locale)
    utc_day = _weekday_name(utc_dt.weekday(), "en")
    return f"{local_day}, {local_dt:%d/%m/%Y %H:%M} ({_timezone_label(local_tz, local_dt)}) / {utc_day}, {utc_dt:%d/%m/%Y %H:%M} UTC"


def format_kickoff_from_et(date_str, kickoff_et, locale="pt"):
    if not date_str or not kickoff_et:
        return "N/A"

    try:
        source_tz = ZoneInfo("America/New_York") if ZoneInfo else None
        if source_tz is None:
            return f"{date_str} {kickoff_et}"
        source_dt = datetime.fromisoformat(f"{date_str}T{kickoff_et}:00").replace(tzinfo=source_tz)
        local_dt = source_dt.astimezone(_local_timezone())
        utc_dt = source_dt.astimezone(timezone.utc)
        local_day = _weekday_name(local_dt.weekday(), locale)
        utc_day = _weekday_name(utc_dt.weekday(), "en")
        return f"{local_day}, {local_dt:%d/%m/%Y %H:%M} ({_timezone_label(_local_timezone(), local_dt)}) / {utc_day}, {utc_dt:%d/%m/%Y %H:%M} UTC"
    except Exception:
        return f"{date_str} {kickoff_et}"


def get_broadcasts(match, api_key):
    if not match:
        return []

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    query = f'"{home}" "{away}" onde assistir transmissão'
    url = "https://news.google.com/rss/search?q=" + quote(query) + "&hl=pt-BR&gl=BR&ceid=BR:pt-419"

    try:
        with urlopen(url, timeout=20) as resp:
            xml = resp.read().decode("utf-8", "ignore")
    except Exception:
        return []

    text_blobs = re.findall(r"<item>(.*?)</item>", xml, re.S)[:5]
    found = []

    for blob in text_blobs:
        haystack = f"{_extract_tag(blob, 'title')} {_extract_tag(blob, 'description')}"
        link = _extract_tag(blob, "link")
        if link:
            haystack += " " + _fetch_page_text(link)
        for keyword in MATCH_BROADCAST_KEYWORDS:
            if keyword.lower() in haystack.lower() and keyword not in found:
                found.append(keyword)

    return found


def _extract_tag(xml, tag):
    match = re.search(rf"<{tag}>(.*?)</{tag}>", xml, re.S)
    if not match:
        return ""
    return match.group(1).strip()


def _fetch_page_text(url):
    try:
        with urlopen(url, timeout=6) as resp:
            html = resp.read().decode("utf-8", "ignore")
    except Exception:
        return ""

    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()[:5000]


def _local_timezone():
    tz_name = os.environ.get("TZ")
    if tz_name and ZoneInfo:
        try:
            return ZoneInfo(tz_name)
        except Exception:
            pass
    return datetime.now().astimezone().tzinfo


def _timezone_label(tzinfo, dt):
    label = getattr(tzinfo, "key", None)
    if label:
        return label
    name = dt.tzname() or "local"
    return name


def _weekday_name(weekday, locale="pt"):
    names = WEEKDAYS.get(locale, WEEKDAYS["pt"])
    return names[weekday]
