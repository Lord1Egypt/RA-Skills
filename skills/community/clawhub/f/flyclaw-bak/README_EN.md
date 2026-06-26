# FlyClaw - Flight Information Aggregation CLI Tool

**FlyClaw** is a lightweight command-line tool that aggregates flight information (dynamics, prices, schedules, etc.) using a multi-source aggregation architecture powered by open-source libraries and free public APIs, with native Chinese/English query support and native OpenClaw skill integration, covering both Chinese domestic and international flights. Lightweight Python implementation — no browser automation, no complexity, no overhead.

Core value: A single data source is unreliable, incomplete, and limited in coverage -- FlyClaw's value lies in **aggregation, deduplication, gap-filling, and presentation**.

[中文说明](README.md)

**Author**: nuaa02@gmail.com  Xiaohongshu @深度连接
**GitHub**: [https://github.com/AI4MSE/FlyClaw](https://github.com/AI4MSE/FlyClaw)
**License**: [Apache-2.0](LICENSE)

## Features

- **Zero API Key Required**: No account registration needed, works out of the box, secure — and avoids the complexity, unreliability, and slowness of browser automation
- **Multi-Source Aggregation**: Fliggy, Google Flights, Skiplagged, FR24, Airplanes.live — five data sources queried concurrently, fetching flight status, prices, and live positions via open-source libraries and free public APIs. **Plugin architecture, infinitely extensible** — each data source is an independent module (one file under `sources/`). Special thanks to the above open data sources for providing convenience for public benefit and common needs!
- **Complementary Price Sources**: Fliggy + Google Flights + Skiplagged queried concurrently, with support for round-trip search, multiple passengers, cabin class selection, and stopover control
- **Unified Currency Output**: Defaults to CNY (Chinese Yuan), switchable to USD via `--currency usd`. Each record includes a `currency` field
- **City-Level Smart Search**: Accepts mixed Chinese/English city names and IATA codes, auto-expands to all airports ("Shanghai" → PVG+SHA), auto-filters closed/cargo-only airports
- **7000+ Airport Cache**: Covers 99% of IATA-coded airports worldwide, with Chinese/English names and aliases (AI-translated — corrections welcome)
- **Smart Retry & Early Return**: Auto-retries on transient errors, returns results early without waiting for slow sources
- **Codeshare Deduplication**: Automatically identifies and merges codeshare flights, showing only the operating carrier by default

## Quick Start

### Installation (OpenClaw)

Skill files: SKILL.md (Chinese) / SKILL_EN.md (English)
Install from the skill marketplace:

```bash
clawclub install flyclaw
```
Or share this GitHub URL with your OpenClaw assistant to install automatically.

### Installation (Non-OpenClaw)

```bash
# Create conda environment
conda create -n flyclaw python=3.11 -y
conda activate flyclaw

# Install core dependencies
pip install requests pyyaml curl_cffi flights
```

### Requirements

- Python 3.11+
- conda environment (recommended)

### Configuration

The default `config.yaml` includes recommended values and works out of the box:

```yaml
sources:
  fr24:
    enabled: true
    priority: 1
    timeout: 10
  google_flights:
    enabled: true
    priority: 2
    timeout: 15
    serpapi_key: ""  # Leave empty to skip SerpAPI; fill in to auto-enable
    retry: 2           # Smart retry on empty responses (0 = disable)
    retry_delay: 0.5   # Initial retry wait seconds
    retry_backoff: 2.0  # Retry wait multiplier (0.5 → 1.0 → 2.0s)
  skiplagged:
    enabled: true
    priority: 2
    timeout: 12
    retry: 4           # Smart retry on empty responses (0 = disable)
    retry_delay: 0.5   # Initial retry wait seconds
    retry_backoff: 2.0  # Retry wait multiplier (0.5 → 1.0 → 2.0s)
    mcp_enabled: false  # MCP experimental backend (default off); true = try MCP first then REST
    mcp_url: "https://mcp.skiplagged.com/mcp"  # MCP server URL
  airplanes_live:
    enabled: true
    priority: 3
    timeout: 6
  fast_flights:
    enabled: false  # Optional: only used with --compare flag
    timeout: 15

cache:
  dir: cache
  airport_update_days: 99999  # Auto-update disabled by default (pre-built data); 0 = disable, 30 = monthly
  airport_update_url: ""   # Custom update URL; empty = use built-in default URL

query:
  timeout: 20      # Global query timeout in seconds (per-source timeouts still apply)
  return_time: 12   # Smart return: return early when results available (seconds); 0 = disable
  filter_inactive_airports: true  # Filter out closed/non-commercial airports from multi-airport queries
  route_relay: true           # Enable route relay: auto-query price sources when flight route discovered
  relay_timeout: 8            # Relay-specific timeout in seconds (fast fail)
  relay_engines:              # Which engines to use for route relay price lookup
    google_flights: true
    skiplagged: true

output:
  format: json  # table / json
  language: both  # cn / en / both
```

### Usage Examples

```bash
# Query by flight number (multi-source concurrent)
conda run -n flyclaw python flyclaw.py query --flight CA981

# Query by flight number, filter by date
conda run -n flyclaw python flyclaw.py query --flight CA981 --date 2026-04-01

# Search by route (with prices) — city-level search covers all airports automatically
conda run -n flyclaw python flyclaw.py search --from Shanghai --to "New York" --date 2026-04-01
# Shanghai(PVG+SHA) → New York(JFK+EWR+LGA) all airport combinations

# Round-trip search
conda run -n flyclaw python flyclaw.py search --from PVG --to LAX --date 2026-04-15 --return 2026-04-25

# Business class + 2 adults
conda run -n flyclaw python flyclaw.py search --from PVG --to JFK --date 2026-04-15 --cabin business -a 2

# Nonstop + sort by price + JSON output
conda run -n flyclaw python flyclaw.py search --from PVG --to NRT --date 2026-04-15 --stops 0 --sort cheapest -o json

# Include connecting flights
conda run -n flyclaw python flyclaw.py search --from PVG --to JFK --date 2026-04-15 --stops any

# Disable route relay
conda run -n flyclaw python flyclaw.py query --flight CA981 --no-relay

# Chinese input is also supported
conda run -n flyclaw python flyclaw.py search --from 上海 --to 纽约 --date 2026-04-01

# Verbose mode (show data sources and cabin info)
conda run -n flyclaw python flyclaw.py query --flight CA981 -v

# Custom timeout
conda run -n flyclaw python flyclaw.py query --flight CA981 --timeout 10 --return-time 5

# Update airport data
conda run -n flyclaw python flyclaw.py update-airports --url http://example.com/airports.json
```

### Search Parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--from` | — | (required) | Origin (IATA/Chinese/English) |
| `--to` | — | (required) | Destination |
| `--date` | `-d` | — | Travel date YYYY-MM-DD |
| `--return` | `-r` | — | Return date (enables round-trip) |
| `--adults` | `-a` | 1 | Number of adult passengers |
| `--children` | — | 0 | Number of children |
| `--infants` | — | 0 | Number of infants |
| `--cabin` | `-C` | economy | Cabin: economy/premium/business/first |
| `--limit` | `-l` | No limit | Maximum results (returns all by default, truncates when specified) |
| `--sort` | `-s` | — | Sort: cheapest/fastest/departure/arrival |
| `--stops` | — | 0 | Stop control: 0=nonstop/1/2/any |
### Debug Features (for developers, regular users can ignore)

These features are for development debugging only and require additional optional dependencies. **OpenClaw skill users should NOT install** mcp, fast-flights, or playwright debug dependencies.

**MCP backend** is experimental and disabled by default (`mcp_enabled: false`). It adds ~8s handshake latency and is not needed for regular use.

**Cross-verification**: `--compare` flag compares fli vs fast-flights v3 results with flight number matching:

```bash
# Requires: pip install fast-flights>=3.0rc0
conda run -n flyclaw python flyclaw.py search --from PVG --to CAN --date 2026-04-01 --compare
```

**Browser baseline verification**: `--browser` with `--compare` launches Playwright browser for three-way verification:

```bash
# Requires: pip install playwright && playwright install chromium
conda run -n flyclaw python flyclaw.py search --from PVG --to CAN --date 2026-04-01 --compare --browser
```

Without fast-flights / playwright installed, `--compare` / `--browser` will show install instructions without affecting normal usage.

### Sample Output

```
  CA981  (Air China)
  Beijing(PEK) -> New York(JFK)
  Departure: 2026-04-01 13:00    Arrival: 2026-04-01 14:30
  Price: $856 | Stops: 0 | Duration: 840min
```

Round-trip output:
```
  CA981  (Air China)
  Shanghai(PVG) -> Los Angeles(LAX)
  Departure: 2026-04-15 10:00    Arrival: 2026-04-15 14:00
  Price: $2400 (round-trip) | Stops: 0 | Duration: 840min
  ── Return ──
  CA982  (Air China)
  Departure: 2026-04-25 18:00    Arrival: 2026-04-26 22:00
  Stops: 0 | Duration: 900min
```

## Data Sources

FlyClaw uses a multi-source aggregation architecture powered by open-source libraries and free public APIs. No API key required. Please comply with local laws when using the data.

## Dependencies and Licenses

| Dependency | Version | License | Purpose |
|-----------|---------|---------|---------|
| requests | >=2.28.0 | Apache-2.0 | HTTP requests |
| pyyaml | >=6.0 | MIT | YAML config parsing |
| curl_cffi | >=0.5.0 | MIT | Skiplagged API requests |
| flights (fli) | latest | MIT | Google Flights queries (required, GF enabled by default) |
| mcp | >=1.26.0 | MIT | Skiplagged MCP backend (experimental, default off, not needed for regular use) |
| fast-flights | >=3.0rc0 | MIT | --compare cross-verification (optional, debug) |
| playwright | latest | Apache-2.0 | --compare --browser browser verification (optional, debug) |

Python: 3.11+

## Disclaimer

- Multi-source aggregation powered by open-source libraries and free public APIs
- **No API key required** for all core features
- For study and research purposes only. Please comply with local laws
- Google Flights may not be available in some regions (e.g. mainland China)
- Prices from different data sources (Google Flights, Skiplagged) may vary (tax-inclusive/exclusive, cabin differences) — for reference only
- No personal data is collected, stored, or transmitted

## License

[Apache-2.0](LICENSE) | nuaa02@gmail.com
