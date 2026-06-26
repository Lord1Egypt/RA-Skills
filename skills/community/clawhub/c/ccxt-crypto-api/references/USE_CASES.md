# Known Use Cases (KUC)

Total: **100**

## `KUC-101`
**Source**: `examples/bots/py/bitfinex-lending-bot.py`

Automates cryptocurrency lending on Bitfinex by checking for lending opportunities and executing market orders to deploy funds into lending markets.

## `KUC-102`
**Source**: `examples/bots/py/spot-arbitrage-bot.py`

Scans multiple exchanges (OKX, Bybit, Binance, KuCoin, BitMart, Gate.io) for price discrepancies in spot markets and executes arbitrage trades.

## `KUC-103`
**Source**: `examples/ccxt.pro/py/binance-create-order-cancel-order.py`

Demonstrates creating a limit order on Binance and then canceling it, useful for testing order workflows.

## `KUC-104`
**Source**: `examples/ccxt.pro/py/binance-fetch-balance-snapshot-watch-balance-updates.py`

Captures initial balance snapshot and continuously monitors for balance updates via WebSocket, printing changes when they occur.

## `KUC-105`
**Source**: `examples/ccxt.pro/py/binance-futures-watch-balance.py`

Continuously watches futures, delivery, and spot balances on Binance simultaneously using asyncio.

## `KUC-106`
**Source**: `examples/ccxt.pro/py/binance-futures-watch-order-book.py`

Streams real-time order book updates for BTC/USDT futures contract on Binance.

## `KUC-107`
**Source**: `examples/ccxt.pro/py/binance-futures.py`

Continuously monitors and prints order book updates with timestamps for BTC/USDT on Binance.

## `KUC-108`
**Source**: `examples/ccxt.pro/py/binance-reload-markets.py`

Periodically reloads market data from Binance while simultaneously watching order books, ensuring market data stays current.

## `KUC-109`
**Source**: `examples/ccxt.pro/py/binance-spot-and-futures.py`

Watches multiple order books across different market types (spot, futures) and displays them together.

## `KUC-110`
**Source**: `examples/ccxt.pro/py/binance-watch-many-orderbooks.py`

Subscribes to order book updates for multiple trading pairs simultaneously on Binance, printing each updates.

## `KUC-111`
**Source**: `examples/ccxt.pro/py/binance-watch-margin-balance.py`

Monitors margin account balance changes on Binance via WebSocket, printing updates when margin positions change.

## `KUC-112`
**Source**: `examples/ccxt.pro/py/binance-watch-ohlcv.py`

Streams real-time OHLCV (candlestick) data for ETH/USDT on Binance with configurable timeframe and limit.

## `KUC-113`
**Source**: `examples/ccxt.pro/py/binance-watch-order-book-individual-updates.py`

Captures and displays individual high-frequency order book updates by subclassing Binance exchange to intercept messages.

## `KUC-114`
**Source**: `examples/ccxt.pro/py/binance-watch-orderbook-watch-balance.py`

Simultaneously monitors order book and balance updates, displaying them together with common handler logic.

## `KUC-115`
**Source**: `examples/ccxt.pro/py/binance-watch-orders-being-placed.py`

Watches active orders and balance updates while also placing delayed orders to demonstrate order lifecycle monitoring.

## `KUC-116`
**Source**: `examples/ccxt.pro/py/binance-watch-spot-futures-balances-continuously.py`

Continuously monitors balance across multiple Binance accounts (spot, USD-M futures, COIN-M futures) and prints each currency totals.

## `KUC-117`
**Source**: `examples/ccxt.pro/py/bitmex_watch_ohlcv.py`

Streams real-time OHLCV candlestick data for BTC/USD perpetual contract on Bitmex with formatted table output.

## `KUC-118`
**Source**: `examples/ccxt.pro/py/bitmex_watch_ticker_and_ohlcv.py`

Simultaneously streams ticker data and OHLCV candlesticks on Bitmex with color-coded output for visual distinction.

## `KUC-119`
**Source**: `examples/ccxt.pro/py/bitvavo-watch-order-book.py`

Streams real-time order book updates for BTC/EUR on Bitvavo European exchange with nonce verification.

## `KUC-120`
**Source**: `examples/ccxt.pro/py/build-ohlcv-many-symbols.py`

Constructs OHLCV candlesticks from individual trades for multiple symbols, supporting both complete and incomplete candles.

## `KUC-121`
**Source**: `examples/ccxt.pro/py/coinbase-watch-all-trades.py`

Watches each trade updates on Coinbase for BTC/USD and tracks the last trade ID to avoid duplicates.

## `KUC-122`
**Source**: `examples/ccxt.pro/py/coinbase-watch-trades.py`

Streams trade data for BTC/USD on Coinbase, printing latest trade with count of cached trades.

## `KUC-123`
**Source**: `examples/ccxt.pro/py/consume-all-trades.py`

Continuously consumes and prints each trade updates for BTC/USD on Bitmex, clearing trade cache after processing.

## `KUC-124`
**Source**: `examples/ccxt.pro/py/gateio-watch-trades.py`

Watches trade updates on Gate.io for BTC/USDT with timestamp-based pagination to fetch incremental updates.

## `KUC-125`
**Source**: `examples/ccxt.pro/py/intercept-original-ohlcv-updates.py`

Subclasses Binance to intercept and process raw OHLCV WebSocket messages before passing to standard handler.

## `KUC-126`
**Source**: `examples/ccxt.pro/py/kucoin-watch-multiple-orderbooks.py`

Watches order books for multiple symbols (KDA/USDT, KDA/BTC, BTC/USDT) simultaneously on KuCoin with authentication.

## `KUC-127`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-different-streams.py`

Monitors multiple data streams (order book, ticker, trades) across multiple exchanges simultaneously.

## `KUC-128`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-orderbooks-synchronized.py`

Watches order books across multiple exchanges and displays each current order books together in a synchronized view.

## `KUC-129`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-orderbooks-throttled.py`

Watches order books across multiple exchanges with throttled output every 5 seconds to manage display bandwidth.

## `KUC-130`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-streams-with-keys.py`

Advanced multi-exchange monitoring supporting both symbol-specific and global streams (like server time) with API authentication.

## `KUC-131`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-streams.py`

Watches order books for multiple symbols across OKX and Binance simultaneously using async gather patterns.

## `KUC-132`
**Source**: `examples/ccxt.pro/py/many-exchanges-many-symbols-watch-trades.py`

Streams trade data for multiple symbols across OKX and Binance with incremental updates enabled.

## `KUC-133`
**Source**: `examples/ccxt.pro/py/many-exchanges.py`

Simple example watching BTC/USDT order books across Kraken, Binance, and Bitmex simultaneously.

## `KUC-134`
**Source**: `examples/ccxt.pro/py/multiple-exchanges-watch-orderbook-continuously.py`

Monitors CELO/USD order books across Coinbase Pro, OKCoin, and Bittrex, printing when top bid changes.

## `KUC-135`
**Source**: `examples/ccxt.pro/py/okex-create-swap-order.py`

Places a market order for BTC/USDT perpetual swap contract on OKX with configurable position direction.

## `KUC-136`
**Source**: `examples/ccxt.pro/py/okex-watch-margin-balance-with-params.py`

Watches OKX margin account balance for specific symbol (BTC/USDT) using params-based approach with verbose output.

## `KUC-137`
**Source**: `examples/ccxt.pro/py/okex-watch-margin-balance.py`

Continuously monitors OKX margin account balance changes for BTC/USDT with verbose debugging enabled.

## `KUC-138`
**Source**: `examples/ccxt.pro/py/okx-bbo-tbt.py`

Streams best bid/ask data tick-by-tick on OKX for high-frequency price monitoring.

## `KUC-139`
**Source**: `examples/ccxt.pro/py/on-connected-user-hook.py`

Demonstrates WebSocket connection lifecycle hook by placing an order immediately upon connection establishment.

## `KUC-140`
**Source**: `examples/ccxt.pro/py/one-exchange-different-streams.py`

Watches both order book and trades streams simultaneously for BTC/USD on Bitstamp.

## `KUC-141`
**Source**: `examples/ccxt.pro/py/one-exchange-many-streams.py`

Watches order books for multiple symbols (BTC/USDT, ETH/USDT, ETH/BTC) on FTX exchange with throttling.

## `KUC-142`
**Source**: `examples/ccxt.pro/py/phemex-cancel-all-orders.py`

Cancels each open orders for a specific symbol (UNI/USDT) on Phemex exchange.

## `KUC-143`
**Source**: `examples/ccxt.pro/py/spot-vs-future-arbitrage-bitmart.py`

Monitors both spot and futures order books on BitMart to detect arbitrage opportunities between the two markets.

## `KUC-144`
**Source**: `examples/ccxt.pro/py/watch-all-symbols.py`

Watches order books for each available trading pairs on Kraken, printing every 100th update to manage output.

## `KUC-145`
**Source**: `examples/ccxt.pro/py/watch-custom-exchange-specific-streams.py`

Implements custom WebSocket handler for Binance mini ticker stream not natively supported in CCXT Pro.

## `KUC-146`
**Source**: `examples/ccxt.pro/py/watch-many-exchanges-many-tickers.py`

Streams ticker data (bid/ask/last) for multiple symbols across Binance and FTX simultaneously.

## `KUC-147`
**Source**: `examples/ccxt.pro/py/watch-ticker-to-csv.py`

Streams ticker data for multiple symbols and writes results to CSV files for historical analysis.

## `KUC-148`
**Source**: `examples/py/aiohttp-custom-session-connector.py`

Configures CCXT async support to use SOCKS proxy for exchanges that require it for connectivity.

## `KUC-149`
**Source**: `examples/py/all-exchanges.py`

Lists each cryptocurrency exchanges supported by the CCXT library for discovery purposes.

## `KUC-150`
**Source**: `examples/py/arbitrage-pairs.py`

Scans multiple exchanges to find arbitrage opportunities by comparing prices across different trading pairs.

## `KUC-151`
**Source**: `examples/py/asciichart.py`

Provides terminal-based charting capability to visualize price data using ASCII art.

## `KUC-152`
**Source**: `examples/py/async-analyse-augur-v1-vs-v2-exchanges.py`

Compares trading pairs across Augur v1 and v2 exchanges to identify differences in available markets.

## `KUC-153`
**Source**: `examples/py/async-balance-coinbasepro.py`

Fetches account balance from Coinbase Pro exchange using sandbox environment for testing.

## `KUC-154`
**Source**: `examples/py/async-balance-gdax.py`

Fetches account balance from GDAX (Coinbase) exchange using sandbox mode.

## `KUC-155`
**Source**: `examples/py/async-balance.py`

Fetches account balance from Bittrex exchange asynchronously.

## `KUC-156`
**Source**: `examples/py/async-balances.py`

Fetches balances from multiple exchanges (Kraken, Bitfinex) concurrently.

## `KUC-157`
**Source**: `examples/py/async-basic-callchain.py`

Demonstrates sequential async operations pattern: load markets, fetch ticker, fetch order book on multiple exchanges.

## `KUC-158`
**Source**: `examples/py/async-basic-orderbook.py`

Fetches order book data from OKX exchange asynchronously.

## `KUC-159`
**Source**: `examples/py/async-basic-rate-limiter.py`

Demonstrates CCXT's built-in rate limiting by making 100 consecutive API calls without hitting exchange limits.

## `KUC-160`
**Source**: `examples/py/async-basic.py`

Simple example demonstrating async market loading from Binance exchange.

## `KUC-161`
**Source**: `examples/py/async-binance-cancel-option-order.py`

Cancels a specific options order on Binance using the implicit API for options trading.

## `KUC-162`
**Source**: `examples/py/async-binance-create-margin-order.py`

Places a limit buy order on Binance using margin trading account type.

## `KUC-163`
**Source**: `examples/py/async-binance-create-option-order.py`

Places a call options order on Binance USDT Options market.

## `KUC-164`
**Source**: `examples/py/async-binance-create-trailing-percent-order.py`

Places a trailing percent stop order on Binance USD-M futures with reduce-only flag.

## `KUC-165`
**Source**: `examples/py/async-binance-fetch-margin-balance-with-options.py`

Fetches margin account balance from Binance using options-based configuration.

## `KUC-166`
**Source**: `examples/py/async-binance-fetch-margin-balance-with-params.py`

Fetches Binance margin balance using params-based approach specifying type.

## `KUC-167`
**Source**: `examples/py/async-binance-fetch-option-OHLCV.py`

Fetches historical candlestick data for Binance options contracts.

## `KUC-168`
**Source**: `examples/py/async-binance-fetch-option-details.py`

Fetches options market details (mark price, etc.) from Binance using implicit API.

## `KUC-169`
**Source**: `examples/py/async-binance-fetch-option-order.py`

Fetches open options orders from Binance with pagination support.

## `KUC-170`
**Source**: `examples/py/async-binance-fetch-option-orderbook.py`

Fetches options order book from Binance USDT Options market.

## `KUC-171`
**Source**: `examples/py/async-binance-fetch-option-position.py`

Fetches options position information from Binance.

## `KUC-172`
**Source**: `examples/py/async-binance-fetch-option-ticker.py`

Fetches ticker/price information for Binance options contracts.

## `KUC-173`
**Source**: `examples/py/async-binance-fetch-ticker-continuously.py`

Continuously fetches ticker data from Binance with error handling and retry logic for robustness.

## `KUC-174`
**Source**: `examples/py/async-binance-futures-vs-spot.py`

Compares account data (balance, orders, trades) between Binance spot and futures accounts.

## `KUC-175`
**Source**: `examples/py/async-binance-margin-borrow.py`

Borrows cryptocurrency from Binance margin account for trading or other purposes.

## `KUC-176`
**Source**: `examples/py/async-binance-margin-repay.py`

Repays borrowed cryptocurrency on Binance margin account to reduce margin debt.

## `KUC-177`
**Source**: `examples/py/async-binance-usdm-fetch-continuous-klines-ohlcv.py`

Fetches continuous klines (perpetual contract) data from Binance USD-M futures.

## `KUC-178`
**Source**: `examples/py/async-bitfinex-public-get-symbols.py`

Fetches list of trading symbols available on Bitfinex exchange via public API.

## `KUC-179`
**Source**: `examples/py/async-bitget-perpetual-futures-swaps.py`

Places perpetual swap orders and fetches balance on Bitget exchange with API authentication.

## `KUC-180`
**Source**: `examples/py/async-bitstamp-create-limit-buy-order.py`

Places a limit buy order on Bitstamp exchange with configurable price and amount.

## `KUC-181`
**Source**: `examples/py/async-bitstamp-create-order-cancel-order.py`

Places a sell limit order on Bitstamp then cancels it, demonstrating full order lifecycle.

## `KUC-182`
**Source**: `examples/py/async-bittrex-orderbook.py`

Async generator that continuously polls order book data from Bittrex exchange.

## `KUC-183`
**Source**: `examples/py/async-bybit-transfer.py`

Fetches transfer history and executes internal transfers between Bybit account wallets (spot, derivatives, options).

## `KUC-184`
**Source**: `examples/py/async-fetch-balance.py`

Simple async example to fetch account balance from Bitstamp exchange.

## `KUC-185`
**Source**: `examples/py/async-fetch-many-orderbooks-continuously.py`

Continuously fetches order books for multiple symbols across OKX and Binance exchanges.

## `KUC-186`
**Source**: `examples/py/async-fetch-ohlcv-indicators-discord-webhook.py`

Fetches OHLCV data, calculates RSI indicator, and sends alerts to Discord when RSI conditions are met.

## `KUC-187`
**Source**: `examples/py/async-fetch-ohlcv-multiple-symbols-continuously.py`

Continuously fetches latest OHLCV candles for multiple symbols on Binance in a loop.

## `KUC-188`
**Source**: `examples/py/async-fetch-order-book-from-many-exchanges.py`

Fetches order book from multiple exchanges (Binance, KuCoin, Huobi) concurrently for the same symbol.

## `KUC-189`
**Source**: `examples/py/async-fetch-ticker.py`

Simple one-liner to fetch current ticker price from Binance.

## `KUC-190`
**Source**: `examples/py/async-gather-concurrency.py`

Demonstrates concurrent API calls using asyncio.gather to fetch order books from multiple symbols efficiently.

## `KUC-191`
**Source**: `examples/py/async-gdax-fetch-order-book-continuously.py`

Continuously polls order book data from Binance (mislabeled as GDAX in example) in a while loop.

## `KUC-192`
**Source**: `examples/py/async-generator-basic.py`

Demonstrates async generator pattern to continuously yield ticker data from Poloniex.

## `KUC-193`
**Source**: `examples/py/async-generator-multiple-tickers.py`

Async generator that cycles through multiple tickers on Kraken with round-robin approach.

## `KUC-194`
**Source**: `examples/py/async-generator-ticker-poller.py`

Authenticated async generator that polls BTC/USD ticker from Kraken continuously.

## `KUC-195`
**Source**: `examples/py/async-hollaex-sandbox.py`

Tests Hollaex API connectivity using sandbox mode with test API keys.

## `KUC-196`
**Source**: `examples/py/async-instantiate-all-at-once.py`

Creates instances of each CCXT-supported exchanges and demonstrates accessing one.

## `KUC-197`
**Source**: `examples/py/async-kucoin-rate-limit.py`

Demonstrates robust OHLCV fetching from KuCoin with proper rate limit handling and retry logic.

## `KUC-198`
**Source**: `examples/py/async-macd.py`

Calculates MACD (Moving Average Convergence Divergence) indicator on live OHLCV data for trading decisions.

## `KUC-199`
**Source**: `examples/py/async-market-making-symbols.py`

Scans each exchanges to find symbols with 0% maker fees, useful for market making strategies.

## `KUC-200`
**Source**: `examples/py/async-multiple-accounts.py`

Manages multiple exchange accounts simultaneously, fetching balance data from each account.
