# book-market-positioning — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**15 endpoints across 4 platform group(s).**

## Datasets (6)

### `datasets_goodreads_authors_facets`

- **HTTP:** `GET /datasets/goodreads-authors/facets`
- **What:** Facet Goodreads authors dataset. Returns value counts over the Goodreads authors dataset for the required `facet`, either `genres` or `run_id`. Filters `q`, `name`, `genre`, `run_id`, `min_rating` (0 to 5) and `min_ratings_count` narrow the result, which lists the top 50 values with their counts.
- **Params:** `facet` (string, **required**) — Facet enum: genres, run_id; `genre` (string, optional) — Exact genre filter, max 128 characters; `min_rating` (number, optional) — Minimum average rating, 0 through 5; `min_ratings_count` (integer, optional) — Minimum number of ratings; `name` (string, optional) — Exact author name filter, max 128 characters; `q` (string, optional) — Full-text query over name, about and genres, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters

### `datasets_goodreads_authors_item`

- **HTTP:** `GET /datasets/goodreads-authors/items/{id}`
- **What:** Get a Goodreads author from dataset. Returns one Goodreads author from the dataset by numeric author `id`. The record has name, about text, genres, birth and death dates, website, average rating, ratings and reviews counts, image and Goodreads URL. An id not in the dataset returns 404.
- **Params:** `id` (string, **required**) — Goodreads author id, e.g. 153394

### `datasets_goodreads_authors_search`

- **HTTP:** `GET /datasets/goodreads-authors/search`
- **What:** Search Goodreads authors dataset. Searches the crawled public Goodreads author profile index. Authors are discovered as a byproduct of the books crawl (every credited book contributor, plus the genre/search/list seed sources) — not a full catalog. Sort enum: `relevance`, `rating_desc`, `reviews_desc`, `name_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `genre` (string, optional) — Exact genre filter (e.g. Fantasy, Romance, Nonfiction), max 128 characters; `min_rating` (number, optional) — Minimum average rating, 0 through 5; `min_ratings_count` (integer, optional) — Minimum number of ratings; `name` (string, optional) — Exact author name filter, max 128 characters; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over name, about and genres, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, rating_desc, reviews_desc, name_asc

### `datasets_goodreads_books_facets`

- **HTTP:** `GET /datasets/goodreads-books/facets`
- **What:** Facet Goodreads books dataset. Returns terms aggregation counts for the Goodreads books dataset. Facet enum: `genres`, `format`, `language`, `publisher`, `primary_author`, `primary_author_id`, `series_name`, `publication_year`, `run_id`.
- **Params:** `author` (string, optional) — Exact author name filter, max 128 characters; `author_id` (string, optional) — Exact Goodreads author id filter, max 128 characters; `facet` (string, **required**) — Facet enum: genres, format, language, publisher, primary_author, primary_author_id, series_name, publication_year, run_id; `format` (string, optional) — Exact format filter, max 128 characters; `genre` (string, optional) — Exact genre filter, max 128 characters; `isbn` (string, optional) — Exact ISBN-10 filter, max 128 characters; `isbn13` (string, optional) — Exact ISBN-13 filter, max 128 characters; `language` (string, optional) — Exact language filter, max 128 characters; `max_pages` (integer, optional) — Maximum page count; `max_publication_year` (integer, optional) — Maximum publication year; `min_pages` (integer, optional) — Minimum page count; `min_publication_year` (integer, optional) — Minimum publication year; `min_rating` (number, optional) — Minimum average rating, 0 through 5; `min_ratings_count` (integer, optional) — Minimum number of ratings; `publisher` (string, optional) — Exact publisher filter, max 128 characters; `q` (string, optional) — Full-text query over title, author and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `series` (string, optional) — Exact series name filter, max 128 characters

### `datasets_goodreads_books_item`

- **HTTP:** `GET /datasets/goodreads-books/items/{id}`
- **What:** Get a Goodreads book from dataset. Returns one Goodreads book from the dataset by `id`. The record has title, authors, series, genres, format, page count, publisher, publication date, ISBN and ISBN-13, language, description, average rating with a one-to-five-star breakdown, and review counts. An unknown id returns 404.
- **Params:** `id` (string, **required**) — Goodreads book id, e.g. 2767052

### `datasets_goodreads_books_search`

- **HTTP:** `GET /datasets/goodreads-books/search`
- **What:** Search Goodreads books dataset. Searches the crawled public Goodreads book catalog stored in a search index. Discovered from curated Listopia "best of" lists, a search-term sweep, and author bibliography expansion — not a full catalog. Sort enum: `relevance`, `rating_desc`, `reviews_desc`, `publication_desc`, `publication_asc`, `pages_desc`, `pages_asc`, `title_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `author` (string, optional) — Exact author name filter (matches any credited contributor), max 128 characters; `author_id` (string, optional) — Exact Goodreads author id filter, max 128 characters; `format` (string, optional) — Exact format filter (e.g. Hardcover, Paperback, Kindle Edition), max 128 characters; `genre` (string, optional) — Exact genre filter (e.g. Fantasy, Romance, Nonfiction), max 128 characters; `isbn` (string, optional) — Exact ISBN-10 filter, max 128 characters; `isbn13` (string, optional) — Exact ISBN-13 filter, max 128 characters; `language` (string, optional) — Exact language filter (e.g. English, Spanish), max 128 characters; `max_pages` (integer, optional) — Maximum page count; `max_publication_year` (integer, optional) — Maximum publication year; `min_pages` (integer, optional) — Minimum page count; `min_publication_year` (integer, optional) — Minimum publication year; `min_rating` (number, optional) — Minimum average rating, 0 through 5; `min_ratings_count` (integer, optional) — Minimum number of ratings; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `publisher` (string, optional) — Exact publisher filter, max 128 characters; `q` (string, optional) — Full-text query over title, author and description, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `series` (string, optional) — Exact series name filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, rating_desc, reviews_desc, publication_desc, publication_asc, pages_desc, pages_asc, title_asc

## Goodreads (5)

### `goodreads_author_books`

- **HTTP:** `GET /goodreads/author/{id}/books`
- **What:** List a Goodreads author's books. Lists the books of a Goodreads author by author `id`, about 30 per page; `page` is 1-based and defaults to 1. Each book has its `id`, title, author, average rating, ratings count and Goodreads URL, and the `id` can be used to look up the full book.
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

### `goodreads_search`

- **HTTP:** `GET /goodreads/search`
- **What:** Search Goodreads books. Searches Goodreads for books by title or author using `q`, returning up to `limit` results (default 10, max 50). Each result has its id, title, author and author id, average rating, ratings count, page count, a truncated description, cover image URL and Goodreads URL. Only books are returned, not authors or lists.
- **Params:** `limit` (integer, optional) — Max results, default 10, max 50; `q` (string, **required**) — Search query

## AppleBooks (2)

### `apple_books_book`

- **HTTP:** `GET /apple-books/book/{id}`
- **What:** Retrieve Apple Books book details. Returns book metadata from Apple Books, including ISBN, page count, publisher, audience, rating histogram, and series linkage.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Books numeric book ID; `lang` (string, optional) — Result language tag

### `apple_books_search`

- **HTTP:** `GET /apple-books/search`
- **What:** Search Apple Books titles. Searches Apple Books ebooks by `term`, which is required. `country` is the two-letter storefront code (default `us`), `lang` a language tag such as `en-us`, `limit` the result count (default 50, max 200) and `page` starts at 1. Results include `isbn`, `publisher`, `page_count`, price, rating, genres and series details.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of books per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

## Audible (2)

### `audible_product`

- **HTTP:** `GET /audible/product/{asin}`
- **What:** Get an Audible audiobook. Returns an Audible audiobook: description, authors, narrators, series, category ladders, publisher, release date, runtime, language, sample audio URL, rating (overall/performance/story), and public list price.
- **Params:** `asin` (string, **required**) — Audible ASIN

### `audible_search`

- **HTTP:** `GET /audible/search`
- **What:** Search Audible's catalog. Searches Audible's audiobook catalog by keyword, title, author, narrator, or category id. At least one filter is required.
- **Params:** `author` (string, optional) — Match by author name; `category_id` (string, optional) — Restrict to a category id from GET /audible/categories; `limit` (integer, optional) — Max results, default 10, max 50; `narrator` (string, optional) — Match by narrator name; `page` (integer, optional) — Zero-based result page, default 0; `q` (string, optional) — Free-text query matched across title, subtitle, and author; `title` (string, optional) — Match by title
