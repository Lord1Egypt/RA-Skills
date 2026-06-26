# Data Integration Reference

This document provides comprehensive technical specifications for data integration within the AI-Company unified skill framework. It covers financial data retrieval, news and intelligence gathering, information services integration, multi-source data fusion, and standardized data schemas that ensure consistency across all data operations.

The specifications outlined here are designed to be implementation-agnostic while providing sufficient detail for developers to build robust data integration pipelines. All templates and examples are designed to be VirusTotal-compliant, avoiding dynamic code execution patterns that could trigger security scanning systems.

---

## 1. Financial Data Integration

Financial data forms the backbone of many analytical workflows within the AI-Company framework. This section details the patterns, schemas, and caching strategies required to effectively integrate stock quotes, exchange-traded funds, futures contracts, earnings data, and macroeconomic indicators into a unified data pipeline.

### 1.1 Stock Quotes and Market Data

Stock quote data represents real-time or delayed price information for publicly traded securities. The integration pattern for stock quotes follows a RESTful API architecture that supports both individual security queries and batch retrieval for multiple securities.

#### API Patterns for Stock Data

The primary endpoint pattern for stock quote retrieval follows a consistent structure across most financial data providers:

```
GET /api/v1/quote/{exchange}:{symbol}
GET /api/v1/quotes/batch?symbols={exchange}:{symbol1},{exchange}:{symbol2}
GET /api/v1/historical/{exchange}:{symbol}?period={period}&interval={interval}
```

The REST pattern requires three key parameters: the exchange code identifying the trading venue, the security symbol as listed on that exchange, and optional filters for time range and data granularity. The exchange:symbol format ensures uniqueness across global markets where the same ticker symbol might reference different securities on different exchanges.

Authentication for financial data APIs typically employs API key-based authentication passed via the Authorization header:

```
Authorization: Bearer {api_key}
X-API-Key: {api_key}
```

Rate limiting for stock data APIs generally allows between 100 and 1000 requests per minute depending on the subscription tier. Implementations should track request counts and implement exponential backoff when encountering rate limit responses (HTTP 429).

#### Stock Data Schema

The standard schema for stock quote data includes the following fields:

```json
{
  "symbol": "AAPL",
  "exchange": "NASDAQ",
  "exchange_code": "XNAS",
  "name": "Apple Inc.",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "price": 189.45,
  "open": 188.20,
  "high": 190.15,
  "low": 187.80,
  "close": 189.45,
  "previous_close": 188.90,
  "volume": 52341000,
  "market_cap": 2950000000000,
  "pe_ratio": 28.5,
  "dividend_yield": 0.52,
  "52_week_high": 198.23,
  "52_week_low": 164.08,
  "bid": 189.44,
  "ask": 189.46,
  "bid_size": 100,
  "ask_size": 200,
  "data_source": "primary_exchange",
  "data_quality_score": 0.98
}
```

The timestamp field follows ISO-8601 format with UTC timezone designation. Prices are represented as decimal numbers with precision appropriate to the security's price category. High-precision securities like penny stocks may include additional decimal places while large-cap indices typically round to two decimal places.

Historical daily data follows a similar schema but includes additional fields for adjusted prices that account for splits and dividends:

```json
{
  "symbol": "AAPL",
  "exchange": "NASDAQ",
  "date": "2026-04-25",
  "open": 188.20,
  "high": 190.15,
  "low": 187.80,
  "close": 189.45,
  "adjusted_close": 189.45,
  "volume": 52341000,
  "turnover": 9876543210,
  "change": 0.55,
  "change_percent": 0.29
}
```

#### Caching Strategies for Stock Data

Stock data caching requires careful consideration of data freshness requirements versus API rate limits. The recommended caching strategy employs a tiered approach with different TTL (time-to-live) values based on data type.

Real-time quote data should use aggressive caching with short TTL values, typically 15 to 60 seconds for non-professional data feeds. Cache entries should include the retrieval timestamp and be invalidated when the market is closed if the cached data exceeds the trading session's closing time.

Intraday data with minute-level granularity should cache for 5 to 15 minutes, depending on the volatility of the security. High-volatility securities like those involved in earnings announcements or significant news events may require shorter cache durations.

End-of-day historical data can be cached for extended periods, with TTL values of 24 hours for the most recent trading day and indefinite caching for historical data that will not change. Once a trading day closes and the data is confirmed final, that day's data becomes immutable and can be cached permanently.

The cache key structure should follow a consistent pattern:

```
stock:quote:{exchange}:{symbol}:{timestamp_bucket}
stock:history:{exchange}:{symbol}:{date_range}
stock:minute:{exchange}:{symbol}:{timestamp}
```

### 1.2 Exchange-Traded Funds (ETF)

Exchange-traded funds represent baskets of securities that trade like individual stocks. ETF data integration presents unique challenges due to the dual-layer structure of ETF pricing: the market price at which shares trade and the net asset value (NAV) that represents the underlying holdings' worth.

#### ETF-Specific API Patterns

ETF data retrieval typically extends standard stock APIs with additional endpoints:

```
GET /api/v1/etf/{exchange}:{symbol}
GET /api/v1/etf/{exchange}:{symbol}/holdings
GET /api/v1/etf/{exchange}:{symbol}/nav
GET /api/v1/etf/{exchange}:{symbol}/tracking
```

The holdings endpoint returns the constituent securities that make up the ETF, which is essential for understanding exposure and calculating theoretical NAV. The tracking endpoint provides performance comparison against benchmark indices.

#### ETF Data Schema

```json
{
  "symbol": "SPY",
  "exchange": "NYSE",
  "exchange_code": "XNYS",
  "name": "SPDR S&P 500 ETF Trust",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "price": 502.35,
  "nav": 501.98,
  "premium_discount": 0.07,
  "premium_discount_percent": 0.014,
  "bid": 502.34,
  "ask": 502.36,
  "volume": 45231000,
  "avg_volume_30d": 52100000,
  "total_assets": 425000000000,
  "nav_per_share": 501.98,
  "dividend_yield": 1.35,
  "expense_ratio": 0.0945,
  "tracking_index": "SPX",
  "tracking_index_name": "S&P 500 Index",
  "tracking_error": 0.02,
  "data_source": "index_provider",
  "data_quality_score": 0.99
}
```

The premium/discount field indicates how the market price compares to the NAV, which is critical for understanding whether an ETF is trading at a premium or discount to its intrinsic value. Large premiums or discounts can indicate market stress or liquidity issues.

### 1.3 Futures Contracts

Futures data integration requires special handling due to the continuous nature of futures pricing across contract months and the roll mechanics required to maintain continuous contract series.

#### Futures API Patterns

```
GET /api/v1/futures/{exchange}:{symbol}
GET /api/v1/futures/{exchange}:{symbol}/contract/{month_code}
GET /api/v1/futures/continuous/{exchange}:{symbol}
GET /api/v1/futures/{exchange}:{symbol}/term_structure
```

The continuous endpoint provides adjusted data that stitches together individual contract months into a continuous series, handling the price adjustments required during contract rolls. The term structure endpoint returns the entire forward curve across available contract months.

#### Futures Data Schema

```json
{
  "symbol": "CL",
  "exchange": "NYMEX",
  "exchange_code": "XNYM",
  "name": "Crude Oil WTI",
  "contract_month": "202606",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "price": 78.45,
  "open": 77.80,
  "high": 79.20,
  "low": 77.50,
  "close": 78.45,
  "settlement": 78.42,
  "volume": 245000,
  "open_interest": 1850000,
  "last_trading_day": "2026-05-19",
  "delivery_date": "2026-05-31",
  "contract_size": 1000,
  "price_increment": 0.01,
  "currency": "USD",
  "data_source": "exchange",
  "data_quality_score": 0.99
}
```

Continuous futures data requires additional fields to handle the roll adjustment:

```json
{
  "symbol": "CL",
  "contract_month": "continuous",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "price": 78.35,
  "source_contract": "CL202606",
  "target_contract": "CL202607",
  "roll_date": "2026-04-25",
  "roll_adjustment": 0.10,
  "roll_complete": true
}
```

### 1.4 Earnings and Financial Statements

Corporate earnings data includes income statements, balance sheets, and cash flow statements that provide fundamental analysis inputs for equity valuation.

#### Earnings API Patterns

```
GET /api/v1/earnings/{exchange}:{symbol}/calendar
GET /api/v1/financials/{exchange}:{symbol}/income
GET /api/v1/financials/{exchange}:{symbol}/balance
GET /api/v1/financials/{exchange}:{symbol}/cashflow
```

#### Earnings Calendar Schema

```json
{
  "symbol": "AAPL",
  "exchange": "NASDAQ",
  "company_name": "Apple Inc.",
  "fiscal_period": "Q2 2026",
  "fiscal_quarter": 2,
  "fiscal_year": 2026,
  "report_date": "2026-04-28",
  "report_time": "after_market",
  "estimate_eps": 2.45,
  "actual_eps": null,
  "estimate_revenue": 95000000000,
  "actual_revenue": null,
  "conference_call_date": "2026-04-28",
  "conference_call_time": "17:00:00-05:00",
  "data_source": "company_filing",
  "data_quality_score": 0.95
}
```

#### Income Statement Schema

```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "fiscal_period": "Q1 2026",
  "fiscal_quarter": 1,
  "fiscal_year": 2026,
  "currency": "USD",
  "report_date": "2026-01-28",
  "items": {
    "revenue": 124300000000,
    "cost_of_revenue": 73900000000,
    "gross_profit": 50400000000,
    "operating_expenses": {
      "research_and_development": 7800000000,
      "selling_general_admin": 6200000000,
      "total_operating_expenses": 14000000000
    },
    "operating_income": 36400000000,
    "interest_expense": 650000000,
    "other_income_expense": 420000000,
    "income_before_tax": 36220000000,
    "income_tax_expense": 5620000000,
    "net_income": 30600000000,
    "ebitda": 41200000000,
    "eps_basic": 1.95,
    "eps_diluted": 1.93,
    "weighted_avg_shares_basic": 15200000000,
    "weighted_avg_shares_diluted": 15800000000
  },
  "data_source": "sec_filing",
  "data_quality_score": 0.98
}
```

### 1.5 Macroeconomic Indicators

Macroeconomic data integration covers indicators such as GDP, inflation rates, employment figures, and central bank policy decisions that influence market conditions.

#### Macro API Patterns

```
GET /api/v1/macro/{indicator_code}
GET /api/v1/macro/{indicator_code}?country={country_code}&period={range}
GET /api/v1/macro/indicators/calendar
```

#### GDP Data Schema

```json
{
  "indicator": "GDP",
  "indicator_name": "Gross Domestic Product",
  "country": "USA",
  "country_name": "United States",
  "timestamp": "2026-04-27T08:00:00.000Z",
  "period": "2025Q4",
  "period_type": "quarterly",
  "value": 28500000000000,
  "value_raw": 28.5,
  "value_unit": "trillion",
  "currency": "USD",
  "growth_rate": 2.4,
  "growth_rate_yoy": 2.4,
  "growth_rate_qoq": 0.6,
  "previous_value": 28320000000000,
  "release_date": "2026-01-30",
  "next_release_date": "2026-04-30",
  "data_source": "bea",
  "data_quality_score": 0.99
}
```

#### Inflation (CPI) Schema

```json
{
  "indicator": "CPI",
  "indicator_name": "Consumer Price Index",
  "country": "USA",
  "country_name": "United States",
  "timestamp": "2026-04-27T08:00:00.000Z",
  "period": "2026-03",
  "period_type": "monthly",
  "value": 315.5,
  "previous_value": 314.2,
  "change": 1.3,
  "change_percent": 0.41,
  "yoy_change_percent": 2.8,
  "core_change_percent": 3.1,
  "category": "all_items",
  "release_date": "2026-04-10",
  "next_release_date": "2026-05-12",
  "data_source": "bls",
  "data_quality_score": 0.99
}
```

---

## 2. News and Intelligence Integration

News and intelligence data provides context for market movements, sentiment analysis for securities, and early warning indicators for significant market events. This section details the patterns for integrating real-time news feeds, social media sentiment, and intelligence data sources into a cohesive information pipeline.

### 2.1 Real-Time News Feeds

Real-time news integration requires handling high-velocity data streams with appropriate filtering, deduplication, and enrichment pipelines.

#### News API Patterns

```
GET /api/v1/news/latest?limit={count}
GET /api/v1/news/search?q={query}&from={date}&to={date}
GET /api/v1/news/symbol/{exchange}:{symbol}
GET /api/v1/news/category/{category}
```

The symbol-specific endpoint returns news articles specifically related to a given security, while category endpoints filter by broader topics such as markets, technology, politics, or economics.

#### News Data Schema

```json
{
  "article_id": "news_abc123xyz",
  "title": "Federal Reserve Signals Potential Rate Cut in Q3 2026",
  "summary": "Federal Reserve officials indicated on Wednesday that they may consider cutting interest rates in the third quarter of 2026 if inflation continues to moderate toward the 2% target.",
  "content": "Full article content would appear here with complete text...",
  "source": {
    "name": "Financial Times",
    "code": "FT",
    "reliability_score": 0.95,
    "tier": 1
  },
  "url": "https://www.ft.com/fed-rate-cut-q3",
  "published_at": "2026-04-27T14:30:00.000Z",
  "retrieved_at": "2026-04-27T14:31:15.000Z",
  "entities": [
    {
      "type": "organization",
      "name": "Federal Reserve",
      "ticker": null,
      "confidence": 0.99
    },
    {
      "type": "person",
      "name": "Jerome Powell",
      "role": "Federal Reserve Chair",
      "confidence": 0.97
    },
    {
      "type": "geographic",
      "name": "United States",
      "confidence": 0.98
    }
  ],
  "topics": ["monetary_policy", "interest_rates", "federal_reserve"],
  "sentiment": {
    "overall": "positive",
    "score": 0.65,
    "confidence": 0.82
  },
  "related_symbols": [],
  "impact_assessment": {
    "market_impact": "medium",
    "sectors_affected": ["banking", "real_estate", "utilities"],
    "expected_volatility": "moderate"
  },
  "data_source": "news_aggregator",
  "data_quality_score": 0.88
}
```

#### News Deduplication Strategy

News deduplication requires similarity detection across article content. The recommended approach combines multiple signals:

First, calculate a content hash (SHA-256) of normalized article text after removing whitespace normalization, HTML stripping, and lowercasing. Exact duplicates will share identical hashes.

Second, implement fuzzy matching using n-gram analysis for near-duplicate detection. Articles sharing more than 85% of 5-gram sequences should be considered duplicates, with the higher-quality source (based on reliability_score and content completeness) retained.

Third, use semantic embedding similarity for story-level deduplication. Multiple articles covering the same event from different sources should be grouped into a single story cluster, with a representative article selected for the primary story view.

### 2.2 Social Sentiment Analysis

Social sentiment integration captures market mood from platforms such as Twitter/X, Reddit, stock forums, and financial social networks. This data requires careful handling due to noise, manipulation attempts, and the need for attribution verification.

#### Social API Patterns

```
GET /api/v1/social/sentiment/{exchange}:{symbol}
GET /api/v1/social/trending?category={category}
GET /api/v1/social/mentions/{exchange}:{symbol}?from={date}&to={date}
```

#### Social Sentiment Schema

```json
{
  "symbol": "GME",
  "exchange": "NYSE",
  "timestamp": "2026-04-27T15:00:00.000Z",
  "time_bucket": "15min",
  "metrics": {
    "total_mentions": 45230,
    "unique_authors": 12850,
    "bullish_count": 28450,
    "bearish_count": 8920,
    "neutral_count": 7860,
    "weighted_sentiment_score": 0.42,
    "sentiment_trend": "increasing"
  },
  "platform_breakdown": [
    {
      "platform": "twitter",
      "mentions": 18500,
      "avg_sentiment": 0.38,
      "influence_score": 0.65
    },
    {
      "platform": "reddit",
      "mentions": 15200,
      "avg_sentiment": 0.52,
      "influence_score": 0.45
    },
    {
      "platform": "stocktwits",
      "mentions": 9500,
      "avg_sentiment": 0.35,
      "influence_score": 0.55
    }
  ],
  "influencer_impact": {
    "top_influencers": [
      {
        "handle": "DeepFuckingValue",
        "followers": 2500000,
        "sentiment": "bullish",
        "impact_score": 0.85
      }
    ],
    "aggregate_influencer_sentiment": 0.72
  },
  "manipulation_indicators": {
    "bot_probability": 0.15,
    "coordinated_activity": false,
    "suspicious_patterns": []
  },
  "data_source": "social_analytics",
  "data_quality_score": 0.72
}
```

### 2.3 Source Classification

News and intelligence sources require classification by reliability, expertise domain, and publication tier to weight their influence appropriately in downstream analysis.

#### Source Classification Schema

```json
{
  "source_id": "reuters",
  "name": "Reuters",
  "display_name": "Reuters News Agency",
  "tier": 1,
  "reliability_score": 0.95,
  "domains": ["general_news", "financial_news", "global_coverage"],
  "regions": ["global"],
  "languages": ["en", "zh", "ja", "de", "fr", "es"],
  "contact_info": {
    "headquarters": "London, UK",
    "established": 1851
  },
  "verification_practices": [
    "multiple_source_confirmation",
    "on_record_sources_only",
    "editorial_review_process"
  ],
  "classification_date": "2026-01-15",
  "last_verified": "2026-04-20"
}
```

Source tier classifications follow this standard:

- **Tier 1**: Established wire services and major financial news organizations with rigorous editorial standards and multi-source verification practices (Reuters, Bloomberg, Associated Press)
- **Tier 2**: Major newspapers, financial publications, and recognized industry outlets with editorial oversight (Wall Street Journal, Financial Times, Barron's)
- **Tier 3**: Recognized industry blogs, specialized publications, and regional news outlets with some editorial oversight
- **Tier 4**: Independent contributors, user-generated content platforms, and social media sources requiring additional verification

### 2.4 Sentiment Analysis Integration

Sentiment analysis converts qualitative text content into quantitative sentiment scores that can be used in quantitative trading models and qualitative analysis workflows.

#### Sentiment Analysis API Patterns

```
POST /api/v1/sentiment/analyze
Content-Type: application/json

{
  "text": "The company's earnings beat expectations by 15% with strong revenue growth across all segments.",
  "domain": "financial",
  "model_version": "finance-sentiment-v2.1"
}
```

#### Sentiment Response Schema

```json
{
  "request_id": "sentiment_req_456xyz",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "input_text": "The company's earnings beat expectations by 15%...",
  "domain": "financial",
  "model_version": "finance-sentiment-v2.1",
  "results": {
    "overall_sentiment": "bullish",
    "polarity_score": 0.78,
    "polarity_label": "strongly_bullish",
    "confidence": 0.89,
    "emotions": {
      "joy": 0.45,
      "confidence": 0.35,
      "anticipation": 0.25,
      "fear": 0.05,
      "anger": 0.02,
      "sadness": 0.01
    },
    "key_phrases": [
      "beat expectations",
      "strong revenue growth",
      "all segments"
    ],
    "entities_with_sentiment": [
      {
        "entity": "earnings",
        "sentiment": "bullish",
        "score": 0.85,
        "context": "beat expectations by 15%"
      }
    ]
  },
  "processing_time_ms": 45
}
```

#### Sentiment Score Ranges

Polarity scores follow a standardized range from -1.0 (extremely bearish) to +1.0 (extremely bullish):

- **Strongly Bullish**: 0.6 to 1.0
- **Moderately Bullish**: 0.2 to 0.6
- **Neutral**: -0.2 to 0.2
- **Moderately Bearish**: -0.6 to -0.2
- **Strongly Bearish**: -1.0 to -0.6

### 2.5 Confidence Scoring

Confidence scoring provides a quantitative measure of reliability for aggregated sentiment data, accounting for source quality, sample size, and measurement consistency.

#### Confidence Scoring Formula

The overall confidence score combines multiple factors:

```
Confidence = BaseScore * sqrt(SampleWeight) * SourceQualityFactor * ConsistencyFactor

Where:
- BaseScore = 0.5 (minimum baseline)
- SampleWeight = min(mention_count / 1000, 1.0)
- SourceQualityFactor = weighted_average(source_reliability_scores)
- ConsistencyFactor = 1.0 - (standard_deviation_of_sentiment / max_possible_deviation)
```

#### Confidence Schema

```json
{
  "symbol": "TSLA",
  "exchange": "NASDAQ",
  "timestamp": "2026-04-27T15:00:00.000Z",
  "confidence_metrics": {
    "overall_confidence": 0.82,
    "components": {
      "sample_size": {
        "value": 0.75,
        "mention_count": 85420,
        "threshold_met": true
      },
      "source_quality": {
        "value": 0.88,
        "weighted_avg_reliability": 0.72,
        "tier1_percentage": 0.35
      },
      "consistency": {
        "value": 0.94,
        "sentiment_std_deviation": 0.12,
        "score_range": 0.65
      },
      "recency": {
        "value": 0.98,
        "data_age_minutes": 15,
        "freshness_threshold_minutes": 60
      }
    },
    "confidence_band": {
      "lower": 0.75,
      "upper": 0.89,
      "interpretation": "high_confidence"
    }
  },
  "data_source": "sentiment_aggregator",
  "data_quality_score": 0.82
}
```

---

## 3. Information Services Integration

Information services cover auxiliary data types including weather data, geolocation services, timezone conversions, and other utility services that support financial analysis and operational workflows.

### 3.1 Weather Data Integration

Weather data affects commodity markets, energy demand, agricultural futures, and insurance sectors. Integration patterns must handle multiple data formats and forecast horizons.

#### Weather API Patterns

```
GET /api/v1/weather/current?location={lat},{lon}
GET /api/v1/weather/forecast?location={lat},{lon}&days={count}
GET /api/v1/weather/historical?location={lat},{lon}&from={date}&to={date}
```

#### Weather Data Schema

```json
{
  "location": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "city": "New York",
    "region": "New York",
    "country": "US",
    "timezone": "America/New_York"
  },
  "timestamp": "2026-04-27T15:00:00.000Z",
  "current": {
    "temperature": 18.5,
    "temperature_unit": "celsius",
    "feels_like": 17.2,
    "humidity": 65,
    "wind_speed": 12.5,
    "wind_direction": 225,
    "wind_direction_cardinal": "SW",
    "pressure": 1013.25,
    "visibility": 16.0,
    "uv_index": 5,
    "condition": "partly_cloudy",
    "condition_code": 802
  },
  "forecast": [
    {
      "date": "2026-04-28",
      "high": 22.0,
      "low": 14.0,
      "condition": "sunny",
      "precipitation_probability": 10,
      "precipitation_amount": 0.0
    }
  ],
  "alerts": [],
  "data_source": "weather_provider",
  "data_quality_score": 0.95
}
```

### 3.2 Geolocation Services

Geolocation integration supports address parsing, coordinate lookup, and distance calculations that are essential for event correlation and market analysis.

#### Geolocation API Patterns

```
GET /api/v1/geo/lookup?address={address_string}
GET /api/v1/geo/lookup?lat={lat}&lon={lon}
GET /api/v1/geo/distance?from={lat1},{lon1}&to={lat2},{lon2}
```

#### Geolocation Schema

```json
{
  "query": {
    "input": "Wall Street, New York, NY",
    "input_type": "address"
  },
  "results": [
    {
      "formatted_address": "Wall Street, New York, NY 10005, USA",
      "location": {
        "latitude": 40.7074,
        "longitude": -74.0113
      },
      "components": {
        "street_number": null,
        "street": "Wall Street",
        "city": "New York",
        "county": "New York County",
        "state": "NY",
        "postal_code": "10005",
        "country": "US"
      },
      "accuracy": "high",
      "timezone": "America/New_York",
      "match_confidence": 0.95
    }
  ],
  "data_source": "geocoding_provider",
  "data_quality_score": 0.92
}
```

### 3.3 Timezone Conversion Services

Timezone handling is critical for global financial operations where markets in different regions operate on different local times. Incorrect timezone handling can lead to missed data windows, incorrect event attribution, and scheduling failures.

#### Timezone API Patterns

```
GET /api/v1/timezone/convert?time={iso8601}&from={tz_from}&to={tz_to}
GET /api/v1/timezone/now?location={location_code}
GET /api/v1/timezone/markets?date={iso8601}
```

#### Timezone Conversion Schema

```json
{
  "query": {
    "input_time": "2026-04-27T09:30:00",
    "input_timezone": "America/New_York",
    "target_timezone": "Asia/Shanghai",
    "format": "iso8601"
  },
  "result": {
    "converted_time": "2026-04-27T21:30:00+08:00",
    "converted_time_unix": 1745770200,
    "offset_difference_hours": 12,
    "dst_affected": false
  },
  "market_context": {
    "nyse_open": false,
    "nyse_closed": false,
    "shanghai_open": true,
    "time_until_nyse_open": "PT16H"
  }
}
```

#### Market Hours Schema

```json
{
  "timestamp": "2026-04-27T15:00:00.000Z",
  "markets": [
    {
      "exchange": "NYSE",
      "code": "XNYS",
      "timezone": "America/New_York",
      "status": "open",
      "current_time": "2026-04-27T11:00:00-04:00",
      "session": {
        "type": "regular",
        "open": "09:30:00-04:00",
        "close": "16:00:00-04:00",
        "trading_hours": "09:30-16:00 ET"
      },
      "next_event": {
        "type": "close",
        "time": "2026-04-27T16:00:00-04:00",
        "time_until": "PT5H"
      }
    },
    {
      "exchange": "SSE",
      "code": "XSHG",
      "timezone": "Asia/Shanghai",
      "status": "closed",
      "current_time": "2026-04-28T00:00:00+08:00",
      "session": {
        "type": "regular",
        "open": "09:30:00+08:00",
        "close": "15:00:00+08:00",
        "trading_hours": "09:30-15:00 CST"
      },
      "next_event": {
        "type": "open",
        "time": "2026-04-28T09:30:00+08:00",
        "time_until": "PT9H30M"
      }
    }
  ],
  "data_source": "market_hours_provider",
  "data_quality_score": 0.98
}
```

### 3.4 Provider Integration Patterns

All external data providers should be integrated using a consistent adapter pattern that abstracts provider-specific implementations behind a common interface.

#### Provider Adapter Interface

```javascript
// Provider adapter interface definition
class DataProviderAdapter {
  constructor(config) {
    this.config = config;
    this.rateLimiter = new RateLimiter(config.rateLimit);
    this.circuitBreaker = new CircuitBreaker(config.circuitBreaker);
    this.cache = new CacheLayer(config.cacheConfig);
  }

  async fetch(endpoint, params) {
    // Rate limiting check
    await this.rateLimiter.acquire();
    
    // Circuit breaker check
    if (this.circuitBreaker.isOpen()) {
      throw new ProviderUnavailableError('Circuit breaker is open');
    }
    
    // Cache check
    const cacheKey = this.buildCacheKey(endpoint, params);
    const cached = await this.cache.get(cacheKey);
    if (cached && !this.isStale(cached)) {
      return cached;
    }
    
    try {
      const response = await this.executeRequest(endpoint, params);
      await this.cache.set(cacheKey, response);
      this.circuitBreaker.recordSuccess();
      return response;
    } catch (error) {
      this.circuitBreaker.recordFailure();
      throw error;
    }
  }

  buildCacheKey(endpoint, params) {
    const normalizedParams = Object.keys(params)
      .sort()
      .reduce((acc, key) => ({ ...acc, [key]: params[key] }), {});
    const paramString = JSON.stringify(normalizedParams);
    return `${this.providerName}:${endpoint}:${hash(paramString)}`;
  }

  normalizeTimestamp(timestamp) {
    return new Date(timestamp).toISOString();
  }

  normalizeSymbol(symbol, exchange) {
    return `${exchange}:${symbol}`;
  }
}
```

### 3.5 Fallback Strategies

Robust data integration requires comprehensive fallback strategies that gracefully degrade when primary data sources become unavailable.

#### Fallback Configuration Schema

```json
{
  "data_type": "stock_quote",
  "primary_provider": "bloomberg",
  "providers": [
    {
      "name": "bloomberg",
      "priority": 1,
      "enabled": true,
      "weight": 0.60,
      "timeout_ms": 5000,
      "retry_config": {
        "max_attempts": 3,
        "backoff_multiplier": 2,
        "initial_delay_ms": 1000
      }
    },
    {
      "name": "refinitiv",
      "priority": 2,
      "enabled": true,
      "weight": 0.30,
      "timeout_ms": 8000,
      "retry_config": {
        "max_attempts": 2,
        "backoff_multiplier": 2,
        "initial_delay_ms": 2000
      }
    },
    {
      "name": "iex_cloud",
      "priority": 3,
      "enabled": true,
      "weight": 0.10,
      "timeout_ms": 10000,
      "retry_config": {
        "max_attempts": 1,
        "backoff_multiplier": 1,
        "initial_delay_ms": 0
      }
    }
  ],
  "aggregation_strategy": "weighted_average",
  "stale_threshold_seconds": 60,
  "fallback_timeout_seconds": 15
}
```

#### Circuit Breaker Implementation

```javascript
class CircuitBreaker {
  constructor(config) {
    this.failureThreshold = config.failureThreshold || 5;
    this.successThreshold = config.successThreshold || 3;
    this.timeout = config.timeout || 60000;
    this.state = 'CLOSED';
    this.failures = 0;
    this.successes = 0;
    this.lastFailureTime = null;
  }

  recordSuccess() {
    this.failures = 0;
    if (this.state === 'HALF_OPEN') {
      this.successes++;
      if (this.successes >= this.successThreshold) {
        this.state = 'CLOSED';
        this.successes = 0;
      }
    }
  }

  recordFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();
    if (this.state === 'HALF_OPEN') {
      this.state = 'OPEN';
    } else if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }

  isOpen() {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime >= this.timeout) {
        this.state = 'HALF_OPEN';
        return false;
      }
      return true;
    }
    return false;
  }

  getState() {
    return {
      state: this.state,
      failures: this.failures,
      successes: this.successes,
      lastFailureTime: this.lastFailureTime
    };
  }
}
```

### 3.6 Rate Limiting

Rate limiting controls API consumption to stay within provider-imposed quotas. The implementation should support multiple strategies including fixed window, sliding window, and token bucket algorithms.

#### Rate Limiter Implementation

```javascript
class RateLimiter {
  constructor(config) {
    this.maxRequests = config.maxRequests || 100;
    this.windowMs = config.windowMs || 60000;
    this.strategy = config.strategy || 'sliding_window';
    this.requests = [];
  }

  async acquire(weight = 1) {
    if (this.strategy === 'token_bucket') {
      return this.acquireTokenBucket(weight);
    }
    return this.acquireSlidingWindow(weight);
  }

  async acquireSlidingWindow(weight) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Remove expired requests
    this.requests = this.requests.filter(ts => ts > windowStart);
    
    const currentCount = this.requests.reduce((sum, _) => sum + 1, 0);
    
    if (currentCount + weight > this.maxRequests) {
      const waitTime = this.windowMs - (now - this.requests[0]);
      throw new RateLimitError(`Rate limit exceeded. Retry after ${waitTime}ms`, waitTime);
    }
    
    for (let i = 0; i < weight; i++) {
      this.requests.push(now);
    }
    
    return true;
  }

  async acquireTokenBucket(weight) {
    if (!this.tokens) {
      this.tokens = this.maxRequests;
      this.lastRefill = Date.now();
    }
    
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    const refillAmount = Math.floor((elapsed / this.windowMs) * this.maxRequests);
    this.tokens = Math.min(this.maxRequests, this.tokens + refillAmount);
    this.lastRefill = now;
    
    if (this.tokens < weight) {
      const waitTime = Math.ceil((weight - this.tokens) / (this.maxRequests / this.windowMs));
      throw new RateLimitError(`Rate limit exceeded. Retry after ${waitTime}ms`, waitTime);
    }
    
    this.tokens -= weight;
    return true;
  }

  getStatus() {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const activeRequests = this.requests.filter(ts => ts > windowStart).length;
    
    return {
      strategy: this.strategy,
      currentRequests: activeRequests,
      maxRequests: this.maxRequests,
      remainingRequests: Math.max(0, this.maxRequests - activeRequests),
      resetAt: new Date(now + this.windowMs).toISOString()
    };
  }
}
```

---

## 4. Multi-Source Data Fusion

Multi-source data fusion combines information from multiple providers to produce unified, consistent, and high-quality data outputs. This section details the technical approaches for schema normalization, conflict resolution, and quality scoring across heterogeneous data sources.

### 4.1 Schema Normalization

Schema normalization transforms provider-specific data formats into a unified canonical schema that supports consistent processing across all downstream components.

#### Normalization Pipeline

The normalization pipeline processes incoming data through a sequence of transformation stages:

**Stage 1: Field Mapping**

Field mapping translates provider-specific field names to canonical field names using configurable mapping tables:

```json
{
  "provider": "bloomberg",
  "mapping_version": "1.0.0",
  "field_mappings": {
    "PRIMARY_EXCHANGE": "exchange",
    "TICKER": "symbol",
    "LAST_PRICE": "price",
    "OPEN_PRC": "open",
    "HIGH_1": "high",
    "LOW_1": "low",
    "CLOSE_PRCE": "close",
    "PREVCLS": "previous_close",
    "VOLUME": "volume",
    "MKTCAP": "market_cap",
    "PE_RATIO": "pe_ratio",
    "DVD_YLD_12M": "dividend_yield",
    "ALL_EXCHANGES": "aggregated",
    "NET_CHANGE": "change",
    "PCT_CHANGE": "change_percent"
  }
}
```

**Stage 2: Type Conversion**

Type conversion ensures all fields conform to expected data types:

```javascript
const typeConverters = {
  price: (value) => parseFloat(value).toFixed(2),
  volume: (value) => parseInt(value, 10),
  timestamp: (value) => new Date(value).toISOString(),
  percentage: (value) => parseFloat(value) / 100,
  boolean: (value) => ['true', '1', 'yes', 'on'].includes(String(value).toLowerCase()),
  nullHandling: (value, defaultValue) => value === '' || value === null ? defaultValue : value
};
```

**Stage 3: Value Validation**

Value validation applies business rules to ensure data integrity:

```javascript
const validationRules = {
  price: (value) => value >= 0 && value < 1000000,
  volume: (value) => value >= 0 && value < 1e15,
  percentage: (value) => value >= -100 && value <= 100,
  timestamp: (value) => !isNaN(Date.parse(value)),
  symbol: (value) => /^[A-Z0-9]{1,10}$/.test(value),
  exchange: (value) => ['NYSE', 'NASDAQ', 'LSE', 'TSE', 'HKEX', 'SSE', 'SZSE'].includes(value)
};
```

**Stage 4: Enrichment**

Enrichment adds derived fields and metadata:

```javascript
const enrichmentFunctions = {
  addCalculatedFields: (data) => ({
    ...data,
    mid_price: data.bid && data.ask ? (data.bid + data.ask) / 2 : null,
    spread: data.bid && data.ask ? data.ask - data.bid : null,
    spread_percent: data.bid && data.ask ? ((data.ask - data.bid) / data.mid_price) * 100 : null,
    vwap_proxy: data.price && data.volume ? data.price * data.volume : null
  }),
  
  addTimestampMetadata: (data) => ({
    ...data,
    ingested_at: new Date().toISOString(),
    data_age_seconds: Math.floor((Date.now() - new Date(data.timestamp)) / 1000)
  }),
  
  addProviderMetadata: (data, provider) => ({
    ...data,
    source_provider: provider.name,
    source_quality_score: provider.reliabilityScore,
    source_timestamp: provider.timestamp
  })
};
```

### 4.2 Conflict Resolution

When multiple sources provide different values for the same data point, conflict resolution determines which value to use or how to combine them.

#### Conflict Detection

Conflicts are detected by comparing normalized values across sources:

```javascript
function detectConflict(observations, fieldName, tolerance = 0.001) {
  const values = observations
    .map(obs => obs[fieldName])
    .filter(v => v !== null && v !== undefined);
  
  if (values.length < 2) {
    return { hasConflict: false };
  }
  
  const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
  const maxDeviation = Math.max(...values.map(v => Math.abs(v - mean) / mean));
  
  return {
    hasConflict: maxDeviation > tolerance,
    values,
    mean,
    maxDeviation,
    conflictLevel: maxDeviation > tolerance ? 'significant' : 'minor'
  };
}
```

#### Conflict Resolution Strategies

The framework supports multiple resolution strategies configured per data type:

```json
{
  "conflict_resolution": {
    "stock_quote": {
      "strategy": "weighted_quality_score",
      "fields": {
        "price": {
          "strategy": "weighted_average",
          "weights": ["provider_quality_score", "recency_score"],
          "tolerance": 0.001
        },
        "volume": {
          "strategy": "max",
          "tolerance": 0.05
        }
      }
    },
    "news_sentiment": {
      "strategy": "tiered_priority",
      "tiers": [
        { "tier": 1, "weight": 0.5 },
        { "tier": 2, "weight": 0.3 },
        { "tier": 3, "weight": 0.15 },
        { "tier": 4, "weight": 0.05 }
      ]
    },
    "earnings_estimate": {
      "strategy": "consensus",
      "exclude_outliers": true,
      "outlier_std_multiplier": 2
    }
  }
}
```

#### Resolution Strategy Implementations

**Weighted Average Strategy**: Combines values proportionally to their source quality scores:

```javascript
function resolveWeightedAverage(observations, fieldName, weights) {
  let weightedSum = 0;
  let totalWeight = 0;
  
  for (const obs of observations) {
    const value = obs[fieldName];
    const weight = calculateCompositeWeight(obs, weights);
    
    if (value !== null && value !== undefined && !isNaN(value)) {
      weightedSum += value * weight;
      totalWeight += weight;
    }
  }
  
  return totalWeight > 0 ? weightedSum / totalWeight : null;
}
```

**Consensus Strategy**: Uses median or trimmed mean to exclude outlier estimates:

```javascript
function resolveConsensus(observations, fieldName, excludeOutliers = true, stdMultiplier = 2) {
  const values = observations
    .map(obs => obs[fieldName])
    .filter(v => v !== null && v !== undefined && !isNaN(v))
    .sort((a, b) => a - b);
  
  if (values.length === 0) return null;
  
  if (!excludeOutliers || values.length < 4) {
    return values[Math.floor(values.length / 2)];
  }
  
  const median = values[Math.floor(values.length / 2)];
  const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
  const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
  const stdDev = Math.sqrt(variance);
  
  const lowerBound = median - (stdMultiplier * stdDev);
  const upperBound = median + (stdMultiplier * stdDev);
  
  const filteredValues = values.filter(v => v >= lowerBound && v <= upperBound);
  
  if (filteredValues.length === 0) return median;
  
  return filteredValues[Math.floor(filteredValues.length / 2)];
}
```

**Tiered Priority Strategy**: Selects the highest-quality source's value:

```javascript
function resolveTieredPriority(observations, fieldName, tiers) {
  const sorted = [...observations].sort((a, b) => {
    const tierA = tiers.findIndex(t => t.tier === a.sourceTier);
    const tierB = tiers.findIndex(t => t.tier === b.sourceTier);
    return tierA - tierB;
  });
  
  return sorted[0]?.[fieldName] ?? null;
}
```

### 4.3 Quality Scoring

Quality scoring provides a unified metric for data reliability that accounts for source reliability, data freshness, completeness, and consistency.

#### Quality Score Components

```javascript
const qualityComponents = {
  sourceReliability: (observation) => {
    const scores = {
      'bloomberg': 0.98,
      'refinitiv': 0.96,
      'factset': 0.94,
      'iex': 0.85,
      'yahoo': 0.80
    };
    return scores[observation.source] ?? 0.70;
  },
  
  freshness: (observation, maxAgeSeconds = 300) => {
    const ageSeconds = (Date.now() - new Date(observation.timestamp)) / 1000;
    return Math.max(0, 1 - (ageSeconds / maxAgeSeconds));
  },
  
  completeness: (observation, requiredFields) => {
    const filledFields = requiredFields.filter(f => 
      observation[f] !== null && 
      observation[f] !== undefined && 
      observation[f] !== ''
    );
    return filledFields.length / requiredFields.length;
  },
  
  consistency: (observations, fieldName) => {
    const values = observations
      .map(obs => obs[fieldName])
      .filter(v => v !== null && v !== undefined);
    
    if (values.length < 2) return 1.0;
    
    const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
    const maxDeviation = Math.max(...values.map(v => Math.abs(v - mean) / mean));
    
    return Math.max(0, 1 - maxDeviation * 10);
  }
};
```

#### Combined Quality Score

```javascript
function calculateQualityScore(observation, relatedObservations = [], context = {}) {
  const weights = context.weights || {
    sourceReliability: 0.40,
    freshness: 0.25,
    completeness: 0.20,
    consistency: 0.15
  };
  
  const componentScores = {
    sourceReliability: qualityComponents.sourceReliability(observation),
    freshness: qualityComponents.freshness(observation, context.maxAgeSeconds),
    completeness: qualityComponents.completeness(observation, context.requiredFields || []),
    consistency: relatedObservations.length > 0 
      ? qualityComponents.consistency(relatedObservations, context.fieldName)
      : 1.0
  };
  
  const overallScore = Object.keys(weights).reduce((sum, key) => {
    return sum + (componentScores[key] * weights[key]);
  }, 0);
  
  return {
    overall: Math.round(overallScore * 100) / 100,
    components: componentScores,
    confidence: calculateConfidence(componentScores),
    grade: scoreToGrade(overallScore)
  };
}

function scoreToGrade(score) {
  if (score >= 0.95) return 'A+';
  if (score >= 0.90) return 'A';
  if (score >= 0.85) return 'B+';
  if (score >= 0.80) return 'B';
  if (score >= 0.70) return 'C';
  if (score >= 0.60) return 'D';
  return 'F';
}

function calculateConfidence(components) {
  const variances = Object.values(components).map(s => Math.pow(1 - s, 2));
  const avgVariance = variances.reduce((sum, v) => sum + v, 0) / variances.length;
  return 1 - Math.sqrt(avgVariance);
}
```

#### Quality Score Schema

```json
{
  "data_point_id": "quote_AAPL_XNAS_20260427T1530",
  "timestamp": "2026-04-27T15:30:00.000Z",
  "quality_score": {
    "overall": 0.92,
    "grade": "A",
    "confidence": 0.85,
    "components": {
      "source_reliability": 0.96,
      "freshness": 0.95,
      "completeness": 0.88,
      "consistency": 0.89
    },
    "component_weights": {
      "source_reliability": 0.40,
      "freshness": 0.25,
      "completeness": 0.20,
      "consistency": 0.15
    },
    "flags": [],
    "warnings": ["Minor inconsistency in bid/ask spread"],
    "recommendations": []
  },
  "source_breakdown": [
    {
      "source": "bloomberg",
      "value": 189.45,
      "quality_contribution": 0.38
    },
    {
      "source": "refinitiv",
      "value": 189.44,
      "quality_contribution": 0.36
    },
    {
      "source": "iex",
      "value": 189.50,
      "quality_contribution": 0.18
    }
  ]
}
```

---

## 5. Standardization Schema

Standardization ensures consistent data formats, conventions, and response structures across all components of the data integration framework. This section defines the canonical schemas, conventions, and error handling patterns that all data operations must follow.

### 5.1 Timestamp Conventions

All timestamps within the framework follow ISO-8601 format with explicit timezone designation. This ensures unambiguous temporal ordering and correct time-based operations across global deployments.

#### Timestamp Format Standards

**Primary Format (Full Precision)**

```
YYYY-MM-DDTHH:mm:ss.SSSZ
Example: 2026-04-27T15:30:00.000Z
```

The `Z` suffix indicates UTC timezone. For local times with explicit offsets:

```
YYYY-MM-DDTHH:mm:ss.SSS±HH:mm
Example: 2026-04-27T11:30:00.000-04:00
```

**Compact Format (Historical Data)**

```
YYYY-MM-DD
Example: 2026-04-27
```

**Unix Timestamp (Internal Processing)**

```
Seconds since epoch (1970-01-01T00:00:00Z)
Example: 1745765400
```

#### Timestamp Validation Rules

```javascript
const timestampValidation = {
  isValidISO8601: (value) => {
    const regex = /^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d{3})?(Z|[+-]\d{2}:\d{2})?)?$/;
    if (!regex.test(value)) return false;
    const date = new Date(value);
    return !isNaN(date.getTime());
  },
  
  isValidUnixTimestamp: (value) => {
    const num = parseInt(value, 10);
    return !isNaN(num) && num > 0 && num < 1e12;
  },
  
  normalizeToISO: (value) => {
    if (timestampValidation.isValidISO8601(value)) {
      return new Date(value).toISOString();
    }
    if (timestampValidation.isValidUnixTimestamp(value)) {
      return new Date(parseInt(value, 10) * 1000).toISOString();
    }
    throw new InvalidTimestampError(`Cannot parse timestamp: ${value}`);
  },
  
  normalizeToUnix: (value) => {
    const iso = timestampValidation.normalizeToISO(value);
    return Math.floor(new Date(iso).getTime() / 1000);
  }
};
```

### 5.2 Symbol Conventions

Financial symbols follow a standardized format that ensures uniqueness across global markets.

#### Symbol Format Standard

The canonical symbol format is `{exchange}:{symbol}` where:

- **Exchange**: ISO 10383 market identifier code (MIC) in uppercase
- **Symbol**: Exchange-specific security identifier

```
Examples:
NYSE:AAPL      - Apple on NYSE
XNAS:MSFT      - Microsoft on NASDAQ
XLON:HSBA      - HSBC on London Stock Exchange
XHKG:0700      - Tencent on HKEX
XSHG:600519    - Kweichow Moutai on Shanghai
XSHE:000858    - Wuliangye on Shenzhen
```

#### Symbol Validation Rules

```javascript
const symbolValidation = {
  MIC_CODES: new Set([
    'XNAS', 'XNYS', 'XASE', 'ARCX', 'XOTO',
    'XLON', 'XPAR', 'XFRA', 'XSWX', 'XMIL',
    'XHKG', 'XSHG', 'XSHE', 'XTKS', 'XJPX',
    'KSC', 'XKRX', 'ASX', 'XNZE', 'XBOM',
    'SGX', 'XIDX', 'XBKK', 'XKLS'
  ]),
  
  isValidMIC: (mic) => {
    return symbolValidation.MIC_CODES.has(mic.toUpperCase());
  },
  
  isValidSymbol: (symbol) => {
    // Symbol should be 1-10 alphanumeric characters
    return /^[A-Z0-9]{1,10}$/i.test(symbol);
  },
  
  isValidCanonicalSymbol: (canonical) => {
    const parts = canonical.split(':');
    if (parts.length !== 2) return false;
    const [exchange, symbol] = parts;
    return symbolValidation.isValidMIC(exchange) && symbolValidation.isValidSymbol(symbol);
  },
  
  normalizeSymbol: (input) => {
    const parts = input.split(':');
    if (parts.length === 2) {
      return `${parts[0].toUpperCase()}:${parts[1].toUpperCase()}`;
    }
    // Assume NASDAQ for US symbols without exchange
    if (/^[A-Z]{1,4}$/i.test(input)) {
      return `XNAS:${input.toUpperCase()}`;
    }
    throw new InvalidSymbolError(`Invalid symbol format: ${input}`);
  },
  
  parseSymbol: (canonical) => {
    const parts = canonical.split(':');
    if (parts.length !== 2) {
      throw new InvalidSymbolError(`Invalid canonical symbol: ${canonical}`);
    }
    return {
      exchange: parts[0].toUpperCase(),
      symbol: parts[1].toUpperCase(),
      mic: parts[0].toUpperCase()
    };
  }
};
```

### 5.3 Error Response Schema

All API errors follow a consistent schema that enables reliable error handling across the framework.

#### Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded. Please retry after 5000 milliseconds.",
    "details": {
      "provider": "bloomberg",
      "retry_after_ms": 5000,
      "limit_type": "requests_per_minute",
      "current_usage": 100,
      "limit": 100
    },
    "timestamp": "2026-04-27T15:30:00.000Z",
    "request_id": "req_abc123xyz",
    "documentation_url": "https://docs.example.com/errors/RATE_LIMIT_EXCEEDED"
  }
}
```

#### Standard Error Codes

| Code | HTTP Status | Description | Retryable |
|------|-------------|-------------|-----------|
| `INVALID_REQUEST` | 400 | Malformed request or invalid parameters | No |
| `MISSING_REQUIRED_FIELD` | 400 | Required field not provided | No |
| `INVALID_SYMBOL` | 400 | Symbol format invalid or not found | No |
| `INVALID_TIMESTAMP` | 400 | Timestamp format invalid | No |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication | No |
| `FORBIDDEN` | 403 | Insufficient permissions | No |
| `NOT_FOUND` | 404 | Resource not found | No |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not supported | No |
| `RATE_LIMIT_EXCEEDED` | 429 | API rate limit hit | Yes |
| `QUOTA_EXCEEDED` | 429 | Monthly quota exhausted | Yes |
| `PROVIDER_UNAVAILABLE` | 503 | External provider is down | Yes |
| `SERVICE_UNAVAILABLE` | 503 | Internal service unavailable | Yes |
| `TIMEOUT` | 504 | Request timed out | Yes |
| `INTERNAL_ERROR` | 500 | Unexpected server error | Yes |

#### Error Handler Implementation

```javascript
class ErrorHandler {
  constructor(config) {
    this.errorLog = new ErrorLogger(config.logging);
    this.alertSystem = new AlertSystem(config.alerts);
  }

  handleError(error, context = {}) {
    const errorResponse = this.formatError(error, context);
    this.errorLog.log(errorResponse);
    
    if (this.shouldAlert(error)) {
      this.alertSystem.send(errorResponse);
    }
    
    return errorResponse;
  }

  formatError(error, context) {
    const code = this.mapErrorToCode(error);
    const httpStatus = this.codeToHTTPStatus(code);
    
    return {
      error: {
        code,
        message: error.message || this.getDefaultMessage(code),
        details: this.extractDetails(error),
        timestamp: new Date().toISOString(),
        request_id: context.requestId || this.generateRequestId(),
        documentation_url: this.getDocumentationURL(code)
      },
      httpStatus
    };
  }

  mapErrorToCode(error) {
    const errorMap = {
      'ValidationError': 'INVALID_REQUEST',
      'SymbolNotFoundError': 'NOT_FOUND',
      'RateLimitError': 'RATE_LIMIT_EXCEEDED',
      'ProviderTimeoutError': 'TIMEOUT',
      'AuthenticationError': 'UNAUTHORIZED',
      'AuthorizationError': 'FORBIDDEN'
    };
    return errorMap[error.name] || 'INTERNAL_ERROR';
  }

  extractDetails(error) {
    if (error.details) return error.details;
    if (error.provider) return { provider: error.provider };
    return {};
  }

  shouldAlert(error) {
    const alertConditions = [
      error.name === 'ProviderUnavailableError',
      error.name === 'ServiceUnavailableError',
      error.message?.includes('circuit breaker'),
      error.retryCount > 3
    ];
    return alertConditions.some(Boolean);
  }

  generateRequestId() {
    return `req_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 9)}`;
  }

  codeToHTTPStatus(code) {
    const statusMap = {
      'INVALID_REQUEST': 400,
      'MISSING_REQUIRED_FIELD': 400,
      'INVALID_SYMBOL': 400,
      'INVALID_TIMESTAMP': 400,
      'UNAUTHORIZED': 401,
      'FORBIDDEN': 403,
      'NOT_FOUND': 404,
      'METHOD_NOT_ALLOWED': 405,
      'RATE_LIMIT_EXCEEDED': 429,
      'QUOTA_EXCEEDED': 429,
      'PROVIDER_UNAVAILABLE': 503,
      'SERVICE_UNAVAILABLE': 503,
      'TIMEOUT': 504,
      'INTERNAL_ERROR': 500
    };
    return statusMap[code] || 500;
  }

  getDocumentationURL(code) {
    return `https://docs.ai-company.dev/errors/${code}`;
  }

  getDefaultMessage(code) {
    const messages = {
      'INVALID_REQUEST': 'The request could not be processed due to invalid parameters.',
      'NOT_FOUND': 'The requested resource was not found.',
      'RATE_LIMIT_EXCEEDED': 'API rate limit exceeded. Please retry after the specified delay.',
      'TIMEOUT': 'The request timed out. Please retry.',
      'INTERNAL_ERROR': 'An unexpected error occurred. Please try again later.'
    };
    return messages[code] || 'An error occurred.';
  }
}
```

### 5.4 Success Response Schema

Successful responses follow a consistent envelope format that includes metadata alongside the requested data.

#### Success Response Format

```json
{
  "success": true,
  "data": {
    /* Response data */
  },
  "metadata": {
    "request_id": "req_abc123xyz",
    "timestamp": "2026-04-27T15:30:00.000Z",
    "data_source": "primary_provider",
    "data_age_seconds": 15,
    "quality_score": 0.92,
    "pagination": {
      "page": 1,
      "page_size": 100,
      "total_pages": 5,
      "total_records": 450
    }
  }
}
```

#### Batch Response Format

```json
{
  "success": true,
  "data": [
    { "symbol": "AAPL", "price": 189.45, "status": "success" },
    { "symbol": "INVALID", "error": "Symbol not found", "status": "error" },
    { "symbol": "MSFT", "price": 415.20, "status": "success" }
  ],
  "metadata": {
    "request_id": "req_batch_456xyz",
    "timestamp": "2026-04-27T15:30:00.000Z",
    "total_requested": 3,
    "total_successful": 2,
    "total_failed": 1,
    "partial_success": true
  }
}
```

### 5.5 Pagination Schema

List endpoints support pagination with consistent parameter and response formats.

#### Pagination Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `page_size` | integer | 100 | Records per page (max 1000) |
| `offset` | integer | 0 | Alternative to page for offset-based pagination |
| `limit` | integer | 100 | Maximum records to return |
| `cursor` | string | null | Cursor for cursor-based pagination |

#### Pagination Response

```json
{
  "success": true,
  "data": [ /* Array of records */ ],
  "metadata": {
    "pagination": {
      "page": 1,
      "page_size": 100,
      "total_records": 1523,
      "total_pages": 16,
      "has_next": true,
      "has_previous": false,
      "next_cursor": "eyJsYXN0IjogIjE2MDAifQ==",
      "previous_cursor": null
    },
    "request_id": "req_paginated_789xyz",
    "timestamp": "2026-04-27T15:30:00.000Z"
  }
}
```

### 5.6 Data Freshness Indicators

All time-sensitive data includes freshness metadata to enable informed consumption decisions.

#### Freshness Schema

```json
{
  "data_point": {
    "value": 189.45,
    "timestamp": "2026-04-27T15:30:00.000Z",
    "freshness": {
      "age_seconds": 15,
      "age_formatted": "15 seconds",
      "is_fresh": true,
      "fresh_threshold_seconds": 300,
      "market_open_fresh_threshold_seconds": 60,
      "market_closed_fresh_threshold_seconds": 3600
    },
    "data_delay": {
      "is_delayed": false,
      "delay_seconds": 0,
      "delay_category": "real_time",
      "provider_delay_info": null
    }
  }
}
```

#### Freshness Thresholds by Data Type

| Data Type | Market Open Threshold | Market Closed Threshold |
|-----------|----------------------|------------------------|
| Stock Quote | 60 seconds | 1 hour |
| Intraday OHLCV | 5 minutes | 1 hour |
| Daily OHLCV | 1 day | None (EOD) |
| News Article | 5 minutes | 5 minutes |
| Earnings | 1 hour | 1 hour |
| Macro Indicator | 1 hour | 1 hour |

---

## Appendix A: Complete Data Schema Reference

This appendix provides a consolidated reference of all schema types used throughout the data integration framework.

### Common Fields

All data objects include these standard fields:

```json
{
  "id": "unique_identifier",
  "created_at": "2026-04-27T15:30:00.000Z",
  "updated_at": "2026-04-27T15:30:00.000Z",
  "version": 1,
  "source": "provider_name",
  "quality_score": 0.92,
  "metadata": {}
}
```

### Geographic Coordinate Schema

```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "altitude": null,
  "precision": "high",
  "datum": "WGS84"
}
```

### Currency Amount Schema

```json
{
  "value": 189450000,
  "display_value": "$1,894.50",
  "currency": "USD",
  "currency_code": "840",
  "amount_type": "per_share",
  "converted_values": {
    "EUR": 175.20,
    "GBP": 151.30,
    "JPY": 28450.00,
    "CNY": 1375.80
  }
}
```

### Percentage Schema

```json
{
  "value": 2.45,
  "display_value": "2.45%",
  "direction": "positive",
  "basis_points": 245,
  "change_from": 185.20,
  "change_to": 189.45
}
```

---

## Appendix B: Integration Testing Patterns

### Unit Test Template

```javascript
describe('DataProvider Integration', () => {
  let provider;
  
  beforeEach(() => {
    provider = new DataProviderAdapter({
      name: 'test_provider',
      baseUrl: 'https://api.test-provider.com',
      apiKey: process.env.TEST_API_KEY,
      rateLimit: { maxRequests: 10, windowMs: 1000 },
      cacheConfig: { enabled: true, ttlSeconds: 60 }
    });
  });
  
  describe('fetchQuote', () => {
    it('should return normalized quote data', async () => {
      const result = await provider.fetchQuote('XNAS:AAPL');
      
      expect(result).to.have.property('symbol').equal('AAPL');
      expect(result).to.have.property('exchange').equal('XNAS');
      expect(result).to.have.property('price').that.is.a('number');
      expect(result).to.have.property('timestamp').that.matches(/^\d{4}-\d{2}-\d{2}T/);
      expect(result.quality_score).to.be.at.least(0.7);
    });
    
    it('should throw InvalidSymbolError for invalid symbols', async () => {
      await expect(provider.fetchQuote('INVALID'))
        .to.be.rejectedWith('InvalidSymbolError');
    });
    
    it('should handle rate limiting gracefully', async () => {
      const requests = Array(15).fill().map(() => provider.fetchQuote('XNAS:AAPL'));
      const results = await Promise.allSettled(requests);
      
      const failures = results.filter(r => r.status === 'rejected');
      expect(failures.length).to.be.greaterThan(0);
      expect(failures[0].reason).to.be.instanceOf(RateLimitError);
    });
  });
});
```

### Integration Test Template

```javascript
describe('Multi-Source Fusion Integration', () => {
  const fusionEngine = new FusionEngine({
    providers: [
      { name: 'bloomberg', weight: 0.5 },
      { name: 'refinitiv', weight: 0.3 },
      { name: 'iex', weight: 0.2 }
    ],
    conflictResolution: {
      strategy: 'weighted_average',
      tolerance: 0.001
    }
  });
  
  it('should fuse data from multiple providers', async () => {
    const observations = [
      { source: 'bloomberg', price: 189.45, quality: 0.98 },
      { source: 'refinitiv', price: 189.44, quality: 0.96 },
      { source: 'iex', price: 189.50, quality: 0.85 }
    ];
    
    const result = fusionEngine.fuse(observations, 'price');
    
    expect(result.value).to.be.closeTo(189.46, 0.01);
    expect(result.confidence).to.be.at.least(0.8);
    expect(result.sources).to.have.lengthOf(3);
  });
  
  it('should detect and flag conflicts', async () => {
    const observations = [
      { source: 'bloomberg', price: 189.45 },
      { source: 'refinitiv', price: 195.00 }
    ];
    
    const result = fusionEngine.fuse(observations, 'price');
    
    expect(result.flags).to.include('conflict_detected');
    expect(result.conflict_resolution).to.equal('manual_review_required');
  });
});
```

---

## Appendix C: Security Considerations

### API Key Management

API keys should never be hardcoded or logged. Use environment variables or secrets management systems:

```javascript
// CORRECT: Environment variable
const apiKey = process.env.PROVIDER_API_KEY;

// INCORRECT: Hardcoded key
const apiKey = 'sk_live_abc123xyz';
```

### Input Sanitization

All external inputs must be sanitized before use in API calls:

```javascript
function sanitizeSymbol(input) {
  // Remove any characters except alphanumeric and colon
  const sanitized = input.replace(/[^A-Za-z0-9:]/g, '');
  // Validate length
  if (sanitized.length > 15) {
    throw new ValidationError('Symbol too long');
  }
  return sanitized;
}

function sanitizeQuery(input) {
  // Remove potential injection characters
  const sanitized = input
    .replace(/[<>]/g, '')
    .replace(/['"]/g, '')
    .trim();
  // Limit length
  return sanitized.substring(0, 500);
}
```

### Certificate Validation

All HTTPS connections must validate certificates:

```javascript
const https = require('https');

const agent = new https.Agent({
  rejectUnauthorized: true,
  cert: fs.readFileSync('./certs/client.crt'),
  key: fs.readFileSync('./certs/client.key')
});
```

---

*Document Version: 1.0.0*
*Last Updated: 2026-04-27*
*Maintainer: CTO-data Team*
