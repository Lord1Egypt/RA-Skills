"""English locale — en.py"""

STRINGS = {
    # ── General ────────────────────────────────────────────────────────────
    "general.error":            "Error",
    "general.no_trades":        "No trades in last 30 days.",
    "general.na":               "N/A",
    "general.unknown":          "Unknown",
    "general.yes":              "Yes",
    "general.no":               "No",
    "general.goodbye":          "Goodbye! Trade smart. 👋",
    "general.unknown_cmd":      "Unknown command: {cmd}. Type 'help'.",
    "general.unauthorized":     "⛔ Unauthorized. This bot is private.",

    # ── Language ───────────────────────────────────────────────────────────
    "lang.current":             "Current language: {lang}",
    "lang.choose":              "🌐 Choose a language:",
    "lang.set":                 "🌐 Language set to English 🇬🇧",
    "lang.invalid":             "⚠️ Use `/lang en` or `/lang nl`",
    "lang.switched":            "🌐 Language switched to English.",

    # ── Market ─────────────────────────────────────────────────────────────
    "market.title":             "{symbol} Market Context",
    "market.price":             "Price",
    "market.rsi":               "RSI",
    "market.trend":             "Trend",
    "market.sma50":             "SMA 50",
    "market.sma200":            "SMA 200",
    "market.ema21":             "EMA 21",
    "market.vs_sma200":         "vs SMA200",
    "market.fear_greed":        "Fear & Greed",
    "market.trend.strong_up":   "strong uptrend",
    "market.trend.recovering":  "recovering",
    "market.trend.downtrend":   "downtrend",
    "market.trend.mixed":       "mixed",
    "market.rsi.oversold":      "oversold",
    "market.rsi.overbought":    "overbought",
    "market.rsi.neutral":       "neutral",
    "market.rsi.neutral_high":  "neutral-high",
    "market.rsi.neutral_low":   "neutral-low",

    # ── Portfolio ──────────────────────────────────────────────────────────
    "portfolio.title":          "Portfolio Health: {score}/100 (Grade: {grade})",
    "portfolio.total":          "Total Value",
    "portfolio.stablecoins":    "Stablecoins",
    "portfolio.holdings":       "Meaningful holdings",
    "portfolio.top_holdings":   "Top Holdings",
    "portfolio.suggestions":    "💡 Suggestions",
    "portfolio.col.asset":      "Asset",
    "portfolio.col.amount":     "Amount",
    "portfolio.col.usd":        "USD Value",
    "portfolio.col.pct":        "% of Portfolio",
    "portfolio.earn_suffix":    " (Earn)",
    "portfolio.sug.diversify":  "Consider diversifying — you have {n} meaningful holdings. Aim for 5–10.",
    "portfolio.sug.no_stable":  "Only {pct}% in stablecoins. Keep 10–30% as dry powder for opportunities.",
    "portfolio.sug.too_stable": "{pct}% stablecoins is high — are you sitting on the sidelines too long?",
    "portfolio.sug.conc_warn":  "Your top holding is {pct}% of portfolio. Consider rebalancing if >30%.",
    "portfolio.sug.conc_high":  "⚠️ High concentration: {asset} is {pct}% of your portfolio.",
    "portfolio.sug.conc_extreme": "🚨 Extreme concentration: {asset} is {pct}%. One bad day can wipe you.",
    "portfolio.sug.bnb_chain":  "BNB chain tokens are {pct}% of portfolio — some cross-chain diversification helps.",
    "portfolio.sug.bnb_high":   "⚠️ {pct}% BNB chain exposure — consider diversifying across chains.",
    "portfolio.sug.dust":       "You have {n} dust positions (<$5). Clean them up with Binance's Convert Dust feature.",

    # ── DCA ────────────────────────────────────────────────────────────────
    "dca.title":                "Smart DCA Recommendations (Budget: ${budget}/mo | Profile: {profile})",
    "dca.col.symbol":           "Symbol",
    "dca.col.price":            "Price",
    "dca.col.rsi":              "RSI",
    "dca.col.fg":               "F&G",
    "dca.col.multiplier":       "Multiplier",
    "dca.col.weekly":           "Weekly Buy",
    "dca.col.coins":            "Coins",
    "dca.col.vs_sma200":        "vs SMA200",
    "dca.why":                  "Why for {symbol}:",
    "dca.profile.conservative": "Conservative",
    "dca.profile.moderate":     "Moderate",
    "dca.profile.aggressive":   "Aggressive",
    "dca.reason.rsi_oversold":  "📉 RSI is {rsi} (oversold) — historically a good accumulation zone",
    "dca.reason.rsi_overbought":"📈 RSI is {rsi} (overbought) — reduce size, don't chase",
    "dca.reason.rsi_neutral":   "📊 RSI is {rsi} (neutral range)",
    "dca.reason.extreme_fear":  "😱 Extreme Fear ({fg}) — others are panicking, consider buying more",
    "dca.reason.extreme_greed": "🤑 Extreme Greed ({fg}) — markets are euphoric, scale back buys",
    "dca.reason.fg_neutral":    "😐 Fear & Greed at {fg} ({label})",
    "dca.reason.deep_discount": "💎 Price is {pct}% below 200-day SMA — historically discounted",
    "dca.reason.premium":       "⚠️ Price is {pct}% above 200-day SMA — premium territory",
    "dca.reason.below_sma50":   "📉 Below 50-day SMA — short-term downtrend, but good for DCA",
    "dca.reason.increase":      "➡️ Recommendation: Increase DCA (×{mult})",
    "dca.reason.reduce":        "➡️ Recommendation: Reduce DCA (×{mult})",
    "dca.reason.normal":        "➡️ Recommendation: Normal DCA (×{mult})",
    "dca.projection.title":     "{symbol} — {months}-Month DCA Projection",
    "dca.projection.invested":  "Total invested",
    "dca.projection.value":     "Projected value",
    "dca.projection.roi":       "Projected ROI",
    "dca.projection.note":      "Projection assumes 5% avg monthly growth. Crypto is volatile — illustrative only.",

    # ── Behavior ───────────────────────────────────────────────────────────
    "behavior.title":                   "Behavioral Analysis",
    "behavior.fomo":                    "FOMO Score",
    "behavior.overtrade":               "Overtrading Index",
    "behavior.overtrade.total":         "Trades last 30d",
    "behavior.overtrade.week":          "Avg per week",
    "behavior.overtrade.tip":           "Consider a 'do nothing' week. Studies show reducing trade frequency improves returns.",
    "behavior.panic":                   "Panic Sell Detector",
    "behavior.panic.none":              "✅ No recent panic sells detected!",
    "behavior.panic.found":             "⚠️ Sold {symbol} at ${sell} ({date}) — now ${now} (+{pct}%)",
    "behavior.streaks":                 "🏆 Streaks",
    "behavior.streak.no_panic":         "No panic sells",
    "behavior.streak.dca":              "DCA consistency",
    "behavior.streak.days":             "{n} days",
    "behavior.streak.weeks":            "{n} weeks",
    "behavior.fomo.label.low":          "Low 🟢",
    "behavior.fomo.label.med":          "Medium 🟡",
    "behavior.fomo.label.high":         "High 🔴",
    "behavior.fomo.fg":                 "Current F&G",
    "behavior.fomo.rapid":              "Rapid buy clusters (last 30d)",
    "behavior.overtrade.label.healthy": "Healthy 🟢",
    "behavior.overtrade.label.mod":     "Moderate 🟡",
    "behavior.overtrade.label.high":    "High ⚠️",
    "behavior.overtrade.label.over":    "Overtrader 🔴",

    # ── Alerts ─────────────────────────────────────────────────────────────
    "alert.set":                "✅ Alert set: {symbol} {condition} {threshold}",
    "alert.none":               "No active alerts.",
    "alert.triggered_title":    "Alert: {symbol}",
    "alert.none_triggered":     "No alerts triggered.",
    "alert.col.symbol":         "Symbol",
    "alert.col.condition":      "Condition",
    "alert.col.threshold":      "Threshold",
    "alert.col.created":        "Created",
    "alert.col.notes":          "Notes",
    "alert.title":              "🔔 Active Alerts",
    "alert.ctx.price_hit":      "Price hit *${value}* (your target: ${threshold})\n\n",
    "alert.ctx.rsi_hit":        "RSI hit *{value}* (your target: {threshold})\n\n",
    "alert.ctx.header":         "📊 *Market Context:*\n",
    "alert.ctx.meaning":        "🧠 *What this means:*\n",
    "alert.ctx.rsi_ob_caution": "• Price broke through, but RSI is overbought — could reverse soon\n",
    "alert.ctx.greed_caution":  "• Breaking above with extreme greed — be cautious, market may be euphoric\n",
    "alert.ctx.healthy_break":  "• Healthy breakout above your target — trend looks confirmed\n",
    "alert.ctx.above_sma200":   "• Price is above 200-day SMA — long-term bullish signal ✅\n",
    "alert.ctx.oversold_buy":   "• Dropped to your target and RSI is oversold — potential buying opportunity 💎\n",
    "alert.ctx.extreme_fear_buy": "• Extreme fear in the market — historically good accumulation zones\n",
    "alert.ctx.dropped":        "• Price dropped to your level — evaluate if drop is news-driven or market-wide\n",
    "alert.ctx.below_sma200":   "• ⚠️ Below 200-day SMA — long-term trend is bearish, size positions carefully\n",

    # ── Education ──────────────────────────────────────────────────────────
    "edu.not_found":            "No lesson found for topic: {topic}",
    "edu.table.title":          "📚 Available Lessons",
    "edu.table.key":            "Topic Key",
    "edu.table.title_col":      "Title",

    # ── CLI ────────────────────────────────────────────────────────────────
    "cli.help": """
[bold]Commands:[/bold]
  portfolio          — Analyze your portfolio health
  dca [symbols...]   — Smart DCA recommendations
  behavior           — Behavioral bias analysis
  alert SYMBOL COND VALUE  — Set alert (above/below/rsi_above/rsi_below)
  alerts             — List active alerts
  check-alerts       — Manually check if any alerts triggered
  learn [topic]      — Educational content
  market [symbol]    — Market context for a symbol
  fg                 — Fear & Greed index
  project [symbol]   — 12-month DCA projection

[bold cyan]AI Commands (Claude):[/bold cyan]
  coach              — AI coaching summary of your portfolio
  weekly             — AI weekly coaching brief
  ask <question>     — Ask Claude anything about your portfolio
  models             — List available Claude models
  model <id>         — Switch active Claude model

[bold yellow]Settings:[/bold yellow]
  lang               — Show available languages
  lang en|nl         — Switch language
  quit               — Exit
""",
    "cli.analyzing":            "🔍 Analyzing your portfolio...",
    "cli.fetching_dca":         "📐 Getting DCA recommendations for {symbols}...",
    "cli.lang_switched":        "🌐 Language switched to English.",
    "cli.lang_invalid":         "⚠️ Unsupported language. Use: lang en  or  lang nl",
    "cli.lang_list":            "🌐 Available languages:\n{langs}\nUsage: lang <code>",
    "cli.demo_mode":            "[bold cyan]Demo Mode[/bold cyan] — Showing BinanceCoach capabilities",
    "cli.market_overview":      "📊 Market Overview",
    "cli.today_lesson":         "📚 Today's Lesson:",
    "cli.dca_projection":       "📈 DCA Projection (12 months, {symbol}):",
    "cli.fg_title":             "Fear & Greed Index",
    "cli.fg_score":             "Score",
    "cli.fg_status":            "Status",
    "cli.fg_accumulate":        "Time to accumulate! 💎",
    "cli.fg_careful":           "Reduce buys, be careful 📉",
    "cli.fg_neutral":           "Neutral territory",
    "cli.no_api_warn":          "⚠️  No Binance API keys found. Market data only (no portfolio).",

    # ── Telegram bot ───────────────────────────────────────────────────────
    "tg.start": (
        "👋 <b>BinanceCoach</b> — Your AI Trading Behavior Coach\n\n"
        "<b>Standard commands:</b>\n"
        "/portfolio — Portfolio health score &amp; analysis\n"
        "/dca [BTCUSDT ETHUSDT] — Smart DCA recommendations\n"
        "/market [BTCUSDT] — Market context for a coin\n"
        "/fg — Fear &amp; Greed index\n"
        "/alert BTCUSDT above 70000 — Set a price alert\n"
        "/alerts — List active alerts\n"
        "/checkalerts — Check if any alert triggered\n"
        "/behavior — Behavioral bias analysis\n"
        "/project [BTCUSDT] — 12-month DCA projection\n"
        "/learn [topic] — Educational lessons\n\n"
        "<b>🤖 AI commands (Claude):</b>\n"
        "/coach — AI coaching summary of your portfolio\n"
        "/weekly — AI weekly coaching brief\n"
        "/ask &lt;question&gt; — Ask Claude anything\n"
        "/models — List available Claude models\n"
        "/model &lt;id&gt; — Switch Claude model\n\n"
        "<b>Settings:</b>\n"
        "/lang — Choose language 🌐\n"
    ),
    "tg.analyzing":             "🔍 Analyzing your portfolio...",
    "tg.fetching_dca":          "📐 Getting DCA recommendations for {symbols}...",
    "tg.alert_set": (
        "🔔 Alert set!\n<b>{symbol}</b> {condition} <b>{threshold}</b>\n\n"
        "I'll notify you with full market context when triggered."
    ),
    "tg.alert_usage":           "Usage: <code>/alert BTCUSDT above 70000</code> or <code>/alert BTCUSDT rsi_below 30</code>",
    "tg.lang_set":              "🌐 Language set to English 🇬🇧",
    "tg.lang_invalid":          "⚠️ Use <code>/lang en</code> or <code>/lang nl</code>",
    "tg.lang_choose":           "🌐 <b>Choose a language:</b>",
    "tg.lang_no_args":          "Send <code>/lang en</code> or <code>/lang nl</code>, or tap a button below:",
    "tg.learn_list_suffix":     "\n\nUse: <code>/learn rsi_oversold</code>",
    "tg.learn_not_found":       "Topic '{topic}' not found. Use /learn for list.",
    "tg.fg_accumulate":         "Time to accumulate! 💎",
    "tg.fg_careful":            "Reduce buys, be careful 📉",
    "tg.fg_neutral":            "Neutral territory",
    "tg.dca_base":              "(Base: ${base} × {mult})",
    "tg.dca_why":               "<b>Why:</b>\n",
    "tg.behavior.fomo":         "<b>FOMO Score:</b>",
    "tg.behavior.overtrade":    "<b>Overtrading:</b>",
    "tg.behavior.panic":        "<b>Panic Sell Check:</b>",
    "tg.ai.analyzing":          "🤖 Analysing portfolio &amp; calling Claude...",
    "tg.ai.weekly":             "🤖 Generating weekly coaching brief...",
    "tg.ai.asking":             "🤖 Asking Claude...",
    "tg.ai.no_key":             "⚠️ Anthropic API key not configured.\nAdd <code>ANTHROPIC_API_KEY</code> to your <code>.env</code> file.",
    "tg.ai.no_question":        "Usage: <code>/ask {example}</code>",
    "tg.ai.model_switched":     "✅ Model switched to: <code>{model}</code>",
    "tg.ai.model_usage":        "Usage: <code>/model claude-sonnet-4-6</code>\nSee /models for all options.",
    "tg.ai.models_footer":      "Switch: <code>/model claude-sonnet-4-6</code>",
    "tg.ai.error":              "❌ AI error: {error}",
    "tg.error":                 "❌ Error: {error}",
    "tg.checking_alerts":       "🔍 Checking alerts...",
    "tg.bot_online":            "✅ Bot is online! Send /start for the menu.",
}

LESSONS = {
    "rsi_oversold": {
        "title": "What does RSI Oversold mean?",
        "content": (
            "RSI (Relative Strength Index) below 30 means an asset has been sold heavily in recent days.\n\n"
            "It doesn't mean 'definitely buy' — it means selling pressure has been extreme and a bounce is statistically more likely.\n\n"
            "📌 Key points:\n"
            "• RSI < 30 = oversold (potential opportunity)\n"
            "• RSI > 70 = overbought (potential top)\n"
            "• RSI alone is not a buy signal — use it alongside trend and volume\n"
            "• In strong downtrends, RSI can stay oversold for weeks\n\n"
            "💡 Best practice: Combine with Fear & Greed, SMA trends, and your DCA strategy."
        ),
    },
    "rsi_overbought": {
        "title": "What does RSI Overbought mean?",
        "content": (
            "RSI above 70 means buying pressure has been intense recently.\n\n"
            "This doesn't mean 'sell everything' — in strong bull markets, RSI can stay elevated for extended periods.\n\n"
            "📌 Key points:\n"
            "• Overbought doesn't mean a crash is coming\n"
            "• It means the upside momentum may slow down\n"
            "• Good time to: stop adding, consider taking partial profits\n"
            "• Bad time to: FOMO buy at market tops"
        ),
    },
    "fear_greed": {
        "title": "The Fear & Greed Index Explained",
        "content": (
            "The Crypto Fear & Greed Index (0-100) measures market sentiment.\n\n"
            "• 0-25: Extreme Fear — people are panicking\n"
            "• 25-45: Fear\n"
            "• 45-55: Neutral\n"
            "• 55-75: Greed\n"
            "• 75-100: Extreme Greed — euphoria / bubble risk\n\n"
            "Warren Buffett: 'Be fearful when others are greedy, and greedy when others are fearful.'\n\n"
            "📌 How to use it:\n"
            "• Extreme Fear (< 25): Consider increasing DCA\n"
            "• Extreme Greed (> 75): Reduce buys, take some profits\n"
            "• Don't use it alone — it's one signal of many"
        ),
    },
    "dca": {
        "title": "Dollar Cost Averaging (DCA) Explained",
        "content": (
            "DCA means buying a fixed amount at regular intervals, regardless of price.\n\n"
            "Why it works:\n"
            "• You buy more coins when prices are low\n"
            "• You buy fewer when prices are high\n"
            "• Removes emotional decision-making\n"
            "• No need to time the market perfectly\n\n"
            "📊 Example — Buy $100 of BTC every week:\n"
            "• Week 1: BTC = $50,000 → 0.002 BTC\n"
            "• Week 2: BTC = $40,000 → 0.0025 BTC  ← More coins!\n"
            "• Week 3: BTC = $45,000 → 0.0022 BTC\n"
            "Average cost per coin < average price over the period ✅\n\n"
            "💡 Smart DCA: Adjust amounts based on RSI and Fear & Greed (exactly what BinanceCoach does!)"
        ),
    },
    "sma_200": {
        "title": "The 200-Day Moving Average",
        "content": (
            "The 200-day SMA is one of the most watched indicators by institutional investors.\n\n"
            "It represents the average price over the last 200 days.\n\n"
            "📌 What it tells you:\n"
            "• Price above 200d SMA = long-term uptrend (bull market)\n"
            "• Price below 200d SMA = long-term downtrend (bear market)\n"
            "• 'Golden Cross': 50d SMA crosses above 200d SMA → bullish signal\n"
            "• 'Death Cross': 50d SMA crosses below 200d SMA → bearish signal\n\n"
            "How BinanceCoach uses it:\n"
            "• Price 20%+ below SMA200 → historically good accumulation zone\n"
            "• Price 30%+ above SMA200 → market may be stretched, reduce buys"
        ),
    },
    "concentration_risk": {
        "title": "What is Concentration Risk?",
        "content": (
            "Concentration risk is when too much of your portfolio is in one asset.\n\n"
            "Example: If 80% of your portfolio is BTC and BTC drops 50%, you lose 40% of your total wealth.\n\n"
            "📌 General guidelines:\n"
            "• No single position > 30-40% of total portfolio\n"
            "• Hold 5-10 different assets for meaningful diversification\n"
            "• Stablecoins (10-30%) act as dry powder for opportunities\n"
            "• Diversify across chains (BNB, Ethereum, Solana, etc.)\n\n"
            "⚠️ Remember: Diversification doesn't eliminate risk — it distributes it."
        ),
    },
    "panic_selling": {
        "title": "Why Panic Selling Destroys Returns",
        "content": (
            "Panic selling is when fear drives you to sell at a loss — often right before a recovery.\n\n"
            "💀 The pattern:\n"
            "1. Price drops → you feel scared\n"
            "2. You sell to 'stop the bleeding'\n"
            "3. Price recovers → you buy back higher\n"
            "4. Repeat until portfolio is destroyed\n\n"
            "✅ How to stop:\n"
            "• Pre-set your 'sell rules' before emotions kick in\n"
            "• Use DCA to stay systematic\n"
            "• Remember: Volatility is the price you pay for crypto returns\n"
            "• If you can't sleep, you're too big in position size"
        ),
    },
}
