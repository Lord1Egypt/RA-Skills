# Football Auto-Quant & Betting Skill

An advanced OpenClaw skill designed for automated football (soccer) analysis and execution on **Singbet** Asian Handicap markets.

## 🚀 Features
- **Real-time Monitoring**: Integrates with **The Odds API** for live in-play data.
- **Asian Handicap Focus**: Specialized logic for AH and Over/Under markets.
- **Automated Execution**: Connects to Singbet agent portals (hga030.com/sangbet.com).
- **Built-in Risk Management**: 
  - Hard limit of 30 bets per day.
  - Fixed small-stake testing ($$10$$ USD).
  - Automated win/loss tracking.

## 🛠 Setup
1. **API Key**: Ensure you have a valid key from [The Odds API](https://the-odds-api.com/).
2. **Account**: You must have an active betting account from a Singbet international agent (e.g., sangbet.com).
3. **Configuration**: Update the `config` section in the skill settings with your credentials.

## 📈 Strategy
The AI monitors live pressure indices (possession, shots, dangerous attacks) and compares them against the handicap spreads. It triggers a bet only when a statistical discrepancy is detected.

## ⚖️ Disclaimer
This tool is for educational and research purposes only. Betting involves significant financial risk. The developers are not responsible for any financial losses incurred. Please gamble responsibly and comply with local regulations.
