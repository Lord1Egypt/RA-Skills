import re
import urllib.parse
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

TEAM_NEWS_QUERIES = {
    "pt": {
        "vasco": "Clube de Regatas Vasco da Gama futebol",
        "vasco da gama": "Clube de Regatas Vasco da Gama futebol",
        "chelsea": "Chelsea FC futebol",
        "chelsea fc": "Chelsea FC futebol",
        "bournemouth": "AFC Bournemouth futebol",
        "afc bournemouth": "AFC Bournemouth futebol",
    },
    "en": {
        "vasco": "Vasco da Gama football",
        "vasco da gama": "Vasco da Gama football",
        "chelsea": "Chelsea FC football",
        "chelsea fc": "Chelsea FC football",
        "bournemouth": "AFC Bournemouth football",
        "afc bournemouth": "AFC Bournemouth football",
    },
}

LOW_VALUE_NEWS = (
    "onde assistir",
    "where to watch",
    "horário",
    "schedule",
    "escalação",
    "prováveis escalações",
    "possible lineups",
    "lineup",
    "lineups",
    "preview",
    "palpite",
    "odds",
    "transmissão",
    "broadcast",
    "live stream",
    "match preview",
    "análise de jogo",
    "match analysis",
    "latest news",
    "rumours and gossip",
    "rumours",
    "gossip",
    "live updates",
    "highlights",
    "live blog",
    "live score",
    "scores",
    "results",
    "match centre",
    "transfer centre",
    "news now",
)

NON_FOOTBALL_NEWS = (
    "basquete",
    "basketball",
    "remo",
    "rowing",
    "volei",
    "vôlei",
    "volleyball",
    "futsal",
    "e-sports",
    "esports",
)

LOW_PRIORITY_TEAM_NEWS = (
    "sub-20",
    "sub20",
    "sub-17",
    "sub17",
    "base",
    "categorias de base",
    "academy",
    "women",
    "women's",
    "feminino",
)

PREFERRED_NEWS_SOURCES = (
    "ge",
    "vasco.com.br",
    "cbf",
    "ferj",
    "lance",
)

LOW_CREDIBILITY_SOURCES = (
    "vivente andante",
    "vascainos unidos",
    "vascofanatico",
    "vasconet",
    "vasconoticias",
)

SPECIFIC_NEWS_HINTS = (
    "signs",
    "signed",
    "signing",
    "joins",
    "joined",
    "join",
    "appoints",
    "appointed",
    "sacks",
    "sacked",
    "injury",
    "injured",
    "ruled out",
    "returns",
    "returned",
    "confirms",
    "confirmed",
    "report",
    "reports",
    "exclusive",
    "deal",
    "contract",
    "extension",
    "loan",
    "bid",
    "talks",
    "race",
    "boost",
    "reveals",
    "says",
    "insists",
    "set to",
    "close to",
    "considering",
    "opens talks",
    "picks up injury",
    "transfer",
    "transfers",
    "contrata",
    "contratado",
    "contratação",
    "contratacao",
    "convocado",
    "convocação",
    "convocacao",
    "oficializa",
    "lesão",
    "lesao",
    "retorna",
    "confirma",
    "negocia",
    "emprest",
    "renova",
    "revela",
)

GENERIC_SUMMARY_PATTERNS = (
    "comprehensive up-to-date news coverage",
    "aggregated from sources all over the world by google news",
    "google news",
    "latest news coverage",
    "coverage, aggregated from sources",
)


def canonical_team_query(team, locale="pt"):
    key = team.lower().strip()
    lang = "en" if locale == "en" else "pt"
    return TEAM_NEWS_QUERIES.get(lang, {}).get(key, f"{team} football" if lang == "en" else f"{team} futebol")


def get_news(team, locale="pt"):
    query = canonical_team_query(team, locale)
    if locale == "en":
        url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query + " football") + "&hl=en-US&gl=US&ceid=US:en"
    else:
        url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query + " futebol profissional") + "&hl=pt-BR&gl=BR&ceid=BR:pt-419"

    try:
        with urlopen(url, timeout=20) as resp:
            xml = resp.read().decode("utf-8", "ignore")
    except (HTTPError, URLError, ValueError, TimeoutError):
        return []

    primary_news = []
    secondary_news = []
    seen = set()
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)

    for item_xml in items:
        title = unescape(_extract_tag(item_xml, "title"))
        source = _extract_source(item_xml)
        rss_summary = unescape(_extract_tag(item_xml, "description"))
        rss_summary = _clean_summary(rss_summary)

        article_kind = _classify_article(team, title, source, rss_summary)
        if article_kind is None:
            continue

        summary = _clean_summary(rss_summary)
        if not summary or _is_generic_summary(summary) or not _has_specific_detail(summary):
            summary = _fallback_summary(title, locale=locale)

        key = _normalize_title(title)
        if key in seen:
            continue
        seen.add(key)

        item = {
            "title": title,
            "source": unescape(source),
            "summary": summary,
        }

        if article_kind == "secondary":
            secondary_news.append(item)
        else:
            primary_news.append(item)

    news_list = sorted(primary_news, key=lambda item: (_source_score(item.get("source", "")), item.get("title", "")))[:3]
    if len(news_list) < 3:
        secondary_news = sorted(secondary_news, key=lambda item: (_source_score(item.get("source", "")), item.get("title", "")))
        news_list.extend(secondary_news[: 3 - len(news_list)])

    return news_list


def _extract_tag(xml, tag):
    match = re.search(rf"<{tag}>(.*?)</{tag}>", xml, re.S)
    if not match:
        return ""
    return unescape(match.group(1).strip())


def _extract_source(xml):
    match = re.search(r"<source[^>]*>(.*?)</source>", xml, re.S)
    if not match:
        return ""
    return match.group(1).strip()


def _is_low_value_news(text):
    normalized = _normalize_text(text)
    return any(term in normalized for term in LOW_VALUE_NEWS)


def _is_non_football_news(text):
    normalized = _normalize_text(text)
    return any(term in normalized for term in NON_FOOTBALL_NEWS)


def _is_low_priority_team_news(text):
    normalized = _normalize_text(text)
    return any(term in normalized for term in LOW_PRIORITY_TEAM_NEWS)


def _source_score(source):
    raw = (source or "").strip().lower()
    if any(term in raw for term in LOW_CREDIBILITY_SOURCES):
        return 2
    if raw in PREFERRED_NEWS_SOURCES:
        return 0
    return 1


def _matches_team_context(team, title, source, summary):
    text = _normalize_text(f"{title} {source} {summary}")
    team_text = _normalize_text(team)

    aliases = {team_text}
    if "vasco" in team_text:
        aliases.update({"vasco", "vasco da gama", "cr vasco da gama"})
    elif "chelsea" in team_text:
        aliases.update({"chelsea", "chelsea fc"})
    elif "bournemouth" in team_text:
        aliases.update({"bournemouth", "afc bournemouth"})

    if not any(alias and alias in text for alias in aliases):
        return False

    if re.search(r"\bex\b", text) or "former" in text:
        return False

    return True


def _classify_article(team, title, source, summary):
    haystack = f"{title} {source} {summary}"
    if _is_low_value_news(haystack) or _is_non_football_news(haystack):
        return None

    if not _matches_team_context(team, title, source, summary):
        return None

    normalized_title = _normalize_text(title)
    if not normalized_title:
        return None

    if _looks_like_scoreline(normalized_title):
        return None

    if _looks_like_generic_hub(normalized_title, source, summary):
        return None

    is_secondary = _is_low_priority_team_news(haystack)

    if _has_specific_detail(title) or _has_specific_detail(summary):
        return "secondary" if is_secondary else "primary"

    # Keep some specific article headlines even when the feed summary is thin.
    words = normalized_title.split()
    if len(words) >= 6 and not _is_generic_headline(normalized_title):
        return "secondary" if is_secondary else "primary"

    return None


def _looks_like_generic_hub(title, source, summary):
    text = _normalize_text(f"{title} {source} {summary}")
    generic_terms = (
        "latest news",
        "rumours and gossip",
        "live updates",
        "goals and highlights",
        "where to watch",
        "match preview",
        "live blog",
        "live score",
        "match centre",
        "transfer centre",
        "results",
        "scores",
        "flashscore",
        "round-up",
        "round up",
    )
    generic_hits = sum(term in text for term in generic_terms)
    if generic_hits >= 1:
        return True

    if " - sky sports" in text and ("latest news" in text or "rumours" in text or "live" in text):
        return True

    return False


def _looks_like_scoreline(title):
    return bool(re.search(r"\b\d+\s*[:\-]\s*\d+\b", title)) and len(title.split()) <= 8


def _has_specific_detail(text):
    normalized = _normalize_text(text)
    return any(term in normalized for term in SPECIFIC_NEWS_HINTS)


def _is_generic_summary(text):
    if not text:
        return True

    normalized = _normalize_text(text)
    return any(term in normalized for term in GENERIC_SUMMARY_PATTERNS)


def _is_generic_headline(title):
    generic_terms = (
        "latest news",
        "rumours",
        "gossip",
        "live updates",
        "highlights",
        "scores",
        "results",
        "preview",
        "where to watch",
    )
    return any(term in title for term in generic_terms)


def _clean_summary(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:220]


def _fallback_summary(title, locale="pt"):
    if locale == "en":
        return f"Relevant club update with a specific development in the headline: {title}."
    return f"Atualização relevante do clube com um desdobramento específico no título: {title}."


def _normalize_title(text):
    return _normalize_text(text)


def _normalize_text(text):
    text = text.lower()
    text = re.sub(r"[\s\-–—]+", " ", text)
    text = re.sub(r"[^a-z0-9áàâãéêíóôõúçñ ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()
