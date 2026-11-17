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
    -X|-d) echo "only GET are supported by the crawlora-datasets skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the crawlora-datasets skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the crawlora-datasets skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /datasets) route_allowed=true ;;
  /datasets/airbnb-hosts/facets) route_allowed=true ;;
  /datasets/airbnb-hosts/search) route_allowed=true ;;
  /datasets/airbnb-markets/facets) route_allowed=true ;;
  /datasets/airbnb-markets/nearby) route_allowed=true ;;
  /datasets/airbnb-markets/search) route_allowed=true ;;
  /datasets/apple-books/facets) route_allowed=true ;;
  /datasets/apple-books/search) route_allowed=true ;;
  /datasets/apple-maps-places/facets) route_allowed=true ;;
  /datasets/apple-maps-places/nearby) route_allowed=true ;;
  /datasets/apple-maps-places/search) route_allowed=true ;;
  /datasets/apple-podcasts-shows/facets) route_allowed=true ;;
  /datasets/apple-podcasts-shows/search) route_allowed=true ;;
  /datasets/apps-charts/facets) route_allowed=true ;;
  /datasets/apps-charts/search) route_allowed=true ;;
  /datasets/apps-reviews/facets) route_allowed=true ;;
  /datasets/apps-reviews/search) route_allowed=true ;;
  /datasets/apps/facets) route_allowed=true ;;
  /datasets/apps/search) route_allowed=true ;;
  /datasets/bbb-businesses/facets) route_allowed=true ;;
  /datasets/bbb-businesses/search) route_allowed=true ;;
  /datasets/bbb-scamtracker-reports/facets) route_allowed=true ;;
  /datasets/bbb-scamtracker-reports/search) route_allowed=true ;;
  /datasets/boxofficemojo/facets) route_allowed=true ;;
  /datasets/boxofficemojo/search) route_allowed=true ;;
  /datasets/chrome-extensions/changes) route_allowed=true ;;
  /datasets/chrome-extensions/facets) route_allowed=true ;;
  /datasets/chrome-extensions/metrics) route_allowed=true ;;
  /datasets/chrome-extensions/search) route_allowed=true ;;
  /datasets/chrome-extensions/trending) route_allowed=true ;;
  /datasets/creators/facets) route_allowed=true ;;
  /datasets/creators/search) route_allowed=true ;;
  /datasets/doordash-stores/facets) route_allowed=true ;;
  /datasets/doordash-stores/nearby) route_allowed=true ;;
  /datasets/doordash-stores/search) route_allowed=true ;;
  /datasets/facebook-pages/facets) route_allowed=true ;;
  /datasets/facebook-pages/search) route_allowed=true ;;
  /datasets/github-users/facets) route_allowed=true ;;
  /datasets/github-users/nearby) route_allowed=true ;;
  /datasets/github-users/search) route_allowed=true ;;
  /datasets/goodreads-authors/facets) route_allowed=true ;;
  /datasets/goodreads-authors/search) route_allowed=true ;;
  /datasets/goodreads-books/facets) route_allowed=true ;;
  /datasets/goodreads-books/search) route_allowed=true ;;
  /datasets/google-map-businesses/facets) route_allowed=true ;;
  /datasets/google-map-businesses/nearby) route_allowed=true ;;
  /datasets/google-map-businesses/search) route_allowed=true ;;
  /datasets/housing-markets/facets) route_allowed=true ;;
  /datasets/housing-markets/search) route_allowed=true ;;
  /datasets/instagram-users/facets) route_allowed=true ;;
  /datasets/instagram-users/search) route_allowed=true ;;
  /datasets/jobs/companies) route_allowed=true ;;
  /datasets/jobs/facets) route_allowed=true ;;
  /datasets/jobs/nearby) route_allowed=true ;;
  /datasets/jobs/search) route_allowed=true ;;
  /datasets/journalists/facets) route_allowed=true ;;
  /datasets/journalists/search) route_allowed=true ;;
  /datasets/llms/facets) route_allowed=true ;;
  /datasets/llms/search) route_allowed=true ;;
  /datasets/numbeo-cities/facets) route_allowed=true ;;
  /datasets/numbeo-cities/search) route_allowed=true ;;
  /datasets/numbeo-countries/search) route_allowed=true ;;
  /datasets/pitchbook-advisors/facets) route_allowed=true ;;
  /datasets/pitchbook-advisors/search) route_allowed=true ;;
  /datasets/pitchbook-companies/facets) route_allowed=true ;;
  /datasets/pitchbook-companies/search) route_allowed=true ;;
  /datasets/pitchbook-funds/facets) route_allowed=true ;;
  /datasets/pitchbook-funds/search) route_allowed=true ;;
  /datasets/pitchbook-investors/facets) route_allowed=true ;;
  /datasets/pitchbook-investors/search) route_allowed=true ;;
  /datasets/pitchbook-limited-partners/facets) route_allowed=true ;;
  /datasets/pitchbook-limited-partners/search) route_allowed=true ;;
  /datasets/playstation-games/facets) route_allowed=true ;;
  /datasets/playstation-games/search) route_allowed=true ;;
  /datasets/producthunt-makers/facets) route_allowed=true ;;
  /datasets/producthunt-makers/search) route_allowed=true ;;
  /datasets/producthunt-products/facets) route_allowed=true ;;
  /datasets/producthunt-products/search) route_allowed=true ;;
  /datasets/producthunt-trends/facets) route_allowed=true ;;
  /datasets/producthunt-trends/search) route_allowed=true ;;
  /datasets/reddit-trending/facets) route_allowed=true ;;
  /datasets/reddit-trending/search) route_allowed=true ;;
  /datasets/sec-companies/facets) route_allowed=true ;;
  /datasets/sec-companies/search) route_allowed=true ;;
  /datasets/sec-institutional-positions/facets) route_allowed=true ;;
  /datasets/sec-institutional-positions/search) route_allowed=true ;;
  /datasets/starbucks-stores/facets) route_allowed=true ;;
  /datasets/starbucks-stores/nearby) route_allowed=true ;;
  /datasets/starbucks-stores/search) route_allowed=true ;;
  /datasets/steam-achievements/facets) route_allowed=true ;;
  /datasets/steam-achievements/search) route_allowed=true ;;
  /datasets/steam-charts/facets) route_allowed=true ;;
  /datasets/steam-charts/search) route_allowed=true ;;
  /datasets/steam-games/facets) route_allowed=true ;;
  /datasets/steam-games/search) route_allowed=true ;;
  /datasets/steam-news/facets) route_allowed=true ;;
  /datasets/steam-news/search) route_allowed=true ;;
  /datasets/steam-playercounts/facets) route_allowed=true ;;
  /datasets/steam-playercounts/search) route_allowed=true ;;
  /datasets/steam-prices/facets) route_allowed=true ;;
  /datasets/steam-prices/search) route_allowed=true ;;
  /datasets/steam-reviews/facets) route_allowed=true ;;
  /datasets/steam-reviews/search) route_allowed=true ;;
  /datasets/substack/facets) route_allowed=true ;;
  /datasets/substack/search) route_allowed=true ;;
  /datasets/techstack/facets) route_allowed=true ;;
  /datasets/techstack/search) route_allowed=true ;;
  /datasets/trustmrr/facets) route_allowed=true ;;
  /datasets/trustmrr/search) route_allowed=true ;;
  /datasets/vehicle-listings/facets) route_allowed=true ;;
  /datasets/vehicle-listings/search) route_allowed=true ;;
  /datasets/x-users/facets) route_allowed=true ;;
  /datasets/x-users/search) route_allowed=true ;;
  /datasets/youtube-creators/facets) route_allowed=true ;;
  /datasets/youtube-creators/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/datasets/airbnb-hosts/items/[^/]+$'
  '^/datasets/airbnb-markets/items/[^/]+$'
  '^/datasets/apple-books/items/[^/]+/[^/]+$'
  '^/datasets/apple-maps-places/items/[^/]+$'
  '^/datasets/apple-podcasts-shows/items/[^/]+$'
  '^/datasets/apps-charts/items/[^/]+$'
  '^/datasets/apps-reviews/items/[^/]+$'
  '^/datasets/apps/items/[^/]+$'
  '^/datasets/bbb-businesses/items/[^/]+$'
  '^/datasets/bbb-scamtracker-reports/items/[^/]+$'
  '^/datasets/boxofficemojo/items/[^/]+$'
  '^/datasets/chrome-extensions/history/[^/]+$'
  '^/datasets/chrome-extensions/items/[^/]+$'
  '^/datasets/creators/items/[^/]+$'
  '^/datasets/doordash-stores/items/[^/]+$'
  '^/datasets/facebook-pages/items/[^/]+$'
  '^/datasets/github-users/items/[^/]+$'
  '^/datasets/goodreads-authors/items/[^/]+$'
  '^/datasets/goodreads-books/items/[^/]+$'
  '^/datasets/google-map-businesses/items/[^/]+$'
  '^/datasets/housing-markets/items/[^/]+/[^/]+$'
  '^/datasets/instagram-users/items/[^/]+$'
  '^/datasets/jobs/companies/[^/]+$'
  '^/datasets/jobs/items/[^/]+$'
  '^/datasets/journalists/items/[^/]+/[^/]+$'
  '^/datasets/llms/items/[^/]+$'
  '^/datasets/numbeo-cities/items/[^/]+$'
  '^/datasets/numbeo-countries/items/[^/]+$'
  '^/datasets/pitchbook-advisors/items/[^/]+$'
  '^/datasets/pitchbook-companies/items/[^/]+$'
  '^/datasets/pitchbook-funds/items/[^/]+$'
  '^/datasets/pitchbook-investors/items/[^/]+$'
  '^/datasets/pitchbook-limited-partners/items/[^/]+$'
  '^/datasets/playstation-games/items/[^/]+$'
  '^/datasets/producthunt-makers/items/[^/]+$'
  '^/datasets/producthunt-products/items/[^/]+$'
  '^/datasets/reddit-trending/items/[^/]+$'
  '^/datasets/sec-companies/financials/[^/]+$'
  '^/datasets/sec-companies/insider/[^/]+$'
  '^/datasets/sec-companies/items/[^/]+$'
  '^/datasets/starbucks-stores/items/[^/]+$'
  '^/datasets/steam-achievements/items/[^/]+/[^/]+$'
  '^/datasets/steam-charts/items/[^/]+$'
  '^/datasets/steam-games/items/[^/]+$'
  '^/datasets/steam-news/items/[^/]+/[^/]+$'
  '^/datasets/steam-playercounts/items/[^/]+/[^/]+$'
  '^/datasets/steam-prices/items/[^/]+/[^/]+$'
  '^/datasets/steam-reviews/items/[^/]+/[^/]+$'
  '^/datasets/substack/items/[^/]+$'
  '^/datasets/techstack/items/[^/]+$'
  '^/datasets/trustmrr/history/[^/]+$'
  '^/datasets/trustmrr/items/[^/]+$'
  '^/datasets/vehicle-listings/items/[^/]+$'
  '^/datasets/vehicle-listings/price-history/[^/]+$'
  '^/datasets/x-users/items/[^/]+$'
  '^/datasets/youtube-creators/items/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the crawlora-datasets skill catalog" >&2
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