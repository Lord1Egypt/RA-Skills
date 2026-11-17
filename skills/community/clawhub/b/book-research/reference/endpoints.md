# book-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**35 endpoints across 3 platform group(s).**

## Goodreads (10)

### `goodreads_author`

- **HTTP:** `GET /goodreads/author/{id}`
- **What:** Get a Goodreads author. Returns a Goodreads author profile: bio, birth/death dates, website, genres, photo, and aggregate rating stats.
- **Params:** `id` (string, **required**) — Goodreads author id

### `goodreads_author_books`

- **HTTP:** `GET /goodreads/author/{id}/books`
- **What:** List a Goodreads author's books. Lists the books of a Goodreads author by author `id`, about 30 per page; `page` is 1-based and defaults to 1. Each book has its `id`, title, author, average rating, ratings count and Goodreads URL, and the `id` can be used to look up the full book.
- **Params:** `id` (string, **required**) — Goodreads author id; `page` (integer, optional) — 1-based page number, default 1

### `goodreads_author_quotes`

- **HTTP:** `GET /goodreads/author/{id}/quotes`
- **What:** List a Goodreads author's attributed quotes. Returns an author's paginated attributed-quotes list (quote text, tags, like count, and — when the quote is credited to a specific book — that book's title, id, and work id).
- **Params:** `id` (string, **required**) — Goodreads author id; `page` (integer, optional) — 1-based page number, default 1

### `goodreads_book`

- **HTTP:** `GET /goodreads/book/{id}`
- **What:** Get a Goodreads book. Returns a Goodreads book: description, authors, series, genres, format, pages, publisher, publication date, ISBNs, and aggregate rating with the full 1-5 star distribution.
- **Params:** `id` (string, **required**) — Goodreads book id

### `goodreads_book_editions`

- **HTTP:** `GET /goodreads/book/{id}/editions`
- **What:** List a Goodreads book's editions. Returns a work's paginated edition list (per-edition book id, format, page count, publication date, publisher, ISBN/ISBN13/ASIN, language, and rating) — every other translation, printing, and format of the requested book id. Goodreads keys editions by a separate "work id", not the book id in the path; requests against a book with no editions data return an upstream error.
- **Params:** `id` (string, **required**) — Goodreads book id; `page` (integer, optional) — 1-based page number, default 1

### `goodreads_book_reviews`

- **HTTP:** `GET /goodreads/book/{id}/reviews`
- **What:** Get a Goodreads book's featured reviews. Returns a book's featured reviews (reviewer, rating, text, date, like/comment counts, spoiler flag), sorted by like count.
- **Params:** `id` (string, **required**) — Goodreads book id; `limit` (integer, optional) — Max reviews, default 10, max 50

### `goodreads_genre`

- **HTTP:** `GET /goodreads/genre/{name}`
- **What:** Get a Goodreads genre shelf. Returns up to 50 books on a Goodreads genre/shelf tag page (e.g. fantasy, romance, science-fiction), Goodreads' per-tag "top books" view: title, author, average rating, ratings count, publication year, and how many times the book was shelved under this specific tag. Goodreads' genre/shelf taxonomy is an open, user-generated folksonomy of thousands of tags, not a small fixed list, so there is no directory endpoint — pass any known tag slug, e.g. from a book's genres[] field or a value seen on goodreads.com. There is no pagination beyond the first 50.
- **Params:** `name` (string, **required**) — Goodreads genre/shelf tag

### `goodreads_list`

- **HTTP:** `GET /goodreads/list/{id}`
- **What:** Get a Goodreads Listopia list. Returns a Goodreads Listopia list (ranked book list) by id, paginated.
- **Params:** `id` (string, **required**) — Goodreads list id; `page` (integer, optional) — 1-based page number, default 1

### `goodreads_lists`

- **HTTP:** `GET /goodreads/lists`
- **What:** List curated Goodreads Listopia lists. Returns a catalog of well-known Goodreads Listopia lists (id, name, category). Goodreads has no directory or search endpoint for the tens of thousands of user-created lists, so this is served from a live popular-lists source when available, falling back to a curated, hand-picked catalog otherwise. Pass a returned id to GET /goodreads/list/{id} for that list's ranked book contents. Category enum: `general`, `genre`, `era`, `young_adult`, `children`, `holiday`.
- **Params:** _none_

### `goodreads_search`

- **HTTP:** `GET /goodreads/search`
- **What:** Search Goodreads books. Searches Goodreads for books by title or author using `q`, returning up to `limit` results (default 10, max 50). Each result has its id, title, author and author id, average rating, ratings count, page count, a truncated description, cover image URL and Goodreads URL. Only books are returned, not authors or lists.
- **Params:** `limit` (integer, optional) — Max results, default 10, max 50; `q` (string, **required**) — Search query

## AppleBooks (14)

### `apple_books_audiobook`

- **HTTP:** `GET /apple-books/audiobook/{id}`
- **What:** Retrieve Apple Books audiobook details. Returns audiobook metadata from Apple Books, including narrator, duration, audio preview, and a cross-link to the ebook edition (when one exists).
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric audiobook ID; `lang` (string, optional) — Result language tag

### `apple_books_audiobook_charts`

- **HTTP:** `GET /apple-books/audiobook/charts`
- **What:** Retrieve Apple Books audiobook chart rankings. Returns the 40 audiobook rows Apple currently serves in its paid top chart for one storefront. `genre_id` narrows the page using an ID from `GET /apple-books/genres?media=audiobook`. The upstream page has no free/paid selector or pagination.
- **Params:** `country` (string, optional) — Two-letter storefront code, default us; `genre_id` (string, optional) — Audiobook genre ID. Allowed values: 50000042, 50000043, 50000040, 50000049, 50000044, 50000051, 50000052, 50000053, 50000069, 50000055, 50000054, 50000056

### `apple_books_audiobook_reviews`

- **HTTP:** `GET /apple-books/audiobook/{id}/reviews`
- **What:** Retrieve Apple Books audiobook customer reviews. Returns a page of an audiobook's customer reviews. The default first page is served from the audiobook's own catalog page; deeper pages (page>1 or a larger limit) page through Apple's review API directly, up to 20 per page.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric audiobook ID; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Reviews per page, default 10, max 20; `page` (integer, optional) — Review page number, default 1

### `apple_books_audiobook_search`

- **HTTP:** `GET /apple-books/audiobook/search`
- **What:** Search Apple Books audiobooks. Searches Apple Books audiobooks by `term`, which is required. `country` is the two-letter storefront code (default `us`), `lang` a language tag such as `en-us`, `limit` the result count (default 50, max 200) and `page` starts at 1. Results include `narrator`, `duration_seconds`, price, rating, genres and `preview_url`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of audiobooks per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_books_audiobook_series`

- **HTTP:** `GET /apple-books/audiobook-series/{id}`
- **What:** Retrieve an Apple Books audiobook series and its full audiobook list. Returns series metadata and the full ordered list of audiobooks in the series from Apple Books' public catalog page. An audio-book-series is a catalog resource distinct from a book-series, even for the same conceptual series.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric audiobook series ID; `lang` (string, optional) — Result language tag

### `apple_books_audiobook_similar`

- **HTTP:** `GET /apple-books/audiobook/{id}/similar`
- **What:** Retrieve "Customers Also Bought" audiobooks. Returns the 'Customers Also Bought' audiobooks shown on the Apple Books page of one audiobook, identified by its numeric `id`. `country` (default `us`) and `lang` (such as `en-us`) choose the storefront and language. Each item has name, author, `narrator`, `duration_seconds`, price, rating and `series_name`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric audiobook ID; `lang` (string, optional) — Result language tag

### `apple_books_author`

- **HTTP:** `GET /apple-books/author/{id}`
- **What:** Retrieve an Apple Books author's bibliography. Returns an Apple Books author by numeric author `id`: name, URL, genres, their ebooks and, where available, audiobooks. Books carry details such as ISBN, page count, publisher, price, rating and series; audiobooks add narrator, duration and preview. `country` is a two-letter storefront code (default `us`) and `lang` a language tag such as `en-us`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric author ID; `lang` (string, optional) — Result language tag

### `apple_books_book`

- **HTTP:** `GET /apple-books/book/{id}`
- **What:** Retrieve Apple Books book details. Returns book metadata from Apple Books, including ISBN, page count, publisher, audience, rating histogram, and series linkage.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric book ID; `lang` (string, optional) — Result language tag

### `apple_books_book_reviews`

- **HTTP:** `GET /apple-books/book/{id}/reviews`
- **What:** Retrieve Apple Books customer reviews. Returns a page of a book's customer reviews. The default first page is served from the book's own catalog page; deeper pages (page>1 or a larger limit) page through Apple's review API directly, up to 20 per page.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric book ID; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Reviews per page, default 10, max 20; `page` (integer, optional) — Review page number, default 1

### `apple_books_book_similar`

- **HTTP:** `GET /apple-books/book/{id}/similar`
- **What:** Retrieve "Customers Also Bought" books. Returns the 'Customers Also Bought' books shown on the Apple Books page of one book, identified by its numeric `id`. `country` (default `us`) and `lang` (such as `en-us`) choose the storefront and language. Each item has name, author, `publisher`, `isbn`, `page_count`, price, rating and `series_sequence`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric book ID; `lang` (string, optional) — Result language tag

### `apple_books_charts`

- **HTTP:** `GET /apple-books/charts`
- **What:** Retrieve Apple Books chart rankings. Returns Apple Books ebook chart rankings for `collection`, `top-free` (default) or `top-paid`. Omit `genre` for all genres, or use one of the discovered ebook category IDs. `country` defaults to `us`; `limit` defaults to 50 and maxes at 200. Each entry has `name`, author, `genres`, `release_date`, `artwork_url` and `url`.
- **Params:** `collection` (string, optional) — Chart collection. Allowed values: top-free, top-paid; `country` (string, optional) — Two-letter storefront country code; `genre` (integer, optional) — Optional ebook genre ID. Allowed values: 9008, 9009, 9026, 9027, 9028, 9031, 9025, 9015, 11086, 9032, 9002, 9034, 9018, 9003, 9020, 9035, 11165. Use apple_books_genres with media=book to discover names.; `limit` (integer, optional) — Number of chart items to return

### `apple_books_genres`

- **HTTP:** `GET /apple-books/genres`
- **What:** List Apple Books chart genres. Reads every category link from Apple's current chart page. The ebook and audiobook genre ID spaces differ; pass `media=book` before filtering ebook charts or `media=audiobook` before filtering audiobook charts.
- **Params:** `country` (string, optional) — Two-letter storefront code, default us; `media` (string, **required**) — Media taxonomy: book or audiobook

### `apple_books_search`

- **HTTP:** `GET /apple-books/search`
- **What:** Search Apple Books titles. Searches Apple Books ebooks by `term`, which is required. `country` is the two-letter storefront code (default `us`), `lang` a language tag such as `en-us`, `limit` the result count (default 50, max 200) and `page` starts at 1. Results include `isbn`, `publisher`, `page_count`, price, rating, genres and series details.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of books per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_books_series`

- **HTTP:** `GET /apple-books/series/{id}`
- **What:** Retrieve an Apple Books series and its full book list. Returns an Apple Books series by its numeric `id`: the series `name` and `url`, and its books in series order. Each book has `series_sequence`, author, `publisher`, `isbn`, `page_count`, price and rating. `country` (default `us`) and `lang` choose the storefront and language.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric series ID; `lang` (string, optional) — Result language tag

## Audible (11)

### `audible_author_charts`

- **HTTP:** `GET /audible/charts/authors`
- **What:** Get Audible's top-author chart. Returns one page of Audible's ranked author chart. It exposes only rank, author identity, image metadata when available, and a canonical author URI; author detail is not included.
- **Params:** `page` (integer, optional) — 1-based result page, default 1

### `audible_categories`

- **HTTP:** `GET /audible/categories`
- **What:** Get Audible's genre/category tree. Returns Audible's full genre/category tree (root genres with their subgenres), including the category ids accepted by GET /audible/search's category_id filter.
- **Params:** _none_

### `audible_category`

- **HTTP:** `GET /audible/category/{id}`
- **What:** Get one Audible category node. Returns one Audible category node and its immediate children by id — cheaper than fetching the full tree from GET /audible/categories when only one node is needed.
- **Params:** `id` (string, **required**) — Audible category id from GET /audible/categories

### `audible_charts`

- **HTTP:** `GET /audible/charts`
- **What:** Get an Audible chart (audible.com/charts). Returns one page of an Audible chart — a ranked list with real chart position, price, and rating. This endpoint is less stable than the rest of this family. Its own filters (category, access level, language, duration, Audible-Originals-only) were individually verified to actually change results. category_id, access_level, and content_type=podcasts are mutually exclusive.
- **Params:** `access_level` (string, optional) — Membership access level, default all; `category_id` (string, optional) — Restrict to a category id from GET /audible/categories; `chart` (string, optional) — Chart type, default most_listened; `content_type` (string, optional) — Content type, default audiobooks; `duration` (string, optional) — Runtime-length filter, default all; `language` (string, optional) — Language filter, default all; `originals_only` (boolean, optional) — Restrict to Audible Originals only; `page` (integer, optional) — 1-based result page, default 1, 20 results per page

### `audible_editorial_list`

- **HTTP:** `GET /audible/list/{list}`
- **What:** Get an Audible curated editorial list. Returns one of Audible's hand-curated "Popular Lists" pages, as its themed shelves (heading + ordered ASINs). Pair an ASIN from any shelf with GET /audible/products (batch) or GET /audible/product/{asin} for full title/author/price/rating detail. "Best of the Year" is not covered.
- **Params:** `list` (string, **required**) — Editorial list slug

### `audible_product`

- **HTTP:** `GET /audible/product/{asin}`
- **What:** Get an Audible audiobook. Returns an Audible audiobook: description, authors, narrators, series, category ladders, publisher, release date, runtime, language, sample audio URL, rating (overall/performance/story), and public list price.
- **Params:** `asin` (string, **required**) — Audible ASIN

### `audible_product_related`

- **HTTP:** `GET /audible/product/{asin}/related`
- **What:** Get Audible titles related to an audiobook. Returns Audible titles related to a given ASIN by a required relation type: same series, same narrator, same author, next in series, or raw similarity.
- **Params:** `asin` (string, **required**) — Audible ASIN; `limit` (integer, optional) — Max results, default 10, max 50; `similarity_type` (string, **required**) — How to relate titles to the given ASIN

### `audible_product_reviews`

- **HTTP:** `GET /audible/product/{asin}/reviews`
- **What:** Get an Audible audiobook's customer reviews. Returns a page of an Audible audiobook's customer reviews (author, title, body, overall/performance/story ratings, helpful votes, submission date).
- **Params:** `asin` (string, **required**) — Audible ASIN; `limit` (integer, optional) — Max reviews, default 10, max 50; `page` (integer, optional) — Zero-based result page, default 0

### `audible_products`

- **HTTP:** `GET /audible/products`
- **What:** Get multiple Audible audiobooks in one call. Returns Audible audiobooks for up to 50 ASINs in a single request — the same fields as GET /audible/product/{asin}. Unrecognized ASINs are silently omitted rather than failing the whole batch.
- **Params:** `asins` (string, **required**) — Comma-separated Audible ASINs, up to 50

### `audible_search`

- **HTTP:** `GET /audible/search`
- **What:** Search Audible's catalog. Searches Audible's audiobook catalog by keyword, title, author, narrator, or category id. At least one filter is required.
- **Params:** `author` (string, optional) — Match by author name; `category_id` (string, optional) — Restrict to a category id from GET /audible/categories; `limit` (integer, optional) — Max results, default 10, max 50; `narrator` (string, optional) — Match by narrator name; `page` (integer, optional) — Zero-based result page, default 0; `q` (string, optional) — Free-text query matched across title, subtitle, and author; `title` (string, optional) — Match by title

### `audible_series`

- **HTTP:** `GET /audible/series/{asin}`
- **What:** Get an Audible series' ordered book list. Returns an Audible series and every book in it, in series order. A series has its own ASIN distinct from any book in it — find one via a book's series[].asin field from GET /audible/product/{asin}.
- **Params:** `asin` (string, **required**) — Audible series ASIN, from a product's series[].asin field
