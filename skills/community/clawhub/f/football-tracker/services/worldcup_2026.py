import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


BASE_DIR = Path(__file__).resolve().parent.parent
SCHEDULE_PATH = BASE_DIR / "storage" / "worldcup_2026_schedule.txt"
MATCH_META_PATH = BASE_DIR / "storage" / "worldcup_2026_match_meta.json"
SOURCE_TZ = "America/New_York"
COMPETITION_ID = 17
COMPETITION_NAME = "FIFA World Cup 2026™"


def _normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.lower().strip())

GROUPS = {
    "A": [("Mexico", "MEX"), ("South Africa", "RSA"), ("Korea Republic", "KOR"), ("Czechia", "CZE")],
    "B": [("Canada", "CAN"), ("Bosnia & Herzegovina", "BIH"), ("Qatar", "QAT"), ("Switzerland", "SUI")],
    "C": [("Brazil", "BRA"), ("Morocco", "MAR"), ("Haiti", "HAI"), ("Scotland", "SCO")],
    "D": [("USA", "USA"), ("Paraguay", "PAR"), ("Australia", "AUS"), ("Türkiye", "TUR")],
    "E": [("Germany", "GER"), ("Curaçao", "CUW"), ("Côte d'Ivoire", "CIV"), ("Ecuador", "ECU")],
    "F": [("Netherlands", "NED"), ("Japan", "JPN"), ("Sweden", "SWE"), ("Tunisia", "TUN")],
    "G": [("Belgium", "BEL"), ("Egypt", "EGY"), ("Iran", "IRN"), ("New Zealand", "NZL")],
    "H": [("Spain", "ESP"), ("Cabo Verde", "CPV"), ("Saudi Arabia", "KSA"), ("Uruguay", "URU")],
    "I": [("France", "FRA"), ("Senegal", "SEN"), ("Iraq", "IRQ"), ("Norway", "NOR")],
    "J": [("Argentina", "ARG"), ("Algeria", "ALG"), ("Austria", "AUT"), ("Jordan", "JOR")],
    "K": [("Portugal", "POR"), ("Congo DR", "COD"), ("Uzbekistan", "UZB"), ("Colombia", "COL")],
    "L": [("England", "ENG"), ("Croatia", "CRO"), ("Ghana", "GHA"), ("Panama", "PAN")],
}

TEAM_NAMES_PT = {
    "MEX": "México",
    "RSA": "África do Sul",
    "KOR": "Coreia do Sul",
    "CZE": "Chéquia",
    "CAN": "Canadá",
    "BIH": "Bósnia e Herzegovina",
    "QAT": "Catar",
    "SUI": "Suíça",
    "BRA": "Brasil",
    "MAR": "Marrocos",
    "HAI": "Haiti",
    "SCO": "Escócia",
    "USA": "Estados Unidos",
    "PAR": "Paraguai",
    "AUS": "Austrália",
    "TUR": "Turquia",
    "GER": "Alemanha",
    "CUW": "Curaçao",
    "CIV": "Costa do Marfim",
    "ECU": "Equador",
    "NED": "Países Baixos",
    "JPN": "Japão",
    "SWE": "Suécia",
    "TUN": "Tunísia",
    "BEL": "Bélgica",
    "EGY": "Egito",
    "IRN": "Irã",
    "NZL": "Nova Zelândia",
    "ESP": "Espanha",
    "CPV": "Cabo Verde",
    "KSA": "Arábia Saudita",
    "URU": "Uruguai",
    "FRA": "França",
    "SEN": "Senegal",
    "IRQ": "Iraque",
    "NOR": "Noruega",
    "ARG": "Argentina",
    "ALG": "Argélia",
    "AUT": "Áustria",
    "JOR": "Jordânia",
    "POR": "Portugal",
    "COD": "RD Congo",
    "UZB": "Uzbequistão",
    "COL": "Colômbia",
    "ENG": "Inglaterra",
    "CRO": "Croácia",
    "GHA": "Gana",
    "PAN": "Panamá",
}

TEAM_FLAGS = {
    "MEX": "🇲🇽",
    "RSA": "🇿🇦",
    "KOR": "🇰🇷",
    "CZE": "🇨🇿",
    "CAN": "🇨🇦",
    "BIH": "🇧🇦",
    "QAT": "🇶🇦",
    "SUI": "🇨🇭",
    "BRA": "🇧🇷",
    "MAR": "🇲🇦",
    "HAI": "🇭🇹",
    "SCO": "🏴",
    "USA": "🇺🇸",
    "PAR": "🇵🇾",
    "AUS": "🇦🇺",
    "TUR": "🇹🇷",
    "GER": "🇩🇪",
    "CUW": "🇨🇼",
    "CIV": "🇨🇮",
    "ECU": "🇪🇨",
    "NED": "🇳🇱",
    "JPN": "🇯🇵",
    "SWE": "🇸🇪",
    "TUN": "🇹🇳",
    "BEL": "🇧🇪",
    "EGY": "🇪🇬",
    "IRN": "🇮🇷",
    "NZL": "🇳🇿",
    "ESP": "🇪🇸",
    "CPV": "🇨🇻",
    "KSA": "🇸🇦",
    "URU": "🇺🇾",
    "FRA": "🇫🇷",
    "SEN": "🇸🇳",
    "IRQ": "🇮🇶",
    "NOR": "🇳🇴",
    "ARG": "🇦🇷",
    "ALG": "🇩🇿",
    "AUT": "🇦🇹",
    "JOR": "🇯🇴",
    "POR": "🇵🇹",
    "COD": "🇨🇩",
    "UZB": "🇺🇿",
    "COL": "🇨🇴",
    "ENG": "🏴",
    "CRO": "🇭🇷",
    "GHA": "🇬🇭",
    "PAN": "🇵🇦",
}

PHASE_RULES = {
    "group_stage": "48 teams in 12 groups. The top 2 from each group advance, plus the best third-placed teams until the round of 32 is filled.",
    "round_of_32": "Knockout round seeded by group position and the best third-placed teams.",
    "round_of_16": "Round of 16 with the 16 winners from the prior round.",
    "quarter_finals": "Quarter-finals with the remaining 8 teams.",
    "semi_finals": "Semi-finals with 4 teams.",
    "bronze_final": "Third-place playoff between the semi-final losers.",
    "final": "Single-match final between the semi-final winners.",
}

TEAM_DATA = {}
ALIASES = {}
for group, teams in GROUPS.items():
    for name, code in teams:
        TEAM_DATA[code] = {"code": code, "name": name, "group": group}
        for alias in {name, code}:
            ALIASES[_normalize(alias)] = code
        pt_name = TEAM_NAMES_PT.get(code)
        if pt_name:
            ALIASES[_normalize(pt_name)] = code

ALIASES.update({
    _normalize("Brazil"): "BRA",
    _normalize("Brasil"): "BRA",
    _normalize("Morocco"): "MAR",
    _normalize("Marrocos"): "MAR",
    _normalize("Mexico"): "MEX",
    _normalize("México"): "MEX",
    _normalize("South Africa"): "RSA",
    _normalize("Africa do Sul"): "RSA",
    _normalize("Korea Republic"): "KOR",
    _normalize("Coreia do Sul"): "KOR",
    _normalize("Chéquia"): "CZE",
    _normalize("Canadá"): "CAN",
    _normalize("Canada"): "CAN",
    _normalize("Bosnia & Herzegovina"): "BIH",
    _normalize("Bosnia and Herzegovina"): "BIH",
    _normalize("Bósnia e Herzegovina"): "BIH",
    _normalize("Estados Unidos"): "USA",
    _normalize("United States"): "USA",
    _normalize("Türkiye"): "TUR",
    _normalize("Turkey"): "TUR",
    _normalize("Turquia"): "TUR",
    _normalize("Curaçao"): "CUW",
    _normalize("Cote d'Ivoire"): "CIV",
    _normalize("Côte d'Ivoire"): "CIV",
    _normalize("Costa do Marfim"): "CIV",
    _normalize("Cape Verde"): "CPV",
    _normalize("Cabo Verde"): "CPV",
    _normalize("Congo DR"): "COD",
    _normalize("DR Congo"): "COD",
    _normalize("RD Congo"): "COD",
    _normalize("Saudi Arabia"): "KSA",
    _normalize("Arábia Saudita"): "KSA",
    _normalize("New Zealand"): "NZL",
    _normalize("Nova Zelândia"): "NZL",
    _normalize("South Africa"): "RSA",
    _normalize("Korea Republic"): "KOR",
    _normalize("África do Sul"): "RSA",
    _normalize("México"): "MEX",
    _normalize("Alemanha"): "GER",
    _normalize("Espanha"): "ESP",
    _normalize("França"): "FRA",
    _normalize("Argentina"): "ARG",
    _normalize("Brasil"): "BRA",
    _normalize("Inglaterra"): "ENG",
    _normalize("Croácia"): "CRO",
    _normalize("Panamá"): "PAN",
    _normalize("Gana"): "GHA",
})

KNOWN_MATCH_META = {
    ("MEX", "RSA"): {"date": "2026-06-11", "venue": "Mexico City, Mexico City - Mexico City Stadium"},
    ("CAN", "BIH"): {"date": "2026-06-12", "venue": "Toronto, Ontario - Toronto Stadium"},
    ("USA", "PAR"): {"date": "2026-06-12", "venue": "Los Angeles, California - Los Angeles Stadium"},
    ("BRA", "MAR"): {"date": "2026-06-13", "venue": "New York / New Jersey - New York New Jersey Stadium"},
    ("CUW", "GER"): {"date": "2026-06-14", "venue": "Houston, Texas - Houston Stadium"},
    ("ENG", "CRO"): {
        "date": "2026-06-17",
        "venue": "Dallas, Texas - Dallas Stadium",
    },
    ("BRA", "HAI"): {"date": "2026-06-19", "venue": "Philadelphia, Pennsylvania - Philadelphia Stadium"},
    ("TUN", "JPN"): {"date": "2026-06-20", "venue": "Monterrey, Nuevo León - Monterrey Stadium"},
    ("BRA", "SCO"): {"date": "2026-06-24", "venue": "Miami Gardens, Florida - Miami Stadium"},
}

_MATCH_META_CACHE = None

FIXTURE_RE = re.compile(
    r"((?:W\d{2,3})|(?:[12][A-Z])|(?:3\s+[A-Z]+)|(?:[A-Z]{3}))\s*v\s*((?:W\d{2,3})|(?:[12][A-Z])|(?:3\s+[A-Z]+)|(?:[A-Z]{3}))(?:\s+([A-Z]))?\s*(\d{1,3})\s*(\d{2}:\d{2})",
    re.M,
)
FIXTURE_FIXUPS = [
    {"home": "PAR", "away": "TUR", "group": "D", "match_number": 31, "kickoff_et": "23:00"},
    {"home": "IRQ", "away": "NOR", "group": "I", "match_number": 18, "kickoff_et": "18:00"},
    {"home": "COD", "away": "UZB", "group": "K", "match_number": 72, "kickoff_et": "19:30"},
    {"home": "L101", "away": "L102", "group": "", "match_number": 103, "kickoff_et": "17:00", "stage": "knockout"},
    {"home": "W101", "away": "W102", "group": "", "match_number": 104, "kickoff_et": "15:00", "stage": "knockout"},
]


def get_team(team_name):
    code = ALIASES.get(_normalize(team_name))
    if not code:
        return None
    return TEAM_DATA[code]


def is_worldcup_team(team_name):
    return get_team(team_name) is not None


def build_team_summary(team_name, locale="pt"):
    team = get_team(team_name)
    if not team:
        return None
    team = dict(team)
    team["type"] = "worldcup"

    fixtures = _team_fixtures(team["code"])
    now = datetime.now(timezone.utc)
    future = []
    for fixture in fixtures:
        fixture_dt = _fixture_datetime_utc(fixture)
        if fixture_dt is None or fixture_dt >= now:
            future.append(fixture)
    future.sort(key=lambda item: (item.get("date") or "9999-99-99", item["match_number"]))

    next_fixture = future[0] if future else (fixtures[0] if fixtures else None)
    previous = [fixture for fixture in fixtures if fixture is not next_fixture]
    previous.sort(key=lambda item: (item.get("date") or "0000-00-00", item["match_number"]), reverse=True)
    last_fixture = None
    for candidate in previous:
        candidate_dt = _fixture_datetime_utc(candidate)
        if candidate_dt and candidate_dt < now:
            last_fixture = candidate
            break

    return {
        "team": team,
        "matches": {
            "last": _format_fixture(last_fixture, locale=locale) if last_fixture else "N/A",
            "next": _format_fixture(next_fixture, locale=locale, include_venue=False) if next_fixture else "N/A",
            "next_venue": (_fixture_meta(next_fixture).get("venue") if next_fixture else None)
            or ("Indisponível" if locale == "pt" else "Unavailable"),
            "next_round": _group_round_number(team["code"], next_fixture),
            "broadcasts": _worldcup_broadcasts(next_fixture, locale=locale),
            "competition": COMPETITION_NAME,
            "competition_type": _competition_type(next_fixture),
            "competition_id": COMPETITION_ID,
        },
        "standings": format_group_table(team["code"], locale=locale),
    }


def format_group_table(team_code, locale="pt"):
    team = TEAM_DATA.get(team_code)
    if not team:
        return "posição não disponível" if locale == "pt" else "standing not available"

    group = team["group"]
    header_group, played, points, goal_diff = {
        "pt": ("Grupo", "PJ", "Pts", "SG"),
        "en": ("Group", "MP", "Pts", "GD"),
    }.get(locale, ("Grupo", "PJ", "Pts", "SG"))

    lines = [f"{header_group} {group}"]
    for idx, (name, code) in enumerate(GROUPS[group], start=1):
        marker = " <=" if code == team_code else ""
        lines.append(f"{idx}. {display_team_name(code, locale)} - 0 {played}, 0 {points}, 0 {goal_diff}{marker}")
    lines.append("")
    lines.append(_bracket_note(locale))
    return "\n".join(lines)


def get_phase_rules(locale="pt"):
    if locale == "en":
        return dict(PHASE_RULES)
    return {
        "group_stage": "48 seleções em 12 grupos. Avançam os 2 primeiros de cada grupo e os melhores terceiros até fechar a rodada de 32.",
        "round_of_32": "Rodada eliminatória com confrontos definidos por posição de grupo e melhores terceiros.",
        "round_of_16": "Oitavas de final com os 16 vencedores da rodada anterior.",
        "quarter_finals": "Quartas com os 8 classificados restantes.",
        "semi_finals": "Semifinais com 4 seleções.",
        "bronze_final": "Disputa de terceiro lugar entre os perdedores das semifinais.",
        "final": "Final única entre os vencedores das semifinais.",
    }


def _team_fixtures(team_code):
    fixtures = []
    for fixture in _load_fixtures():
        if team_code in (fixture["home_code"], fixture["away_code"]):
            fixtures.append(fixture)
    fixtures.sort(key=lambda item: item["match_number"])
    return fixtures


def _load_fixtures():
    fixtures = []
    if SCHEDULE_PATH.exists():
        raw = SCHEDULE_PATH.read_text(encoding="utf-8", errors="ignore")
        for home, away, group, match_number, kickoff_et in FIXTURE_RE.findall(raw):
            home = home.replace(" ", "")
            away = away.replace(" ", "")
            if home.startswith("3") and len(home) == 4 and home[1:] in TEAM_DATA:
                home = home[1:]
            if away.startswith("3") and len(away) == 4 and away[1:] in TEAM_DATA:
                away = away[1:]
            fixture = {
                "home_code": home,
                "away_code": away,
                "group": group or None,
                "match_number": int(match_number),
                "kickoff_et": kickoff_et,
                "stage": "group" if int(match_number) <= 72 else "knockout",
            }
            fixture.update(_fixture_meta(fixture))
            fixtures.append(fixture)

    existing = {(f["home_code"], f["away_code"], f["match_number"]) for f in fixtures}
    for extra in FIXTURE_FIXUPS:
        key = (extra["home"], extra["away"], extra["match_number"])
        if key not in existing:
            fixture = {
                "home_code": extra["home"],
                "away_code": extra["away"],
                "group": extra.get("group") or None,
                "match_number": extra["match_number"],
                "kickoff_et": extra["kickoff_et"],
                "stage": extra.get("stage") or ("group" if extra["match_number"] <= 72 else "knockout"),
            }
            fixture.update(_fixture_meta(fixture))
            fixtures.append(fixture)

    fixtures.sort(key=lambda item: item["match_number"])
    return fixtures


def _load_match_meta():
    global _MATCH_META_CACHE
    if _MATCH_META_CACHE is not None:
        return _MATCH_META_CACHE

    data = {}
    if MATCH_META_PATH.exists():
        try:
            data = json.loads(MATCH_META_PATH.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    _MATCH_META_CACHE = data
    return _MATCH_META_CACHE


def _fixture_meta(home, away=None):
    match_number = None
    if away is None and isinstance(home, dict):
        fixture = home
        home = fixture.get("home_code")
        away = fixture.get("away_code")
        match_number = fixture.get("match_number")

    meta = {}
    if match_number is not None:
        meta = _load_match_meta().get(str(match_number)) or {}

    if not meta:
        meta = KNOWN_MATCH_META.get((home, away)) or KNOWN_MATCH_META.get((away, home)) or {}

    return {"date": meta.get("date"), "venue": meta.get("venue")}


def _format_fixture(fixture, locale="pt", include_venue=True):
    if not fixture:
        return "N/A"

    home = display_team_name(fixture["home_code"], locale)
    away = display_team_name(fixture["away_code"], locale)
    text = f"{home} x {away}"
    kickoff = _format_kickoff(fixture, locale=locale)
    if kickoff != "N/A":
        text = f"{text}\n{kickoff}"
    if include_venue:
        venue = _fixture_meta(fixture).get("venue")
        if venue:
            text = f"{text}\n🏟️ {venue}"
    return text


def _format_kickoff(fixture, locale="pt"):
    if not fixture or not fixture.get("date") or not fixture.get("kickoff_et"):
        return "N/A"

    try:
        source_tz = ZoneInfo(SOURCE_TZ) if ZoneInfo else None
        if source_tz is None:
            return f"{fixture['date']} {fixture['kickoff_et']}"

        source_dt = datetime.fromisoformat(f"{fixture['date']}T{fixture['kickoff_et']}:00").replace(tzinfo=source_tz)
        local_dt = source_dt.astimezone(_local_timezone())
        utc_dt = source_dt.astimezone(timezone.utc)
        local_day = _weekday_name(local_dt.weekday(), locale)
        utc_day = _weekday_name(utc_dt.weekday(), "en")
        return f"{local_day}, {local_dt:%d/%m/%Y %H:%M} ({_timezone_label(local_dt)}) / {utc_day}, {utc_dt:%d/%m/%Y %H:%M} UTC"
    except Exception:
        return f"{fixture['date']} {fixture['kickoff_et']}"


def _fixture_datetime_utc(fixture):
    if not fixture or not fixture.get("date") or not fixture.get("kickoff_et"):
        return None
    try:
        source_tz = ZoneInfo(SOURCE_TZ) if ZoneInfo else None
        if source_tz is None:
            return None
        return datetime.fromisoformat(f"{fixture['date']}T{fixture['kickoff_et']}:00").replace(tzinfo=source_tz).astimezone(timezone.utc)
    except Exception:
        return None


def _group_round_number(team_code, fixture):
    if not fixture:
        return None
    fixtures = [item for item in _team_fixtures(team_code) if item["stage"] == "group"]
    fixtures.sort(key=lambda item: item["match_number"])
    for idx, item in enumerate(fixtures, start=1):
        if item["match_number"] == fixture["match_number"]:
            return idx
    return None


def _bracket_note(locale="pt"):
    if locale == "en":
        return "Knockout path: 1st/2nd places + best thirds enter the round of 32, then round of 16, quarter-finals, semi-finals, bronze final and final."
    return "Caminho eliminatório: 1º/2º lugares + melhores terceiros entram na rodada de 32, depois oitavas, quartas, semis, bronze e final."


def _worldcup_broadcasts(fixture, locale="pt"):
    if not fixture:
        return []

    if locale == "en":
        return ["CazéTV / YouTube"]

    return ["CazéTV / YouTube"]


def _local_timezone():
    if ZoneInfo:
        try:
            return ZoneInfo("America/Sao_Paulo")
        except Exception:
            pass
    return datetime.now().astimezone().tzinfo


def _timezone_label(dt):
    tzinfo = _local_timezone()
    label = getattr(tzinfo, "key", None)
    return label or dt.tzname() or "local"


def _weekday_name(weekday, locale="pt"):
    names = {
        "pt": ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"],
        "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    }
    return names.get(locale, names["pt"])[weekday]


def _normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.lower().strip())


def display_team_name(team_code, locale="pt"):
    team = TEAM_DATA.get(team_code)
    if not team:
        return team_code
    if locale == "pt":
        return TEAM_NAMES_PT.get(team_code, team["name"])
    return team["name"]


def display_team_heading(team_code, locale="pt"):
    flag = TEAM_FLAGS.get(team_code, "🏳️")
    return f"{flag}{display_team_name(team_code, locale)}"


def _competition_type(fixture):
    if not fixture:
        return "WORLD_CUP"

    stage = fixture.get("stage")
    if stage == "group":
        return "WORLD_CUP_GROUP"

    match_number = fixture.get("match_number") or 0
    if 73 <= match_number <= 88:
        return "WORLD_CUP_ROUND_OF_32"
    if 89 <= match_number <= 96:
        return "WORLD_CUP_ROUND_OF_16"
    if 97 <= match_number <= 100:
        return "WORLD_CUP_QUARTER_FINAL"
    if 101 <= match_number <= 102:
        return "WORLD_CUP_SEMI_FINAL"
    if match_number == 103:
        return "WORLD_CUP_BRONZE_FINAL"
    if match_number == 104:
        return "WORLD_CUP_FINAL"
    return "WORLD_CUP"
