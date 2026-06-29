# 🔮 Financial Astrology Skill

**Vedic (Sidereal) astrology analysis for financial markets** — Gold (XAU/USD) & Bitcoin (BTC/USD) day trading.

<p align="center">
  <a href="https://clawhub.ai/skills/financial-astrology"><img src="https://img.shields.io/badge/clawhub-skill-blue" alt="ClawHub"></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/swisseph-v2.10.3.2-orange" alt="Swiss Ephemeris">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**[🇻🇳 Tiếng Việt](README.vi.md)**

---

## 📖 Overview

**Financial Astrology** analyzes planetary positions (Vedic/Sidereal system) and applies them to **short-term trading (Day Trading M15/H1)**. Built on [Swiss Ephemeris](https://www.astro.com/swisseph) — the world's most accurate astronomical library — running 100% offline with no external API dependencies.

> ⚠️ **Disclaimer:** Correlation ≠ causation. This is a **supplementary** tool, not a prediction engine. Investing involves risk.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌙 **Moon Phase** | Market sentiment by lunar phase |
| 🌟 **Nakshatra** | 27 Nakshatras + Pada + Trading quality |
| 🪐 **Planets** | 8 planets + 3 outer planets (sidereal positions) |
| 🏠 **Houses** | Whole Sign Houses + Ascendant |
| 🔗 **Aspects** | Conjunction, Trine, Square, Opposition, Sextile... |
| 🔥 **Combustion** | Planet swallowed by Sun — false signal detection |
| ⚡ **Cazimi** | Planet in heart of Sun — ultra-concentrated energy |
| 🌙☌ **Moon Combinations** | Chandra-Mangal, Vish Yoga, Grahan Yoga... |
| ⏰ **Hora** | Planetary Hours (Chaldean order, sunrise-based) |
| 📊 **Sector Analysis** | Gold→Sun/Venus, Bitcoin→Rahu/Uranus, Banking→Jupiter/Saturn |
| 🌀 **Dasha** | Vimshottari Dasha for Natal Charts |
| 🎯 **Day Trading Signal** | M15/H1 trading signals with sentiment, volatility, strategy |

## 🚀 Installation

```bash
pip install pyswisseph
git clone https://github.com/kimminhpro/financial-astrology-skill.git
cd financial-astrology-skill
python3 scripts/financial_astrology.py
```

For OpenClaw: copy to agent `skills/` folder.

## 🔧 Usage

```bash
# Current time (JST default)
python3 scripts/financial_astrology.py

# Specific time
python3 scripts/financial_astrology.py --date "2026-05-02 12:10:00" --tz Asia/Tokyo

# By asset
python3 scripts/financial_astrology.py --asset gold
python3 scripts/financial_astrology.py --asset btc

# JSON output
python3 scripts/financial_astrology.py --json

# Natal Chart + Vimshottari Dasha
python3 scripts/financial_astrology.py --date "1995-04-25 18:30:00" --tz Asia/Ho_Chi_Minh --lat 21.1861 --lon 106.0763 --natal

# Hora (Planetary Hours) via Python
python3 -c "from scripts.hora_service import get_current_hora; print(get_current_hora())"
```

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--tz` | Asia/Tokyo | IANA timezone |
| `--date` | Now | YYYY-MM-DD HH:MM:SS |
| `--lat` | 34.9333 | Latitude (Hekinan, Japan) |
| `--lon` | 136.9667 | Longitude |
| `--asset` | all | gold, btc, stocks, all |
| `--json` | False | JSON output |
| `--natal` | False | Vimshottari Dasha calculation |

## 🔬 Core Principles

### 🌙 Moon is the "Activator"

> *"Each planet has a tendency, but the Moon decides WHICH tendency gets activated TODAY."*

In Vedic Astrology, Moon = **Manas (Mind)**. Since financial markets reflect crowd psychology (Fear & Greed), the Moon's movement through Nakshatras determines daily trader mood. The planet the Moon interacts with today (via conjunction, aspect, or Nakshatra lord) sets the trend for the session.

### 🏛️ Astrology System

| Component | System | Rationale |
|-----------|--------|-----------|
| Zodiac | **Sidereal** (Nirayana) | Vedic Astrology |
| Ayanamsa | **Lahiri** | Vedic standard |
| House System | **Whole Sign** | Best for Vedic |
| Nodes | **True Node** | Rahu/Ketu 180° opposite |

### 🌙 Moon Phases & Market Behavior

| Phase | Market Psychology | Strategy |
|-------|------------------|----------|
| 🌑 New Moon | Low volatility, sideways | Wait for breakout |
| 🌒 Waxing Crescent | Gradual optimism, Bullish | Buy dips, momentum |
| 🌓 First Quarter | Conflict, decision point | Watch reversal |
| 🌔 Waxing Gibbous | High optimism, Bullish | Trend following |
| 🌕 Full Moon | Peak emotion, HIGH volatility | Avoid overtrading |
| 🌖 Waning Gibbous | Declining optimism | Take profit, tighten SL |
| 🌗 Last Quarter | Reassessment, volatility | Hedge, reduce positions |
| 🌘 Waning Crescent | Pessimism, Bearish | Short, cash is king |

### Moon + Planet Combinations (Day Trading signals)

| Combination | Trend | Strategy |
|-------------|-------|----------|
| 🌙☌♂ Mars (Chandra-Mangal) | Bull Run 🐂 | Buy dips, momentum |
| 🌙☌♄ Saturn (Vish Yoga) | Slow Bleed 🐻 | Sell on rise |
| 🌙☌🐉 Rahu (Grahan Yoga) | The Trap 🕳️ | Option buying, tight SL |
| 🌙☌🔻 Ketu | Panic Button 💥 | Hedge, short |
| 🌙☌♃ Jupiter | Expansion 📈 | Position trading |
| 🌙☌☿ Mercury | Info Flow 📡 | Scalping |
| 🌙☌♀ Venus | Risk Appetite 💎 | Growth stocks |
| 🌙☌☀ Sun | Stable Uptrend ☀️ | Gold, bonds |

## 📊 Sample Output

```
═══════════════════════════════════════════
  🔮 FINANCIAL ASTROLOGY ANALYSIS
  📅 14/06/2026 23:35 JST
  📍 Hekinan, Japan (34.93°N, 136.97°E)
  🎯 All Markets
═══════════════════════════════════════════

🌙 MOON PHASE: Waxing Gibbous (86.4%)
→ Sentiment: High optimism, Bullish
→ Strategy: Trend following

🌟 MOON NAKSHATRA: Anuradha (17)
→ Lord: Saturn ♄
→ Pada: 1
→ Quality: ✅ Good for trading

🔥 KEY ASPECTS TODAY:
  • Moon □ Mars: ⚠️⚠️ PANIC SELL / FOMO BUY
  • Moon △ Jupiter: ✅ Bullish, expansion

📊 DAY TRADING SIGNAL:
→ Primary trend: Bullish with high volatility
→ Caution: Moon square Mars
→ Strategy: Buy dips, tight SL
```

## 💎 Planet & Asset Classes

| Asset | Ruling Planet | Sector |
|-------|-------------|--------|
| 🥇 Gold (XAU/USD) | ☀️ Sun, ♀️ Venus | Safe haven |
| ₿ Bitcoin | 🐉 Rahu, ⛧ Uranus | Crypto |
| 💻 Tech | ⛧ Uranus | Innovation |
| 🏦 Banking | ♃ Jupiter, ♄ Saturn | Finance |
| ⛽ Energy | ♂️ Mars | Oil, gas |

## ⚠️ Warnings

- ❌ NOT a profit guarantee
- ❌ NOT a replacement for TA/FA
- ❌ NOT for automated trading decisions
- ✅ Always use stop-loss
- ✅ Always take personal responsibility

## 📚 References

- *Financial Astrology* — J.N. Bhasin
- *The World According to the Stars* — Raymond Merrman
- Swiss Ephemeris: https://www.astro.com/swisseph
- pyswisseph: https://github.com/aloistr/pyswisseph

## 📝 License

MIT
