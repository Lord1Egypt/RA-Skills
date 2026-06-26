# Known Use Cases (KUC)

Total: **26**

## `KUC-101`
**Source**: `main.py`

Provides unified entry point for starting FastAPI server or running pre/post-market analysis.

## `KUC-102`
**Source**: `app/main.py`

Creates and configures FastAPI application instance with CORS, routers, and lifespan management.

## `KUC-103`
**Source**: `app/static.py`

Serves frontend static files and implements SPA catch-each routing for client-side navigation.

## `KUC-104`
**Source**: `app/routers/alerts.py`

Manages user notifications across portfolios including unread counts, marking as read, and dismissing alerts.

## `KUC-105`
**Source**: `app/routers/auth.py`

Handles user registration, login, and JWT token generation for secure API access.

## `KUC-106`
**Source**: `app/routers/stocks.py`

Manages user's stock watchlist with CRUD operations, real-time quotes, and financial data retrieval.

## `KUC-107`
**Source**: `app/routers/sentiment.py`

Analyzes market sentiment from news and generates AI-powered sentiment reports.

## `KUC-108`
**Source**: `app/routers/generate.py`

Generates pre-market and post-market investment reports for funds or each user's portfolios.

## `KUC-109`
**Source**: `app/routers/market.py`

Provides fund search functionality and real-time market data using Akshare and TuShare APIs.

## `KUC-110`
**Source**: `app/routers/health.py`

Provides basic health check endpoint for system monitoring and load balancer checks.

## `KUC-111`
**Source**: `app/routers/assistant.py`

Provides conversational AI assistant with RAG-enhanced responses for investment queries.

## `KUC-112`
**Source**: `app/routers/recommendations.py`

Generates AI investment recommendations using quantitative factor-based engine for stocks and funds.

## `KUC-113`
**Source**: `app/routers/preferences.py`

Manages user's investment preferences including risk level presets and portfolio settings.

## `KUC-114`
**Source**: `app/routers/widgets.py`

Provides pre-aggregated market data for dashboard widgets including northbound flow and sector performance.

## `KUC-115`
**Source**: `app/routers/dashboard.py`

Provides dashboard overview, system statistics, and customizable layout management.

## `KUC-116`
**Source**: `app/routers/details.py`

Retrieves detailed stock information including spot data, historical prices, and financial indicators.

## `KUC-117`
**Source**: `app/routers/admin.py`

Provides admin endpoints for system testing, LLM connection verification, and web search testing.

## `KUC-118`
**Source**: `app/routers/funds.py`

Manages investment funds with diagnosis, risk metrics, drawdown analysis, and comparison features.

## `KUC-119`
**Source**: `app/routers/commodities.py`

Analyzes gold and silver commodities with price trends and investment insights.

## `KUC-120`
**Source**: `app/routers/reports.py`

Manages generated reports including listing, viewing, and organizing pre/post-market analysis files.

## `KUC-121`
**Source**: `app/routers/settings.py`

Manages application settings including LLM provider configuration and API key management.

## `KUC-122`
**Source**: `app/routers/portfolios.py`

Manages portfolios with unified positions, transactions, DIP plans, AI rebalancing, stress testing, and correlation analysis.

## `KUC-123`
**Source**: `app/routers/compare.py`

Compares multiple stocks side-by-side with metrics including price, PE, PB, market cap, and turnover.

## `KUC-124`
**Source**: `app/routers/news.py`

Aggregates and personalizes financial news feed with categories and bookmarking functionality.

## `KUC-125`
**Source**: `test_scan.py`

Tests raw TuShare API data access for money flow and HSGT northbound data scanning.

## `KUC-126`
**Source**: `test_hsgt_min.py`

Tests high-frequency northbound capital flow minute-level data retrieval.
