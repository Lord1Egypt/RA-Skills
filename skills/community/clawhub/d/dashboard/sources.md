# Data Sources by Use Case

## Business / SaaS Metrics
- **Stripe/Paddle:** MRR, churn, LTV, subscriptions via API
- **Analytics:** Mixpanel, Amplitude, PostHog, Google Analytics
- **CRM:** HubSpot, Pipedrive for sales pipeline
- **Custom DB:** Direct PostgreSQL/MySQL queries for user data

## Infrastructure / DevOps
- **Containers:** Docker stats, compose status, restart counts
- **Servers:** CPU, RAM, disk via SSH or agent
- **CI/CD:** GitLab/GitHub Actions API for pipeline status
- **Logs:** Container stdout/stderr, application logs
- **Monitoring:** Prometheus metrics if available (not required)
- **SSL:** Certificate expiration tracking

## IoT / Home Automation
- **Home Assistant:** REST API or WebSocket with Long-Lived Token
- **Sensors:** Temperature, humidity, motion, door/window status
- **Energy:** Smart meter readings, consumption tracking
- **Cameras:** Snapshot URLs, RTSP streams

## Financial / Trading
- **Crypto exchanges:** Binance, Coinbase, Kraken APIs
- **Brokers:** Interactive Brokers, Degiro (where API available)
- **On-chain:** Wallet addresses for ETH/BTC holdings
- **Price feeds:** CoinGecko, Yahoo Finance
- **Manual entry:** For assets without APIs (real estate, art)

## Content Creator
- **YouTube:** Studio API for views, subscribers, revenue
- **TikTok:** Analytics export or API
- **Social:** Twitter, Instagram insights
- **Monetization:** AdSense, sponsorship tracking (often manual)

## Universal
- **CSV upload:** For any data not API-accessible
- **Google Sheets:** Live connection to collaborative spreadsheets
- **REST endpoints:** Generic JSON API consumption
- **Webhooks:** Receive push updates from external services
