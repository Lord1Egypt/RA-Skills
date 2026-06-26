import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from storage.user_config import get_api_key, set_api_key
from services.team_resolver import resolve_team
from services.football_api import get_matches, get_standings
from services.news_service import get_news
from services.worldcup_2026 import build_team_summary
from utils.formatter import format_team
from utils.cache import Cache

cache = Cache()
CONFIG_PATH = BASE_DIR / "config.json"
VERSION = "unknown"


def _load_version():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("version", "unknown")
    except Exception:
        return "unknown"


VERSION = _load_version()


def setup_message(locale="pt"):
    if locale == "en":
        return """
⚙️ Setup required

The skill only needs a valid football-data.org API key for club lookups.
National teams from the 2026 World Cup work without an API key.

set_api_key YOUR_KEY

You can send the key to me and I will finish the configuration for you.
"""

    return """
⚙️ Configuração necessária

A skill só precisa de uma API key válida do football-data.org para buscar clubes.
Seleções da Copa do Mundo 2026 funcionam sem API key.

set_api_key SUA_KEY

Você pode me enviar a chave e eu finalizo a configuração para você.
"""


def handle_input(text, user_id):

    text = text.strip()
    locale = _detect_locale(text)
    text = _strip_locale_tokens(text)

    # ----------------------------
    # 1. SETUP COMMAND
    # ----------------------------
    if text.startswith("set_api_key") or text.startswith("API_KEY:"):

        if text.startswith("set_api_key"):
            key = text.replace("set_api_key", "").strip()
        else:
            key = text.replace("API_KEY:", "").strip()

        set_api_key(user_id, key)

        return "✅ API_KEY configured successfully!" if locale == "en" else "✅ API_KEY configurada com sucesso!"

    # ----------------------------
    # 2. GET API KEY / PRE-RESOLVE TEAMS
    # ----------------------------
    api_key = get_api_key(user_id)
    teams = [t.strip() for t in text.split(",") if t.strip()]
    resolved_teams = []
    needs_api_key = False

    for team in teams:
        team_data = None
        try:
            team_data = resolve_team(team, api_key or "")
        except Exception:
            team_data = None

        if team_data is None:
            needs_api_key = True
        elif team_data.get("type") != "worldcup" and not api_key:
            needs_api_key = True

        resolved_teams.append((team, team_data))

    if needs_api_key and not api_key and not all((item[1] and item[1].get("type") == "worldcup") for item in resolved_teams):
        return setup_message(locale)

    # ----------------------------
    # 3. PROCESS TEAMS
    # ----------------------------

    results = []

    for team, team_data in resolved_teams:

        if team_data and team_data.get("type") == "worldcup":
            worldcup = build_team_summary(team_data["name"], locale=locale)
            if worldcup:
                matches = worldcup["matches"]
                standings = worldcup["standings"]
                news = get_news(f"{team_data['name']} World Cup 2026", locale=locale)
                results.append(
                    format_team(team_data, matches, standings, news, locale=locale, version=VERSION)
                )
                continue

        if team_data:
            team_id = team_data["id"]
            try:
                matches = cache.get_or_fetch(
                    f"matches_{team_id}",
                    lambda: get_matches(team_id, api_key, locale=locale)
                )
            except Exception:
                matches = {
                    "last": "N/A",
                    "next": "N/A",
                    "competition": "N/A",
                    "competition_id": None,
                }

            standings = get_standings(team_id, api_key, matches.get("competition_id"), locale=locale)
        else:
            team_data = {"id": None, "name": team}
            matches = {
                "last": "N/A",
                "next": "N/A",
                "competition": "N/A",
                "competition_id": None,
            }
            standings = "standing not available" if locale == "en" else "posição não disponível"

        news = get_news(team, locale=locale)

        results.append(
            format_team(team_data, matches, standings, news, locale=locale, version=VERSION)
        )

    return "\n━━━━━━━━━━━━━━\n".join(results)


def _detect_locale(text):
    lower = text.lower()

    for marker in ("locale=en", "lang=en", "language=en"):
        if marker in lower:
            return "en"
    for marker in ("locale=pt", "lang=pt", "language=pt", "locale=pt-br", "lang=pt-br"):
        if marker in lower:
            return "pt"

    english_markers = (
        "last match",
        "next match",
        "standings",
        "broadcast",
        "where to watch",
        "recent news",
        "kickoff",
    )
    portuguese_markers = (
        "último jogo",
        "proxima partida",
        "próxima partida",
        "posição",
        "transmissão",
        "notícias",
        "horário",
    )

    english_hits = sum(marker in lower for marker in english_markers)
    portuguese_hits = sum(marker in lower for marker in portuguese_markers)

    return "en" if english_hits > portuguese_hits else "pt"

def _strip_locale_tokens(text):
    cleaned = text
    for token in ("locale=en", "lang=en", "language=en", "locale=pt", "lang=pt", "language=pt", "locale=pt-br", "lang=pt-br", "language=pt-br"):
        cleaned = cleaned.replace(token, "")
    return " ".join(cleaned.split()).strip()
