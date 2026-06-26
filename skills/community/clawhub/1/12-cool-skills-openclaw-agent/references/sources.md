# Information Sources for Auto-Watchdog

This document lists the primary and configurable sources used by the `auto-watchdog` skill for gathering information on crypto, stock markets, and general news. These sources are categorized for easier management and can be extended or modified as needed.

## Crypto News Sources

- **CoinDesk**: Leading source for cryptocurrency news and prices. [https://www.coindesk.com/]
- **CoinTelegraph**: Independent publication covering blockchain, cryptocurrency, and fintech. [https://cointelegraph.com/]
- **Decrypt**: Reporting on the latest news and trends in crypto. [https://decrypt.co/]
- **The Block**: Research-driven news and insights on digital assets. [https://www.theblockcrypto.com/]

## Stock Market News Sources

- **Bloomberg**: Global business and financial news. [https://www.bloomberg.com/markets]
- **Reuters Business News**: Breaking news and analysis on business and finance. [https://www.reuters.com/business/]
- **Wall Street Journal (WSJ)**: Comprehensive news and analysis, focusing on business and finance. [https://www.wsj.com/news/markets]
- **Financial Times (FT)**: International business, finance, and economic news. [https://www.ft.com/markets]
- **Forbes (Markets)**: Insights and analysis on stock markets and investments. [https://www.forbes.com/markets/]

## General News Sources

- **Associated Press (AP)**: Global news coverage. [https://apnews.com/]
- **Reuters (World News)**: International news and current events. [https://www.reuters.com/world/]
- **BBC News**: International news, analysis, and features. [https://www.bbc.com/news]
- **The Guardian**: UK and international news. [https://www.theguardian.com/world]

## Social Media / Real-time Information

- **X (formerly Twitter)**: Real-time updates and trending topics. (Requires API access and specific query formulation for effective monitoring).
- **Reddit (r/CryptoCurrency, r/Stocks, r/WorldNews)**: Community-driven discussions and news aggregation.

## Adding Custom Sources

Users can suggest additional sources to be integrated into the monitoring process. For each new source, please provide:

- **Name**: The name of the source.
- **URL**: The primary URL for the source.
- **Category**: (e.g., Crypto, Stocks, General News, Blog, Forum).
- **Description**: A brief explanation of what the source covers.

Example:

```
- **MyCryptoBlog**: Independent blog focusing on altcoin analysis. [https://www.mycryptoblog.com/]
```

## Configuration

The `monitor.py` script will be updated to dynamically fetch and utilize these sources. Future enhancements will include a configuration mechanism to prioritize or filter sources based on user preferences.
