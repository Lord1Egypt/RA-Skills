# Disclaimer

This project is a local single-user data workbench built around AKShare and third-party public financial data interfaces.

## Not Financial Advice

This software is provided for learning, research, and personal data workflow automation only. It does not provide investment advice, trading advice, portfolio recommendations, or any guarantee about data accuracy, completeness, timeliness, or availability.

Always verify important financial data with official or licensed sources before making decisions.

## Data Sources And Usage Limits

The project may call public data interfaces exposed through AKShare, including sources such as Eastmoney, Sina, macro data providers, exchanges, and other third-party websites or services.

Users are responsible for:

- complying with AKShare's license and documentation;
- complying with each upstream data provider's terms of service, robots policies, and rate limits;
- avoiding abusive request patterns, excessive retries, scraping at scale, IP rotation abuse, or attempts to bypass provider restrictions;
- obtaining a licensed data feed when high-frequency, commercial, production, or bulk usage is required.

The included Codex/OpenClaw skill uses conservative defaults, local caching, and slower Eastmoney request pacing to reduce accidental rate-limit pressure. These defaults are not a permission to exceed upstream limits.

## API Keys And Local Secrets

The application can store local AI model configuration in `backend/app/config/ai_config.json`. This file is intentionally excluded from distribution and should not be committed to a public repository.

Do not publish `.env` files, API keys, proxy credentials, cookies, private certificates, or generated cache/log files.

## Third-Party Dependencies

This repository's original source code is released under the MIT License. Third-party dependencies, including AKShare, FastAPI, React, Vite, pandas, and related packages, remain under their own licenses. Review those licenses before redistribution or commercial use.

## No Warranty

The software is provided "as is" without warranty of any kind. The authors and contributors are not liable for data-source outages, provider blocking, incorrect data, trading losses, operational issues, or any damages arising from use of this software.
