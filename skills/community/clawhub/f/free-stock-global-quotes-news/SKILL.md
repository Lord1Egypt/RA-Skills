---
name: free-stock-global-quotes-news
description: "global-quotes: free stock quotes and news. Use when: user asks for global stock price, quote, ticker symbol, or company news for US (e.g. AAPL), HK (0700.HK), or China A-shares (000001.SZ, 600000.SS). Uses free sources: Yahoo/Finnhub for US, Tencent/EastMoney/AkShare for CN/HK."
metadata:
  openclaw:
    emoji: "📈"
    requires: { bins: ["python3"] }
  env:
    optional:
      - FINNHUB_API_KEY
      - HTTPS_PROXY
      - HTTP_PROXY
  optionalDeps: ["akshare"]
---

# Yahoo Finance Skill

Get quotes and basic market data from Yahoo Finance (no API key).

## When to Use

- "苹果股价" / "AAPL 价格" / "特斯拉今天涨了多少"
- "港股腾讯" / "0700.HK 行情"
- "茅台股价" / "600519.SS" / "000001.SZ 平安银行"
- Any request for stock quote, current price, or day change
- 美股公司新闻：用 `scripts/news.py`（需 FINNHUB_API_KEY）

## Symbol Format

| Market   | Example    | Format   |
|----------|------------|----------|
| US       | AAPL, MSFT | Ticker   |
| Hong Kong| 0700.HK    | Code.HK  |
| Shanghai | 600519.SS  | Code.SS  |
| Shenzhen | 000001.SZ  | Code.SZ  |

## Commands

### A-shares / HK quotes (CN/HK, no keys; 腾讯→东财→AkShare)

Use `cn_quote.py` for A 股 / 港股，依次尝试 **腾讯行情 → 东方财富 Push2 → AkShare**，直到某个可用就停止。

```bash
# A-shares
python3 scripts/cn_quote.py 600519.SS
python3 scripts/cn_quote.py 000001.SZ
python3 scripts/cn_quote.py 300750.SZ

# HK stocks
python3 scripts/cn_quote.py 0700.HK
python3 scripts/cn_quote.py hk00700
```

- 无需任何 API key。
- 优先使用腾讯行情 (`qt.gtimg.cn`)，失败时尝试东方财富 Push2 接口（仅 A 股），再尝试本地安装的 AkShare（如果存在）。

### Single or multiple quotes (unified entry: US + A-share/HK)

**一个脚本覆盖美股与 A 股/港股**：`quote.py` 会根据 symbol 自动选择数据源——A 股/港股（`*.SS` / `*.SZ` / `*.HK` 等）走 cn_quote（腾讯→东财→AkShare），美股及其他走 Yahoo/Finnhub。Agent 只需调 `scripts/quote.py` 即可。

```bash
python3 scripts/quote.py AAPL
python3 scripts/quote.py 0700.HK 9988.HK
python3 scripts/quote.py 600519.SS 000001.SZ
```

### With time range (for previous close / context)

```bash
python3 scripts/quote.py AAPL --range 5d
python3 scripts/quote.py MSFT --range 1mo
```

### JSON output

```bash
python3 scripts/quote.py AAPL --json
```

### Company news（新闻：A股/港股 东方财富→AkShare；美股 Finnhub）

**A股/港股**：依次使用 **东方财富 → AkShare**，直到某个可用即停（无需 API key，服务器需安装 AkShare）。  
**美股**：使用 Finnhub，需设置 `FINNHUB_API_KEY`。

```bash
# A 股 / 港股
python3 scripts/news.py 600519.SS
python3 scripts/news.py 贵州茅台 --limit 5
python3 scripts/news.py 0700.HK

# 美股
python3 scripts/news.py AAPL
python3 scripts/news.py MSFT --limit 5 --from 2025-02-01 --to 2025-02-25
```

- `--limit`：最多返回条数，默认 10。
- `--from` / `--to`：日期 YYYY-MM-DD（仅美股 Finnhub 使用），默认最近 7 天。
- `--json`：输出原始 JSON。
- **港股个股新闻**：AkShare 对港股个股新闻支持有限，可能返回空，属正常情况。

### Range options (quote)

- `1d` — today (default)
- `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`

## Path

From the skill directory (e.g. workspace `skills/yahoo-finance/`):

```bash
python3 scripts/quote.py <SYMBOL> [--range 1d|5d|1mo|...] [--json]
```

From workspace root, use the full path to the skill's `scripts/quote.py` so the agent can invoke it via `exec`.

## Server 403 (e.g. datacenter IP blocked by Yahoo)

On servers, Yahoo often returns 403. Two options:

1. **Finnhub fallback (recommended)**  
   Free API key at https://finnhub.io. Set `FINNHUB_API_KEY` in the environment (e.g. in `~/.openclaw/.env` or your process env). The script will use Finnhub when Yahoo returns 403. US symbols (AAPL, MSFT) work; HK/CN symbols may differ.

2. **Proxy（代理）**  
   脚本会读取环境变量 `HTTPS_PROXY`、`HTTP_PROXY`，请求会经代理发出，可避免机房 IP 被 Yahoo 封。

   **优先：用户/进程级**（仅影响当前 skill，推荐）  
   在 gateway 可读到的环境里设置即可，例如 `~/.openclaw/.env` 中加入 `HTTPS_PROXY=...` 和 `HTTP_PROXY=...`。或当前 shell 测试：`export HTTPS_PROXY=http://127.0.0.1:7890` 后执行 `python3 scripts/quote.py AAPL`。

   **可选：systemd 全局**（仅当你用 systemd 跑 gateway 且希望所有请求走代理时）  
   编辑 `/etc/systemd/system/openclaw-gateway.service` 在 `[Service]` 下增加 `Environment=HTTPS_PROXY=...` / `HTTP_PROXY=...`，然后 `sudo systemctl daemon-reload && sudo systemctl restart openclaw-gateway`。注意这会对该服务下所有请求生效。

**可选环境变量**（仅 `quote.py`）：`OPENCLAW_QUOTE_TIMEOUT`（默认 12 秒）、`OPENCLAW_QUOTE_RETRY_DELAY`（单 symbol 顺序时的间隔，默认 0.4 秒）、`OPENCLAW_QUOTE_CACHE_TTL`（结果缓存秒数，0=关闭）。多 symbol 时默认**并行**请求以提升性能，可通过 `OPENCLAW_QUOTE_PARALLEL=0` 关闭；`OPENCLAW_QUOTE_MAX_WORKERS`（默认 6）控制并行度。**失败重试**：`quote.py` 单次 HTTP 请求默认最多重试 2 次（共 3 次），5xx/超时/断线会指数退避；可通过 `OPENCLAW_QUOTE_RETRIES=0` 关闭。`cn_quote.py` 与 `news.py` 同样对单次请求做最多 2 次重试。

## Notes

- Yahoo: real-time/near-real-time for **美股 / 港股 / A 股**，但在服务器机房 IP 上可能 403，需要配合代理使用。
- Finnhub fallback: 只保证 **美股**（AAPL/MSFT 等）有稳定数据；A 股 / 港股 在免费档通常无有效行情或直接 403。
- 建议：港股 / A 股 查询优先走 Yahoo（必要时加 HTTPS_PROXY），美股在 Yahoo 403 时可以用 Finnhub 作为备份。

## 可改进点 (Possible improvements)

- **测试**：对解析逻辑做单元测试（mock HTTP），便于改版不 regression。
- **cn_quote 港股**：AkShare 单股接口仅 A 股；港股仍走腾讯/东财，无单股历史接口时保持现状。
