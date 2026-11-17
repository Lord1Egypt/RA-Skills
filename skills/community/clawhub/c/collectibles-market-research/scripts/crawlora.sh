#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /path
#
# GET key=value args become the query string. Prints raw JSON to stdout — pipe into `jq`.
set -euo pipefail

: "${CRAWLORA_API_KEY:?Set CRAWLORA_API_KEY first — get a free key at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills}"
# The key is written to a curl config file below. Restrict it to the key
# alphabet so a newline, quote, or config directive cannot alter that file.
case "$CRAWLORA_API_KEY" in
  *[!A-Za-z0-9._-]*) echo "invalid CRAWLORA_API_KEY format" >&2; exit 2 ;;
esac
# Fixed, non-overridable: an env-configurable base URL would let anything that
# can set CRAWLORA_API_BASE redirect this key to an attacker-controlled host.
base="https://api.crawlora.net/api/v1"

method="GET"
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X|-d) echo "only GET are supported by the collectibles-market-research skill" >&2; exit 2 ;;
    *) args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh /<route> [k=v ...]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET) ;;
  *)
    echo "only GET are supported by the collectibles-market-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the collectibles-market-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /alt/asset) route_allowed=true ;;
  /alt/auctions) route_allowed=true ;;
  /alt/card-search) route_allowed=true ;;
  /alt/categories) route_allowed=true ;;
  /alt/listing) route_allowed=true ;;
  /alt/market-trends) route_allowed=true ;;
  /alt/search) route_allowed=true ;;
  /alt/sold-listings) route_allowed=true ;;
  /alt/top-movers) route_allowed=true ;;
  /comc/categories) route_allowed=true ;;
  /comc/listing) route_allowed=true ;;
  /comc/search) route_allowed=true ;;
  /fanatics/categories) route_allowed=true ;;
  /fanatics/category) route_allowed=true ;;
  /fanatics/product) route_allowed=true ;;
  /fanatics/search) route_allowed=true ;;
  /fanaticscollect/auctions) route_allowed=true ;;
  /fanaticscollect/categories) route_allowed=true ;;
  /fanaticscollect/instant-packs/release) route_allowed=true ;;
  /fanaticscollect/instant-packs/releases) route_allowed=true ;;
  /fanaticscollect/instant-rips/categories) route_allowed=true ;;
  /fanaticscollect/instant-rips/pack-categories) route_allowed=true ;;
  /fanaticscollect/instant-rips/pack-checklist) route_allowed=true ;;
  /fanaticscollect/instant-rips/packs) route_allowed=true ;;
  /fanaticscollect/instant-rips/recently-ripped) route_allowed=true ;;
  /fanaticscollect/newsroom) route_allowed=true ;;
  /fanaticscollect/newsroom/filters) route_allowed=true ;;
  /fanaticscollect/search) route_allowed=true ;;
  /fanaticscollect/sold-items) route_allowed=true ;;
  /fanaticscollect/trending-searches) route_allowed=true ;;
  /fanaticslive/browse) route_allowed=true ;;
  /fanaticslive/leagues) route_allowed=true ;;
  /fanaticslive/shops) route_allowed=true ;;
  /goldin/auctions) route_allowed=true ;;
  /goldin/categories) route_allowed=true ;;
  /goldin/listing) route_allowed=true ;;
  /goldin/search) route_allowed=true ;;
  /goldin/suggest) route_allowed=true ;;
  /pristine-auction/categories) route_allowed=true ;;
  /pristine-auction/search) route_allowed=true ;;
  /pristine-marketplace/collections) route_allowed=true ;;
  /pristine-marketplace/pages) route_allowed=true ;;
  /pristine-marketplace/products) route_allowed=true ;;
  /pristine-marketplace/reviews) route_allowed=true ;;
  /pristine-marketplace/search) route_allowed=true ;;
  /pristine-marketplace/search/suggest) route_allowed=true ;;
  /pristine-marketplace/sitemap/urls) route_allowed=true ;;
  /pristine-marketplace/sitemaps) route_allowed=true ;;
  /pristine-marketplace/store) route_allowed=true ;;
  /psa/autographfacts/categories) route_allowed=true ;;
  /psa/autographfacts/gallery) route_allowed=true ;;
  /psa/autographfacts/subject) route_allowed=true ;;
  /psa/autographfacts/subjects) route_allowed=true ;;
  /psa/cardfacts/categories) route_allowed=true ;;
  /psa/cardfacts/checklist) route_allowed=true ;;
  /psa/cardfacts/sets) route_allowed=true ;;
  /psa/cert-lookup) route_allowed=true ;;
  /psa/price-guide/categories) route_allowed=true ;;
  /psa/price-guide/search) route_allowed=true ;;
  /psa/price-guide/set) route_allowed=true ;;
  /psa/price-guide/sets) route_allowed=true ;;
  /psa/probatfacts/categories) route_allowed=true ;;
  /psa/probatfacts/gallery) route_allowed=true ;;
  /psa/probatfacts/subject) route_allowed=true ;;
  /psa/probatfacts/subjects) route_allowed=true ;;
  /psa/ticketfacts/categories) route_allowed=true ;;
  /psa/ticketfacts/gallery) route_allowed=true ;;
  /psa/ticketfacts/subject) route_allowed=true ;;
  /psa/ticketfacts/subjects) route_allowed=true ;;
  /psastore/collections) route_allowed=true ;;
  /psastore/pages) route_allowed=true ;;
  /psastore/products) route_allowed=true ;;
  /psastore/search/suggest) route_allowed=true ;;
  /psastore/sitemap/urls) route_allowed=true ;;
  /psastore/sitemaps) route_allowed=true ;;
  /psastore/store) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/fanaticscollect/listing/[^/]+$'
  '^/fanaticslive/channel/[^/]+$'
  '^/fanaticslive/shop/[^/]+$'
  '^/fanaticslive/shop/[^/]+/shows$'
  '^/fanaticslive/show/[^/]+$'
  '^/fanaticslive/show/[^/]+/instant-rips$'
  '^/pristine-auction/lot/[^/]+$'
  '^/pristine-marketplace/collections/[^/]+/products$'
  '^/pristine-marketplace/pages/[^/]+$'
  '^/pristine-marketplace/products/[^/]+$'
  '^/pristine-marketplace/products/[^/]+/recommendations$'
  '^/psastore/collections/[^/]+/products$'
  '^/psastore/pages/[^/]+$'
  '^/psastore/products/[^/]+$'
  '^/psastore/products/[^/]+/recommendations$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the collectibles-market-research skill catalog" >&2
  exit 2
fi



# Keep the API key out of the curl process command line. A private temporary
# config supplies the header and is removed automatically on exit.
umask 077
curl_config="$(mktemp "${TMPDIR:-/tmp}/crawlora-curl.XXXXXX")"
chmod 600 "$curl_config"
trap 'rm -f "$curl_config"' EXIT
printf 'header = "x-api-key: %s"\n' "$CRAWLORA_API_KEY" >"$curl_config"
auth=(--config "$curl_config")

# GET-only skill: no request body or alternate method is accepted.
# -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
qs=()
for kv in ${rest[@]+"${rest[@]}"}; do
  [ -n "$kv" ] || continue
  case "$kv" in
    *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
  esac
  qs+=(--data-urlencode "$kv")
done
curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"