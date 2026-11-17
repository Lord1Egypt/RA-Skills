# Apiguru endpoint reference

Generated from the API spec - do not edit by hand.

- Base URL: `https://agent.apiguru.app/agent/v1`, keyless or with an API key in the `X-API-KEY` header (what `scripts/probe.py` uses either way; `limit`, `compact` and `fields` apply to both)
- Also keyed: `https://dash.apiguru.app/api/v1` (send `X-API-KEY`; full answers, no `limit`, `compact` or `fields`)

All endpoints are `GET` with query parameters.

## Marketplaces

Pass as `geo`, chosen from the user's request or the Amazon domain they mention (amazon.de -> DE). The API assumes `US` only when the parameter is omitted; do not rely on that default.

| Code | Domain |
|---|---|
| `US` | amazon.com |
| `CA` | amazon.ca |
| `DE` | amazon.de |
| `MX` | amazon.com.mx |
| `UK` | amazon.co.uk |
| `FR` | amazon.fr |
| `IT` | amazon.it |
| `ES` | amazon.es |
| `AU` | amazon.com.au |
| `BR` | amazon.com.br |
| `IN` | amazon.in |
| `JP` | amazon.co.jp |
| `NL` | amazon.nl |
| `AE` | amazon.ae |
| `PL` | amazon.pl |
| `SA` | amazon.sa |
| `SG` | amazon.sg |
| `SE` | amazon.se |
| `TR` | amazon.com.tr |
| `BE` | amazon.com.be |
| `IE` | amazon.ie |
| `ZA` | amazon.co.za |
| `EG` | amazon.eg |

## `GET /v2/product-details`

Use for one product's current listing. Not for several ASINs (product_details_batch), seller offers or stock (offers_stock), or review text (product_reviews). Fetches the complete product record for one ASIN on one marketplace: title, price, star rating, rating count, images, description, feature bullets, variations and category.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `asin` | string | yes | Single Amazon ASIN, 10 uppercase alphanumeric characters. Exactly one - comma-separated lists are rejected; use product_details_batch for many. |
| `geo` | enum | no | Marketplace country code. Default `US`. |

> 404 means the ASIN is absent from that marketplace and IS billed. 503 is a temporary failure on our side and is NOT billed - retry. Bullet points and specs are what Amazon shows for the listing; on multi-variant listings they can describe the product family rather than the exact variant. A null field means Amazon did not show it. Beside the price the record carries what the page shows there: `discount_percentage` (the saving against `product_original_price`, an integer), `product_price_per_unit` ("$0.59/fluid ounce"), `deal_badge` ("Limited time deal"), `coupon` and `promotion` in the page's own words, and `subscribe_and_save` -- `{price, price_per_unit, max_savings_price, max_savings_percentage}`, null when the listing has no such option. `return_policy` is the buy box's Returns line ("FREE refund/replacement until Jan 31, 2027"), and `buybox_winner.seller_url` is the seller's page. Three things a listing states are named at the top level: `whats_in_the_box` (the page's "What's in the box" list, an array of strings), `warranty` ("1 year manufacturer") and `ingredients` (the ingredient list as the page prints it); each is null when the listing states none. `product_information` still holds the same rows under the page's own labels. `product_photos` is this listing's whole gallery at full size, in the page's order (it used to hold one image, or thumbnails); other variants' images stay under `variation`. A page that comes back with no product on it is fetched again and, failing that, answered as the unbilled 503 -- never as an empty record. Keys of `product_information`, `tech_specs` and the other specification tables are trimmed: Amazon prints some rows twice, once with a trailing space ("Package Dimensions "), and the copies are merged under the clean name; when they differ the listing's own value wins (the second copy of "ASIN" on a variant often names the parent).

## `GET /v2/product-reviews`

Use for what customers say about one product. Not for its full review history (Amazon serves full and star-filtered review lists only to signed-in accounts) or for seller feedback (seller_reviews). Returns the overall rating, rating count, review_histogram (percent of all ratings per star), Amazon's 'customers say' AI summary where that marketplace shows one, and the reviews on the product page (typically up to 8 from this marketplace and 5 from other countries), each with rating, review_date, review_country, from_this_marketplace, verified flag and helpful_votes; from_rating/to_rating keep a star window.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `asin` | string | yes | Single Amazon ASIN, 10 uppercase alphanumeric characters. |
| `geo` | enum | no | Marketplace country code. Default `US`. |
| `from_rating` | integer | no | Lowest star rating to include, 1-5. Filters the reviews the product page shows (see review_coverage). |
| `to_rating` | integer | no | Highest star rating to include, 1-5. from_rating=1&to_rating=3 keeps the critical ones among them. |

> Same 404-billed / 503-not-billed semantics as product_details. No paging or sort: the reviews are those on the product page; review_coverage says how many and from where. from_rating/to_rating filter them. review_histogram (here and on product_details) gives the share of every rating. customers_say is null where Amazon shows no summary (several marketplaces never do); customers_say_note then says so.

## `GET /search`

Use to find products by keyword and filters. Rows are result snippets; for the authoritative record of one ASIN call product_details. Search Amazon products by keyword. Filters: page, sort_by, category_id (browse node), min_price / max_price (decimals), product_condition (NEW / USED / RENEWED), brand, seller_id, today_deals and deal_type (coupons, all_discounts, buy_more_save_more). Every answer carries filters_applied, filters_ignored (with the reason) and available_filters for that marketplace.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `query` | string | yes | Search keywords. Required and must be non-empty. |
| `page` | integer | no | Result page, 1-based. metadata.total_pages says how far it goes. Default `1`. |
| `geo` | enum | no | Marketplace country code. Default `US`. |
| `sort_by` | enum | no | Result ordering. Default `RELEVANCE`. |
| `category_id` | string | no | Amazon browse node id to restrict to, e.g. 172282 (Electronics on US). Take one from a best_sellers answer's available_subcategories, a product's category_path, or node= in an Amazon URL. Ids differ per marketplace. |
| `min_price` | number | no | Lowest price, in the marketplace currency; decimals such as 19.99 are fine. |
| `max_price` | number | no | Highest price, in the marketplace currency. |
| `product_condition` | enum | no | NEW, USED or RENEWED (case-insensitive). Applied with the marketplace's own condition node; where a marketplace does not offer one, the answer's filters_ignored says so and available_filters lists what it does offer. USED lists products that have a used offer: `product_price` stays the featured offer's price (usually a new item's) and `product_minimum_offer_price` is the lowest price among the listing's other offers. |
| `brand` | string | no | Brand name as Amazon spells it (case-insensitive), e.g. Samsung. |
| `seller_id` | string | no | Restrict results to one seller's offers: an Amazon seller id, 'A' followed by 9-20 letters and digits (e.g. A2A1RNLLUK3HYA). |
| `today_deals` | boolean | no | Only items in Today's Deals, using that marketplace's own refinement. Where a marketplace has none (amazon.fr on 2026-09-08) it is reported under filters_ignored. Default `False`. |
| `deal_type` | enum | no | A specific promotion refinement: today_deals, all_discounts, coupons or buy_more_save_more. available_filters.deal_type lists the ones this marketplace has. |

`sort_by` accepts: `RELEVANCE`, `BEST_SELLERS`, `LOW_HIGH_PRICE`, `HIGH_LOW_PRICE`, `REVIEWS`, `NEWEST`

`product_condition` accepts: `NEW`, `USED`, `RENEWED`

`deal_type` accepts: `today_deals`, `all_discounts`, `coupons`, `buy_more_save_more`

> Blank values and the literal string 'null' are treated as unset. Invalid page, sort_by, price, product_condition or deal_type is a free 400 naming the parameter and the allowed values. Condition and deal refinements are per marketplace; a marketplace that lacks one gets the unfiltered feed plus an entry under filters_ignored, never a silent empty page. `product_num_ratings` is an integer; `offers_count` is the "N offers" count a result card shows, an integer, and null when the card shows none (most cards; it used to default to 1; "21+ used & new offers" reads 21); `product_minimum_offer_price` is the price on the card's "More Buying Choices" line -- the lowest among the listing's other offers, new or used -- a decimal string, null when the card shows no such line; under product_condition=USED the answer carries `price_note`, which says which price is which, and offers_stock with the USED_* conditions returns the used offers themselves; `product_brand` is the brand line Amazon prints above some titles (fashion and many branded listings) and null on cards without one -- product_details has `brand_name` for every ASIN; `product_star_rating`, `product_price` and `product_original_price` are decimal strings; a null field means Amazon did not show it. `is_prime` is true when the result carries a Prime badge or its delivery line offers Prime delivery. `metadata.reachable_pages` says how far `page` can go: Amazon serves at most 7 pages of a query even when `metadata.total_pages` counts more (then `pagination_note` says how to split the query). `metadata.next_page` is the page to ask for next (null on the last one) and `_links.next` its link; each row's `position` is its place on this page, from 1, sponsored rows counted as Amazon lists them; a page past the end is a free 400 `page_out_of_range`. A full page is up to 48 results and about 54 KB; the tool returns the first 10 as light rows by default and the answer carries `_truncated`, `_omitted_fields`, `_projection` and `_notes`. filters_applied echoes the effective sort_by (RELEVANCE when none was sent). A BEST_SELLERS ordering is Amazon's query-scoped popularity, not a category rank: a row's `badges` / `is_best_seller` are what the result card showed for this query, and an ASIN that is #1 in its subcategory can carry no badge here while product_details reports best_seller=true with the rank. For a rank claim, use product_details or best_sellers. An empty `products` list is served as success only when Amazon itself reports 0 results (metadata.total is 0 and `hint` says so). Anything else that is not a usable result is an unbilled, retryable 503 with code upstream_unavailable.

## `GET /product`

Use to enrich a list of ASINs in one call; compare the ASINs in `results` with the ones you sent. Batch variant of product_details. Accepts a comma-separated ASIN list, deduplicates it, and fetches all of them concurrently. Far cheaper and faster than N single calls.

**Price:** $0.0024 per item (max 20)

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `asins` | string | yes | Comma-separated ASIN list, maximum 20 after de-duplication. Each must be 10 uppercase alphanumeric characters. |
| `geo` | enum | no | Marketplace country code. Default `US`. |

> Billed per ASIN processed, including ones that come back not-found. More than 20 ASINs returns 413. Bullet points and specs are what Amazon shows for the listing; on multi-variant listings they can describe the product family rather than the exact variant. A null field means Amazon did not show it. ASINs Amazon has no record for on that marketplace are listed in not_returned (billed, like a not-found product_details call; retrying will not help). The batch record comes from Amazon's app, not the product page: price, rating, availability, images, bullets and variants, but no best-seller ranks, no category path and no merchant (seller) id. For those call product_details per ASIN. On an API key both cost one request per ASIN, so the batch saves calls and time, not money; keyless (x402) it is also cheaper per item. Compact rows carry brand, weight {raw, unit, value} and dimension {length, width, height, unit, raw} in product_details' shape, read from the row's product_attributes (package dimensions first); outside amazon.com Amazon's app prints centimetres under an inches label, so there dimension.unit is cm while raw keeps Amazon's text.

## `GET /stock`

Use to compare sellers' current offers and see who holds the buy box, and, with check_inventory, how many units a buyer can add to the cart now. The stock number is not a sales estimate. Not for the listing's own details (product_details). Returns the current offer list per ASIN (seller, price, condition, buy-box winner) and, optionally, the actual purchasable stock quantity. The whole offer list comes by default; `page` returns it ten offers at a time.

**Price:** $0.0045 per item (max 10)

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `asins` | string | yes | Comma-separated ASIN list, maximum 10. Each must be 10 uppercase alphanumeric characters; malformed entries are rejected with 400. |
| `geo` | enum | no | Marketplace country code. Default `US`. |
| `check_inventory` | boolean | no | Add each offer's purchasable stock quantity (`inventory_response`), read with a cart check. Slower, and each check that reads a quantity is billed, so leave off unless you need the number. Default `False`. |
| `offers_count` | string | no | 'all' for every offer (default), 'winner' for the buy-box offer only, or a specific alphanumeric Offer ID. Every offer carries is_buybox_winner; with 'winner' the per-ASIN data holds that one offer and offers_total says how many exist. An ASIN with no featured offer answers an empty list with an explanatory error. The response echoes filters_applied. Default `all`. |
| `condition` | string | no | Comma-separated condition filter: ALL, NEW, USED_LIKE_NEW, USED_VERY_GOOD, USED_GOOD, USED_ACCEPTABLE (case-insensitive). Omit for every offer. The filter covers the buy-box offer too: it is in the answer only when its own condition is among those asked for. An unknown value is a free 400 listing the allowed ones; it used to be silently treated as ALL. |
| `page` | integer | no | One page of each ASIN's offer list instead of the whole list. Amazon lists ten offers a page, in its own order (it starts from the lowest price with delivery); page 1 also carries the buy-box offer. One request per ASIN whatever the listing's size, and each row then says `page` and `total_pages`. Omit for the whole list, which is one request per page of ten. |

> On an account, a call is billed per page of the offer list it delivers, plus the cart checks of check_inventory. Amazon lists ten offers a page, so an ASIN with up to ten offers is one request and each further page of its list is one more (a listing with 35 offers: 4). `page` (1, 2, ...) returns that page alone for one request per ASIN -- page 1 is the buy-box offer and the first ten of the list -- and each row then carries `page` and `total_pages`. A page past the end is answered like a not-found item: code `page_out_of_range`, billed, with `total_pages` and `offers_total` in the row; `total_pages` on any page says how far to go, so there is no need to ask. Without `page` the whole list comes, up to 10 pages (100 offers and the buy-box offer); a longer list says so in `coverage_note`, and `page=11` onward reaches the rest. `offers_total` is Amazon's own count of the offers under the condition filter, not the number returned; when fewer are returned, `coverage_note` says why (a page that could not be read this time, the 10-page limit, or offers that cannot be added to a cart). A condition filter covers the buy-box offer too: it is in the answer only when its own condition was asked for. offers_count=winner returns only the offer flagged is_buybox_winner (offers_total keeps the full count); it used to scope only the inventory check and return every offer. /scrape is a legacy alias for the same handler. When Amazon will not return the offer list for an ASIN, the result carries source=product_page: the featured (buy-box) offer read from the product page, offers_on_amazon (how many offers Amazon says exist) and a note; other sellers' offers and stock are then not included. With check_inventory, a cart check that cannot read a quantity is retried once on another session; one that still fails says so on the offer, inventory_response {"error": "cart check failed", "code": "cart_check_failed", "retryable": true}, is not billed, and never reads as a quantity of 0. An offer whose price Amazon shows only in the cart ("Add to cart to see product details") has `price` null and `price_hidden` true; it used to read as price 0. Each offer carries `ships_from` (the "Ships from" name: Amazon for FBA, else the seller), `delivery_message` (the offer's own delivery promise, e.g. "FREE delivery Friday, October 16 on orders shipped by Amazon over $35") and `delivery_message_secondary` (the "Or fastest delivery ..." line), null when the offer shows none. `delivery` is the same value as `ships_from`, kept for existing integrations; it never held delivery information. A row for an ASIN that could not be answered carries `error`, `code`, `http_status`, `billed`, `retryable` and `next_step`, like a top-level error: `upstream_unavailable` (not billed, retry that ASIN), `no_offers` ("No offers found": the offer list holds no offer that can be bought as is -- customizable listings have none; billed like a 404) or `asin_redirected` (Amazon answers the ASIN with another listing's offers; billed like a 404). On agent.apiguru.app the answer also carries `success` and `_links` (self, and `details_url` per row); `billable_requests_count` is there on your own key only.

## `GET /v2/best-sellers`

Use for what sells best in a department right now. The rank is Amazon's, not a sales figure. Best-seller rankings for a department of one marketplace, 50 per page. Every answer carries the department it resolved to and how (category_resolution: by slug, name or a fragment of a name, with a hint when a fragment such as 'shoes' landed on the whole 'Clothing, Shoes & Jewelry' department, or 'subcategory' when a word such as 'camera' named a subcategory), available_categories (that marketplace's departments with slugs; MCP: with compact=false) and available_subcategories (the children of the node shown, with the ids subcategory_code takes). On amazon.com subcategory_code also takes any browse node id at any depth, or a name resolved under the department ("women's shoes", "mules & clogs"); category.subcategory_path gives the node's full path and category.heading the page's own title line.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `category` | string | no | Best-seller department, by slug or by name as Amazon shows it for that marketplace (case-insensitive; a unique fragment works, and the answer's category_resolution says when a fragment was used -- 'shoes' is the whole 'Clothing, Shoes & Jewelry' department, and the hint then lists the Shoes subcategories with their ids). Departments and their slugs differ per marketplace: amazon.com has electronics, amazon.de has ce-de (Electronics & Photo). A word that names a subcategory works too: category=camera on amazon.es is Electronics > Camera & Photo (category_resolution.via says 'subcategory'; several equally good matches are a free 400 listing each as category + subcategory_code). REST answers list the marketplace's departments under available_categories (the MCP tool with compact=false); an unknown name is a free 400 listing them. Default `appliances`. |
| `subcategory_code` | string | no | Browse node id under `category`: one from available_subcategories of a previous answer, or on amazon.com any node id at any depth (679410011 is Women > Shoes > Mules & Clogs) or a name resolved under the department ("women's shoes", "mens boots", "mules & clogs"). A name that fits two nodes equally (Men > Shoes > Boots and Women > Shoes > Boots) is a free 400 listing both ids with their paths. |
| `page` | integer | no | Result page, 1-based, 50 rows each; Amazon's lists stop at page 5. Default `1`. |
| `geo` | enum | no | Marketplace country code. Default `US`. |

> No required parameters - calling it bare returns US appliances page 1. `category` accepts a slug, a display name, one of the older US department names, or a unique fragment; category_resolution.via says which, and a fragment match adds a hint naming the subcategories that carry the word, with ids. On amazon.com the whole browse tree is known: subcategory_code takes any node id or a name at any depth, subcategory_name and subcategory_path are filled without a fetch, and available_subcategories lists the node's real children (empty on a leaf). Other marketplaces name only what their navigation showed. page is capped at 5 (a 400 beyond, not a 500). `rank` is the position within the requested list on this page. Rows are the same for every marketplace; only the department vocabulary differs, and the answer carries it.

## `GET /v2/deals`

Use for items currently promoted in Amazon's deals feed. Not for one product's price (product_details); for a brand by name use search with brand= and today_deals=true. Returns the current Amazon deals feed: ASIN, title, deal price, list price, discount, deal badge, start/end time and product links. Filter by department (categories), brand id (brands), rating cut-off, price bounds, minimum discount and Prime program. Every answer carries available_filters (the category and brand ids this marketplace accepts, with names), filters_applied / filters_ignored (what took effect) and next_offset (the next page, null when the feed ends).

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `geo` | enum | no | Marketplace country code. Default `US`. |
| `offset` | integer | no | Row to start at. A page is 30 rows; pass the previous answer's next_offset for the next page. Default `0`. |
| `categories` | string | no | Department to restrict to: its id from available_filters.categories, or its name as Amazon shows it for that marketplace (case-insensitive; a unique fragment such as "electronics" works). US departments: Amazon Devices & Accessories, Appliances, Arts Crafts & Sewing, Audible Books & Originals, Automotive, Baby Products, Beauty & Personal Care, Books, CDs & Vinyl, Cell Phones & Accessories, Clothing Shoes & Jewelry, Collectibles & Fine Art, Electronics, Everything Else, Grocery & Gourmet Food, Handmade Products, Health & Household, Home & Kitchen, Industrial & Scientific, Kindle Store, Movies & TV, Musical Instruments, Office Products, Patio Lawn & Garden, Pet Supplies, Software, Sports & Outdoors, Tools & Home Improvement, Toys & Games, Video Games. Other marketplaces use their own localised names -- read them from available_filters.categories of any deals answer for that geo. An unknown name is a free 400 listing the valid names. |
| `brands` | string | no | Comma-separated brand ids, e.g. 46655 for Samsung on US. Take them from brand_id on any deals row or from available_filters.brands (the brands present in the current result). Names resolve only when this marketplace has already shown that brand; for a brand by name use /search with brand=<name> and today_deals=true instead. |
| `min_product_star_rating` | enum | no | Amazon's deals feed offers one rating cut-off: 4 = four stars and up. ALL or omitted = no cut-off. Other values are rejected with a free 400. |
| `min_price` | number | no | Lowest deal price to return, in the marketplace currency. Applied to the fetched rows; see notes. |
| `max_price` | number | no | Highest deal price to return, in the marketplace currency. |
| `min_discount` | integer | no | Smallest discount percentage to return, e.g. 50 for half price or better. |
| `max_discount` | integer | no | Largest discount percentage to return. |
| `prime_exclusive` | boolean | no | Only deals in Amazon's Prime Exclusive program. Default `False`. |
| `prime_early_access` | boolean | no | Only Prime Early Access deals. A marketplace lists the programs it is running under available_filters.prime_programs; when Early Access is not running the answer is empty with a hint saying so. Default `False`. |

`min_product_star_rating` accepts: `4`, `ALL`

> Filters are by id: categories takes a department id or name, brands takes brand ids only; available_filters in every answer lists both with names, and filters_applied / filters_ignored report what Amazon honoured. A page is 30 rows; page with offset=next_offset (null when exhausted); total_count caps at 500. min_price, max_price, min_discount and max_discount are applied to the rows after retrieval, scanning up to 3 feed pages per call, so a page can hold fewer than 30 rows and total_count does not reflect them. An empty answer carries a hint saying why. Deal prices expire: check deal_ends_at. The older price_range and discount_range parameters are still accepted, as buckets (1-5 = under 25 / 25-50 / 50-100 / 100-200 / 200 and up; 1-4 = 10 / 25 / 50 / 70 percent off or more) or as bands such as 25-50 and 70+.

## `GET /seller-profile`

Use to vet sellers: name, rating and feedback counts as Amazon displays them. Returns the storefront profile for each seller id: business name, rating, feedback counts, address and marketplace presence.

**Price:** $0.0036 per item (max 10)

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `seller_ids` | string | yes | Comma-separated seller IDs, maximum 10. Each must be an Amazon seller id -- 'A' followed by 9-20 letters and digits, e.g. A2A1RNLLUK3HYA -- or the whole call 400s. |
| `geo` | enum | no | Marketplace country code. Default `US`. |

> Seller ID validation is all-or-nothing: one malformed id rejects the entire request with 400. Every row in results is an object with `status`: `ok` (the profile), `not_found` (Amazon has no page for that id on this marketplace; billed, like a 404) or `unavailable` (could not be retrieved right now; NOT billed on the keyed path, `retryable: true`). A row is never null. billable_requests_count counts ok + not_found rows; on the pay-per-call rail the per-item quote is settled up front, so retry `unavailable` ids in a separate call rather than expecting a partial refund. On agent.apiguru.app the answer also carries `success` and `_links.self`; `billable_requests_count` is there on your own key only.

## `GET /v2/seller-products`

Use to list one seller's storefront. Products listed by a seller: a storefront search. Takes the same filters as search -- query, page, sort_by, category_id, min_price / max_price, product_condition, brand, today_deals, deal_type -- and answers with filters_applied, filters_ignored and available_filters like search does.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `seller_id` | string | yes | Amazon seller id whose storefront to list: 'A' followed by 9-20 letters and digits, the seller= or me= value of a storefront URL (e.g. A2A1RNLLUK3HYA). Required. |
| `query` | string | no | Optional keywords to search within this seller's storefront. |
| `page` | integer | no | Result page, 1-based. metadata.total_pages says how far it goes. Default `1`. |
| `geo` | enum | no | Marketplace country code. Default `US`. |
| `sort_by` | enum | no | Result ordering. Default `RELEVANCE`. |
| `category_id` | string | no | Amazon browse node id to restrict to, e.g. 172282 (Electronics on US). Take one from a best_sellers answer's available_subcategories, a product's category_path, or node= in an Amazon URL. Ids differ per marketplace. |
| `min_price` | number | no | Lowest price, in the marketplace currency; decimals such as 19.99 are fine. |
| `max_price` | number | no | Highest price, in the marketplace currency. |
| `product_condition` | enum | no | NEW, USED or RENEWED (case-insensitive). Applied with the marketplace's own condition node; where a marketplace does not offer one, the answer's filters_ignored says so and available_filters lists what it does offer. |
| `brand` | string | no | Brand name as Amazon spells it (case-insensitive), e.g. Samsung. |
| `today_deals` | boolean | no | Only items in Today's Deals, using that marketplace's own refinement. Where a marketplace has none (amazon.fr on 2026-09-08) it is reported under filters_ignored. Default `False`. |
| `deal_type` | enum | no | A specific promotion refinement: today_deals, all_discounts, coupons or buy_more_save_more. available_filters.deal_type lists the ones this marketplace has. |

`sort_by` accepts: `RELEVANCE`, `BEST_SELLERS`, `LOW_HIGH_PRICE`, `HIGH_LOW_PRICE`, `REVIEWS`, `NEWEST`

`product_condition` accepts: `NEW`, `USED`, `RENEWED`

`deal_type` accepts: `today_deals`, `all_discounts`, `coupons`, `buy_more_save_more`

> A malformed seller_id is a free 400, as on seller_profile_batch. metadata.total_pages counts every page of the result (48 rows a page), but Amazon serves at most 7 pages of one query: metadata.reachable_pages is how far page can go, and when it is less, pagination_note says how to see the rest (min_price/max_price bands or category_id). _links.next is the next page while there is one; a page past the end is a free 400 page_out_of_range. Invalid sort_by, price, product_condition or deal_type is a free 400 that lists the allowed values. No single sort order lists a whole storefront: Amazon's relevance order (the default) can count far fewer products than the store holds and repeats products across pages, and other orders include products it leaves out (measured on one store: relevance 321, NEWEST 1,898; on another, relevance and NEWEST shared 90 of 161 products). Page 1 of a storefront without `query` carries `coverage_note` with the recipe: page through sort_by=RELEVANCE and sort_by=NEWEST, split a store larger than 336 products into min_price/max_price bands, dedupe by asin. An empty storefront carries `note`: Amazon reports 0 products for a seller with no listings on that marketplace and for an id that is not a seller alike, so check it with seller_profile_batch (`_links.seller_profile`). Rows have the search row shape: `offers_count` is null unless the card shows a count, and `product_brand` is null on most storefront cards (Amazon prints no brand line there; product_details has `brand_name`). Rows carry `position` (their place on this page, from 1) and metadata carries `next_page`, as on search.

## `GET /v2/seller-reviews`

Use for a seller's customer feedback (service, shipping). Not for product reviews (product_reviews). Returns paginated seller feedback, optionally filtered to a star-rating window.

**Price:** $0.003 per call

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `seller_id` | string | yes | Amazon seller id: 'A' followed by 9-20 letters and digits, the seller= or me= value of a storefront URL (e.g. A2A1RNLLUK3HYA). Required. |
| `page` | integer | no | Result page, 1-based, 5 reviews a page; has_next_page in the answer says whether another exists. Default `1`. |
| `from_rating` | integer | no | Lowest star rating to include, 1-5. |
| `to_rating` | integer | no | Highest star rating to include, 1-5. |
| `geo` | enum | no | Marketplace country code. Default `US`. |

> from_rating and to_rating are optional; omit both for unfiltered feedback. A page holds 5 reviews and the answer carries current_page and has_next_page; Amazon exposes no total, so page until has_next_page is false (up to page 100).

## Formats

- ASIN: `^[A-Z0-9]{10}$` - On agent.apiguru.app and the MCP server any case is accepted and upper-cased, and an Amazon product URL (/dp/ASIN, /gp/product/ASIN, ?asin=) works in place of an ASIN; its domain sets geo unless geo names another marketplace (then 400). The answer lists what was rewritten under parameters_interpreted (MCP: _input_interpreted).
- Seller ID: `^[Aa][A-Za-z0-9]{9,20}$` - An Amazon seller id is 'A' followed by 9-20 letters and digits (10-21 characters in all) -- the seller= or me= value of a storefront URL, e.g. A2A1RNLLUK3HYA. Anything else is rejected with 400 before any fetch.
- Sample ASIN for testing: `B09DJLW458`
