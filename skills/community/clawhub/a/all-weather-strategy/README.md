# All Weather Strategy - OpenClaw Professional Skill

Developed by **wzwangyc**, this skill brings common-sense risk-parity asset allocation to the OpenClaw AI environment. It is designed to be highly interactive and beginner-friendly while providing professional-grade financial analysis.

## 🌟 Key Features
- **Intelligent Onboarding**: The AI will proactively ask you to confirm investment amounts and ETF pools before running.
- **Robust Math**: Built-in Risk Parity solver handles complex diversification automatically.
- **Full Transparency**: View annualized return forecasts and volatility risk indicators.
- **Export Ready**: Get a professional PDF report with a single click.

## 🚀 Quick Start
If you are an AI assistant using this skill:
1. Load `scripts/engine.py`.
2. Greet the user and offer the **Default Config** (10,000元, 365天 lookback).
3. If confirmed, run `engine.run()`.

## 📂 Structure
- `scripts/engine.py`: Core logic with native default support.
- `app.py`: Beautiful Streamlit interface.
- `resources/`: Contains SimHei.ttf for full Chinese PDF support.

---
**Copyright © 2026 wzwangyc. All Rights Reserved.**
