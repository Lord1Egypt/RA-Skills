#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /amazon/search k=laptop s=relevanceblender
#   GET  :  crawlora.sh /youtube/transcript/dQw4w9WgXcQ
#   POST :  crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}'
#   POST :  crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["bitcoin"]}'
#
# GET key=value args become the query string. POST takes one JSON body argument
# (or pass it with -d '<json>'). Prints raw JSON to stdout — pipe into `jq`.
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
body=""
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X)
      [ $# -ge 2 ] || { echo "-X requires an HTTP method" >&2; exit 2; }
      method="$2"; shift 2 ;;
    -d)
      [ $# -ge 2 ] || { echo "-d requires a request body" >&2; exit 2; }
      body="$2"; shift 2 ;;
    *)  args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh [-X METHOD] /path [k=v ... | json-body]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET|POST) ;;
  *)
    echo "only GET and POST are supported by the crawlora skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the crawlora skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /1stdibs/categories) route_allowed=true ;;
  /1stdibs/designers) route_allowed=true ;;
  /1stdibs/product) route_allowed=true ;;
  /1stdibs/search) route_allowed=true ;;
  /7now/catalog) route_allowed=true ;;
  /7now/categories) route_allowed=true ;;
  /7now/category) route_allowed=true ;;
  /7now/combo) route_allowed=true ;;
  /7now/combos) route_allowed=true ;;
  /7now/deals) route_allowed=true ;;
  /7now/offers) route_allowed=true ;;
  /7now/popular) route_allowed=true ;;
  /7now/product) route_allowed=true ;;
  /7now/promotion) route_allowed=true ;;
  /7now/search) route_allowed=true ;;
  /7now/stores) route_allowed=true ;;
  /7now/suggest) route_allowed=true ;;
  /abcau/article) route_allowed=true ;;
  /abcau/author) route_allowed=true ;;
  /abcau/headlines) route_allowed=true ;;
  /abcau/news) route_allowed=true ;;
  /abcau/sections) route_allowed=true ;;
  /abcnews/article) route_allowed=true ;;
  /abcnews/author) route_allowed=true ;;
  /abcnews/headlines) route_allowed=true ;;
  /abcnews/news) route_allowed=true ;;
  /abcnews/sections) route_allowed=true ;;
  /accor/amenities) route_allowed=true ;;
  /accor/brands) route_allowed=true ;;
  /accor/catalog/hotels) route_allowed=true ;;
  /accor/destination/hotels) route_allowed=true ;;
  /accor/property) route_allowed=true ;;
  /accor/search) route_allowed=true ;;
  /accor/search/details) route_allowed=true ;;
  /accor/search/suggest) route_allowed=true ;;
  /adidas/product) route_allowed=true ;;
  /adidas/product/review-topics) route_allowed=true ;;
  /adidas/product/reviews) route_allowed=true ;;
  /adidas/search) route_allowed=true ;;
  /adidas/store) route_allowed=true ;;
  /adidas/stores) route_allowed=true ;;
  /adidas/suggest) route_allowed=true ;;
  /agoda/activities/search) route_allowed=true ;;
  /agoda/flights/itinerary-amenities) route_allowed=true ;;
  /agoda/flights/search) route_allowed=true ;;
  /agoda/flights/search-locations) route_allowed=true ;;
  /agoda/homes/search) route_allowed=true ;;
  /agoda/hotels/search) route_allowed=true ;;
  /airbnb/search) route_allowed=true ;;
  /alcom/headlines) route_allowed=true ;;
  /alcom/news) route_allowed=true ;;
  /alcom/sections) route_allowed=true ;;
  /aliexpress/reviews) route_allowed=true ;;
  /aliexpress/search) route_allowed=true ;;
  /aliexpress/search-filters) route_allowed=true ;;
  /aljazeera/article) route_allowed=true ;;
  /aljazeera/author) route_allowed=true ;;
  /aljazeera/categories) route_allowed=true ;;
  /aljazeera/headlines) route_allowed=true ;;
  /aljazeera/topic) route_allowed=true ;;
  /allbirds/collections) route_allowed=true ;;
  /allbirds/pages) route_allowed=true ;;
  /allbirds/products) route_allowed=true ;;
  /allbirds/search/suggest) route_allowed=true ;;
  /allbirds/sitemap/urls) route_allowed=true ;;
  /allbirds/sitemaps) route_allowed=true ;;
  /allbirds/store) route_allowed=true ;;
  /alt/asset) route_allowed=true ;;
  /alt/auctions) route_allowed=true ;;
  /alt/card-search) route_allowed=true ;;
  /alt/categories) route_allowed=true ;;
  /alt/listing) route_allowed=true ;;
  /alt/market-trends) route_allowed=true ;;
  /alt/search) route_allowed=true ;;
  /alt/sold-listings) route_allowed=true ;;
  /alt/top-movers) route_allowed=true ;;
  /amazon-jobs/categories) route_allowed=true ;;
  /amazon-jobs/job) route_allowed=true ;;
  /amazon-jobs/search) route_allowed=true ;;
  /amazon/charts) route_allowed=true ;;
  /amazon/charts/categories) route_allowed=true ;;
  /amazon/search) route_allowed=true ;;
  /androidauthority/article) route_allowed=true ;;
  /androidauthority/headlines) route_allowed=true ;;
  /androidauthority/news) route_allowed=true ;;
  /androidauthority/sections) route_allowed=true ;;
  /androidpolice/article) route_allowed=true ;;
  /androidpolice/author) route_allowed=true ;;
  /androidpolice/headlines) route_allowed=true ;;
  /androidpolice/news) route_allowed=true ;;
  /androidpolice/sections) route_allowed=true ;;
  /anime/airing-schedule) route_allowed=true ;;
  /anime/character/search) route_allowed=true ;;
  /anime/rankings) route_allowed=true ;;
  /anime/search) route_allowed=true ;;
  /apnews/article) route_allowed=true ;;
  /apnews/author) route_allowed=true ;;
  /apnews/fact-check) route_allowed=true ;;
  /apnews/headlines) route_allowed=true ;;
  /apnews/news) route_allowed=true ;;
  /apnews/sections) route_allowed=true ;;
  /apple-books/audiobook/search) route_allowed=true ;;
  /apple-books/charts) route_allowed=true ;;
  /apple-books/search) route_allowed=true ;;
  /apple-jobs/job) route_allowed=true ;;
  /apple-jobs/locations) route_allowed=true ;;
  /apple-jobs/search) route_allowed=true ;;
  /apple-maps/autocomplete) route_allowed=true ;;
  /apple-maps/categories) route_allowed=true ;;
  /apple-maps/category-search) route_allowed=true ;;
  /apple-maps/directions) route_allowed=true ;;
  /apple-maps/eta) route_allowed=true ;;
  /apple-maps/guides) route_allowed=true ;;
  /apple-maps/guides/cities) route_allowed=true ;;
  /apple-maps/guides/guide) route_allowed=true ;;
  /apple-maps/guides/lookup) route_allowed=true ;;
  /apple-maps/guides/nearby) route_allowed=true ;;
  /apple-maps/guides/publisher) route_allowed=true ;;
  /apple-maps/guides/publishers) route_allowed=true ;;
  /apple-maps/place) route_allowed=true ;;
  /apple-maps/place/photos) route_allowed=true ;;
  /apple-maps/places) route_allowed=true ;;
  /apple-maps/reverse-geocode) route_allowed=true ;;
  /apple-maps/search) route_allowed=true ;;
  /apple-maps/transit-departures) route_allowed=true ;;
  /apple-maps/venue/browse) route_allowed=true ;;
  /apple-podcasts/charts) route_allowed=true ;;
  /apple-podcasts/charts/rankings) route_allowed=true ;;
  /apple-podcasts/episodes/search) route_allowed=true ;;
  /apple-podcasts/new) route_allowed=true ;;
  /apple-podcasts/search) route_allowed=true ;;
  /appstore/app) route_allowed=true ;;
  /appstore/categories) route_allowed=true ;;
  /appstore/collection) route_allowed=true ;;
  /appstore/collections) route_allowed=true ;;
  /appstore/editorial) route_allowed=true ;;
  /appstore/editorial/category) route_allowed=true ;;
  /appstore/list) route_allowed=true ;;
  /appstore/ratings) route_allowed=true ;;
  /appstore/reviews) route_allowed=true ;;
  /appstore/search) route_allowed=true ;;
  /appstore/similar) route_allowed=true ;;
  /arbys/categories) route_allowed=true ;;
  /arbys/directory) route_allowed=true ;;
  /arbys/location) route_allowed=true ;;
  /arbys/locations) route_allowed=true ;;
  /arbys/menu) route_allowed=true ;;
  /arstechnica/article) route_allowed=true ;;
  /arstechnica/author) route_allowed=true ;;
  /arstechnica/headlines) route_allowed=true ;;
  /arstechnica/news) route_allowed=true ;;
  /arstechnica/sections) route_allowed=true ;;
  /audible/categories) route_allowed=true ;;
  /audible/charts) route_allowed=true ;;
  /audible/charts/authors) route_allowed=true ;;
  /audible/products) route_allowed=true ;;
  /audible/search) route_allowed=true ;;
  /autotrader/search) route_allowed=true ;;
  /axios/article) route_allowed=true ;;
  /axios/categories) route_allowed=true ;;
  /axios/headlines) route_allowed=true ;;
  /baidu/search) route_allowed=true ;;
  /baidu/suggest) route_allowed=true ;;
  /balenciaga/categories) route_allowed=true ;;
  /balenciaga/category) route_allowed=true ;;
  /balenciaga/product) route_allowed=true ;;
  /balenciaga/product/variants) route_allowed=true ;;
  /balenciaga/search) route_allowed=true ;;
  /balenciaga/store-countries) route_allowed=true ;;
  /balenciaga/stores) route_allowed=true ;;
  /barrons/article) route_allowed=true ;;
  /barrons/headlines) route_allowed=true ;;
  /barrons/news) route_allowed=true ;;
  /barrons/topics) route_allowed=true ;;
  /bbb/article) route_allowed=true ;;
  /bbb/business) route_allowed=true ;;
  /bbb/business/complaints) route_allowed=true ;;
  /bbb/business/more-info) route_allowed=true ;;
  /bbb/business/reviews) route_allowed=true ;;
  /bbb/category) route_allowed=true ;;
  /bbb/local-bbb) route_allowed=true ;;
  /bbb/local-bbbs) route_allowed=true ;;
  /bbb/news) route_allowed=true ;;
  /bbb/news/topics) route_allowed=true ;;
  /bbb/page) route_allowed=true ;;
  /bbb/regions) route_allowed=true ;;
  /bbb/scamtracker/search) route_allowed=true ;;
  /bbb/scamtracker/state-stats) route_allowed=true ;;
  /bbb/search) route_allowed=true ;;
  /bbb/search/filters) route_allowed=true ;;
  /bbc/article) route_allowed=true ;;
  /bbc/author) route_allowed=true ;;
  /bbc/headlines) route_allowed=true ;;
  /bbc/live) route_allowed=true ;;
  /bbc/search) route_allowed=true ;;
  /benzinga/article) route_allowed=true ;;
  /benzinga/headlines) route_allowed=true ;;
  /benzinga/news) route_allowed=true ;;
  /benzinga/search) route_allowed=true ;;
  /benzinga/sections) route_allowed=true ;;
  /bestbuy/brands) route_allowed=true ;;
  /bestbuy/categories) route_allowed=true ;;
  /bestbuy/categories/trending) route_allowed=true ;;
  /bestbuy/category) route_allowed=true ;;
  /bestbuy/category/subcategories) route_allowed=true ;;
  /bestbuy/product) route_allowed=true ;;
  /bestbuy/product/questions) route_allowed=true ;;
  /bestbuy/product/related) route_allowed=true ;;
  /bestbuy/product/reviews) route_allowed=true ;;
  /bestbuy/search) route_allowed=true ;;
  /bestbuy/stores) route_allowed=true ;;
  /bigcommerce/category) route_allowed=true ;;
  /bigcommerce/product) route_allowed=true ;;
  /bigcommerce/search) route_allowed=true ;;
  /bilibili/anime-home) route_allowed=true ;;
  /bilibili/autocomplete) route_allowed=true ;;
  /bilibili/guochuang-home) route_allowed=true ;;
  /bilibili/must-watch) route_allowed=true ;;
  /bilibili/popular) route_allowed=true ;;
  /bilibili/ranking) route_allowed=true ;;
  /bilibili/vertical-home) route_allowed=true ;;
  /bilibili/weekly) route_allowed=true ;;
  /billboard/article) route_allowed=true ;;
  /billboard/author) route_allowed=true ;;
  /billboard/headlines) route_allowed=true ;;
  /billboard/news) route_allowed=true ;;
  /billboard/sections) route_allowed=true ;;
  /bing/images) route_allowed=true ;;
  /bing/news) route_allowed=true ;;
  /bing/search) route_allowed=true ;;
  /bing/suggest) route_allowed=true ;;
  /bing/videos) route_allowed=true ;;
  /birminghammail/article) route_allowed=true ;;
  /birminghammail/author) route_allowed=true ;;
  /birminghammail/headlines) route_allowed=true ;;
  /birminghammail/news) route_allowed=true ;;
  /birminghammail/sections) route_allowed=true ;;
  /bleacherreport/article) route_allowed=true ;;
  /bleacherreport/author) route_allowed=true ;;
  /bleacherreport/headlines) route_allowed=true ;;
  /bleacherreport/news) route_allowed=true ;;
  /bleacherreport/sections) route_allowed=true ;;
  /bloomberg/article) route_allowed=true ;;
  /bloomberg/author) route_allowed=true ;;
  /bloomberg/categories) route_allowed=true ;;
  /bloomberg/headlines) route_allowed=true ;;
  /bloomberg/news) route_allowed=true ;;
  /bloomberg/news-sitemaps) route_allowed=true ;;
  /bluesky/author-feed) route_allowed=true ;;
  /bluesky/followers) route_allowed=true ;;
  /bluesky/follows) route_allowed=true ;;
  /bluesky/post-likes) route_allowed=true ;;
  /bluesky/post-quotes) route_allowed=true ;;
  /bluesky/post-reposted-by) route_allowed=true ;;
  /bluesky/post-thread) route_allowed=true ;;
  /bluesky/posts) route_allowed=true ;;
  /bluesky/profile) route_allowed=true ;;
  /bluesky/search-actors) route_allowed=true ;;
  /bluesky/trending-topics) route_allowed=true ;;
  /bonhams/auctions/search) route_allowed=true ;;
  /bonhams/lots/search) route_allowed=true ;;
  /booking-attractions/detail) route_allowed=true ;;
  /booking-attractions/reviews) route_allowed=true ;;
  /booking-attractions/search) route_allowed=true ;;
  /booking-flights/autocomplete) route_allowed=true ;;
  /booking-flights/search) route_allowed=true ;;
  /booking/hotel-detail) route_allowed=true ;;
  /booking/reviews) route_allowed=true ;;
  /booking/search) route_allowed=true ;;
  /boots/search) route_allowed=true ;;
  /boots/suggest) route_allowed=true ;;
  /bostonglobe/news) route_allowed=true ;;
  /boxofficemojo/brand) route_allowed=true ;;
  /boxofficemojo/brands) route_allowed=true ;;
  /boxofficemojo/calendar) route_allowed=true ;;
  /boxofficemojo/calendar/changes) route_allowed=true ;;
  /boxofficemojo/calendar/date) route_allowed=true ;;
  /boxofficemojo/date/domestic) route_allowed=true ;;
  /boxofficemojo/franchise) route_allowed=true ;;
  /boxofficemojo/franchises) route_allowed=true ;;
  /boxofficemojo/genre) route_allowed=true ;;
  /boxofficemojo/genres) route_allowed=true ;;
  /boxofficemojo/lifetime-grosses) route_allowed=true ;;
  /boxofficemojo/release) route_allowed=true ;;
  /boxofficemojo/release-group) route_allowed=true ;;
  /boxofficemojo/showdown) route_allowed=true ;;
  /boxofficemojo/showdowns) route_allowed=true ;;
  /boxofficemojo/title) route_allowed=true ;;
  /boxofficemojo/weekend/domestic) route_allowed=true ;;
  /boxofficemojo/weekend/domestic/by-distributor) route_allowed=true ;;
  /boxofficemojo/weekend/domestic/estimates) route_allowed=true ;;
  /boxofficemojo/year/domestic) route_allowed=true ;;
  /boxofficemojo/year/worldwide) route_allowed=true ;;
  /brand/retrieve) route_allowed=true ;;
  /brave/images) route_allowed=true ;;
  /brave/news) route_allowed=true ;;
  /brave/search) route_allowed=true ;;
  /brave/suggest) route_allowed=true ;;
  /brave/videos) route_allowed=true ;;
  /breitbart/article) route_allowed=true ;;
  /breitbart/author) route_allowed=true ;;
  /breitbart/headlines) route_allowed=true ;;
  /breitbart/news) route_allowed=true ;;
  /breitbart/sections) route_allowed=true ;;
  /brisbanetimes/article) route_allowed=true ;;
  /brisbanetimes/author) route_allowed=true ;;
  /brisbanetimes/headlines) route_allowed=true ;;
  /brisbanetimes/news) route_allowed=true ;;
  /brisbanetimes/sections) route_allowed=true ;;
  /brooklinen/collections) route_allowed=true ;;
  /brooklinen/pages) route_allowed=true ;;
  /brooklinen/products) route_allowed=true ;;
  /brooklinen/search/suggest) route_allowed=true ;;
  /brooklinen/sitemap/urls) route_allowed=true ;;
  /brooklinen/sitemaps) route_allowed=true ;;
  /brooklinen/store) route_allowed=true ;;
  /burberry/categories) route_allowed=true ;;
  /burberry/category) route_allowed=true ;;
  /burberry/product) route_allowed=true ;;
  /burberry/related) route_allowed=true ;;
  /burberry/search) route_allowed=true ;;
  /burberry/suggest) route_allowed=true ;;
  /burgerking/availability) route_allowed=true ;;
  /burgerking/locations) route_allowed=true ;;
  /burgerking/menu) route_allowed=true ;;
  /burgerking/product) route_allowed=true ;;
  /businessinsider/article) route_allowed=true ;;
  /businessinsider/author) route_allowed=true ;;
  /businessinsider/headlines) route_allowed=true ;;
  /businessinsider/news) route_allowed=true ;;
  /businessinsider/sections) route_allowed=true ;;
  /businessstandard/article) route_allowed=true ;;
  /businessstandard/author) route_allowed=true ;;
  /businessstandard/headlines) route_allowed=true ;;
  /businessstandard/news) route_allowed=true ;;
  /businessstandard/sections) route_allowed=true ;;
  /capterra/product) route_allowed=true ;;
  /capterra/product/reviews) route_allowed=true ;;
  /capterra/search) route_allowed=true ;;
  /carmax/search) route_allowed=true ;;
  /carmax/search/suggestions) route_allowed=true ;;
  /carmax/shop-by-brand) route_allowed=true ;;
  /carmax/stores) route_allowed=true ;;
  /carsdotcom/search) route_allowed=true ;;
  /cbc/article) route_allowed=true ;;
  /cbc/author) route_allowed=true ;;
  /cbc/headlines) route_allowed=true ;;
  /cbc/news) route_allowed=true ;;
  /cbc/sections) route_allowed=true ;;
  /cbr/article) route_allowed=true ;;
  /cbr/author) route_allowed=true ;;
  /cbr/headlines) route_allowed=true ;;
  /cbr/news) route_allowed=true ;;
  /cbr/sections) route_allowed=true ;;
  /cbsnews/article) route_allowed=true ;;
  /cbsnews/author) route_allowed=true ;;
  /cbsnews/headlines) route_allowed=true ;;
  /cbsnews/news) route_allowed=true ;;
  /cbsnews/sections) route_allowed=true ;;
  /cbssports/article) route_allowed=true ;;
  /cbssports/author) route_allowed=true ;;
  /cbssports/headlines) route_allowed=true ;;
  /cbssports/news) route_allowed=true ;;
  /cbssports/sections) route_allowed=true ;;
  /chewy/brands) route_allowed=true ;;
  /chewy/categories) route_allowed=true ;;
  /chewy/category) route_allowed=true ;;
  /chewy/facets) route_allowed=true ;;
  /chewy/gtin-lookup) route_allowed=true ;;
  /chewy/inventory) route_allowed=true ;;
  /chewy/item-attributes) route_allowed=true ;;
  /chewy/product) route_allowed=true ;;
  /chewy/product-questions) route_allowed=true ;;
  /chewy/product-reviews) route_allowed=true ;;
  /chewy/products) route_allowed=true ;;
  /chewy/search) route_allowed=true ;;
  /chewy/suggest) route_allowed=true ;;
  /chewy/variants) route_allowed=true ;;
  /chicagotribune/article) route_allowed=true ;;
  /chicagotribune/author) route_allowed=true ;;
  /chicagotribune/headlines) route_allowed=true ;;
  /chicagotribune/news) route_allowed=true ;;
  /chicagotribune/sections) route_allowed=true ;;
  /chick-fil-a/content) route_allowed=true ;;
  /chick-fil-a/content-taxonomy) route_allowed=true ;;
  /chick-fil-a/faq) route_allowed=true ;;
  /chick-fil-a/location) route_allowed=true ;;
  /chick-fil-a/locations) route_allowed=true ;;
  /chick-fil-a/menu) route_allowed=true ;;
  /chick-fil-a/menu-item) route_allowed=true ;;
  /chick-fil-a/menu-taxonomy) route_allowed=true ;;
  /chipotle/ingredients) route_allowed=true ;;
  /chipotle/meals) route_allowed=true ;;
  /chipotle/menu) route_allowed=true ;;
  /chipotle/menu/metadata) route_allowed=true ;;
  /chipotle/restaurant) route_allowed=true ;;
  /chipotle/restaurant/meals) route_allowed=true ;;
  /chipotle/restaurant/menu) route_allowed=true ;;
  /chipotle/restaurants) route_allowed=true ;;
  /chromewebstore/categories) route_allowed=true ;;
  /chromewebstore/category) route_allowed=true ;;
  /chromewebstore/charts) route_allowed=true ;;
  /chromewebstore/collection) route_allowed=true ;;
  /chromewebstore/developer) route_allowed=true ;;
  /chromewebstore/item) route_allowed=true ;;
  /chromewebstore/permissions) route_allowed=true ;;
  /chromewebstore/privacy) route_allowed=true ;;
  /chromewebstore/reviews) route_allowed=true ;;
  /chromewebstore/search) route_allowed=true ;;
  /chromewebstore/similar) route_allowed=true ;;
  /chromewebstore/suggest) route_allowed=true ;;
  /chrono24/autocomplete) route_allowed=true ;;
  /chrono24/brands) route_allowed=true ;;
  /chrono24/dealer) route_allowed=true ;;
  /chrono24/dealer/reviews) route_allowed=true ;;
  /chrono24/facets) route_allowed=true ;;
  /chrono24/listing) route_allowed=true ;;
  /chrono24/models) route_allowed=true ;;
  /chrono24/search) route_allowed=true ;;
  /clevelandcom/news) route_allowed=true ;;
  /cna/article) route_allowed=true ;;
  /cna/author) route_allowed=true ;;
  /cna/headlines) route_allowed=true ;;
  /cna/news) route_allowed=true ;;
  /cna/sections) route_allowed=true ;;
  /cnbc/article) route_allowed=true ;;
  /cnbc/author) route_allowed=true ;;
  /cnbc/categories) route_allowed=true ;;
  /cnbc/headlines) route_allowed=true ;;
  /cnet/article) route_allowed=true ;;
  /cnet/author) route_allowed=true ;;
  /cnet/headlines) route_allowed=true ;;
  /cnet/news) route_allowed=true ;;
  /cnet/sections) route_allowed=true ;;
  /cnn/article) route_allowed=true ;;
  /cnn/author) route_allowed=true ;;
  /cnn/headlines) route_allowed=true ;;
  /cnn/live-story) route_allowed=true ;;
  /coingecko/categories) route_allowed=true ;;
  /coingecko/chains) route_allowed=true ;;
  /coingecko/exchanges) route_allowed=true ;;
  /coingecko/gainers-losers) route_allowed=true ;;
  /coingecko/global) route_allowed=true ;;
  /coingecko/global/charts) route_allowed=true ;;
  /coingecko/learn/articles) route_allowed=true ;;
  /coingecko/markets) route_allowed=true ;;
  /coingecko/new-coins) route_allowed=true ;;
  /coingecko/news) route_allowed=true ;;
  /coingecko/nfts) route_allowed=true ;;
  /coingecko/search) route_allowed=true ;;
  /coingecko/token-unlocks) route_allowed=true ;;
  /coingecko/treasuries) route_allowed=true ;;
  /coingecko/trending) route_allowed=true ;;
  /colehaan/collections) route_allowed=true ;;
  /colehaan/pages) route_allowed=true ;;
  /colehaan/products) route_allowed=true ;;
  /colehaan/search/suggest) route_allowed=true ;;
  /colehaan/sitemap/urls) route_allowed=true ;;
  /colehaan/sitemaps) route_allowed=true ;;
  /colehaan/store) route_allowed=true ;;
  /collider/article) route_allowed=true ;;
  /collider/author) route_allowed=true ;;
  /collider/headlines) route_allowed=true ;;
  /collider/news) route_allowed=true ;;
  /collider/sections) route_allowed=true ;;
  /comc/categories) route_allowed=true ;;
  /comc/listing) route_allowed=true ;;
  /comc/search) route_allowed=true ;;
  /congress/report) route_allowed=true ;;
  /congress/stock-disclosures) route_allowed=true ;;
  /costco/categories) route_allowed=true ;;
  /costco/search) route_allowed=true ;;
  /costco/warehouses) route_allowed=true ;;
  /courtlistener/courts) route_allowed=true ;;
  /courtlistener/people) route_allowed=true ;;
  /courtlistener/search) route_allowed=true ;;
  /cricinfo/calendar) route_allowed=true ;;
  /cricinfo/commentary) route_allowed=true ;;
  /cricinfo/grounds) route_allowed=true ;;
  /cricinfo/live) route_allowed=true ;;
  /cricinfo/match) route_allowed=true ;;
  /cricinfo/news) route_allowed=true ;;
  /cricinfo/photos) route_allowed=true ;;
  /cricinfo/rankings) route_allowed=true ;;
  /cricinfo/records) route_allowed=true ;;
  /cricinfo/records/index) route_allowed=true ;;
  /cricinfo/rss) route_allowed=true ;;
  /cricinfo/scores) route_allowed=true ;;
  /cricinfo/series) route_allowed=true ;;
  /cricinfo/squads) route_allowed=true ;;
  /cricinfo/stats) route_allowed=true ;;
  /cricinfo/story) route_allowed=true ;;
  /cricinfo/team) route_allowed=true ;;
  /cricinfo/team/schedule) route_allowed=true ;;
  /cricinfo/teams) route_allowed=true ;;
  /cricinfo/venue) route_allowed=true ;;
  /cricinfo/venue/matches) route_allowed=true ;;
  /cricinfo/videos) route_allowed=true ;;
  /ctvnews/article) route_allowed=true ;;
  /ctvnews/author) route_allowed=true ;;
  /ctvnews/headlines) route_allowed=true ;;
  /ctvnews/news) route_allowed=true ;;
  /ctvnews/sections) route_allowed=true ;;
  /culvers/calendar) route_allowed=true ;;
  /culvers/categories) route_allowed=true ;;
  /culvers/directory) route_allowed=true ;;
  /culvers/flavor) route_allowed=true ;;
  /culvers/item) route_allowed=true ;;
  /culvers/menu) route_allowed=true ;;
  /culvers/store) route_allowed=true ;;
  /cvs/brands) route_allowed=true ;;
  /cvs/categories) route_allowed=true ;;
  /cvs/category) route_allowed=true ;;
  /cvs/search) route_allowed=true ;;
  /cvs/store-locator) route_allowed=true ;;
  /dailycaller/article) route_allowed=true ;;
  /dailycaller/author) route_allowed=true ;;
  /dailycaller/headlines) route_allowed=true ;;
  /dailycaller/news) route_allowed=true ;;
  /dailycaller/sections) route_allowed=true ;;
  /dailyexpress/article) route_allowed=true ;;
  /dailyexpress/author) route_allowed=true ;;
  /dailyexpress/headlines) route_allowed=true ;;
  /dailyexpress/news) route_allowed=true ;;
  /dailyexpress/sections) route_allowed=true ;;
  /dailykos/article) route_allowed=true ;;
  /dailykos/headlines) route_allowed=true ;;
  /dailykos/news) route_allowed=true ;;
  /dailykos/sections) route_allowed=true ;;
  /dailymail/article) route_allowed=true ;;
  /dailymail/author) route_allowed=true ;;
  /dailymail/headlines) route_allowed=true ;;
  /dailymail/news) route_allowed=true ;;
  /dailymail/sections) route_allowed=true ;;
  /dailymaverick/article) route_allowed=true ;;
  /dailymaverick/headlines) route_allowed=true ;;
  /dailymaverick/news) route_allowed=true ;;
  /dailymaverick/sections) route_allowed=true ;;
  /dailyrecord/article) route_allowed=true ;;
  /dailyrecord/author) route_allowed=true ;;
  /dailyrecord/headlines) route_allowed=true ;;
  /dailyrecord/news) route_allowed=true ;;
  /dailyrecord/sections) route_allowed=true ;;
  /dailystaruk/article) route_allowed=true ;;
  /dailystaruk/author) route_allowed=true ;;
  /dailystaruk/headlines) route_allowed=true ;;
  /dailystaruk/news) route_allowed=true ;;
  /dailystaruk/sections) route_allowed=true ;;
  /dailywire/article) route_allowed=true ;;
  /dailywire/author) route_allowed=true ;;
  /dailywire/headlines) route_allowed=true ;;
  /dailywire/news) route_allowed=true ;;
  /dailywire/sections) route_allowed=true ;;
  /dawn/article) route_allowed=true ;;
  /dawn/author) route_allowed=true ;;
  /dawn/headlines) route_allowed=true ;;
  /dawn/news) route_allowed=true ;;
  /dawn/sections) route_allowed=true ;;
  /deadline/article) route_allowed=true ;;
  /deadline/author) route_allowed=true ;;
  /deadline/headlines) route_allowed=true ;;
  /deadline/news) route_allowed=true ;;
  /deadline/sections) route_allowed=true ;;
  /deliveroo/fulfillment-times) route_allowed=true ;;
  /deliveroo/restaurant) route_allowed=true ;;
  /deliveroo/restaurant/menu) route_allowed=true ;;
  /deliveroo/search) route_allowed=true ;;
  /deliveroo/search/filters) route_allowed=true ;;
  /denverpost/article) route_allowed=true ;;
  /denverpost/author) route_allowed=true ;;
  /denverpost/headlines) route_allowed=true ;;
  /denverpost/news) route_allowed=true ;;
  /denverpost/sections) route_allowed=true ;;
  /depop/brands) route_allowed=true ;;
  /depop/categories) route_allowed=true ;;
  /depop/search) route_allowed=true ;;
  /depop/search-sellers) route_allowed=true ;;
  /depop/search/facets) route_allowed=true ;;
  /depop/sizes) route_allowed=true ;;
  /depop/suggest) route_allowed=true ;;
  /developer/search) route_allowed=true ;;
  /developer/sources) route_allowed=true ;;
  /discogs/search) route_allowed=true ;;
  /dominos/coupons) route_allowed=true ;;
  /dominos/customization) route_allowed=true ;;
  /dominos/menu) route_allowed=true ;;
  /dominos/nutrition) route_allowed=true ;;
  /dominos/store) route_allowed=true ;;
  /dominos/store-locator) route_allowed=true ;;
  /doordash/explore) route_allowed=true ;;
  /doordash/feed) route_allowed=true ;;
  /doordash/search) route_allowed=true ;;
  /doordash/search/autocomplete) route_allowed=true ;;
  /doordash/search/filters) route_allowed=true ;;
  /doordash/search/items) route_allowed=true ;;
  /draftkings/sportsbook/event) route_allowed=true ;;
  /draftkings/sportsbook/event-context) route_allowed=true ;;
  /draftkings/sportsbook/event-markets) route_allowed=true ;;
  /draftkings/sportsbook/featured-leagues) route_allowed=true ;;
  /draftkings/sportsbook/futures) route_allowed=true ;;
  /draftkings/sportsbook/league-events) route_allowed=true ;;
  /draftkings/sportsbook/leagues) route_allowed=true ;;
  /draftkings/sportsbook/live) route_allowed=true ;;
  /draftkings/sportsbook/odds) route_allowed=true ;;
  /draftkings/sportsbook/quick-links) route_allowed=true ;;
  /draftkings/sportsbook/team) route_allowed=true ;;
  /draftkings/sportsbook/teams) route_allowed=true ;;
  /duckduckgo/image) route_allowed=true ;;
  /duckduckgo/news) route_allowed=true ;;
  /duckduckgo/search) route_allowed=true ;;
  /duckduckgo/shopping) route_allowed=true ;;
  /duckduckgo/suggest) route_allowed=true ;;
  /duckduckgo/video) route_allowed=true ;;
  /dunkin/directory) route_allowed=true ;;
  /dunkin/menu) route_allowed=true ;;
  /dunkin/nearby) route_allowed=true ;;
  /dunkin/store) route_allowed=true ;;
  /dw/article) route_allowed=true ;;
  /dw/author) route_allowed=true ;;
  /dw/headlines) route_allowed=true ;;
  /dw/news) route_allowed=true ;;
  /dw/sections) route_allowed=true ;;
  /ebay/live/streams) route_allowed=true ;;
  /ebay/live/streams/batch) route_allowed=true ;;
  /ebay/search) route_allowed=true ;;
  /economictimes/article) route_allowed=true ;;
  /economictimes/author) route_allowed=true ;;
  /economictimes/headlines) route_allowed=true ;;
  /economictimes/news) route_allowed=true ;;
  /economictimes/sections) route_allowed=true ;;
  /engadget/article) route_allowed=true ;;
  /engadget/author) route_allowed=true ;;
  /engadget/headlines) route_allowed=true ;;
  /engadget/news) route_allowed=true ;;
  /engadget/sections) route_allowed=true ;;
  /eonline/article) route_allowed=true ;;
  /eonline/author) route_allowed=true ;;
  /eonline/headlines) route_allowed=true ;;
  /eonline/news) route_allowed=true ;;
  /eonline/sections) route_allowed=true ;;
  /espn/athlete) route_allowed=true ;;
  /espn/game-summary) route_allowed=true ;;
  /espn/news) route_allowed=true ;;
  /espn/rankings) route_allowed=true ;;
  /espn/scoreboard) route_allowed=true ;;
  /espn/standings) route_allowed=true ;;
  /espn/team) route_allowed=true ;;
  /espn/team-roster) route_allowed=true ;;
  /espn/teams) route_allowed=true ;;
  /etsy/search) route_allowed=true ;;
  /etsy/shop/search) route_allowed=true ;;
  /euronews/article) route_allowed=true ;;
  /euronews/author) route_allowed=true ;;
  /euronews/headlines) route_allowed=true ;;
  /euronews/news) route_allowed=true ;;
  /euronews/sections) route_allowed=true ;;
  /everlane/collections) route_allowed=true ;;
  /everlane/pages) route_allowed=true ;;
  /everlane/products) route_allowed=true ;;
  /everlane/search/suggest) route_allowed=true ;;
  /everlane/sitemap/urls) route_allowed=true ;;
  /everlane/sitemaps) route_allowed=true ;;
  /everlane/store) route_allowed=true ;;
  /ew/article) route_allowed=true ;;
  /ew/author) route_allowed=true ;;
  /ew/headlines) route_allowed=true ;;
  /ew/news) route_allowed=true ;;
  /ew/sections) route_allowed=true ;;
  /expedia/activities/search) route_allowed=true ;;
  /expedia/flights/search) route_allowed=true ;;
  /expedia/locations/search) route_allowed=true ;;
  /expedia/properties/detail) route_allowed=true ;;
  /expedia/properties/filters) route_allowed=true ;;
  /expedia/properties/reviews) route_allowed=true ;;
  /expedia/properties/search) route_allowed=true ;;
  /expresstribune/article) route_allowed=true ;;
  /expresstribune/author) route_allowed=true ;;
  /expresstribune/headlines) route_allowed=true ;;
  /expresstribune/news) route_allowed=true ;;
  /expresstribune/sections) route_allowed=true ;;
  /facebook/marketplace/search) route_allowed=true ;;
  /fanatics/categories) route_allowed=true ;;
  /fanatics/category) route_allowed=true ;;
  /fanatics/product) route_allowed=true ;;
  /fanatics/search) route_allowed=true ;;
  /fanaticscollect/auctions) route_allowed=true ;;
  /fanaticscollect/categories) route_allowed=true ;;
  /fanaticscollect/instant-rips/categories) route_allowed=true ;;
  /fanaticscollect/search) route_allowed=true ;;
  /fanaticscollect/sold-items) route_allowed=true ;;
  /fanaticscollect/trending-searches) route_allowed=true ;;
  /fanaticslive/browse) route_allowed=true ;;
  /fanaticslive/leagues) route_allowed=true ;;
  /fanaticslive/shops) route_allowed=true ;;
  /farfetch/categories) route_allowed=true ;;
  /farfetch/designers) route_allowed=true ;;
  /farfetch/product) route_allowed=true ;;
  /farfetch/search) route_allowed=true ;;
  /fashionnova/collections) route_allowed=true ;;
  /fashionnova/pages) route_allowed=true ;;
  /fashionnova/products) route_allowed=true ;;
  /fashionnova/search/suggest) route_allowed=true ;;
  /fashionnova/sitemap/urls) route_allowed=true ;;
  /fashionnova/sitemaps) route_allowed=true ;;
  /fashionnova/store) route_allowed=true ;;
  /fashionphile/collections) route_allowed=true ;;
  /fashionphile/pages) route_allowed=true ;;
  /fashionphile/products) route_allowed=true ;;
  /fashionphile/search) route_allowed=true ;;
  /fashionphile/search/suggest) route_allowed=true ;;
  /fashionphile/sitemap/urls) route_allowed=true ;;
  /fashionphile/sitemaps) route_allowed=true ;;
  /fashionphile/store) route_allowed=true ;;
  /fastcompany/article) route_allowed=true ;;
  /fastcompany/author) route_allowed=true ;;
  /fastcompany/headlines) route_allowed=true ;;
  /fastcompany/news) route_allowed=true ;;
  /fastcompany/sections) route_allowed=true ;;
  /fiveguys/directory) route_allowed=true ;;
  /fiveguys/faq) route_allowed=true ;;
  /fiveguys/faq-categories) route_allowed=true ;;
  /fiveguys/menu) route_allowed=true ;;
  /fiveguys/nearby) route_allowed=true ;;
  /fiveguys/nutrition) route_allowed=true ;;
  /fiveguys/ordering-locations) route_allowed=true ;;
  /fiveguys/ordering-menu) route_allowed=true ;;
  /fiveguys/search) route_allowed=true ;;
  /fiveguys/store) route_allowed=true ;;
  /fiverr/search) route_allowed=true ;;
  /flashscore/calendar) route_allowed=true ;;
  /flashscore/calendar-categories) route_allowed=true ;;
  /flashscore/competitions) route_allowed=true ;;
  /flashscore/entity-news) route_allowed=true ;;
  /flashscore/match-box-score) route_allowed=true ;;
  /flashscore/match-darts) route_allowed=true ;;
  /flashscore/match-h2h) route_allowed=true ;;
  /flashscore/match-highlights) route_allowed=true ;;
  /flashscore/match-info) route_allowed=true ;;
  /flashscore/match-lineups) route_allowed=true ;;
  /flashscore/match-missing-players) route_allowed=true ;;
  /flashscore/match-momentum) route_allowed=true ;;
  /flashscore/match-news) route_allowed=true ;;
  /flashscore/match-odds) route_allowed=true ;;
  /flashscore/match-player-stats) route_allowed=true ;;
  /flashscore/match-point-by-point) route_allowed=true ;;
  /flashscore/match-predicted-lineups) route_allowed=true ;;
  /flashscore/match-report) route_allowed=true ;;
  /flashscore/match-standings) route_allowed=true ;;
  /flashscore/match-stats) route_allowed=true ;;
  /flashscore/match-tv) route_allowed=true ;;
  /flashscore/navigation) route_allowed=true ;;
  /flashscore/news) route_allowed=true ;;
  /flashscore/news-article) route_allowed=true ;;
  /flashscore/news-article-body) route_allowed=true ;;
  /flashscore/news-categories) route_allowed=true ;;
  /flashscore/news-most-read) route_allowed=true ;;
  /flashscore/odds-geos) route_allowed=true ;;
  /flashscore/player) route_allowed=true ;;
  /flashscore/player-fixtures) route_allowed=true ;;
  /flashscore/player-injuries) route_allowed=true ;;
  /flashscore/player-match-log) route_allowed=true ;;
  /flashscore/player-news) route_allowed=true ;;
  /flashscore/player-results) route_allowed=true ;;
  /flashscore/player-transfers) route_allowed=true ;;
  /flashscore/ranking-categories) route_allowed=true ;;
  /flashscore/rankings) route_allowed=true ;;
  /flashscore/scores) route_allowed=true ;;
  /flashscore/search) route_allowed=true ;;
  /flashscore/sports) route_allowed=true ;;
  /flashscore/team) route_allowed=true ;;
  /flashscore/team-fixtures) route_allowed=true ;;
  /flashscore/team-news) route_allowed=true ;;
  /flashscore/team-outright-odds) route_allowed=true ;;
  /flashscore/team-results) route_allowed=true ;;
  /flashscore/team-squad) route_allowed=true ;;
  /flashscore/team-transfers) route_allowed=true ;;
  /flashscore/top-search) route_allowed=true ;;
  /flashscore/tournament-archive-seasons) route_allowed=true ;;
  /flashscore/tournament-events) route_allowed=true ;;
  /flashscore/tournament-outright-odds) route_allowed=true ;;
  /flashscore/tournament-seasons) route_allowed=true ;;
  /flashscore/tournament-standings) route_allowed=true ;;
  /flashscore/tournament-standings-views) route_allowed=true ;;
  /foodpanda/restaurant) route_allowed=true ;;
  /foodpanda/restaurant/menu) route_allowed=true ;;
  /foodpanda/restaurant/reviews) route_allowed=true ;;
  /foodpanda/search) route_allowed=true ;;
  /foodpanda/search/cuisines) route_allowed=true ;;
  /forbes/article) route_allowed=true ;;
  /forbes/author) route_allowed=true ;;
  /forbes/billionaires) route_allowed=true ;;
  /forbes/categories) route_allowed=true ;;
  /forbes/headlines) route_allowed=true ;;
  /forbes/person) route_allowed=true ;;
  /foreignaffairs/article) route_allowed=true ;;
  /foreignaffairs/author) route_allowed=true ;;
  /foreignaffairs/headlines) route_allowed=true ;;
  /foreignaffairs/topic) route_allowed=true ;;
  /foreignaffairs/topics) route_allowed=true ;;
  /foreignpolicy/article) route_allowed=true ;;
  /foreignpolicy/author) route_allowed=true ;;
  /foreignpolicy/headlines) route_allowed=true ;;
  /foreignpolicy/live) route_allowed=true ;;
  /foreignpolicy/live-detail) route_allowed=true ;;
  /foreignpolicy/project) route_allowed=true ;;
  /foreignpolicy/projects) route_allowed=true ;;
  /foreignpolicy/topic) route_allowed=true ;;
  /fortune/article) route_allowed=true ;;
  /fortune/author) route_allowed=true ;;
  /fortune/companies) route_allowed=true ;;
  /fortune/companies/filters) route_allowed=true ;;
  /fortune/company) route_allowed=true ;;
  /fortune/headlines) route_allowed=true ;;
  /fortune/news) route_allowed=true ;;
  /fortune/ranking) route_allowed=true ;;
  /fortune/ranking/filters) route_allowed=true ;;
  /fortune/ranking/lists) route_allowed=true ;;
  /fortune/ranking/years) route_allowed=true ;;
  /fortune/sections) route_allowed=true ;;
  /fotmob/audio-matches) route_allowed=true ;;
  /fotmob/fifa-ranking-periods) route_allowed=true ;;
  /fotmob/fifa-rankings) route_allowed=true ;;
  /fotmob/latest-news) route_allowed=true ;;
  /fotmob/league) route_allowed=true ;;
  /fotmob/leagues) route_allowed=true ;;
  /fotmob/lineup-builder-players) route_allowed=true ;;
  /fotmob/lineup-builder-team) route_allowed=true ;;
  /fotmob/match) route_allowed=true ;;
  /fotmob/match-media) route_allowed=true ;;
  /fotmob/matches) route_allowed=true ;;
  /fotmob/news) route_allowed=true ;;
  /fotmob/news-article) route_allowed=true ;;
  /fotmob/player) route_allowed=true ;;
  /fotmob/player-match-stats) route_allowed=true ;;
  /fotmob/player-matches) route_allowed=true ;;
  /fotmob/player-stats) route_allowed=true ;;
  /fotmob/search) route_allowed=true ;;
  /fotmob/seasons) route_allowed=true ;;
  /fotmob/stats) route_allowed=true ;;
  /fotmob/stats-categories) route_allowed=true ;;
  /fotmob/table) route_allowed=true ;;
  /fotmob/team) route_allowed=true ;;
  /fotmob/team-fixtures) route_allowed=true ;;
  /fotmob/team-news) route_allowed=true ;;
  /fotmob/transfers) route_allowed=true ;;
  /fotmob/trending-news) route_allowed=true ;;
  /fotmob/trending-searches) route_allowed=true ;;
  /fotmob/tv-guide) route_allowed=true ;;
  /fotmob/tv-guide-channels) route_allowed=true ;;
  /fotmob/tv-guide-countries) route_allowed=true ;;
  /foxnews/article) route_allowed=true ;;
  /foxnews/author) route_allowed=true ;;
  /foxnews/headlines) route_allowed=true ;;
  /foxnews/news) route_allowed=true ;;
  /foxnews/search) route_allowed=true ;;
  /foxnews/sections) route_allowed=true ;;
  /foxsports/article) route_allowed=true ;;
  /foxsports/headlines) route_allowed=true ;;
  /foxsports/news) route_allowed=true ;;
  /foxsports/sections) route_allowed=true ;;
  /france24/article) route_allowed=true ;;
  /france24/author) route_allowed=true ;;
  /france24/headlines) route_allowed=true ;;
  /france24/news) route_allowed=true ;;
  /france24/sections) route_allowed=true ;;
  /freemalaysiatoday/news) route_allowed=true ;;
  /freemalaysiatoday/sections) route_allowed=true ;;
  /ft/article) route_allowed=true ;;
  /ft/author) route_allowed=true ;;
  /ft/categories) route_allowed=true ;;
  /ft/headlines) route_allowed=true ;;
  /ft/news) route_allowed=true ;;
  /ft/search) route_allowed=true ;;
  /gamerant/article) route_allowed=true ;;
  /gamerant/author) route_allowed=true ;;
  /gamerant/headlines) route_allowed=true ;;
  /gamerant/news) route_allowed=true ;;
  /gamerant/sections) route_allowed=true ;;
  /gamesradar/article) route_allowed=true ;;
  /gamesradar/author) route_allowed=true ;;
  /gamesradar/headlines) route_allowed=true ;;
  /gamesradar/news) route_allowed=true ;;
  /gamesradar/sections) route_allowed=true ;;
  /gbnews/article) route_allowed=true ;;
  /gbnews/author) route_allowed=true ;;
  /gbnews/headlines) route_allowed=true ;;
  /gbnews/news) route_allowed=true ;;
  /gbnews/sections) route_allowed=true ;;
  /gdelt/context) route_allowed=true ;;
  /gdelt/search) route_allowed=true ;;
  /gdelt/timeline) route_allowed=true ;;
  /gdelt/tonechart) route_allowed=true ;;
  /gdelt/tv-concept-entities) route_allowed=true ;;
  /gdelt/tv-search) route_allowed=true ;;
  /gdelt/tv-showchart) route_allowed=true ;;
  /gdelt/tv-stationchart) route_allowed=true ;;
  /gdelt/tv-stationdetails) route_allowed=true ;;
  /gdelt/tv-timeline) route_allowed=true ;;
  /gdelt/tv-visual-entities) route_allowed=true ;;
  /gdelt/tv-wordcloud) route_allowed=true ;;
  /geocoding/lookup) route_allowed=true ;;
  /geocoding/reverse) route_allowed=true ;;
  /geocoding/search) route_allowed=true ;;
  /ghanaweb/archive) route_allowed=true ;;
  /ghanaweb/archive/months) route_allowed=true ;;
  /ghanaweb/article) route_allowed=true ;;
  /ghanaweb/headlines) route_allowed=true ;;
  /ghanaweb/news) route_allowed=true ;;
  /ghanaweb/sections) route_allowed=true ;;
  /ghanaweb/video) route_allowed=true ;;
  /ghanaweb/video-sections) route_allowed=true ;;
  /ghanaweb/videos) route_allowed=true ;;
  /github/search/repositories) route_allowed=true ;;
  /github/search/users) route_allowed=true ;;
  /github/trending) route_allowed=true ;;
  /github/trending/developers) route_allowed=true ;;
  /gizmodo/article) route_allowed=true ;;
  /gizmodo/author) route_allowed=true ;;
  /gizmodo/headlines) route_allowed=true ;;
  /gizmodo/news) route_allowed=true ;;
  /gizmodo/sections) route_allowed=true ;;
  /globalnews/article) route_allowed=true ;;
  /globalnews/author) route_allowed=true ;;
  /globalnews/headlines) route_allowed=true ;;
  /globalnews/news) route_allowed=true ;;
  /globalnews/sections) route_allowed=true ;;
  /globeandmail/article) route_allowed=true ;;
  /globeandmail/author) route_allowed=true ;;
  /globeandmail/headlines) route_allowed=true ;;
  /globeandmail/news) route_allowed=true ;;
  /globeandmail/sections) route_allowed=true ;;
  /gmanews/article) route_allowed=true ;;
  /gmanews/headlines) route_allowed=true ;;
  /gmanews/news) route_allowed=true ;;
  /gmanews/sections) route_allowed=true ;;
  /goat/collection) route_allowed=true ;;
  /goat/countries) route_allowed=true ;;
  /goat/curated) route_allowed=true ;;
  /goat/listings/count) route_allowed=true ;;
  /goat/search) route_allowed=true ;;
  /goat/search/facets) route_allowed=true ;;
  /goat/searches/trending) route_allowed=true ;;
  /goat/suggest) route_allowed=true ;;
  /goldin/auctions) route_allowed=true ;;
  /goldin/categories) route_allowed=true ;;
  /goldin/listing) route_allowed=true ;;
  /goldin/search) route_allowed=true ;;
  /goldin/suggest) route_allowed=true ;;
  /goodreads/lists) route_allowed=true ;;
  /goodreads/search) route_allowed=true ;;
  /goodrx/answer) route_allowed=true ;;
  /goodrx/answers) route_allowed=true ;;
  /goodrx/brands) route_allowed=true ;;
  /goodrx/class) route_allowed=true ;;
  /goodrx/classes) route_allowed=true ;;
  /goodrx/comparison) route_allowed=true ;;
  /goodrx/comparisons) route_allowed=true ;;
  /goodrx/condition) route_allowed=true ;;
  /goodrx/condition-drugs) route_allowed=true ;;
  /goodrx/conditions) route_allowed=true ;;
  /goodrx/drug-guide) route_allowed=true ;;
  /goodrx/drug-guides) route_allowed=true ;;
  /goodrx/drug-info) route_allowed=true ;;
  /goodrx/drug-options) route_allowed=true ;;
  /goodrx/drug-prices) route_allowed=true ;;
  /goodrx/drugs) route_allowed=true ;;
  /goodrx/health-article) route_allowed=true ;;
  /goodrx/health-articles) route_allowed=true ;;
  /goodrx/health-topics) route_allowed=true ;;
  /goodrx/pet-medications) route_allowed=true ;;
  /google-jobs/job) route_allowed=true ;;
  /google-jobs/search) route_allowed=true ;;
  /google/finance/context) route_allowed=true ;;
  /google/finance/markets/earnings) route_allowed=true ;;
  /google/finance/markets/featured) route_allowed=true ;;
  /google/finance/markets/headline) route_allowed=true ;;
  /google/finance/markets/indices) route_allowed=true ;;
  /google/finance/markets/movers) route_allowed=true ;;
  /google/finance/markets/top) route_allowed=true ;;
  /google/finance/markets/trending) route_allowed=true ;;
  /google/finance/search) route_allowed=true ;;
  /google/jobs) route_allowed=true ;;
  /google/map/search) route_allowed=true ;;
  /google/news) route_allowed=true ;;
  /google/suggest) route_allowed=true ;;
  /google/trends/categories) route_allowed=true ;;
  /google/trends/enums) route_allowed=true ;;
  /google/trends/explore) route_allowed=true ;;
  /google/trends/explore/interest-by-region) route_allowed=true ;;
  /google/trends/explore/interest-over-time) route_allowed=true ;;
  /google/trends/explore/related-topics) route_allowed=true ;;
  /google/trends/explore/rising-queries) route_allowed=true ;;
  /google/trends/explore/top-queries) route_allowed=true ;;
  /google/trends/locations) route_allowed=true ;;
  /google/trends/trending) route_allowed=true ;;
  /google/trends/trending/detail) route_allowed=true ;;
  /google/videos) route_allowed=true ;;
  /googlepatents/classification) route_allowed=true ;;
  /googlepatents/coverage) route_allowed=true ;;
  /googlepatents/detail) route_allowed=true ;;
  /googlepatents/recent) route_allowed=true ;;
  /googlepatents/search) route_allowed=true ;;
  /googlepatents/suggest) route_allowed=true ;;
  /googleplay/app) route_allowed=true ;;
  /googleplay/categories) route_allowed=true ;;
  /googleplay/datasafety) route_allowed=true ;;
  /googleplay/list) route_allowed=true ;;
  /googleplay/permissions) route_allowed=true ;;
  /googleplay/ratings) route_allowed=true ;;
  /googleplay/reviews) route_allowed=true ;;
  /googleplay/search) route_allowed=true ;;
  /googleplay/similar) route_allowed=true ;;
  /gq/article) route_allowed=true ;;
  /gq/author) route_allowed=true ;;
  /gq/headlines) route_allowed=true ;;
  /gq/news) route_allowed=true ;;
  /gq/sections) route_allowed=true ;;
  /grailed/categories) route_allowed=true ;;
  /grailed/collection) route_allowed=true ;;
  /grailed/collections) route_allowed=true ;;
  /grailed/designers) route_allowed=true ;;
  /grailed/listing) route_allowed=true ;;
  /grailed/search) route_allowed=true ;;
  /grailed/seller) route_allowed=true ;;
  /grailed/seller-reviews) route_allowed=true ;;
  /grailed/similar-listings) route_allowed=true ;;
  /grailed/sold-listings) route_allowed=true ;;
  /grailed/suggest) route_allowed=true ;;
  /greystar/articles) route_allowed=true ;;
  /greystar/location) route_allowed=true ;;
  /greystar/locations) route_allowed=true ;;
  /greystar/markets) route_allowed=true ;;
  /greystar/newsroom) route_allowed=true ;;
  /greystar/search) route_allowed=true ;;
  /greystar/unit-locations) route_allowed=true ;;
  /greystar/units) route_allowed=true ;;
  /grubhub/availability) route_allowed=true ;;
  /grubhub/offers) route_allowed=true ;;
  /grubhub/restaurant) route_allowed=true ;;
  /grubhub/restaurant/menu) route_allowed=true ;;
  /grubhub/restaurant/reviews) route_allowed=true ;;
  /grubhub/search) route_allowed=true ;;
  /grubhub/timepicker) route_allowed=true ;;
  /guardian/article) route_allowed=true ;;
  /guardian/author) route_allowed=true ;;
  /guardian/headlines) route_allowed=true ;;
  /guardian/topic) route_allowed=true ;;
  /gucci/categories) route_allowed=true ;;
  /gucci/category) route_allowed=true ;;
  /gucci/product) route_allowed=true ;;
  /gucci/recommendations) route_allowed=true ;;
  /gucci/search) route_allowed=true ;;
  /gucci/size-guide) route_allowed=true ;;
  /gucci/store) route_allowed=true ;;
  /gucci/stores) route_allowed=true ;;
  /gucci/stores/search) route_allowed=true ;;
  /gucci/suggest) route_allowed=true ;;
  /gulfnews/article) route_allowed=true ;;
  /gulfnews/author) route_allowed=true ;;
  /gulfnews/headlines) route_allowed=true ;;
  /gulfnews/news) route_allowed=true ;;
  /gulfnews/sections) route_allowed=true ;;
  /gymshark/collections) route_allowed=true ;;
  /gymshark/pages) route_allowed=true ;;
  /gymshark/products) route_allowed=true ;;
  /gymshark/sitemap/urls) route_allowed=true ;;
  /gymshark/sitemaps) route_allowed=true ;;
  /gymshark/store) route_allowed=true ;;
  /hbr/article) route_allowed=true ;;
  /hbr/categories) route_allowed=true ;;
  /hbr/headlines) route_allowed=true ;;
  /hbr/topic) route_allowed=true ;;
  /healthgrades/autocomplete) route_allowed=true ;;
  /healthgrades/facilities/filters) route_allowed=true ;;
  /healthgrades/facilities/search) route_allowed=true ;;
  /healthgrades/facility) route_allowed=true ;;
  /healthgrades/health-article) route_allowed=true ;;
  /healthgrades/health-articles) route_allowed=true ;;
  /healthgrades/health-topics) route_allowed=true ;;
  /healthgrades/hospital) route_allowed=true ;;
  /healthgrades/hospital-awards) route_allowed=true ;;
  /healthgrades/hospital-awards/filters) route_allowed=true ;;
  /healthgrades/locations) route_allowed=true ;;
  /healthgrades/physician) route_allowed=true ;;
  /healthgrades/physicians/filters) route_allowed=true ;;
  /healthgrades/physicians/search) route_allowed=true ;;
  /healthgrades/specialties) route_allowed=true ;;
  /healthgrades/top-searches) route_allowed=true ;;
  /hermes/categories) route_allowed=true ;;
  /hermes/category) route_allowed=true ;;
  /hermes/product) route_allowed=true ;;
  /hermes/product/recommendations) route_allowed=true ;;
  /hermes/products) route_allowed=true ;;
  /hermes/search) route_allowed=true ;;
  /hermes/stores) route_allowed=true ;;
  /hermes/suggest) route_allowed=true ;;
  /hindustantimes/article) route_allowed=true ;;
  /hindustantimes/author) route_allowed=true ;;
  /hindustantimes/headlines) route_allowed=true ;;
  /hindustantimes/news) route_allowed=true ;;
  /hindustantimes/sections) route_allowed=true ;;
  /hm/categories) route_allowed=true ;;
  /hm/listing) route_allowed=true ;;
  /hm/search) route_allowed=true ;;
  /hm/search/suggestions) route_allowed=true ;;
  /hm/stores) route_allowed=true ;;
  /hollywoodreporter/article) route_allowed=true ;;
  /hollywoodreporter/author) route_allowed=true ;;
  /hollywoodreporter/headlines) route_allowed=true ;;
  /hollywoodreporter/news) route_allowed=true ;;
  /hollywoodreporter/sections) route_allowed=true ;;
  /homedepot/categories) route_allowed=true ;;
  /homedepot/category) route_allowed=true ;;
  /homedepot/search) route_allowed=true ;;
  /homedepot/suggest) route_allowed=true ;;
  /hotels/autocomplete) route_allowed=true ;;
  /hotels/offers) route_allowed=true ;;
  /hotels/property) route_allowed=true ;;
  /hotels/rates) route_allowed=true ;;
  /hotels/reviews) route_allowed=true ;;
  /hotels/reviews/archive) route_allowed=true ;;
  /hotels/search) route_allowed=true ;;
  /houston-chronicle/article) route_allowed=true ;;
  /houston-chronicle/author) route_allowed=true ;;
  /houston-chronicle/headlines) route_allowed=true ;;
  /houston-chronicle/news) route_allowed=true ;;
  /houston-chronicle/sections) route_allowed=true ;;
  /howtogeek/news) route_allowed=true ;;
  /huffpost/article) route_allowed=true ;;
  /huffpost/author) route_allowed=true ;;
  /huffpost/headlines) route_allowed=true ;;
  /huffpost/news) route_allowed=true ;;
  /huffpost/sections) route_allowed=true ;;
  /ign/article) route_allowed=true ;;
  /ign/author) route_allowed=true ;;
  /ign/headlines) route_allowed=true ;;
  /ign/news) route_allowed=true ;;
  /ign/sections) route_allowed=true ;;
  /ikea/availability) route_allowed=true ;;
  /ikea/categories) route_allowed=true ;;
  /ikea/category) route_allowed=true ;;
  /ikea/product) route_allowed=true ;;
  /ikea/reviews) route_allowed=true ;;
  /ikea/search) route_allowed=true ;;
  /ikea/store) route_allowed=true ;;
  /ikea/stores) route_allowed=true ;;
  /ikea/suggest) route_allowed=true ;;
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
  /importyeti/company) route_allowed=true ;;
  /importyeti/search) route_allowed=true ;;
  /indeed/job) route_allowed=true ;;
  /indeed/locations/suggest) route_allowed=true ;;
  /indeed/search) route_allowed=true ;;
  /independent/article) route_allowed=true ;;
  /independent/author) route_allowed=true ;;
  /independent/headlines) route_allowed=true ;;
  /independent/news) route_allowed=true ;;
  /independent/sections) route_allowed=true ;;
  /indianexpress/article) route_allowed=true ;;
  /indianexpress/author) route_allowed=true ;;
  /indianexpress/headlines) route_allowed=true ;;
  /indianexpress/news) route_allowed=true ;;
  /indianexpress/sections) route_allowed=true ;;
  /indiatoday/article) route_allowed=true ;;
  /indiatoday/author) route_allowed=true ;;
  /indiatoday/headlines) route_allowed=true ;;
  /indiatoday/news) route_allowed=true ;;
  /indiatoday/sections) route_allowed=true ;;
  /indiewire/article) route_allowed=true ;;
  /indiewire/author) route_allowed=true ;;
  /indiewire/headlines) route_allowed=true ;;
  /indiewire/news) route_allowed=true ;;
  /indiewire/sections) route_allowed=true ;;
  /inews/article) route_allowed=true ;;
  /inews/author) route_allowed=true ;;
  /inews/headlines) route_allowed=true ;;
  /inews/news) route_allowed=true ;;
  /inews/sections) route_allowed=true ;;
  /inquirer/article) route_allowed=true ;;
  /inquirer/author) route_allowed=true ;;
  /inquirer/headlines) route_allowed=true ;;
  /inquirer/news) route_allowed=true ;;
  /inquirer/sections) route_allowed=true ;;
  /instacart/departments) route_allowed=true ;;
  /instacart/item) route_allowed=true ;;
  /instacart/search) route_allowed=true ;;
  /instacart/search-nearby) route_allowed=true ;;
  /instacart/stores) route_allowed=true ;;
  /instacart/trending) route_allowed=true ;;
  /investopedia/article) route_allowed=true ;;
  /investopedia/author) route_allowed=true ;;
  /investopedia/headlines) route_allowed=true ;;
  /investopedia/news) route_allowed=true ;;
  /investopedia/sections) route_allowed=true ;;
  /iol/article) route_allowed=true ;;
  /iol/author) route_allowed=true ;;
  /iol/headlines) route_allowed=true ;;
  /iol/news) route_allowed=true ;;
  /iol/sections) route_allowed=true ;;
  /irishindependent/article) route_allowed=true ;;
  /irishindependent/author) route_allowed=true ;;
  /irishindependent/headlines) route_allowed=true ;;
  /irishindependent/news) route_allowed=true ;;
  /irishindependent/sections) route_allowed=true ;;
  /irishtimes/article) route_allowed=true ;;
  /irishtimes/author) route_allowed=true ;;
  /irishtimes/headlines) route_allowed=true ;;
  /irishtimes/news) route_allowed=true ;;
  /irishtimes/sections) route_allowed=true ;;
  /japantimes/article) route_allowed=true ;;
  /japantimes/author) route_allowed=true ;;
  /japantimes/headlines) route_allowed=true ;;
  /japantimes/news) route_allowed=true ;;
  /japantimes/sections) route_allowed=true ;;
  /jcrew/categories) route_allowed=true ;;
  /jcrew/category) route_allowed=true ;;
  /jcrew/product) route_allowed=true ;;
  /jcrew/product/reviews) route_allowed=true ;;
  /jcrew/search) route_allowed=true ;;
  /jcrew/size-chart) route_allowed=true ;;
  /jcrew/stores) route_allowed=true ;;
  /jcrew/suggest) route_allowed=true ;;
  /jerusalempost/article) route_allowed=true ;;
  /jerusalempost/author) route_allowed=true ;;
  /jerusalempost/authors) route_allowed=true ;;
  /jerusalempost/headlines) route_allowed=true ;;
  /jerusalempost/news) route_allowed=true ;;
  /jerusalempost/sections) route_allowed=true ;;
  /jimmy-johns/menu) route_allowed=true ;;
  /jimmy-johns/modifiers) route_allowed=true ;;
  /jimmy-johns/nearby) route_allowed=true ;;
  /jimmy-johns/sitemap) route_allowed=true ;;
  /jimmy-johns/store) route_allowed=true ;;
  /jobs/ashby/board) route_allowed=true ;;
  /jobs/company-search) route_allowed=true ;;
  /jobs/eightfold/board) route_allowed=true ;;
  /jobs/eightfold/job) route_allowed=true ;;
  /jobs/gem/board) route_allowed=true ;;
  /jobs/greenhouse/board) route_allowed=true ;;
  /jobs/greenhouse/job) route_allowed=true ;;
  /jobs/hiring-signals) route_allowed=true ;;
  /jobs/icims/board) route_allowed=true ;;
  /jobs/icims/job) route_allowed=true ;;
  /jobs/lever/posting) route_allowed=true ;;
  /jobs/lever/postings) route_allowed=true ;;
  /jobs/oracle/board) route_allowed=true ;;
  /jobs/oracle/job) route_allowed=true ;;
  /jobs/personio/feed) route_allowed=true ;;
  /jobs/phenom/board) route_allowed=true ;;
  /jobs/phenom/job) route_allowed=true ;;
  /jobs/pinpoint/board) route_allowed=true ;;
  /jobs/recruitee/offer) route_allowed=true ;;
  /jobs/recruitee/offers) route_allowed=true ;;
  /jobs/rippling/board) route_allowed=true ;;
  /jobs/rippling/job) route_allowed=true ;;
  /jobs/smartrecruiters/posting) route_allowed=true ;;
  /jobs/smartrecruiters/postings) route_allowed=true ;;
  /jobs/teamtailor/jobs) route_allowed=true ;;
  /jobs/ukg/board) route_allowed=true ;;
  /jobs/workable/posting) route_allowed=true ;;
  /jobs/workable/postings) route_allowed=true ;;
  /jobs/workday/board) route_allowed=true ;;
  /jobs/workday/job) route_allowed=true ;;
  /justeat/restaurant) route_allowed=true ;;
  /justeat/restaurant/menu) route_allowed=true ;;
  /justeat/search) route_allowed=true ;;
  /justeat/search/filters) route_allowed=true ;;
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
  /kalshi/events) route_allowed=true ;;
  /kalshi/events/multivariate) route_allowed=true ;;
  /kalshi/exchange/schedule) route_allowed=true ;;
  /kalshi/exchange/status) route_allowed=true ;;
  /kalshi/historical/cutoff) route_allowed=true ;;
  /kalshi/historical/markets) route_allowed=true ;;
  /kalshi/historical/trades) route_allowed=true ;;
  /kalshi/markets) route_allowed=true ;;
  /kalshi/markets/history) route_allowed=true ;;
  /kalshi/markets/orderbooks) route_allowed=true ;;
  /kalshi/series) route_allowed=true ;;
  /kalshi/trades) route_allowed=true ;;
  /kfc/delivery-estimate) route_allowed=true ;;
  /kfc/menu) route_allowed=true ;;
  /kfc/nearby) route_allowed=true ;;
  /kfc/promotion) route_allowed=true ;;
  /kfc/promotions) route_allowed=true ;;
  /kfc/store) route_allowed=true ;;
  /kfc/stores) route_allowed=true ;;
  /khaleejtimes/article) route_allowed=true ;;
  /khaleejtimes/author) route_allowed=true ;;
  /khaleejtimes/headlines) route_allowed=true ;;
  /khaleejtimes/news) route_allowed=true ;;
  /khaleejtimes/sections) route_allowed=true ;;
  /kickstarter/comments) route_allowed=true ;;
  /kickstarter/discover) route_allowed=true ;;
  /kickstarter/project) route_allowed=true ;;
  /kickstarter/updates) route_allowed=true ;;
  /kohls/category) route_allowed=true ;;
  /kohls/product/reviews) route_allowed=true ;;
  /kohls/stores) route_allowed=true ;;
  /kohls/suggest) route_allowed=true ;;
  /kotaku/article) route_allowed=true ;;
  /kotaku/author) route_allowed=true ;;
  /kotaku/headlines) route_allowed=true ;;
  /kotaku/news) route_allowed=true ;;
  /kotaku/sections) route_allowed=true ;;
  /kroger/categories) route_allowed=true ;;
  /kroger/category) route_allowed=true ;;
  /kroger/coupons) route_allowed=true ;;
  /kroger/product) route_allowed=true ;;
  /kroger/product/reviews) route_allowed=true ;;
  /kroger/products) route_allowed=true ;;
  /kroger/related-tags) route_allowed=true ;;
  /kroger/search) route_allowed=true ;;
  /kroger/store) route_allowed=true ;;
  /kroger/suggest) route_allowed=true ;;
  /kyliecosmetics/collections) route_allowed=true ;;
  /kyliecosmetics/pages) route_allowed=true ;;
  /kyliecosmetics/products) route_allowed=true ;;
  /kyliecosmetics/search/suggest) route_allowed=true ;;
  /kyliecosmetics/sitemap/urls) route_allowed=true ;;
  /kyliecosmetics/sitemaps) route_allowed=true ;;
  /kyliecosmetics/store) route_allowed=true ;;
  /latimes/article) route_allowed=true ;;
  /latimes/author) route_allowed=true ;;
  /latimes/headlines) route_allowed=true ;;
  /latimes/sections) route_allowed=true ;;
  /lazada/categories) route_allowed=true ;;
  /lazada/category-products) route_allowed=true ;;
  /lazada/home) route_allowed=true ;;
  /lazada/product) route_allowed=true ;;
  /lazada/search) route_allowed=true ;;
  /leboncoin/listing) route_allowed=true ;;
  /leboncoin/search) route_allowed=true ;;
  /letterboxd/popular) route_allowed=true ;;
  /letterboxd/search) route_allowed=true ;;
  /linkedin/product/categories) route_allowed=true ;;
  /linkedin/products/search) route_allowed=true ;;
  /livemint/article) route_allowed=true ;;
  /livemint/author) route_allowed=true ;;
  /livemint/headlines) route_allowed=true ;;
  /livemint/news) route_allowed=true ;;
  /livemint/sections) route_allowed=true ;;
  /liverpoolecho/article) route_allowed=true ;;
  /liverpoolecho/author) route_allowed=true ;;
  /liverpoolecho/headlines) route_allowed=true ;;
  /liverpoolecho/news) route_allowed=true ;;
  /liverpoolecho/sections) route_allowed=true ;;
  /livescience/article) route_allowed=true ;;
  /livescience/author) route_allowed=true ;;
  /livescience/headlines) route_allowed=true ;;
  /livescience/news) route_allowed=true ;;
  /livescience/sections) route_allowed=true ;;
  /livescore/competition) route_allowed=true ;;
  /livescore/competitions) route_allowed=true ;;
  /livescore/live-scores) route_allowed=true ;;
  /livescore/match) route_allowed=true ;;
  /livescore/match-stats) route_allowed=true ;;
  /livescore/news) route_allowed=true ;;
  /livescore/news-article) route_allowed=true ;;
  /livescore/news-categories) route_allowed=true ;;
  /livescore/news-feed) route_allowed=true ;;
  /livescore/news-publishers) route_allowed=true ;;
  /livescore/player) route_allowed=true ;;
  /livescore/scores) route_allowed=true ;;
  /livescore/scores-toc) route_allowed=true ;;
  /livescore/search) route_allowed=true ;;
  /livescore/sports) route_allowed=true ;;
  /livescore/team) route_allowed=true ;;
  /lululemon/categories) route_allowed=true ;;
  /lululemon/category) route_allowed=true ;;
  /lululemon/outfit) route_allowed=true ;;
  /lululemon/stores) route_allowed=true ;;
  /macrumors/article) route_allowed=true ;;
  /macrumors/author) route_allowed=true ;;
  /macrumors/headlines) route_allowed=true ;;
  /macrumors/news) route_allowed=true ;;
  /macrumors/sections) route_allowed=true ;;
  /macys/product/reviews) route_allowed=true ;;
  /macys/suggest) route_allowed=true ;;
  /makeuseof/article) route_allowed=true ;;
  /makeuseof/author) route_allowed=true ;;
  /makeuseof/headlines) route_allowed=true ;;
  /makeuseof/news) route_allowed=true ;;
  /makeuseof/sections) route_allowed=true ;;
  /malaymail/article) route_allowed=true ;;
  /malaymail/headlines) route_allowed=true ;;
  /malaymail/news) route_allowed=true ;;
  /malaymail/sections) route_allowed=true ;;
  /manga/rankings) route_allowed=true ;;
  /manga/search) route_allowed=true ;;
  /marketwatch/article) route_allowed=true ;;
  /marketwatch/author) route_allowed=true ;;
  /marketwatch/headlines) route_allowed=true ;;
  /marketwatch/news) route_allowed=true ;;
  /marketwatch/sections) route_allowed=true ;;
  /mashable/article) route_allowed=true ;;
  /mashable/author) route_allowed=true ;;
  /mashable/headlines) route_allowed=true ;;
  /mashable/news) route_allowed=true ;;
  /mashable/sections) route_allowed=true ;;
  /mcdonalds/categories) route_allowed=true ;;
  /mcdonalds/item) route_allowed=true ;;
  /mcdonalds/item-list) route_allowed=true ;;
  /mcdonalds/menu) route_allowed=true ;;
  /mcdonalds/restaurant-menu) route_allowed=true ;;
  /mcdonalds/restaurants) route_allowed=true ;;
  /mediaite/article) route_allowed=true ;;
  /mediaite/author) route_allowed=true ;;
  /mediaite/headlines) route_allowed=true ;;
  /mediaite/news) route_allowed=true ;;
  /mediaite/sections) route_allowed=true ;;
  /medicalnewstoday/article) route_allowed=true ;;
  /medicalnewstoday/author) route_allowed=true ;;
  /medicalnewstoday/headlines) route_allowed=true ;;
  /medicalnewstoday/news) route_allowed=true ;;
  /medicalnewstoday/sections) route_allowed=true ;;
  /men/article) route_allowed=true ;;
  /men/author) route_allowed=true ;;
  /men/headlines) route_allowed=true ;;
  /men/news) route_allowed=true ;;
  /men/sections) route_allowed=true ;;
  /mercari/autocomplete) route_allowed=true ;;
  /mercari/home) route_allowed=true ;;
  /mercari/master) route_allowed=true ;;
  /mercari/search) route_allowed=true ;;
  /meta-jobs/job) route_allowed=true ;;
  /meta-jobs/list) route_allowed=true ;;
  /meta-jobs/search) route_allowed=true ;;
  /metacritic/browse) route_allowed=true ;;
  /metaculus/comments-feed) route_allowed=true ;;
  /metaculus/questions) route_allowed=true ;;
  /metaculus/top-comments) route_allowed=true ;;
  /metro/article) route_allowed=true ;;
  /metro/author) route_allowed=true ;;
  /metro/headlines) route_allowed=true ;;
  /metro/news) route_allowed=true ;;
  /metro/sections) route_allowed=true ;;
  /microsoftstore/categories) route_allowed=true ;;
  /microsoftstore/category) route_allowed=true ;;
  /microsoftstore/charts) route_allowed=true ;;
  /microsoftstore/editorial) route_allowed=true ;;
  /microsoftstore/events) route_allowed=true ;;
  /microsoftstore/product) route_allowed=true ;;
  /microsoftstore/publisher) route_allowed=true ;;
  /microsoftstore/recommended) route_allowed=true ;;
  /microsoftstore/related) route_allowed=true ;;
  /microsoftstore/reviews) route_allowed=true ;;
  /microsoftstore/reviews/summary) route_allowed=true ;;
  /microsoftstore/search) route_allowed=true ;;
  /microsoftstore/spotlight) route_allowed=true ;;
  /microsoftstore/suggest) route_allowed=true ;;
  /mirror/article) route_allowed=true ;;
  /mirror/author) route_allowed=true ;;
  /mirror/headlines) route_allowed=true ;;
  /mirror/news) route_allowed=true ;;
  /mirror/sections) route_allowed=true ;;
  /mlb/discovery) route_allowed=true ;;
  /mlb/editorial-feed) route_allowed=true ;;
  /mlb/game) route_allowed=true ;;
  /mlb/game-boxscore) route_allowed=true ;;
  /mlb/game-play-by-play) route_allowed=true ;;
  /mlb/league-leaders) route_allowed=true ;;
  /mlb/league-stats) route_allowed=true ;;
  /mlb/player) route_allowed=true ;;
  /mlb/player-stats) route_allowed=true ;;
  /mlb/prospect-rankings) route_allowed=true ;;
  /mlb/prospect-stats) route_allowed=true ;;
  /mlb/schedule) route_allowed=true ;;
  /mlb/search) route_allowed=true ;;
  /mlb/standings) route_allowed=true ;;
  /mlb/statcast-abs-challenges) route_allowed=true ;;
  /mlb/statcast-active-spin) route_allowed=true ;;
  /mlb/statcast-arm-angle) route_allowed=true ;;
  /mlb/statcast-arm-strength) route_allowed=true ;;
  /mlb/statcast-arm-strength-player) route_allowed=true ;;
  /mlb/statcast-arm-value) route_allowed=true ;;
  /mlb/statcast-arm-value-details) route_allowed=true ;;
  /mlb/statcast-baserunning) route_allowed=true ;;
  /mlb/statcast-bat-tracking) route_allowed=true ;;
  /mlb/statcast-batted-ball) route_allowed=true ;;
  /mlb/statcast-birthday-index) route_allowed=true ;;
  /mlb/statcast-catcher-blocking) route_allowed=true ;;
  /mlb/statcast-catcher-blocking-details) route_allowed=true ;;
  /mlb/statcast-catcher-framing) route_allowed=true ;;
  /mlb/statcast-catcher-framing-details) route_allowed=true ;;
  /mlb/statcast-catcher-pop-time) route_allowed=true ;;
  /mlb/statcast-catcher-stance) route_allowed=true ;;
  /mlb/statcast-catcher-throwing) route_allowed=true ;;
  /mlb/statcast-catcher-throwing-details) route_allowed=true ;;
  /mlb/statcast-expected) route_allowed=true ;;
  /mlb/statcast-fielding-run-value) route_allowed=true ;;
  /mlb/statcast-first-base-receiving) route_allowed=true ;;
  /mlb/statcast-first-base-receiving-details) route_allowed=true ;;
  /mlb/statcast-home-runs) route_allowed=true ;;
  /mlb/statcast-home-runs-details) route_allowed=true ;;
  /mlb/statcast-leaders) route_allowed=true ;;
  /mlb/statcast-oaa) route_allowed=true ;;
  /mlb/statcast-park-factors) route_allowed=true ;;
  /mlb/statcast-percentile) route_allowed=true ;;
  /mlb/statcast-pitch-arsenal) route_allowed=true ;;
  /mlb/statcast-pitch-arsenal-details) route_allowed=true ;;
  /mlb/statcast-pitch-arsenals) route_allowed=true ;;
  /mlb/statcast-pitch-movement) route_allowed=true ;;
  /mlb/statcast-pitch-tempo) route_allowed=true ;;
  /mlb/statcast-pitch-tempo-player) route_allowed=true ;;
  /mlb/statcast-pitch-timer) route_allowed=true ;;
  /mlb/statcast-player-details) route_allowed=true ;;
  /mlb/statcast-rolling) route_allowed=true ;;
  /mlb/statcast-run-value) route_allowed=true ;;
  /mlb/statcast-running-game) route_allowed=true ;;
  /mlb/statcast-running-game-details) route_allowed=true ;;
  /mlb/statcast-sprint-speed) route_allowed=true ;;
  /mlb/statcast-sprint-speed-teams) route_allowed=true ;;
  /mlb/statcast-swing-path) route_allowed=true ;;
  /mlb/statcast-swing-timing) route_allowed=true ;;
  /mlb/statcast-swing-timing-details) route_allowed=true ;;
  /mlb/statcast-top-performers) route_allowed=true ;;
  /mlb/statcast-year-to-year) route_allowed=true ;;
  /mlb/team-roster) route_allowed=true ;;
  /mlb/team-stats) route_allowed=true ;;
  /mlb/teams) route_allowed=true ;;
  /mlb/transactions) route_allowed=true ;;
  /mlive/news) route_allowed=true ;;
  /modaoperandi/categories) route_allowed=true ;;
  /modaoperandi/designers) route_allowed=true ;;
  /modaoperandi/product) route_allowed=true ;;
  /modaoperandi/search) route_allowed=true ;;
  /moncler/categories) route_allowed=true ;;
  /moncler/category) route_allowed=true ;;
  /moncler/product) route_allowed=true ;;
  /moncler/search) route_allowed=true ;;
  /moncler/stores) route_allowed=true ;;
  /moncler/suggest) route_allowed=true ;;
  /moneycontrol/article) route_allowed=true ;;
  /moneycontrol/author) route_allowed=true ;;
  /moneycontrol/headlines) route_allowed=true ;;
  /moneycontrol/news) route_allowed=true ;;
  /moneycontrol/sections) route_allowed=true ;;
  /motleyfool/article) route_allowed=true ;;
  /motleyfool/author) route_allowed=true ;;
  /motleyfool/headlines) route_allowed=true ;;
  /motleyfool/news) route_allowed=true ;;
  /motleyfool/sections) route_allowed=true ;;
  /nationafrica/article) route_allowed=true ;;
  /nationafrica/author) route_allowed=true ;;
  /nationafrica/headlines) route_allowed=true ;;
  /nationafrica/news) route_allowed=true ;;
  /nationafrica/sections) route_allowed=true ;;
  /national/article) route_allowed=true ;;
  /national/author) route_allowed=true ;;
  /national/headlines) route_allowed=true ;;
  /national/news) route_allowed=true ;;
  /national/sections) route_allowed=true ;;
  /nationalpost/article) route_allowed=true ;;
  /nationalpost/author) route_allowed=true ;;
  /nationalpost/headlines) route_allowed=true ;;
  /nationalpost/news) route_allowed=true ;;
  /nationalpost/sections) route_allowed=true ;;
  /nbc/article) route_allowed=true ;;
  /nbc/author) route_allowed=true ;;
  /nbc/headlines) route_allowed=true ;;
  /nbc/news) route_allowed=true ;;
  /nbc/sections) route_allowed=true ;;
  /ndtv/article) route_allowed=true ;;
  /ndtv/author) route_allowed=true ;;
  /ndtv/headlines) route_allowed=true ;;
  /ndtv/latest-videos) route_allowed=true ;;
  /ndtv/live-blog) route_allowed=true ;;
  /ndtv/live-blogs) route_allowed=true ;;
  /ndtv/news) route_allowed=true ;;
  /ndtv/search) route_allowed=true ;;
  /ndtv/sections) route_allowed=true ;;
  /ndtv/video) route_allowed=true ;;
  /ndtv/video-categories) route_allowed=true ;;
  /ndtv/videos) route_allowed=true ;;
  /news18/article) route_allowed=true ;;
  /news18/author) route_allowed=true ;;
  /news18/headlines) route_allowed=true ;;
  /news18/news) route_allowed=true ;;
  /news18/sections) route_allowed=true ;;
  /news24/article) route_allowed=true ;;
  /news24/headlines) route_allowed=true ;;
  /news24/news) route_allowed=true ;;
  /news24/sections) route_allowed=true ;;
  /newscomau/article) route_allowed=true ;;
  /newscomau/author) route_allowed=true ;;
  /newscomau/headlines) route_allowed=true ;;
  /newscomau/news) route_allowed=true ;;
  /newscomau/sections) route_allowed=true ;;
  /newsmax/article) route_allowed=true ;;
  /newsmax/author) route_allowed=true ;;
  /newsmax/headlines) route_allowed=true ;;
  /newsmax/news) route_allowed=true ;;
  /newsmax/sections) route_allowed=true ;;
  /newsweek/article) route_allowed=true ;;
  /newsweek/author) route_allowed=true ;;
  /newsweek/headlines) route_allowed=true ;;
  /newsweek/news) route_allowed=true ;;
  /newsweek/sections) route_allowed=true ;;
  /newyorker/article) route_allowed=true ;;
  /newyorker/author) route_allowed=true ;;
  /newyorker/headlines) route_allowed=true ;;
  /newyorker/news) route_allowed=true ;;
  /newyorker/sections) route_allowed=true ;;
  /nike/categories) route_allowed=true ;;
  /nike/product) route_allowed=true ;;
  /nike/product/availability) route_allowed=true ;;
  /nike/product/details) route_allowed=true ;;
  /nike/product/recommendations) route_allowed=true ;;
  /nike/product/reviews) route_allowed=true ;;
  /nike/search) route_allowed=true ;;
  /nike/stores) route_allowed=true ;;
  /nike/suggest) route_allowed=true ;;
  /ninetofivegoogle/article) route_allowed=true ;;
  /ninetofivegoogle/author) route_allowed=true ;;
  /ninetofivegoogle/headlines) route_allowed=true ;;
  /ninetofivegoogle/news) route_allowed=true ;;
  /ninetofivegoogle/sections) route_allowed=true ;;
  /ninetofivemac/article) route_allowed=true ;;
  /ninetofivemac/author) route_allowed=true ;;
  /ninetofivemac/headlines) route_allowed=true ;;
  /ninetofivemac/news) route_allowed=true ;;
  /ninetofivemac/sections) route_allowed=true ;;
  /njcom/news) route_allowed=true ;;
  /npr/article) route_allowed=true ;;
  /npr/author) route_allowed=true ;;
  /npr/categories) route_allowed=true ;;
  /npr/headlines) route_allowed=true ;;
  /npr/topic) route_allowed=true ;;
  /numbeo/cost-of-living/country) route_allowed=true ;;
  /numbeo/cost-of-living/rankings) route_allowed=true ;;
  /numbeo/cost-of-living/rankings-by-country) route_allowed=true ;;
  /numbeo/indices/country) route_allowed=true ;;
  /numbeo/indices/rankings) route_allowed=true ;;
  /numbeo/indices/rankings-by-country) route_allowed=true ;;
  /nydailynews/article) route_allowed=true ;;
  /nydailynews/author) route_allowed=true ;;
  /nydailynews/headlines) route_allowed=true ;;
  /nydailynews/news) route_allowed=true ;;
  /nydailynews/sections) route_allowed=true ;;
  /nymag/article) route_allowed=true ;;
  /nymag/author) route_allowed=true ;;
  /nymag/headlines) route_allowed=true ;;
  /nymag/news) route_allowed=true ;;
  /nymag/sections) route_allowed=true ;;
  /nypost/article) route_allowed=true ;;
  /nypost/author) route_allowed=true ;;
  /nypost/headlines) route_allowed=true ;;
  /nypost/news) route_allowed=true ;;
  /nypost/sections) route_allowed=true ;;
  /nyt/article) route_allowed=true ;;
  /nyt/author) route_allowed=true ;;
  /nyt/categories) route_allowed=true ;;
  /nyt/headlines) route_allowed=true ;;
  /nyt/sections) route_allowed=true ;;
  /nzherald/article) route_allowed=true ;;
  /nzherald/author) route_allowed=true ;;
  /nzherald/headlines) route_allowed=true ;;
  /nzherald/news) route_allowed=true ;;
  /nzherald/sections) route_allowed=true ;;
  /ohpolly/collections) route_allowed=true ;;
  /ohpolly/pages) route_allowed=true ;;
  /ohpolly/products) route_allowed=true ;;
  /ohpolly/search/suggest) route_allowed=true ;;
  /ohpolly/sitemap/urls) route_allowed=true ;;
  /ohpolly/sitemaps) route_allowed=true ;;
  /ohpolly/store) route_allowed=true ;;
  /oldnavy/categories) route_allowed=true ;;
  /oldnavy/category) route_allowed=true ;;
  /oldnavy/product) route_allowed=true ;;
  /oldnavy/product/availability) route_allowed=true ;;
  /oldnavy/product/reviews) route_allowed=true ;;
  /oldnavy/search) route_allowed=true ;;
  /oldnavy/stores) route_allowed=true ;;
  /opensea/activity) route_allowed=true ;;
  /opensea/categories) route_allowed=true ;;
  /opensea/chains) route_allowed=true ;;
  /opensea/collections) route_allowed=true ;;
  /opensea/drops) route_allowed=true ;;
  /opensea/most-watched) route_allowed=true ;;
  /opensea/rankings) route_allowed=true ;;
  /opensea/search/collections) route_allowed=true ;;
  /opensea/top-movers) route_allowed=true ;;
  /opentable/restaurant) route_allowed=true ;;
  /opentable/restaurant/menus) route_allowed=true ;;
  /opentable/restaurant/reviews) route_allowed=true ;;
  /opentable/search) route_allowed=true ;;
  /otto/categories) route_allowed=true ;;
  /otto/product) route_allowed=true ;;
  /otto/search) route_allowed=true ;;
  /pagesix/article) route_allowed=true ;;
  /pagesix/author) route_allowed=true ;;
  /pagesix/headlines) route_allowed=true ;;
  /pagesix/news) route_allowed=true ;;
  /pagesix/sections) route_allowed=true ;;
  /pandamart/search) route_allowed=true ;;
  /pandamart/store) route_allowed=true ;;
  /pandamart/store/categories) route_allowed=true ;;
  /pandamart/store/product) route_allowed=true ;;
  /pandamart/store/products) route_allowed=true ;;
  /pandamart/store/search) route_allowed=true ;;
  /panera/at-work-locations) route_allowed=true ;;
  /panera/cafe) route_allowed=true ;;
  /panera/catering-delivery-info) route_allowed=true ;;
  /panera/catering-menu) route_allowed=true ;;
  /panera/geocode) route_allowed=true ;;
  /panera/item-detail) route_allowed=true ;;
  /panera/item-options) route_allowed=true ;;
  /panera/locations) route_allowed=true ;;
  /panera/menu) route_allowed=true ;;
  /panera/quantity-rules) route_allowed=true ;;
  /panera/retired-products) route_allowed=true ;;
  /panera/time-slots) route_allowed=true ;;
  /panera/upsell-suggestions) route_allowed=true ;;
  /papajohns/allergens) route_allowed=true ;;
  /papajohns/colombia/menu) route_allowed=true ;;
  /papajohns/deals) route_allowed=true ;;
  /papajohns/directory) route_allowed=true ;;
  /papajohns/elsalvador/menu) route_allowed=true ;;
  /papajohns/india/deal) route_allowed=true ;;
  /papajohns/india/menu) route_allowed=true ;;
  /papajohns/india/menu/item) route_allowed=true ;;
  /papajohns/india/stores) route_allowed=true ;;
  /papajohns/intl/deals) route_allowed=true ;;
  /papajohns/intl/ingredients) route_allowed=true ;;
  /papajohns/intl/menu) route_allowed=true ;;
  /papajohns/intl/offer) route_allowed=true ;;
  /papajohns/intl/product) route_allowed=true ;;
  /papajohns/intl/stores) route_allowed=true ;;
  /papajohns/menu) route_allowed=true ;;
  /papajohns/menu/item) route_allowed=true ;;
  /papajohns/nearby) route_allowed=true ;;
  /papajohns/nutrition) route_allowed=true ;;
  /papajohns/peru/menu) route_allowed=true ;;
  /papajohns/poland/menu) route_allowed=true ;;
  /papajohns/russia/menu) route_allowed=true ;;
  /papajohns/store) route_allowed=true ;;
  /patreon/creator) route_allowed=true ;;
  /patreon/creator/tiers) route_allowed=true ;;
  /patreon/explore) route_allowed=true ;;
  /patreon/rss) route_allowed=true ;;
  /pcgamer/article) route_allowed=true ;;
  /pcgamer/author) route_allowed=true ;;
  /pcgamer/headlines) route_allowed=true ;;
  /pcgamer/news) route_allowed=true ;;
  /pcgamer/sections) route_allowed=true ;;
  /pcmag/article) route_allowed=true ;;
  /pcmag/author) route_allowed=true ;;
  /pcmag/headlines) route_allowed=true ;;
  /pcmag/news) route_allowed=true ;;
  /pcmag/sections) route_allowed=true ;;
  /people/article) route_allowed=true ;;
  /people/author) route_allowed=true ;;
  /people/headlines) route_allowed=true ;;
  /people/news) route_allowed=true ;;
  /people/sections) route_allowed=true ;;
  /phillyinquirer/article) route_allowed=true ;;
  /phillyinquirer/author) route_allowed=true ;;
  /phillyinquirer/headlines) route_allowed=true ;;
  /phillyinquirer/news) route_allowed=true ;;
  /phillyinquirer/sections) route_allowed=true ;;
  /philstar/article) route_allowed=true ;;
  /philstar/author) route_allowed=true ;;
  /philstar/headlines) route_allowed=true ;;
  /philstar/news) route_allowed=true ;;
  /philstar/sections) route_allowed=true ;;
  /phonearena/article) route_allowed=true ;;
  /phonearena/author) route_allowed=true ;;
  /phonearena/headlines) route_allowed=true ;;
  /phonearena/news) route_allowed=true ;;
  /phonearena/sections) route_allowed=true ;;
  /physorg/article) route_allowed=true ;;
  /physorg/headlines) route_allowed=true ;;
  /physorg/news) route_allowed=true ;;
  /physorg/sections) route_allowed=true ;;
  /pinterest/categories) route_allowed=true ;;
  /pinterest/search) route_allowed=true ;;
  /pitchbook/advisor) route_allowed=true ;;
  /pitchbook/company) route_allowed=true ;;
  /pitchbook/fund) route_allowed=true ;;
  /pitchbook/investor) route_allowed=true ;;
  /pitchbook/limited-partner) route_allowed=true ;;
  /pizzahut/bundle-choices) route_allowed=true ;;
  /pizzahut/delivery-estimate) route_allowed=true ;;
  /pizzahut/menu) route_allowed=true ;;
  /pizzahut/modifiers) route_allowed=true ;;
  /pizzahut/store) route_allowed=true ;;
  /pizzahut/stores) route_allowed=true ;;
  /playstation/browse) route_allowed=true ;;
  /playstation/category) route_allowed=true ;;
  /playstation/concept) route_allowed=true ;;
  /playstation/concept/reviews) route_allowed=true ;;
  /playstation/deals) route_allowed=true ;;
  /playstation/latest) route_allowed=true ;;
  /playstation/page) route_allowed=true ;;
  /playstation/product) route_allowed=true ;;
  /playstation/search) route_allowed=true ;;
  /playstation/suggest) route_allowed=true ;;
  /politico/article) route_allowed=true ;;
  /politico/author) route_allowed=true ;;
  /politico/categories) route_allowed=true ;;
  /politico/headlines) route_allowed=true ;;
  /politico/topic) route_allowed=true ;;
  /polygon/article) route_allowed=true ;;
  /polygon/author) route_allowed=true ;;
  /polygon/headlines) route_allowed=true ;;
  /polygon/news) route_allowed=true ;;
  /polygon/sections) route_allowed=true ;;
  /polymarket/activity/trades) route_allowed=true ;;
  /polymarket/dashboards/macro) route_allowed=true ;;
  /polymarket/events) route_allowed=true ;;
  /polymarket/events/similar) route_allowed=true ;;
  /polymarket/fee-types) route_allowed=true ;;
  /polymarket/homepage/feed) route_allowed=true ;;
  /polymarket/leaderboard) route_allowed=true ;;
  /polymarket/markets) route_allowed=true ;;
  /polymarket/predictions) route_allowed=true ;;
  /polymarket/rewards/markets) route_allowed=true ;;
  /polymarket/search) route_allowed=true ;;
  /polymarket/tags) route_allowed=true ;;
  /polymarket/tokens/midpoints) route_allowed=true ;;
  /polymarket/tokens/orderbooks) route_allowed=true ;;
  /polymarket/tokens/prices) route_allowed=true ;;
  /polymarket/tokens/spreads) route_allowed=true ;;
  /popeyes/faq) route_allowed=true ;;
  /popeyes/location) route_allowed=true ;;
  /popeyes/locations) route_allowed=true ;;
  /popeyes/menu) route_allowed=true ;;
  /popeyes/offers) route_allowed=true ;;
  /popeyes/promotions) route_allowed=true ;;
  /popeyes/quests) route_allowed=true ;;
  /popeyes/rewards) route_allowed=true ;;
  /popularmechanics/news) route_allowed=true ;;
  /poshmark/brands) route_allowed=true ;;
  /poshmark/categories) route_allowed=true ;;
  /poshmark/search) route_allowed=true ;;
  /prada/categories) route_allowed=true ;;
  /prada/category) route_allowed=true ;;
  /prada/product) route_allowed=true ;;
  /prada/search) route_allowed=true ;;
  /prada/stores) route_allowed=true ;;
  /prada/suggest) route_allowed=true ;;
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
  /producthunt/leaderboard) route_allowed=true ;;
  /producthunt/search) route_allowed=true ;;
  /propublica/article) route_allowed=true ;;
  /propublica/author) route_allowed=true ;;
  /propublica/headlines) route_allowed=true ;;
  /propublica/news) route_allowed=true ;;
  /propublica/sections) route_allowed=true ;;
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
  /punch/article) route_allowed=true ;;
  /punch/author) route_allowed=true ;;
  /punch/headlines) route_allowed=true ;;
  /punch/news) route_allowed=true ;;
  /punch/sections) route_allowed=true ;;
  /quince/categories) route_allowed=true ;;
  /quince/navigation) route_allowed=true ;;
  /quince/product) route_allowed=true ;;
  /quince/product/faq) route_allowed=true ;;
  /quince/product/reviews) route_allowed=true ;;
  /quince/search) route_allowed=true ;;
  /quince/sitemap/urls) route_allowed=true ;;
  /quince/sitemaps) route_allowed=true ;;
  /quince/suggest) route_allowed=true ;;
  /qwant/suggest) route_allowed=true ;;
  /raisingcanes/directory) route_allowed=true ;;
  /raisingcanes/menu) route_allowed=true ;;
  /raisingcanes/nearby) route_allowed=true ;;
  /raisingcanes/promotion) route_allowed=true ;;
  /raisingcanes/promotions) route_allowed=true ;;
  /raisingcanes/store) route_allowed=true ;;
  /rappler/article) route_allowed=true ;;
  /rappler/author) route_allowed=true ;;
  /rappler/headlines) route_allowed=true ;;
  /rappler/news) route_allowed=true ;;
  /rappler/sections) route_allowed=true ;;
  /rawstory/article) route_allowed=true ;;
  /rawstory/author) route_allowed=true ;;
  /rawstory/headlines) route_allowed=true ;;
  /rawstory/news) route_allowed=true ;;
  /rawstory/sections) route_allowed=true ;;
  /rebag/collections) route_allowed=true ;;
  /rebag/pages) route_allowed=true ;;
  /rebag/products) route_allowed=true ;;
  /rebag/search) route_allowed=true ;;
  /rebag/search/suggest) route_allowed=true ;;
  /rebag/sitemap/urls) route_allowed=true ;;
  /rebag/sitemaps) route_allowed=true ;;
  /rebag/store) route_allowed=true ;;
  /reddit/leads) route_allowed=true ;;
  /reddit/search) route_allowed=true ;;
  /reddit/subreddits/posts) route_allowed=true ;;
  /reddit/trends) route_allowed=true ;;
  /redfin/estimate) route_allowed=true ;;
  /redfin/property) route_allowed=true ;;
  /redfin/region-trends) route_allowed=true ;;
  /redfin/search) route_allowed=true ;;
  /redfin/similar) route_allowed=true ;;
  /research/jobs) route_allowed=true ;;
  /research/papers/metadata) route_allowed=true ;;
  /research/papers/read) route_allowed=true ;;
  /research/papers/related) route_allowed=true ;;
  /research/papers/search) route_allowed=true ;;
  /research/sources) route_allowed=true ;;
  /resy/availability) route_allowed=true ;;
  /resy/cuisines) route_allowed=true ;;
  /resy/event) route_allowed=true ;;
  /resy/events) route_allowed=true ;;
  /resy/locations) route_allowed=true ;;
  /resy/restaurant) route_allowed=true ;;
  /resy/search) route_allowed=true ;;
  /retailmenot/autocomplete) route_allowed=true ;;
  /retailmenot/blog-categories) route_allowed=true ;;
  /retailmenot/blog-post) route_allowed=true ;;
  /retailmenot/blog-posts) route_allowed=true ;;
  /retailmenot/blog-tags) route_allowed=true ;;
  /retailmenot/cashback) route_allowed=true ;;
  /retailmenot/categories) route_allowed=true ;;
  /retailmenot/category) route_allowed=true ;;
  /retailmenot/deal-event) route_allowed=true ;;
  /retailmenot/deal-events) route_allowed=true ;;
  /retailmenot/home) route_allowed=true ;;
  /retailmenot/store) route_allowed=true ;;
  /retailmenot/stores) route_allowed=true ;;
  /reuters/article) route_allowed=true ;;
  /reuters/articles) route_allowed=true ;;
  /reuters/author) route_allowed=true ;;
  /reuters/news) route_allowed=true ;;
  /reuters/section) route_allowed=true ;;
  /reuters/sections) route_allowed=true ;;
  /reverb/categories) route_allowed=true ;;
  /reverb/listing) route_allowed=true ;;
  /reverb/makes) route_allowed=true ;;
  /reverb/price-guide) route_allowed=true ;;
  /reverb/price-guide-search) route_allowed=true ;;
  /reverb/search) route_allowed=true ;;
  /reverb/shop) route_allowed=true ;;
  /reverb/shop-feedback) route_allowed=true ;;
  /rightmove/agents) route_allowed=true ;;
  /rightmove/autocomplete) route_allowed=true ;;
  /rightmove/commercial/search) route_allowed=true ;;
  /rightmove/new-homes/search) route_allowed=true ;;
  /rightmove/search) route_allowed=true ;;
  /rightmove/student/search) route_allowed=true ;;
  /rnz/article) route_allowed=true ;;
  /rnz/author) route_allowed=true ;;
  /rnz/headlines) route_allowed=true ;;
  /rnz/news) route_allowed=true ;;
  /rnz/sections) route_allowed=true ;;
  /roblox/badges) route_allowed=true ;;
  /roblox/game) route_allowed=true ;;
  /roblox/rankings) route_allowed=true ;;
  /roblox/search) route_allowed=true ;;
  /rollingstone/article) route_allowed=true ;;
  /rollingstone/author) route_allowed=true ;;
  /rollingstone/headlines) route_allowed=true ;;
  /rollingstone/news) route_allowed=true ;;
  /rollingstone/sections) route_allowed=true ;;
  /rothys/collections) route_allowed=true ;;
  /rothys/pages) route_allowed=true ;;
  /rothys/products) route_allowed=true ;;
  /rothys/search/suggest) route_allowed=true ;;
  /rothys/sitemap/urls) route_allowed=true ;;
  /rothys/sitemaps) route_allowed=true ;;
  /rothys/store) route_allowed=true ;;
  /rottentomatoes/browse/filters) route_allowed=true ;;
  /rottentomatoes/browse/movies) route_allowed=true ;;
  /rottentomatoes/browse/tv) route_allowed=true ;;
  /rottentomatoes/critics/authors) route_allowed=true ;;
  /rottentomatoes/editorial/content) route_allowed=true ;;
  /rottentomatoes/editorial/detail) route_allowed=true ;;
  /rottentomatoes/editorial/search) route_allowed=true ;;
  /rottentomatoes/editorial/section) route_allowed=true ;;
  /rottentomatoes/editorial/taxonomies) route_allowed=true ;;
  /rottentomatoes/editorial/terms) route_allowed=true ;;
  /rottentomatoes/editorial/types) route_allowed=true ;;
  /rottentomatoes/episode) route_allowed=true ;;
  /rottentomatoes/movie) route_allowed=true ;;
  /rottentomatoes/movie/reviews) route_allowed=true ;;
  /rottentomatoes/person) route_allowed=true ;;
  /rottentomatoes/search) route_allowed=true ;;
  /rottentomatoes/season) route_allowed=true ;;
  /rottentomatoes/series) route_allowed=true ;;
  /rottentomatoes/sitemap/urls) route_allowed=true ;;
  /rottentomatoes/sitemaps) route_allowed=true ;;
  /rover/search) route_allowed=true ;;
  /rover/trainer-search) route_allowed=true ;;
  /rte/article) route_allowed=true ;;
  /rte/author) route_allowed=true ;;
  /rte/headlines) route_allowed=true ;;
  /rte/news) route_allowed=true ;;
  /rte/sections) route_allowed=true ;;
  /salon/article) route_allowed=true ;;
  /salon/author) route_allowed=true ;;
  /salon/headlines) route_allowed=true ;;
  /salon/news) route_allowed=true ;;
  /salon/sections) route_allowed=true ;;
  /samsclub/category) route_allowed=true ;;
  /samsclub/departments) route_allowed=true ;;
  /sbsnews/article) route_allowed=true ;;
  /sbsnews/author) route_allowed=true ;;
  /sbsnews/headlines) route_allowed=true ;;
  /sbsnews/news) route_allowed=true ;;
  /sbsnews/sections) route_allowed=true ;;
  /sciencealert/article) route_allowed=true ;;
  /sciencealert/author) route_allowed=true ;;
  /sciencealert/headlines) route_allowed=true ;;
  /sciencealert/news) route_allowed=true ;;
  /sciencealert/sections) route_allowed=true ;;
  /scmp/article) route_allowed=true ;;
  /scmp/author) route_allowed=true ;;
  /scmp/headlines) route_allowed=true ;;
  /scmp/sections) route_allowed=true ;;
  /screenrant/article) route_allowed=true ;;
  /screenrant/author) route_allowed=true ;;
  /screenrant/headlines) route_allowed=true ;;
  /screenrant/news) route_allowed=true ;;
  /screenrant/sections) route_allowed=true ;;
  /seatgeek/categories) route_allowed=true ;;
  /seatgeek/cities) route_allowed=true ;;
  /seatgeek/event) route_allowed=true ;;
  /seatgeek/events-by-category) route_allowed=true ;;
  /seatgeek/events-near) route_allowed=true ;;
  /seatgeek/performer) route_allowed=true ;;
  /seatgeek/performer-events) route_allowed=true ;;
  /seatgeek/search) route_allowed=true ;;
  /seatgeek/trending) route_allowed=true ;;
  /seatgeek/venue) route_allowed=true ;;
  /seatgeek/venue-events) route_allowed=true ;;
  /seattletimes/article) route_allowed=true ;;
  /seattletimes/author) route_allowed=true ;;
  /seattletimes/headlines) route_allowed=true ;;
  /seattletimes/news) route_allowed=true ;;
  /seattletimes/sections) route_allowed=true ;;
  /sec/company/intelligence) route_allowed=true ;;
  /sec/company/search) route_allowed=true ;;
  /sec/company/submissions) route_allowed=true ;;
  /sec/filing) route_allowed=true ;;
  /sec/filing/sections) route_allowed=true ;;
  /sec/financials) route_allowed=true ;;
  /sec/frames) route_allowed=true ;;
  /sec/full-text-search) route_allowed=true ;;
  /sec/insider) route_allowed=true ;;
  /sec/institutional-holdings) route_allowed=true ;;
  /sephora/brands) route_allowed=true ;;
  /sephora/categories) route_allowed=true ;;
  /sephora/category) route_allowed=true ;;
  /sephora/product) route_allowed=true ;;
  /sephora/product/questions) route_allowed=true ;;
  /sephora/product/reviews) route_allowed=true ;;
  /sephora/search) route_allowed=true ;;
  /sephora/stores) route_allowed=true ;;
  /sephora/suggest) route_allowed=true ;;
  /sevennewsau/article) route_allowed=true ;;
  /sevennewsau/author) route_allowed=true ;;
  /sevennewsau/headlines) route_allowed=true ;;
  /sevennewsau/news) route_allowed=true ;;
  /sevennewsau/sections) route_allowed=true ;;
  /sfgate/article) route_allowed=true ;;
  /sfgate/author) route_allowed=true ;;
  /sfgate/headlines) route_allowed=true ;;
  /sfgate/news) route_allowed=true ;;
  /sfgate/sections) route_allowed=true ;;
  /shakeshack/locations) route_allowed=true ;;
  /shakeshack/menu) route_allowed=true ;;
  /shakeshack/nearby) route_allowed=true ;;
  /shakeshack/store) route_allowed=true ;;
  /shein/category/filters) route_allowed=true ;;
  /shein/category/goods) route_allowed=true ;;
  /shein/category/nav) route_allowed=true ;;
  /shein/products/aggregation-filters) route_allowed=true ;;
  /shein/products/detail) route_allowed=true ;;
  /shein/products/search) route_allowed=true ;;
  /shein/search/autocomplete) route_allowed=true ;;
  /shein/search/keywords) route_allowed=true ;;
  /shop-app/analysis) route_allowed=true ;;
  /shop-app/categories) route_allowed=true ;;
  /shop-app/search) route_allowed=true ;;
  /shop-app/suggestions) route_allowed=true ;;
  /shopify/collections) route_allowed=true ;;
  /shopify/pages) route_allowed=true ;;
  /shopify/products) route_allowed=true ;;
  /shopify/search/suggest) route_allowed=true ;;
  /shopify/sitemap/urls) route_allowed=true ;;
  /shopify/sitemaps) route_allowed=true ;;
  /shopify/store) route_allowed=true ;;
  /similarweb/search) route_allowed=true ;;
  /skims/collections) route_allowed=true ;;
  /skims/pages) route_allowed=true ;;
  /skims/products) route_allowed=true ;;
  /skims/search/suggest) route_allowed=true ;;
  /skims/sitemap/urls) route_allowed=true ;;
  /skims/sitemaps) route_allowed=true ;;
  /skims/store) route_allowed=true ;;
  /skynews/article) route_allowed=true ;;
  /skynews/author) route_allowed=true ;;
  /skynews/headlines) route_allowed=true ;;
  /skynews/news) route_allowed=true ;;
  /skynews/sections) route_allowed=true ;;
  /skynews/video) route_allowed=true ;;
  /skynews/videos) route_allowed=true ;;
  /skysports/article) route_allowed=true ;;
  /skysports/author) route_allowed=true ;;
  /skysports/headlines) route_allowed=true ;;
  /skysports/news) route_allowed=true ;;
  /skysports/sections) route_allowed=true ;;
  /slate/article) route_allowed=true ;;
  /slate/categories) route_allowed=true ;;
  /slate/headlines) route_allowed=true ;;
  /slickdeals/categories) route_allowed=true ;;
  /slickdeals/category) route_allowed=true ;;
  /slickdeals/comments) route_allowed=true ;;
  /slickdeals/deal) route_allowed=true ;;
  /slickdeals/deal-types) route_allowed=true ;;
  /slickdeals/forums) route_allowed=true ;;
  /slickdeals/frontpage) route_allowed=true ;;
  /slickdeals/primary-categories) route_allowed=true ;;
  /slickdeals/primary-category) route_allowed=true ;;
  /slickdeals/search) route_allowed=true ;;
  /slickdeals/search/advanced) route_allowed=true ;;
  /sloanreview/article) route_allowed=true ;;
  /sloanreview/articles) route_allowed=true ;;
  /sloanreview/categories) route_allowed=true ;;
  /sloanreview/headlines) route_allowed=true ;;
  /sloanreview/topic) route_allowed=true ;;
  /smh/article) route_allowed=true ;;
  /smh/author) route_allowed=true ;;
  /smh/headlines) route_allowed=true ;;
  /smh/news) route_allowed=true ;;
  /smh/sections) route_allowed=true ;;
  /sofascore/categories) route_allowed=true ;;
  /sofascore/category-tournaments) route_allowed=true ;;
  /sofascore/draft) route_allowed=true ;;
  /sofascore/draft-picks) route_allowed=true ;;
  /sofascore/esports-game) route_allowed=true ;;
  /sofascore/event) route_allowed=true ;;
  /sofascore/event-at-bat-pitches) route_allowed=true ;;
  /sofascore/event-at-bats) route_allowed=true ;;
  /sofascore/event-average-positions) route_allowed=true ;;
  /sofascore/event-baseball-top-performers) route_allowed=true ;;
  /sofascore/event-best-players) route_allowed=true ;;
  /sofascore/event-comments) route_allowed=true ;;
  /sofascore/event-esports-games) route_allowed=true ;;
  /sofascore/event-graph) route_allowed=true ;;
  /sofascore/event-h2h) route_allowed=true ;;
  /sofascore/event-highlights) route_allowed=true ;;
  /sofascore/event-incidents) route_allowed=true ;;
  /sofascore/event-innings) route_allowed=true ;;
  /sofascore/event-lineups) route_allowed=true ;;
  /sofascore/event-managers) route_allowed=true ;;
  /sofascore/event-odds) route_allowed=true ;;
  /sofascore/event-player-heatmap) route_allowed=true ;;
  /sofascore/event-player-statistics) route_allowed=true ;;
  /sofascore/event-point-by-point) route_allowed=true ;;
  /sofascore/event-pregame-form) route_allowed=true ;;
  /sofascore/event-shotmap) route_allowed=true ;;
  /sofascore/event-statistics) route_allowed=true ;;
  /sofascore/event-team-heatmap) route_allowed=true ;;
  /sofascore/event-team-streaks) route_allowed=true ;;
  /sofascore/event-tennis-power) route_allowed=true ;;
  /sofascore/event-tv-channels) route_allowed=true ;;
  /sofascore/event-votes) route_allowed=true ;;
  /sofascore/live-events) route_allowed=true ;;
  /sofascore/manager) route_allowed=true ;;
  /sofascore/manager-events) route_allowed=true ;;
  /sofascore/mma-card) route_allowed=true ;;
  /sofascore/mma-schedule) route_allowed=true ;;
  /sofascore/odds-dropping) route_allowed=true ;;
  /sofascore/odds-winning) route_allowed=true ;;
  /sofascore/player) route_allowed=true ;;
  /sofascore/player-attributes) route_allowed=true ;;
  /sofascore/player-events) route_allowed=true ;;
  /sofascore/player-last-year-summary) route_allowed=true ;;
  /sofascore/player-national-team-statistics) route_allowed=true ;;
  /sofascore/player-penalty-history) route_allowed=true ;;
  /sofascore/player-ratings) route_allowed=true ;;
  /sofascore/player-season-heatmap) route_allowed=true ;;
  /sofascore/player-season-statistics) route_allowed=true ;;
  /sofascore/player-statistical-rankings) route_allowed=true ;;
  /sofascore/player-statistics-seasons) route_allowed=true ;;
  /sofascore/player-tournaments) route_allowed=true ;;
  /sofascore/player-transfers) route_allowed=true ;;
  /sofascore/ranking-types) route_allowed=true ;;
  /sofascore/rankings) route_allowed=true ;;
  /sofascore/referee) route_allowed=true ;;
  /sofascore/referee-events) route_allowed=true ;;
  /sofascore/referee-statistics) route_allowed=true ;;
  /sofascore/round-events) route_allowed=true ;;
  /sofascore/scheduled-events) route_allowed=true ;;
  /sofascore/scheduled-tournaments) route_allowed=true ;;
  /sofascore/search) route_allowed=true ;;
  /sofascore/search-typed) route_allowed=true ;;
  /sofascore/season-events) route_allowed=true ;;
  /sofascore/sports) route_allowed=true ;;
  /sofascore/stage) route_allowed=true ;;
  /sofascore/stage-categories) route_allowed=true ;;
  /sofascore/stage-driver-performance) route_allowed=true ;;
  /sofascore/stage-featured) route_allowed=true ;;
  /sofascore/stage-schedule) route_allowed=true ;;
  /sofascore/stage-seasons) route_allowed=true ;;
  /sofascore/stage-standings) route_allowed=true ;;
  /sofascore/stage-substages) route_allowed=true ;;
  /sofascore/standings) route_allowed=true ;;
  /sofascore/team) route_allowed=true ;;
  /sofascore/team-achievements) route_allowed=true ;;
  /sofascore/team-events) route_allowed=true ;;
  /sofascore/team-goal-distributions) route_allowed=true ;;
  /sofascore/team-near-events) route_allowed=true ;;
  /sofascore/team-of-the-week) route_allowed=true ;;
  /sofascore/team-of-the-week-periods) route_allowed=true ;;
  /sofascore/team-performance) route_allowed=true ;;
  /sofascore/team-player-statistics) route_allowed=true ;;
  /sofascore/team-player-statistics-seasons) route_allowed=true ;;
  /sofascore/team-players) route_allowed=true ;;
  /sofascore/team-rankings) route_allowed=true ;;
  /sofascore/team-season-statistics) route_allowed=true ;;
  /sofascore/team-statistics-seasons) route_allowed=true ;;
  /sofascore/team-top-players) route_allowed=true ;;
  /sofascore/team-tournaments) route_allowed=true ;;
  /sofascore/team-transfers) route_allowed=true ;;
  /sofascore/tennis-player-grand-slam-results) route_allowed=true ;;
  /sofascore/tournament-cuptree) route_allowed=true ;;
  /sofascore/tournament-info) route_allowed=true ;;
  /sofascore/tournament-player-of-the-season) route_allowed=true ;;
  /sofascore/tournament-player-statistics) route_allowed=true ;;
  /sofascore/tournament-rounds) route_allowed=true ;;
  /sofascore/tournament-seasons) route_allowed=true ;;
  /sofascore/tournament-statistics-info) route_allowed=true ;;
  /sofascore/tournament-team-of-the-season) route_allowed=true ;;
  /sofascore/tournament-teams) route_allowed=true ;;
  /sofascore/tournament-top-players) route_allowed=true ;;
  /sofascore/tournament-top-teams) route_allowed=true ;;
  /sofascore/tournament-venues) route_allowed=true ;;
  /sofascore/tournament-winners) route_allowed=true ;;
  /sofascore/tournaments-with-feature) route_allowed=true ;;
  /sofascore/trending-events) route_allowed=true ;;
  /sofascore/trending-players) route_allowed=true ;;
  /sofascore/venue) route_allowed=true ;;
  /sofascore/venue-events) route_allowed=true ;;
  /sonic/availability) route_allowed=true ;;
  /sonic/categories) route_allowed=true ;;
  /sonic/deals) route_allowed=true ;;
  /sonic/directory) route_allowed=true ;;
  /sonic/item) route_allowed=true ;;
  /sonic/location-suggest) route_allowed=true ;;
  /sonic/locations) route_allowed=true ;;
  /sonic/menu) route_allowed=true ;;
  /sonic/nearby) route_allowed=true ;;
  /sonic/nutrition-documents) route_allowed=true ;;
  /sonic/sitemap) route_allowed=true ;;
  /sonic/store) route_allowed=true ;;
  /soundcloud/playlist) route_allowed=true ;;
  /soundcloud/profile) route_allowed=true ;;
  /soundcloud/search) route_allowed=true ;;
  /soundcloud/track) route_allowed=true ;;
  /soundcloud/user-tracks) route_allowed=true ;;
  /space/article) route_allowed=true ;;
  /space/author) route_allowed=true ;;
  /space/headlines) route_allowed=true ;;
  /space/news) route_allowed=true ;;
  /space/sections) route_allowed=true ;;
  /sparkfun/categories) route_allowed=true ;;
  /sparkfun/category) route_allowed=true ;;
  /sparkfun/product) route_allowed=true ;;
  /sparkfun/search) route_allowed=true ;;
  /sportingnews/article) route_allowed=true ;;
  /sportingnews/author) route_allowed=true ;;
  /sportingnews/headlines) route_allowed=true ;;
  /sportingnews/news) route_allowed=true ;;
  /sportingnews/sections) route_allowed=true ;;
  /sportskeeda/article) route_allowed=true ;;
  /sportskeeda/author) route_allowed=true ;;
  /sportskeeda/college-basketball-schedule) route_allowed=true ;;
  /sportskeeda/college-basketball-schedule-options) route_allowed=true ;;
  /sportskeeda/cricket-commentary) route_allowed=true ;;
  /sportskeeda/cricket-match) route_allowed=true ;;
  /sportskeeda/depth-chart) route_allowed=true ;;
  /sportskeeda/draft-picks) route_allowed=true ;;
  /sportskeeda/draft-picks-options) route_allowed=true ;;
  /sportskeeda/event-calendar) route_allowed=true ;;
  /sportskeeda/event-calendar-options) route_allowed=true ;;
  /sportskeeda/feed) route_allowed=true ;;
  /sportskeeda/football-data) route_allowed=true ;;
  /sportskeeda/football-options) route_allowed=true ;;
  /sportskeeda/guessing-game) route_allowed=true ;;
  /sportskeeda/guessing-game-entities) route_allowed=true ;;
  /sportskeeda/guessing-games) route_allowed=true ;;
  /sportskeeda/nba-queries) route_allowed=true ;;
  /sportskeeda/news) route_allowed=true ;;
  /sportskeeda/page-data) route_allowed=true ;;
  /sportskeeda/page-options) route_allowed=true ;;
  /sportskeeda/player-stats) route_allowed=true ;;
  /sportskeeda/profile) route_allowed=true ;;
  /sportskeeda/quiz) route_allowed=true ;;
  /sportskeeda/quiz-categories) route_allowed=true ;;
  /sportskeeda/quizzes) route_allowed=true ;;
  /sportskeeda/salary-cap) route_allowed=true ;;
  /sportskeeda/schedule) route_allowed=true ;;
  /sportskeeda/sections) route_allowed=true ;;
  /sportskeeda/sitemap-items) route_allowed=true ;;
  /sportskeeda/sitemaps) route_allowed=true ;;
  /sportskeeda/standings) route_allowed=true ;;
  /sportskeeda/standings-options) route_allowed=true ;;
  /sportskeeda/taxonomy-search) route_allowed=true ;;
  /sportskeeda/topic) route_allowed=true ;;
  /sportskeeda/trade-values) route_allowed=true ;;
  /sportskeeda/transactions) route_allowed=true ;;
  /sportskeeda/transactions-options) route_allowed=true ;;
  /sportskeeda/video) route_allowed=true ;;
  /sportskeeda/videos) route_allowed=true ;;
  /sportskeeda/wiki-activity) route_allowed=true ;;
  /sportskeeda/wiki-article) route_allowed=true ;;
  /sportskeeda/wiki-categories) route_allowed=true ;;
  /sportskeeda/wiki-contributors) route_allowed=true ;;
  /sportskeeda/wiki-issues) route_allowed=true ;;
  /sportskeeda/wiki-options) route_allowed=true ;;
  /sportskeeda/wiki-pages) route_allowed=true ;;
  /sportskeeda/wiki-summary) route_allowed=true ;;
  /spotify-podcasts/categories) route_allowed=true ;;
  /spotify-podcasts/charts) route_allowed=true ;;
  /spotify-podcasts/episode) route_allowed=true ;;
  /spotify-podcasts/home) route_allowed=true ;;
  /spotify-podcasts/search) route_allowed=true ;;
  /spotify-podcasts/show) route_allowed=true ;;
  /spotify-podcasts/show/episodes) route_allowed=true ;;
  /spotify-podcasts/show/recommendations) route_allowed=true ;;
  /spotify/album) route_allowed=true ;;
  /spotify/album/tracks) route_allowed=true ;;
  /spotify/albums/search) route_allowed=true ;;
  /spotify/artist) route_allowed=true ;;
  /spotify/artist/albums) route_allowed=true ;;
  /spotify/artist/playlists) route_allowed=true ;;
  /spotify/artist/related) route_allowed=true ;;
  /spotify/artists/search) route_allowed=true ;;
  /spotify/audiobook) route_allowed=true ;;
  /spotify/audiobook/chapters) route_allowed=true ;;
  /spotify/audiobooks/search) route_allowed=true ;;
  /spotify/chapter) route_allowed=true ;;
  /spotify/episodes/search) route_allowed=true ;;
  /spotify/featured-charts-by-country) route_allowed=true ;;
  /spotify/genre) route_allowed=true ;;
  /spotify/home) route_allowed=true ;;
  /spotify/playlist) route_allowed=true ;;
  /spotify/playlists/search) route_allowed=true ;;
  /spotify/popular-by-country) route_allowed=true ;;
  /spotify/profile) route_allowed=true ;;
  /spotify/profile/followers) route_allowed=true ;;
  /spotify/profile/playlists) route_allowed=true ;;
  /spotify/profiles/search) route_allowed=true ;;
  /spotify/search) route_allowed=true ;;
  /spotify/section) route_allowed=true ;;
  /spotify/shows/search) route_allowed=true ;;
  /spotify/track) route_allowed=true ;;
  /spotify/track/recommended) route_allowed=true ;;
  /spotify/track/similar-albums) route_allowed=true ;;
  /spotify/tracks/search) route_allowed=true ;;
  /standard/article) route_allowed=true ;;
  /standard/author) route_allowed=true ;;
  /standard/headlines) route_allowed=true ;;
  /standard/news) route_allowed=true ;;
  /standard/sections) route_allowed=true ;;
  /starbucks/menu) route_allowed=true ;;
  /starbucks/nearest-store) route_allowed=true ;;
  /starbucks/stores) route_allowed=true ;;
  /startpage/suggest) route_allowed=true ;;
  /startribune/news) route_allowed=true ;;
  /steam/achievements) route_allowed=true ;;
  /steam/app) route_allowed=true ;;
  /steam/charts/concurrent) route_allowed=true ;;
  /steam/charts/most-played) route_allowed=true ;;
  /steam/charts/top-releases) route_allowed=true ;;
  /steam/community-recommendations) route_allowed=true ;;
  /steam/featured) route_allowed=true ;;
  /steam/featured-categories) route_allowed=true ;;
  /steam/items) route_allowed=true ;;
  /steam/news) route_allowed=true ;;
  /steam/package) route_allowed=true ;;
  /steam/players) route_allowed=true ;;
  /steam/reviews) route_allowed=true ;;
  /steam/reviews/histogram) route_allowed=true ;;
  /steam/search) route_allowed=true ;;
  /steam/search/results) route_allowed=true ;;
  /steam/steamspy) route_allowed=true ;;
  /steam/tags) route_allowed=true ;;
  /steam/tags/list) route_allowed=true ;;
  /steam/top-sellers) route_allowed=true ;;
  /stevemadden/collections) route_allowed=true ;;
  /stevemadden/pages) route_allowed=true ;;
  /stevemadden/products) route_allowed=true ;;
  /stevemadden/search/suggest) route_allowed=true ;;
  /stevemadden/sitemap/urls) route_allowed=true ;;
  /stevemadden/sitemaps) route_allowed=true ;;
  /stevemadden/store) route_allowed=true ;;
  /stockx/brands) route_allowed=true ;;
  /stockx/categories) route_allowed=true ;;
  /stockx/releases) route_allowed=true ;;
  /stockx/search) route_allowed=true ;;
  /straitstimes/article) route_allowed=true ;;
  /straitstimes/author) route_allowed=true ;;
  /straitstimes/headlines) route_allowed=true ;;
  /straitstimes/news) route_allowed=true ;;
  /straitstimes/sections) route_allowed=true ;;
  /strava/challenges) route_allowed=true ;;
  /strava/routes) route_allowed=true ;;
  /strava/routes/detail) route_allowed=true ;;
  /streeteasy/areas) route_allowed=true ;;
  /streeteasy/market-data/catalog) route_allowed=true ;;
  /streeteasy/market-data/indices) route_allowed=true ;;
  /streeteasy/market-data/inventory) route_allowed=true ;;
  /streeteasy/market-data/series) route_allowed=true ;;
  /streeteasy/quick-search) route_allowed=true ;;
  /streeteasy/rentals/search) route_allowed=true ;;
  /streeteasy/sales/search) route_allowed=true ;;
  /stubhub/carousel) route_allowed=true ;;
  /stubhub/categories) route_allowed=true ;;
  /stubhub/category-events) route_allowed=true ;;
  /stubhub/explore) route_allowed=true ;;
  /stubhub/navigation-categories) route_allowed=true ;;
  /stubhub/performer-events) route_allowed=true ;;
  /stubhub/search) route_allowed=true ;;
  /stubhub/suggested-searches) route_allowed=true ;;
  /stubhub/trending) route_allowed=true ;;
  /stubhub/trending-events) route_allowed=true ;;
  /stubhub/venue-events) route_allowed=true ;;
  /stuff/article) route_allowed=true ;;
  /stuff/author) route_allowed=true ;;
  /stuff/headlines) route_allowed=true ;;
  /stuff/news) route_allowed=true ;;
  /stuff/sections) route_allowed=true ;;
  /substack/categories) route_allowed=true ;;
  /substack/category) route_allowed=true ;;
  /substack/explore) route_allowed=true ;;
  /substack/leaderboard) route_allowed=true ;;
  /substack/note) route_allowed=true ;;
  /substack/note/replies) route_allowed=true ;;
  /substack/note/restacks) route_allowed=true ;;
  /substack/notes) route_allowed=true ;;
  /substack/notes/tabs) route_allowed=true ;;
  /substack/post) route_allowed=true ;;
  /substack/publication) route_allowed=true ;;
  /substack/publication/contributors) route_allowed=true ;;
  /substack/publication/posts) route_allowed=true ;;
  /substack/publication/recommendations) route_allowed=true ;;
  /substack/search) route_allowed=true ;;
  /substack/user) route_allowed=true ;;
  /substack/user/activity) route_allowed=true ;;
  /substack/user/connections) route_allowed=true ;;
  /substack/user/search) route_allowed=true ;;
  /subway/available-times) route_allowed=true ;;
  /subway/combos) route_allowed=true ;;
  /subway/menu) route_allowed=true ;;
  /subway/nearby) route_allowed=true ;;
  /subway/sitemap) route_allowed=true ;;
  /subway/store) route_allowed=true ;;
  /sun/article) route_allowed=true ;;
  /sun/author) route_allowed=true ;;
  /sun/headlines) route_allowed=true ;;
  /sun/news) route_allowed=true ;;
  /sun/sections) route_allowed=true ;;
  /swiggy/collections) route_allowed=true ;;
  /swiggy/restaurant) route_allowed=true ;;
  /swiggy/restaurant/menu) route_allowed=true ;;
  /swiggy/search) route_allowed=true ;;
  /taco-bell/app-menu) route_allowed=true ;;
  /taco-bell/categories) route_allowed=true ;;
  /taco-bell/menu) route_allowed=true ;;
  /taco-bell/nutrition) route_allowed=true ;;
  /taco-bell/product) route_allowed=true ;;
  /taco-bell/store) route_allowed=true ;;
  /taco-bell/store-menu) route_allowed=true ;;
  /taco-bell/stores) route_allowed=true ;;
  /target/categories) route_allowed=true ;;
  /target/category-products) route_allowed=true ;;
  /target/filter-options) route_allowed=true ;;
  /target/product) route_allowed=true ;;
  /target/questions) route_allowed=true ;;
  /target/reviews) route_allowed=true ;;
  /target/search) route_allowed=true ;;
  /target/stores) route_allowed=true ;;
  /techcrunch/article) route_allowed=true ;;
  /techcrunch/author) route_allowed=true ;;
  /techcrunch/headlines) route_allowed=true ;;
  /techcrunch/news) route_allowed=true ;;
  /techcrunch/sections) route_allowed=true ;;
  /techradar/article) route_allowed=true ;;
  /techradar/author) route_allowed=true ;;
  /techradar/headlines) route_allowed=true ;;
  /techradar/news) route_allowed=true ;;
  /techradar/sections) route_allowed=true ;;
  /telegraph/article) route_allowed=true ;;
  /telegraph/author) route_allowed=true ;;
  /telegraph/headlines) route_allowed=true ;;
  /telegraph/news) route_allowed=true ;;
  /telegraph/sections) route_allowed=true ;;
  /tes/jobs/detail) route_allowed=true ;;
  /tes/jobs/employer) route_allowed=true ;;
  /tes/jobs/search) route_allowed=true ;;
  /tes/resources/detail) route_allowed=true ;;
  /tes/resources/search) route_allowed=true ;;
  /tes/resources/shop) route_allowed=true ;;
  /tes/schools/search) route_allowed=true ;;
  /tesla-jobs/job) route_allowed=true ;;
  /tesla-jobs/list) route_allowed=true ;;
  /theage/article) route_allowed=true ;;
  /theage/author) route_allowed=true ;;
  /theage/headlines) route_allowed=true ;;
  /theage/news) route_allowed=true ;;
  /theage/sections) route_allowed=true ;;
  /theatlantic/article) route_allowed=true ;;
  /theatlantic/author) route_allowed=true ;;
  /theatlantic/headlines) route_allowed=true ;;
  /theatlantic/sections) route_allowed=true ;;
  /theblaze/article) route_allowed=true ;;
  /theblaze/author) route_allowed=true ;;
  /theblaze/headlines) route_allowed=true ;;
  /theblaze/news) route_allowed=true ;;
  /theblaze/sections) route_allowed=true ;;
  /thebodyshop/collections) route_allowed=true ;;
  /thebodyshop/pages) route_allowed=true ;;
  /thebodyshop/products) route_allowed=true ;;
  /thebodyshop/search/suggest) route_allowed=true ;;
  /thebodyshop/sitemap/urls) route_allowed=true ;;
  /thebodyshop/sitemaps) route_allowed=true ;;
  /thebodyshop/store) route_allowed=true ;;
  /thedailybeast/article) route_allowed=true ;;
  /thedailybeast/author) route_allowed=true ;;
  /thedailybeast/headlines) route_allowed=true ;;
  /thedailybeast/news) route_allowed=true ;;
  /thedailybeast/sections) route_allowed=true ;;
  /thehill/article) route_allowed=true ;;
  /thehill/author) route_allowed=true ;;
  /thehill/headlines) route_allowed=true ;;
  /thehill/news) route_allowed=true ;;
  /thehill/sections) route_allowed=true ;;
  /thehindu/article) route_allowed=true ;;
  /thehindu/author) route_allowed=true ;;
  /thehindu/headlines) route_allowed=true ;;
  /thehindu/news) route_allowed=true ;;
  /thehindu/sections) route_allowed=true ;;
  /thejournal/article) route_allowed=true ;;
  /thejournal/author) route_allowed=true ;;
  /thejournal/headlines) route_allowed=true ;;
  /thejournal/news) route_allowed=true ;;
  /thejournal/sections) route_allowed=true ;;
  /thenextweb/article) route_allowed=true ;;
  /thenextweb/author) route_allowed=true ;;
  /thenextweb/headlines) route_allowed=true ;;
  /thenextweb/news) route_allowed=true ;;
  /thenextweb/sections) route_allowed=true ;;
  /therealreal/autocomplete) route_allowed=true ;;
  /therealreal/categories) route_allowed=true ;;
  /therealreal/category) route_allowed=true ;;
  /therealreal/collection) route_allowed=true ;;
  /therealreal/collections) route_allowed=true ;;
  /therealreal/conditions) route_allowed=true ;;
  /therealreal/designer) route_allowed=true ;;
  /therealreal/designers) route_allowed=true ;;
  /therealreal/listing) route_allowed=true ;;
  /therealreal/search) route_allowed=true ;;
  /therealreal/similar) route_allowed=true ;;
  /thestarmy/article) route_allowed=true ;;
  /thestarmy/author) route_allowed=true ;;
  /thestarmy/headlines) route_allowed=true ;;
  /thestarmy/news) route_allowed=true ;;
  /thestarmy/sections) route_allowed=true ;;
  /theverge/article) route_allowed=true ;;
  /theverge/author) route_allowed=true ;;
  /theverge/headlines) route_allowed=true ;;
  /theverge/news) route_allowed=true ;;
  /theverge/sections) route_allowed=true ;;
  /thisismoney/article) route_allowed=true ;;
  /thisismoney/author) route_allowed=true ;;
  /thisismoney/headlines) route_allowed=true ;;
  /thisismoney/news) route_allowed=true ;;
  /thisismoney/sections) route_allowed=true ;;
  /threads/search) route_allowed=true ;;
  /threads/search/topics) route_allowed=true ;;
  /ticketmaster/attraction) route_allowed=true ;;
  /ticketmaster/attraction-events) route_allowed=true ;;
  /ticketmaster/attraction-related) route_allowed=true ;;
  /ticketmaster/attraction-reviews) route_allowed=true ;;
  /ticketmaster/discover-categories) route_allowed=true ;;
  /ticketmaster/discover-category-events) route_allowed=true ;;
  /ticketmaster/discover-cities) route_allowed=true ;;
  /ticketmaster/discover-city-events) route_allowed=true ;;
  /ticketmaster/event) route_allowed=true ;;
  /ticketmaster/search-events) route_allowed=true ;;
  /ticketmaster/suggest) route_allowed=true ;;
  /ticketmaster/trending-attractions) route_allowed=true ;;
  /ticketmaster/venue) route_allowed=true ;;
  /ticketmaster/venue-enhanced-details) route_allowed=true ;;
  /ticketmaster/venue-events) route_allowed=true ;;
  /ticketweb/event) route_allowed=true ;;
  /ticketweb/search) route_allowed=true ;;
  /ticketweb/venue) route_allowed=true ;;
  /tiffany/categories) route_allowed=true ;;
  /tiffany/category) route_allowed=true ;;
  /tiffany/content-search) route_allowed=true ;;
  /tiffany/filters) route_allowed=true ;;
  /tiffany/product) route_allowed=true ;;
  /tiffany/search) route_allowed=true ;;
  /tiffany/stores) route_allowed=true ;;
  /tiffany/suggest) route_allowed=true ;;
  /tiktok/category) route_allowed=true ;;
  /tiktok/comments) route_allowed=true ;;
  /tiktok/creative-center/filters) route_allowed=true ;;
  /tiktok/creative-center/hashtags) route_allowed=true ;;
  /tiktok/creative-center/top-content) route_allowed=true ;;
  /tiktok/creative-center/videos) route_allowed=true ;;
  /tiktok/hashtags) route_allowed=true ;;
  /tiktok/mobile/feed) route_allowed=true ;;
  /tiktok/mobile/hashtag) route_allowed=true ;;
  /tiktok/mobile/hashtag/posts) route_allowed=true ;;
  /tiktok/mobile/hashtags) route_allowed=true ;;
  /tiktok/mobile/live/effects) route_allowed=true ;;
  /tiktok/mobile/live/gifts) route_allowed=true ;;
  /tiktok/mobile/live/search) route_allowed=true ;;
  /tiktok/mobile/music/beats) route_allowed=true ;;
  /tiktok/mobile/music/collections) route_allowed=true ;;
  /tiktok/mobile/music/pick) route_allowed=true ;;
  /tiktok/mobile/music/posts) route_allowed=true ;;
  /tiktok/mobile/music/related) route_allowed=true ;;
  /tiktok/mobile/music/trending) route_allowed=true ;;
  /tiktok/mobile/search) route_allowed=true ;;
  /tiktok/mobile/search/music) route_allowed=true ;;
  /tiktok/mobile/search/user) route_allowed=true ;;
  /tiktok/mobile/trending/categories) route_allowed=true ;;
  /tiktok/mobile/trending/effects) route_allowed=true ;;
  /tiktok/popular-trend/country-industry-meta) route_allowed=true ;;
  /tiktok/posts) route_allowed=true ;;
  /tiktok/search) route_allowed=true ;;
  /tiktok/search/hashtag) route_allowed=true ;;
  /tiktok/search/user) route_allowed=true ;;
  /tiktok/top-ads/analysis) route_allowed=true ;;
  /tiktok/top-ads/detail) route_allowed=true ;;
  /tiktok/top-ads/filters) route_allowed=true ;;
  /tiktok/top-ads/list) route_allowed=true ;;
  /tiktok/top-ads/location-info) route_allowed=true ;;
  /tiktok/top-ads/locations) route_allowed=true ;;
  /tiktok/top-ads/recommend) route_allowed=true ;;
  /tiktok/top-ads/safety) route_allowed=true ;;
  /tiktok/top-ads/spotlight) route_allowed=true ;;
  /tiktok/top-ads/suggestions) route_allowed=true ;;
  /tiktok/trending) route_allowed=true ;;
  /time/article) route_allowed=true ;;
  /time/author) route_allowed=true ;;
  /time/headlines) route_allowed=true ;;
  /time/news) route_allowed=true ;;
  /time/sections) route_allowed=true ;;
  /timeslive/article) route_allowed=true ;;
  /timeslive/headlines) route_allowed=true ;;
  /timeslive/news) route_allowed=true ;;
  /timeslive/sections) route_allowed=true ;;
  /timesofindia/article) route_allowed=true ;;
  /timesofindia/author) route_allowed=true ;;
  /timesofindia/headlines) route_allowed=true ;;
  /timesofindia/news) route_allowed=true ;;
  /timesofindia/sections) route_allowed=true ;;
  /timesofisrael/article) route_allowed=true ;;
  /timesofisrael/author) route_allowed=true ;;
  /timesofisrael/headlines) route_allowed=true ;;
  /timesofisrael/news) route_allowed=true ;;
  /timesofisrael/sections) route_allowed=true ;;
  /tmdb/genres) route_allowed=true ;;
  /tmdb/movie/list) route_allowed=true ;;
  /tmdb/person/list) route_allowed=true ;;
  /tmdb/search) route_allowed=true ;;
  /tmdb/tv/list) route_allowed=true ;;
  /tmz/article) route_allowed=true ;;
  /tmz/author) route_allowed=true ;;
  /tmz/headlines) route_allowed=true ;;
  /tmz/news) route_allowed=true ;;
  /tmz/sections) route_allowed=true ;;
  /tokopedia/autocomplete) route_allowed=true ;;
  /tokopedia/category) route_allowed=true ;;
  /tokopedia/home) route_allowed=true ;;
  /tokopedia/home/tabs) route_allowed=true ;;
  /tokopedia/product) route_allowed=true ;;
  /tokopedia/product/review-filters) route_allowed=true ;;
  /tokopedia/search) route_allowed=true ;;
  /tokopedia/search/filters) route_allowed=true ;;
  /tomsguide/article) route_allowed=true ;;
  /tomsguide/author) route_allowed=true ;;
  /tomsguide/headlines) route_allowed=true ;;
  /tomsguide/news) route_allowed=true ;;
  /tomsguide/sections) route_allowed=true ;;
  /tomshardware/article) route_allowed=true ;;
  /tomshardware/author) route_allowed=true ;;
  /tomshardware/headlines) route_allowed=true ;;
  /tomshardware/news) route_allowed=true ;;
  /tomshardware/sections) route_allowed=true ;;
  /torontostar/article) route_allowed=true ;;
  /torontostar/author) route_allowed=true ;;
  /torontostar/headlines) route_allowed=true ;;
  /torontostar/news) route_allowed=true ;;
  /torontostar/sections) route_allowed=true ;;
  /townhall/article) route_allowed=true ;;
  /townhall/author) route_allowed=true ;;
  /townhall/headlines) route_allowed=true ;;
  /townhall/news) route_allowed=true ;;
  /townhall/sections) route_allowed=true ;;
  /tripadvisor/autocomplete) route_allowed=true ;;
  /tripadvisor/enums) route_allowed=true ;;
  /tripadvisor/hotels) route_allowed=true ;;
  /tripadvisor/place) route_allowed=true ;;
  /tripadvisor/reviews) route_allowed=true ;;
  /tripadvisor/search) route_allowed=true ;;
  /tripcom/hotels/search) route_allowed=true ;;
  /trustmrr/acquire) route_allowed=true ;;
  /trustmrr/categories) route_allowed=true ;;
  /trustmrr/leaderboard) route_allowed=true ;;
  /trustmrr/marketplace) route_allowed=true ;;
  /trustmrr/startups) route_allowed=true ;;
  /trustpilot/business-units/search) route_allowed=true ;;
  /trustpilot/categories) route_allowed=true ;;
  /trustpilot/categories/search) route_allowed=true ;;
  /twitch/channel) route_allowed=true ;;
  /twitch/clips) route_allowed=true ;;
  /twitch/schedule) route_allowed=true ;;
  /twitch/search) route_allowed=true ;;
  /twitch/streams) route_allowed=true ;;
  /twitch/team) route_allowed=true ;;
  /twitch/top-games) route_allowed=true ;;
  /twitch/videos) route_allowed=true ;;
  /twitch/vod-comments) route_allowed=true ;;
  /ubereats/feed) route_allowed=true ;;
  /ubereats/search) route_allowed=true ;;
  /ulta/categories) route_allowed=true ;;
  /ulta/category) route_allowed=true ;;
  /ulta/product/questions) route_allowed=true ;;
  /ulta/product/reviews) route_allowed=true ;;
  /ulta/search) route_allowed=true ;;
  /ulta/stores) route_allowed=true ;;
  /ulta/suggest) route_allowed=true ;;
  /upwork/search) route_allowed=true ;;
  /usatoday/article) route_allowed=true ;;
  /usatoday/author) route_allowed=true ;;
  /usatoday/headlines) route_allowed=true ;;
  /usatoday/news) route_allowed=true ;;
  /usatoday/sections) route_allowed=true ;;
  /usmagazine/article) route_allowed=true ;;
  /usmagazine/author) route_allowed=true ;;
  /usmagazine/headlines) route_allowed=true ;;
  /usmagazine/news) route_allowed=true ;;
  /usmagazine/sections) route_allowed=true ;;
  /usptoppubs/detail) route_allowed=true ;;
  /usptoppubs/search) route_allowed=true ;;
  /vanguardng/article) route_allowed=true ;;
  /vanguardng/author) route_allowed=true ;;
  /vanguardng/headlines) route_allowed=true ;;
  /vanguardng/news) route_allowed=true ;;
  /vanguardng/sections) route_allowed=true ;;
  /vanityfair/article) route_allowed=true ;;
  /vanityfair/author) route_allowed=true ;;
  /vanityfair/headlines) route_allowed=true ;;
  /vanityfair/news) route_allowed=true ;;
  /vanityfair/sections) route_allowed=true ;;
  /variety/article) route_allowed=true ;;
  /variety/author) route_allowed=true ;;
  /variety/headlines) route_allowed=true ;;
  /variety/news) route_allowed=true ;;
  /variety/sections) route_allowed=true ;;
  /vestiaire/brands) route_allowed=true ;;
  /vestiaire/categories) route_allowed=true ;;
  /vestiaire/conditions) route_allowed=true ;;
  /vestiaire/product) route_allowed=true ;;
  /vestiaire/search) route_allowed=true ;;
  /vestiaire/search-sellers) route_allowed=true ;;
  /vestiaire/seller) route_allowed=true ;;
  /vestiaire/suggest) route_allowed=true ;;
  /vice/article) route_allowed=true ;;
  /vice/author) route_allowed=true ;;
  /vice/headlines) route_allowed=true ;;
  /vice/news) route_allowed=true ;;
  /vice/sections) route_allowed=true ;;
  /vinted/brand) route_allowed=true ;;
  /vinted/brands) route_allowed=true ;;
  /vinted/catalog) route_allowed=true ;;
  /vinted/categories) route_allowed=true ;;
  /vinted/category) route_allowed=true ;;
  /vinted/item) route_allowed=true ;;
  /vinted/member) route_allowed=true ;;
  /vox/article) route_allowed=true ;;
  /vox/author) route_allowed=true ;;
  /vox/headlines) route_allowed=true ;;
  /vox/news) route_allowed=true ;;
  /vox/sections) route_allowed=true ;;
  /vrbo/locations/search) route_allowed=true ;;
  /vrbo/search) route_allowed=true ;;
  /vrbo/travel-pages) route_allowed=true ;;
  /walesonline/article) route_allowed=true ;;
  /walesonline/author) route_allowed=true ;;
  /walesonline/headlines) route_allowed=true ;;
  /walesonline/news) route_allowed=true ;;
  /walesonline/sections) route_allowed=true ;;
  /walgreens/stores) route_allowed=true ;;
  /walmart/search) route_allowed=true ;;
  /wapo/article) route_allowed=true ;;
  /wapo/author) route_allowed=true ;;
  /wapo/headlines) route_allowed=true ;;
  /wapo/news) route_allowed=true ;;
  /wapo/sections) route_allowed=true ;;
  /wayfair/categories) route_allowed=true ;;
  /wayfair/category) route_allowed=true ;;
  /wccftech/article) route_allowed=true ;;
  /wccftech/author) route_allowed=true ;;
  /wccftech/headlines) route_allowed=true ;;
  /wccftech/news) route_allowed=true ;;
  /wccftech/sections) route_allowed=true ;;
  /web/capabilities) route_allowed=true ;;
  /web/crawl) route_allowed=true ;;
  /web/map) route_allowed=true ;;
  /web/search) route_allowed=true ;;
  /wendys/categories) route_allowed=true ;;
  /wendys/directory) route_allowed=true ;;
  /wendys/item) route_allowed=true ;;
  /wendys/menu) route_allowed=true ;;
  /wendys/nearby) route_allowed=true ;;
  /wendys/nutrition) route_allowed=true ;;
  /wendys/restaurant) route_allowed=true ;;
  /wendys/store) route_allowed=true ;;
  /wendys/store-menu) route_allowed=true ;;
  /wendys/time-slots) route_allowed=true ;;
  /whataburger/sitemap) route_allowed=true ;;
  /whataburger/store) route_allowed=true ;;
  /whatnot/browse) route_allowed=true ;;
  /whatnot/categories) route_allowed=true ;;
  /wingstop/delivery-store) route_allowed=true ;;
  /wingstop/directory) route_allowed=true ;;
  /wingstop/flavors) route_allowed=true ;;
  /wingstop/menu) route_allowed=true ;;
  /wingstop/nearby) route_allowed=true ;;
  /wingstop/store) route_allowed=true ;;
  /wired/article) route_allowed=true ;;
  /wired/author) route_allowed=true ;;
  /wired/headlines) route_allowed=true ;;
  /wired/news) route_allowed=true ;;
  /wired/sections) route_allowed=true ;;
  /wish/categories) route_allowed=true ;;
  /wish/search) route_allowed=true ;;
  /wish/suggest) route_allowed=true ;;
  /wolt/cities) route_allowed=true ;;
  /wolt/collections) route_allowed=true ;;
  /wolt/restaurant) route_allowed=true ;;
  /wolt/restaurant/availability) route_allowed=true ;;
  /wolt/restaurant/menu) route_allowed=true ;;
  /wolt/restaurant/menu/search) route_allowed=true ;;
  /wolt/search) route_allowed=true ;;
  /wolt/search/filters) route_allowed=true ;;
  /wsj/article) route_allowed=true ;;
  /wsj/author) route_allowed=true ;;
  /xbox/browse) route_allowed=true ;;
  /xbox/collection) route_allowed=true ;;
  /xbox/game) route_allowed=true ;;
  /xbox/reviews) route_allowed=true ;;
  /xbox/search) route_allowed=true ;;
  /xda/article) route_allowed=true ;;
  /xda/author) route_allowed=true ;;
  /xda/headlines) route_allowed=true ;;
  /xda/news) route_allowed=true ;;
  /xda/sections) route_allowed=true ;;
  /yahoo-autos/article) route_allowed=true ;;
  /yahoo-autos/category) route_allowed=true ;;
  /yahoo-autos/home) route_allowed=true ;;
  /yahoo-entertainment/article) route_allowed=true ;;
  /yahoo-entertainment/category) route_allowed=true ;;
  /yahoo-entertainment/home) route_allowed=true ;;
  /yahoo-finance/calendars) route_allowed=true ;;
  /yahoo-finance/download) route_allowed=true ;;
  /yahoo-finance/industries) route_allowed=true ;;
  /yahoo-finance/lookup) route_allowed=true ;;
  /yahoo-finance/screener) route_allowed=true ;;
  /yahoo-finance/screeners) route_allowed=true ;;
  /yahoo-finance/search) route_allowed=true ;;
  /yahoo-finance/sectors) route_allowed=true ;;
  /yahoo-health/article) route_allowed=true ;;
  /yahoo-health/category) route_allowed=true ;;
  /yahoo-health/home) route_allowed=true ;;
  /yahoo-life/article) route_allowed=true ;;
  /yahoo-life/home) route_allowed=true ;;
  /yahoo-news/article) route_allowed=true ;;
  /yahoo-news/category) route_allowed=true ;;
  /yahoo-news/comments) route_allowed=true ;;
  /yahoo-news/comments/replies) route_allowed=true ;;
  /yahoo-news/home) route_allowed=true ;;
  /yahoo-news/related) route_allowed=true ;;
  /yahoo-news/suggest) route_allowed=true ;;
  /yahoo-search/images) route_allowed=true ;;
  /yahoo-search/local) route_allowed=true ;;
  /yahoo-search/news) route_allowed=true ;;
  /yahoo-search/search) route_allowed=true ;;
  /yahoo-search/suggest) route_allowed=true ;;
  /yahoo-search/videos) route_allowed=true ;;
  /yahoo-shopping/article) route_allowed=true ;;
  /yahoo-shopping/category) route_allowed=true ;;
  /yahoo-shopping/home) route_allowed=true ;;
  /yahoo-shopping/shopping-list) route_allowed=true ;;
  /yahoo-shopping/shopping-lists) route_allowed=true ;;
  /yahoo-shopping/store) route_allowed=true ;;
  /yahoo-shopping/stores) route_allowed=true ;;
  /yahoo-sports/game) route_allowed=true ;;
  /yahoo-sports/golf-leaderboard) route_allowed=true ;;
  /yahoo-sports/golf-schedule) route_allowed=true ;;
  /yahoo-sports/mma-fight-card) route_allowed=true ;;
  /yahoo-sports/mma-schedule) route_allowed=true ;;
  /yahoo-sports/motorsports-race) route_allowed=true ;;
  /yahoo-sports/motorsports-schedule) route_allowed=true ;;
  /yahoo-sports/news) route_allowed=true ;;
  /yahoo-sports/olympics-medals) route_allowed=true ;;
  /yahoo-sports/player) route_allowed=true ;;
  /yahoo-sports/scoreboard) route_allowed=true ;;
  /yahoo-sports/standings) route_allowed=true ;;
  /yahoo-sports/team) route_allowed=true ;;
  /yahoo-sports/team-roster) route_allowed=true ;;
  /yahoo-sports/team-schedule) route_allowed=true ;;
  /yahoo-sports/tennis-rankings) route_allowed=true ;;
  /yahoo-sports/tennis-schedule) route_allowed=true ;;
  /yahoo-sports/tennis-scoreboard) route_allowed=true ;;
  /yahoo-tech/article) route_allowed=true ;;
  /yahoo-tech/category) route_allowed=true ;;
  /yahoo-tech/home) route_allowed=true ;;
  /yandex/search) route_allowed=true ;;
  /yandex/suggest) route_allowed=true ;;
  /yardbarker/article) route_allowed=true ;;
  /yardbarker/author) route_allowed=true ;;
  /yardbarker/headlines) route_allowed=true ;;
  /yardbarker/news) route_allowed=true ;;
  /yardbarker/sections) route_allowed=true ;;
  /yelp/geocode) route_allowed=true ;;
  /yelp/search) route_allowed=true ;;
  /yoox/categories) route_allowed=true ;;
  /yoox/designers) route_allowed=true ;;
  /yoox/product) route_allowed=true ;;
  /yoox/search) route_allowed=true ;;
  /youtube/search) route_allowed=true ;;
  /youtube/suggest) route_allowed=true ;;
  /zalando/categories) route_allowed=true ;;
  /zalando/category) route_allowed=true ;;
  /zalando/markets) route_allowed=true ;;
  /zalando/product) route_allowed=true ;;
  /zalando/search) route_allowed=true ;;
  /zalando/suggest) route_allowed=true ;;
  /zappos/brand) route_allowed=true ;;
  /zappos/brands) route_allowed=true ;;
  /zappos/search) route_allowed=true ;;
  /zappos/suggest) route_allowed=true ;;
  /zara/categories) route_allowed=true ;;
  /zara/search) route_allowed=true ;;
  /zara/stores) route_allowed=true ;;
  /zara/suggest) route_allowed=true ;;
  /zaxbys/menu) route_allowed=true ;;
  /zaxbys/nearby) route_allowed=true ;;
  /zaxbys/store) route_allowed=true ;;
  /zdnet/article) route_allowed=true ;;
  /zdnet/author) route_allowed=true ;;
  /zdnet/headlines) route_allowed=true ;;
  /zdnet/news) route_allowed=true ;;
  /zdnet/sections) route_allowed=true ;;
  /zillow/autocomplete) route_allowed=true ;;
  /zillow/search) route_allowed=true ;;
  /zomato/cities) route_allowed=true ;;
  /zomato/collection) route_allowed=true ;;
  /zomato/collections) route_allowed=true ;;
  /zomato/restaurant) route_allowed=true ;;
  /zomato/restaurant/menu) route_allowed=true ;;
  /zomato/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/agoda/activities/[^/]+$'
  '^/agoda/hotels/[^/]+$'
  '^/airbnb/host/[^/]+$'
  '^/airbnb/host/[^/]+/listings$'
  '^/airbnb/host/[^/]+/reviews$'
  '^/airbnb/room/[^/]+$'
  '^/airbnb/room/[^/]+/calendar$'
  '^/airbnb/room/[^/]+/reviews$'
  '^/allbirds/collections/[^/]+/products$'
  '^/allbirds/pages/[^/]+$'
  '^/allbirds/products/[^/]+$'
  '^/allbirds/products/[^/]+/recommendations$'
  '^/amazon/product/[^/]+$'
  '^/amazon/suggest/[^/]+$'
  '^/anime/character/[^/]+$'
  '^/anime/title/[^/]+$'
  '^/anime/title/[^/]+/characters$'
  '^/anime/title/[^/]+/recommendations$'
  '^/anime/title/[^/]+/staff$'
  '^/apple-books/audiobook-series/[^/]+$'
  '^/apple-books/audiobook/[^/]+$'
  '^/apple-books/audiobook/[^/]+/reviews$'
  '^/apple-books/audiobook/[^/]+/similar$'
  '^/apple-books/author/[^/]+$'
  '^/apple-books/book/[^/]+$'
  '^/apple-books/book/[^/]+/reviews$'
  '^/apple-books/book/[^/]+/similar$'
  '^/apple-books/series/[^/]+$'
  '^/apple-podcasts/show/[^/]+$'
  '^/apple-podcasts/show/[^/]+/episodes$'
  '^/apple-podcasts/show/[^/]+/related$'
  '^/appstore/developer/[^/]+$'
  '^/appstore/privacy/[^/]+$'
  '^/appstore/suggest/[^/]+$'
  '^/appstore/version-history/[^/]+$'
  '^/audible/category/[^/]+$'
  '^/audible/list/[^/]+$'
  '^/audible/product/[^/]+$'
  '^/audible/product/[^/]+/related$'
  '^/audible/product/[^/]+/reviews$'
  '^/audible/series/[^/]+$'
  '^/autotrader/dealer/[^/]+$'
  '^/autotrader/vehicle/[^/]+$'
  '^/bbb/scamtracker/[^/]+$'
  '^/bonhams/auctions/[^/]+$'
  '^/bonhams/auctions/[^/]+/lots$'
  '^/bonhams/lots/[^/]+/[^/]+$'
  '^/brooklinen/collections/[^/]+/products$'
  '^/brooklinen/pages/[^/]+$'
  '^/brooklinen/products/[^/]+$'
  '^/brooklinen/products/[^/]+/recommendations$'
  '^/carmax/store/[^/]+$'
  '^/carmax/vehicle/[^/]+$'
  '^/carmax/vehicle/[^/]+/recommendations$'
  '^/carsdotcom/vehicle/[^/]+$'
  '^/coingecko/category/[^/]+/coins$'
  '^/coingecko/chains/[^/]+$'
  '^/coingecko/coin/[^/]+$'
  '^/coingecko/coin/[^/]+/analysis$'
  '^/coingecko/exchange/[^/]+$'
  '^/coingecko/nft/category/[^/]+$'
  '^/colehaan/collections/[^/]+/products$'
  '^/colehaan/pages/[^/]+$'
  '^/colehaan/products/[^/]+$'
  '^/colehaan/products/[^/]+/recommendations$'
  '^/costco/product/[^/]+$'
  '^/costco/product/[^/]+/availability$'
  '^/costco/product/[^/]+/reviews$'
  '^/cvs/product-ingredients/[^/]+$'
  '^/cvs/product/[^/]+$'
  '^/depop/item/[^/]+$'
  '^/depop/item/[^/]+/similar$'
  '^/depop/shop/[^/]+$'
  '^/discogs/artist/[^/]+$'
  '^/discogs/artist/[^/]+/releases$'
  '^/discogs/label/[^/]+$'
  '^/discogs/label/[^/]+/releases$'
  '^/discogs/master/[^/]+$'
  '^/discogs/release/[^/]+$'
  '^/doordash/store/[^/]+$'
  '^/doordash/store/[^/]+/fulfillment$'
  '^/doordash/store/[^/]+/info$'
  '^/doordash/store/[^/]+/item/[^/]+$'
  '^/doordash/store/[^/]+/menu$'
  '^/doordash/store/[^/]+/reviews$'
  '^/ebay/item/[^/]+$'
  '^/ebay/live/streams/[^/]+$'
  '^/ebay/live/streams/[^/]+/items$'
  '^/ebay/seller/[^/]+$'
  '^/ebay/seller/[^/]+/about$'
  '^/ebay/seller/[^/]+/feedback$'
  '^/ebay/seller/[^/]+/shop$'
  '^/etsy/listing/[^/]+$'
  '^/etsy/listing/[^/]+/reviews$'
  '^/etsy/shop/[^/]+$'
  '^/etsy/shop/[^/]+/listings$'
  '^/etsy/shop/[^/]+/reviews$'
  '^/everlane/collections/[^/]+/products$'
  '^/everlane/pages/[^/]+$'
  '^/everlane/products/[^/]+$'
  '^/everlane/products/[^/]+/recommendations$'
  '^/facebook/[^/]+$'
  '^/fanaticscollect/listing/[^/]+$'
  '^/fanaticslive/channel/[^/]+$'
  '^/fanaticslive/shop/[^/]+$'
  '^/fanaticslive/shop/[^/]+/shows$'
  '^/fanaticslive/show/[^/]+$'
  '^/fanaticslive/show/[^/]+/instant-rips$'
  '^/fashionnova/collections/[^/]+/products$'
  '^/fashionnova/pages/[^/]+$'
  '^/fashionnova/products/[^/]+$'
  '^/fashionnova/products/[^/]+/recommendations$'
  '^/fashionphile/collections/[^/]+/products$'
  '^/fashionphile/pages/[^/]+$'
  '^/fashionphile/products/[^/]+$'
  '^/fashionphile/products/[^/]+/recommendations$'
  '^/fiverr/gig/[^/]+/[^/]+$'
  '^/fiverr/seller/[^/]+$'
  '^/github/org/[^/]+$'
  '^/github/org/[^/]+/repos$'
  '^/github/repo/[^/]+/[^/]+$'
  '^/github/repo/[^/]+/[^/]+/contributors$'
  '^/github/repo/[^/]+/[^/]+/forks$'
  '^/github/repo/[^/]+/[^/]+/languages$'
  '^/github/repo/[^/]+/[^/]+/releases$'
  '^/github/user/[^/]+$'
  '^/github/user/[^/]+/events$'
  '^/github/user/[^/]+/followers$'
  '^/github/user/[^/]+/following$'
  '^/github/user/[^/]+/pinned$'
  '^/github/user/[^/]+/repos$'
  '^/goat/product/[^/]+$'
  '^/goat/product/[^/]+/recommended$'
  '^/goodreads/author/[^/]+$'
  '^/goodreads/author/[^/]+/books$'
  '^/goodreads/author/[^/]+/quotes$'
  '^/goodreads/book/[^/]+$'
  '^/goodreads/book/[^/]+/editions$'
  '^/goodreads/book/[^/]+/reviews$'
  '^/goodreads/genre/[^/]+$'
  '^/goodreads/list/[^/]+$'
  '^/google/finance/analyst-articles/[^/]+$'
  '^/google/finance/chart/[^/]+$'
  '^/google/finance/classification/[^/]+$'
  '^/google/finance/company/[^/]+$'
  '^/google/finance/financials/[^/]+$'
  '^/google/finance/markets/categories/[^/]+/news$'
  '^/google/finance/markets/categories/[^/]+/stocks$'
  '^/google/finance/news/[^/]+$'
  '^/google/finance/quote/[^/]+$'
  '^/google/finance/related/[^/]+$'
  '^/google/finance/ticker/[^/]+$'
  '^/google/map/place/[^/]+$'
  '^/google/map/place/[^/]+/photos$'
  '^/google/map/place/[^/]+/reviews$'
  '^/googleplay/developer/[^/]+$'
  '^/googleplay/suggest/[^/]+$'
  '^/greystar/articles/[^/]+/[^/]+$'
  '^/greystar/newsroom/[^/]+$'
  '^/greystar/properties/[^/]+$'
  '^/gymshark/collections/[^/]+/products$'
  '^/gymshark/pages/[^/]+$'
  '^/gymshark/products/[^/]+$'
  '^/gymshark/products/[^/]+/recommendations$'
  '^/hm/product/[^/]+$'
  '^/hm/product/[^/]+/related$'
  '^/homedepot/product/[^/]+$'
  '^/homedepot/product/[^/]+/questions$'
  '^/instagram/post/[^/]+/[^/]+$'
  '^/instagram/profile/[^/]+$'
  '^/instagram/reels/[^/]+$'
  '^/kalshi/event/[^/]+$'
  '^/kalshi/event/[^/]+/history$'
  '^/kalshi/event/[^/]+/metadata$'
  '^/kalshi/historical/market/[^/]+$'
  '^/kalshi/historical/market/[^/]+/history$'
  '^/kalshi/market/[^/]+$'
  '^/kalshi/market/[^/]+/history$'
  '^/kalshi/market/[^/]+/orderbook$'
  '^/kalshi/series/[^/]+$'
  '^/kyliecosmetics/collections/[^/]+/products$'
  '^/kyliecosmetics/pages/[^/]+$'
  '^/kyliecosmetics/products/[^/]+$'
  '^/kyliecosmetics/products/[^/]+/recommendations$'
  '^/letterboxd/film/[^/]+$'
  '^/letterboxd/film/[^/]+/rating-histogram$'
  '^/letterboxd/film/[^/]+/reviews$'
  '^/letterboxd/film/[^/]+/similar$'
  '^/letterboxd/member/[^/]+$'
  '^/letterboxd/person/[^/]+$'
  '^/linkedin/company/[^/]+$'
  '^/linkedin/product/[^/]+$'
  '^/linkedin/showcase/[^/]+$'
  '^/lululemon/product/[^/]+$'
  '^/macys/product/[^/]+$'
  '^/manga/title/[^/]+$'
  '^/manga/title/[^/]+/characters$'
  '^/manga/title/[^/]+/recommendations$'
  '^/manga/title/[^/]+/staff$'
  '^/mercari/item/[^/]+$'
  '^/metacritic/game/[^/]+$'
  '^/metacritic/game/[^/]+/critic-reviews$'
  '^/metacritic/game/[^/]+/user-reviews$'
  '^/metacritic/movie/[^/]+$'
  '^/metacritic/movie/[^/]+/critic-reviews$'
  '^/metacritic/movie/[^/]+/user-reviews$'
  '^/metacritic/tv/[^/]+$'
  '^/metacritic/tv/[^/]+/critic-reviews$'
  '^/metacritic/tv/[^/]+/user-reviews$'
  '^/metaculus/category/[^/]+/questions$'
  '^/metaculus/project/[^/]+/questions$'
  '^/metaculus/question/[^/]+$'
  '^/metaculus/question/[^/]+/forecast-history$'
  '^/metaculus/question/[^/]+/forecasts$'
  '^/metaculus/question/[^/]+/metadata$'
  '^/metaculus/question/[^/]+/options$'
  '^/metaculus/tournament/[^/]+/questions$'
  '^/numbeo/cost-of-living/city/[^/]+$'
  '^/numbeo/indices/city/[^/]+$'
  '^/ohpolly/collections/[^/]+/products$'
  '^/ohpolly/pages/[^/]+$'
  '^/ohpolly/products/[^/]+$'
  '^/ohpolly/products/[^/]+/recommendations$'
  '^/opensea/collection/[^/]+$'
  '^/opensea/collection/[^/]+/activity$'
  '^/opensea/collection/[^/]+/best-deals$'
  '^/opensea/collection/[^/]+/chart$'
  '^/opensea/collection/[^/]+/depth$'
  '^/opensea/collection/[^/]+/holders$'
  '^/opensea/collection/[^/]+/items$'
  '^/opensea/collection/[^/]+/offers$'
  '^/opensea/collection/[^/]+/rarest-items$'
  '^/opensea/collection/[^/]+/search-items$'
  '^/opensea/collection/[^/]+/social-proof$'
  '^/opensea/collection/[^/]+/top-sales$'
  '^/opensea/collection/[^/]+/trait-offers$'
  '^/opensea/collection/[^/]+/traits$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/activity$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/chart$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/depth$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/listings$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/offers$'
  '^/opensea/item/[^/]+/[^/]+/[^/]+/owners$'
  '^/opensea/profile/[^/]+$'
  '^/opensea/profile/[^/]+/activity$'
  '^/opensea/profile/[^/]+/collections$'
  '^/opensea/profile/[^/]+/created$'
  '^/opensea/profile/[^/]+/items$'
  '^/opensea/profile/[^/]+/search-items$'
  '^/pinterest/board/[^/]+/[^/]+$'
  '^/pinterest/ideas/[^/]+$'
  '^/pinterest/pin/[^/]+$'
  '^/pinterest/user/[^/]+$'
  '^/pinterest/user/[^/]+/boards$'
  '^/pinterest/user/[^/]+/pins$'
  '^/polymarket/clob/market/[^/]+$'
  '^/polymarket/event/[^/]+$'
  '^/polymarket/events/[^/]+/tags$'
  '^/polymarket/market/[^/]+$'
  '^/polymarket/market/[^/]+/liquidity$'
  '^/polymarket/market/[^/]+/tags$'
  '^/polymarket/rewards/market/[^/]+$'
  '^/polymarket/tag/[^/]+$'
  '^/polymarket/tag/[^/]+/related-tags$'
  '^/polymarket/token/[^/]+/midpoint$'
  '^/polymarket/token/[^/]+/orderbook$'
  '^/polymarket/token/[^/]+/price$'
  '^/polymarket/token/[^/]+/price-history$'
  '^/polymarket/token/[^/]+/spread$'
  '^/poshmark/brand/[^/]+$'
  '^/poshmark/category/[^/]+$'
  '^/poshmark/closet/[^/]+$'
  '^/poshmark/listing/[^/]+$'
  '^/poshmark/trend/[^/]+$'
  '^/pristine-auction/lot/[^/]+$'
  '^/pristine-marketplace/collections/[^/]+/products$'
  '^/pristine-marketplace/pages/[^/]+$'
  '^/pristine-marketplace/products/[^/]+$'
  '^/pristine-marketplace/products/[^/]+/recommendations$'
  '^/producthunt/category/[^/]+$'
  '^/producthunt/category/[^/]+/products$'
  '^/producthunt/product/[^/]+$'
  '^/producthunt/product/[^/]+/about$'
  '^/producthunt/product/[^/]+/alternatives$'
  '^/producthunt/product/[^/]+/customers$'
  '^/producthunt/product/[^/]+/launches$'
  '^/producthunt/product/[^/]+/makers$'
  '^/producthunt/product/[^/]+/reviews$'
  '^/psastore/collections/[^/]+/products$'
  '^/psastore/pages/[^/]+$'
  '^/psastore/products/[^/]+$'
  '^/psastore/products/[^/]+/recommendations$'
  '^/rebag/collections/[^/]+/products$'
  '^/rebag/pages/[^/]+$'
  '^/rebag/products/[^/]+$'
  '^/rebag/products/[^/]+/recommendations$'
  '^/reddit/comments/[^/]+$'
  '^/reddit/domain/[^/]+/posts$'
  '^/reddit/post/[^/]+$'
  '^/reddit/subreddit/[^/]+/about$'
  '^/reddit/subreddit/[^/]+/comments$'
  '^/reddit/subreddit/[^/]+/posts$'
  '^/reddit/user/[^/]+/comments$'
  '^/reddit/user/[^/]+/posts$'
  '^/research/jobs/[^/]+$'
  '^/research/jobs/[^/]+/cancel$'
  '^/research/jobs/[^/]+/events$'
  '^/research/jobs/[^/]+/results$'
  '^/rightmove/agents/[^/]+$'
  '^/rightmove/properties/[^/]+$'
  '^/rothys/collections/[^/]+/products$'
  '^/rothys/pages/[^/]+$'
  '^/rothys/products/[^/]+$'
  '^/rothys/products/[^/]+/recommendations$'
  '^/rover/sitter/[^/]+$'
  '^/rover/trainer/[^/]+$'
  '^/samsclub/content/[^/]+$'
  '^/samsclub/product/[^/]+$'
  '^/samsclub/product/[^/]+/related$'
  '^/shop-app/products/[^/]+$'
  '^/shop-app/products/[^/]+/related$'
  '^/shop-app/products/[^/]+/reviews$'
  '^/shop-app/products/[^/]+/shop$'
  '^/shop-app/products/[^/]+/variant$'
  '^/shop-app/products/[^/]+/variants$'
  '^/shop-app/shops/[^/]+$'
  '^/shop-app/shops/[^/]+/collections/[^/]+/products$'
  '^/shop-app/shops/[^/]+/locations$'
  '^/shop-app/shops/[^/]+/products$'
  '^/shop-app/shops/[^/]+/reviews$'
  '^/shop-app/shops/[^/]+/typeahead$'
  '^/shopify/collections/[^/]+/products$'
  '^/shopify/pages/[^/]+$'
  '^/shopify/products/[^/]+$'
  '^/shopify/products/[^/]+/recommendations$'
  '^/similarweb/web/[^/]+$'
  '^/skims/collections/[^/]+/products$'
  '^/skims/pages/[^/]+$'
  '^/skims/products/[^/]+$'
  '^/skims/products/[^/]+/recommendations$'
  '^/starbucks/product/[^/]+/[^/]+$'
  '^/starbucks/product/[^/]+/[^/]+/nutrition$'
  '^/steam/category/[^/]+$'
  '^/stevemadden/collections/[^/]+/products$'
  '^/stevemadden/pages/[^/]+$'
  '^/stevemadden/products/[^/]+$'
  '^/stevemadden/products/[^/]+/recommendations$'
  '^/stockx/product/[^/]+$'
  '^/strava/clubs/[^/]+$'
  '^/streeteasy/buildings/[^/]+$'
  '^/streeteasy/schools/[^/]+$'
  '^/streeteasy/units/[^/]+/[^/]+$'
  '^/thebodyshop/collections/[^/]+/products$'
  '^/thebodyshop/pages/[^/]+$'
  '^/thebodyshop/products/[^/]+$'
  '^/thebodyshop/products/[^/]+/recommendations$'
  '^/threads/post/[^/]+/[^/]+$'
  '^/threads/post/[^/]+/[^/]+/replies$'
  '^/threads/profile/[^/]+$'
  '^/threads/profile/[^/]+/media$'
  '^/threads/profile/[^/]+/posts$'
  '^/threads/profile/[^/]+/replies$'
  '^/threads/profile/[^/]+/reposts$'
  '^/threads/profile/[^/]+/topics$'
  '^/tiktok/explore/[^/]+$'
  '^/tiktok/hashtag/[^/]+$'
  '^/tiktok/post/[^/]+$'
  '^/tiktok/profile/[^/]+$'
  '^/tmdb/collection/[^/]+$'
  '^/tmdb/movie/[^/]+$'
  '^/tmdb/person/[^/]+$'
  '^/tmdb/tv/[^/]+$'
  '^/tripcom/hotels/[^/]+$'
  '^/trustmrr/category/[^/]+$'
  '^/trustmrr/startup/[^/]+$'
  '^/trustpilot/business/[^/]+$'
  '^/trustpilot/business/[^/]+/related$'
  '^/trustpilot/business/[^/]+/reviews$'
  '^/trustpilot/category/[^/]+$'
  '^/ubereats/store/[^/]+$'
  '^/ubereats/store/[^/]+/menu$'
  '^/ubereats/store/[^/]+/reviews$'
  '^/ulta/product/[^/]+$'
  '^/upwork/freelancer/[^/]+$'
  '^/upwork/job/[^/]+$'
  '^/vrbo/properties/[^/]+$'
  '^/vrbo/properties/[^/]+/rate-calendar$'
  '^/vrbo/properties/[^/]+/reviews$'
  '^/vrbo/travel-pages/[^/]+$'
  '^/walmart/product/[^/]+$'
  '^/walmart/product/[^/]+/reviews$'
  '^/wayfair/product/[^/]+$'
  '^/web/crawl/[^/]+$'
  '^/web/crawl/[^/]+/cancel$'
  '^/web/crawl/[^/]+/results$'
  '^/whatnot/live/[^/]+$'
  '^/whatnot/seller/[^/]+$'
  '^/wish/product/[^/]+$'
  '^/wish/product/[^/]+/related$'
  '^/wish/product/[^/]+/reviews$'
  '^/x/post/[^/]+$'
  '^/x/profile/[^/]+$'
  '^/x/profile/[^/]+/posts$'
  '^/yahoo-finance/calendars/[^/]+$'
  '^/yahoo-finance/industries/[^/]+$'
  '^/yahoo-finance/market/[^/]+/status$'
  '^/yahoo-finance/market/[^/]+/summary$'
  '^/yahoo-finance/screener/[^/]+$'
  '^/yahoo-finance/sectors/[^/]+$'
  '^/yahoo-finance/ticker/[^/]+/actions$'
  '^/yahoo-finance/ticker/[^/]+/analysts$'
  '^/yahoo-finance/ticker/[^/]+/calendar$'
  '^/yahoo-finance/ticker/[^/]+/capital-gains$'
  '^/yahoo-finance/ticker/[^/]+/dividends$'
  '^/yahoo-finance/ticker/[^/]+/earnings$'
  '^/yahoo-finance/ticker/[^/]+/earnings-dates$'
  '^/yahoo-finance/ticker/[^/]+/financials$'
  '^/yahoo-finance/ticker/[^/]+/funds$'
  '^/yahoo-finance/ticker/[^/]+/history$'
  '^/yahoo-finance/ticker/[^/]+/history-metadata$'
  '^/yahoo-finance/ticker/[^/]+/holders$'
  '^/yahoo-finance/ticker/[^/]+/info$'
  '^/yahoo-finance/ticker/[^/]+/isin$'
  '^/yahoo-finance/ticker/[^/]+/news$'
  '^/yahoo-finance/ticker/[^/]+/options$'
  '^/yahoo-finance/ticker/[^/]+/options/[^/]+$'
  '^/yahoo-finance/ticker/[^/]+/quote$'
  '^/yahoo-finance/ticker/[^/]+/sec-filings$'
  '^/yahoo-finance/ticker/[^/]+/shares$'
  '^/yahoo-finance/ticker/[^/]+/shares-full$'
  '^/yahoo-finance/ticker/[^/]+/splits$'
  '^/yahoo-finance/ticker/[^/]+/sustainability$'
  '^/yahoo-finance/ticker/[^/]+/valuation$'
  '^/yahoo-finance/trending/[^/]+$'
  '^/yelp/business/[^/]+$'
  '^/yelp/business/[^/]+/menu$'
  '^/yelp/business/[^/]+/photos$'
  '^/yelp/business/[^/]+/reviews$'
  '^/yelp/business/[^/]+/reviews/highlights$'
  '^/yelp/business/[^/]+/reviews/search$'
  '^/youtube/captions/[^/]+$'
  '^/youtube/channel/[^/]+/playlists$'
  '^/youtube/channel/[^/]+/search$'
  '^/youtube/channel/[^/]+/shorts$'
  '^/youtube/channel/[^/]+/videos$'
  '^/youtube/comments/[^/]+$'
  '^/youtube/playlist/[^/]+$'
  '^/youtube/profile/[^/]+$'
  '^/youtube/tag/[^/]+$'
  '^/youtube/transcript/[^/]+$'
  '^/youtube/transcript/[^/]+/languages$'
  '^/youtube/video/[^/]+$'
  '^/zappos/product/[^/]+$'
  '^/zara/category/[^/]+/products$'
  '^/zara/product/[^/]+$'
  '^/zillow/property/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the crawlora skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/1stdibs/categories$'
  '^GET:/1stdibs/designers$'
  '^GET:/1stdibs/product$'
  '^GET:/1stdibs/search$'
  '^GET:/7now/catalog$'
  '^GET:/7now/categories$'
  '^GET:/7now/category$'
  '^GET:/7now/combo$'
  '^GET:/7now/combos$'
  '^GET:/7now/deals$'
  '^GET:/7now/offers$'
  '^GET:/7now/popular$'
  '^GET:/7now/product$'
  '^GET:/7now/promotion$'
  '^GET:/7now/search$'
  '^GET:/7now/stores$'
  '^GET:/7now/suggest$'
  '^GET:/abcau/article$'
  '^GET:/abcau/author$'
  '^GET:/abcau/headlines$'
  '^GET:/abcau/news$'
  '^GET:/abcau/sections$'
  '^GET:/abcnews/article$'
  '^GET:/abcnews/author$'
  '^GET:/abcnews/headlines$'
  '^GET:/abcnews/news$'
  '^GET:/abcnews/sections$'
  '^GET:/accor/amenities$'
  '^GET:/accor/brands$'
  '^GET:/accor/catalog/hotels$'
  '^GET:/accor/destination/hotels$'
  '^GET:/accor/property$'
  '^GET:/accor/search$'
  '^GET:/accor/search/details$'
  '^GET:/accor/search/suggest$'
  '^GET:/adidas/product$'
  '^GET:/adidas/product/review-topics$'
  '^GET:/adidas/product/reviews$'
  '^GET:/adidas/search$'
  '^GET:/adidas/store$'
  '^GET:/adidas/stores$'
  '^GET:/adidas/suggest$'
  '^GET:/agoda/activities/[^/]+$'
  '^GET:/agoda/activities/search$'
  '^GET:/agoda/flights/search$'
  '^GET:/agoda/flights/search-locations$'
  '^GET:/agoda/homes/search$'
  '^GET:/agoda/hotels/[^/]+$'
  '^GET:/agoda/hotels/search$'
  '^GET:/airbnb/host/[^/]+$'
  '^GET:/airbnb/host/[^/]+/listings$'
  '^GET:/airbnb/host/[^/]+/reviews$'
  '^GET:/airbnb/room/[^/]+$'
  '^GET:/airbnb/room/[^/]+/calendar$'
  '^GET:/airbnb/room/[^/]+/reviews$'
  '^GET:/airbnb/search$'
  '^GET:/alcom/headlines$'
  '^GET:/alcom/news$'
  '^GET:/alcom/sections$'
  '^GET:/aliexpress/reviews$'
  '^GET:/aliexpress/search$'
  '^GET:/aliexpress/search-filters$'
  '^GET:/aljazeera/article$'
  '^GET:/aljazeera/author$'
  '^GET:/aljazeera/categories$'
  '^GET:/aljazeera/headlines$'
  '^GET:/aljazeera/topic$'
  '^GET:/allbirds/collections$'
  '^GET:/allbirds/collections/[^/]+/products$'
  '^GET:/allbirds/pages$'
  '^GET:/allbirds/pages/[^/]+$'
  '^GET:/allbirds/products$'
  '^GET:/allbirds/products/[^/]+$'
  '^GET:/allbirds/products/[^/]+/recommendations$'
  '^GET:/allbirds/search/suggest$'
  '^GET:/allbirds/sitemap/urls$'
  '^GET:/allbirds/sitemaps$'
  '^GET:/allbirds/store$'
  '^GET:/alt/asset$'
  '^GET:/alt/auctions$'
  '^GET:/alt/card-search$'
  '^GET:/alt/categories$'
  '^GET:/alt/listing$'
  '^GET:/alt/market-trends$'
  '^GET:/alt/search$'
  '^GET:/alt/sold-listings$'
  '^GET:/alt/top-movers$'
  '^GET:/amazon-jobs/categories$'
  '^GET:/amazon-jobs/job$'
  '^GET:/amazon-jobs/search$'
  '^GET:/amazon/charts$'
  '^GET:/amazon/charts/categories$'
  '^GET:/amazon/product/[^/]+$'
  '^GET:/amazon/search$'
  '^GET:/amazon/suggest/[^/]+$'
  '^GET:/androidauthority/article$'
  '^GET:/androidauthority/headlines$'
  '^GET:/androidauthority/news$'
  '^GET:/androidauthority/sections$'
  '^GET:/androidpolice/article$'
  '^GET:/androidpolice/author$'
  '^GET:/androidpolice/headlines$'
  '^GET:/androidpolice/news$'
  '^GET:/androidpolice/sections$'
  '^GET:/anime/airing-schedule$'
  '^GET:/anime/character/[^/]+$'
  '^GET:/anime/character/search$'
  '^GET:/anime/rankings$'
  '^GET:/anime/search$'
  '^GET:/anime/title/[^/]+$'
  '^GET:/anime/title/[^/]+/characters$'
  '^GET:/anime/title/[^/]+/recommendations$'
  '^GET:/anime/title/[^/]+/staff$'
  '^GET:/apnews/article$'
  '^GET:/apnews/author$'
  '^GET:/apnews/fact-check$'
  '^GET:/apnews/headlines$'
  '^GET:/apnews/news$'
  '^GET:/apnews/sections$'
  '^GET:/apple-books/audiobook-series/[^/]+$'
  '^GET:/apple-books/audiobook/[^/]+$'
  '^GET:/apple-books/audiobook/[^/]+/reviews$'
  '^GET:/apple-books/audiobook/[^/]+/similar$'
  '^GET:/apple-books/audiobook/search$'
  '^GET:/apple-books/author/[^/]+$'
  '^GET:/apple-books/book/[^/]+$'
  '^GET:/apple-books/book/[^/]+/reviews$'
  '^GET:/apple-books/book/[^/]+/similar$'
  '^GET:/apple-books/charts$'
  '^GET:/apple-books/search$'
  '^GET:/apple-books/series/[^/]+$'
  '^GET:/apple-jobs/job$'
  '^GET:/apple-jobs/locations$'
  '^GET:/apple-jobs/search$'
  '^GET:/apple-maps/autocomplete$'
  '^GET:/apple-maps/categories$'
  '^GET:/apple-maps/category-search$'
  '^GET:/apple-maps/directions$'
  '^GET:/apple-maps/eta$'
  '^GET:/apple-maps/guides$'
  '^GET:/apple-maps/guides/cities$'
  '^GET:/apple-maps/guides/guide$'
  '^GET:/apple-maps/guides/lookup$'
  '^GET:/apple-maps/guides/nearby$'
  '^GET:/apple-maps/guides/publisher$'
  '^GET:/apple-maps/guides/publishers$'
  '^GET:/apple-maps/place$'
  '^GET:/apple-maps/place/photos$'
  '^GET:/apple-maps/places$'
  '^GET:/apple-maps/reverse-geocode$'
  '^GET:/apple-maps/search$'
  '^GET:/apple-maps/transit-departures$'
  '^GET:/apple-maps/venue/browse$'
  '^GET:/apple-podcasts/charts$'
  '^GET:/apple-podcasts/charts/rankings$'
  '^GET:/apple-podcasts/episodes/search$'
  '^GET:/apple-podcasts/new$'
  '^GET:/apple-podcasts/search$'
  '^GET:/apple-podcasts/show/[^/]+$'
  '^GET:/apple-podcasts/show/[^/]+/episodes$'
  '^GET:/apple-podcasts/show/[^/]+/related$'
  '^GET:/appstore/app$'
  '^GET:/appstore/categories$'
  '^GET:/appstore/collection$'
  '^GET:/appstore/collections$'
  '^GET:/appstore/developer/[^/]+$'
  '^GET:/appstore/editorial$'
  '^GET:/appstore/editorial/category$'
  '^GET:/appstore/list$'
  '^GET:/appstore/privacy/[^/]+$'
  '^GET:/appstore/ratings$'
  '^GET:/appstore/reviews$'
  '^GET:/appstore/search$'
  '^GET:/appstore/similar$'
  '^GET:/appstore/suggest/[^/]+$'
  '^GET:/appstore/version-history/[^/]+$'
  '^GET:/arbys/categories$'
  '^GET:/arbys/directory$'
  '^GET:/arbys/location$'
  '^GET:/arbys/locations$'
  '^GET:/arbys/menu$'
  '^GET:/arstechnica/article$'
  '^GET:/arstechnica/author$'
  '^GET:/arstechnica/headlines$'
  '^GET:/arstechnica/news$'
  '^GET:/arstechnica/sections$'
  '^GET:/audible/categories$'
  '^GET:/audible/category/[^/]+$'
  '^GET:/audible/charts$'
  '^GET:/audible/charts/authors$'
  '^GET:/audible/list/[^/]+$'
  '^GET:/audible/product/[^/]+$'
  '^GET:/audible/product/[^/]+/related$'
  '^GET:/audible/product/[^/]+/reviews$'
  '^GET:/audible/products$'
  '^GET:/audible/search$'
  '^GET:/audible/series/[^/]+$'
  '^GET:/autotrader/dealer/[^/]+$'
  '^GET:/autotrader/search$'
  '^GET:/autotrader/vehicle/[^/]+$'
  '^GET:/axios/article$'
  '^GET:/axios/categories$'
  '^GET:/axios/headlines$'
  '^GET:/baidu/search$'
  '^GET:/baidu/suggest$'
  '^GET:/balenciaga/categories$'
  '^GET:/balenciaga/category$'
  '^GET:/balenciaga/product$'
  '^GET:/balenciaga/product/variants$'
  '^GET:/balenciaga/search$'
  '^GET:/balenciaga/store-countries$'
  '^GET:/balenciaga/stores$'
  '^GET:/barrons/article$'
  '^GET:/barrons/headlines$'
  '^GET:/barrons/news$'
  '^GET:/barrons/topics$'
  '^GET:/bbb/article$'
  '^GET:/bbb/business$'
  '^GET:/bbb/business/complaints$'
  '^GET:/bbb/business/more-info$'
  '^GET:/bbb/business/reviews$'
  '^GET:/bbb/category$'
  '^GET:/bbb/local-bbb$'
  '^GET:/bbb/local-bbbs$'
  '^GET:/bbb/news$'
  '^GET:/bbb/news/topics$'
  '^GET:/bbb/page$'
  '^GET:/bbb/regions$'
  '^GET:/bbb/scamtracker/[^/]+$'
  '^GET:/bbb/scamtracker/search$'
  '^GET:/bbb/scamtracker/state-stats$'
  '^GET:/bbb/search$'
  '^GET:/bbb/search/filters$'
  '^GET:/bbc/article$'
  '^GET:/bbc/author$'
  '^GET:/bbc/headlines$'
  '^GET:/bbc/live$'
  '^GET:/bbc/search$'
  '^GET:/benzinga/article$'
  '^GET:/benzinga/headlines$'
  '^GET:/benzinga/news$'
  '^GET:/benzinga/search$'
  '^GET:/benzinga/sections$'
  '^GET:/bestbuy/brands$'
  '^GET:/bestbuy/categories$'
  '^GET:/bestbuy/categories/trending$'
  '^GET:/bestbuy/category$'
  '^GET:/bestbuy/category/subcategories$'
  '^GET:/bestbuy/product$'
  '^GET:/bestbuy/product/questions$'
  '^GET:/bestbuy/product/related$'
  '^GET:/bestbuy/product/reviews$'
  '^GET:/bestbuy/search$'
  '^GET:/bestbuy/stores$'
  '^GET:/bigcommerce/category$'
  '^GET:/bigcommerce/product$'
  '^GET:/bigcommerce/search$'
  '^GET:/bilibili/anime-home$'
  '^GET:/bilibili/autocomplete$'
  '^GET:/bilibili/guochuang-home$'
  '^GET:/bilibili/must-watch$'
  '^GET:/bilibili/popular$'
  '^GET:/bilibili/ranking$'
  '^GET:/bilibili/vertical-home$'
  '^GET:/bilibili/weekly$'
  '^GET:/billboard/article$'
  '^GET:/billboard/author$'
  '^GET:/billboard/headlines$'
  '^GET:/billboard/news$'
  '^GET:/billboard/sections$'
  '^GET:/bing/images$'
  '^GET:/bing/news$'
  '^GET:/bing/search$'
  '^GET:/bing/suggest$'
  '^GET:/bing/videos$'
  '^GET:/birminghammail/article$'
  '^GET:/birminghammail/author$'
  '^GET:/birminghammail/headlines$'
  '^GET:/birminghammail/news$'
  '^GET:/birminghammail/sections$'
  '^GET:/bleacherreport/article$'
  '^GET:/bleacherreport/author$'
  '^GET:/bleacherreport/headlines$'
  '^GET:/bleacherreport/news$'
  '^GET:/bleacherreport/sections$'
  '^GET:/bloomberg/article$'
  '^GET:/bloomberg/author$'
  '^GET:/bloomberg/categories$'
  '^GET:/bloomberg/headlines$'
  '^GET:/bloomberg/news$'
  '^GET:/bloomberg/news-sitemaps$'
  '^GET:/bluesky/author-feed$'
  '^GET:/bluesky/followers$'
  '^GET:/bluesky/follows$'
  '^GET:/bluesky/post-likes$'
  '^GET:/bluesky/post-quotes$'
  '^GET:/bluesky/post-reposted-by$'
  '^GET:/bluesky/post-thread$'
  '^GET:/bluesky/posts$'
  '^GET:/bluesky/profile$'
  '^GET:/bluesky/search-actors$'
  '^GET:/bluesky/trending-topics$'
  '^GET:/bonhams/auctions/[^/]+$'
  '^GET:/bonhams/auctions/[^/]+/lots$'
  '^GET:/bonhams/auctions/search$'
  '^GET:/bonhams/lots/[^/]+/[^/]+$'
  '^GET:/bonhams/lots/search$'
  '^GET:/booking-attractions/detail$'
  '^GET:/booking-attractions/reviews$'
  '^GET:/booking-attractions/search$'
  '^GET:/booking-flights/autocomplete$'
  '^GET:/booking-flights/search$'
  '^GET:/booking/hotel-detail$'
  '^GET:/booking/reviews$'
  '^GET:/booking/search$'
  '^GET:/boots/search$'
  '^GET:/boots/suggest$'
  '^GET:/bostonglobe/news$'
  '^GET:/boxofficemojo/brand$'
  '^GET:/boxofficemojo/brands$'
  '^GET:/boxofficemojo/calendar$'
  '^GET:/boxofficemojo/calendar/changes$'
  '^GET:/boxofficemojo/calendar/date$'
  '^GET:/boxofficemojo/date/domestic$'
  '^GET:/boxofficemojo/franchise$'
  '^GET:/boxofficemojo/franchises$'
  '^GET:/boxofficemojo/genre$'
  '^GET:/boxofficemojo/genres$'
  '^GET:/boxofficemojo/lifetime-grosses$'
  '^GET:/boxofficemojo/release$'
  '^GET:/boxofficemojo/release-group$'
  '^GET:/boxofficemojo/showdown$'
  '^GET:/boxofficemojo/showdowns$'
  '^GET:/boxofficemojo/title$'
  '^GET:/boxofficemojo/weekend/domestic$'
  '^GET:/boxofficemojo/weekend/domestic/by-distributor$'
  '^GET:/boxofficemojo/weekend/domestic/estimates$'
  '^GET:/boxofficemojo/year/domestic$'
  '^GET:/boxofficemojo/year/worldwide$'
  '^GET:/brand/retrieve$'
  '^GET:/brave/images$'
  '^GET:/brave/news$'
  '^GET:/brave/search$'
  '^GET:/brave/suggest$'
  '^GET:/brave/videos$'
  '^GET:/breitbart/article$'
  '^GET:/breitbart/author$'
  '^GET:/breitbart/headlines$'
  '^GET:/breitbart/news$'
  '^GET:/breitbart/sections$'
  '^GET:/brisbanetimes/article$'
  '^GET:/brisbanetimes/author$'
  '^GET:/brisbanetimes/headlines$'
  '^GET:/brisbanetimes/news$'
  '^GET:/brisbanetimes/sections$'
  '^GET:/brooklinen/collections$'
  '^GET:/brooklinen/collections/[^/]+/products$'
  '^GET:/brooklinen/pages$'
  '^GET:/brooklinen/pages/[^/]+$'
  '^GET:/brooklinen/products$'
  '^GET:/brooklinen/products/[^/]+$'
  '^GET:/brooklinen/products/[^/]+/recommendations$'
  '^GET:/brooklinen/search/suggest$'
  '^GET:/brooklinen/sitemap/urls$'
  '^GET:/brooklinen/sitemaps$'
  '^GET:/brooklinen/store$'
  '^GET:/burberry/categories$'
  '^GET:/burberry/category$'
  '^GET:/burberry/product$'
  '^GET:/burberry/related$'
  '^GET:/burberry/search$'
  '^GET:/burberry/suggest$'
  '^GET:/burgerking/availability$'
  '^GET:/burgerking/locations$'
  '^GET:/burgerking/menu$'
  '^GET:/burgerking/product$'
  '^GET:/businessinsider/article$'
  '^GET:/businessinsider/author$'
  '^GET:/businessinsider/headlines$'
  '^GET:/businessinsider/news$'
  '^GET:/businessinsider/sections$'
  '^GET:/businessstandard/article$'
  '^GET:/businessstandard/author$'
  '^GET:/businessstandard/headlines$'
  '^GET:/businessstandard/news$'
  '^GET:/businessstandard/sections$'
  '^GET:/capterra/product$'
  '^GET:/capterra/product/reviews$'
  '^GET:/capterra/search$'
  '^GET:/carmax/search$'
  '^GET:/carmax/search/suggestions$'
  '^GET:/carmax/shop-by-brand$'
  '^GET:/carmax/store/[^/]+$'
  '^GET:/carmax/stores$'
  '^GET:/carmax/vehicle/[^/]+$'
  '^GET:/carmax/vehicle/[^/]+/recommendations$'
  '^GET:/carsdotcom/search$'
  '^GET:/carsdotcom/vehicle/[^/]+$'
  '^GET:/cbc/article$'
  '^GET:/cbc/author$'
  '^GET:/cbc/headlines$'
  '^GET:/cbc/news$'
  '^GET:/cbc/sections$'
  '^GET:/cbr/article$'
  '^GET:/cbr/author$'
  '^GET:/cbr/headlines$'
  '^GET:/cbr/news$'
  '^GET:/cbr/sections$'
  '^GET:/cbsnews/article$'
  '^GET:/cbsnews/author$'
  '^GET:/cbsnews/headlines$'
  '^GET:/cbsnews/news$'
  '^GET:/cbsnews/sections$'
  '^GET:/cbssports/article$'
  '^GET:/cbssports/author$'
  '^GET:/cbssports/headlines$'
  '^GET:/cbssports/news$'
  '^GET:/cbssports/sections$'
  '^GET:/chewy/brands$'
  '^GET:/chewy/categories$'
  '^GET:/chewy/category$'
  '^GET:/chewy/facets$'
  '^GET:/chewy/gtin-lookup$'
  '^GET:/chewy/inventory$'
  '^GET:/chewy/item-attributes$'
  '^GET:/chewy/product$'
  '^GET:/chewy/product-questions$'
  '^GET:/chewy/product-reviews$'
  '^GET:/chewy/products$'
  '^GET:/chewy/search$'
  '^GET:/chewy/suggest$'
  '^GET:/chewy/variants$'
  '^GET:/chicagotribune/article$'
  '^GET:/chicagotribune/author$'
  '^GET:/chicagotribune/headlines$'
  '^GET:/chicagotribune/news$'
  '^GET:/chicagotribune/sections$'
  '^GET:/chick-fil-a/content$'
  '^GET:/chick-fil-a/content-taxonomy$'
  '^GET:/chick-fil-a/faq$'
  '^GET:/chick-fil-a/location$'
  '^GET:/chick-fil-a/locations$'
  '^GET:/chick-fil-a/menu$'
  '^GET:/chick-fil-a/menu-item$'
  '^GET:/chick-fil-a/menu-taxonomy$'
  '^GET:/chipotle/ingredients$'
  '^GET:/chipotle/meals$'
  '^GET:/chipotle/menu$'
  '^GET:/chipotle/menu/metadata$'
  '^GET:/chipotle/restaurant$'
  '^GET:/chipotle/restaurant/meals$'
  '^GET:/chipotle/restaurant/menu$'
  '^GET:/chipotle/restaurants$'
  '^GET:/chromewebstore/categories$'
  '^GET:/chromewebstore/category$'
  '^GET:/chromewebstore/charts$'
  '^GET:/chromewebstore/collection$'
  '^GET:/chromewebstore/developer$'
  '^GET:/chromewebstore/item$'
  '^GET:/chromewebstore/permissions$'
  '^GET:/chromewebstore/privacy$'
  '^GET:/chromewebstore/reviews$'
  '^GET:/chromewebstore/search$'
  '^GET:/chromewebstore/similar$'
  '^GET:/chromewebstore/suggest$'
  '^GET:/chrono24/autocomplete$'
  '^GET:/chrono24/brands$'
  '^GET:/chrono24/dealer$'
  '^GET:/chrono24/dealer/reviews$'
  '^GET:/chrono24/facets$'
  '^GET:/chrono24/listing$'
  '^GET:/chrono24/models$'
  '^GET:/chrono24/search$'
  '^GET:/clevelandcom/news$'
  '^GET:/cna/article$'
  '^GET:/cna/author$'
  '^GET:/cna/headlines$'
  '^GET:/cna/news$'
  '^GET:/cna/sections$'
  '^GET:/cnbc/article$'
  '^GET:/cnbc/author$'
  '^GET:/cnbc/categories$'
  '^GET:/cnbc/headlines$'
  '^GET:/cnet/article$'
  '^GET:/cnet/author$'
  '^GET:/cnet/headlines$'
  '^GET:/cnet/news$'
  '^GET:/cnet/sections$'
  '^GET:/cnn/article$'
  '^GET:/cnn/author$'
  '^GET:/cnn/headlines$'
  '^GET:/cnn/live-story$'
  '^GET:/coingecko/categories$'
  '^GET:/coingecko/category/[^/]+/coins$'
  '^GET:/coingecko/chains$'
  '^GET:/coingecko/chains/[^/]+$'
  '^GET:/coingecko/coin/[^/]+$'
  '^GET:/coingecko/coin/[^/]+/analysis$'
  '^GET:/coingecko/exchange/[^/]+$'
  '^GET:/coingecko/exchanges$'
  '^GET:/coingecko/gainers-losers$'
  '^GET:/coingecko/global$'
  '^GET:/coingecko/global/charts$'
  '^GET:/coingecko/learn/articles$'
  '^GET:/coingecko/markets$'
  '^GET:/coingecko/new-coins$'
  '^GET:/coingecko/news$'
  '^GET:/coingecko/nft/category/[^/]+$'
  '^GET:/coingecko/nfts$'
  '^GET:/coingecko/search$'
  '^GET:/coingecko/token-unlocks$'
  '^GET:/coingecko/treasuries$'
  '^GET:/coingecko/trending$'
  '^GET:/colehaan/collections$'
  '^GET:/colehaan/collections/[^/]+/products$'
  '^GET:/colehaan/pages$'
  '^GET:/colehaan/pages/[^/]+$'
  '^GET:/colehaan/products$'
  '^GET:/colehaan/products/[^/]+$'
  '^GET:/colehaan/products/[^/]+/recommendations$'
  '^GET:/colehaan/search/suggest$'
  '^GET:/colehaan/sitemap/urls$'
  '^GET:/colehaan/sitemaps$'
  '^GET:/colehaan/store$'
  '^GET:/collider/article$'
  '^GET:/collider/author$'
  '^GET:/collider/headlines$'
  '^GET:/collider/news$'
  '^GET:/collider/sections$'
  '^GET:/comc/categories$'
  '^GET:/comc/listing$'
  '^GET:/comc/search$'
  '^GET:/congress/report$'
  '^GET:/congress/stock-disclosures$'
  '^GET:/costco/categories$'
  '^GET:/costco/product/[^/]+$'
  '^GET:/costco/product/[^/]+/availability$'
  '^GET:/costco/product/[^/]+/reviews$'
  '^GET:/costco/search$'
  '^GET:/costco/warehouses$'
  '^GET:/courtlistener/courts$'
  '^GET:/courtlistener/people$'
  '^GET:/courtlistener/search$'
  '^GET:/cricinfo/calendar$'
  '^GET:/cricinfo/commentary$'
  '^GET:/cricinfo/grounds$'
  '^GET:/cricinfo/live$'
  '^GET:/cricinfo/match$'
  '^GET:/cricinfo/news$'
  '^GET:/cricinfo/photos$'
  '^GET:/cricinfo/rankings$'
  '^GET:/cricinfo/records$'
  '^GET:/cricinfo/records/index$'
  '^GET:/cricinfo/rss$'
  '^GET:/cricinfo/scores$'
  '^GET:/cricinfo/series$'
  '^GET:/cricinfo/squads$'
  '^GET:/cricinfo/stats$'
  '^GET:/cricinfo/story$'
  '^GET:/cricinfo/team$'
  '^GET:/cricinfo/team/schedule$'
  '^GET:/cricinfo/teams$'
  '^GET:/cricinfo/venue$'
  '^GET:/cricinfo/venue/matches$'
  '^GET:/cricinfo/videos$'
  '^GET:/ctvnews/article$'
  '^GET:/ctvnews/author$'
  '^GET:/ctvnews/headlines$'
  '^GET:/ctvnews/news$'
  '^GET:/ctvnews/sections$'
  '^GET:/culvers/calendar$'
  '^GET:/culvers/categories$'
  '^GET:/culvers/directory$'
  '^GET:/culvers/flavor$'
  '^GET:/culvers/item$'
  '^GET:/culvers/menu$'
  '^GET:/culvers/store$'
  '^GET:/cvs/brands$'
  '^GET:/cvs/categories$'
  '^GET:/cvs/category$'
  '^GET:/cvs/product-ingredients/[^/]+$'
  '^GET:/cvs/product/[^/]+$'
  '^GET:/cvs/search$'
  '^GET:/cvs/store-locator$'
  '^GET:/dailycaller/article$'
  '^GET:/dailycaller/author$'
  '^GET:/dailycaller/headlines$'
  '^GET:/dailycaller/news$'
  '^GET:/dailycaller/sections$'
  '^GET:/dailyexpress/article$'
  '^GET:/dailyexpress/author$'
  '^GET:/dailyexpress/headlines$'
  '^GET:/dailyexpress/news$'
  '^GET:/dailyexpress/sections$'
  '^GET:/dailykos/article$'
  '^GET:/dailykos/headlines$'
  '^GET:/dailykos/news$'
  '^GET:/dailykos/sections$'
  '^GET:/dailymail/article$'
  '^GET:/dailymail/author$'
  '^GET:/dailymail/headlines$'
  '^GET:/dailymail/news$'
  '^GET:/dailymail/sections$'
  '^GET:/dailymaverick/article$'
  '^GET:/dailymaverick/headlines$'
  '^GET:/dailymaverick/news$'
  '^GET:/dailymaverick/sections$'
  '^GET:/dailyrecord/article$'
  '^GET:/dailyrecord/author$'
  '^GET:/dailyrecord/headlines$'
  '^GET:/dailyrecord/news$'
  '^GET:/dailyrecord/sections$'
  '^GET:/dailystaruk/article$'
  '^GET:/dailystaruk/author$'
  '^GET:/dailystaruk/headlines$'
  '^GET:/dailystaruk/news$'
  '^GET:/dailystaruk/sections$'
  '^GET:/dailywire/article$'
  '^GET:/dailywire/author$'
  '^GET:/dailywire/headlines$'
  '^GET:/dailywire/news$'
  '^GET:/dailywire/sections$'
  '^GET:/dawn/article$'
  '^GET:/dawn/author$'
  '^GET:/dawn/headlines$'
  '^GET:/dawn/news$'
  '^GET:/dawn/sections$'
  '^GET:/deadline/article$'
  '^GET:/deadline/author$'
  '^GET:/deadline/headlines$'
  '^GET:/deadline/news$'
  '^GET:/deadline/sections$'
  '^GET:/deliveroo/fulfillment-times$'
  '^GET:/deliveroo/restaurant$'
  '^GET:/deliveroo/restaurant/menu$'
  '^GET:/deliveroo/search$'
  '^GET:/deliveroo/search/filters$'
  '^GET:/denverpost/article$'
  '^GET:/denverpost/author$'
  '^GET:/denverpost/headlines$'
  '^GET:/denverpost/news$'
  '^GET:/denverpost/sections$'
  '^GET:/depop/brands$'
  '^GET:/depop/categories$'
  '^GET:/depop/item/[^/]+$'
  '^GET:/depop/item/[^/]+/similar$'
  '^GET:/depop/search$'
  '^GET:/depop/search-sellers$'
  '^GET:/depop/search/facets$'
  '^GET:/depop/shop/[^/]+$'
  '^GET:/depop/sizes$'
  '^GET:/depop/suggest$'
  '^GET:/developer/sources$'
  '^GET:/discogs/artist/[^/]+$'
  '^GET:/discogs/artist/[^/]+/releases$'
  '^GET:/discogs/label/[^/]+$'
  '^GET:/discogs/label/[^/]+/releases$'
  '^GET:/discogs/master/[^/]+$'
  '^GET:/discogs/release/[^/]+$'
  '^GET:/discogs/search$'
  '^GET:/dominos/coupons$'
  '^GET:/dominos/customization$'
  '^GET:/dominos/menu$'
  '^GET:/dominos/nutrition$'
  '^GET:/dominos/store$'
  '^GET:/dominos/store-locator$'
  '^GET:/doordash/explore$'
  '^GET:/doordash/feed$'
  '^GET:/doordash/search$'
  '^GET:/doordash/search/autocomplete$'
  '^GET:/doordash/search/filters$'
  '^GET:/doordash/search/items$'
  '^GET:/doordash/store/[^/]+$'
  '^GET:/doordash/store/[^/]+/fulfillment$'
  '^GET:/doordash/store/[^/]+/info$'
  '^GET:/doordash/store/[^/]+/item/[^/]+$'
  '^GET:/doordash/store/[^/]+/menu$'
  '^GET:/doordash/store/[^/]+/reviews$'
  '^GET:/draftkings/sportsbook/event$'
  '^GET:/draftkings/sportsbook/event-context$'
  '^GET:/draftkings/sportsbook/event-markets$'
  '^GET:/draftkings/sportsbook/featured-leagues$'
  '^GET:/draftkings/sportsbook/futures$'
  '^GET:/draftkings/sportsbook/league-events$'
  '^GET:/draftkings/sportsbook/leagues$'
  '^GET:/draftkings/sportsbook/live$'
  '^GET:/draftkings/sportsbook/odds$'
  '^GET:/draftkings/sportsbook/quick-links$'
  '^GET:/draftkings/sportsbook/team$'
  '^GET:/draftkings/sportsbook/teams$'
  '^GET:/duckduckgo/image$'
  '^GET:/duckduckgo/news$'
  '^GET:/duckduckgo/search$'
  '^GET:/duckduckgo/shopping$'
  '^GET:/duckduckgo/suggest$'
  '^GET:/duckduckgo/video$'
  '^GET:/dunkin/directory$'
  '^GET:/dunkin/menu$'
  '^GET:/dunkin/nearby$'
  '^GET:/dunkin/store$'
  '^GET:/dw/article$'
  '^GET:/dw/author$'
  '^GET:/dw/headlines$'
  '^GET:/dw/news$'
  '^GET:/dw/sections$'
  '^GET:/ebay/item/[^/]+$'
  '^GET:/ebay/live/streams$'
  '^GET:/ebay/live/streams/[^/]+$'
  '^GET:/ebay/live/streams/[^/]+/items$'
  '^GET:/ebay/live/streams/batch$'
  '^GET:/ebay/seller/[^/]+$'
  '^GET:/ebay/seller/[^/]+/about$'
  '^GET:/ebay/seller/[^/]+/feedback$'
  '^GET:/ebay/seller/[^/]+/shop$'
  '^GET:/economictimes/article$'
  '^GET:/economictimes/author$'
  '^GET:/economictimes/headlines$'
  '^GET:/economictimes/news$'
  '^GET:/economictimes/sections$'
  '^GET:/engadget/article$'
  '^GET:/engadget/author$'
  '^GET:/engadget/headlines$'
  '^GET:/engadget/news$'
  '^GET:/engadget/sections$'
  '^GET:/eonline/article$'
  '^GET:/eonline/author$'
  '^GET:/eonline/headlines$'
  '^GET:/eonline/news$'
  '^GET:/eonline/sections$'
  '^GET:/espn/athlete$'
  '^GET:/espn/game-summary$'
  '^GET:/espn/news$'
  '^GET:/espn/rankings$'
  '^GET:/espn/scoreboard$'
  '^GET:/espn/standings$'
  '^GET:/espn/team$'
  '^GET:/espn/team-roster$'
  '^GET:/espn/teams$'
  '^GET:/etsy/listing/[^/]+$'
  '^GET:/etsy/listing/[^/]+/reviews$'
  '^GET:/etsy/search$'
  '^GET:/etsy/shop/[^/]+$'
  '^GET:/etsy/shop/[^/]+/listings$'
  '^GET:/etsy/shop/[^/]+/reviews$'
  '^GET:/etsy/shop/search$'
  '^GET:/euronews/article$'
  '^GET:/euronews/author$'
  '^GET:/euronews/headlines$'
  '^GET:/euronews/news$'
  '^GET:/euronews/sections$'
  '^GET:/everlane/collections$'
  '^GET:/everlane/collections/[^/]+/products$'
  '^GET:/everlane/pages$'
  '^GET:/everlane/pages/[^/]+$'
  '^GET:/everlane/products$'
  '^GET:/everlane/products/[^/]+$'
  '^GET:/everlane/products/[^/]+/recommendations$'
  '^GET:/everlane/search/suggest$'
  '^GET:/everlane/sitemap/urls$'
  '^GET:/everlane/sitemaps$'
  '^GET:/everlane/store$'
  '^GET:/ew/article$'
  '^GET:/ew/author$'
  '^GET:/ew/headlines$'
  '^GET:/ew/news$'
  '^GET:/ew/sections$'
  '^GET:/expresstribune/article$'
  '^GET:/expresstribune/author$'
  '^GET:/expresstribune/headlines$'
  '^GET:/expresstribune/news$'
  '^GET:/expresstribune/sections$'
  '^GET:/facebook/[^/]+$'
  '^GET:/facebook/marketplace/search$'
  '^GET:/fanatics/categories$'
  '^GET:/fanatics/category$'
  '^GET:/fanatics/product$'
  '^GET:/fanatics/search$'
  '^GET:/fanaticscollect/auctions$'
  '^GET:/fanaticscollect/categories$'
  '^GET:/fanaticscollect/instant-rips/categories$'
  '^GET:/fanaticscollect/listing/[^/]+$'
  '^GET:/fanaticscollect/search$'
  '^GET:/fanaticscollect/sold-items$'
  '^GET:/fanaticscollect/trending-searches$'
  '^GET:/fanaticslive/browse$'
  '^GET:/fanaticslive/channel/[^/]+$'
  '^GET:/fanaticslive/leagues$'
  '^GET:/fanaticslive/shop/[^/]+$'
  '^GET:/fanaticslive/shop/[^/]+/shows$'
  '^GET:/fanaticslive/shops$'
  '^GET:/fanaticslive/show/[^/]+$'
  '^GET:/fanaticslive/show/[^/]+/instant-rips$'
  '^GET:/farfetch/categories$'
  '^GET:/farfetch/designers$'
  '^GET:/farfetch/product$'
  '^GET:/farfetch/search$'
  '^GET:/fashionnova/collections$'
  '^GET:/fashionnova/collections/[^/]+/products$'
  '^GET:/fashionnova/pages$'
  '^GET:/fashionnova/pages/[^/]+$'
  '^GET:/fashionnova/products$'
  '^GET:/fashionnova/products/[^/]+$'
  '^GET:/fashionnova/products/[^/]+/recommendations$'
  '^GET:/fashionnova/search/suggest$'
  '^GET:/fashionnova/sitemap/urls$'
  '^GET:/fashionnova/sitemaps$'
  '^GET:/fashionnova/store$'
  '^GET:/fashionphile/collections$'
  '^GET:/fashionphile/collections/[^/]+/products$'
  '^GET:/fashionphile/pages$'
  '^GET:/fashionphile/pages/[^/]+$'
  '^GET:/fashionphile/products$'
  '^GET:/fashionphile/products/[^/]+$'
  '^GET:/fashionphile/products/[^/]+/recommendations$'
  '^GET:/fashionphile/search$'
  '^GET:/fashionphile/search/suggest$'
  '^GET:/fashionphile/sitemap/urls$'
  '^GET:/fashionphile/sitemaps$'
  '^GET:/fashionphile/store$'
  '^GET:/fastcompany/article$'
  '^GET:/fastcompany/author$'
  '^GET:/fastcompany/headlines$'
  '^GET:/fastcompany/news$'
  '^GET:/fastcompany/sections$'
  '^GET:/fiveguys/directory$'
  '^GET:/fiveguys/faq$'
  '^GET:/fiveguys/faq-categories$'
  '^GET:/fiveguys/menu$'
  '^GET:/fiveguys/nearby$'
  '^GET:/fiveguys/nutrition$'
  '^GET:/fiveguys/ordering-locations$'
  '^GET:/fiveguys/ordering-menu$'
  '^GET:/fiveguys/search$'
  '^GET:/fiveguys/store$'
  '^GET:/fiverr/gig/[^/]+/[^/]+$'
  '^GET:/fiverr/search$'
  '^GET:/fiverr/seller/[^/]+$'
  '^GET:/flashscore/calendar$'
  '^GET:/flashscore/calendar-categories$'
  '^GET:/flashscore/competitions$'
  '^GET:/flashscore/entity-news$'
  '^GET:/flashscore/match-box-score$'
  '^GET:/flashscore/match-darts$'
  '^GET:/flashscore/match-h2h$'
  '^GET:/flashscore/match-highlights$'
  '^GET:/flashscore/match-info$'
  '^GET:/flashscore/match-lineups$'
  '^GET:/flashscore/match-missing-players$'
  '^GET:/flashscore/match-momentum$'
  '^GET:/flashscore/match-news$'
  '^GET:/flashscore/match-odds$'
  '^GET:/flashscore/match-player-stats$'
  '^GET:/flashscore/match-point-by-point$'
  '^GET:/flashscore/match-predicted-lineups$'
  '^GET:/flashscore/match-report$'
  '^GET:/flashscore/match-standings$'
  '^GET:/flashscore/match-stats$'
  '^GET:/flashscore/match-tv$'
  '^GET:/flashscore/navigation$'
  '^GET:/flashscore/news$'
  '^GET:/flashscore/news-article$'
  '^GET:/flashscore/news-article-body$'
  '^GET:/flashscore/news-categories$'
  '^GET:/flashscore/news-most-read$'
  '^GET:/flashscore/odds-geos$'
  '^GET:/flashscore/player$'
  '^GET:/flashscore/player-fixtures$'
  '^GET:/flashscore/player-injuries$'
  '^GET:/flashscore/player-match-log$'
  '^GET:/flashscore/player-news$'
  '^GET:/flashscore/player-results$'
  '^GET:/flashscore/player-transfers$'
  '^GET:/flashscore/ranking-categories$'
  '^GET:/flashscore/rankings$'
  '^GET:/flashscore/scores$'
  '^GET:/flashscore/search$'
  '^GET:/flashscore/sports$'
  '^GET:/flashscore/team$'
  '^GET:/flashscore/team-fixtures$'
  '^GET:/flashscore/team-news$'
  '^GET:/flashscore/team-outright-odds$'
  '^GET:/flashscore/team-results$'
  '^GET:/flashscore/team-squad$'
  '^GET:/flashscore/team-transfers$'
  '^GET:/flashscore/top-search$'
  '^GET:/flashscore/tournament-archive-seasons$'
  '^GET:/flashscore/tournament-events$'
  '^GET:/flashscore/tournament-outright-odds$'
  '^GET:/flashscore/tournament-seasons$'
  '^GET:/flashscore/tournament-standings$'
  '^GET:/flashscore/tournament-standings-views$'
  '^GET:/foodpanda/restaurant$'
  '^GET:/foodpanda/restaurant/menu$'
  '^GET:/foodpanda/restaurant/reviews$'
  '^GET:/foodpanda/search$'
  '^GET:/foodpanda/search/cuisines$'
  '^GET:/forbes/article$'
  '^GET:/forbes/author$'
  '^GET:/forbes/billionaires$'
  '^GET:/forbes/categories$'
  '^GET:/forbes/headlines$'
  '^GET:/forbes/person$'
  '^GET:/foreignaffairs/article$'
  '^GET:/foreignaffairs/author$'
  '^GET:/foreignaffairs/headlines$'
  '^GET:/foreignaffairs/topic$'
  '^GET:/foreignaffairs/topics$'
  '^GET:/foreignpolicy/article$'
  '^GET:/foreignpolicy/author$'
  '^GET:/foreignpolicy/headlines$'
  '^GET:/foreignpolicy/live$'
  '^GET:/foreignpolicy/live-detail$'
  '^GET:/foreignpolicy/project$'
  '^GET:/foreignpolicy/projects$'
  '^GET:/foreignpolicy/topic$'
  '^GET:/fortune/article$'
  '^GET:/fortune/author$'
  '^GET:/fortune/companies$'
  '^GET:/fortune/companies/filters$'
  '^GET:/fortune/company$'
  '^GET:/fortune/headlines$'
  '^GET:/fortune/news$'
  '^GET:/fortune/ranking$'
  '^GET:/fortune/ranking/filters$'
  '^GET:/fortune/ranking/lists$'
  '^GET:/fortune/ranking/years$'
  '^GET:/fortune/sections$'
  '^GET:/fotmob/audio-matches$'
  '^GET:/fotmob/fifa-ranking-periods$'
  '^GET:/fotmob/fifa-rankings$'
  '^GET:/fotmob/latest-news$'
  '^GET:/fotmob/league$'
  '^GET:/fotmob/leagues$'
  '^GET:/fotmob/lineup-builder-players$'
  '^GET:/fotmob/lineup-builder-team$'
  '^GET:/fotmob/match$'
  '^GET:/fotmob/match-media$'
  '^GET:/fotmob/matches$'
  '^GET:/fotmob/news$'
  '^GET:/fotmob/news-article$'
  '^GET:/fotmob/player$'
  '^GET:/fotmob/player-match-stats$'
  '^GET:/fotmob/player-matches$'
  '^GET:/fotmob/player-stats$'
  '^GET:/fotmob/search$'
  '^GET:/fotmob/seasons$'
  '^GET:/fotmob/stats$'
  '^GET:/fotmob/stats-categories$'
  '^GET:/fotmob/table$'
  '^GET:/fotmob/team$'
  '^GET:/fotmob/team-fixtures$'
  '^GET:/fotmob/team-news$'
  '^GET:/fotmob/transfers$'
  '^GET:/fotmob/trending-news$'
  '^GET:/fotmob/trending-searches$'
  '^GET:/fotmob/tv-guide$'
  '^GET:/fotmob/tv-guide-channels$'
  '^GET:/fotmob/tv-guide-countries$'
  '^GET:/foxnews/article$'
  '^GET:/foxnews/author$'
  '^GET:/foxnews/headlines$'
  '^GET:/foxnews/news$'
  '^GET:/foxnews/search$'
  '^GET:/foxnews/sections$'
  '^GET:/foxsports/article$'
  '^GET:/foxsports/headlines$'
  '^GET:/foxsports/news$'
  '^GET:/foxsports/sections$'
  '^GET:/france24/article$'
  '^GET:/france24/author$'
  '^GET:/france24/headlines$'
  '^GET:/france24/news$'
  '^GET:/france24/sections$'
  '^GET:/freemalaysiatoday/news$'
  '^GET:/freemalaysiatoday/sections$'
  '^GET:/ft/article$'
  '^GET:/ft/author$'
  '^GET:/ft/categories$'
  '^GET:/ft/headlines$'
  '^GET:/ft/news$'
  '^GET:/ft/search$'
  '^GET:/gamerant/article$'
  '^GET:/gamerant/author$'
  '^GET:/gamerant/headlines$'
  '^GET:/gamerant/news$'
  '^GET:/gamerant/sections$'
  '^GET:/gamesradar/article$'
  '^GET:/gamesradar/author$'
  '^GET:/gamesradar/headlines$'
  '^GET:/gamesradar/news$'
  '^GET:/gamesradar/sections$'
  '^GET:/gbnews/article$'
  '^GET:/gbnews/author$'
  '^GET:/gbnews/headlines$'
  '^GET:/gbnews/news$'
  '^GET:/gbnews/sections$'
  '^GET:/gdelt/context$'
  '^GET:/gdelt/search$'
  '^GET:/gdelt/timeline$'
  '^GET:/gdelt/tonechart$'
  '^GET:/gdelt/tv-concept-entities$'
  '^GET:/gdelt/tv-search$'
  '^GET:/gdelt/tv-showchart$'
  '^GET:/gdelt/tv-stationchart$'
  '^GET:/gdelt/tv-stationdetails$'
  '^GET:/gdelt/tv-timeline$'
  '^GET:/gdelt/tv-visual-entities$'
  '^GET:/gdelt/tv-wordcloud$'
  '^GET:/geocoding/lookup$'
  '^GET:/geocoding/reverse$'
  '^GET:/geocoding/search$'
  '^GET:/ghanaweb/archive$'
  '^GET:/ghanaweb/archive/months$'
  '^GET:/ghanaweb/article$'
  '^GET:/ghanaweb/headlines$'
  '^GET:/ghanaweb/news$'
  '^GET:/ghanaweb/sections$'
  '^GET:/ghanaweb/video$'
  '^GET:/ghanaweb/video-sections$'
  '^GET:/ghanaweb/videos$'
  '^GET:/github/org/[^/]+$'
  '^GET:/github/org/[^/]+/repos$'
  '^GET:/github/repo/[^/]+/[^/]+$'
  '^GET:/github/repo/[^/]+/[^/]+/contributors$'
  '^GET:/github/repo/[^/]+/[^/]+/forks$'
  '^GET:/github/repo/[^/]+/[^/]+/languages$'
  '^GET:/github/repo/[^/]+/[^/]+/releases$'
  '^GET:/github/search/repositories$'
  '^GET:/github/search/users$'
  '^GET:/github/trending$'
  '^GET:/github/trending/developers$'
  '^GET:/github/user/[^/]+$'
  '^GET:/github/user/[^/]+/events$'
  '^GET:/github/user/[^/]+/followers$'
  '^GET:/github/user/[^/]+/following$'
  '^GET:/github/user/[^/]+/pinned$'
  '^GET:/github/user/[^/]+/repos$'
  '^GET:/gizmodo/article$'
  '^GET:/gizmodo/author$'
  '^GET:/gizmodo/headlines$'
  '^GET:/gizmodo/news$'
  '^GET:/gizmodo/sections$'
  '^GET:/globalnews/article$'
  '^GET:/globalnews/author$'
  '^GET:/globalnews/headlines$'
  '^GET:/globalnews/news$'
  '^GET:/globalnews/sections$'
  '^GET:/globeandmail/article$'
  '^GET:/globeandmail/author$'
  '^GET:/globeandmail/headlines$'
  '^GET:/globeandmail/news$'
  '^GET:/globeandmail/sections$'
  '^GET:/gmanews/article$'
  '^GET:/gmanews/headlines$'
  '^GET:/gmanews/news$'
  '^GET:/gmanews/sections$'
  '^GET:/goat/collection$'
  '^GET:/goat/countries$'
  '^GET:/goat/curated$'
  '^GET:/goat/listings/count$'
  '^GET:/goat/product/[^/]+$'
  '^GET:/goat/product/[^/]+/recommended$'
  '^GET:/goat/search$'
  '^GET:/goat/search/facets$'
  '^GET:/goat/searches/trending$'
  '^GET:/goat/suggest$'
  '^GET:/goldin/auctions$'
  '^GET:/goldin/categories$'
  '^GET:/goldin/listing$'
  '^GET:/goldin/search$'
  '^GET:/goldin/suggest$'
  '^GET:/goodreads/author/[^/]+$'
  '^GET:/goodreads/author/[^/]+/books$'
  '^GET:/goodreads/author/[^/]+/quotes$'
  '^GET:/goodreads/book/[^/]+$'
  '^GET:/goodreads/book/[^/]+/editions$'
  '^GET:/goodreads/book/[^/]+/reviews$'
  '^GET:/goodreads/genre/[^/]+$'
  '^GET:/goodreads/list/[^/]+$'
  '^GET:/goodreads/lists$'
  '^GET:/goodreads/search$'
  '^GET:/goodrx/answer$'
  '^GET:/goodrx/answers$'
  '^GET:/goodrx/brands$'
  '^GET:/goodrx/class$'
  '^GET:/goodrx/classes$'
  '^GET:/goodrx/comparison$'
  '^GET:/goodrx/comparisons$'
  '^GET:/goodrx/condition$'
  '^GET:/goodrx/condition-drugs$'
  '^GET:/goodrx/conditions$'
  '^GET:/goodrx/drug-guide$'
  '^GET:/goodrx/drug-guides$'
  '^GET:/goodrx/drug-info$'
  '^GET:/goodrx/drug-options$'
  '^GET:/goodrx/drug-prices$'
  '^GET:/goodrx/drugs$'
  '^GET:/goodrx/health-article$'
  '^GET:/goodrx/health-articles$'
  '^GET:/goodrx/health-topics$'
  '^GET:/goodrx/pet-medications$'
  '^GET:/google-jobs/job$'
  '^GET:/google-jobs/search$'
  '^GET:/google/finance/analyst-articles/[^/]+$'
  '^GET:/google/finance/chart/[^/]+$'
  '^GET:/google/finance/classification/[^/]+$'
  '^GET:/google/finance/company/[^/]+$'
  '^GET:/google/finance/context$'
  '^GET:/google/finance/financials/[^/]+$'
  '^GET:/google/finance/markets/categories/[^/]+/news$'
  '^GET:/google/finance/markets/categories/[^/]+/stocks$'
  '^GET:/google/finance/markets/earnings$'
  '^GET:/google/finance/markets/featured$'
  '^GET:/google/finance/markets/headline$'
  '^GET:/google/finance/markets/indices$'
  '^GET:/google/finance/markets/movers$'
  '^GET:/google/finance/markets/top$'
  '^GET:/google/finance/markets/trending$'
  '^GET:/google/finance/news/[^/]+$'
  '^GET:/google/finance/quote/[^/]+$'
  '^GET:/google/finance/related/[^/]+$'
  '^GET:/google/finance/search$'
  '^GET:/google/finance/ticker/[^/]+$'
  '^GET:/google/map/place/[^/]+$'
  '^GET:/google/map/place/[^/]+/photos$'
  '^GET:/google/map/place/[^/]+/reviews$'
  '^GET:/google/news$'
  '^GET:/google/suggest$'
  '^GET:/google/trends/categories$'
  '^GET:/google/trends/enums$'
  '^GET:/google/trends/locations$'
  '^GET:/google/trends/trending$'
  '^GET:/google/videos$'
  '^GET:/googlepatents/classification$'
  '^GET:/googlepatents/coverage$'
  '^GET:/googlepatents/detail$'
  '^GET:/googlepatents/recent$'
  '^GET:/googlepatents/search$'
  '^GET:/googlepatents/suggest$'
  '^GET:/googleplay/app$'
  '^GET:/googleplay/categories$'
  '^GET:/googleplay/datasafety$'
  '^GET:/googleplay/developer/[^/]+$'
  '^GET:/googleplay/list$'
  '^GET:/googleplay/permissions$'
  '^GET:/googleplay/ratings$'
  '^GET:/googleplay/reviews$'
  '^GET:/googleplay/search$'
  '^GET:/googleplay/similar$'
  '^GET:/googleplay/suggest/[^/]+$'
  '^GET:/gq/article$'
  '^GET:/gq/author$'
  '^GET:/gq/headlines$'
  '^GET:/gq/news$'
  '^GET:/gq/sections$'
  '^GET:/grailed/categories$'
  '^GET:/grailed/collection$'
  '^GET:/grailed/collections$'
  '^GET:/grailed/designers$'
  '^GET:/grailed/listing$'
  '^GET:/grailed/search$'
  '^GET:/grailed/seller$'
  '^GET:/grailed/seller-reviews$'
  '^GET:/grailed/similar-listings$'
  '^GET:/grailed/sold-listings$'
  '^GET:/grailed/suggest$'
  '^GET:/greystar/articles$'
  '^GET:/greystar/articles/[^/]+/[^/]+$'
  '^GET:/greystar/location$'
  '^GET:/greystar/locations$'
  '^GET:/greystar/markets$'
  '^GET:/greystar/newsroom$'
  '^GET:/greystar/newsroom/[^/]+$'
  '^GET:/greystar/properties/[^/]+$'
  '^GET:/greystar/search$'
  '^GET:/greystar/unit-locations$'
  '^GET:/greystar/units$'
  '^GET:/grubhub/availability$'
  '^GET:/grubhub/offers$'
  '^GET:/grubhub/restaurant$'
  '^GET:/grubhub/restaurant/menu$'
  '^GET:/grubhub/restaurant/reviews$'
  '^GET:/grubhub/search$'
  '^GET:/grubhub/timepicker$'
  '^GET:/guardian/article$'
  '^GET:/guardian/author$'
  '^GET:/guardian/headlines$'
  '^GET:/guardian/topic$'
  '^GET:/gucci/categories$'
  '^GET:/gucci/category$'
  '^GET:/gucci/product$'
  '^GET:/gucci/recommendations$'
  '^GET:/gucci/search$'
  '^GET:/gucci/size-guide$'
  '^GET:/gucci/store$'
  '^GET:/gucci/stores$'
  '^GET:/gucci/stores/search$'
  '^GET:/gucci/suggest$'
  '^GET:/gulfnews/article$'
  '^GET:/gulfnews/author$'
  '^GET:/gulfnews/headlines$'
  '^GET:/gulfnews/news$'
  '^GET:/gulfnews/sections$'
  '^GET:/gymshark/collections$'
  '^GET:/gymshark/collections/[^/]+/products$'
  '^GET:/gymshark/pages$'
  '^GET:/gymshark/pages/[^/]+$'
  '^GET:/gymshark/products$'
  '^GET:/gymshark/products/[^/]+$'
  '^GET:/gymshark/products/[^/]+/recommendations$'
  '^GET:/gymshark/sitemap/urls$'
  '^GET:/gymshark/sitemaps$'
  '^GET:/gymshark/store$'
  '^GET:/hbr/article$'
  '^GET:/hbr/categories$'
  '^GET:/hbr/headlines$'
  '^GET:/hbr/topic$'
  '^GET:/healthgrades/autocomplete$'
  '^GET:/healthgrades/facilities/filters$'
  '^GET:/healthgrades/facilities/search$'
  '^GET:/healthgrades/facility$'
  '^GET:/healthgrades/health-article$'
  '^GET:/healthgrades/health-articles$'
  '^GET:/healthgrades/health-topics$'
  '^GET:/healthgrades/hospital$'
  '^GET:/healthgrades/hospital-awards$'
  '^GET:/healthgrades/hospital-awards/filters$'
  '^GET:/healthgrades/locations$'
  '^GET:/healthgrades/physician$'
  '^GET:/healthgrades/physicians/filters$'
  '^GET:/healthgrades/physicians/search$'
  '^GET:/healthgrades/specialties$'
  '^GET:/healthgrades/top-searches$'
  '^GET:/hermes/categories$'
  '^GET:/hermes/category$'
  '^GET:/hermes/product$'
  '^GET:/hermes/product/recommendations$'
  '^GET:/hermes/products$'
  '^GET:/hermes/search$'
  '^GET:/hermes/stores$'
  '^GET:/hermes/suggest$'
  '^GET:/hindustantimes/article$'
  '^GET:/hindustantimes/author$'
  '^GET:/hindustantimes/headlines$'
  '^GET:/hindustantimes/news$'
  '^GET:/hindustantimes/sections$'
  '^GET:/hm/categories$'
  '^GET:/hm/listing$'
  '^GET:/hm/product/[^/]+$'
  '^GET:/hm/product/[^/]+/related$'
  '^GET:/hm/search$'
  '^GET:/hm/search/suggestions$'
  '^GET:/hm/stores$'
  '^GET:/hollywoodreporter/article$'
  '^GET:/hollywoodreporter/author$'
  '^GET:/hollywoodreporter/headlines$'
  '^GET:/hollywoodreporter/news$'
  '^GET:/hollywoodreporter/sections$'
  '^GET:/homedepot/categories$'
  '^GET:/homedepot/category$'
  '^GET:/homedepot/product/[^/]+$'
  '^GET:/homedepot/product/[^/]+/questions$'
  '^GET:/homedepot/search$'
  '^GET:/homedepot/suggest$'
  '^GET:/hotels/autocomplete$'
  '^GET:/houston-chronicle/article$'
  '^GET:/houston-chronicle/author$'
  '^GET:/houston-chronicle/headlines$'
  '^GET:/houston-chronicle/news$'
  '^GET:/houston-chronicle/sections$'
  '^GET:/howtogeek/news$'
  '^GET:/huffpost/article$'
  '^GET:/huffpost/author$'
  '^GET:/huffpost/headlines$'
  '^GET:/huffpost/news$'
  '^GET:/huffpost/sections$'
  '^GET:/ign/article$'
  '^GET:/ign/author$'
  '^GET:/ign/headlines$'
  '^GET:/ign/news$'
  '^GET:/ign/sections$'
  '^GET:/ikea/availability$'
  '^GET:/ikea/categories$'
  '^GET:/ikea/category$'
  '^GET:/ikea/product$'
  '^GET:/ikea/reviews$'
  '^GET:/ikea/search$'
  '^GET:/ikea/store$'
  '^GET:/ikea/stores$'
  '^GET:/ikea/suggest$'
  '^GET:/imdb/charts$'
  '^GET:/imdb/image-types$'
  '^GET:/imdb/name$'
  '^GET:/imdb/name/awards$'
  '^GET:/imdb/name/credits$'
  '^GET:/imdb/name/images$'
  '^GET:/imdb/name/videos$'
  '^GET:/imdb/search$'
  '^GET:/imdb/search/title$'
  '^GET:/imdb/title$'
  '^GET:/imdb/title/awards$'
  '^GET:/imdb/title/box-office$'
  '^GET:/imdb/title/company-credits$'
  '^GET:/imdb/title/connections$'
  '^GET:/imdb/title/credits$'
  '^GET:/imdb/title/episodes$'
  '^GET:/imdb/title/filming-locations$'
  '^GET:/imdb/title/goofs$'
  '^GET:/imdb/title/images$'
  '^GET:/imdb/title/keywords$'
  '^GET:/imdb/title/parental-guide$'
  '^GET:/imdb/title/public-facts-analysis$'
  '^GET:/imdb/title/quotes$'
  '^GET:/imdb/title/ratings$'
  '^GET:/imdb/title/release-info$'
  '^GET:/imdb/title/reviews$'
  '^GET:/imdb/title/similar$'
  '^GET:/imdb/title/technical-specs$'
  '^GET:/imdb/title/trivia$'
  '^GET:/imdb/title/videos$'
  '^GET:/importyeti/company$'
  '^GET:/importyeti/search$'
  '^GET:/indeed/job$'
  '^GET:/indeed/locations/suggest$'
  '^GET:/indeed/search$'
  '^GET:/independent/article$'
  '^GET:/independent/author$'
  '^GET:/independent/headlines$'
  '^GET:/independent/news$'
  '^GET:/independent/sections$'
  '^GET:/indianexpress/article$'
  '^GET:/indianexpress/author$'
  '^GET:/indianexpress/headlines$'
  '^GET:/indianexpress/news$'
  '^GET:/indianexpress/sections$'
  '^GET:/indiatoday/article$'
  '^GET:/indiatoday/author$'
  '^GET:/indiatoday/headlines$'
  '^GET:/indiatoday/news$'
  '^GET:/indiatoday/sections$'
  '^GET:/indiewire/article$'
  '^GET:/indiewire/author$'
  '^GET:/indiewire/headlines$'
  '^GET:/indiewire/news$'
  '^GET:/indiewire/sections$'
  '^GET:/inews/article$'
  '^GET:/inews/author$'
  '^GET:/inews/headlines$'
  '^GET:/inews/news$'
  '^GET:/inews/sections$'
  '^GET:/inquirer/article$'
  '^GET:/inquirer/author$'
  '^GET:/inquirer/headlines$'
  '^GET:/inquirer/news$'
  '^GET:/inquirer/sections$'
  '^GET:/instacart/departments$'
  '^GET:/instacart/item$'
  '^GET:/instacart/search$'
  '^GET:/instacart/search-nearby$'
  '^GET:/instacart/stores$'
  '^GET:/instacart/trending$'
  '^GET:/instagram/post/[^/]+/[^/]+$'
  '^GET:/instagram/profile/[^/]+$'
  '^GET:/instagram/reels/[^/]+$'
  '^GET:/investopedia/article$'
  '^GET:/investopedia/author$'
  '^GET:/investopedia/headlines$'
  '^GET:/investopedia/news$'
  '^GET:/investopedia/sections$'
  '^GET:/iol/article$'
  '^GET:/iol/author$'
  '^GET:/iol/headlines$'
  '^GET:/iol/news$'
  '^GET:/iol/sections$'
  '^GET:/irishindependent/article$'
  '^GET:/irishindependent/author$'
  '^GET:/irishindependent/headlines$'
  '^GET:/irishindependent/news$'
  '^GET:/irishindependent/sections$'
  '^GET:/irishtimes/article$'
  '^GET:/irishtimes/author$'
  '^GET:/irishtimes/headlines$'
  '^GET:/irishtimes/news$'
  '^GET:/irishtimes/sections$'
  '^GET:/japantimes/article$'
  '^GET:/japantimes/author$'
  '^GET:/japantimes/headlines$'
  '^GET:/japantimes/news$'
  '^GET:/japantimes/sections$'
  '^GET:/jcrew/categories$'
  '^GET:/jcrew/category$'
  '^GET:/jcrew/product$'
  '^GET:/jcrew/product/reviews$'
  '^GET:/jcrew/search$'
  '^GET:/jcrew/size-chart$'
  '^GET:/jcrew/stores$'
  '^GET:/jcrew/suggest$'
  '^GET:/jerusalempost/article$'
  '^GET:/jerusalempost/author$'
  '^GET:/jerusalempost/authors$'
  '^GET:/jerusalempost/headlines$'
  '^GET:/jerusalempost/news$'
  '^GET:/jerusalempost/sections$'
  '^GET:/jimmy-johns/menu$'
  '^GET:/jimmy-johns/modifiers$'
  '^GET:/jimmy-johns/nearby$'
  '^GET:/jimmy-johns/sitemap$'
  '^GET:/jimmy-johns/store$'
  '^GET:/jobs/ashby/board$'
  '^GET:/jobs/company-search$'
  '^GET:/jobs/eightfold/board$'
  '^GET:/jobs/eightfold/job$'
  '^GET:/jobs/gem/board$'
  '^GET:/jobs/greenhouse/board$'
  '^GET:/jobs/greenhouse/job$'
  '^GET:/jobs/hiring-signals$'
  '^GET:/jobs/icims/board$'
  '^GET:/jobs/icims/job$'
  '^GET:/jobs/lever/posting$'
  '^GET:/jobs/lever/postings$'
  '^GET:/jobs/oracle/board$'
  '^GET:/jobs/oracle/job$'
  '^GET:/jobs/personio/feed$'
  '^GET:/jobs/phenom/board$'
  '^GET:/jobs/phenom/job$'
  '^GET:/jobs/pinpoint/board$'
  '^GET:/jobs/recruitee/offer$'
  '^GET:/jobs/recruitee/offers$'
  '^GET:/jobs/rippling/board$'
  '^GET:/jobs/rippling/job$'
  '^GET:/jobs/smartrecruiters/posting$'
  '^GET:/jobs/smartrecruiters/postings$'
  '^GET:/jobs/teamtailor/jobs$'
  '^GET:/jobs/ukg/board$'
  '^GET:/jobs/workable/posting$'
  '^GET:/jobs/workable/postings$'
  '^GET:/jobs/workday/board$'
  '^GET:/jobs/workday/job$'
  '^GET:/justeat/restaurant$'
  '^GET:/justeat/restaurant/menu$'
  '^GET:/justeat/search$'
  '^GET:/justeat/search/filters$'
  '^GET:/justwatch/age-certifications$'
  '^GET:/justwatch/discover$'
  '^GET:/justwatch/episode/by-id$'
  '^GET:/justwatch/episode/offers$'
  '^GET:/justwatch/genre/titles$'
  '^GET:/justwatch/genres$'
  '^GET:/justwatch/monetization/titles$'
  '^GET:/justwatch/new$'
  '^GET:/justwatch/popular$'
  '^GET:/justwatch/provider/titles$'
  '^GET:/justwatch/providers$'
  '^GET:/justwatch/search$'
  '^GET:/justwatch/season/by-id$'
  '^GET:/justwatch/season/episodes$'
  '^GET:/justwatch/show/seasons$'
  '^GET:/justwatch/title$'
  '^GET:/justwatch/title/analysis$'
  '^GET:/justwatch/title/by-id$'
  '^GET:/justwatch/title/media$'
  '^GET:/justwatch/title/offers$'
  '^GET:/justwatch/title/similar$'
  '^GET:/kalshi/event/[^/]+$'
  '^GET:/kalshi/event/[^/]+/history$'
  '^GET:/kalshi/event/[^/]+/metadata$'
  '^GET:/kalshi/events$'
  '^GET:/kalshi/events/multivariate$'
  '^GET:/kalshi/exchange/schedule$'
  '^GET:/kalshi/exchange/status$'
  '^GET:/kalshi/historical/cutoff$'
  '^GET:/kalshi/historical/market/[^/]+$'
  '^GET:/kalshi/historical/market/[^/]+/history$'
  '^GET:/kalshi/historical/markets$'
  '^GET:/kalshi/historical/trades$'
  '^GET:/kalshi/market/[^/]+$'
  '^GET:/kalshi/market/[^/]+/history$'
  '^GET:/kalshi/market/[^/]+/orderbook$'
  '^GET:/kalshi/markets$'
  '^GET:/kalshi/markets/history$'
  '^GET:/kalshi/markets/orderbooks$'
  '^GET:/kalshi/series$'
  '^GET:/kalshi/series/[^/]+$'
  '^GET:/kalshi/trades$'
  '^GET:/kfc/delivery-estimate$'
  '^GET:/kfc/menu$'
  '^GET:/kfc/nearby$'
  '^GET:/kfc/promotion$'
  '^GET:/kfc/promotions$'
  '^GET:/kfc/store$'
  '^GET:/kfc/stores$'
  '^GET:/khaleejtimes/article$'
  '^GET:/khaleejtimes/author$'
  '^GET:/khaleejtimes/headlines$'
  '^GET:/khaleejtimes/news$'
  '^GET:/khaleejtimes/sections$'
  '^GET:/kickstarter/comments$'
  '^GET:/kickstarter/discover$'
  '^GET:/kickstarter/project$'
  '^GET:/kickstarter/updates$'
  '^GET:/kohls/category$'
  '^GET:/kohls/product/reviews$'
  '^GET:/kohls/stores$'
  '^GET:/kohls/suggest$'
  '^GET:/kotaku/article$'
  '^GET:/kotaku/author$'
  '^GET:/kotaku/headlines$'
  '^GET:/kotaku/news$'
  '^GET:/kotaku/sections$'
  '^GET:/kroger/categories$'
  '^GET:/kroger/category$'
  '^GET:/kroger/coupons$'
  '^GET:/kroger/product$'
  '^GET:/kroger/product/reviews$'
  '^GET:/kroger/products$'
  '^GET:/kroger/related-tags$'
  '^GET:/kroger/search$'
  '^GET:/kroger/store$'
  '^GET:/kroger/suggest$'
  '^GET:/kyliecosmetics/collections$'
  '^GET:/kyliecosmetics/collections/[^/]+/products$'
  '^GET:/kyliecosmetics/pages$'
  '^GET:/kyliecosmetics/pages/[^/]+$'
  '^GET:/kyliecosmetics/products$'
  '^GET:/kyliecosmetics/products/[^/]+$'
  '^GET:/kyliecosmetics/products/[^/]+/recommendations$'
  '^GET:/kyliecosmetics/search/suggest$'
  '^GET:/kyliecosmetics/sitemap/urls$'
  '^GET:/kyliecosmetics/sitemaps$'
  '^GET:/kyliecosmetics/store$'
  '^GET:/latimes/article$'
  '^GET:/latimes/author$'
  '^GET:/latimes/headlines$'
  '^GET:/latimes/sections$'
  '^GET:/lazada/categories$'
  '^GET:/lazada/category-products$'
  '^GET:/lazada/home$'
  '^GET:/lazada/product$'
  '^GET:/lazada/search$'
  '^GET:/leboncoin/listing$'
  '^GET:/leboncoin/search$'
  '^GET:/letterboxd/film/[^/]+$'
  '^GET:/letterboxd/film/[^/]+/rating-histogram$'
  '^GET:/letterboxd/film/[^/]+/reviews$'
  '^GET:/letterboxd/film/[^/]+/similar$'
  '^GET:/letterboxd/member/[^/]+$'
  '^GET:/letterboxd/person/[^/]+$'
  '^GET:/letterboxd/popular$'
  '^GET:/letterboxd/search$'
  '^GET:/linkedin/company/[^/]+$'
  '^GET:/linkedin/product/[^/]+$'
  '^GET:/linkedin/product/categories$'
  '^GET:/linkedin/products/search$'
  '^GET:/linkedin/showcase/[^/]+$'
  '^GET:/livemint/article$'
  '^GET:/livemint/author$'
  '^GET:/livemint/headlines$'
  '^GET:/livemint/news$'
  '^GET:/livemint/sections$'
  '^GET:/liverpoolecho/article$'
  '^GET:/liverpoolecho/author$'
  '^GET:/liverpoolecho/headlines$'
  '^GET:/liverpoolecho/news$'
  '^GET:/liverpoolecho/sections$'
  '^GET:/livescience/article$'
  '^GET:/livescience/author$'
  '^GET:/livescience/headlines$'
  '^GET:/livescience/news$'
  '^GET:/livescience/sections$'
  '^GET:/livescore/competition$'
  '^GET:/livescore/competitions$'
  '^GET:/livescore/live-scores$'
  '^GET:/livescore/match$'
  '^GET:/livescore/match-stats$'
  '^GET:/livescore/news$'
  '^GET:/livescore/news-article$'
  '^GET:/livescore/news-categories$'
  '^GET:/livescore/news-feed$'
  '^GET:/livescore/news-publishers$'
  '^GET:/livescore/player$'
  '^GET:/livescore/scores$'
  '^GET:/livescore/scores-toc$'
  '^GET:/livescore/search$'
  '^GET:/livescore/sports$'
  '^GET:/livescore/team$'
  '^GET:/lululemon/categories$'
  '^GET:/lululemon/category$'
  '^GET:/lululemon/outfit$'
  '^GET:/lululemon/product/[^/]+$'
  '^GET:/lululemon/stores$'
  '^GET:/macrumors/article$'
  '^GET:/macrumors/author$'
  '^GET:/macrumors/headlines$'
  '^GET:/macrumors/news$'
  '^GET:/macrumors/sections$'
  '^GET:/macys/product/[^/]+$'
  '^GET:/macys/product/reviews$'
  '^GET:/macys/suggest$'
  '^GET:/makeuseof/article$'
  '^GET:/makeuseof/author$'
  '^GET:/makeuseof/headlines$'
  '^GET:/makeuseof/news$'
  '^GET:/makeuseof/sections$'
  '^GET:/malaymail/article$'
  '^GET:/malaymail/headlines$'
  '^GET:/malaymail/news$'
  '^GET:/malaymail/sections$'
  '^GET:/manga/rankings$'
  '^GET:/manga/search$'
  '^GET:/manga/title/[^/]+$'
  '^GET:/manga/title/[^/]+/characters$'
  '^GET:/manga/title/[^/]+/recommendations$'
  '^GET:/manga/title/[^/]+/staff$'
  '^GET:/marketwatch/article$'
  '^GET:/marketwatch/author$'
  '^GET:/marketwatch/headlines$'
  '^GET:/marketwatch/news$'
  '^GET:/marketwatch/sections$'
  '^GET:/mashable/article$'
  '^GET:/mashable/author$'
  '^GET:/mashable/headlines$'
  '^GET:/mashable/news$'
  '^GET:/mashable/sections$'
  '^GET:/mcdonalds/categories$'
  '^GET:/mcdonalds/item$'
  '^GET:/mcdonalds/item-list$'
  '^GET:/mcdonalds/menu$'
  '^GET:/mcdonalds/restaurant-menu$'
  '^GET:/mcdonalds/restaurants$'
  '^GET:/mediaite/article$'
  '^GET:/mediaite/author$'
  '^GET:/mediaite/headlines$'
  '^GET:/mediaite/news$'
  '^GET:/mediaite/sections$'
  '^GET:/medicalnewstoday/article$'
  '^GET:/medicalnewstoday/author$'
  '^GET:/medicalnewstoday/headlines$'
  '^GET:/medicalnewstoday/news$'
  '^GET:/medicalnewstoday/sections$'
  '^GET:/men/article$'
  '^GET:/men/author$'
  '^GET:/men/headlines$'
  '^GET:/men/news$'
  '^GET:/men/sections$'
  '^GET:/mercari/autocomplete$'
  '^GET:/mercari/home$'
  '^GET:/mercari/item/[^/]+$'
  '^GET:/mercari/master$'
  '^GET:/mercari/search$'
  '^GET:/meta-jobs/job$'
  '^GET:/meta-jobs/list$'
  '^GET:/meta-jobs/search$'
  '^GET:/metacritic/browse$'
  '^GET:/metacritic/game/[^/]+$'
  '^GET:/metacritic/game/[^/]+/critic-reviews$'
  '^GET:/metacritic/game/[^/]+/user-reviews$'
  '^GET:/metacritic/movie/[^/]+$'
  '^GET:/metacritic/movie/[^/]+/critic-reviews$'
  '^GET:/metacritic/movie/[^/]+/user-reviews$'
  '^GET:/metacritic/tv/[^/]+$'
  '^GET:/metacritic/tv/[^/]+/critic-reviews$'
  '^GET:/metacritic/tv/[^/]+/user-reviews$'
  '^GET:/metaculus/category/[^/]+/questions$'
  '^GET:/metaculus/comments-feed$'
  '^GET:/metaculus/project/[^/]+/questions$'
  '^GET:/metaculus/question/[^/]+$'
  '^GET:/metaculus/question/[^/]+/forecast-history$'
  '^GET:/metaculus/question/[^/]+/forecasts$'
  '^GET:/metaculus/question/[^/]+/metadata$'
  '^GET:/metaculus/question/[^/]+/options$'
  '^GET:/metaculus/questions$'
  '^GET:/metaculus/top-comments$'
  '^GET:/metaculus/tournament/[^/]+/questions$'
  '^GET:/metro/article$'
  '^GET:/metro/author$'
  '^GET:/metro/headlines$'
  '^GET:/metro/news$'
  '^GET:/metro/sections$'
  '^GET:/microsoftstore/categories$'
  '^GET:/microsoftstore/category$'
  '^GET:/microsoftstore/charts$'
  '^GET:/microsoftstore/editorial$'
  '^GET:/microsoftstore/events$'
  '^GET:/microsoftstore/product$'
  '^GET:/microsoftstore/publisher$'
  '^GET:/microsoftstore/recommended$'
  '^GET:/microsoftstore/related$'
  '^GET:/microsoftstore/reviews$'
  '^GET:/microsoftstore/reviews/summary$'
  '^GET:/microsoftstore/search$'
  '^GET:/microsoftstore/spotlight$'
  '^GET:/microsoftstore/suggest$'
  '^GET:/mirror/article$'
  '^GET:/mirror/author$'
  '^GET:/mirror/headlines$'
  '^GET:/mirror/news$'
  '^GET:/mirror/sections$'
  '^GET:/mlb/discovery$'
  '^GET:/mlb/editorial-feed$'
  '^GET:/mlb/game$'
  '^GET:/mlb/game-boxscore$'
  '^GET:/mlb/game-play-by-play$'
  '^GET:/mlb/league-leaders$'
  '^GET:/mlb/league-stats$'
  '^GET:/mlb/player$'
  '^GET:/mlb/player-stats$'
  '^GET:/mlb/prospect-rankings$'
  '^GET:/mlb/prospect-stats$'
  '^GET:/mlb/schedule$'
  '^GET:/mlb/search$'
  '^GET:/mlb/standings$'
  '^GET:/mlb/statcast-abs-challenges$'
  '^GET:/mlb/statcast-active-spin$'
  '^GET:/mlb/statcast-arm-angle$'
  '^GET:/mlb/statcast-arm-strength$'
  '^GET:/mlb/statcast-arm-strength-player$'
  '^GET:/mlb/statcast-arm-value$'
  '^GET:/mlb/statcast-arm-value-details$'
  '^GET:/mlb/statcast-baserunning$'
  '^GET:/mlb/statcast-bat-tracking$'
  '^GET:/mlb/statcast-batted-ball$'
  '^GET:/mlb/statcast-birthday-index$'
  '^GET:/mlb/statcast-catcher-blocking$'
  '^GET:/mlb/statcast-catcher-blocking-details$'
  '^GET:/mlb/statcast-catcher-framing$'
  '^GET:/mlb/statcast-catcher-framing-details$'
  '^GET:/mlb/statcast-catcher-pop-time$'
  '^GET:/mlb/statcast-catcher-stance$'
  '^GET:/mlb/statcast-catcher-throwing$'
  '^GET:/mlb/statcast-catcher-throwing-details$'
  '^GET:/mlb/statcast-expected$'
  '^GET:/mlb/statcast-fielding-run-value$'
  '^GET:/mlb/statcast-first-base-receiving$'
  '^GET:/mlb/statcast-first-base-receiving-details$'
  '^GET:/mlb/statcast-home-runs$'
  '^GET:/mlb/statcast-home-runs-details$'
  '^GET:/mlb/statcast-leaders$'
  '^GET:/mlb/statcast-oaa$'
  '^GET:/mlb/statcast-park-factors$'
  '^GET:/mlb/statcast-percentile$'
  '^GET:/mlb/statcast-pitch-arsenal$'
  '^GET:/mlb/statcast-pitch-arsenal-details$'
  '^GET:/mlb/statcast-pitch-arsenals$'
  '^GET:/mlb/statcast-pitch-movement$'
  '^GET:/mlb/statcast-pitch-tempo$'
  '^GET:/mlb/statcast-pitch-tempo-player$'
  '^GET:/mlb/statcast-pitch-timer$'
  '^GET:/mlb/statcast-player-details$'
  '^GET:/mlb/statcast-rolling$'
  '^GET:/mlb/statcast-run-value$'
  '^GET:/mlb/statcast-running-game$'
  '^GET:/mlb/statcast-running-game-details$'
  '^GET:/mlb/statcast-sprint-speed$'
  '^GET:/mlb/statcast-sprint-speed-teams$'
  '^GET:/mlb/statcast-swing-path$'
  '^GET:/mlb/statcast-swing-timing$'
  '^GET:/mlb/statcast-swing-timing-details$'
  '^GET:/mlb/statcast-top-performers$'
  '^GET:/mlb/statcast-year-to-year$'
  '^GET:/mlb/team-roster$'
  '^GET:/mlb/team-stats$'
  '^GET:/mlb/teams$'
  '^GET:/mlb/transactions$'
  '^GET:/mlive/news$'
  '^GET:/modaoperandi/categories$'
  '^GET:/modaoperandi/designers$'
  '^GET:/modaoperandi/product$'
  '^GET:/modaoperandi/search$'
  '^GET:/moncler/categories$'
  '^GET:/moncler/category$'
  '^GET:/moncler/product$'
  '^GET:/moncler/search$'
  '^GET:/moncler/stores$'
  '^GET:/moncler/suggest$'
  '^GET:/moneycontrol/article$'
  '^GET:/moneycontrol/author$'
  '^GET:/moneycontrol/headlines$'
  '^GET:/moneycontrol/news$'
  '^GET:/moneycontrol/sections$'
  '^GET:/motleyfool/article$'
  '^GET:/motleyfool/author$'
  '^GET:/motleyfool/headlines$'
  '^GET:/motleyfool/news$'
  '^GET:/motleyfool/sections$'
  '^GET:/nationafrica/article$'
  '^GET:/nationafrica/author$'
  '^GET:/nationafrica/headlines$'
  '^GET:/nationafrica/news$'
  '^GET:/nationafrica/sections$'
  '^GET:/national/article$'
  '^GET:/national/author$'
  '^GET:/national/headlines$'
  '^GET:/national/news$'
  '^GET:/national/sections$'
  '^GET:/nationalpost/article$'
  '^GET:/nationalpost/author$'
  '^GET:/nationalpost/headlines$'
  '^GET:/nationalpost/news$'
  '^GET:/nationalpost/sections$'
  '^GET:/nbc/article$'
  '^GET:/nbc/author$'
  '^GET:/nbc/headlines$'
  '^GET:/nbc/news$'
  '^GET:/nbc/sections$'
  '^GET:/ndtv/article$'
  '^GET:/ndtv/author$'
  '^GET:/ndtv/headlines$'
  '^GET:/ndtv/latest-videos$'
  '^GET:/ndtv/live-blog$'
  '^GET:/ndtv/live-blogs$'
  '^GET:/ndtv/news$'
  '^GET:/ndtv/search$'
  '^GET:/ndtv/sections$'
  '^GET:/ndtv/video$'
  '^GET:/ndtv/video-categories$'
  '^GET:/ndtv/videos$'
  '^GET:/news18/article$'
  '^GET:/news18/author$'
  '^GET:/news18/headlines$'
  '^GET:/news18/news$'
  '^GET:/news18/sections$'
  '^GET:/news24/article$'
  '^GET:/news24/headlines$'
  '^GET:/news24/news$'
  '^GET:/news24/sections$'
  '^GET:/newscomau/article$'
  '^GET:/newscomau/author$'
  '^GET:/newscomau/headlines$'
  '^GET:/newscomau/news$'
  '^GET:/newscomau/sections$'
  '^GET:/newsmax/article$'
  '^GET:/newsmax/author$'
  '^GET:/newsmax/headlines$'
  '^GET:/newsmax/news$'
  '^GET:/newsmax/sections$'
  '^GET:/newsweek/article$'
  '^GET:/newsweek/author$'
  '^GET:/newsweek/headlines$'
  '^GET:/newsweek/news$'
  '^GET:/newsweek/sections$'
  '^GET:/newyorker/article$'
  '^GET:/newyorker/author$'
  '^GET:/newyorker/headlines$'
  '^GET:/newyorker/news$'
  '^GET:/newyorker/sections$'
  '^GET:/nike/categories$'
  '^GET:/nike/product$'
  '^GET:/nike/product/availability$'
  '^GET:/nike/product/details$'
  '^GET:/nike/product/recommendations$'
  '^GET:/nike/product/reviews$'
  '^GET:/nike/search$'
  '^GET:/nike/stores$'
  '^GET:/nike/suggest$'
  '^GET:/ninetofivegoogle/article$'
  '^GET:/ninetofivegoogle/author$'
  '^GET:/ninetofivegoogle/headlines$'
  '^GET:/ninetofivegoogle/news$'
  '^GET:/ninetofivegoogle/sections$'
  '^GET:/ninetofivemac/article$'
  '^GET:/ninetofivemac/author$'
  '^GET:/ninetofivemac/headlines$'
  '^GET:/ninetofivemac/news$'
  '^GET:/ninetofivemac/sections$'
  '^GET:/njcom/news$'
  '^GET:/npr/article$'
  '^GET:/npr/author$'
  '^GET:/npr/categories$'
  '^GET:/npr/headlines$'
  '^GET:/npr/topic$'
  '^GET:/numbeo/cost-of-living/city/[^/]+$'
  '^GET:/numbeo/cost-of-living/country$'
  '^GET:/numbeo/cost-of-living/rankings$'
  '^GET:/numbeo/cost-of-living/rankings-by-country$'
  '^GET:/numbeo/indices/city/[^/]+$'
  '^GET:/numbeo/indices/country$'
  '^GET:/numbeo/indices/rankings$'
  '^GET:/numbeo/indices/rankings-by-country$'
  '^GET:/nydailynews/article$'
  '^GET:/nydailynews/author$'
  '^GET:/nydailynews/headlines$'
  '^GET:/nydailynews/news$'
  '^GET:/nydailynews/sections$'
  '^GET:/nymag/article$'
  '^GET:/nymag/author$'
  '^GET:/nymag/headlines$'
  '^GET:/nymag/news$'
  '^GET:/nymag/sections$'
  '^GET:/nypost/article$'
  '^GET:/nypost/author$'
  '^GET:/nypost/headlines$'
  '^GET:/nypost/news$'
  '^GET:/nypost/sections$'
  '^GET:/nyt/article$'
  '^GET:/nyt/author$'
  '^GET:/nyt/categories$'
  '^GET:/nyt/headlines$'
  '^GET:/nyt/sections$'
  '^GET:/nzherald/article$'
  '^GET:/nzherald/author$'
  '^GET:/nzherald/headlines$'
  '^GET:/nzherald/news$'
  '^GET:/nzherald/sections$'
  '^GET:/ohpolly/collections$'
  '^GET:/ohpolly/collections/[^/]+/products$'
  '^GET:/ohpolly/pages$'
  '^GET:/ohpolly/pages/[^/]+$'
  '^GET:/ohpolly/products$'
  '^GET:/ohpolly/products/[^/]+$'
  '^GET:/ohpolly/products/[^/]+/recommendations$'
  '^GET:/ohpolly/search/suggest$'
  '^GET:/ohpolly/sitemap/urls$'
  '^GET:/ohpolly/sitemaps$'
  '^GET:/ohpolly/store$'
  '^GET:/oldnavy/categories$'
  '^GET:/oldnavy/category$'
  '^GET:/oldnavy/product$'
  '^GET:/oldnavy/product/availability$'
  '^GET:/oldnavy/product/reviews$'
  '^GET:/oldnavy/search$'
  '^GET:/oldnavy/stores$'
  '^GET:/opensea/activity$'
  '^GET:/opensea/categories$'
  '^GET:/opensea/chains$'
  '^GET:/opensea/collection/[^/]+$'
  '^GET:/opensea/collection/[^/]+/activity$'
  '^GET:/opensea/collection/[^/]+/best-deals$'
  '^GET:/opensea/collection/[^/]+/chart$'
  '^GET:/opensea/collection/[^/]+/depth$'
  '^GET:/opensea/collection/[^/]+/holders$'
  '^GET:/opensea/collection/[^/]+/items$'
  '^GET:/opensea/collection/[^/]+/offers$'
  '^GET:/opensea/collection/[^/]+/rarest-items$'
  '^GET:/opensea/collection/[^/]+/search-items$'
  '^GET:/opensea/collection/[^/]+/social-proof$'
  '^GET:/opensea/collection/[^/]+/top-sales$'
  '^GET:/opensea/collection/[^/]+/trait-offers$'
  '^GET:/opensea/collection/[^/]+/traits$'
  '^GET:/opensea/collections$'
  '^GET:/opensea/drops$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/activity$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/chart$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/depth$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/listings$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/offers$'
  '^GET:/opensea/item/[^/]+/[^/]+/[^/]+/owners$'
  '^GET:/opensea/most-watched$'
  '^GET:/opensea/profile/[^/]+$'
  '^GET:/opensea/profile/[^/]+/activity$'
  '^GET:/opensea/profile/[^/]+/collections$'
  '^GET:/opensea/profile/[^/]+/created$'
  '^GET:/opensea/profile/[^/]+/items$'
  '^GET:/opensea/profile/[^/]+/search-items$'
  '^GET:/opensea/rankings$'
  '^GET:/opensea/search/collections$'
  '^GET:/opensea/top-movers$'
  '^GET:/opentable/restaurant$'
  '^GET:/opentable/restaurant/menus$'
  '^GET:/opentable/restaurant/reviews$'
  '^GET:/opentable/search$'
  '^GET:/otto/categories$'
  '^GET:/otto/product$'
  '^GET:/otto/search$'
  '^GET:/pagesix/article$'
  '^GET:/pagesix/author$'
  '^GET:/pagesix/headlines$'
  '^GET:/pagesix/news$'
  '^GET:/pagesix/sections$'
  '^GET:/pandamart/search$'
  '^GET:/pandamart/store$'
  '^GET:/pandamart/store/categories$'
  '^GET:/pandamart/store/product$'
  '^GET:/pandamart/store/products$'
  '^GET:/pandamart/store/search$'
  '^GET:/panera/at-work-locations$'
  '^GET:/panera/cafe$'
  '^GET:/panera/catering-delivery-info$'
  '^GET:/panera/catering-menu$'
  '^GET:/panera/geocode$'
  '^GET:/panera/item-detail$'
  '^GET:/panera/item-options$'
  '^GET:/panera/locations$'
  '^GET:/panera/menu$'
  '^GET:/panera/quantity-rules$'
  '^GET:/panera/retired-products$'
  '^GET:/panera/time-slots$'
  '^GET:/panera/upsell-suggestions$'
  '^GET:/papajohns/allergens$'
  '^GET:/papajohns/colombia/menu$'
  '^GET:/papajohns/deals$'
  '^GET:/papajohns/directory$'
  '^GET:/papajohns/elsalvador/menu$'
  '^GET:/papajohns/india/deal$'
  '^GET:/papajohns/india/menu$'
  '^GET:/papajohns/india/menu/item$'
  '^GET:/papajohns/india/stores$'
  '^GET:/papajohns/intl/deals$'
  '^GET:/papajohns/intl/ingredients$'
  '^GET:/papajohns/intl/menu$'
  '^GET:/papajohns/intl/offer$'
  '^GET:/papajohns/intl/product$'
  '^GET:/papajohns/intl/stores$'
  '^GET:/papajohns/menu$'
  '^GET:/papajohns/menu/item$'
  '^GET:/papajohns/nearby$'
  '^GET:/papajohns/nutrition$'
  '^GET:/papajohns/peru/menu$'
  '^GET:/papajohns/poland/menu$'
  '^GET:/papajohns/russia/menu$'
  '^GET:/papajohns/store$'
  '^GET:/patreon/creator$'
  '^GET:/patreon/creator/tiers$'
  '^GET:/patreon/explore$'
  '^GET:/patreon/rss$'
  '^GET:/pcgamer/article$'
  '^GET:/pcgamer/author$'
  '^GET:/pcgamer/headlines$'
  '^GET:/pcgamer/news$'
  '^GET:/pcgamer/sections$'
  '^GET:/pcmag/article$'
  '^GET:/pcmag/author$'
  '^GET:/pcmag/headlines$'
  '^GET:/pcmag/news$'
  '^GET:/pcmag/sections$'
  '^GET:/people/article$'
  '^GET:/people/author$'
  '^GET:/people/headlines$'
  '^GET:/people/news$'
  '^GET:/people/sections$'
  '^GET:/phillyinquirer/article$'
  '^GET:/phillyinquirer/author$'
  '^GET:/phillyinquirer/headlines$'
  '^GET:/phillyinquirer/news$'
  '^GET:/phillyinquirer/sections$'
  '^GET:/philstar/article$'
  '^GET:/philstar/author$'
  '^GET:/philstar/headlines$'
  '^GET:/philstar/news$'
  '^GET:/philstar/sections$'
  '^GET:/phonearena/article$'
  '^GET:/phonearena/author$'
  '^GET:/phonearena/headlines$'
  '^GET:/phonearena/news$'
  '^GET:/phonearena/sections$'
  '^GET:/physorg/article$'
  '^GET:/physorg/headlines$'
  '^GET:/physorg/news$'
  '^GET:/physorg/sections$'
  '^GET:/pinterest/board/[^/]+/[^/]+$'
  '^GET:/pinterest/categories$'
  '^GET:/pinterest/ideas/[^/]+$'
  '^GET:/pinterest/pin/[^/]+$'
  '^GET:/pinterest/search$'
  '^GET:/pinterest/user/[^/]+$'
  '^GET:/pinterest/user/[^/]+/boards$'
  '^GET:/pinterest/user/[^/]+/pins$'
  '^GET:/pitchbook/advisor$'
  '^GET:/pitchbook/company$'
  '^GET:/pitchbook/fund$'
  '^GET:/pitchbook/investor$'
  '^GET:/pitchbook/limited-partner$'
  '^GET:/pizzahut/bundle-choices$'
  '^GET:/pizzahut/delivery-estimate$'
  '^GET:/pizzahut/menu$'
  '^GET:/pizzahut/modifiers$'
  '^GET:/pizzahut/store$'
  '^GET:/pizzahut/stores$'
  '^GET:/playstation/browse$'
  '^GET:/playstation/category$'
  '^GET:/playstation/concept$'
  '^GET:/playstation/concept/reviews$'
  '^GET:/playstation/deals$'
  '^GET:/playstation/latest$'
  '^GET:/playstation/page$'
  '^GET:/playstation/product$'
  '^GET:/playstation/search$'
  '^GET:/playstation/suggest$'
  '^GET:/politico/article$'
  '^GET:/politico/author$'
  '^GET:/politico/categories$'
  '^GET:/politico/headlines$'
  '^GET:/politico/topic$'
  '^GET:/polygon/article$'
  '^GET:/polygon/author$'
  '^GET:/polygon/headlines$'
  '^GET:/polygon/news$'
  '^GET:/polygon/sections$'
  '^GET:/polymarket/activity/trades$'
  '^GET:/polymarket/clob/market/[^/]+$'
  '^GET:/polymarket/dashboards/macro$'
  '^GET:/polymarket/event/[^/]+$'
  '^GET:/polymarket/events$'
  '^GET:/polymarket/events/[^/]+/tags$'
  '^GET:/polymarket/events/similar$'
  '^GET:/polymarket/fee-types$'
  '^GET:/polymarket/homepage/feed$'
  '^GET:/polymarket/leaderboard$'
  '^GET:/polymarket/market/[^/]+$'
  '^GET:/polymarket/market/[^/]+/liquidity$'
  '^GET:/polymarket/market/[^/]+/tags$'
  '^GET:/polymarket/markets$'
  '^GET:/polymarket/predictions$'
  '^GET:/polymarket/rewards/market/[^/]+$'
  '^GET:/polymarket/rewards/markets$'
  '^GET:/polymarket/search$'
  '^GET:/polymarket/tag/[^/]+$'
  '^GET:/polymarket/tag/[^/]+/related-tags$'
  '^GET:/polymarket/tags$'
  '^GET:/polymarket/token/[^/]+/midpoint$'
  '^GET:/polymarket/token/[^/]+/orderbook$'
  '^GET:/polymarket/token/[^/]+/price$'
  '^GET:/polymarket/token/[^/]+/price-history$'
  '^GET:/polymarket/token/[^/]+/spread$'
  '^GET:/popeyes/faq$'
  '^GET:/popeyes/location$'
  '^GET:/popeyes/locations$'
  '^GET:/popeyes/menu$'
  '^GET:/popeyes/offers$'
  '^GET:/popeyes/promotions$'
  '^GET:/popeyes/quests$'
  '^GET:/popeyes/rewards$'
  '^GET:/popularmechanics/news$'
  '^GET:/poshmark/brand/[^/]+$'
  '^GET:/poshmark/brands$'
  '^GET:/poshmark/categories$'
  '^GET:/poshmark/category/[^/]+$'
  '^GET:/poshmark/closet/[^/]+$'
  '^GET:/poshmark/listing/[^/]+$'
  '^GET:/poshmark/search$'
  '^GET:/poshmark/trend/[^/]+$'
  '^GET:/prada/categories$'
  '^GET:/prada/category$'
  '^GET:/prada/product$'
  '^GET:/prada/search$'
  '^GET:/prada/stores$'
  '^GET:/prada/suggest$'
  '^GET:/pristine-auction/categories$'
  '^GET:/pristine-auction/lot/[^/]+$'
  '^GET:/pristine-auction/search$'
  '^GET:/pristine-marketplace/collections$'
  '^GET:/pristine-marketplace/collections/[^/]+/products$'
  '^GET:/pristine-marketplace/pages$'
  '^GET:/pristine-marketplace/pages/[^/]+$'
  '^GET:/pristine-marketplace/products$'
  '^GET:/pristine-marketplace/products/[^/]+$'
  '^GET:/pristine-marketplace/products/[^/]+/recommendations$'
  '^GET:/pristine-marketplace/reviews$'
  '^GET:/pristine-marketplace/search$'
  '^GET:/pristine-marketplace/search/suggest$'
  '^GET:/pristine-marketplace/sitemap/urls$'
  '^GET:/pristine-marketplace/sitemaps$'
  '^GET:/pristine-marketplace/store$'
  '^GET:/producthunt/category/[^/]+$'
  '^GET:/producthunt/category/[^/]+/products$'
  '^GET:/producthunt/leaderboard$'
  '^GET:/producthunt/product/[^/]+$'
  '^GET:/producthunt/product/[^/]+/about$'
  '^GET:/producthunt/product/[^/]+/alternatives$'
  '^GET:/producthunt/product/[^/]+/customers$'
  '^GET:/producthunt/product/[^/]+/launches$'
  '^GET:/producthunt/product/[^/]+/makers$'
  '^GET:/producthunt/product/[^/]+/reviews$'
  '^GET:/producthunt/search$'
  '^GET:/propublica/article$'
  '^GET:/propublica/author$'
  '^GET:/propublica/headlines$'
  '^GET:/propublica/news$'
  '^GET:/propublica/sections$'
  '^GET:/psa/autographfacts/categories$'
  '^GET:/psa/autographfacts/gallery$'
  '^GET:/psa/autographfacts/subject$'
  '^GET:/psa/autographfacts/subjects$'
  '^GET:/psa/cardfacts/categories$'
  '^GET:/psa/cardfacts/checklist$'
  '^GET:/psa/cardfacts/sets$'
  '^GET:/psa/cert-lookup$'
  '^GET:/psa/price-guide/categories$'
  '^GET:/psa/price-guide/search$'
  '^GET:/psa/price-guide/set$'
  '^GET:/psa/probatfacts/categories$'
  '^GET:/psa/probatfacts/gallery$'
  '^GET:/psa/probatfacts/subject$'
  '^GET:/psa/probatfacts/subjects$'
  '^GET:/psa/ticketfacts/categories$'
  '^GET:/psa/ticketfacts/gallery$'
  '^GET:/psa/ticketfacts/subject$'
  '^GET:/psa/ticketfacts/subjects$'
  '^GET:/psastore/collections$'
  '^GET:/psastore/collections/[^/]+/products$'
  '^GET:/psastore/pages$'
  '^GET:/psastore/pages/[^/]+$'
  '^GET:/psastore/products$'
  '^GET:/psastore/products/[^/]+$'
  '^GET:/psastore/products/[^/]+/recommendations$'
  '^GET:/psastore/search/suggest$'
  '^GET:/psastore/sitemap/urls$'
  '^GET:/psastore/sitemaps$'
  '^GET:/psastore/store$'
  '^GET:/punch/article$'
  '^GET:/punch/author$'
  '^GET:/punch/headlines$'
  '^GET:/punch/news$'
  '^GET:/punch/sections$'
  '^GET:/quince/categories$'
  '^GET:/quince/navigation$'
  '^GET:/quince/product$'
  '^GET:/quince/product/faq$'
  '^GET:/quince/product/reviews$'
  '^GET:/quince/search$'
  '^GET:/quince/sitemap/urls$'
  '^GET:/quince/sitemaps$'
  '^GET:/quince/suggest$'
  '^GET:/qwant/suggest$'
  '^GET:/raisingcanes/directory$'
  '^GET:/raisingcanes/menu$'
  '^GET:/raisingcanes/nearby$'
  '^GET:/raisingcanes/promotion$'
  '^GET:/raisingcanes/promotions$'
  '^GET:/raisingcanes/store$'
  '^GET:/rappler/article$'
  '^GET:/rappler/author$'
  '^GET:/rappler/headlines$'
  '^GET:/rappler/news$'
  '^GET:/rappler/sections$'
  '^GET:/rawstory/article$'
  '^GET:/rawstory/author$'
  '^GET:/rawstory/headlines$'
  '^GET:/rawstory/news$'
  '^GET:/rawstory/sections$'
  '^GET:/rebag/collections$'
  '^GET:/rebag/collections/[^/]+/products$'
  '^GET:/rebag/pages$'
  '^GET:/rebag/pages/[^/]+$'
  '^GET:/rebag/products$'
  '^GET:/rebag/products/[^/]+$'
  '^GET:/rebag/products/[^/]+/recommendations$'
  '^GET:/rebag/search$'
  '^GET:/rebag/search/suggest$'
  '^GET:/rebag/sitemap/urls$'
  '^GET:/rebag/sitemaps$'
  '^GET:/rebag/store$'
  '^GET:/reddit/comments/[^/]+$'
  '^GET:/reddit/domain/[^/]+/posts$'
  '^GET:/reddit/leads$'
  '^GET:/reddit/post/[^/]+$'
  '^GET:/reddit/search$'
  '^GET:/reddit/subreddit/[^/]+/about$'
  '^GET:/reddit/subreddit/[^/]+/comments$'
  '^GET:/reddit/subreddit/[^/]+/posts$'
  '^GET:/reddit/subreddits/posts$'
  '^GET:/reddit/trends$'
  '^GET:/reddit/user/[^/]+/comments$'
  '^GET:/reddit/user/[^/]+/posts$'
  '^GET:/redfin/estimate$'
  '^GET:/redfin/property$'
  '^GET:/redfin/region-trends$'
  '^GET:/redfin/search$'
  '^GET:/redfin/similar$'
  '^GET:/research/jobs/[^/]+$'
  '^GET:/research/jobs/[^/]+/events$'
  '^GET:/research/jobs/[^/]+/results$'
  '^GET:/research/papers/metadata$'
  '^GET:/research/papers/search$'
  '^GET:/research/sources$'
  '^GET:/resy/availability$'
  '^GET:/resy/cuisines$'
  '^GET:/resy/event$'
  '^GET:/resy/events$'
  '^GET:/resy/locations$'
  '^GET:/resy/restaurant$'
  '^GET:/resy/search$'
  '^GET:/retailmenot/autocomplete$'
  '^GET:/retailmenot/blog-categories$'
  '^GET:/retailmenot/blog-post$'
  '^GET:/retailmenot/blog-posts$'
  '^GET:/retailmenot/blog-tags$'
  '^GET:/retailmenot/cashback$'
  '^GET:/retailmenot/categories$'
  '^GET:/retailmenot/category$'
  '^GET:/retailmenot/deal-event$'
  '^GET:/retailmenot/deal-events$'
  '^GET:/retailmenot/home$'
  '^GET:/retailmenot/store$'
  '^GET:/retailmenot/stores$'
  '^GET:/reuters/article$'
  '^GET:/reuters/articles$'
  '^GET:/reuters/author$'
  '^GET:/reuters/news$'
  '^GET:/reuters/section$'
  '^GET:/reuters/sections$'
  '^GET:/reverb/categories$'
  '^GET:/reverb/listing$'
  '^GET:/reverb/makes$'
  '^GET:/reverb/price-guide$'
  '^GET:/reverb/price-guide-search$'
  '^GET:/reverb/search$'
  '^GET:/reverb/shop$'
  '^GET:/reverb/shop-feedback$'
  '^GET:/rightmove/agents$'
  '^GET:/rightmove/agents/[^/]+$'
  '^GET:/rightmove/autocomplete$'
  '^GET:/rightmove/commercial/search$'
  '^GET:/rightmove/new-homes/search$'
  '^GET:/rightmove/properties/[^/]+$'
  '^GET:/rightmove/search$'
  '^GET:/rightmove/student/search$'
  '^GET:/rnz/article$'
  '^GET:/rnz/author$'
  '^GET:/rnz/headlines$'
  '^GET:/rnz/news$'
  '^GET:/rnz/sections$'
  '^GET:/roblox/badges$'
  '^GET:/roblox/game$'
  '^GET:/roblox/rankings$'
  '^GET:/roblox/search$'
  '^GET:/rollingstone/article$'
  '^GET:/rollingstone/author$'
  '^GET:/rollingstone/headlines$'
  '^GET:/rollingstone/news$'
  '^GET:/rollingstone/sections$'
  '^GET:/rothys/collections$'
  '^GET:/rothys/collections/[^/]+/products$'
  '^GET:/rothys/pages$'
  '^GET:/rothys/pages/[^/]+$'
  '^GET:/rothys/products$'
  '^GET:/rothys/products/[^/]+$'
  '^GET:/rothys/products/[^/]+/recommendations$'
  '^GET:/rothys/search/suggest$'
  '^GET:/rothys/sitemap/urls$'
  '^GET:/rothys/sitemaps$'
  '^GET:/rothys/store$'
  '^GET:/rottentomatoes/browse/filters$'
  '^GET:/rottentomatoes/browse/movies$'
  '^GET:/rottentomatoes/browse/tv$'
  '^GET:/rottentomatoes/critics/authors$'
  '^GET:/rottentomatoes/editorial/content$'
  '^GET:/rottentomatoes/editorial/detail$'
  '^GET:/rottentomatoes/editorial/search$'
  '^GET:/rottentomatoes/editorial/section$'
  '^GET:/rottentomatoes/editorial/taxonomies$'
  '^GET:/rottentomatoes/editorial/terms$'
  '^GET:/rottentomatoes/editorial/types$'
  '^GET:/rottentomatoes/episode$'
  '^GET:/rottentomatoes/movie$'
  '^GET:/rottentomatoes/movie/reviews$'
  '^GET:/rottentomatoes/person$'
  '^GET:/rottentomatoes/search$'
  '^GET:/rottentomatoes/season$'
  '^GET:/rottentomatoes/series$'
  '^GET:/rottentomatoes/sitemap/urls$'
  '^GET:/rottentomatoes/sitemaps$'
  '^GET:/rover/search$'
  '^GET:/rover/sitter/[^/]+$'
  '^GET:/rover/trainer-search$'
  '^GET:/rover/trainer/[^/]+$'
  '^GET:/rte/article$'
  '^GET:/rte/author$'
  '^GET:/rte/headlines$'
  '^GET:/rte/news$'
  '^GET:/rte/sections$'
  '^GET:/salon/article$'
  '^GET:/salon/author$'
  '^GET:/salon/headlines$'
  '^GET:/salon/news$'
  '^GET:/salon/sections$'
  '^GET:/samsclub/category$'
  '^GET:/samsclub/content/[^/]+$'
  '^GET:/samsclub/departments$'
  '^GET:/samsclub/product/[^/]+$'
  '^GET:/samsclub/product/[^/]+/related$'
  '^GET:/sbsnews/article$'
  '^GET:/sbsnews/author$'
  '^GET:/sbsnews/headlines$'
  '^GET:/sbsnews/news$'
  '^GET:/sbsnews/sections$'
  '^GET:/sciencealert/article$'
  '^GET:/sciencealert/author$'
  '^GET:/sciencealert/headlines$'
  '^GET:/sciencealert/news$'
  '^GET:/sciencealert/sections$'
  '^GET:/scmp/article$'
  '^GET:/scmp/author$'
  '^GET:/scmp/headlines$'
  '^GET:/scmp/sections$'
  '^GET:/screenrant/article$'
  '^GET:/screenrant/author$'
  '^GET:/screenrant/headlines$'
  '^GET:/screenrant/news$'
  '^GET:/screenrant/sections$'
  '^GET:/seatgeek/categories$'
  '^GET:/seatgeek/cities$'
  '^GET:/seatgeek/event$'
  '^GET:/seatgeek/events-by-category$'
  '^GET:/seatgeek/events-near$'
  '^GET:/seatgeek/performer$'
  '^GET:/seatgeek/performer-events$'
  '^GET:/seatgeek/search$'
  '^GET:/seatgeek/trending$'
  '^GET:/seatgeek/venue$'
  '^GET:/seatgeek/venue-events$'
  '^GET:/seattletimes/article$'
  '^GET:/seattletimes/author$'
  '^GET:/seattletimes/headlines$'
  '^GET:/seattletimes/news$'
  '^GET:/seattletimes/sections$'
  '^GET:/sec/company/intelligence$'
  '^GET:/sec/company/search$'
  '^GET:/sec/company/submissions$'
  '^GET:/sec/filing$'
  '^GET:/sec/filing/sections$'
  '^GET:/sec/financials$'
  '^GET:/sec/frames$'
  '^GET:/sec/full-text-search$'
  '^GET:/sec/insider$'
  '^GET:/sec/institutional-holdings$'
  '^GET:/sephora/brands$'
  '^GET:/sephora/categories$'
  '^GET:/sephora/category$'
  '^GET:/sephora/product$'
  '^GET:/sephora/product/questions$'
  '^GET:/sephora/product/reviews$'
  '^GET:/sephora/search$'
  '^GET:/sephora/stores$'
  '^GET:/sephora/suggest$'
  '^GET:/sevennewsau/article$'
  '^GET:/sevennewsau/author$'
  '^GET:/sevennewsau/headlines$'
  '^GET:/sevennewsau/news$'
  '^GET:/sevennewsau/sections$'
  '^GET:/sfgate/article$'
  '^GET:/sfgate/author$'
  '^GET:/sfgate/headlines$'
  '^GET:/sfgate/news$'
  '^GET:/sfgate/sections$'
  '^GET:/shakeshack/locations$'
  '^GET:/shakeshack/menu$'
  '^GET:/shakeshack/nearby$'
  '^GET:/shakeshack/store$'
  '^GET:/shein/category/filters$'
  '^GET:/shein/category/goods$'
  '^GET:/shein/category/nav$'
  '^GET:/shein/products/detail$'
  '^GET:/shop-app/analysis$'
  '^GET:/shop-app/categories$'
  '^GET:/shop-app/products/[^/]+$'
  '^GET:/shop-app/products/[^/]+/related$'
  '^GET:/shop-app/products/[^/]+/reviews$'
  '^GET:/shop-app/products/[^/]+/shop$'
  '^GET:/shop-app/products/[^/]+/variant$'
  '^GET:/shop-app/products/[^/]+/variants$'
  '^GET:/shop-app/search$'
  '^GET:/shop-app/shops/[^/]+$'
  '^GET:/shop-app/shops/[^/]+/collections/[^/]+/products$'
  '^GET:/shop-app/shops/[^/]+/locations$'
  '^GET:/shop-app/shops/[^/]+/products$'
  '^GET:/shop-app/shops/[^/]+/reviews$'
  '^GET:/shop-app/shops/[^/]+/typeahead$'
  '^GET:/shop-app/suggestions$'
  '^GET:/shopify/collections$'
  '^GET:/shopify/collections/[^/]+/products$'
  '^GET:/shopify/pages$'
  '^GET:/shopify/pages/[^/]+$'
  '^GET:/shopify/products$'
  '^GET:/shopify/products/[^/]+$'
  '^GET:/shopify/products/[^/]+/recommendations$'
  '^GET:/shopify/search/suggest$'
  '^GET:/shopify/sitemap/urls$'
  '^GET:/shopify/sitemaps$'
  '^GET:/shopify/store$'
  '^GET:/similarweb/search$'
  '^GET:/similarweb/web/[^/]+$'
  '^GET:/skims/collections$'
  '^GET:/skims/collections/[^/]+/products$'
  '^GET:/skims/pages$'
  '^GET:/skims/pages/[^/]+$'
  '^GET:/skims/products$'
  '^GET:/skims/products/[^/]+$'
  '^GET:/skims/products/[^/]+/recommendations$'
  '^GET:/skims/search/suggest$'
  '^GET:/skims/sitemap/urls$'
  '^GET:/skims/sitemaps$'
  '^GET:/skims/store$'
  '^GET:/skynews/article$'
  '^GET:/skynews/author$'
  '^GET:/skynews/headlines$'
  '^GET:/skynews/news$'
  '^GET:/skynews/sections$'
  '^GET:/skynews/video$'
  '^GET:/skynews/videos$'
  '^GET:/skysports/article$'
  '^GET:/skysports/author$'
  '^GET:/skysports/headlines$'
  '^GET:/skysports/news$'
  '^GET:/skysports/sections$'
  '^GET:/slate/article$'
  '^GET:/slate/categories$'
  '^GET:/slate/headlines$'
  '^GET:/slickdeals/categories$'
  '^GET:/slickdeals/category$'
  '^GET:/slickdeals/comments$'
  '^GET:/slickdeals/deal$'
  '^GET:/slickdeals/deal-types$'
  '^GET:/slickdeals/forums$'
  '^GET:/slickdeals/frontpage$'
  '^GET:/slickdeals/primary-categories$'
  '^GET:/slickdeals/primary-category$'
  '^GET:/slickdeals/search$'
  '^GET:/slickdeals/search/advanced$'
  '^GET:/sloanreview/article$'
  '^GET:/sloanreview/articles$'
  '^GET:/sloanreview/categories$'
  '^GET:/sloanreview/headlines$'
  '^GET:/sloanreview/topic$'
  '^GET:/smh/article$'
  '^GET:/smh/author$'
  '^GET:/smh/headlines$'
  '^GET:/smh/news$'
  '^GET:/smh/sections$'
  '^GET:/sofascore/categories$'
  '^GET:/sofascore/category-tournaments$'
  '^GET:/sofascore/draft$'
  '^GET:/sofascore/draft-picks$'
  '^GET:/sofascore/esports-game$'
  '^GET:/sofascore/event$'
  '^GET:/sofascore/event-at-bat-pitches$'
  '^GET:/sofascore/event-at-bats$'
  '^GET:/sofascore/event-average-positions$'
  '^GET:/sofascore/event-baseball-top-performers$'
  '^GET:/sofascore/event-best-players$'
  '^GET:/sofascore/event-comments$'
  '^GET:/sofascore/event-esports-games$'
  '^GET:/sofascore/event-graph$'
  '^GET:/sofascore/event-h2h$'
  '^GET:/sofascore/event-highlights$'
  '^GET:/sofascore/event-incidents$'
  '^GET:/sofascore/event-innings$'
  '^GET:/sofascore/event-lineups$'
  '^GET:/sofascore/event-managers$'
  '^GET:/sofascore/event-odds$'
  '^GET:/sofascore/event-player-heatmap$'
  '^GET:/sofascore/event-player-statistics$'
  '^GET:/sofascore/event-point-by-point$'
  '^GET:/sofascore/event-pregame-form$'
  '^GET:/sofascore/event-shotmap$'
  '^GET:/sofascore/event-statistics$'
  '^GET:/sofascore/event-team-heatmap$'
  '^GET:/sofascore/event-team-streaks$'
  '^GET:/sofascore/event-tennis-power$'
  '^GET:/sofascore/event-tv-channels$'
  '^GET:/sofascore/event-votes$'
  '^GET:/sofascore/live-events$'
  '^GET:/sofascore/manager$'
  '^GET:/sofascore/manager-events$'
  '^GET:/sofascore/mma-card$'
  '^GET:/sofascore/mma-schedule$'
  '^GET:/sofascore/odds-dropping$'
  '^GET:/sofascore/odds-winning$'
  '^GET:/sofascore/player$'
  '^GET:/sofascore/player-attributes$'
  '^GET:/sofascore/player-events$'
  '^GET:/sofascore/player-last-year-summary$'
  '^GET:/sofascore/player-national-team-statistics$'
  '^GET:/sofascore/player-penalty-history$'
  '^GET:/sofascore/player-ratings$'
  '^GET:/sofascore/player-season-heatmap$'
  '^GET:/sofascore/player-season-statistics$'
  '^GET:/sofascore/player-statistical-rankings$'
  '^GET:/sofascore/player-statistics-seasons$'
  '^GET:/sofascore/player-tournaments$'
  '^GET:/sofascore/player-transfers$'
  '^GET:/sofascore/ranking-types$'
  '^GET:/sofascore/rankings$'
  '^GET:/sofascore/referee$'
  '^GET:/sofascore/referee-events$'
  '^GET:/sofascore/referee-statistics$'
  '^GET:/sofascore/round-events$'
  '^GET:/sofascore/scheduled-events$'
  '^GET:/sofascore/scheduled-tournaments$'
  '^GET:/sofascore/search$'
  '^GET:/sofascore/search-typed$'
  '^GET:/sofascore/season-events$'
  '^GET:/sofascore/sports$'
  '^GET:/sofascore/stage$'
  '^GET:/sofascore/stage-categories$'
  '^GET:/sofascore/stage-driver-performance$'
  '^GET:/sofascore/stage-featured$'
  '^GET:/sofascore/stage-schedule$'
  '^GET:/sofascore/stage-seasons$'
  '^GET:/sofascore/stage-standings$'
  '^GET:/sofascore/stage-substages$'
  '^GET:/sofascore/standings$'
  '^GET:/sofascore/team$'
  '^GET:/sofascore/team-achievements$'
  '^GET:/sofascore/team-events$'
  '^GET:/sofascore/team-goal-distributions$'
  '^GET:/sofascore/team-near-events$'
  '^GET:/sofascore/team-of-the-week$'
  '^GET:/sofascore/team-of-the-week-periods$'
  '^GET:/sofascore/team-performance$'
  '^GET:/sofascore/team-player-statistics$'
  '^GET:/sofascore/team-player-statistics-seasons$'
  '^GET:/sofascore/team-players$'
  '^GET:/sofascore/team-rankings$'
  '^GET:/sofascore/team-season-statistics$'
  '^GET:/sofascore/team-statistics-seasons$'
  '^GET:/sofascore/team-top-players$'
  '^GET:/sofascore/team-tournaments$'
  '^GET:/sofascore/team-transfers$'
  '^GET:/sofascore/tennis-player-grand-slam-results$'
  '^GET:/sofascore/tournament-cuptree$'
  '^GET:/sofascore/tournament-info$'
  '^GET:/sofascore/tournament-player-of-the-season$'
  '^GET:/sofascore/tournament-player-statistics$'
  '^GET:/sofascore/tournament-rounds$'
  '^GET:/sofascore/tournament-seasons$'
  '^GET:/sofascore/tournament-statistics-info$'
  '^GET:/sofascore/tournament-team-of-the-season$'
  '^GET:/sofascore/tournament-teams$'
  '^GET:/sofascore/tournament-top-players$'
  '^GET:/sofascore/tournament-top-teams$'
  '^GET:/sofascore/tournament-venues$'
  '^GET:/sofascore/tournament-winners$'
  '^GET:/sofascore/tournaments-with-feature$'
  '^GET:/sofascore/trending-events$'
  '^GET:/sofascore/trending-players$'
  '^GET:/sofascore/venue$'
  '^GET:/sofascore/venue-events$'
  '^GET:/sonic/availability$'
  '^GET:/sonic/categories$'
  '^GET:/sonic/deals$'
  '^GET:/sonic/directory$'
  '^GET:/sonic/item$'
  '^GET:/sonic/location-suggest$'
  '^GET:/sonic/locations$'
  '^GET:/sonic/menu$'
  '^GET:/sonic/nearby$'
  '^GET:/sonic/nutrition-documents$'
  '^GET:/sonic/sitemap$'
  '^GET:/sonic/store$'
  '^GET:/soundcloud/playlist$'
  '^GET:/soundcloud/profile$'
  '^GET:/soundcloud/search$'
  '^GET:/soundcloud/track$'
  '^GET:/soundcloud/user-tracks$'
  '^GET:/space/article$'
  '^GET:/space/author$'
  '^GET:/space/headlines$'
  '^GET:/space/news$'
  '^GET:/space/sections$'
  '^GET:/sparkfun/categories$'
  '^GET:/sparkfun/category$'
  '^GET:/sparkfun/product$'
  '^GET:/sparkfun/search$'
  '^GET:/sportingnews/article$'
  '^GET:/sportingnews/author$'
  '^GET:/sportingnews/headlines$'
  '^GET:/sportingnews/news$'
  '^GET:/sportingnews/sections$'
  '^GET:/sportskeeda/article$'
  '^GET:/sportskeeda/author$'
  '^GET:/sportskeeda/college-basketball-schedule$'
  '^GET:/sportskeeda/college-basketball-schedule-options$'
  '^GET:/sportskeeda/cricket-commentary$'
  '^GET:/sportskeeda/cricket-match$'
  '^GET:/sportskeeda/depth-chart$'
  '^GET:/sportskeeda/draft-picks$'
  '^GET:/sportskeeda/draft-picks-options$'
  '^GET:/sportskeeda/event-calendar$'
  '^GET:/sportskeeda/event-calendar-options$'
  '^GET:/sportskeeda/feed$'
  '^GET:/sportskeeda/football-data$'
  '^GET:/sportskeeda/football-options$'
  '^GET:/sportskeeda/guessing-game$'
  '^GET:/sportskeeda/guessing-game-entities$'
  '^GET:/sportskeeda/guessing-games$'
  '^GET:/sportskeeda/nba-queries$'
  '^GET:/sportskeeda/news$'
  '^GET:/sportskeeda/page-data$'
  '^GET:/sportskeeda/page-options$'
  '^GET:/sportskeeda/player-stats$'
  '^GET:/sportskeeda/profile$'
  '^GET:/sportskeeda/quiz$'
  '^GET:/sportskeeda/quiz-categories$'
  '^GET:/sportskeeda/quizzes$'
  '^GET:/sportskeeda/salary-cap$'
  '^GET:/sportskeeda/schedule$'
  '^GET:/sportskeeda/sections$'
  '^GET:/sportskeeda/sitemap-items$'
  '^GET:/sportskeeda/sitemaps$'
  '^GET:/sportskeeda/standings$'
  '^GET:/sportskeeda/standings-options$'
  '^GET:/sportskeeda/taxonomy-search$'
  '^GET:/sportskeeda/topic$'
  '^GET:/sportskeeda/trade-values$'
  '^GET:/sportskeeda/transactions$'
  '^GET:/sportskeeda/transactions-options$'
  '^GET:/sportskeeda/video$'
  '^GET:/sportskeeda/videos$'
  '^GET:/sportskeeda/wiki-activity$'
  '^GET:/sportskeeda/wiki-article$'
  '^GET:/sportskeeda/wiki-categories$'
  '^GET:/sportskeeda/wiki-contributors$'
  '^GET:/sportskeeda/wiki-issues$'
  '^GET:/sportskeeda/wiki-options$'
  '^GET:/sportskeeda/wiki-pages$'
  '^GET:/sportskeeda/wiki-summary$'
  '^GET:/spotify-podcasts/categories$'
  '^GET:/spotify-podcasts/charts$'
  '^GET:/spotify-podcasts/episode$'
  '^GET:/spotify-podcasts/home$'
  '^GET:/spotify-podcasts/search$'
  '^GET:/spotify-podcasts/show$'
  '^GET:/spotify-podcasts/show/episodes$'
  '^GET:/spotify-podcasts/show/recommendations$'
  '^GET:/spotify/album$'
  '^GET:/spotify/album/tracks$'
  '^GET:/spotify/albums/search$'
  '^GET:/spotify/artist$'
  '^GET:/spotify/artist/albums$'
  '^GET:/spotify/artist/playlists$'
  '^GET:/spotify/artist/related$'
  '^GET:/spotify/artists/search$'
  '^GET:/spotify/audiobook$'
  '^GET:/spotify/audiobook/chapters$'
  '^GET:/spotify/audiobooks/search$'
  '^GET:/spotify/chapter$'
  '^GET:/spotify/episodes/search$'
  '^GET:/spotify/featured-charts-by-country$'
  '^GET:/spotify/genre$'
  '^GET:/spotify/home$'
  '^GET:/spotify/playlist$'
  '^GET:/spotify/playlists/search$'
  '^GET:/spotify/popular-by-country$'
  '^GET:/spotify/profile$'
  '^GET:/spotify/profile/followers$'
  '^GET:/spotify/profile/playlists$'
  '^GET:/spotify/profiles/search$'
  '^GET:/spotify/search$'
  '^GET:/spotify/section$'
  '^GET:/spotify/shows/search$'
  '^GET:/spotify/track$'
  '^GET:/spotify/track/recommended$'
  '^GET:/spotify/track/similar-albums$'
  '^GET:/spotify/tracks/search$'
  '^GET:/standard/article$'
  '^GET:/standard/author$'
  '^GET:/standard/headlines$'
  '^GET:/standard/news$'
  '^GET:/standard/sections$'
  '^GET:/starbucks/menu$'
  '^GET:/starbucks/nearest-store$'
  '^GET:/starbucks/product/[^/]+/[^/]+$'
  '^GET:/starbucks/stores$'
  '^GET:/startpage/suggest$'
  '^GET:/startribune/news$'
  '^GET:/steam/achievements$'
  '^GET:/steam/app$'
  '^GET:/steam/category/[^/]+$'
  '^GET:/steam/charts/concurrent$'
  '^GET:/steam/charts/most-played$'
  '^GET:/steam/charts/top-releases$'
  '^GET:/steam/community-recommendations$'
  '^GET:/steam/featured$'
  '^GET:/steam/featured-categories$'
  '^GET:/steam/items$'
  '^GET:/steam/news$'
  '^GET:/steam/package$'
  '^GET:/steam/players$'
  '^GET:/steam/reviews$'
  '^GET:/steam/reviews/histogram$'
  '^GET:/steam/search$'
  '^GET:/steam/search/results$'
  '^GET:/steam/steamspy$'
  '^GET:/steam/tags$'
  '^GET:/steam/tags/list$'
  '^GET:/steam/top-sellers$'
  '^GET:/stevemadden/collections$'
  '^GET:/stevemadden/collections/[^/]+/products$'
  '^GET:/stevemadden/pages$'
  '^GET:/stevemadden/pages/[^/]+$'
  '^GET:/stevemadden/products$'
  '^GET:/stevemadden/products/[^/]+$'
  '^GET:/stevemadden/products/[^/]+/recommendations$'
  '^GET:/stevemadden/search/suggest$'
  '^GET:/stevemadden/sitemap/urls$'
  '^GET:/stevemadden/sitemaps$'
  '^GET:/stevemadden/store$'
  '^GET:/stockx/brands$'
  '^GET:/stockx/categories$'
  '^GET:/stockx/product/[^/]+$'
  '^GET:/stockx/releases$'
  '^GET:/stockx/search$'
  '^GET:/straitstimes/article$'
  '^GET:/straitstimes/author$'
  '^GET:/straitstimes/headlines$'
  '^GET:/straitstimes/news$'
  '^GET:/straitstimes/sections$'
  '^GET:/strava/challenges$'
  '^GET:/strava/clubs/[^/]+$'
  '^GET:/strava/routes$'
  '^GET:/strava/routes/detail$'
  '^GET:/streeteasy/areas$'
  '^GET:/streeteasy/buildings/[^/]+$'
  '^GET:/streeteasy/market-data/catalog$'
  '^GET:/streeteasy/market-data/indices$'
  '^GET:/streeteasy/market-data/inventory$'
  '^GET:/streeteasy/market-data/series$'
  '^GET:/streeteasy/quick-search$'
  '^GET:/streeteasy/rentals/search$'
  '^GET:/streeteasy/sales/search$'
  '^GET:/streeteasy/schools/[^/]+$'
  '^GET:/streeteasy/units/[^/]+/[^/]+$'
  '^GET:/stubhub/carousel$'
  '^GET:/stubhub/categories$'
  '^GET:/stubhub/category-events$'
  '^GET:/stubhub/explore$'
  '^GET:/stubhub/navigation-categories$'
  '^GET:/stubhub/performer-events$'
  '^GET:/stubhub/search$'
  '^GET:/stubhub/suggested-searches$'
  '^GET:/stubhub/trending$'
  '^GET:/stubhub/trending-events$'
  '^GET:/stubhub/venue-events$'
  '^GET:/stuff/article$'
  '^GET:/stuff/author$'
  '^GET:/stuff/headlines$'
  '^GET:/stuff/news$'
  '^GET:/stuff/sections$'
  '^GET:/substack/categories$'
  '^GET:/substack/category$'
  '^GET:/substack/explore$'
  '^GET:/substack/leaderboard$'
  '^GET:/substack/note$'
  '^GET:/substack/note/replies$'
  '^GET:/substack/note/restacks$'
  '^GET:/substack/notes$'
  '^GET:/substack/notes/tabs$'
  '^GET:/substack/post$'
  '^GET:/substack/publication$'
  '^GET:/substack/publication/contributors$'
  '^GET:/substack/publication/posts$'
  '^GET:/substack/publication/recommendations$'
  '^GET:/substack/search$'
  '^GET:/substack/user$'
  '^GET:/substack/user/activity$'
  '^GET:/substack/user/connections$'
  '^GET:/substack/user/search$'
  '^GET:/subway/available-times$'
  '^GET:/subway/combos$'
  '^GET:/subway/menu$'
  '^GET:/subway/nearby$'
  '^GET:/subway/sitemap$'
  '^GET:/subway/store$'
  '^GET:/sun/article$'
  '^GET:/sun/author$'
  '^GET:/sun/headlines$'
  '^GET:/sun/news$'
  '^GET:/sun/sections$'
  '^GET:/swiggy/collections$'
  '^GET:/swiggy/restaurant$'
  '^GET:/swiggy/restaurant/menu$'
  '^GET:/swiggy/search$'
  '^GET:/taco-bell/app-menu$'
  '^GET:/taco-bell/categories$'
  '^GET:/taco-bell/menu$'
  '^GET:/taco-bell/nutrition$'
  '^GET:/taco-bell/product$'
  '^GET:/taco-bell/store$'
  '^GET:/taco-bell/store-menu$'
  '^GET:/taco-bell/stores$'
  '^GET:/target/categories$'
  '^GET:/target/category-products$'
  '^GET:/target/filter-options$'
  '^GET:/target/product$'
  '^GET:/target/questions$'
  '^GET:/target/reviews$'
  '^GET:/target/search$'
  '^GET:/target/stores$'
  '^GET:/techcrunch/article$'
  '^GET:/techcrunch/author$'
  '^GET:/techcrunch/headlines$'
  '^GET:/techcrunch/news$'
  '^GET:/techcrunch/sections$'
  '^GET:/techradar/article$'
  '^GET:/techradar/author$'
  '^GET:/techradar/headlines$'
  '^GET:/techradar/news$'
  '^GET:/techradar/sections$'
  '^GET:/telegraph/article$'
  '^GET:/telegraph/author$'
  '^GET:/telegraph/headlines$'
  '^GET:/telegraph/news$'
  '^GET:/telegraph/sections$'
  '^GET:/tes/jobs/detail$'
  '^GET:/tes/jobs/employer$'
  '^GET:/tes/jobs/search$'
  '^GET:/tes/resources/detail$'
  '^GET:/tes/resources/search$'
  '^GET:/tes/resources/shop$'
  '^GET:/tes/schools/search$'
  '^GET:/tesla-jobs/job$'
  '^GET:/tesla-jobs/list$'
  '^GET:/theage/article$'
  '^GET:/theage/author$'
  '^GET:/theage/headlines$'
  '^GET:/theage/news$'
  '^GET:/theage/sections$'
  '^GET:/theatlantic/article$'
  '^GET:/theatlantic/author$'
  '^GET:/theatlantic/headlines$'
  '^GET:/theatlantic/sections$'
  '^GET:/theblaze/article$'
  '^GET:/theblaze/author$'
  '^GET:/theblaze/headlines$'
  '^GET:/theblaze/news$'
  '^GET:/theblaze/sections$'
  '^GET:/thebodyshop/collections$'
  '^GET:/thebodyshop/collections/[^/]+/products$'
  '^GET:/thebodyshop/pages$'
  '^GET:/thebodyshop/pages/[^/]+$'
  '^GET:/thebodyshop/products$'
  '^GET:/thebodyshop/products/[^/]+$'
  '^GET:/thebodyshop/products/[^/]+/recommendations$'
  '^GET:/thebodyshop/search/suggest$'
  '^GET:/thebodyshop/sitemap/urls$'
  '^GET:/thebodyshop/sitemaps$'
  '^GET:/thebodyshop/store$'
  '^GET:/thedailybeast/article$'
  '^GET:/thedailybeast/author$'
  '^GET:/thedailybeast/headlines$'
  '^GET:/thedailybeast/news$'
  '^GET:/thedailybeast/sections$'
  '^GET:/thehill/article$'
  '^GET:/thehill/author$'
  '^GET:/thehill/headlines$'
  '^GET:/thehill/news$'
  '^GET:/thehill/sections$'
  '^GET:/thehindu/article$'
  '^GET:/thehindu/author$'
  '^GET:/thehindu/headlines$'
  '^GET:/thehindu/news$'
  '^GET:/thehindu/sections$'
  '^GET:/thejournal/article$'
  '^GET:/thejournal/author$'
  '^GET:/thejournal/headlines$'
  '^GET:/thejournal/news$'
  '^GET:/thejournal/sections$'
  '^GET:/thenextweb/article$'
  '^GET:/thenextweb/author$'
  '^GET:/thenextweb/headlines$'
  '^GET:/thenextweb/news$'
  '^GET:/thenextweb/sections$'
  '^GET:/therealreal/autocomplete$'
  '^GET:/therealreal/categories$'
  '^GET:/therealreal/category$'
  '^GET:/therealreal/collection$'
  '^GET:/therealreal/collections$'
  '^GET:/therealreal/conditions$'
  '^GET:/therealreal/designer$'
  '^GET:/therealreal/designers$'
  '^GET:/therealreal/listing$'
  '^GET:/therealreal/search$'
  '^GET:/therealreal/similar$'
  '^GET:/thestarmy/article$'
  '^GET:/thestarmy/author$'
  '^GET:/thestarmy/headlines$'
  '^GET:/thestarmy/news$'
  '^GET:/thestarmy/sections$'
  '^GET:/theverge/article$'
  '^GET:/theverge/author$'
  '^GET:/theverge/headlines$'
  '^GET:/theverge/news$'
  '^GET:/theverge/sections$'
  '^GET:/thisismoney/article$'
  '^GET:/thisismoney/author$'
  '^GET:/thisismoney/headlines$'
  '^GET:/thisismoney/news$'
  '^GET:/thisismoney/sections$'
  '^GET:/threads/post/[^/]+/[^/]+$'
  '^GET:/threads/post/[^/]+/[^/]+/replies$'
  '^GET:/threads/profile/[^/]+$'
  '^GET:/threads/profile/[^/]+/media$'
  '^GET:/threads/profile/[^/]+/posts$'
  '^GET:/threads/profile/[^/]+/replies$'
  '^GET:/threads/profile/[^/]+/reposts$'
  '^GET:/threads/profile/[^/]+/topics$'
  '^GET:/threads/search$'
  '^GET:/threads/search/topics$'
  '^GET:/ticketmaster/attraction$'
  '^GET:/ticketmaster/attraction-events$'
  '^GET:/ticketmaster/attraction-related$'
  '^GET:/ticketmaster/attraction-reviews$'
  '^GET:/ticketmaster/discover-categories$'
  '^GET:/ticketmaster/discover-category-events$'
  '^GET:/ticketmaster/discover-cities$'
  '^GET:/ticketmaster/discover-city-events$'
  '^GET:/ticketmaster/event$'
  '^GET:/ticketmaster/search-events$'
  '^GET:/ticketmaster/suggest$'
  '^GET:/ticketmaster/trending-attractions$'
  '^GET:/ticketmaster/venue$'
  '^GET:/ticketmaster/venue-enhanced-details$'
  '^GET:/ticketmaster/venue-events$'
  '^GET:/ticketweb/event$'
  '^GET:/ticketweb/search$'
  '^GET:/ticketweb/venue$'
  '^GET:/tiffany/categories$'
  '^GET:/tiffany/category$'
  '^GET:/tiffany/content-search$'
  '^GET:/tiffany/filters$'
  '^GET:/tiffany/product$'
  '^GET:/tiffany/search$'
  '^GET:/tiffany/stores$'
  '^GET:/tiffany/suggest$'
  '^GET:/tiktok/category$'
  '^GET:/tiktok/comments$'
  '^GET:/tiktok/creative-center/filters$'
  '^GET:/tiktok/creative-center/hashtags$'
  '^GET:/tiktok/creative-center/top-content$'
  '^GET:/tiktok/creative-center/videos$'
  '^GET:/tiktok/explore/[^/]+$'
  '^GET:/tiktok/hashtag/[^/]+$'
  '^GET:/tiktok/hashtags$'
  '^GET:/tiktok/mobile/feed$'
  '^GET:/tiktok/mobile/hashtag$'
  '^GET:/tiktok/mobile/hashtag/posts$'
  '^GET:/tiktok/mobile/hashtags$'
  '^GET:/tiktok/mobile/live/effects$'
  '^GET:/tiktok/mobile/live/gifts$'
  '^GET:/tiktok/mobile/live/search$'
  '^GET:/tiktok/mobile/music/beats$'
  '^GET:/tiktok/mobile/music/collections$'
  '^GET:/tiktok/mobile/music/pick$'
  '^GET:/tiktok/mobile/music/posts$'
  '^GET:/tiktok/mobile/music/related$'
  '^GET:/tiktok/mobile/music/trending$'
  '^GET:/tiktok/mobile/search$'
  '^GET:/tiktok/mobile/search/music$'
  '^GET:/tiktok/mobile/search/user$'
  '^GET:/tiktok/mobile/trending/categories$'
  '^GET:/tiktok/mobile/trending/effects$'
  '^GET:/tiktok/popular-trend/country-industry-meta$'
  '^GET:/tiktok/post/[^/]+$'
  '^GET:/tiktok/posts$'
  '^GET:/tiktok/profile/[^/]+$'
  '^GET:/tiktok/search$'
  '^GET:/tiktok/search/hashtag$'
  '^GET:/tiktok/search/user$'
  '^GET:/tiktok/top-ads/analysis$'
  '^GET:/tiktok/top-ads/detail$'
  '^GET:/tiktok/top-ads/filters$'
  '^GET:/tiktok/top-ads/list$'
  '^GET:/tiktok/top-ads/location-info$'
  '^GET:/tiktok/top-ads/locations$'
  '^GET:/tiktok/top-ads/recommend$'
  '^GET:/tiktok/top-ads/safety$'
  '^GET:/tiktok/top-ads/spotlight$'
  '^GET:/tiktok/top-ads/suggestions$'
  '^GET:/tiktok/trending$'
  '^GET:/time/article$'
  '^GET:/time/author$'
  '^GET:/time/headlines$'
  '^GET:/time/news$'
  '^GET:/time/sections$'
  '^GET:/timeslive/article$'
  '^GET:/timeslive/headlines$'
  '^GET:/timeslive/news$'
  '^GET:/timeslive/sections$'
  '^GET:/timesofindia/article$'
  '^GET:/timesofindia/author$'
  '^GET:/timesofindia/headlines$'
  '^GET:/timesofindia/news$'
  '^GET:/timesofindia/sections$'
  '^GET:/timesofisrael/article$'
  '^GET:/timesofisrael/author$'
  '^GET:/timesofisrael/headlines$'
  '^GET:/timesofisrael/news$'
  '^GET:/timesofisrael/sections$'
  '^GET:/tmdb/collection/[^/]+$'
  '^GET:/tmdb/genres$'
  '^GET:/tmdb/movie/[^/]+$'
  '^GET:/tmdb/movie/list$'
  '^GET:/tmdb/person/[^/]+$'
  '^GET:/tmdb/person/list$'
  '^GET:/tmdb/search$'
  '^GET:/tmdb/tv/[^/]+$'
  '^GET:/tmdb/tv/list$'
  '^GET:/tmz/article$'
  '^GET:/tmz/author$'
  '^GET:/tmz/headlines$'
  '^GET:/tmz/news$'
  '^GET:/tmz/sections$'
  '^GET:/tokopedia/autocomplete$'
  '^GET:/tokopedia/category$'
  '^GET:/tokopedia/home$'
  '^GET:/tokopedia/home/tabs$'
  '^GET:/tokopedia/product$'
  '^GET:/tokopedia/product/review-filters$'
  '^GET:/tokopedia/search$'
  '^GET:/tokopedia/search/filters$'
  '^GET:/tomsguide/article$'
  '^GET:/tomsguide/author$'
  '^GET:/tomsguide/headlines$'
  '^GET:/tomsguide/news$'
  '^GET:/tomsguide/sections$'
  '^GET:/tomshardware/article$'
  '^GET:/tomshardware/author$'
  '^GET:/tomshardware/headlines$'
  '^GET:/tomshardware/news$'
  '^GET:/tomshardware/sections$'
  '^GET:/torontostar/article$'
  '^GET:/torontostar/author$'
  '^GET:/torontostar/headlines$'
  '^GET:/torontostar/news$'
  '^GET:/torontostar/sections$'
  '^GET:/townhall/article$'
  '^GET:/townhall/author$'
  '^GET:/townhall/headlines$'
  '^GET:/townhall/news$'
  '^GET:/townhall/sections$'
  '^GET:/tripadvisor/autocomplete$'
  '^GET:/tripadvisor/enums$'
  '^GET:/tripadvisor/hotels$'
  '^GET:/tripadvisor/place$'
  '^GET:/tripadvisor/reviews$'
  '^GET:/tripadvisor/search$'
  '^GET:/tripcom/hotels/[^/]+$'
  '^GET:/tripcom/hotels/search$'
  '^GET:/trustmrr/acquire$'
  '^GET:/trustmrr/categories$'
  '^GET:/trustmrr/category/[^/]+$'
  '^GET:/trustmrr/leaderboard$'
  '^GET:/trustmrr/marketplace$'
  '^GET:/trustmrr/startup/[^/]+$'
  '^GET:/trustmrr/startups$'
  '^GET:/trustpilot/business-units/search$'
  '^GET:/trustpilot/business/[^/]+$'
  '^GET:/trustpilot/business/[^/]+/related$'
  '^GET:/trustpilot/business/[^/]+/reviews$'
  '^GET:/trustpilot/categories$'
  '^GET:/trustpilot/categories/search$'
  '^GET:/trustpilot/category/[^/]+$'
  '^GET:/twitch/channel$'
  '^GET:/twitch/clips$'
  '^GET:/twitch/schedule$'
  '^GET:/twitch/search$'
  '^GET:/twitch/streams$'
  '^GET:/twitch/team$'
  '^GET:/twitch/top-games$'
  '^GET:/twitch/videos$'
  '^GET:/twitch/vod-comments$'
  '^GET:/ubereats/feed$'
  '^GET:/ubereats/search$'
  '^GET:/ubereats/store/[^/]+$'
  '^GET:/ubereats/store/[^/]+/menu$'
  '^GET:/ubereats/store/[^/]+/reviews$'
  '^GET:/ulta/categories$'
  '^GET:/ulta/category$'
  '^GET:/ulta/product/[^/]+$'
  '^GET:/ulta/product/questions$'
  '^GET:/ulta/product/reviews$'
  '^GET:/ulta/search$'
  '^GET:/ulta/stores$'
  '^GET:/ulta/suggest$'
  '^GET:/upwork/freelancer/[^/]+$'
  '^GET:/upwork/job/[^/]+$'
  '^GET:/upwork/search$'
  '^GET:/usatoday/article$'
  '^GET:/usatoday/author$'
  '^GET:/usatoday/headlines$'
  '^GET:/usatoday/news$'
  '^GET:/usatoday/sections$'
  '^GET:/usmagazine/article$'
  '^GET:/usmagazine/author$'
  '^GET:/usmagazine/headlines$'
  '^GET:/usmagazine/news$'
  '^GET:/usmagazine/sections$'
  '^GET:/usptoppubs/detail$'
  '^GET:/usptoppubs/search$'
  '^GET:/vanguardng/article$'
  '^GET:/vanguardng/author$'
  '^GET:/vanguardng/headlines$'
  '^GET:/vanguardng/news$'
  '^GET:/vanguardng/sections$'
  '^GET:/vanityfair/article$'
  '^GET:/vanityfair/author$'
  '^GET:/vanityfair/headlines$'
  '^GET:/vanityfair/news$'
  '^GET:/vanityfair/sections$'
  '^GET:/variety/article$'
  '^GET:/variety/author$'
  '^GET:/variety/headlines$'
  '^GET:/variety/news$'
  '^GET:/variety/sections$'
  '^GET:/vestiaire/brands$'
  '^GET:/vestiaire/categories$'
  '^GET:/vestiaire/conditions$'
  '^GET:/vestiaire/product$'
  '^GET:/vestiaire/search$'
  '^GET:/vestiaire/search-sellers$'
  '^GET:/vestiaire/seller$'
  '^GET:/vestiaire/suggest$'
  '^GET:/vice/article$'
  '^GET:/vice/author$'
  '^GET:/vice/headlines$'
  '^GET:/vice/news$'
  '^GET:/vice/sections$'
  '^GET:/vinted/brand$'
  '^GET:/vinted/brands$'
  '^GET:/vinted/catalog$'
  '^GET:/vinted/categories$'
  '^GET:/vinted/category$'
  '^GET:/vinted/item$'
  '^GET:/vinted/member$'
  '^GET:/vox/article$'
  '^GET:/vox/author$'
  '^GET:/vox/headlines$'
  '^GET:/vox/news$'
  '^GET:/vox/sections$'
  '^GET:/vrbo/locations/search$'
  '^GET:/vrbo/properties/[^/]+$'
  '^GET:/vrbo/properties/[^/]+/rate-calendar$'
  '^GET:/vrbo/properties/[^/]+/reviews$'
  '^GET:/vrbo/travel-pages$'
  '^GET:/vrbo/travel-pages/[^/]+$'
  '^GET:/walesonline/article$'
  '^GET:/walesonline/author$'
  '^GET:/walesonline/headlines$'
  '^GET:/walesonline/news$'
  '^GET:/walesonline/sections$'
  '^GET:/walgreens/stores$'
  '^GET:/walmart/product/[^/]+$'
  '^GET:/walmart/product/[^/]+/reviews$'
  '^GET:/walmart/search$'
  '^GET:/wapo/article$'
  '^GET:/wapo/author$'
  '^GET:/wapo/headlines$'
  '^GET:/wapo/news$'
  '^GET:/wapo/sections$'
  '^GET:/wayfair/categories$'
  '^GET:/wayfair/category$'
  '^GET:/wayfair/product/[^/]+$'
  '^GET:/wccftech/article$'
  '^GET:/wccftech/author$'
  '^GET:/wccftech/headlines$'
  '^GET:/wccftech/news$'
  '^GET:/wccftech/sections$'
  '^GET:/web/capabilities$'
  '^GET:/web/crawl/[^/]+$'
  '^GET:/web/crawl/[^/]+/results$'
  '^GET:/wendys/categories$'
  '^GET:/wendys/directory$'
  '^GET:/wendys/item$'
  '^GET:/wendys/menu$'
  '^GET:/wendys/nearby$'
  '^GET:/wendys/nutrition$'
  '^GET:/wendys/restaurant$'
  '^GET:/wendys/store$'
  '^GET:/wendys/store-menu$'
  '^GET:/wendys/time-slots$'
  '^GET:/whataburger/sitemap$'
  '^GET:/whataburger/store$'
  '^GET:/whatnot/browse$'
  '^GET:/whatnot/categories$'
  '^GET:/whatnot/live/[^/]+$'
  '^GET:/whatnot/seller/[^/]+$'
  '^GET:/wingstop/delivery-store$'
  '^GET:/wingstop/directory$'
  '^GET:/wingstop/flavors$'
  '^GET:/wingstop/menu$'
  '^GET:/wingstop/nearby$'
  '^GET:/wingstop/store$'
  '^GET:/wired/article$'
  '^GET:/wired/author$'
  '^GET:/wired/headlines$'
  '^GET:/wired/news$'
  '^GET:/wired/sections$'
  '^GET:/wish/categories$'
  '^GET:/wish/product/[^/]+$'
  '^GET:/wish/product/[^/]+/related$'
  '^GET:/wish/product/[^/]+/reviews$'
  '^GET:/wish/search$'
  '^GET:/wish/suggest$'
  '^GET:/wolt/cities$'
  '^GET:/wolt/collections$'
  '^GET:/wolt/restaurant$'
  '^GET:/wolt/restaurant/availability$'
  '^GET:/wolt/restaurant/menu$'
  '^GET:/wolt/restaurant/menu/search$'
  '^GET:/wolt/search$'
  '^GET:/wolt/search/filters$'
  '^GET:/wsj/article$'
  '^GET:/wsj/author$'
  '^GET:/x/post/[^/]+$'
  '^GET:/x/profile/[^/]+$'
  '^GET:/x/profile/[^/]+/posts$'
  '^GET:/xbox/browse$'
  '^GET:/xbox/collection$'
  '^GET:/xbox/game$'
  '^GET:/xbox/reviews$'
  '^GET:/xbox/search$'
  '^GET:/xda/article$'
  '^GET:/xda/author$'
  '^GET:/xda/headlines$'
  '^GET:/xda/news$'
  '^GET:/xda/sections$'
  '^GET:/yahoo-autos/article$'
  '^GET:/yahoo-autos/category$'
  '^GET:/yahoo-autos/home$'
  '^GET:/yahoo-entertainment/article$'
  '^GET:/yahoo-entertainment/category$'
  '^GET:/yahoo-entertainment/home$'
  '^GET:/yahoo-finance/calendars$'
  '^GET:/yahoo-finance/calendars/[^/]+$'
  '^GET:/yahoo-finance/industries$'
  '^GET:/yahoo-finance/industries/[^/]+$'
  '^GET:/yahoo-finance/lookup$'
  '^GET:/yahoo-finance/market/[^/]+/status$'
  '^GET:/yahoo-finance/market/[^/]+/summary$'
  '^GET:/yahoo-finance/screener/[^/]+$'
  '^GET:/yahoo-finance/screeners$'
  '^GET:/yahoo-finance/search$'
  '^GET:/yahoo-finance/sectors$'
  '^GET:/yahoo-finance/sectors/[^/]+$'
  '^GET:/yahoo-finance/ticker/[^/]+/actions$'
  '^GET:/yahoo-finance/ticker/[^/]+/analysts$'
  '^GET:/yahoo-finance/ticker/[^/]+/calendar$'
  '^GET:/yahoo-finance/ticker/[^/]+/capital-gains$'
  '^GET:/yahoo-finance/ticker/[^/]+/dividends$'
  '^GET:/yahoo-finance/ticker/[^/]+/earnings$'
  '^GET:/yahoo-finance/ticker/[^/]+/earnings-dates$'
  '^GET:/yahoo-finance/ticker/[^/]+/financials$'
  '^GET:/yahoo-finance/ticker/[^/]+/funds$'
  '^GET:/yahoo-finance/ticker/[^/]+/history$'
  '^GET:/yahoo-finance/ticker/[^/]+/history-metadata$'
  '^GET:/yahoo-finance/ticker/[^/]+/holders$'
  '^GET:/yahoo-finance/ticker/[^/]+/info$'
  '^GET:/yahoo-finance/ticker/[^/]+/isin$'
  '^GET:/yahoo-finance/ticker/[^/]+/news$'
  '^GET:/yahoo-finance/ticker/[^/]+/options$'
  '^GET:/yahoo-finance/ticker/[^/]+/options/[^/]+$'
  '^GET:/yahoo-finance/ticker/[^/]+/quote$'
  '^GET:/yahoo-finance/ticker/[^/]+/sec-filings$'
  '^GET:/yahoo-finance/ticker/[^/]+/shares$'
  '^GET:/yahoo-finance/ticker/[^/]+/shares-full$'
  '^GET:/yahoo-finance/ticker/[^/]+/splits$'
  '^GET:/yahoo-finance/ticker/[^/]+/sustainability$'
  '^GET:/yahoo-finance/ticker/[^/]+/valuation$'
  '^GET:/yahoo-finance/trending/[^/]+$'
  '^GET:/yahoo-health/article$'
  '^GET:/yahoo-health/category$'
  '^GET:/yahoo-health/home$'
  '^GET:/yahoo-life/article$'
  '^GET:/yahoo-life/home$'
  '^GET:/yahoo-news/article$'
  '^GET:/yahoo-news/category$'
  '^GET:/yahoo-news/comments$'
  '^GET:/yahoo-news/comments/replies$'
  '^GET:/yahoo-news/home$'
  '^GET:/yahoo-news/related$'
  '^GET:/yahoo-news/suggest$'
  '^GET:/yahoo-search/images$'
  '^GET:/yahoo-search/local$'
  '^GET:/yahoo-search/news$'
  '^GET:/yahoo-search/search$'
  '^GET:/yahoo-search/suggest$'
  '^GET:/yahoo-search/videos$'
  '^GET:/yahoo-shopping/article$'
  '^GET:/yahoo-shopping/category$'
  '^GET:/yahoo-shopping/home$'
  '^GET:/yahoo-shopping/shopping-list$'
  '^GET:/yahoo-shopping/shopping-lists$'
  '^GET:/yahoo-shopping/store$'
  '^GET:/yahoo-shopping/stores$'
  '^GET:/yahoo-sports/game$'
  '^GET:/yahoo-sports/golf-leaderboard$'
  '^GET:/yahoo-sports/golf-schedule$'
  '^GET:/yahoo-sports/mma-fight-card$'
  '^GET:/yahoo-sports/mma-schedule$'
  '^GET:/yahoo-sports/motorsports-race$'
  '^GET:/yahoo-sports/motorsports-schedule$'
  '^GET:/yahoo-sports/news$'
  '^GET:/yahoo-sports/olympics-medals$'
  '^GET:/yahoo-sports/player$'
  '^GET:/yahoo-sports/scoreboard$'
  '^GET:/yahoo-sports/standings$'
  '^GET:/yahoo-sports/team$'
  '^GET:/yahoo-sports/team-roster$'
  '^GET:/yahoo-sports/team-schedule$'
  '^GET:/yahoo-sports/tennis-rankings$'
  '^GET:/yahoo-sports/tennis-schedule$'
  '^GET:/yahoo-sports/tennis-scoreboard$'
  '^GET:/yahoo-tech/article$'
  '^GET:/yahoo-tech/category$'
  '^GET:/yahoo-tech/home$'
  '^GET:/yandex/search$'
  '^GET:/yandex/suggest$'
  '^GET:/yardbarker/article$'
  '^GET:/yardbarker/author$'
  '^GET:/yardbarker/headlines$'
  '^GET:/yardbarker/news$'
  '^GET:/yardbarker/sections$'
  '^GET:/yelp/business/[^/]+$'
  '^GET:/yelp/business/[^/]+/menu$'
  '^GET:/yelp/business/[^/]+/photos$'
  '^GET:/yelp/business/[^/]+/reviews$'
  '^GET:/yelp/business/[^/]+/reviews/highlights$'
  '^GET:/yelp/business/[^/]+/reviews/search$'
  '^GET:/yelp/geocode$'
  '^GET:/yelp/search$'
  '^GET:/yoox/categories$'
  '^GET:/yoox/designers$'
  '^GET:/yoox/product$'
  '^GET:/yoox/search$'
  '^GET:/youtube/captions/[^/]+$'
  '^GET:/youtube/channel/[^/]+/playlists$'
  '^GET:/youtube/channel/[^/]+/search$'
  '^GET:/youtube/channel/[^/]+/shorts$'
  '^GET:/youtube/channel/[^/]+/videos$'
  '^GET:/youtube/comments/[^/]+$'
  '^GET:/youtube/playlist/[^/]+$'
  '^GET:/youtube/profile/[^/]+$'
  '^GET:/youtube/search$'
  '^GET:/youtube/suggest$'
  '^GET:/youtube/tag/[^/]+$'
  '^GET:/youtube/transcript/[^/]+$'
  '^GET:/youtube/transcript/[^/]+/languages$'
  '^GET:/youtube/video/[^/]+$'
  '^GET:/zalando/categories$'
  '^GET:/zalando/category$'
  '^GET:/zalando/markets$'
  '^GET:/zalando/product$'
  '^GET:/zalando/search$'
  '^GET:/zalando/suggest$'
  '^GET:/zappos/brand$'
  '^GET:/zappos/brands$'
  '^GET:/zappos/product/[^/]+$'
  '^GET:/zappos/search$'
  '^GET:/zappos/suggest$'
  '^GET:/zara/categories$'
  '^GET:/zara/category/[^/]+/products$'
  '^GET:/zara/product/[^/]+$'
  '^GET:/zara/search$'
  '^GET:/zara/stores$'
  '^GET:/zara/suggest$'
  '^GET:/zaxbys/menu$'
  '^GET:/zaxbys/nearby$'
  '^GET:/zaxbys/store$'
  '^GET:/zdnet/article$'
  '^GET:/zdnet/author$'
  '^GET:/zdnet/headlines$'
  '^GET:/zdnet/news$'
  '^GET:/zdnet/sections$'
  '^GET:/zillow/autocomplete$'
  '^GET:/zillow/property/[^/]+$'
  '^GET:/zillow/search$'
  '^GET:/zomato/cities$'
  '^GET:/zomato/collection$'
  '^GET:/zomato/collections$'
  '^GET:/zomato/restaurant$'
  '^GET:/zomato/restaurant/menu$'
  '^GET:/zomato/search$'
  '^POST:/agoda/flights/itinerary-amenities$'
  '^POST:/developer/search$'
  '^POST:/ebay/search$'
  '^POST:/expedia/activities/search$'
  '^POST:/expedia/flights/search$'
  '^POST:/expedia/locations/search$'
  '^POST:/expedia/properties/detail$'
  '^POST:/expedia/properties/filters$'
  '^POST:/expedia/properties/reviews$'
  '^POST:/expedia/properties/search$'
  '^POST:/google/jobs$'
  '^POST:/google/map/search$'
  '^POST:/google/news$'
  '^POST:/google/trends/explore$'
  '^POST:/google/trends/explore/interest-by-region$'
  '^POST:/google/trends/explore/interest-over-time$'
  '^POST:/google/trends/explore/related-topics$'
  '^POST:/google/trends/explore/rising-queries$'
  '^POST:/google/trends/explore/top-queries$'
  '^POST:/google/trends/trending/detail$'
  '^POST:/hotels/offers$'
  '^POST:/hotels/property$'
  '^POST:/hotels/rates$'
  '^POST:/hotels/reviews$'
  '^POST:/hotels/reviews/archive$'
  '^POST:/hotels/search$'
  '^POST:/polymarket/tokens/midpoints$'
  '^POST:/polymarket/tokens/orderbooks$'
  '^POST:/polymarket/tokens/prices$'
  '^POST:/polymarket/tokens/spreads$'
  '^POST:/research/jobs$'
  '^POST:/research/jobs/[^/]+/cancel$'
  '^POST:/research/papers/read$'
  '^POST:/research/papers/related$'
  '^POST:/shein/products/aggregation-filters$'
  '^POST:/shein/products/search$'
  '^POST:/shein/search/autocomplete$'
  '^POST:/shein/search/keywords$'
  '^POST:/starbucks/product/[^/]+/[^/]+/nutrition$'
  '^POST:/vrbo/search$'
  '^POST:/web/crawl$'
  '^POST:/web/crawl/[^/]+/cancel$'
  '^POST:/web/map$'
  '^POST:/web/search$'
  '^POST:/yahoo-finance/download$'
  '^POST:/yahoo-finance/screener$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this crawlora route" >&2
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

if [ "$method" = "GET" ]; then
  # -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
  qs=()
  for kv in ${rest[@]+"${rest[@]}"}; do
    [ -n "$kv" ] || continue
    # curl treats both @file and name@file forms as local-file input for
    # --data-urlencode. Reject @ outright so query arguments cannot disclose
    # local files to the Crawlora API.
    case "$kv" in
      *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
    esac
    qs+=(--data-urlencode "$kv")
  done
  # -q must be the first curl option: ignore any user ~/.curlrc so inherited
  # config cannot redirect the request, add uploads, or alter credential use.
  curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"
else
  [ -n "$body" ] || body="${rest[0]:-}"
  [ -n "$body" ] || body='{}'
  # Stream the body on stdin so curl never interprets a user value as its
  # @file shorthand (and cannot read local files supplied in a request body).
  printf '%s' "$body" | curl -q -fsS -X "$method" "${auth[@]}" \
    -H "Content-Type: application/json" --data-binary @- "${base}${path}"
fi
