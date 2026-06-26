from services.worldcup_2026 import display_team_heading

LABELS = {
    "pt": {
        "last_match": "🏟️ Último jogo:",
        "next_match": "📅 Próxima partida:",
        "round": "🔁 Rodada:",
        "kickoff": "⏰ Horário do jogo:",
        "venue": "🏟️ Estado/Cidade da próxima partida:",
        "broadcasts": "📺 Transmissão:",
        "competition": "🏆 Campeonato:",
        "standings": "📊 Posição:",
        "news": "📰 Últimas notícias:",
        "no_news": "• Sem notícias recentes",
        "no_broadcasts": "• Indisponível",
        "no_venue": "• Indisponível",
    },
    "en": {
        "last_match": "🏟️ Last match:",
        "next_match": "📅 Next match:",
        "round": "🔁 Round:",
        "kickoff": "⏰ Kickoff:",
        "venue": "🏟️ Next venue (state/city):",
        "broadcasts": "📺 Broadcast:",
        "competition": "🏆 Competition:",
        "standings": "📊 Standing:",
        "news": "📰 Recent news:",
        "no_news": "• No recent news",
        "no_broadcasts": "• Unavailable",
        "no_venue": "• Unavailable",
    },
}

FOOTERS = {
    "pt": "**Esta skill ainda está em fase beta de desenvolvimento e pode apresentar erros. Verifique as atualizações.**\nVersão atual: `{version}` (As próximas atualizações serão focadas na copa do mundo 2026)",
    "en": "**This skill is still in beta development and may have errors. Check for updates.**\nCurrent version: `{version}` (The next updates will focus on the 2026 World Cup)",
}


def format_team(team, matches, standings, news, locale="pt", version="unknown"):
    labels = LABELS.get(locale, LABELS["pt"])
    footer = FOOTERS.get(locale, FOOTERS["pt"]).format(version=version)
    venue_block = ""
    if matches.get("next_venue") is not None:
        venue_value = matches.get("next_venue") or labels["no_venue"].lstrip("• ").strip()
        venue_block = f"{labels['venue']}\n{venue_value}\n\n"
    display_name = team.get("name", "N/A")
    if team.get("type") == "worldcup" and team.get("code"):
        display_name = display_team_heading(team["code"], locale)
    return f"""{display_name}

{labels['last_match']}
{matches['last']}

{labels['next_match']}
{matches['next']}

{venue_block}

{labels['round']}
{format_round(matches.get('next_round'), matches.get('competition_type'), locale=locale)}

{labels['broadcasts']}
{format_broadcasts(matches.get('broadcasts', []), locale=locale)}

{labels['competition']}
{matches['competition']}

{labels['standings']}
{standings}

{labels['news']}
{format_news(news, locale=locale)}

{footer}
"""


def format_news(news, locale="pt"):
    labels = LABELS.get(locale, LABELS["pt"])

    if not news:
        return labels["no_news"]

    lines = []
    for idx, n in enumerate(news):
        lines.append(f"• **{n['title']}**")
        source = (n.get("source") or "").strip()
        if source:
            lines.append(f"  *Fonte:* {source}")
        summary = (n.get("summary") or "").strip()
        if summary:
            lines.append(f"  **Resumo:** {summary}")
        if idx < len(news) - 1:
            lines.append("")

    return "\n".join(lines)


def format_broadcasts(broadcasts, locale="pt"):
    labels = LABELS.get(locale, LABELS["pt"])

    if not broadcasts:
        return labels["no_broadcasts"]

    return "\n".join(f"• {item}" for item in broadcasts)


def format_round(round_number, competition_type, locale="pt"):
    if competition_type == "WORLD_CUP_GROUP" and round_number not in (None, ""):
        if locale == "en":
            return f"Group stage - Round {round_number}"
        return f"Fase de grupos - Rodada {round_number}"

    world_cup_round_labels = {
        "WORLD_CUP_ROUND_OF_32": {"pt": "Rodada de 32", "en": "Round of 32"},
        "WORLD_CUP_ROUND_OF_16": {"pt": "Oitavas de final", "en": "Round of 16"},
        "WORLD_CUP_QUARTER_FINAL": {"pt": "Quartas de final", "en": "Quarter-finals"},
        "WORLD_CUP_SEMI_FINAL": {"pt": "Semifinais", "en": "Semi-finals"},
        "WORLD_CUP_BRONZE_FINAL": {"pt": "Disputa de 3º lugar", "en": "Bronze final"},
        "WORLD_CUP_FINAL": {"pt": "Final", "en": "Final"},
    }

    if competition_type in world_cup_round_labels:
        return world_cup_round_labels[competition_type].get(locale, world_cup_round_labels[competition_type]["pt"])

    if competition_type != "LEAGUE" or round_number in (None, ""):
        return "N/A"

    if locale == "en":
        return f"Round {round_number}"

    return f"Rodada {round_number}"
