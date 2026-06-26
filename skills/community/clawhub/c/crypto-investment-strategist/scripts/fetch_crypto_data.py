#!/usr/bin/env python3
"""
Crypto Data Fetcher - HYBRID VERSION
Fetches real-time cryptocurrency data with multiple API fallbacks

Priority:
1. Binance API (detailed trading data, multiple timeframes)
2. CoinGecko API (fallback, no geo-blocking)

Usage:
    python fetch_crypto_data.py --symbol BTC
    python fetch_crypto_data.py --symbol ETH --timeframe 1h --limit 100
"""

import argparse
import json
import ssl
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional


class DataSource:
    """Base class for data sources"""

    @staticmethod
    def _fetch(url: str, headers: dict = None) -> dict:
        """Make HTTP GET request"""
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            req.add_header('Accept', 'application/json')

            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)

            # Create SSL context that works on macOS
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)

        except urllib.error.HTTPError as e:
            # Try to read response body for more details
            try:
                error_body = e.read().decode('utf-8')
                error_json = json.loads(error_body)
                msg = error_json.get('msg', str(error_json))
                return {'error': f'HTTP {e.code}: {msg}'}
            except:
                return {'error': f'HTTP {e.code}: {e.reason}'}
        except urllib.error.URLError as e:
            return {'error': f'Connection: {e.reason}'}
        except Exception as e:
            return {'error': str(e)}


class BinanceAPI(DataSource):
    """Binance Spot API - Primary data source with detailed trading data"""

    # Alternative endpoints to try (api1-4 better performance, api-gcp most stable)
    BASE_URLS = [
        "https://api.binance.com",
        "https://api-gcp.binance.com",
        "https://data-api.binance.vision",  # Market data only, no geo-blocking
    ]

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        """Convert symbol to Binance format (BTCUSDT)"""
        symbol = symbol.upper().replace('/', '').replace('-', '').replace('USDT', '').strip()
        return f"{symbol}USDT"

    def _try_endpoints(self, endpoint: str) -> dict:
        """Try multiple Binance endpoints until one works"""
        last_error = None
        for i, base_url in enumerate(self.BASE_URLS):
            url = f"{base_url}{endpoint}"
            data = self._fetch(url)
            if 'error' not in data:
                return data
            last_error = data.get('error', '')
            # Check if it's a geo-blocking error - try next endpoint
            if any(phrase in last_error.lower() for phrase in ['restricted location', 'eligible', '418', '403']):
                continue
            # Other errors (invalid symbol, etc) - return immediately
            return data
        return {'error': last_error or 'All endpoints failed'}

    def get_ticker(self, symbol: str) -> Dict:
        """Get 24hr ticker statistics"""
        binance_symbol = self._normalize_symbol(symbol)
        endpoint = f"/api/v3/ticker/24hr?symbol={binance_symbol}"

        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        return {
            'exchange': 'binance',
            'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
            'timestamp': datetime.now().isoformat(),
            'price': float(data.get('lastPrice', 0)),
            'bid': float(data.get('bidPrice', 0)),
            'ask': float(data.get('askPrice', 0)),
            'bidQty': float(data.get('bidQty', 0)),
            'askQty': float(data.get('askQty', 0)),
            'open_24h': float(data.get('openPrice', 0)),
            'high_24h': float(data.get('highPrice', 0)),
            'low_24h': float(data.get('lowPrice', 0)),
            'volume_24h': float(data.get('volume', 0)),
            'volume_24h_usd': float(data.get('quoteVolume', 0)),
            'change_24h': float(data.get('priceChange', 0)),
            'change_24h_pct': float(data.get('priceChangePercent', 0)),
            'trades_count': int(data.get('count', 0)),
            'open_time': data.get('openTime'),
            'close_time': data.get('closeTime'),
        }

    def get_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 100) -> Dict:
        """Get Kline/candlestick data"""
        binance_symbol = self._normalize_symbol(symbol)

        # Map intervals
        interval_map = {
            '1s': '1s', '1m': '1m', '3m': '3m', '5m': '5m', '15m': '15m', '30m': '30m',
            '1h': '1h', '2h': '2h', '4h': '4h', '6h': '6h', '8h': '8h', '12h': '12h',
            '1d': '1d', '3d': '3d', '1w': '1w', '1M': '1M'
        }

        interval = interval_map.get(interval, interval)

        endpoint = f"/api/v3/klines?symbol={binance_symbol}&interval={interval}&limit={min(limit, 1000)}"
        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        candles = []
        for candle in data:
            candles.append({
                'timestamp': datetime.fromtimestamp(candle[0] / 1000).isoformat(),
                'open': float(candle[1]),
                'high': float(candle[2]),
                'low': float(candle[3]),
                'close': float(candle[4]),
                'volume': float(candle[5]),
                'close_time': candle[6],
                'quote_volume': float(candle[7]),
                'trades': int(candle[8]),
                'taker_buy_base': float(candle[9]),
                'taker_buy_quote': float(candle[10]),
            })

        if candles:
            latest = candles[-1]
            first = candles[0]
            change = ((latest['close'] - first['open']) / first['open']) * 100

            return {
                'exchange': 'binance',
                'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
                'timeframe': interval,
                'candles_count': len(candles),
                'latest_price': latest['close'],
                'period_change_pct': round(change, 2),
                'candles': candles,
            }

        return {'error': 'No candle data'}

    def get_orderbook(self, symbol: str, limit: int = 100) -> Dict:
        """Get order book depth"""
        binance_symbol = self._normalize_symbol(symbol)
        endpoint = f"/api/v3/depth?symbol={binance_symbol}&limit={limit}"

        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        return {
            'exchange': 'binance',
            'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
            'lastUpdateId': data.get('lastUpdateId'),
            'bids': [[float(p), float(q)] for p, q in data.get('bids', [])[:20]],
            'asks': [[float(p), float(q)] for p, q in data.get('asks', [])[:20]],
        }


class BinanceFuturesAPI(DataSource):
    """Binance USDT-M Futures API - For leverage trading analysis"""

    BASE_URLS = [
        "https://fapi.binance.com",
        "https://fapi-gcp.binance.com",
        "https://data-api.binance.vision",
    ]

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        """Convert symbol to Binance Futures format (BTCUSDT)"""
        symbol = symbol.upper().replace('/', '').replace('-', '').replace('USDT', '').strip()
        return f"{symbol}USDT"

    def _try_endpoints(self, endpoint: str) -> dict:
        """Try multiple Binance Futures endpoints until one works"""
        last_error = None
        for base_url in self.BASE_URLS:
            url = f"{base_url}{endpoint}"
            data = self._fetch(url)
            if 'error' not in data:
                return data
            last_error = data.get('error', '')
            if any(phrase in last_error.lower() for phrase in ['restricted location', 'eligible', '418', '403']):
                continue
            return data
        return {'error': last_error or 'All endpoints failed'}

    def get_ticker(self, symbol: str) -> Dict:
        """Get 24hr ticker statistics from futures"""
        binance_symbol = self._normalize_symbol(symbol)
        endpoint = f"/fapi/v1/ticker/24hr?symbol={binance_symbol}"

        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        return {
            'exchange': 'binance_futures',
            'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
            'timestamp': datetime.now().isoformat(),
            'price': float(data.get('lastPrice', 0)),
            'bid': float(data.get('bidPrice', 0)),
            'ask': float(data.get('askPrice', 0)),
            'open_24h': float(data.get('openPrice', 0)),
            'high_24h': float(data.get('highPrice', 0)),
            'low_24h': float(data.get('lowPrice', 0)),
            'volume_24h': float(data.get('volume', 0)),
            'volume_24h_usd': float(data.get('quoteVolume', 0)),
            'change_24h': float(data.get('priceChange', 0)),
            'change_24h_pct': float(data.get('priceChangePercent', 0)),
            'trades_count': int(data.get('count', 0)),
            'mark_price': float(data.get('markPrice', 0)),
            'index_price': float(data.get('indexPrice', 0)),
            'open_interest': float(data.get('openInterest', 0)),
        }

    def get_funding_rate(self, symbol: str) -> Dict:
        """Get current funding rate"""
        binance_symbol = self._normalize_symbol(symbol)
        endpoint = f"/fapi/v1/fundingRate?symbol={binance_symbol}&limit=1"

        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        if not data:
            return {'error': 'No funding rate data'}

        latest = data[-1]
        return {
            'exchange': 'binance_futures',
            'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
            'funding_rate': float(latest.get('fundingRate', 0)),
            'funding_time': latest.get('fundingTime'),
            'mark_price': float(latest.get('markPrice', 0)),
        }

    def get_open_interest(self, symbol: str) -> Dict:
        """Get open interest history"""
        binance_symbol = self._normalize_symbol(symbol)
        endpoint = f"/fapi/v1/openInterest?symbol={binance_symbol}"

        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        return {
            'exchange': 'binance_futures',
            'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
            'open_interest': float(data.get('openInterest', 0)),
            'timestamp': data.get('time'),
        }

    def get_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 100) -> Dict:
        """Get Kline/candlestick data from futures"""
        binance_symbol = self._normalize_symbol(symbol)

        interval_map = {
            '1m': '1m', '3m': '3m', '5m': '5m', '15m': '15m', '30m': '30m',
            '1h': '1h', '2h': '2h', '4h': '4h', '6h': '6h', '8h': '8h', '12h': '12h',
            '1d': '1d', '3d': '3d', '1w': '1w', '1M': '1M'
        }

        interval = interval_map.get(interval, interval)

        endpoint = f"/fapi/v1/klines?symbol={binance_symbol}&interval={interval}&limit={min(limit, 1500)}"
        data = self._try_endpoints(endpoint)

        if 'error' in data:
            return data

        candles = []
        for candle in data:
            candles.append({
                'timestamp': datetime.fromtimestamp(candle[0] / 1000).isoformat(),
                'open': float(candle[1]),
                'high': float(candle[2]),
                'low': float(candle[3]),
                'close': float(candle[4]),
                'volume': float(candle[5]),
                'close_time': candle[6],
                'quote_volume': float(candle[7]),
                'trades': int(candle[8]),
                'taker_buy_base': float(candle[9]),
                'taker_buy_quote': float(candle[10]),
            })

        if candles:
            latest = candles[-1]
            first = candles[0]
            change = ((latest['close'] - first['open']) / first['open']) * 100

            return {
                'exchange': 'binance_futures',
                'symbol': f"{binance_symbol[:-4]}/{binance_symbol[-4:]}",
                'timeframe': interval,
                'candles_count': len(candles),
                'latest_price': latest['close'],
                'period_change_pct': round(change, 2),
                'candles': candles,
            }

        return {'error': 'No candle data'}


class CoinGeckoAPI(DataSource):
    """CoinGecko API - Fallback with no geo-blocking"""

    BASE_URL = "https://api.coingecko.com/api/v3"

    SYMBOL_MAP = {
        # Major cryptocurrencies
        'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin',
        'SOL': 'solana', 'XRP': 'ripple', 'ADA': 'cardano',
        'DOGE': 'dogecoin', 'DOT': 'polkadot', 'MATIC': 'matic-network',
        'LINK': 'chainlink', 'AVAX': 'avalanche-2', 'UNI': 'uniswap',
        'ATOM': 'cosmos', 'LTC': 'litecoin', 'BCH': 'bitcoin-cash',
        'XLM': 'stellar', 'ALGO': 'algorand', 'VET': 'vechain',
        'FIL': 'filecoin', 'ICP': 'internet-computer', 'NEAR': 'near',
        'AAVE': 'aave', 'MKR': 'maker', 'COMP': 'compound-governance-token',
        # Stablecoins & Gold tokens
        'USDT': 'tether', 'USDC': 'usd-coin', 'DAI': 'dai',
        'BUSD': 'binance-usd', 'USDD': 'usdd', 'FRAX': 'frax',
        'PAXG': 'pax-gold', 'XAUT': 'tether-gold',
        # Layer 2 & Scaling
        'ARB': 'arbitrum', 'OP': 'optimism', 'MATIC': 'matic-network',
        # DeFi Bluechips
        'CRV': 'curve-dao-token', 'SNX': 'synthetix-network-token',
        'YFI': 'yearn-finance', 'SUSHI': 'sushi',
        # Exchange tokens
        'KCS': 'kucoin-shares', 'GT': 'gate-token', 'HT': 'huobi-token',
    }

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        symbol = symbol.upper().replace('/', '').replace('-', '').replace('USDT', '').strip()
        return CoinGeckoAPI.SYMBOL_MAP.get(symbol, symbol.lower())

    def get_ticker(self, symbol: str) -> Dict:
        """Get current price and market data"""
        coin_id = self._normalize_symbol(symbol)
        endpoint = f"/coins/{coin_id}?localization=false&tickers=false&community_data=false&developer_data=false"

        data = self._fetch(f"{self.BASE_URL}{endpoint}")

        if 'error' in data:
            return {'error': f'Coin not found: {symbol}'}

        market = data.get('market_data', {})

        return {
            'exchange': 'coingecko',
            'symbol': f"{data.get('symbol', '').upper()}/USDT",
            'coin_id': coin_id,
            'name': data.get('name'),
            'timestamp': datetime.now().isoformat(),
            'price': market.get('current_price', {}).get('usd'),
            'high_24h': market.get('high_24h', {}).get('usd'),
            'low_24h': market.get('low_24h', {}).get('usd'),
            'volume_24h_usd': market.get('total_volume', {}).get('usd'),
            'change_24h': market.get('price_change_24h'),
            'change_24h_pct': market.get('price_change_percentage_24h'),
            'market_cap_usd': market.get('market_cap', {}).get('usd'),
            'rank': market.get('market_cap_rank'),
            'ath': market.get('ath', {}).get('usd'),
        }

    def get_ohlcv(self, symbol: str, days: int = 7) -> Dict:
        """Get historical price data (daily only)"""
        coin_id = self._normalize_symbol(symbol)
        endpoint = f"/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"

        data = self._fetch(f"{self.BASE_URL}{endpoint}")

        if 'error' in data:
            return data

        prices = data.get('prices', [])
        volumes = data.get('total_volumes', [])

        candles = []
        for i, (ts, price) in enumerate(prices):
            volume = volumes[i][1] if i < len(volumes) else 0
            candles.append({
                'timestamp': datetime.fromtimestamp(ts / 1000).isoformat(),
                'open': price,
                'high': price,
                'low': price,
                'close': price,
                'volume': volume,
            })

        return {
            'exchange': 'coingecko',
            'symbol': f"{symbol.upper()}/USDT",
            'timeframe': 'daily',
            'candles': candles,
        }


class HybridDataFetcher:
    """Tries Binance first, falls back to CoinGecko"""

    def __init__(self):
        self.binance = BinanceAPI()
        self.binance_futures = BinanceFuturesAPI()
        self.coingecko = CoinGeckoAPI()

    def get_ticker(self, symbol: str) -> Dict:
        """Try Binance first, fallback to CoinGecko"""
        # Try Binance
        data = self.binance.get_ticker(symbol)

        if 'error' in data:
            # Fallback to CoinGecko
            print(f"[INFO] Binance unavailable, trying CoinGecko...", file=sys.stderr)
            data = self.coingecko.get_ticker(symbol)

        return data

    def get_ohlcv(self, symbol: str, interval: str = '1h', limit: int = 100) -> Dict:
        """Try Binance first, fallback to CoinGecko (daily only)"""
        # Try Binance
        data = self.binance.get_ohlcv(symbol, interval, limit)

        if 'error' in data:
            # Fallback to CoinGecko (daily data only)
            print(f"[INFO] Binance unavailable, trying CoinGecko (daily data)...", file=sys.stderr)

            # Convert interval to days
            days_map = {'1d': 7, '4h': 7, '1h': 7, '1w': 30}
            days = days_map.get(interval, 7)

            data = self.coingecko.get_ohlcv(symbol, days)

        return data

    def get_market_summary(self, symbol: str) -> Dict:
        """Get comprehensive market summary"""
        ticker = self.get_ticker(symbol)

        if 'error' in ticker:
            return ticker

        # Get OHLCV data
        ohlcv_1h = self.get_ohlcv(symbol, interval='1h', limit=24)
        ohlcv_1d = self.get_ohlcv(symbol, interval='1d', limit=7)

        result = {
            'exchange': ticker['exchange'],
            'symbol': ticker['symbol'],
            'timestamp': ticker['timestamp'],
            'current_price': ticker['price'],
            'change_24h_pct': ticker.get('change_24h_pct'),
            'volume_24h_usd': ticker.get('volume_24h_usd'),
            'high_24h': ticker.get('high_24h'),
            'low_24h': ticker.get('low_24h'),
        }

        # Add exchange-specific fields
        if ticker['exchange'] == 'binance':
            result['bid'] = ticker.get('bid')
            result['ask'] = ticker.get('ask')
            result['trades_count'] = ticker.get('trades_count')
        elif ticker['exchange'] == 'coingecko':
            result['coin_id'] = ticker.get('coin_id')
            result['name'] = ticker.get('name')
            result['market_cap_usd'] = ticker.get('market_cap_usd')
            result['rank'] = ticker.get('rank')

        # Add OHLCV data
        result['hourly_data'] = ohlcv_1h.get('candles', [])[-24:] if 'candles' in ohlcv_1h else []
        result['daily_data'] = ohlcv_1d.get('candles', [])[-7:] if 'candles' in ohlcv_1d else []

        return result

    def get_futures_ticker(self, symbol: str) -> Dict:
        """Get futures ticker data (falls back to spot data if futures unavailable)"""
        data = self.binance_futures.get_ticker(symbol)
        if 'error' in data:
            # Fallback to spot data with a note
            spot_data = self.binance.get_ticker(symbol)
            if 'error' not in spot_data:
                spot_data['exchange'] = 'binance_spot'
                spot_data['note'] = 'Futures API unavailable, using spot data as proxy'
                return spot_data
            return data
        return data

    def get_funding_rate(self, symbol: str) -> Dict:
        """Get current funding rate for leverage trading"""
        data = self.binance_futures.get_funding_rate(symbol)
        if 'error' in data:
            return {'error': f'Funding rate unavailable (API restricted): Consider using spot price trends as proxy'}
        return data

    def get_open_interest(self, symbol: str) -> Dict:
        """Get open interest data"""
        data = self.binance_futures.get_open_interest(symbol)
        if 'error' in data:
            return {'error': f'Open interest unavailable (API restricted): Use volume as proxy'}
        return data

    def get_leverage_analysis(self, symbol: str) -> Dict:
        """Get comprehensive leverage trading analysis"""
        # Try futures data first
        futures_ticker = self.get_futures_ticker(symbol)
        funding = self.get_funding_rate(symbol)
        oi = self.get_open_interest(symbol)

        # Get spot OHLCV data for trend analysis (always available via data-api.binance.vision)
        ohlcv_1h = self.binance.get_ohlcv(symbol, interval='1h', limit=48)
        ohlcv_4h = self.binance.get_ohlcv(symbol, interval='4h', limit=24)

        # Calculate trend metrics from spot data
        trend_metrics = {}
        if 'candles' in ohlcv_4h and ohlcv_4h['candles']:
            candles = ohlcv_4h['candles']
            latest = candles[-1]

            # Simple trend analysis
            highs = [c['high'] for c in candles]
            lows = [c['low'] for c in candles]
            closes = [c['close'] for c in candles]

            trend_metrics = {
                'current_price': latest['close'],
                'trend_4h': 'up' if closes[-1] > closes[0] else 'down',
                'price_range_4h': max(highs) - min(lows),
                'volatility': round((max(highs) - min(lows)) / latest['close'] * 100, 2),
            }

        result = {
            'symbol': symbol.upper() + '/USDT',
            'timestamp': datetime.now().isoformat(),
            'futures_data': futures_ticker if 'error' not in futures_ticker else None,
            'funding_rate': funding if 'error' not in funding else None,
            'open_interest': oi if 'error' not in oi else None,
            'trend_metrics': trend_metrics,
            'candles_1h': ohlcv_1h.get('candles', [])[-24:] if 'candles' in ohlcv_1h else [],
            'candles_4h': ohlcv_4h.get('candles', [])[-12:] if 'candles' in ohlcv_4h else [],
        }

        return result


def list_symbols():
    """List all supported trading symbols"""
    symbols = CoinGeckoAPI.SYMBOL_MAP
    categories = {
        'Major': ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'MATIC', 'LINK'],
        'DeFi': ['AVAX', 'UNI', 'ATOM', 'AAVE', 'MKR', 'COMP', 'CRV', 'SNX', 'YFI'],
        'Stablecoins': ['USDT', 'USDC', 'DAI', 'BUSD', 'USDD', 'FRAX'],
        'Gold Tokens': ['PAXG', 'XAUT'],
        'Layer 2': ['ARB', 'OP'],
        'Exchange': ['KCS', 'GT', 'HT'],
    }

    print("\n📊 Supported Trading Symbols:\n")
    for category, syms in categories.items():
        available = [s for s in syms if s in symbols]
        if available:
            print(f"{category}: {', '.join(available)}")

    print(f"\nTotal: {len(symbols)} symbols supported")
    print("\n💡 You can also use any Binance listing directly (e.g., PAXG, BNB, etc.)")
    print("💡 Format: Use symbol without USDT (e.g., 'BTC' not 'BTCUSDT')\n")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Hybrid Crypto Data Fetcher (Binance Spot + Futures + CoinGecko fallback)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fetch_crypto_data.py --symbol BTC
  python fetch_crypto_data.py --symbol ETH --mode ticker
  python fetch_crypto_data.py --symbol SOL --mode ohlcv --timeframe 1h --limit 50
  python fetch_crypto_data.py --symbol BTC --mode futures
  python fetch_crypto_data.py --symbol ETH --mode funding
  python fetch_crypto_data.py --symbol PAXG --mode summary
  python fetch_crypto_data.py --list-symbols

Timeframes (Binance): 1s, 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w
  Note: CoinGecko fallback only provides daily data
        """
    )

    parser.add_argument('--symbol', '-s', required=False,
                       help='Symbol (e.g., BTC, ETH, SOL, PAXG)')
    parser.add_argument('--mode', '-m', default='summary',
                       choices=['ticker', 'ohlcv', 'summary', 'orderbook', 'futures', 'funding', 'leverage'],
                       help='Data mode [default: summary]')
    parser.add_argument('--timeframe', '-t', default='1h',
                       help='Timeframe for OHLCV [default: 1h]')
    parser.add_argument('--limit', '-l', type=int, default=100,
                       help='Number of candles [default: 100, max: 1000]')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--list-symbols', '--list', action='store_true',
                       help='List all supported symbols')

    args = parser.parse_args()

    # Handle list-symbols flag
    if args.list_symbols:
        list_symbols()
        sys.exit(0)

    # Require symbol for other modes
    if not args.symbol:
        parser.error("--symbol is required (unless using --list-symbols)")

    try:
        fetcher = HybridDataFetcher()

        if args.mode == 'ticker':
            data = fetcher.get_ticker(args.symbol)
        elif args.mode == 'ohlcv':
            data = fetcher.get_ohlcv(args.symbol, args.timeframe, args.limit)
        elif args.mode == 'orderbook':
            data = fetcher.binance.get_orderbook(args.symbol)
        elif args.mode == 'futures':
            data = fetcher.get_futures_ticker(args.symbol)
        elif args.mode == 'funding':
            data = fetcher.get_funding_rate(args.symbol)
        elif args.mode == 'leverage':
            data = fetcher.get_leverage_analysis(args.symbol)
        else:  # summary
            data = fetcher.get_market_summary(args.symbol)

        # Output
        json_output = json.dumps(data, indent=2)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"✓ Data saved to {args.output}", file=sys.stderr)
        else:
            print(json_output)

        if 'error' in data:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
