"""Nederlands locale — nl.py"""

STRINGS = {
    # ── Algemeen ───────────────────────────────────────────────────────────
    "general.error":            "Fout",
    "general.no_trades":        "Geen trades in de afgelopen 30 dagen.",
    "general.na":               "N.v.t.",
    "general.unknown":          "Onbekend",
    "general.yes":              "Ja",
    "general.no":               "Nee",
    "general.goodbye":          "Tot ziens! Handel slim. 👋",
    "general.unknown_cmd":      "Onbekend commando: {cmd}. Typ 'help'.",
    "general.unauthorized":     "⛔ Geen toegang. Deze bot is privé.",

    # ── Taal ───────────────────────────────────────────────────────────────
    "lang.current":             "Huidige taal: {lang}",
    "lang.choose":              "🌐 Kies een taal:",
    "lang.set":                 "🌐 Taal ingesteld op Nederlands 🇳🇱",
    "lang.invalid":             "⚠️ Gebruik `/lang en` of `/lang nl`",
    "lang.switched":            "🌐 Taal gewisseld naar Nederlands.",

    # ── Markt ──────────────────────────────────────────────────────────────
    "market.title":             "{symbol} Marktoverzicht",
    "market.price":             "Prijs",
    "market.rsi":               "RSI",
    "market.trend":             "Trend",
    "market.sma50":             "SMA 50",
    "market.sma200":            "SMA 200",
    "market.ema21":             "EMA 21",
    "market.vs_sma200":         "t.o.v. SMA200",
    "market.fear_greed":        "Angst & Hebzucht",
    "market.trend.strong_up":   "sterke opgaande trend",
    "market.trend.recovering":  "herstellende",
    "market.trend.downtrend":   "neergaande trend",
    "market.trend.mixed":       "gemengd",
    "market.rsi.oversold":      "oververkocht",
    "market.rsi.overbought":    "overkocht",
    "market.rsi.neutral":       "neutraal",
    "market.rsi.neutral_high":  "neutraal-hoog",
    "market.rsi.neutral_low":   "neutraal-laag",

    # ── Portfolio ──────────────────────────────────────────────────────────
    "portfolio.title":          "Portfolio Gezondheid: {score}/100 (Cijfer: {grade})",
    "portfolio.total":          "Totale Waarde",
    "portfolio.stablecoins":    "Stablecoins",
    "portfolio.holdings":       "Significante posities",
    "portfolio.top_holdings":   "Top Posities",
    "portfolio.suggestions":    "💡 Suggesties",
    "portfolio.col.asset":      "Asset",
    "portfolio.col.amount":     "Hoeveelheid",
    "portfolio.col.usd":        "USD Waarde",
    "portfolio.col.pct":        "% van Portfolio",
    "portfolio.earn_suffix":    " (Sparen)",
    "portfolio.sug.diversify":  "Overweeg te diversifiëren — je hebt {n} significante posities. Streef naar 5–10.",
    "portfolio.sug.no_stable":  "Slechts {pct}% in stablecoins. Houd 10–30% achter de hand voor kansen.",
    "portfolio.sug.too_stable": "{pct}% stablecoins is veel — zit je te lang aan de zijlijn?",
    "portfolio.sug.conc_warn":  "Je grootste positie is {pct}% van je portfolio. Overweeg herbalanceren als >30%.",
    "portfolio.sug.conc_high":  "⚠️ Hoge concentratie: {asset} is {pct}% van je portfolio.",
    "portfolio.sug.conc_extreme": "🚨 Extreme concentratie: {asset} is {pct}%. Één slechte dag kan je portfolio verwoesten.",
    "portfolio.sug.bnb_chain":  "BNB chain tokens zijn {pct}% van portfolio — wat cross-chain diversificatie helpt.",
    "portfolio.sug.bnb_high":   "⚠️ {pct}% BNB chain blootstelling — overweeg diversificatie over meerdere blockchains.",
    "portfolio.sug.dust":       "Je hebt {n} stofposities (<$5). Ruim ze op via de 'Convert Dust' functie van Binance.",

    # ── DCA ────────────────────────────────────────────────────────────────
    "dca.title":                "Slimme DCA Aanbevelingen (Budget: ${budget}/mnd | Profiel: {profile})",
    "dca.col.symbol":           "Symbool",
    "dca.col.price":            "Prijs",
    "dca.col.rsi":              "RSI",
    "dca.col.fg":               "A&H",
    "dca.col.multiplier":       "Vermenigv.",
    "dca.col.weekly":           "Weeklijks Kopen",
    "dca.col.coins":            "Munten",
    "dca.col.vs_sma200":        "t.o.v. SMA200",
    "dca.why":                  "Waarom voor {symbol}:",
    "dca.profile.conservative": "Conservatief",
    "dca.profile.moderate":     "Gematigd",
    "dca.profile.aggressive":   "Agressief",
    "dca.reason.rsi_oversold":  "📉 RSI is {rsi} (oververkocht) — historisch gezien een goed aankoopmoment",
    "dca.reason.rsi_overbought":"📈 RSI is {rsi} (overkocht) — verklein positie, niet achternalopen",
    "dca.reason.rsi_neutral":   "📊 RSI is {rsi} (neutraal bereik)",
    "dca.reason.extreme_fear":  "😱 Extreme Angst ({fg}) — anderen paniekeren, overweeg meer te kopen",
    "dca.reason.extreme_greed": "🤑 Extreme Hebzucht ({fg}) — markten zijn euforisch, koop minder",
    "dca.reason.fg_neutral":    "😐 Angst & Hebzucht op {fg} ({label})",
    "dca.reason.deep_discount": "💎 Prijs is {pct}% onder 200-daags gemiddelde — historisch goedkoop",
    "dca.reason.premium":       "⚠️ Prijs is {pct}% boven 200-daags gemiddelde — dure zone",
    "dca.reason.below_sma50":   "📉 Onder 50-daags gemiddelde — kortetermijn neerwaartse trend, maar goed voor DCA",
    "dca.reason.increase":      "➡️ Aanbeveling: Meer DCA inzetten (×{mult})",
    "dca.reason.reduce":        "➡️ Aanbeveling: Minder DCA inzetten (×{mult})",
    "dca.reason.normal":        "➡️ Aanbeveling: Normaal DCA bedrag (×{mult})",
    "dca.projection.title":     "{symbol} — {months}-Maanden DCA Projectie",
    "dca.projection.invested":  "Totaal geïnvesteerd",
    "dca.projection.value":     "Verwachte waarde",
    "dca.projection.roi":       "Verwacht rendement",
    "dca.projection.note":      "Projectie gaat uit van 5% gem. maandelijkse groei. Crypto is volatiel — puur illustratief.",

    # ── Gedrag ─────────────────────────────────────────────────────────────
    "behavior.title":                   "Gedragsanalyse",
    "behavior.fomo":                    "FOMO Score",
    "behavior.overtrade":               "Overhandel Index",
    "behavior.overtrade.total":         "Trades afgelopen 30 dagen",
    "behavior.overtrade.week":          "Gem. per week",
    "behavior.overtrade.tip":           "Overweeg een 'doe niets' week. Studies tonen aan dat minder handelen betere rendementen oplevert.",
    "behavior.panic":                   "Paniekaanval Detector",
    "behavior.panic.none":              "✅ Geen recente paniekaanvallen gedetecteerd!",
    "behavior.panic.found":             "⚠️ Verkocht {symbol} voor ${sell} ({date}) — nu ${now} (+{pct}%)",
    "behavior.streaks":                 "🏆 Reeksen",
    "behavior.streak.no_panic":         "Geen paniekaanvallen",
    "behavior.streak.dca":              "DCA consistentie",
    "behavior.streak.days":             "{n} dagen",
    "behavior.streak.weeks":            "{n} weken",
    "behavior.fomo.label.low":          "Laag 🟢",
    "behavior.fomo.label.med":          "Gemiddeld 🟡",
    "behavior.fomo.label.high":         "Hoog 🔴",
    "behavior.fomo.fg":                 "Huidige A&H",
    "behavior.fomo.rapid":              "Snelle aankoopclusters (laatste 30d)",
    "behavior.overtrade.label.healthy": "Gezond 🟢",
    "behavior.overtrade.label.mod":     "Matig 🟡",
    "behavior.overtrade.label.high":    "Hoog ⚠️",
    "behavior.overtrade.label.over":    "Overhandelaar 🔴",

    # ── Meldingen ──────────────────────────────────────────────────────────
    "alert.set":                "✅ Melding ingesteld: {symbol} {condition} {threshold}",
    "alert.none":               "Geen actieve meldingen.",
    "alert.triggered_title":    "Melding: {symbol}",
    "alert.none_triggered":     "Geen meldingen geactiveerd.",
    "alert.col.symbol":         "Symbool",
    "alert.col.condition":      "Conditie",
    "alert.col.threshold":      "Drempelwaarde",
    "alert.col.created":        "Aangemaakt",
    "alert.col.notes":          "Notities",
    "alert.title":              "🔔 Actieve Meldingen",
    "alert.ctx.price_hit":      "Prijs bereikte *${value}* (jouw doel: ${threshold})\n\n",
    "alert.ctx.rsi_hit":        "RSI bereikte *{value}* (jouw doel: {threshold})\n\n",
    "alert.ctx.header":         "📊 *Marktcontext:*\n",
    "alert.ctx.meaning":        "🧠 *Wat dit betekent:*\n",
    "alert.ctx.rsi_ob_caution": "• Prijs brak door, maar RSI is overkocht — kan snel omkeren\n",
    "alert.ctx.greed_caution":  "• Doorbraak bij extreme hebzucht — wees voorzichtig, markt kan euforisch zijn\n",
    "alert.ctx.healthy_break":  "• Gezonde uitbraak boven jouw doel — trend lijkt bevestigd\n",
    "alert.ctx.above_sma200":   "• Prijs is boven 200-daags gemiddelde — langetermijn bullish signaal ✅\n",
    "alert.ctx.oversold_buy":   "• Gedaald naar jouw doel en RSI is oververkocht — mogelijke koopkans 💎\n",
    "alert.ctx.extreme_fear_buy": "• Extreme angst op de markt — historisch gezien goede aankoopzones\n",
    "alert.ctx.dropped":        "• Prijs daalde naar jouw niveau — beoordeel of de daling nieuws- of marktbreed is\n",
    "alert.ctx.below_sma200":   "• ⚠️ Onder 200-daags gemiddelde — langetermijn trend is bearish, wees voorzichtig\n",

    # ── Educatie ───────────────────────────────────────────────────────────
    "edu.not_found":            "Geen les gevonden voor onderwerp: {topic}",
    "edu.table.title":          "📚 Beschikbare Lessen",
    "edu.table.key":            "Onderwerp",
    "edu.table.title_col":      "Titel",

    # ── CLI ────────────────────────────────────────────────────────────────
    "cli.help": """
[bold]Commando's:[/bold]
  portfolio          — Analyseer je portfolio gezondheid
  dca [symbolen...]  — Slimme DCA aanbevelingen
  behavior           — Gedragsanalyse
  alert SYMBOOL COND WAARDE — Melding instellen (above/below/rsi_above/rsi_below)
  alerts             — Actieve meldingen bekijken
  check-alerts       — Handmatig meldingen controleren
  learn [onderwerp]  — Educatieve content
  market [symbool]   — Marktcontext voor een coin
  fg                 — Angst & Hebzucht index
  project [symbool]  — 12-maanden DCA projectie

[bold cyan]AI Commando's (Claude):[/bold cyan]
  coach              — AI coaching samenvatting van je portfolio
  weekly             — AI wekelijkse coaching brief
  ask <vraag>        — Stel Claude een vraag over je portfolio
  models             — Beschikbare Claude modellen
  model <id>         — Wissel van Claude model

[bold yellow]Instellingen:[/bold yellow]
  lang               — Beschikbare talen tonen
  lang en|nl         — Taal wisselen
  quit               — Afsluiten
""",
    "cli.analyzing":            "🔍 Portfolio analyseren...",
    "cli.fetching_dca":         "📐 DCA aanbevelingen ophalen voor {symbols}...",
    "cli.lang_switched":        "🌐 Taal gewisseld naar Nederlands.",
    "cli.lang_invalid":         "⚠️ Niet-ondersteunde taal. Gebruik: lang en  of  lang nl",
    "cli.lang_list":            "🌐 Beschikbare talen:\n{langs}\nGebruik: lang <code>",
    "cli.demo_mode":            "[bold cyan]Demo Modus[/bold cyan] — BinanceCoach mogelijkheden tonen",
    "cli.market_overview":      "📊 Marktoverzicht",
    "cli.today_lesson":         "📚 Les van vandaag:",
    "cli.dca_projection":       "📈 DCA Projectie (12 maanden, {symbol}):",
    "cli.fg_title":             "Angst & Hebzucht Index",
    "cli.fg_score":             "Score",
    "cli.fg_status":            "Status",
    "cli.fg_accumulate":        "Tijd om in te kopen! 💎",
    "cli.fg_careful":           "Minder kopen, wees voorzichtig 📉",
    "cli.fg_neutral":           "Neutraal gebied",
    "cli.no_api_warn":          "⚠️  Geen Binance API-sleutels gevonden. Alleen marktdata (geen portfolio).",

    # ── Telegram bot ───────────────────────────────────────────────────────
    "tg.start": (
        "👋 <b>BinanceCoach</b> — Jouw AI Handelsgedrag Coach\n\n"
        "<b>Standaard commando's:</b>\n"
        "/portfolio — Portfolio gezondheidsscore &amp; analyse\n"
        "/dca [BTCUSDT ETHUSDT] — Slimme DCA aanbevelingen\n"
        "/market [BTCUSDT] — Marktcontext voor een coin\n"
        "/fg — Angst &amp; Hebzucht index\n"
        "/alert BTCUSDT above 70000 — Prijsmelding instellen\n"
        "/alerts — Actieve meldingen bekijken\n"
        "/checkalerts — Meldingen controleren\n"
        "/behavior — Gedragsanalyse\n"
        "/project [BTCUSDT] — 12-maanden DCA projectie\n"
        "/learn [onderwerp] — Educatieve lessen\n\n"
        "<b>🤖 AI commando's (Claude):</b>\n"
        "/coach — AI coaching samenvatting van je portfolio\n"
        "/weekly — AI wekelijkse coaching brief\n"
        "/ask &lt;vraag&gt; — Stel Claude een vraag\n"
        "/models — Beschikbare Claude modellen\n"
        "/model &lt;id&gt; — Wissel van Claude model\n\n"
        "<b>Instellingen:</b>\n"
        "/lang — Taal kiezen 🌐\n"
    ),
    "tg.analyzing":             "🔍 Portfolio analyseren...",
    "tg.fetching_dca":          "📐 DCA aanbevelingen ophalen voor {symbols}...",
    "tg.alert_set": (
        "🔔 Melding ingesteld!\n<b>{symbol}</b> {condition} <b>{threshold}</b>\n\n"
        "Ik stuur je een melding met volledige marktcontext als het geactiveerd wordt."
    ),
    "tg.alert_usage":           "Gebruik: <code>/alert BTCUSDT above 70000</code> of <code>/alert BTCUSDT rsi_below 30</code>",
    "tg.lang_set":              "🌐 Taal ingesteld op Nederlands 🇳🇱",
    "tg.lang_invalid":          "⚠️ Gebruik <code>/lang en</code> of <code>/lang nl</code>",
    "tg.lang_choose":           "🌐 <b>Kies een taal:</b>",
    "tg.lang_no_args":          "Stuur <code>/lang en</code> of <code>/lang nl</code>, of tap een knop hieronder:",
    "tg.learn_list_suffix":     "\n\nGebruik: <code>/learn rsi_oversold</code>",
    "tg.learn_not_found":       "Onderwerp '{topic}' niet gevonden. Gebruik /learn voor de lijst.",
    "tg.fg_accumulate":         "Tijd om in te kopen! 💎",
    "tg.fg_careful":            "Minder kopen, wees voorzichtig 📉",
    "tg.fg_neutral":            "Neutraal gebied",
    "tg.dca_base":              "(Basis: ${base} × {mult})",
    "tg.dca_why":               "<b>Waarom:</b>\n",
    "tg.behavior.fomo":         "<b>FOMO Score:</b>",
    "tg.behavior.overtrade":    "<b>Overhandelen:</b>",
    "tg.behavior.panic":        "<b>Paniekaanval Check:</b>",
    "tg.ai.analyzing":          "🤖 Portfolio analyseren &amp; Claude aanroepen...",
    "tg.ai.weekly":             "🤖 Wekelijkse coaching brief genereren...",
    "tg.ai.asking":             "🤖 Claude raadplegen...",
    "tg.ai.no_key":             "⚠️ Anthropic API-sleutel niet ingesteld.\nVoeg <code>ANTHROPIC_API_KEY</code> toe aan je <code>.env</code> bestand.",
    "tg.ai.no_question":        "Gebruik: <code>/ask {example}</code>",
    "tg.ai.model_switched":     "✅ Model gewisseld naar: <code>{model}</code>",
    "tg.ai.model_usage":        "Gebruik: <code>/model claude-sonnet-4-6</code>\nZie /models voor alle opties.",
    "tg.ai.models_footer":      "Wisselen: <code>/model claude-sonnet-4-6</code>",
    "tg.ai.error":              "❌ AI fout: {error}",
    "tg.error":                 "❌ Fout: {error}",
    "tg.checking_alerts":       "🔍 Meldingen controleren...",
    "tg.bot_online":            "✅ Bot is online! Stuur /start voor het menu.",
}

LESSONS = {
    "rsi_oversold": {
        "title": "Wat betekent RSI Oververkocht?",
        "content": (
            "RSI (Relative Strength Index) onder 30 betekent dat een asset de afgelopen dagen zwaar verkocht is.\n\n"
            "Het betekent niet 'zeker kopen' — het betekent dat de verkoopdruk extreem was en een herstelbeweging statistisch waarschijnlijker is.\n\n"
            "📌 Kernpunten:\n"
            "• RSI < 30 = oververkocht (mogelijke kans)\n"
            "• RSI > 70 = overkocht (mogelijke top)\n"
            "• RSI alleen is geen koopsignaal — combineer met trend en volume\n"
            "• In sterke neerwaartse trends kan RSI wekenlang oververkocht blijven\n\n"
            "💡 Best practice: Combineer met Angst & Hebzucht, SMA-trends en je DCA-strategie."
        ),
    },
    "rsi_overbought": {
        "title": "Wat betekent RSI Overkocht?",
        "content": (
            "RSI boven 70 betekent dat de koopdruk de laatste tijd intensief was.\n\n"
            "Dit betekent niet 'alles verkopen' — in sterke bullmarkten kan RSI langdurig verhoogd blijven.\n\n"
            "📌 Kernpunten:\n"
            "• Overkocht betekent niet dat een crash aankomt\n"
            "• Het betekent dat het opwaartse momentum kan vertragen\n"
            "• Goed moment om: te stoppen met bijkopen, gedeeltelijke winst te nemen\n"
            "• Slecht moment om: FOMO-aankopen te doen op markttops"
        ),
    },
    "fear_greed": {
        "title": "De Angst & Hebzucht Index Uitgelegd",
        "content": (
            "De Crypto Angst & Hebzucht Index (0-100) meet het marktsentiment.\n\n"
            "• 0-25: Extreme Angst — mensen paniekeren\n"
            "• 25-45: Angst\n"
            "• 45-55: Neutraal\n"
            "• 55-75: Hebzucht\n"
            "• 75-100: Extreme Hebzucht — euforie / bubbel risico\n\n"
            "Warren Buffett: 'Wees bang als anderen hebzuchtig zijn, en hebzuchtig als anderen bang zijn.'\n\n"
            "📌 Hoe te gebruiken:\n"
            "• Extreme Angst (< 25): Overweeg DCA te verhogen\n"
            "• Extreme Hebzucht (> 75): Minder kopen, wat winst nemen\n"
            "• Gebruik het niet alleen — het is één signaal van velen"
        ),
    },
    "dca": {
        "title": "Dollar Cost Averaging (DCA) Uitgelegd",
        "content": (
            "DCA betekent het kopen van een vast bedrag met regelmatige tussenpozen, ongeacht de prijs.\n\n"
            "Waarom het werkt:\n"
            "• Je koopt meer munten als de prijzen laag zijn\n"
            "• Je koopt minder als de prijzen hoog zijn\n"
            "• Verwijdert emotionele besluitvorming\n"
            "• Je hoeft de markt niet perfect te timen\n\n"
            "📊 Voorbeeld — Koop elke week €100 aan BTC:\n"
            "• Week 1: BTC = €50.000 → 0,002 BTC\n"
            "• Week 2: BTC = €40.000 → 0,0025 BTC  ← Meer munten!\n"
            "• Week 3: BTC = €45.000 → 0,0022 BTC\n"
            "Gemiddelde kostprijs per munt < gemiddelde prijs over de periode ✅\n\n"
            "💡 Slimme DCA: Pas bedragen aan op basis van RSI en Angst & Hebzucht (precies wat BinanceCoach doet!)"
        ),
    },
    "sma_200": {
        "title": "Het 200-Daags Voortschrijdend Gemiddelde",
        "content": (
            "Het 200-daags SMA is een van de meest gevolgde indicatoren door institutionele beleggers.\n\n"
            "Het vertegenwoordigt de gemiddelde prijs over de laatste 200 dagen.\n\n"
            "📌 Wat het je vertelt:\n"
            "• Prijs boven 200d SMA = langetermijn opgaande trend (bullmarkt)\n"
            "• Prijs onder 200d SMA = langetermijn neergaande trend (bearmarkt)\n"
            "• 'Gouden Kruis': 50d SMA kruist boven 200d SMA → bullish signaal\n"
            "• 'Doodskruis': 50d SMA kruist onder 200d SMA → bearish signaal\n\n"
            "Hoe BinanceCoach het gebruikt:\n"
            "• Prijs 20%+ onder SMA200 → historisch gezien goede aankoopzone\n"
            "• Prijs 30%+ boven SMA200 → markt kan uitgerekt zijn, minder kopen"
        ),
    },
    "concentration_risk": {
        "title": "Wat is Concentratierisico?",
        "content": (
            "Concentratierisico is wanneer te veel van je portfolio in één asset zit.\n\n"
            "Voorbeeld: Als 80% van je portfolio BTC is en BTC daalt 50%, verlies je 40% van je totale vermogen.\n\n"
            "📌 Algemene richtlijnen:\n"
            "• Geen enkele positie > 30-40% van het totale portfolio\n"
            "• Houd 5-10 verschillende assets aan voor betekenisvolle diversificatie\n"
            "• Stablecoins (10-30%) fungeren als reserve voor kansen\n"
            "• Diversifieer over blockchains (BNB, Ethereum, Solana, etc.)\n\n"
            "⚠️ Onthoud: Diversificatie elimineert risico niet — het verdeelt het."
        ),
    },
    "panic_selling": {
        "title": "Waarom Paniekaanvallen Rendementen Vernietigen",
        "content": (
            "Paniekaanvallen zijn wanneer angst je drijft om met verlies te verkopen — vaak vlak voor een herstel.\n\n"
            "💀 Het patroon:\n"
            "1. Prijs daalt → je voelt angst\n"
            "2. Je verkoopt om 'de bloeding te stoppen'\n"
            "3. Prijs herstelt → je koopt terug op een hoger niveau\n"
            "4. Herhaal totdat portfolio vernietigd is\n\n"
            "✅ Hoe te stoppen:\n"
            "• Stel je 'verkoopregels' vooraf in, voordat emoties de kop opsteken\n"
            "• Gebruik DCA om systematisch te blijven\n"
            "• Onthoud: Volatiliteit is de prijs die je betaalt voor crypto rendementen\n"
            "• Als je niet kunt slapen, is je positiegrootte te groot"
        ),
    },
}
