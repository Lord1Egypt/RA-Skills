# developer-oss-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**29 endpoints across 2 platform group(s).**

## GitHub (17)

### `github_org`

- **HTTP:** `GET /github/org/{org}`
- **What:** Retrieve a GitHub organization profile. Returns the public profile of a GitHub organization by its required `org` login, with fields such as name, description, blog URL, location, public repository count, followers and whether the organization is verified.
- **Params:** `org` (string, **required**) — GitHub organization login

### `github_org_repos`

- **HTTP:** `GET /github/org/{org}/repos`
- **What:** List a GitHub organization's public repositories. Lists the public repositories of a GitHub organization, identified by the required `org` login. Filter with `type` (`all`, `public`, `forks`, `sources` or `member`), order with `sort` (`created`, `updated`, `pushed` or `full_name`) and `direction`, and page with `page` and `per_page` (max 100). Each repository has its name, description, language, stars and forks.
- **Params:** `direction` (string, optional) — Sort direction; `org` (string, **required**) — GitHub organization login; `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `sort` (string, optional) — Sort field; `type` (string, optional) — Repository type

### `github_repo`

- **HTTP:** `GET /github/repo/{owner}/{repo}`
- **What:** Retrieve a GitHub repository. Returns the public details of one GitHub repository, identified by the required `owner` and `repo`. Fields include the full name, description, main language, topics, stars, forks, watchers, open issues, license, default branch and last push time.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `repo` (string, **required**) — Repository name

### `github_repo_contributors`

- **HTTP:** `GET /github/repo/{owner}/{repo}/contributors`
- **What:** List a repository's contributors. Lists the contributors to a GitHub repository, identified by the required `owner` and `repo`, ordered by number of contributions. Page with `page` and `per_page` (max 100). Each contributor has their login, id, contribution count, profile URL and account type.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `repo` (string, **required**) — Repository name

### `github_repo_forks`

- **HTTP:** `GET /github/repo/{owner}/{repo}/forks`
- **What:** List a repository's public forks. Lists the public forks of a GitHub repository, identified by the required `owner` and `repo`. Order with `sort` (`newest`, `oldest`, `stargazers` or `watchers`) and page with `page` and `per_page` (max 100). Each fork has its full name, owner, stars, language and creation time.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `repo` (string, **required**) — Repository name; `sort` (string, optional) — Sort order

### `github_repo_languages`

- **HTTP:** `GET /github/repo/{owner}/{repo}/languages`
- **What:** Retrieve a repository's language breakdown. Returns the languages detected in a GitHub repository, identified by the required `owner` and `repo`, as language and byte-count pairs sorted by bytes, largest first.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `repo` (string, **required**) — Repository name

### `github_repo_releases`

- **HTTP:** `GET /github/repo/{owner}/{repo}/releases`
- **What:** List a repository's releases. Lists the published releases of a GitHub repository, identified by the required `owner` and `repo`. Page with `page` and `per_page` (max 100). Each release has its tag name, title, URL, prerelease flag, publication time and author.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `repo` (string, **required**) — Repository name

### `github_search_repositories`

- **HTTP:** `GET /github/search/repositories`
- **What:** Search public GitHub repositories. Searches public GitHub repositories with the required GitHub search query `q`. Order with `sort` (`stars`, `forks`, `help-wanted-issues` or `updated`) and `order`, and page with `page` and `per_page` (max 100). The response has `total_count` and items with full name, owner, description, language, stars, forks, topics and license.
- **Params:** `order` (string, optional) — Sort order; `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `q` (string, **required**) — GitHub repository search query; `sort` (string, optional) — Sort field

### `github_search_users`

- **HTTP:** `GET /github/search/users`
- **What:** Search public GitHub users. Searches public GitHub user accounts with the required GitHub search query `q`. Order with `sort` (`followers`, `repositories` or `joined`) and `order`, and page with `page` and `per_page` (max 100). The response has `total_count` and items with login, id, profile URL, account type and match score.
- **Params:** `order` (string, optional) — Sort order; `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `q` (string, **required**) — GitHub user search query; `sort` (string, optional) — Sort field

### `github_trending`

- **HTTP:** `GET /github/trending`
- **What:** List trending GitHub repositories. Lists the repositories currently trending on GitHub. Filter by programming `language` (such as `go` or `python`) and choose the window with `since` (`daily`, `weekly` or `monthly`). Each repository has its owner, name, URL, description, language, stars, forks and stars gained today.
- **Params:** `language` (string, optional) — Programming language filter (e.g. go, python); `since` (string, optional) — Time window

### `github_trending_developers`

- **HTTP:** `GET /github/trending/developers`
- **What:** List trending GitHub developers. Lists the developers currently trending on GitHub. Filter by programming `language` (such as `go` or `python`) and choose the window with `since` (`daily`, `weekly` or `monthly`). Each developer has a username, display name, profile URL and their popular repository.
- **Params:** `language` (string, optional) — Programming language filter (e.g. go, python); `since` (string, optional) — Time window

### `github_user`

- **HTTP:** `GET /github/user/{username}`
- **What:** Retrieve a GitHub user profile. Returns a public GitHub user's profile plus user-published social links. Email is included only when the user has made it public on their profile.
- **Params:** `username` (string, **required**) — GitHub username

### `github_user_events`

- **HTTP:** `GET /github/user/{username}/events`
- **What:** List a GitHub user's recent public activity. Lists a GitHub user's recent public events, identified by the required `username`. Page with `page` and `per_page` (max 100). Each event has its id, event type such as `PushEvent`, repository name, timestamp and public flag.
- **Params:** `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `username` (string, **required**) — GitHub username

### `github_user_followers`

- **HTTP:** `GET /github/user/{username}/followers`
- **What:** List a GitHub user's followers. Lists the public accounts that follow a GitHub user, identified by the required `username`. Page with `page` and `per_page` (max 100). Each follower has their login, id, avatar URL, profile URL and account type.
- **Params:** `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `username` (string, **required**) — GitHub username

### `github_user_following`

- **HTTP:** `GET /github/user/{username}/following`
- **What:** List who a GitHub user follows. Lists the public accounts a GitHub user follows, identified by the required `username`. Page with `page` and `per_page` (max 100). Each account has its login, id, avatar URL, profile URL and account type.
- **Params:** `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `username` (string, **required**) — GitHub username

### `github_user_pinned`

- **HTTP:** `GET /github/user/{username}/pinned`
- **What:** List a GitHub user's pinned repositories. Returns the repositories a GitHub user has pinned on their profile, identified by the required `username`. Each has its owner, name, URL, description, language, stars and forks. The list is empty when the user has pinned nothing.
- **Params:** `username` (string, **required**) — GitHub username

### `github_user_repos`

- **HTTP:** `GET /github/user/{username}/repos`
- **What:** List a GitHub user's public repositories. Lists the public repositories of a GitHub user, identified by the required `username`. Filter with `type` (`all`, `owner` or `member`), order with `sort` (`created`, `updated`, `pushed` or `full_name`) and `direction`, and page with `page` and `per_page` (max 100). Each repository has its name, description, language, stars, forks, topics, fork flag and last push time.
- **Params:** `direction` (string, optional) — Sort direction; `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `sort` (string, optional) — Sort field; `type` (string, optional) — Repository type; `username` (string, **required**) — GitHub username

## ChromeWebStore (12)

### `chromewebstore_categories`

- **HTTP:** `GET /chromewebstore/categories`
- **What:** List Chrome Web Store categories and collections. Returns the reference taxonomy for the list endpoints: extension category groups and their subcategory slugs, the top-chart identifiers, and known curated collection slugs.
- **Params:** _none_

### `chromewebstore_category`

- **HTTP:** `GET /chromewebstore/category`
- **What:** List items in a Chrome Web Store category. Returns the item cards listed under an extensions category slug (e.g. `productivity/tools`, `lifestyle/shopping`, `make_chrome_yours/privacy`). Use /chromewebstore/categories for the reference taxonomy. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `category` (string, **required**) — Category slug under extensions; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_charts`

- **HTTP:** `GET /chromewebstore/charts`
- **What:** List a Chrome Web Store top chart. Returns the item cards in a store top chart. `chart` accepts `trending`, `popular`, or `notable`. Defaults: `chart=popular`, `num=50`, `country=us`, `lang=en`.
- **Params:** `chart` (string, optional) — Top chart to list; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_collection`

- **HTTP:** `GET /chromewebstore/collection`
- **What:** List items in a curated Chrome Web Store collection. Returns the item cards in a curated store collection slug (e.g. `editors_picks_extensions`, `dark_mode`, `ai_productivity`). Use /chromewebstore/categories for known collection slugs. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `collection` (string, **required**) — Curated collection slug; `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_developer`

- **HTTP:** `GET /chromewebstore/developer`
- **What:** Retrieve a Chrome Web Store publisher and their items. Returns a Chrome Web Store publisher (developer) by publisher id, including the disclosed trader details — legal name, email, phone, address, website, and D-U-N-S number — plus the publisher's listed items ("More from ..."). Trader fields are only present for publishers that identify as EU traders. Defaults: `num=50`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store publisher id (u + 32 hex chars); `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of items

### `chromewebstore_item`

- **HTTP:** `GET /chromewebstore/item`
- **What:** Retrieve Chrome Web Store item details. Returns detail for a Chrome Web Store extension or theme, including name, rating, rating count, user count, version, last-updated date, size, supported languages, developer, category, screenshots, and privacy links. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_permissions`

- **HTTP:** `GET /chromewebstore/permissions`
- **What:** Retrieve a Chrome Web Store item's declared permissions. Returns the permissions a Chrome Web Store extension declares in its manifest: `permissions`, `optional_permissions`, `host_permissions`, `optional_host_permissions`, plus `manifest_version` and `min_browser_version`. Useful for security and supply-chain review. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_privacy`

- **HTTP:** `GET /chromewebstore/privacy`
- **What:** Retrieve a Chrome Web Store item's privacy disclosures. Returns an extension's privacy disclosures as the store renders them: the developer's data-use statement, whether it collects data, the standard data-handling declarations, and the privacy-policy link. Defaults: `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_reviews`

- **HTTP:** `GET /chromewebstore/reviews`
- **What:** Retrieve Chrome Web Store item reviews. Returns the reviews the store renders on an item's reviews page, each with author, star rating, text, posted/edited dates and reviewed version. Defaults: `num=20`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of reviews; `sort` (string, optional) — Review sort order

### `chromewebstore_search`

- **HTTP:** `GET /chromewebstore/search`
- **What:** Search Chrome Web Store items. Returns Chrome Web Store search result cards for a keyword, each with id, name, rating, user count, publisher and detail URL. Defaults: `num=30`, `country=us`, `lang=en`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of results; `term` (string, **required**) — Search keyword

### `chromewebstore_similar`

- **HTTP:** `GET /chromewebstore/similar`
- **What:** Retrieve related Chrome Web Store items. Returns the related-items shelf shown on a Chrome Web Store item's page. `id` is the required 32-character item id; `country` and `lang` default to `us` and `en`. Each card has name, publisher, category, rating, rating count, users, summary, icon and URL. An unknown or removed id returns 404.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Chrome Web Store item id (32-character extension/theme id); `lang` (string, optional) — Two-letter language code

### `chromewebstore_suggest`

- **HTTP:** `GET /chromewebstore/suggest`
- **What:** Suggest Chrome Web Store search terms. Returns search-term suggestions for a Chrome Web Store prefix given in `term`, up to `num` (default 8), with `country` and `lang` defaulting to `us` and `en`. Suggestions are the distinct item names of the top store-search results for that prefix, each returned as a `term`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Two-letter language code; `num` (integer, optional) — Maximum number of suggestions; `term` (string, **required**) — Search prefix to autocomplete
