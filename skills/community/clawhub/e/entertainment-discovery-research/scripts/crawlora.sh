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
    -X|-d) echo "only GET are supported by the entertainment-discovery-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the entertainment-discovery-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the entertainment-discovery-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /imdb/charts) route_allowed=true ;;
  /imdb/image-types) route_allowed=true ;;
  /imdb/name) route_allowed=true ;;
  /imdb/name/awards) route_allowed=true ;;
  /imdb/name/credits) route_allowed=true ;;
  /imdb/name/images) route_allowed=true ;;
  /imdb/name/videos) route_allowed=true ;;
  /imdb/search) route_allowed=true ;;
  /imdb/search/title) route_allowed=true ;;
  /imdb/title) route_allowed=true ;;
  /imdb/title/awards) route_allowed=true ;;
  /imdb/title/box-office) route_allowed=true ;;
  /imdb/title/company-credits) route_allowed=true ;;
  /imdb/title/connections) route_allowed=true ;;
  /imdb/title/credits) route_allowed=true ;;
  /imdb/title/episodes) route_allowed=true ;;
  /imdb/title/filming-locations) route_allowed=true ;;
  /imdb/title/goofs) route_allowed=true ;;
  /imdb/title/images) route_allowed=true ;;
  /imdb/title/keywords) route_allowed=true ;;
  /imdb/title/parental-guide) route_allowed=true ;;
  /imdb/title/public-facts-analysis) route_allowed=true ;;
  /imdb/title/quotes) route_allowed=true ;;
  /imdb/title/ratings) route_allowed=true ;;
  /imdb/title/release-info) route_allowed=true ;;
  /imdb/title/reviews) route_allowed=true ;;
  /imdb/title/similar) route_allowed=true ;;
  /imdb/title/technical-specs) route_allowed=true ;;
  /imdb/title/trivia) route_allowed=true ;;
  /imdb/title/videos) route_allowed=true ;;
  /justwatch/age-certifications) route_allowed=true ;;
  /justwatch/discover) route_allowed=true ;;
  /justwatch/episode/by-id) route_allowed=true ;;
  /justwatch/episode/offers) route_allowed=true ;;
  /justwatch/genre/titles) route_allowed=true ;;
  /justwatch/genres) route_allowed=true ;;
  /justwatch/monetization/titles) route_allowed=true ;;
  /justwatch/new) route_allowed=true ;;
  /justwatch/popular) route_allowed=true ;;
  /justwatch/provider/titles) route_allowed=true ;;
  /justwatch/providers) route_allowed=true ;;
  /justwatch/search) route_allowed=true ;;
  /justwatch/season/by-id) route_allowed=true ;;
  /justwatch/season/episodes) route_allowed=true ;;
  /justwatch/show/seasons) route_allowed=true ;;
  /justwatch/title) route_allowed=true ;;
  /justwatch/title/analysis) route_allowed=true ;;
  /justwatch/title/by-id) route_allowed=true ;;
  /justwatch/title/media) route_allowed=true ;;
  /justwatch/title/offers) route_allowed=true ;;
  /justwatch/title/similar) route_allowed=true ;;
  /metacritic/browse) route_allowed=true ;;
  /rottentomatoes/browse/filters) route_allowed=true ;;
  /rottentomatoes/browse/movies) route_allowed=true ;;
  /rottentomatoes/browse/tv) route_allowed=true ;;
  /rottentomatoes/critic) route_allowed=true ;;
  /rottentomatoes/critic/publications) route_allowed=true ;;
  /rottentomatoes/critic/reviews) route_allowed=true ;;
  /rottentomatoes/critics/authors) route_allowed=true ;;
  /rottentomatoes/editorial/content) route_allowed=true ;;
  /rottentomatoes/editorial/detail) route_allowed=true ;;
  /rottentomatoes/editorial/search) route_allowed=true ;;
  /rottentomatoes/editorial/section) route_allowed=true ;;
  /rottentomatoes/editorial/taxonomies) route_allowed=true ;;
  /rottentomatoes/editorial/terms) route_allowed=true ;;
  /rottentomatoes/editorial/types) route_allowed=true ;;
  /rottentomatoes/episode) route_allowed=true ;;
  /rottentomatoes/episode/reviews) route_allowed=true ;;
  /rottentomatoes/movie) route_allowed=true ;;
  /rottentomatoes/movie/reviews) route_allowed=true ;;
  /rottentomatoes/movie/videos) route_allowed=true ;;
  /rottentomatoes/movies) route_allowed=true ;;
  /rottentomatoes/person) route_allowed=true ;;
  /rottentomatoes/publication) route_allowed=true ;;
  /rottentomatoes/publication/reviews) route_allowed=true ;;
  /rottentomatoes/search) route_allowed=true ;;
  /rottentomatoes/season) route_allowed=true ;;
  /rottentomatoes/season/reviews) route_allowed=true ;;
  /rottentomatoes/series) route_allowed=true ;;
  /rottentomatoes/sitemap/urls) route_allowed=true ;;
  /rottentomatoes/sitemaps) route_allowed=true ;;
  /tmdb/genres) route_allowed=true ;;
  /tmdb/movie/list) route_allowed=true ;;
  /tmdb/person/list) route_allowed=true ;;
  /tmdb/search) route_allowed=true ;;
  /tmdb/tv/list) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/metacritic/movie/[^/]+$'
  '^/metacritic/movie/[^/]+/critic-reviews$'
  '^/metacritic/movie/[^/]+/user-reviews$'
  '^/metacritic/tv/[^/]+$'
  '^/metacritic/tv/[^/]+/critic-reviews$'
  '^/metacritic/tv/[^/]+/user-reviews$'
  '^/tmdb/collection/[^/]+$'
  '^/tmdb/movie/[^/]+$'
  '^/tmdb/person/[^/]+$'
  '^/tmdb/tv/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the entertainment-discovery-research skill catalog" >&2
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