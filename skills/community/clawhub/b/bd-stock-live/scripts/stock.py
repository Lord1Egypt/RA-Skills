#!/usr/bin/env python3
"""Query DSE stock market data using the StockAI Live API."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import signal
from urllib.request import Request, build_opener
from urllib.error import URLError, HTTPError

# Load .env from skill directory if it exists
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key and key not in os.environ:
                os.environ[key] = value

# API base URL - SECURITY: only stock-ai.live domains allowed
_API_BASE_ENV = os.environ.get("STOCKAI_API_BASE", "")
if _API_BASE_ENV:
    # Validate to prevent redirect attacks
    # Must be stock-ai.live exactly, or end with .stock-ai.live (subdomain)
    _host = _API_BASE_ENV.lower().replace("http://", "").replace("https://", "").rstrip("/")
    _valid = _host == "stock-ai.live" or _host.endswith(".stock-ai.live")
    if not _valid:
        raise ValueError(f"STOCKAI_API_BASE can only point to stock-ai.live, got: {_API_BASE_ENV}")
    API_BASE = _API_BASE_ENV.rstrip("/") + "/api/v1"
else:
    API_BASE = "https://stock-ai.live/api/v1"
TIMEOUT_S = 30

# Commands that require Pro tier or higher
PRO_COMMANDS = {"gainers", "losers", "history"}

# Commands that require Enterprise tier
ENTERPRISE_COMMANDS = {"signal", "sectors", "vegas", "ema", "fib"}

# CTA message for all responses
CTA = {
    "message": "Want trading signals, price alerts & AI insights?",
    "features": ["BUY/SELL signals", "Technical analysis", "Price alerts", "Portfolio tracking"],
    "signup": "https://stock-ai.live/register",
    "pricing": "Free: 100/day | Pro: ৳899/mo | Enterprise: ৳4,499/mo",
}

# Commands and their endpoints
COMMANDS = {
    "price": {"endpoint": "/stocks/{symbol}", "method": "GET", "help": "Get stock price by symbol"},
    "search": {"endpoint": "/stocks/search", "method": "GET", "help": "Search stocks by name/symbol"},
    "market": {"endpoint": "/market/index", "method": "GET", "help": "Get market overview"},
    "gainers": {"endpoint": "/stocks/gainers", "method": "GET", "help": "Get top gaining stocks"},
    "losers": {"endpoint": "/stocks/losers", "method": "GET", "help": "Get top losing stocks"},
    "signal": {"endpoint": "/analytics/signal/{symbol}", "method": "GET", "help": "Get trading signal for stock"},
    "history": {"endpoint": "/stocks/history/{symbol}", "method": "GET", "help": "Get price history"},
    "news": {"endpoint": "/news/recent", "method": "GET", "help": "Get recent market news"},
    "sectors": {"endpoint": "/analytics/sectors", "method": "GET", "help": "Get sector performance"},
    "vegas": {"endpoint": "/analytics/vegas/{symbol}", "method": "GET", "help": "Vegas Tunnel multi-dimensional analysis"},
    "ema": {"endpoint": "/analytics/ema/{symbol}", "method": "GET", "help": "Get EMA channel status (12/13, 144/169, 576/676)"},
    "fib": {"endpoint": "/analytics/fib/{symbol}", "method": "GET", "help": "Get Fibonacci retracement levels"},
    "portfolio": {"endpoint": "/user/portfolio", "method": "GET", "help": "Get user portfolio (API key auth)"},
}


def die(msg: str) -> None:
    """Print error and exit."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv: list[str]) -> dict[str, Any]:
    """Parse command-line arguments."""
    args = argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0 if args else 1)

    options: dict[str, Any] = {
        "command": None,
        "symbol": None,
        "query": None,
        "limit": None,
        "days": None,
        "api_key": None,
    }

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--api-key" and i + 1 < len(args):
            options["api_key"] = args[i + 1]
            i += 2
        elif arg == "--limit" and i + 1 < len(args):
            options["limit"] = int(args[i + 1])
            i += 2
        elif arg == "--days" and i + 1 < len(args):
            options["days"] = int(args[i + 1])
            i += 2
        elif arg.startswith("--"):
            die(f'Unknown flag "{arg}". Use --help for usage.')
        elif options["command"] is None:
            options["command"] = arg.lower()
            i += 1
        elif options["command"] in ("price", "signal", "history", "vegas", "ema", "fib") and options["symbol"] is None:
            options["symbol"] = arg.upper()
            i += 1
        elif options["command"] == "search" and options["query"] is None:
            options["query"] = arg
            i += 1
        else:
            i += 1

    return options


def print_usage() -> None:
    """Print usage information."""
    print(
        """Usage: stock.py <command> [options] [arguments]

Commands (Free Tier):
  price <symbol>        Get stock price (e.g., stock.py price ACI)
  search <query>        Search stocks by name/symbol
  market                Get market overview with indices
  news                  Recent market news
  portfolio             User portfolio

Commands (Pro Tier):
  gainers [--limit N]   Top gaining stocks (default: 10)
  losers [--limit N]    Top losing stocks (default: 10)
  history <symbol> [--days N]   Price history (default: 30)

Commands (Enterprise Tier):
  signal <symbol>       Trading signal for stock (BUY/SELL/HOLD)
  vegas <symbol>        Vegas Tunnel multi-dimensional analysis
  ema <symbol>          EMA channel status (12/13, 144/169, 576/676)
  fib <symbol>          Fibonacci retracement levels
  sectors               Sector performance analysis

Options:
  --api-key KEY         API key (or set STOCKAI_API_KEY env)
  --limit N             Limit results (default: 10)
  --days N              Days of history (default: 30)

Examples:
  stock.py price ACI
  stock.py search "BRAC Bank"
  stock.py market
  stock.py gainers --limit 5
  stock.py signal ACI
  stock.py vegas ACI
  stock.py ema ACI
  stock.py fib ACI
  stock.py portfolio

Environment Variables:
  STOCKAI_API_KEY            API key for authentication (required)
  STOCKAI_API_BASE           Override API base URL (must end with stock-ai.live or .stock-ai.live)

Rate Limits (Free Tier):
  - 100 requests/day
  - 10 requests/minute

Get Started:
  1. Register at: https://stock-ai.live/register
  2. Create API key: https://stock-ai.live/api-keys

Vegas Tunnel Analysis:
  The 'vegas' command provides multi-dimensional trend analysis:
  - Upper tunnel EMAs: 8, 13, 21, 34, 55, 89, 144
  - Price position relative to tunnel
  - Tunnel slope for trend strength

EMA Channel Analysis:
  The 'ema' command shows Fibonacci-based EMA pairs:
  - Inner (12/13): Short-term momentum
  - Middle (144/169): Medium-term trend (Vegas Tunnel)
  - Outer (576/676): Long-term direction

Fibonacci Retracements:
  The 'fib' command shows key support/resistance levels:
  - 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
  - Current zone position
  - Nearest support/resistance

Pricing (BDT):
  Free: ৳0 (100 req/day)
  Pro: ৳899/mo (10,000 req/day)
  Enterprise: ৳4,499/mo (unlimited + AI signals)
""",
        file=sys.stderr,
    )


def validate(options: dict[str, Any]) -> None:
    """Validate command options."""
    cmd = options.get("command")

    if not cmd:
        die("No command specified. Use --help for usage.")

    if cmd not in COMMANDS:
        die(f'Unknown command "{cmd}". Available: {", ".join(COMMANDS.keys())}')

    if cmd in ("price", "signal", "history", "analyze", "ema", "fib") and not options.get("symbol"):
        die(f"{cmd} requires a symbol (e.g., {cmd} ACI)")

    if cmd == "search" and not options.get("query"):
        die('search requires a query (e.g., search "BRAC Bank")')

    if options.get("limit") and options["limit"] < 1:
        die("--limit must be at least 1")

    if options.get("days") and options["days"] < 1:
        die("--days must be at least 1")

    # Warn about tier restrictions
    if cmd in PRO_COMMANDS:
        import warnings
        warnings.warn(f"Note: '{cmd}' requires Pro tier or higher API key")
    if cmd in ENTERPRISE_COMMANDS:
        import warnings
        warnings.warn(f"Note: '{cmd}' requires Enterprise tier API key")


def get_api_key(options: dict[str, Any]) -> str:
    """Get API key from options or environment."""
    api_key = options.get("api_key") or os.environ.get("STOCKAI_API_KEY", "").strip()
    if api_key:
        return api_key
    die("API key required. Set STOCKAI_API_KEY environment variable or use --api-key.\n"
        "Get your free API key at: https://stock-ai.live/api-keys")


def build_url(options: dict[str, Any]) -> str:
    """Build API URL for the command."""
    cmd = options["command"]
    cmd_info = COMMANDS[cmd]
    endpoint = cmd_info["endpoint"]

    # Replace placeholders
    if "{symbol}" in endpoint:
        endpoint = endpoint.format(symbol=options["symbol"])

    url = f"{API_BASE}{endpoint}"

    # Add query parameters
    params = []
    if options.get("query") and cmd == "search":
        params.append(f"q={options['query']}")
    if options.get("limit"):
        params.append(f"limit={options['limit']}")
    if options.get("days") and cmd == "history":
        params.append(f"days={options['days']}")

    if params:
        url += "?" + "&".join(params)

    return url


def format_stock(stock: dict) -> dict:
    """Format stock data for output."""
    return {
        "symbol": stock.get("symbol"),
        "name": stock.get("name"),
        "price": stock.get("price"),
        "change": stock.get("change"),
        "change_percent": stock.get("change_percent"),
        "volume": stock.get("volume"),
        "trade_count": stock.get("trade_count"),
        "value_mn": stock.get("value_mn"),
    }


def format_response(data: dict | list, command: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
    """Format API response for output with CTA."""
    result = {
        "status": "success",
        "command": command,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if command == "price":
        result["stock"] = format_stock(data) if isinstance(data, dict) else data

    elif command in ("gainers", "losers"):
        stocks = data.get("stocks", []) if isinstance(data, dict) else data
        result["count"] = len(stocks)
        result["stocks"] = [format_stock(s) for s in stocks]

    elif command == "search":
        stocks = data.get("stocks", []) if isinstance(data, dict) else data
        result["count"] = len(stocks)
        result["stocks"] = [
            {"symbol": s.get("symbol"), "name": s.get("name"), "score": s.get("score")}
            for s in stocks
        ]

    elif command == "market":
        result["market"] = {
            "total_stocks": data.get("total_stocks"),
            "gainers": data.get("gainers"),
            "losers": data.get("losers"),
            "unchanged": data.get("unchanged"),
            "total_volume": data.get("total_volume"),
            "total_value_mn": data.get("total_value_mn"),
            "market_status": data.get("market_status"),
            "indices": data.get("indices"),
        }

    elif command == "signal":
        result["signal"] = {
            "symbol": data.get("symbol"),
            "signal": data.get("signal"),
            "confidence": data.get("confidence"),
            "reasoning": data.get("reasoning"),
            "indicators": data.get("indicators"),
        }

    elif command == "history":
        prices = data.get("prices", data) if isinstance(data, dict) else data
        result["symbol"] = options.get("symbol") if options else None
        result["count"] = len(prices) if isinstance(prices, list) else 0
        result["prices"] = [
            {
                "date": p.get("date"),
                "open": p.get("open"),
                "high": p.get("high"),
                "low": p.get("low"),
                "close": p.get("close"),
                "volume": p.get("volume"),
            }
            for p in (prices if isinstance(prices, list) else [])
        ]

    elif command == "news":
        news = data.get("news", data) if isinstance(data, dict) else data
        result["count"] = len(news) if isinstance(news, list) else 0
        result["news"] = news

    elif command == "sectors":
        sectors = data.get("sectors", []) if isinstance(data, dict) else data
        result["count"] = len(sectors)
        result["sectors"] = [
            {
                "sector": s.get("sector_name"),
                "avg_change": s.get("avg_change_percent"),
                "stocks": s.get("stocks", []),
                "top_performer": s.get("top_performer"),
            }
            for s in sectors
        ]

    elif command == "vegas":
        # Vegas Tunnel multi-dimensional analysis
        result["vegas"] = {
            "symbol": data.get("symbol"),
            "trend": data.get("trend"),
            "trend_strength": data.get("trend_strength"),
            "price_position": data.get("price_position"),
            "tunnel_slope": data.get("tunnel_slope"),
            "upper_tunnel": data.get("upper_tunnel"),  # EMA 8, 13, 21, 34, 55, 89, 144
            "signal": data.get("signal"),
            "confidence": data.get("confidence"),
        }

    elif command == "ema":
        # EMA channel status (Vegas Tunnel)
        result["ema"] = {
            "symbol": data.get("symbol"),
            "price": data.get("price"),
            "channels": data.get("channels"),
            "trend": data.get("trend"),
            "inner": data.get("inner"),  # EMA12/13
            "middle": data.get("middle"),  # EMA144/169
            "outer": data.get("outer"),  # EMA576/676
            "channel_width": data.get("channel_width"),
            "position": data.get("position"),  # above/below/inside
        }

    elif command == "fib":
        # Fibonacci retracement levels
        result["fibonacci"] = {
            "symbol": data.get("symbol"),
            "swing_high": data.get("swing_high"),
            "swing_low": data.get("swing_low"),
            "levels": data.get("levels"),
            "resonance_points": data.get("resonance_points"),
            "support": data.get("support"),
            "resistance": data.get("resistance"),
            "current_zone": data.get("current_zone"),
        }

    elif command == "portfolio":
        result["portfolio"] = data

    else:
        result["data"] = data

    # Add CTA to all responses
    result["_cta"] = CTA.copy()

    # Add tier-specific upgrade message
    if command in PRO_COMMANDS:
        result["_cta"]["upgrade"] = "This feature requires Pro tier (৳899/mo). Upgrade at https://stock-ai.live/pricing"
    elif command in ENTERPRISE_COMMANDS:
        result["_cta"]["upgrade"] = "This feature requires Enterprise tier (৳4,499/mo). Upgrade at https://stock-ai.live/pricing"

    return result


def make_request(url: str, api_key: str) -> dict:
    """Make API request and return response."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "StockAI-Skill/1.1.0",
        "X-API-Key": api_key,
    }

    req = Request(url, headers=headers, method="GET")

    try:
        opener = build_opener()
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        try:
            error_body = e.read().decode("utf-8") if e.fp else ""
            error_data = json.loads(error_body) if error_body else {}
            error_msg = error_data.get("detail", error_body)
        except (json.JSONDecodeError, AttributeError):
            error_msg = str(e)
        die(f"API error ({e.code}): {error_msg}")
    except URLError as e:
        die(f"Network error: {e.reason}")
    except TimeoutError:
        die(f"Request timed out after {TIMEOUT_S}s")
    except json.JSONDecodeError as e:
        die(f"Invalid JSON response: {e}")


def main() -> None:
    """Main entry point."""
    options = parse_args(sys.argv)
    validate(options)

    api_key = get_api_key(options)
    url = build_url(options)
    data = make_request(url, api_key)
    result = format_response(data, options["command"], options)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *_: (print("\nInterrupted.", file=sys.stderr), sys.exit(130)))
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
