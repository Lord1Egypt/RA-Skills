import json
import unicodedata
from urllib.parse import quote
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from pathlib import Path
import re
from services.worldcup_2026 import get_team as get_worldcup_team


BASE_URL = "https://api.football-data.org/v4"
BASE_DIR = Path(__file__).resolve().parent.parent
TEAMS_PATH = BASE_DIR / "storage" / "teams.json"
COMPETITION_HINTS = {
    "vasco": ("BSA", "Vasco da Gama"),
    "vasco da gama": ("BSA", "Vasco da Gama"),
    "cr vasco da gama": ("BSA", "Vasco da Gama"),
    "clube de regatas vasco da gama": ("BSA", "Vasco da Gama"),
    "c.r. vasco da gama": ("BSA", "Vasco da Gama"),
    "coritiba": ("BSA", "Coritiba FBC"),
    "coritiba fbc": ("BSA", "Coritiba FBC"),
    "chapecoense": ("BSA", "Chapecoense AF"),
    "chapecoense af": ("BSA", "Chapecoense AF"),
    "santos": ("BSA", "Santos FC"),
    "santos fc": ("BSA", "Santos FC"),
    "sao paulo": ("BSA", "São Paulo FC"),
    "são paulo": ("BSA", "São Paulo FC"),
    "sao paulo fc": ("BSA", "São Paulo FC"),
    "são paulo fc": ("BSA", "São Paulo FC"),
    "chelsea": ("PL", "Chelsea FC"),
    "chelsea fc": ("PL", "Chelsea FC"),
    "bournemouth": ("PL", "AFC Bournemouth"),
    "afc bournemouth": ("PL", "AFC Bournemouth"),
}


def _get_json(url, api_key, timeout=20):
    req = Request(url, headers={"X-Auth-Token": api_key})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _resolve_from_competition(team_name, api_key):
    key = team_name.lower().strip()
    hint = COMPETITION_HINTS.get(key)
    if not hint:
        return None

    competition_code, target_name = hint
    url = f"{BASE_URL}/competitions/{competition_code}/teams"

    try:
        data = _get_json(url, api_key)
    except (HTTPError, URLError, ValueError):
        return None

    for team in data.get("teams", []):
        name = team.get("name", "")
        short = team.get("shortName", "")
        normalized_name = _normalize(name)
        normalized_short = _normalize(short)
        normalized_target = _normalize(target_name)
        if (
            normalized_target in normalized_name
            or normalized_target in normalized_short
            or normalized_name in normalized_target
            or normalized_short in normalized_target
            or key in normalized_name
            or key in normalized_short
        ):
            return {
                "id": team["id"],
                "name": name,
            }

    return None


def _resolve_from_api(team_name, api_key):
    target = _normalize(team_name)
    offset = 0
    limit = 100
    total = None

    while True:
        url = f"{BASE_URL}/teams?limit={limit}&offset={offset}"
        try:
            data = _get_json(url, api_key)
        except (HTTPError, URLError, ValueError):
            return None

        teams = data.get("teams", [])
        if not teams:
            return None

        for team in teams:
            name = team.get("name", "")
            short = team.get("shortName", "")
            tla = team.get("tla", "")
            if target in _normalize(name) or target in _normalize(short) or target == _normalize(tla):
                return {
                    "id": team["id"],
                    "name": name,
                }

        if total is None:
            total = data.get("count")
        offset += limit
        if total is not None and offset >= total:
            break

    return None

def load_local():
    try:
        with open(TEAMS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_local(data):
    with open(TEAMS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def resolve_team(name, api_key):

    worldcup = get_worldcup_team(name)
    if worldcup:
        return {
            "id": f"worldcup-{worldcup['code']}",
            "name": worldcup["name"],
            "code": worldcup["code"],
            "group": worldcup["group"],
            "type": "worldcup",
        }

    teams = load_local()

    key = _normalize(name)

    if key in teams:
        return {"id": teams[key], "name": name}

    hinted = _resolve_from_competition(name, api_key)
    if hinted:
        teams[key] = hinted["id"]
        save_local(teams)
        return hinted

    discovered = _resolve_from_api(name, api_key)
    if discovered:
        teams[key] = discovered["id"]
        save_local(teams)
        return discovered

    return None


def _normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.lower().strip())
