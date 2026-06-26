# Known Use Cases (KUC)

Total: **40**

## `KUC-101`
**Source**: `examples/demo.py`

Demonstrates how to define and use async callback handlers for receiving real-time market data updates from cryptocurrency exchanges.

## `KUC-102`
**Source**: `examples/demo_arctic.py`

Stores cryptocurrency trade, funding, and ticker data to ArcticDB (Arctic) time-series database for persistence and later analysis.

## `KUC-103`
**Source**: `examples/demo_bequant_bitcoincom_hitbtc.py`

Demonstrates each supported features (ticker, trades, order book, candles) for Bequant and HitBTC exchanges which share the same API.

## `KUC-104`
**Source**: `examples/demo_binance_authenticated.py`

Demonstrates authenticated access to Binance, Binance Delivery, and Binance Futures for receiving account balances, positions, and order updates in real-time.

## `KUC-105`
**Source**: `examples/demo_binance_delivery.py`

Shows data subscription for Binance Delivery perpetual futures including order book, ticker, and trade data.

## `KUC-106`
**Source**: `examples/demo_binancetr.py`

Demonstrates data subscription for Binance TR exchange including ticker, trades, order book with delta updates, and candle data.

## `KUC-107`
**Source**: `examples/demo_bitfinex_authenticated.py`

Demonstrates synchronous authenticated Bitfinex trading operations including balance queries, order management, and trade execution.

## `KUC-108`
**Source**: `examples/demo_bybit_authenticated.py`

Demonstrates Bybit authenticated feeds for receiving order updates and trade fills in real-time for account monitoring.

## `KUC-109`
**Source**: `examples/demo_check_trade_timestamps.py`

Monitors and compares trade timestamps across multiple exchanges to verify timestamp consistency and identify potential synchronization issues.

## `KUC-110`
**Source**: `examples/demo_concurrent_proxy.py`

Demonstrates using HTTP proxy to bypass exchange rate limits when subscribing to many symbols, enabling concurrent order book and open interest data collection.

## `KUC-111`
**Source**: `examples/demo_custom_agg.py`

Demonstrates custom aggregation of trade data over time windows, tracking min/max prices for each symbol within the aggregation period.

## `KUC-112`
**Source**: `examples/demo_deribit_authenticated.py`

Demonstrates Deribit authenticated feeds for order info, trade fills, and balance updates for comprehensive account monitoring.

## `KUC-113`
**Source**: `examples/demo_elastic.py`

Stores order book, funding, and trade data to Elasticsearch for search and analytics capabilities.

## `KUC-114`
**Source**: `examples/demo_existing_loop.py`

Demonstrates integrating cryptofeed with an existing asyncio event loop, allowing concurrent execution with other async tasks.

## `KUC-115`
**Source**: `examples/demo_gateiofutures.py`

Demonstrates subscription to Gate.io futures exchange for ticker, trades, order book, funding, and candle data.

## `KUC-116`
**Source**: `examples/demo_gcppubsub.py`

Publishes trade data to Google Cloud Platform Pub/Sub for event-driven architectures and cloud-based processing.

## `KUC-117`
**Source**: `examples/demo_influxdb.py`

Stores funding, order book, trades, ticker, and candles to InfluxDB time-series database for monitoring and analysis.

## `KUC-118`
**Source**: `examples/demo_kafka.py`

Streams order book and trade data to Apache Kafka with custom topic and partition routing for scalable event processing.

## `KUC-119`
**Source**: `examples/demo_liquidations.py`

Monitors and displays liquidations across each exchanges that support this channel, useful for identifying market stress and volatility.

## `KUC-120`
**Source**: `examples/demo_loop.py`

Demonstrates dynamic addition of feeds to a running event loop and scheduled callbacks for adding/removing feeds over time.

## `KUC-121`
**Source**: `examples/demo_mongo.py`

Stores order book, trades, and ticker data to MongoDB document database with flexible schema for JSON storage.

## `KUC-122`
**Source**: `examples/demo_multicb.py`

Demonstrates registering multiple callback handlers for a single data channel, enabling parallel processing of the same data.

## `KUC-123`
**Source**: `examples/demo_nbbo.py`

Calculates National Best Bid and Offer (NBBO) by aggregating best bid/ask prices across Coinbase, Gemini, and Kraken for a given symbol.

## `KUC-124`
**Source**: `examples/demo_ohlcv.py`

Aggregates trade data into OHLCV (Open, High, Low, Close, Volume) candles over configurable time windows for charting.

## `KUC-125`
**Source**: `examples/demo_okx_authenticated.py`

Demonstrates authenticated OKX exchange for receiving real-time order updates for account monitoring.

## `KUC-126`
**Source**: `examples/demo_playback.py`

Plays back historical market data from captured PCAP files through the callback system for backtesting and analysis.

## `KUC-127`
**Source**: `examples/demo_postgres.py`

Stores comprehensive market data (candles, index, ticker, trades, open interest, liquidations, funding, order books) to PostgreSQL with custom column mapping.

## `KUC-128`
**Source**: `examples/demo_quasardb.py`

Stores ticker, trades, candles, open interest, index, and liquidation data to QuasarDB for high-performance time-series analytics.

## `KUC-129`
**Source**: `examples/demo_questdb.py`

Stores order book, candles, funding, ticker, and trade data to QuestDB for high-performance time-series database operations.

## `KUC-130`
**Source**: `examples/demo_rabbitmq_exchange.py`

Publishes order book data to RabbitMQ using topic exchange routing for flexible message filtering and distribution.

## `KUC-131`
**Source**: `examples/demo_rabbitmq_queue.py`

Publishes order book data to RabbitMQ using queue-based delivery for point-to-point message distribution.

## `KUC-132`
**Source**: `examples/demo_raw_data.py`

Collects raw WebSocket data to files for offline analysis, debugging, or historical data preservation.

## `KUC-133`
**Source**: `examples/demo_redis.py`

Stores trades, funding, candles, order books, open interest, and ticker data to Redis with both pub/sub and persistent storage backends.

## `KUC-134`
**Source**: `examples/demo_renko.py`

Transforms trade data into Renko chart bricks based on fixed price movements for trend visualization independent of time.

## `KUC-135`
**Source**: `examples/demo_tcp.py`

Streams trade data over TCP sockets for network-based data distribution to remote systems or applications.

## `KUC-136`
**Source**: `examples/demo_throttle.py`

Limits the rate of order book callbacks to a specified number per time window, useful for managing downstream system load.

## `KUC-137`
**Source**: `examples/demo_udp.py`

Streams order book and trade data over UDP datagrams for low-latency network distribution to remote systems.

## `KUC-138`
**Source**: `examples/demo_uds.py`

Streams ticker and trade data over Unix domain sockets for high-performance inter-process communication on the same host.

## `KUC-139`
**Source**: `examples/demo_victoriametrics.py`

Stores trade, ticker, order book, and candle data to VictoriaMetrics for Prometheus-compatible time-series monitoring and analytics.

## `KUC-140`
**Source**: `examples/demo_zmq.py`

Publishes order book and ticker data over ZeroMQ pub/sub for lightweight message distribution to multiple subscribers.
