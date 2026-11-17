# company-ranking-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**18 endpoints across 2 platform group(s).**

## Forbes (6)

### `forbes_article`

- **HTTP:** `GET /forbes/article`
- **What:** Forbes article content. Returns public Forbes article metadata and body content. The response preserves rich body HTML, paragraphs, headings, and public embed metadata. Accepts dated /sites/<author>/... and /councils/<council>/... URLs; it does not bypass login, subscription, or bot challenges.
- **Params:** `url` (string, **required**) — Canonical HTTPS Forbes article URL

### `forbes_author`

- **HTTP:** `GET /forbes/author`
- **What:** Forbes contributor/staff author profile. Returns one Forbes contributor or staff author's public byline page: name, display type, bio, headshot, and their most recent bylined articles. This is the journalist byline page at forbes.com/sites/<slug>/, distinct from forbes-person, which is a billionaire net-worth profile from Forbes's rich-list data.
- **Params:** `slug` (string, optional) — Forbes contributor slug, e.g. alisondurkee; `url` (string, optional) — Canonical forbes.com/sites/<slug>/ URL, as an alternative to slug

### `forbes_billionaires`

- **HTTP:** `GET /forbes/billionaires`
- **What:** Forbes billionaires list. Returns a paginated Forbes billionaires list from the public Forbes JSON feed. The default field set includes ranking, worth, person identity, citizenship, category, industry, organization, image, and biography fields.
- **Params:** `limit` (integer, optional) — Page size (1-100); `start` (integer, optional) — Zero-based offset; `year` (integer, optional) — Forbes list year

### `forbes_categories`

- **HTTP:** `GET /forbes/categories`
- **What:** Forbes public editorial sections. Lists the current public Forbes navigation taxonomy, including business, money, innovation, leadership, lifestyle, Forbes Vetted, Advisor, Health, and their public subsections. Article promos, account surfaces, games, video-only links, and external hosts are excluded.
- **Params:** _none_

### `forbes_headlines`

- **HTTP:** `GET /forbes/headlines`
- **What:** Forbes section headlines. Returns up to 50 unique Forbes article cards for one navigation path. `section` is required and takes a `path` value from the Forbes categories endpoint, such as `/business/`. Each card has the title, article URL, description, author, and publication time and image URL when present. A blocked section returns an error, not an empty list.
- **Params:** `section` (string, **required**) — Forbes navigation path from /forbes/categories

### `forbes_person`

- **HTTP:** `GET /forbes/person`
- **What:** Forbes person profile. Returns public Forbes JSON profile data plus the profile page's biography, real-time net-worth display, wealth history, personal facts, editor update, and list-appearance metadata.
- **Params:** `uri` (string, **required**) — Forbes person URI

## Fortune (12)

### `fortune_article`

- **HTTP:** `GET /fortune/article`
- **What:** Get Fortune article content. Returns one Fortune article by its canonical `url`. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked articles return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Fortune article URL

### `fortune_author`

- **HTTP:** `GET /fortune/author`
- **What:** Get a Fortune author profile. Returns one Fortune author's public profile: name, bio, email, social accounts, and one page of their recent articles (30 fortune.com/2026-format article dates use "Month D, YYYY"; converted to YYYY-MM-DD here).
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. sheryl-estrada; `url` (string, optional) — Canonical fortune.com/author/<slug>/ URL, optionally with a /page/<n>/ suffix; alternative to slug

### `fortune_companies`

- **HTTP:** `GET /fortune/companies`
- **What:** Search the Fortune company directory. Searches Fortune's company directory, 30 companies per page, with `page` starting at 1. Filter by `search` (company name), `country`, `industry` (exact title), `ranking` with `year`, and ranges `min_revenue` and `max_revenue` (in $M) and `min_employees` and `max_employees`. Each item has name, slug, URL, country, revenues and description. Invalid `country` or `industry` values return `400`.
- **Params:** `country` (string, optional) — Country/territory slug or title; call fortune-company-filters for the complete accepted set; `industry` (string, optional) — Exact industry title; call fortune-company-filters for the complete accepted set; `max_employees` (integer, optional) — Maximum employee count; `max_revenue` (integer, optional) — Maximum revenue in $M; `min_employees` (integer, optional) — Minimum employee count; `min_revenue` (integer, optional) — Minimum revenue in $M; `page` (integer, optional) — 1-based page number; 30 companies per page; `ranking` (string, optional) — Fortune ranking slug to filter companies that appear on it; call fortune-company-filters for the accepted set; `search` (string, optional) — Case-insensitive company-name search; `year` (string, optional) — Ranking year the ranking filter is evaluated against; defaults to the current year

### `fortune_company`

- **HTTP:** `GET /fortune/company`
- **What:** Get a Fortune company profile. Returns one company's public Fortune profile: fact sheet (headquarters, CEO, ticker, revenues, employees, ...), the Fortune rankings it appears on, workplace data tables, earnings report links, and social accounts, recovered from the company's own fortune.com page.
- **Params:** `slug` (string, optional) — Company slug, e.g. alphabet; `url` (string, optional) — Canonical fortune.com/company/<slug>/ URL; alternative to slug

### `fortune_company_filters`

- **HTTP:** `GET /fortune/companies/filters`
- **What:** Discover Fortune company directory filters. Lists the filter values the Fortune company directory accepts: countries and industries (each with slug and title), the rankings usable with the `ranking` filter and their available years, and the minimum and maximum revenue and employee counts. The rankings are a subset of all Fortune rankings. It takes no parameters.
- **Params:** _none_

### `fortune_headlines`

- **HTTP:** `GET /fortune/headlines`
- **What:** Get Fortune section headlines. Returns the latest Fortune headlines for one section. `section` is required and takes one of 36 slugs such as `latest`, `fortune-500`, `finance`, `artificial-intelligence`, `crypto`, `leadership` or `europe`. Each item has its title and URL.
- **Params:** `section` (string, **required**) — Fortune section slug

### `fortune_news`

- **HTTP:** `GET /fortune/news`
- **What:** Get Fortune top stories. Returns the current Fortune top stories. Each item has its title, URL, summary, publication time, author and image. Takes no parameters; use `fortune-headlines` for a single section.
- **Params:** _none_

### `fortune_ranking`

- **HTTP:** `GET /fortune/ranking`
- **What:** Search a Fortune ranking. Returns rows from a selected Fortune ranking list and year -- the Fortune 500 franchise (including Fortune China 500) or one of Fortune's award/culture rankings. Search, filters, sorting, and pagination are applied against Fortune's public ranking data and validated against that list/year's filter inventory.
- **Params:** `filter` (array, optional) — Repeatable dynamic filter in field:value form; use company for fortune-china-500 or discover list-specific fields and values with fortune-ranking-filters; `industry` (string, optional) — Convenience alias for the live industry filter; `limit` (integer, optional) — Number of rows to return; 0 uses the default 100, maximum 1000; `list` (string, optional) — Accepted values: fortune500, global500, fortune500-europe, southeast-asia-500, fortune-china-500, 100-fastest-growing-companies, 40-under-40, ai-innovators, aiq, americas-most-innovative-companies, asia-future, best-companies, best-companies-europe, best-companies-southeast-asia, best-large-workplaces-in-technology, best-large-workplaces-parents, best-medium-workplaces, best-medium-workplaces-in-technology, best-places-families, best-places-retire-affordably, best-small-workplaces, best-small-workplaces-aging-services-senior-housing-care, best-small-workplaces-bay-area, best-small-workplaces-biotechnology-pharmaceuticals, best-small-workplaces-chicago-area, best-small-workplaces-construction, best-small-workplaces-consulting-professional-services, best-small-workplaces-financial-services-insurance, best-small-workplaces-for-women, best-small-workplaces-health-care, best-small-workplaces-in-technology, best-small-workplaces-manufacturing-production, best-small-workplaces-millennials, best-small-workplaces-new-york, best-small-workplaces-parents, best-small-workplaces-real-estate, best-small-workplaces-retail, best-small-workplaces-technology, best-small-workplaces-texas, best-workplaces-advertising-marketing, best-workplaces-aging-services-at-home-care, best-workplaces-aging-services-senior-housing-care, best-workplaces-baby-boomers, best-workplaces-bay-area, best-workplaces-biotechnology-pharmaceuticals, best-workplaces-camaraderie, best-workplaces-chicago-area, best-workplaces-construction, best-workplaces-consulting-professional-services, best-workplaces-finance-insurance, best-workplaces-financial-services-insurance, best-workplaces-flexibility, best-workplaces-for-african-americans, best-workplaces-for-asian-americans, best-workplaces-for-diversity, best-workplaces-for-hispanics-and-latinos, best-workplaces-for-retirement, best-workplaces-for-women, best-workplaces-gen-x, best-workplaces-giving-back, best-workplaces-health-care, best-workplaces-manufacturing-production, best-workplaces-millennials, best-workplaces-new-york, best-workplaces-parents, best-workplaces-real-estate, best-workplaces-recent-college-graduates, best-workplaces-retail, best-workplaces-technology, best-workplaces-texas, businessperson-of-the-year, candidates-working-women-times-up, change-the-world, creator-25, crypto, cyber, europes-most-innovative-companies, fintech-innovators-asia, food-drink-women-innovators, fortunate50, future-50, global-best-companies, heroes-of-the-fortune-500, impact20, inner-city-100, international-20, lgbtq-leaders, mejores-companias-latinos-hispanos, modern-board-25, most-fantastical-comic-book-businesses, most-important-private-companies, most-powerful-people, most-powerful-rising-executives, most-powerful-women, most-powerful-women-asia, most-powerful-women-europe-middle-east-africa, most-powerful-women-international, nfty-50, the-ledger-40-under-40, unicorns, women-tech-leaders-europe, worlds-best-workplaces, worlds-greatest-leaders, worlds-most-admired-companies. Defaults to fortune500.; `offset` (integer, optional) — Zero-based result offset; `profitable` (string, optional) — Convenience alias; accepts true/false or yes/no; `search` (string, optional) — Case-insensitive company-name search; Fortune China 500 searches every displayed row column; `sector` (string, optional) — Convenience alias for the live sector filter; `sort_by` (string, optional) — For fortune-china-500: Company, Rank, Rank of last year, Revenues ($M), Profits ($M); otherwise discover sortable fields with fortune-ranking-filters; `sort_order` (string, optional) — Sort direction; `state` (string, optional) — Convenience alias for the live state filter; `year` (string, optional) — For fortune-china-500, accepted values are 2026, 2025, 2024, 2023; otherwise call fortune-ranking-years for this list's accepted years

### `fortune_ranking_filters`

- **HTTP:** `GET /fortune/ranking/filters`
- **What:** Discover Fortune ranking filters. Returns the filter fields and sortable columns for one Fortune ranking list. `list` selects the ranking (default `fortune500`) and `year` a historical edition; omit `year` for the list's current year. Each search field has its field name, title, type and accepted options, and each sortable column has a title and type.
- **Params:** `list` (string, optional) — Accepted values: fortune500, global500, fortune500-europe, southeast-asia-500, fortune-china-500, 100-fastest-growing-companies, 40-under-40, ai-innovators, aiq, americas-most-innovative-companies, asia-future, best-companies, best-companies-europe, best-companies-southeast-asia, best-large-workplaces-in-technology, best-large-workplaces-parents, best-medium-workplaces, best-medium-workplaces-in-technology, best-places-families, best-places-retire-affordably, best-small-workplaces, best-small-workplaces-aging-services-senior-housing-care, best-small-workplaces-bay-area, best-small-workplaces-biotechnology-pharmaceuticals, best-small-workplaces-chicago-area, best-small-workplaces-construction, best-small-workplaces-consulting-professional-services, best-small-workplaces-financial-services-insurance, best-small-workplaces-for-women, best-small-workplaces-health-care, best-small-workplaces-in-technology, best-small-workplaces-manufacturing-production, best-small-workplaces-millennials, best-small-workplaces-new-york, best-small-workplaces-parents, best-small-workplaces-real-estate, best-small-workplaces-retail, best-small-workplaces-technology, best-small-workplaces-texas, best-workplaces-advertising-marketing, best-workplaces-aging-services-at-home-care, best-workplaces-aging-services-senior-housing-care, best-workplaces-baby-boomers, best-workplaces-bay-area, best-workplaces-biotechnology-pharmaceuticals, best-workplaces-camaraderie, best-workplaces-chicago-area, best-workplaces-construction, best-workplaces-consulting-professional-services, best-workplaces-finance-insurance, best-workplaces-financial-services-insurance, best-workplaces-flexibility, best-workplaces-for-african-americans, best-workplaces-for-asian-americans, best-workplaces-for-diversity, best-workplaces-for-hispanics-and-latinos, best-workplaces-for-retirement, best-workplaces-for-women, best-workplaces-gen-x, best-workplaces-giving-back, best-workplaces-health-care, best-workplaces-manufacturing-production, best-workplaces-millennials, best-workplaces-new-york, best-workplaces-parents, best-workplaces-real-estate, best-workplaces-recent-college-graduates, best-workplaces-retail, best-workplaces-technology, best-workplaces-texas, businessperson-of-the-year, candidates-working-women-times-up, change-the-world, creator-25, crypto, cyber, europes-most-innovative-companies, fintech-innovators-asia, food-drink-women-innovators, fortunate50, future-50, global-best-companies, heroes-of-the-fortune-500, impact20, inner-city-100, international-20, lgbtq-leaders, mejores-companias-latinos-hispanos, modern-board-25, most-fantastical-comic-book-businesses, most-important-private-companies, most-powerful-people, most-powerful-rising-executives, most-powerful-women, most-powerful-women-asia, most-powerful-women-europe-middle-east-africa, most-powerful-women-international, nfty-50, the-ledger-40-under-40, unicorns, women-tech-leaders-europe, worlds-best-workplaces, worlds-greatest-leaders, worlds-most-admired-companies. Defaults to fortune500.; `year` (string, optional) — For fortune-china-500, accepted values are 2026, 2025, 2024, 2023; omit for current year or call fortune-ranking-years

### `fortune_ranking_lists`

- **HTTP:** `GET /fortune/ranking/lists`
- **What:** List Fortune ranking lists. Returns every public ranking accepted by the other fortune/ranking endpoints -- the Fortune 500 franchise's regional/global variants (including Fortune China 500) plus Fortune's award and culture rankings.
- **Params:** _none_

### `fortune_ranking_years`

- **HTTP:** `GET /fortune/ranking/years`
- **What:** List Fortune ranking years. Returns every year accepted by Fortune's public ranking source for a selected list, including the 2023-2026 Fortune China 500 editions.
- **Params:** `list` (string, optional) — Accepted values: fortune500, global500, fortune500-europe, southeast-asia-500, fortune-china-500, 100-fastest-growing-companies, 40-under-40, ai-innovators, aiq, americas-most-innovative-companies, asia-future, best-companies, best-companies-europe, best-companies-southeast-asia, best-large-workplaces-in-technology, best-large-workplaces-parents, best-medium-workplaces, best-medium-workplaces-in-technology, best-places-families, best-places-retire-affordably, best-small-workplaces, best-small-workplaces-aging-services-senior-housing-care, best-small-workplaces-bay-area, best-small-workplaces-biotechnology-pharmaceuticals, best-small-workplaces-chicago-area, best-small-workplaces-construction, best-small-workplaces-consulting-professional-services, best-small-workplaces-financial-services-insurance, best-small-workplaces-for-women, best-small-workplaces-health-care, best-small-workplaces-in-technology, best-small-workplaces-manufacturing-production, best-small-workplaces-millennials, best-small-workplaces-new-york, best-small-workplaces-parents, best-small-workplaces-real-estate, best-small-workplaces-retail, best-small-workplaces-technology, best-small-workplaces-texas, best-workplaces-advertising-marketing, best-workplaces-aging-services-at-home-care, best-workplaces-aging-services-senior-housing-care, best-workplaces-baby-boomers, best-workplaces-bay-area, best-workplaces-biotechnology-pharmaceuticals, best-workplaces-camaraderie, best-workplaces-chicago-area, best-workplaces-construction, best-workplaces-consulting-professional-services, best-workplaces-finance-insurance, best-workplaces-financial-services-insurance, best-workplaces-flexibility, best-workplaces-for-african-americans, best-workplaces-for-asian-americans, best-workplaces-for-diversity, best-workplaces-for-hispanics-and-latinos, best-workplaces-for-retirement, best-workplaces-for-women, best-workplaces-gen-x, best-workplaces-giving-back, best-workplaces-health-care, best-workplaces-manufacturing-production, best-workplaces-millennials, best-workplaces-new-york, best-workplaces-parents, best-workplaces-real-estate, best-workplaces-recent-college-graduates, best-workplaces-retail, best-workplaces-technology, best-workplaces-texas, businessperson-of-the-year, candidates-working-women-times-up, change-the-world, creator-25, crypto, cyber, europes-most-innovative-companies, fintech-innovators-asia, food-drink-women-innovators, fortunate50, future-50, global-best-companies, heroes-of-the-fortune-500, impact20, inner-city-100, international-20, lgbtq-leaders, mejores-companias-latinos-hispanos, modern-board-25, most-fantastical-comic-book-businesses, most-important-private-companies, most-powerful-people, most-powerful-rising-executives, most-powerful-women, most-powerful-women-asia, most-powerful-women-europe-middle-east-africa, most-powerful-women-international, nfty-50, the-ledger-40-under-40, unicorns, women-tech-leaders-europe, worlds-best-workplaces, worlds-greatest-leaders, worlds-most-admired-companies. Defaults to fortune500.

### `fortune_sections`

- **HTTP:** `GET /fortune/sections`
- **What:** Get Fortune sections. Lists the Fortune sections accepted by `fortune-headlines`, such as `latest`, `fortune-500`, `finance`, `tech`, `leadership` and `crypto`. Each entry has a stable `slug`, display `name` and the section `url`. Takes no parameters.
- **Params:** _none_
