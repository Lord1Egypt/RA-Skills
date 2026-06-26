#!/usr/bin/env bash
# Bitpanda Developer API CLI
# Requires: curl, BITPANDA_API_KEY env var
set -euo pipefail

BASE_URL="https://developer.bitpanda.com"

_CLEANUP_DIRS=()
cleanup() { if [ ${#_CLEANUP_DIRS[@]} -gt 0 ]; then for d in "${_CLEANUP_DIRS[@]}"; do rm -rf "$d"; done; fi; }
trap cleanup EXIT

die() { echo "Error: $1" >&2; exit 1; }

require_api_key() {
  if [ -z "${BITPANDA_API_KEY:-}" ]; then
    die "BITPANDA_API_KEY environment variable is not set. Get one at https://web.bitpanda.com/my-account/apikey"
  fi
}

api_get() {
  local path="$1"; shift
  local query=""
  while [ $# -gt 0 ]; do
    local key="$1" val="$2"; shift 2
    if [ -n "$val" ]; then query="${query:+${query}&}${key}=${val}"; fi
  done
  local url="${BASE_URL}${path}${query:+?${query}}"
  local http_code body
  body=$(curl -s -w '\n%{http_code}' -H "X-Api-Key: ${BITPANDA_API_KEY}" "$url")
  http_code=$(echo "$body" | tail -n1)
  body=$(echo "$body" | sed '$d')
  if [ "$http_code" -lt 200 ] || [ "$http_code" -ge 300 ]; then
    die "API request failed (HTTP ${http_code}): ${url%%\?*} — ${body}"
  fi
  echo "$body"
}

# Fetch all prices from the paginated ticker API
# Returns a JSON object: { "SYMBOL": { "price": "...", "currency": "...", "price_change_day": "...", "type": "..." }, ... }
fetch_all_ticker_prices() {
  require_api_key
  local all_data="[]"
  local cursor=""
  while true; do
    local resp
    resp=$(api_get "/v1/ticker" "page_size" "500" "cursor" "$cursor") || break
    local page_data
    page_data=$(echo "$resp" | jq -c '.data')
    all_data=$(echo "$all_data" "$page_data" | jq -sc '.[0] + .[1]')
    local has_next
    has_next=$(echo "$resp" | jq -r '.has_next_page')
    [ "$has_next" = "true" ] || break
    cursor=$(echo "$resp" | jq -r '.next_cursor')
  done
  echo "$all_data" | jq 'map({key: .symbol, value: {price: .price, currency: .currency, price_change_day: .price_change_day, type: .type}}) | from_entries'
}

cmd_price() {
  local symbol="${1:?Usage: bitpanda.sh price <SYMBOL>}"
  local ticker
  ticker=$(fetch_all_ticker_prices)
  echo "$ticker" | jq -r --arg s "$symbol" '.[$s] // "not found"'
}

cmd_prices() {
  local all=false
  while [ $# -gt 0 ]; do
    case "$1" in
      --all) all=true; shift;;
      *) die "Unknown option: $1";;
    esac
  done
  local ticker
  ticker=$(fetch_all_ticker_prices)
  if $all; then
    echo "$ticker"
  else
    # Save ticker to a temp file so portfolio reuses it instead of fetching again
    local ticker_tmpdir
    ticker_tmpdir=$(mktemp -d)
    _CLEANUP_DIRS+=("$ticker_tmpdir")
    echo "$ticker" > "$ticker_tmpdir/ticker.json"
    local symbols
    symbols=$(cmd_portfolio --ticker-file "$ticker_tmpdir/ticker.json" | jq -r '[.wallets[].asset_symbol] | unique | .[]')
    echo "$ticker" | jq --argjson syms "$(echo "$symbols" | jq -R . | jq -sc .)" \
      'with_entries(select(.key as $k | $syms | index($k)))'
  fi
}

cmd_balances() {
  require_api_key
  local asset_id="" index_asset_id="" before="" after="" page_size="" non_zero=false
  while [ $# -gt 0 ]; do
    case "$1" in
      --asset-id) asset_id="$2"; shift 2;;
      --index-asset-id) index_asset_id="$2"; shift 2;;
      --before) before="$2"; shift 2;;
      --after) after="$2"; shift 2;;
      --page-size) page_size="$2"; shift 2;;
      --non-zero) non_zero=true; shift;;
      *) die "Unknown option: $1";;
    esac
  done
  local result
  result=$(api_get "/v1/wallets/" \
    "asset_id" "$asset_id" "index_asset_id" "$index_asset_id" \
    "before" "$before" "after" "$after" "page_size" "$page_size")
  if $non_zero; then
    echo "$result" | jq '.data = [.data[] | select(.balance != "0" and .balance != "0.00000000" and (.balance | tonumber) > 0)]'
  else
    echo "$result"
  fi
}

cmd_all_transactions() {
  require_api_key
  local wallet_id="" flow="" asset_id="" from="" to="" before="" after="" page_size=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --wallet-id) wallet_id="$2"; shift 2;;
      --flow) flow="$2"; shift 2;;
      --asset-id) asset_id="$2"; shift 2;;
      --from) from="$2"; shift 2;;
      --to) to="$2"; shift 2;;
      --before) before="$2"; shift 2;;
      --after) after="$2"; shift 2;;
      --page-size) page_size="$2"; shift 2;;
      *) die "Unknown option: $1";;
    esac
  done
  api_get "/v1/transactions" \
    "wallet_id" "$wallet_id" "flow" "$flow" "asset_id" "$asset_id" \
    "from_including" "$from" "to_excluding" "$to" \
    "before" "$before" "after" "$after" "page_size" "$page_size"
}

cmd_asset() {
  require_api_key
  if [ $# -lt 1 ]; then die "Usage: bitpanda.sh asset <asset_id>"; fi
  local asset_id="$1"
  api_get "/v1/assets/${asset_id}"
}

cmd_portfolio() {
  require_api_key
  local ticker_file="" sort_by="name"
  while [ $# -gt 0 ]; do
    case "$1" in
      --ticker-file) ticker_file="$2"; shift 2;;
      --sort) sort_by="$2"; shift 2;;
      *) die "Unknown option: $1";;
    esac
  done

  local all_wallets="[]"
  local cursor=""
  local page=0

  # Auto-paginate all wallets
  while true; do
    local args=("page_size" "100")
    if [ -n "$cursor" ]; then args+=("after" "$cursor"); fi
    local result
    result=$(api_get "/v1/wallets/" "${args[@]}")
    local page_data
    page_data=$(echo "$result" | jq -c '[.data[] | select(.balance != "0" and .balance != "0.00000000" and (.balance | tonumber) > 0)]')
    all_wallets=$(echo "$all_wallets" "$page_data" | jq -sc '.[0] + .[1]')
    page=$((page + 1))

    local has_next
    has_next=$(echo "$result" | jq -r '.has_next_page')
    if [ "$has_next" != "true" ]; then break; fi
    cursor=$(echo "$result" | jq -r '.end_cursor')
  done

  local count
  count=$(echo "$all_wallets" | jq 'length')
  if [ "$count" -eq 0 ]; then
    echo '{"wallets":[],"count":0,"total_eur":0}'
    return
  fi

  # Collect unique asset IDs and resolve names in parallel
  local asset_ids
  asset_ids=$(echo "$all_wallets" | jq -r '[.[].asset_id] | unique | .[]')
  local tmpdir
  tmpdir=$(mktemp -d)
  _CLEANUP_DIRS+=("$tmpdir")

  for aid in $asset_ids; do
    ( api_get "/v1/assets/${aid}" | jq -c '{id: .data.id, name: .data.name, symbol: .data.symbol}' > "${tmpdir}/asset_${aid}.json" 2>/dev/null ) &
  done
  wait

  # Build asset lookup map in one jq call (avoids N sequential invocations)
  if ls "$tmpdir"/asset_*.json 1>/dev/null 2>&1; then
    cat "$tmpdir"/asset_*.json | jq -sc 'map({key: .id, value: .}) | from_entries' > "$tmpdir/assets.json"
  else
    echo '{}' > "$tmpdir/assets.json"
  fi

  # Use pre-fetched ticker if provided, otherwise fetch
  if [ -n "$ticker_file" ]; then
    cp "$ticker_file" "$tmpdir/ticker.json"
  else
    fetch_all_ticker_prices > "$tmpdir/ticker.json"
  fi

  # Write wallets to file to avoid ARG_MAX on large portfolios
  echo "$all_wallets" > "$tmpdir/wallets.json"

  # Merge wallet data with asset names and prices, aggregate by asset
  jq -n --slurpfile wallets "$tmpdir/wallets.json" \
        --slurpfile assets "$tmpdir/assets.json" \
        --slurpfile ticker "$tmpdir/ticker.json" \
        --arg sort_by "$sort_by" '
    ($wallets[0]) as $w | ($assets[0]) as $a | ($ticker[0]) as $t |
    [ $w[] |
      ($a[.asset_id].symbol // "unknown") as $sym |
      ($t[$sym].price // null) as $price |
      {
        asset_name: ($a[.asset_id].name // "unknown"),
        asset_symbol: $sym,
        balance: .balance,
        eur_price: $price,
        eur_value: (if $price then ((.balance | tonumber) * ($price | tonumber)) else null end),
        wallet_type: .wallet_type,
        asset_id: .asset_id,
        wallet_id: .wallet_id
      }
    ]
    | group_by(.asset_symbol)
    | map({
        asset_name: .[0].asset_name,
        asset_symbol: .[0].asset_symbol,
        balance: (map(.balance | tonumber) | add | tostring),
        eur_price: .[0].eur_price,
        eur_value: (map(.eur_value // 0) | add),
        asset_id: .[0].asset_id,
        wallets: map({wallet_id, wallet_type, balance})
      })
    | (if $sort_by == "value" then sort_by(.eur_value // 0) | reverse else sort_by(.asset_name) end)
    | { wallets: ., count: length, total_eur: (map(.eur_value // 0) | add) }
  '
}

cmd_trades() {
  require_api_key
  local operation="" asset_type="" limit=5 from="" to=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --operation) operation="$2"; shift 2;;
      --asset-type) asset_type="$2"; shift 2;;
      --limit) limit="$2"; shift 2;;
      --from) from="$2"; shift 2;;
      --to) to="$2"; shift 2;;
      *) die "Unknown option: $1";;
    esac
  done

  local tmpdir
  tmpdir=$(mktemp -d)
  _CLEANUP_DIRS+=("$tmpdir")

  # Fetch ticker for asset type mapping (type field: cryptocoin, metal, stock, etc.)
  fetch_all_ticker_prices > "$tmpdir/ticker.json" &
  local ticker_pid=$!

  # Fetch transactions, auto-paginating until we have enough matches
  # When asset_type filter is active, collect more since filtering happens post-enrichment
  local collect_limit=$limit
  if [ -n "$asset_type" ]; then collect_limit=$((limit * 10)); fi
  local all_trades="[]"
  local cursor=""
  local found=0
  local max_pages=10

  while [ "$found" -lt "$collect_limit" ] && [ "$max_pages" -gt 0 ]; do
    max_pages=$((max_pages - 1))
    local resp
    resp=$(api_get "/v1/transactions" \
      "page_size" "100" \
      "from_including" "$from" "to_excluding" "$to" \
      "after" "$cursor")

    # Filter for buy/sell trades (have trade_id) on the incoming side
    local page_trades
    page_trades=$(echo "$resp" | jq -c --arg op "$operation" '
      [.data[] | select(
        .trade_id != null and .trade_id != "" and
        .flow == "incoming" and
        (if $op != "" then .operation_type == $op else (.operation_type == "buy" or .operation_type == "sell") end)
      )]')

    all_trades=$(echo "$all_trades" "$page_trades" | jq -sc '.[0] + .[1]')
    found=$(echo "$all_trades" | jq 'length')

    local has_next
    has_next=$(echo "$resp" | jq -r '.has_next_page')
    [ "$has_next" = "true" ] || break
    cursor=$(echo "$resp" | jq -r '.end_cursor')
  done

  wait "$ticker_pid"

  # Build ticker type map: asset_id -> {symbol, type, name} from ticker
  # Ticker is keyed by symbol with type field; we need to also resolve asset names
  local asset_ids
  asset_ids=$(echo "$all_trades" | jq -r '[.[].asset_id] | unique | .[]')

  # Resolve asset names in parallel
  for aid in $asset_ids; do
    ( api_get "/v1/assets/${aid}" | jq -c '{id: .data.id, name: .data.name, symbol: .data.symbol}' > "${tmpdir}/asset_${aid}.json" 2>/dev/null ) &
  done
  wait

  # Build asset lookup
  if ls "$tmpdir"/asset_*.json 1>/dev/null 2>&1; then
    cat "$tmpdir"/asset_*.json | jq -sc 'map({key: .id, value: .}) | from_entries' > "$tmpdir/assets.json"
  else
    echo '{}' > "$tmpdir/assets.json"
  fi

  # Enrich trades with asset name, symbol, type and apply asset_type filter
  echo "$all_trades" > "$tmpdir/trades.json"
  jq -n --slurpfile trades "$tmpdir/trades.json" \
        --slurpfile assets "$tmpdir/assets.json" \
        --slurpfile ticker "$tmpdir/ticker.json" \
        --arg asset_type "$asset_type" \
        --argjson limit "$limit" '
    ($trades[0]) as $t | ($assets[0]) as $a | ($ticker[0]) as $tk |
    [ $t[] |
      ($a[.asset_id].symbol // "unknown") as $sym |
      ($tk[$sym] // {}) as $tk_entry |
      {
        date: .credited_at,
        operation: .operation_type,
        asset_name: ($a[.asset_id].name // "unknown"),
        asset_symbol: $sym,
        asset_type: ($tk_entry.type // "unknown"),
        amount: .asset_amount,
        current_eur_price: ($tk_entry.price // null),
        trade_id: .trade_id,
        asset_id: .asset_id
      }
    ]
    | if $asset_type != "" then map(select(.asset_type == $asset_type)) else . end
    | .[:$limit]
  '
}

cmd_help() {
  cat <<'EOF'
Usage: bitpanda.sh <command> [options]

Commands:
  portfolio               Full portfolio with EUR valuations (--sort name|value)
  trades                  Recent trades with resolved names and asset types
  balances                List all wallets/balances
  all-transactions        List all transactions
  asset <asset_id>        Get asset info (name, symbol) by asset ID
  price <SYMBOL>          Get price for a single asset
  prices                  List prices for held assets (or --all for full ticker)
  help                    Show this help

Prices options:
  --all                   Show all available prices

Balances options:
  --asset-id <id>         Filter by asset ID
  --index-asset-id <id>   Filter by index asset ID
  --non-zero              Only show wallets with balance > 0
  --before <cursor>       Return page before cursor
  --after <cursor>        Return page after cursor
  --page-size <n>         Items per page (1-100, default 25)

Trades options:
  --operation <type>      Filter: buy, sell (default: both)
  --asset-type <type>     Filter: cryptocoin, metal, stock, etc.
  --limit <n>             Number of trades to return (default 5)
  --from <datetime>       From date-time (inclusive)
  --to <datetime>         To date-time (exclusive)

All-transactions options:
  --wallet-id <id>        Filter by wallet ID
  --flow <incoming|outgoing>  Filter by direction
  --asset-id <id>         Filter by asset ID
  --from <datetime>       From date-time (inclusive)
  --to <datetime>         To date-time (exclusive)
  --before <cursor>       Return page before cursor
  --after <cursor>        Return page after cursor
  --page-size <n>         Items per page (1-100, default 25)

Environment:
  BITPANDA_API_KEY    Required. Your Bitpanda API key.

Output is JSON.
EOF
}

case "${1:-help}" in
  portfolio)             shift; cmd_portfolio "$@";;
  trades)                shift; cmd_trades "$@";;
  balances)              shift; cmd_balances "$@";;
  all-transactions)      shift; cmd_all_transactions "$@";;
  asset)                 shift; cmd_asset "$@";;
  price)                 shift; cmd_price "$@";;
  prices)                shift; cmd_prices "$@";;
  help|--help|-h)        cmd_help;;
  *) die "Unknown command: $1. Run 'bitpanda.sh help' for usage.";;
esac
