---
name: firehose-api
description: Firehose monitors the web in real-time — you create rules (Lucene queries), and every crawled page that matches gets delivered via an SSE stream. Use when implementing or discussing API endpoints.
homepage: https://firehose.com
metadata: {"clawdbot":{"requires":{"bins":["curl"],"env":["FIREHOSE_MANAGEMENT_KEY","FIREHOSE_TAP_TOKEN"]},"primaryEnv":"FIREHOSE_TAP_TOKEN"}}
---

# Firehose API Skill

Firehose monitors the web in real-time. You create rules (Lucene queries), and every crawled page that matches gets delivered to you via a Server-Sent Events stream.

## Base URL

```
https://api.firehose.com
```

## Authentication

There are two types of API keys:

- **Management Key** (`fhm_` prefix): Used to manage taps (create, list, update, revoke). Created by admins from the dashboard. Cannot manage rules or stream. Shown once at creation — store securely.
- **Tap Token** (`fh_` prefix): Used to manage rules within a tap and to stream. Retrievable anytime via the dashboard or `GET /v1/taps` (with a management key).

Both use Bearer token authentication:

```
Authorization: Bearer fhm_your_management_key
Authorization: Bearer fh_your_tap_token
```

## Management Key Endpoints

These endpoints require a management key (`fhm_` prefix).

### List Taps

```
GET /v1/taps
```

Response `200`:
```json
{
  "data": [
    { "id": "uuid", "name": "Brand Mentions", "token": "fh_full_tap_token", "token_prefix": "fh_abc", "rules_count": 3, "last_used_at": null, "created_at": "2026-02-27T00:00:00+00:00" }
  ]
}
```

Use this to retrieve all tap tokens and start streaming with a single management key.

### Create Tap

```
POST /v1/taps
Content-Type: application/json

{ "name": "Brand Mentions" }
```

Response `201`:
```json
{
  "data": { "id": "uuid", "name": "Brand Mentions", "token_prefix": "fh_abc", "created_at": "..." },
  "token": "fh_the_full_tap_token"
}
```

The full `token` is also available via `GET /v1/taps`.

### Get Tap

```
GET /v1/taps/:id
```

### Update Tap

```
PUT /v1/taps/:id
Content-Type: application/json

{ "name": "New Name" }
```

### Revoke Tap

```
DELETE /v1/taps/:id
```

Response `204` (no content).

## Tap Token Endpoints

These endpoints require a tap token (`fh_` prefix).

### List Rules

```
GET /v1/rules
```

Response `200`:
```json
{
  "data": [
    { "id": "1", "value": "ahrefs", "tag": "brand-mentions" },
    { "id": "2", "value": "\"site explorer\"", "tag": "product" }
  ],
  "meta": { "count": 2 }
}
```

### Create Rule

```
POST /v1/rules
Content-Type: application/json

{ "value": "ahrefs OR semrush", "tag": "seo-tools" }
```

- `value` (string, required): Lucene query
- `tag` (string, optional): label, max 255 chars
- `nsfw` (boolean, optional): include adult content in results. Default: `false`
- `quality` (boolean, optional): apply quality filters (see [Quality filter](#quality--quality-filter-rule-object-field)). Default: `true`
- Max 25 rules per organization

Response `201`:
```json
{
  "data": { "id": "3", "value": "ahrefs OR semrush", "tag": "seo-tools" }
}
```

### Get Rule

```
GET /v1/rules/:id
```

### Update Rule

```
PUT /v1/rules/:id
Content-Type: application/json

{ "value": "updated query", "tag": "new-tag", "nsfw": true }
```

Supports partial updates.

### Delete Rule

```
DELETE /v1/rules/:id
```

Response `204` (no content).

### Stream (SSE)

```
GET /v1/stream?timeout=60&since=30m&limit=100
```

Opens a Server-Sent Events connection. Only delivers events matching the authenticated tap's rules.

Query params:
- `timeout` (int, default 300): connection duration in seconds (1-300)
- `since` (string): replay buffered events from a relative time window, e.g. `5m`, `1h`, `24h` (max 24h). Events are buffered for approximately 24 hours.
- `offset` (int): start from an exact Kafka offset on the tap's partition
- `limit` (int, 1-10000): close the stream after delivering this many matching events

Headers:
- `Last-Event-ID`: SSE standard reconnect header. Format: `{partition}-{offset}` (as sent in the `id:` field of update events). Resumes from the next offset after the given one.

**Parameter precedence:** `Last-Event-ID` > `offset` > `since` > default (live tail)

#### Resuming after disconnect

When using the browser `EventSource` API, the `Last-Event-ID` header is sent automatically on reconnect. This means if your connection drops, the browser will resume from where it left off (as long as the events are still within the ~24 hour buffer).

#### Event types

**connected** — sent on connection open:
```
event: connected
data: []
```

**update** — a web page matched one of your rules:
```
id: 0-43368
event: update
data: {"query_id":"1","matched_at":"2026-02-13T08:06:32Z","tap_id":"1","document":{"url":"https://example.com/page","title":"Example Page","publish_time":"2026-02-13T08:06:32","diff":{"chunks":[{"typ":"ins","text":"New content added..."}]},"page_category":["/News"],"page_types":["/Article"],"language":"en","markdown":"..."}}
```

#### Update payload fields

| Field | Type | Present | Description |
|-------|------|---------|-------------|
| `tap_id` | string | Always | Tap whose rule matched |
| `query_id` | string | Always | Rule ID that matched |
| `matched_at` | string | Always | ISO-8601 instant (e.g. `2026-02-13T08:06:32.123456Z`) |
| `document` | object | Always | Matched document (see below) |

#### Document fields

| Field | Type | Present | Description |
|-------|------|---------|-------------|
| `url` | string | Always | Document URL |
| `title` | string | If non-null | Page title |
| `publish_time` | string | If non-null | ISO-8601 local datetime (e.g. `2026-02-13T08:06:32`, no timezone) |
| `diff` | object | If non-null | Content diff |
| `diff.chunks[]` | array | If diff present | List of diff chunks |
| `diff.chunks[].typ` | string | Yes | `"ins"` (inserted) or `"del"` (deleted) |
| `diff.chunks[].text` | string | Yes | Chunk text |
| `page_category` | string[] | If non-empty | ML category labels (e.g. `["/News"]`) |
| `page_types` | string[] | If non-empty | ML type labels (e.g. `["/Article"]`) |
| `language` | string | If non-null | ISO 639-1 language code (e.g. `"en"`, `"fr"`, `"zh-cn"`) |
| `markdown` | string | Always | Full page content as markdown |

Serialization: null fields and empty arrays are **omitted** (not `null` or `[]`).

**error** — something went wrong:
```
event: error
data: {"message":"No rules configured. Create rules first via POST /v1/rules."}
```

**end** — stream ended normally (timeout expired or limit reached), reconnect to continue:
```
event: end
data: []
```

## Lucene Query Syntax

The `value` field in rules uses **Lucene ClassicQueryParser** syntax. Queries run against indexed fields extracted from each crawled document.

### Indexed Fields

| Field | Type | Case | Description |
|-------|------|------|-------------|
| `added` | text | insensitive | **Default field.** Text from inserted diff chunks. Tokenized, lowercased, stop words removed. Multi-valued. |
| `removed` | text | insensitive | Text from deleted diff chunks. Tokenized, lowercased, stop words removed. Multi-valued. |
| `added_anchor` | text | insensitive | Anchor text from inserted links. Tokenized, lowercased, stop words removed. Multi-valued. |
| `removed_anchor` | text | insensitive | Anchor text from deleted links. Tokenized, lowercased, stop words removed. Multi-valued. |
| `title` | text | insensitive | Page title. Tokenized and lowercased. |
| `url` | keyword | **sensitive** | Full URL as a single exact token. |
| `domain` | keyword | **sensitive** | Domain extracted from URL (e.g. `example.com`). Multi-valued. |
| `publish_time` | keyword | **sensitive** | ISO-8601 local datetime (e.g. `2025-06-15T15:06:40`). |
| `page_category` | keyword | **sensitive** | ML category label (e.g. `/News`). Multi-valued. |
| `page_type` | keyword | **sensitive** | ML type label (e.g. `/Article/How_to`). Multi-valued. |
| `language` | keyword | **sensitive** | ISO 639-1 language code (e.g. `en`, `fr`, `zh-cn`). Allowed values: `af`, `ar`, `bg`, `bn`, `cs`, `da`, `de`, `el`, `en`, `es`, `et`, `fa`, `fi`, `fr`, `gu`, `he`, `hi`, `hr`, `hu`, `id`, `it`, `ja`, `kn`, `ko`, `lt`, `lv`, `mk`, `ml`, `mr`, `ne`, `nl`, `no`, `pa`, `pl`, `pt`, `ro`, `ru`, `sk`, `sl`, `so`, `sq`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `zh-cn`, `zh-tw`. |
| `recent` | filter | — | Recency filter. Value format: `[n]h`, `[n]d`, or `[n]mo` where n is a positive integer (e.g. `recent:24h`, `recent:7d`, `recent:3mo`). Only returns pages published within this time window. |

**Key distinctions:**
- **Text** fields (`added`, `removed`, `added_anchor`, `removed_anchor`, `title`): tokenized on whitespace/punctuation, lowercased. Queries are case-insensitive.
- **Keyword** fields (`url`, `domain`, `publish_time`, `page_category`, `page_type`, `language`): stored as a single exact token. Must match the full value exactly, case-sensitively.
- **Filter** field (`recent`): not an indexed document field. It is a rule-level filter parsed from the query and applied server-side. Can be combined freely with other Lucene terms using `AND`.
- Null/empty fields are absent — queries against them never match.
- Multi-valued fields: matching **any** value matches the document.

### Term queries

Bare terms search the `added` field by default.

```
ahrefs                       # "ahrefs" anywhere in added content
title:tesla                  # "tesla" in title (case-insensitive)
```

### Phrase queries

```
"quick brown fox"            # exact phrase in content
title:"breaking news"        # exact phrase in title
```

### Boolean operators

```
java AND programming         # both terms in added content
title:tesla OR added:"electric vehicle"
NOT malware                  # exclude term
title:ahrefs AND added:seo   # cross-field boolean
removed:"old feature"        # term appeared in removed (deleted) content
```

### Keyword field queries (exact, case-sensitive)

```
url:"https://example.com/page"
domain:"example.com"
page_category:"/News"
page_type:"/Article/How_to"
language:"en"
```

### URL and domain filtering

The `url` and `domain` fields use KeywordAnalyzer, so the entire value is stored as a single exact token (case-sensitive). You can query them using three Lucene mechanisms: **exact match**, **wildcard queries**, and **regex queries**.

#### Escaping rules

Forward slashes (`/`) are special in Lucene — they delimit regex patterns. You **must** escape them with `\` in wildcard queries. Inside regex patterns (between `/` delimiters), escape them too since they would otherwise be interpreted as the closing delimiter.

| Character | In wildcard queries | In regex queries (`/.../`) | In exact/quoted queries |
|-----------|-------------------|---------------------------|------------------------|
| `/` | `\/` (escape required) | `\/` (escape required) | No escape needed |
| `:` | `\\:` (escape required) | No escape needed | No escape needed inside quotes |
| `*` | Wildcard (matches any chars) | Regex quantifier | Literal inside quotes |

**JSON double-escaping:** When sending queries via the API (JSON body), remember that `\/` in JSON is just an optional escape for `/` — it does NOT produce a backslash. To get a literal `\` before `/` in the Lucene query, you must write `\\/` in the JSON string. For example, the Lucene query `url:*\/abs\/*` must be sent as `"url:*\\/abs\\/*"` in JSON.

#### Exact match

Match a single, specific URL or domain:

```
url:"https://example.com/news/article-1"
domain:"example.com"
```

#### Wildcard queries (`*` and `?`)

`*` matches zero or more characters, `?` matches exactly one character. Forward slashes must be escaped with `\`:

```
# URLs containing /category/ anywhere
url:*\/category\/*

# URLs containing /tag/ anywhere
url:*\/tag\/*

# URLs on a specific domain path
url:https\:\/\/example.com\/blog\/*

# Domain matching (exact, no wildcards needed for simple cases)
domain:"techcrunch.com"
```

#### Regex queries (`/pattern/`)

Regex queries are enclosed in forward slashes. Use [Lucene regex syntax](https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/util/automaton/RegExp.html) (a subset of standard regex — notably, no `\d` shorthand; use `[0-9]` instead). Forward slashes within the pattern must be escaped:

```
# Pagination URLs: /page/ followed by digits (e.g. /page/2, /page/37)
url:/.*\/page\/[0-9]+.*/

# URLs with numeric IDs in a path segment
url:/.*\/articles\/[0-9]+.*/

# URLs ending in specific extensions
url:/.*\.(pdf|xml|json)/
```

#### Combining URL filters with NOT

Use `NOT` to exclude unwanted URL patterns. This is the most common use case — filtering out pagination, category, and tag pages:

```
# Exclude pagination pages (regex for /page/ + digits)
NOT url:/.*\/page\/[0-9]+.*/

# Exclude category and tag pages (wildcard with escaped slashes)
NOT url:*\/category\/*
NOT url:*\/tag\/*

# Full example: match "tesla" in English, excluding junk URLs
title:tesla AND language:"en" AND NOT url:/.*\/page\/[0-9]+.*/ AND NOT url:*\/category\/* AND NOT url:*\/tag\/*
```

#### When to use wildcard vs regex

| Use case | Recommended | Example |
|----------|-------------|---------|
| Contains a path segment | Wildcard | `url:*\/category\/*` |
| Path segment + pattern (digits, extensions) | Regex | `url:/.*\/page\/[0-9]+.*/` |
| Exact URL match | Quoted string | `url:"https://example.com/page"` |
| Domain filter | Quoted string | `domain:"example.com"` |

### Date range queries on `publish_time`

Colons in timestamps must be escaped with `\\` in all query types:

```
publish_time:[2025-01-01T00\\:00\\:00 TO 2025-12-31T23\\:59\\:59]     # inclusive
publish_time:{2025-01-01T00\\:00\\:00 TO 2025-12-31T23\\:59\\:59}     # exclusive
publish_time:2025-06-15T12\\:00\\:00                                    # exact match
```

### Multi-field combinations

```
title:tesla AND page_category:"/News"
title:ahrefs AND added:seo AND page_type:"/Article"
title:tesla AND page_category:"/News" AND language:"en"
domain:"techcrunch.com" AND title:IPO
```

### Filter fields

#### `recent` — recency filter (Lucene query field)

`recent` is a special field you include in the Lucene query string. It is not an indexed document field — the matcher extracts it from the query before evaluation and applies it as a server-side filter.

Only return pages published within a rolling time window. Format: a positive integer followed by `h` (hours), `d` (days), or `mo` (months).

```
recent:1h                            # published in the last hour
recent:24h                           # published in the last 24 hours
recent:7d                            # published in the last 7 days
recent:3mo                           # published in the last 3 months
title:tesla AND recent:24h           # tesla in title, last 24 hours only
```

When omitted, no recency filter is applied (all matching pages are returned regardless of age).

#### `nsfw` — adult content filter (rule object field)

A boolean field on the rule object (not part of the Lucene query). Controls whether results include adult content.

- `true` — include adult content
- `false` or omitted — exclude adult content (default)

Set via the `nsfw` field when creating or updating a rule:
```json
{ "value": "title:tesla", "nsfw": true }
```

#### `quality` — quality filter (rule object field)

A boolean field on the rule object (not part of the Lucene query). Controls whether quality filters are applied on top of the Lucene query. When enabled, results are filtered to:

- Pages published within the last 7 days
- No pagination URLs (e.g. `/page/1`, `/page/2`)
- No tag or category index URLs (e.g. `/tag/seo`, `/category/news`)
- No URLs with query parameters (e.g. `?page=2`, `?sort=date`)

This removes low-value and duplicate content, keeping only fresh, canonical pages.

- `true` or omitted — quality filters applied (default)
- `false` — disable quality filters, return all matches

Set via the `quality` field when creating or updating a rule:
```json
{ "value": "domain:\"example.com\"", "quality": false }
```

### added/removed/anchor field behavior

- `added`: text from **inserted** (`"ins"`) diff chunks only. This is the default field for bare terms.
- `removed`: text from **deleted** (`"del"`) diff chunks only.
- `added_anchor`: anchor text from **inserted** links only.
- `removed_anchor`: anchor text from **deleted** links only.

```
"hello world"       → matches added (ins chunks indexed)
"removed text"      → matches removed (del chunks indexed), not added
added_anchor:buy    → anchor text "buy" appeared in inserted links
removed_anchor:buy  → anchor text "buy" appeared in deleted links
```

### Allowed `page_type` values

<details>
<summary>All page types (110+)</summary>

```
/Listing
/Listing/Product
/Listing/Property
/Listing/Job
/Listing/Service
/Listing/Event
/Listing/Location
/Listing/Business
/Listing_Collection
/Listing_Collection/Product
/Listing_Collection/Property
/Listing_Collection/Job
/Listing_Collection/Service
/Listing_Collection/Event
/Listing_Collection/Location
/Listing_Collection/Business
/Article
/Article/How_to
/Article/Tutorial_or_Guide
/Article/Listicle
/Article/Comparisons
/Article/Roundup
/Article/Product_or_Brand_Review
/Article/Opinion_Piece
/Article/News_Update
/Article/Thought_Leadership
/Article/Story
/Article/Recipe
/Article/FAQ
/Article/Checklists
/Article/Study_or_Research_Findings
/Article/Definitions
/Article/Wiki
/Landing_Page
/Landing_Page/Service_Page
/Landing_Page/Location_Page
/Landing_Page/Product_Page
/Landing_Page/Course_Sales_Page
/Landing_Page/Product_Feature_Page
/Landing_Page/Pricing_Page
/Interactive_Tools
/Interactive_Tools/Calculator
/Interactive_Tools/SaaS_Software
/Interactive_Tools/Map
/Interactive_Tools/Quiz
/Interactive_Tools/Poll
/Interactive_Tools/Simulator
/Interactive_Tools/Generator
/Interactive_Tools/Configurator
/Image
/Image/Infographic
/Image/Mapographic
/Image/Photography
/Image/Vector_Illustration
/Image/Meme
/Image/Diagram
/Image/Flowchart
/Video
/Video/How_to
/Video/Tutorial_or_Guide
/Video/Listicle
/Video/Comparisons
/Video/Compilation
/Video/Roundup
/Video/Product_or_Brand_Review
/Video/Opinion_Piece
/Video/News_Update
/Video/Thought_Leadership
/Video/Story
/Video/Recipe
/Video/Interview
/Video/Webinar
/Video/Vlog
/Audio
/Audio/Podcast
/Audio/Webinar
/Audio/Interview
/Audio/Sound_Byte
/Audio/Music
/Audio/Audiobook
/Audio/Commentary
/Document
/Document/Case_Study
/Document/Ebook
/Document/White_Paper
/Document/Slide_Deck
/Document/Research_Paper
/Document/Template
/Document/Report
/Document/Manual
/Document/Worksheet
/User_Generated_Content
/User_Generated_Content/Forum_Thread
/User_Generated_Content/Discussions
/User_Generated_Content/Social_Media_Post
/User_Generated_Content/Reviews
/User_Generated_Content/Testimonials
/User_Generated_Content/Comments
/User_Generated_Content/Q&A
/Core_Page
/Core_Page/Homepage
/Core_Page/About_Page
/Core_Page/Contact_Page
/Core_Page/FAQ_Page
/Core_Page/Blog_Index
/Core_Page/Services_Page
/Core_Page/Portfolio_Page
/Core_Page/Careers_Page
/Core_Page/Privacy_Policy_Page
/Core_Page/T&C_Page
```

</details>

### Allowed `page_category` values

<details>
<summary>Top-level categories (25)</summary>

```
/Adult
/Arts_and_Entertainment
/Autos_and_Vehicles
/Beauty_and_Fitness
/Books_and_Literature
/Business_and_Industrial
/Computers_and_Electronics
/Finance
/Food_and_Drink
/Games
/Health
/Hobbies_and_Leisure
/Home_and_Garden
/Internet_and_Telecom
/Jobs_and_Education
/Law_and_Government
/News
/Online_Communities
/People_and_Society
/Pets_and_Animals
/Real_Estate
/Reference
/Science
/Sensitive_Subjects
/Shopping
/Sports
/Travel_and_Transportation
```

Categories support hierarchical subcategories (e.g. `/News/Technology_News`, `/Sports/Winter_Sports/Skiing_and_Snowboarding`). Full list of subcategories:

<details>
<summary>All subcategories (700+)</summary>

```
/Arts_and_Entertainment/Celebrities_and_Entertainment_News
/Arts_and_Entertainment/Comics_and_Animation
/Arts_and_Entertainment/Comics_and_Animation/Anime_and_Manga
/Arts_and_Entertainment/Comics_and_Animation/Cartoons
/Arts_and_Entertainment/Comics_and_Animation/Comics
/Arts_and_Entertainment/Entertainment_Industry
/Arts_and_Entertainment/Entertainment_Industry/Film_and_TV_Industry
/Arts_and_Entertainment/Entertainment_Industry/Recording_Industry
/Arts_and_Entertainment/Events_and_Listings
/Arts_and_Entertainment/Events_and_Listings/Bars,_Clubs_and_Nightlife
/Arts_and_Entertainment/Events_and_Listings/Concerts_and_Music_Festivals
/Arts_and_Entertainment/Events_and_Listings/Event_Ticket_Sales
/Arts_and_Entertainment/Events_and_Listings/Expos_and_Conventions
/Arts_and_Entertainment/Events_and_Listings/Film_Festivals
/Arts_and_Entertainment/Events_and_Listings/Food_and_Beverage_Events
/Arts_and_Entertainment/Events_and_Listings/Live_Sporting_Events
/Arts_and_Entertainment/Events_and_Listings/Movie_Listings_and_Theater_Showtimes
/Arts_and_Entertainment/Fun_and_Trivia
/Arts_and_Entertainment/Fun_and_Trivia/Flash-Based_Entertainment
/Arts_and_Entertainment/Fun_and_Trivia/Fun_Tests_and_Silly_Surveys
/Arts_and_Entertainment/Humor
/Arts_and_Entertainment/Humor/Funny_Pictures_and_Videos
/Arts_and_Entertainment/Humor/Live_Comedy
/Arts_and_Entertainment/Humor/Political_Humor
/Arts_and_Entertainment/Humor/Spoofs_and_Satire
/Arts_and_Entertainment/Movies
/Arts_and_Entertainment/Movies/Action_and_Adventure_Films
/Arts_and_Entertainment/Movies/Animated_Films
/Arts_and_Entertainment/Movies/Bollywood_and_South_Asian_Films
/Arts_and_Entertainment/Movies/Classic_Films
/Arts_and_Entertainment/Movies/Comedy_Films
/Arts_and_Entertainment/Movies/Cult_and_Indie_Films
/Arts_and_Entertainment/Movies/DVD_and_Video_Shopping
/Arts_and_Entertainment/Movies/Documentary_Films
/Arts_and_Entertainment/Movies/Drama_Films
/Arts_and_Entertainment/Movies/Family_Films
/Arts_and_Entertainment/Movies/Horror_Films
/Arts_and_Entertainment/Movies/Movie_Memorabilia
/Arts_and_Entertainment/Movies/Movie_Reference
/Arts_and_Entertainment/Movies/Musical_Films
/Arts_and_Entertainment/Movies/Romance_Films
/Arts_and_Entertainment/Movies/Science_Fiction_and_Fantasy_Films
/Arts_and_Entertainment/Movies/Thriller,_Crime_and_Mystery_Films
/Arts_and_Entertainment/Music_and_Audio
/Arts_and_Entertainment/Music_and_Audio/CD_and_Audio_Shopping
/Arts_and_Entertainment/Music_and_Audio/Classical_Music
/Arts_and_Entertainment/Music_and_Audio/Country_Music
/Arts_and_Entertainment/Music_and_Audio/Dance_and_Electronic_Music
/Arts_and_Entertainment/Music_and_Audio/Experimental_and_Industrial_Music
/Arts_and_Entertainment/Music_and_Audio/Folk_and_Traditional_Music
/Arts_and_Entertainment/Music_and_Audio/Jazz_and_Blues
/Arts_and_Entertainment/Music_and_Audio/Music_Art_and_Memorabilia
/Arts_and_Entertainment/Music_and_Audio/Music_Education_and_Instruction
/Arts_and_Entertainment/Music_and_Audio/Music_Equipment_and_Technology
/Arts_and_Entertainment/Music_and_Audio/Music_Reference
/Arts_and_Entertainment/Music_and_Audio/Music_Streams_and_Downloads
/Arts_and_Entertainment/Music_and_Audio/Music_Videos
/Arts_and_Entertainment/Music_and_Audio/Podcasts
/Arts_and_Entertainment/Music_and_Audio/Pop_Music
/Arts_and_Entertainment/Music_and_Audio/Radio
/Arts_and_Entertainment/Music_and_Audio/Religious_Music
/Arts_and_Entertainment/Music_and_Audio/Rock_Music
/Arts_and_Entertainment/Music_and_Audio/Soundtracks
/Arts_and_Entertainment/Music_and_Audio/Urban_and_Hip-Hop
/Arts_and_Entertainment/Music_and_Audio/Vocals_and_Show_Tunes
/Arts_and_Entertainment/Music_and_Audio/World_Music
/Arts_and_Entertainment/Offbeat
/Arts_and_Entertainment/Offbeat/Occult_and_Paranormal
/Arts_and_Entertainment/Online_Media
/Arts_and_Entertainment/Online_Media/Online_Image_Galleries
/Arts_and_Entertainment/Online_Media/Virtual_Tours
/Arts_and_Entertainment/Performing_Arts
/Arts_and_Entertainment/Performing_Arts/Acting_and_Theater
/Arts_and_Entertainment/Performing_Arts/Broadway_and_Musical_Theater
/Arts_and_Entertainment/Performing_Arts/Circus
/Arts_and_Entertainment/Performing_Arts/Dance
/Arts_and_Entertainment/Performing_Arts/Magic
/Arts_and_Entertainment/Performing_Arts/Opera
/Arts_and_Entertainment/TV_and_Video
/Arts_and_Entertainment/TV_and_Video/Online_Video
/Arts_and_Entertainment/TV_and_Video/TV_Commercials
/Arts_and_Entertainment/TV_and_Video/TV_Guides_and_Reference
/Arts_and_Entertainment/TV_and_Video/TV_Networks_and_Stations
/Arts_and_Entertainment/TV_and_Video/TV_Shows_and_Programs
/Arts_and_Entertainment/Visual_Art_and_Design
/Arts_and_Entertainment/Visual_Art_and_Design/Architecture
/Arts_and_Entertainment/Visual_Art_and_Design/Art_Museums_and_Galleries
/Arts_and_Entertainment/Visual_Art_and_Design/Design
/Arts_and_Entertainment/Visual_Art_and_Design/Painting
/Arts_and_Entertainment/Visual_Art_and_Design/Photographic_and_Digital_Arts
/Arts_and_Entertainment/Visual_Art_and_Design/Sculpture
/Arts_and_Entertainment/Visual_Art_and_Design/Visual_Arts_and_Design_Education
/Autos_and_Vehicles/Bicycles_and_Accessories
/Autos_and_Vehicles/Bicycles_and_Accessories/BMX_Bikes
/Autos_and_Vehicles/Bicycles_and_Accessories/Bike_Accessories
/Autos_and_Vehicles/Bicycles_and_Accessories/Bike_Frames
/Autos_and_Vehicles/Bicycles_and_Accessories/Bike_Helmets_and_Protective_Gear
/Autos_and_Vehicles/Bicycles_and_Accessories/Bike_Parts_and_Repair
/Autos_and_Vehicles/Bicycles_and_Accessories/Cruiser_Bicycles
/Autos_and_Vehicles/Bicycles_and_Accessories/Electric_Bicycles
/Autos_and_Vehicles/Bicycles_and_Accessories/Kids'_Bikes
/Autos_and_Vehicles/Bicycles_and_Accessories/Mountain_Bikes
/Autos_and_Vehicles/Bicycles_and_Accessories/Road_Bikes
/Autos_and_Vehicles/Boats_and_Watercraft
/Autos_and_Vehicles/Campers_and_RVs
/Autos_and_Vehicles/Classic_Vehicles
/Autos_and_Vehicles/Commercial_Vehicles
/Autos_and_Vehicles/Commercial_Vehicles/Cargo_Trucks_and_Trailers
/Autos_and_Vehicles/Custom_and_Performance_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Audi
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/BMW
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Bentley
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Buick
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Cadillac
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Chevrolet
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Chrysler
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Citroën
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Daewoo_Motors
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Dodge
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Ferrari
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Fiat
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Ford
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/GMC
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Honda
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Hummer
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Hyundai
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Isuzu
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Jaguar
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Jeep
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Kia
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Lamborghini
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Land_Rover
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Lincoln
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Maserati
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Mazda
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Mercedes-Benz
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Mercury
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Mini
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Mitsubishi
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Nissan
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Peugeot
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Pontiac
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Porsche
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Ram_Trucks
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Renault
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Rolls-Royce
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/SEAT
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Saab
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Saturn
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Skoda
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Subaru
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Suzuki
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Tesla_Motors
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Toyota
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Vauxhall-Opel
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Volkswagen
/Autos_and_Vehicles/Motor_Vehicles_(By_Brand)/Volvo
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Autonomous_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Compact_Cars
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Convertibles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Coupes
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Diesel_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Hatchbacks
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Hybrid_and_Alternative_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Luxury_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Microcars_and_Subcompacts
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Motorcycles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Off-Road_Vehicles
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Scooters_and_Mopeds
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Sedans
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Sports_Cars
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Station_Wagons
/Autos_and_Vehicles/Motor_Vehicles_(By_Type)/Trucks,_Vans_and_SUVs
/Autos_and_Vehicles/Personal_Aircraft
/Autos_and_Vehicles/Vehicle_Codes_and_Driving_Laws
/Autos_and_Vehicles/Vehicle_Codes_and_Driving_Laws/Drunk_Driving_Law
/Autos_and_Vehicles/Vehicle_Codes_and_Driving_Laws/Vehicle_Licensing_and_Registration
/Autos_and_Vehicles/Vehicle_Parts_and_Services
/Autos_and_Vehicles/Vehicle_Parts_and_Services/Gas_Prices_and_Vehicle_Fueling
/Autos_and_Vehicles/Vehicle_Parts_and_Services/Towing_and_Roadside_Assistance
/Autos_and_Vehicles/Vehicle_Parts_and_Services/Vehicle_Modification_and_Tuning
/Autos_and_Vehicles/Vehicle_Parts_and_Services/Vehicle_Parts_and_Accessories
/Autos_and_Vehicles/Vehicle_Parts_and_Services/Vehicle_Repair_and_Maintenance
/Autos_and_Vehicles/Vehicle_Shopping
/Autos_and_Vehicles/Vehicle_Shopping/Used_Vehicles
/Autos_and_Vehicles/Vehicle_Shopping/Vehicle_Dealers_and_Retailers
/Autos_and_Vehicles/Vehicle_Shopping/Vehicle_Specs,_Reviews_and_Comparisons
/Autos_and_Vehicles/Vehicle_Shows
/Beauty_and_Fitness/Beauty_Pageants
/Beauty_and_Fitness/Beauty_Services_and_Spas
/Beauty_and_Fitness/Beauty_Services_and_Spas/Cosmetic_Procedures
/Beauty_and_Fitness/Beauty_Services_and_Spas/Manicures_and_Pedicures
/Beauty_and_Fitness/Beauty_Services_and_Spas/Massage_Therapy
/Beauty_and_Fitness/Body_Art
/Beauty_and_Fitness/Cosmetology_and_Beauty_Professionals
/Beauty_and_Fitness/Face_and_Body_Care
/Beauty_and_Fitness/Face_and_Body_Care/Clean_Beauty
/Beauty_and_Fitness/Face_and_Body_Care/Hygiene_and_Toiletries
/Beauty_and_Fitness/Face_and_Body_Care/Make-Up_and_Cosmetics
/Beauty_and_Fitness/Face_and_Body_Care/Perfumes_and_Fragrances
/Beauty_and_Fitness/Face_and_Body_Care/Skin_and_Nail_Care
/Beauty_and_Fitness/Face_and_Body_Care/Sun_Care_and_Tanning_Products
/Beauty_and_Fitness/Face_and_Body_Care/Unwanted_Body_and_Facial_Hair_Removal
/Beauty_and_Fitness/Fashion_and_Style
/Beauty_and_Fitness/Fashion_and_Style/Fashion_Designers_and_Collections
/Beauty_and_Fitness/Fitness
/Beauty_and_Fitness/Fitness/Bodybuilding
/Beauty_and_Fitness/Fitness/Fitness_Equipment_and_Accessories
/Beauty_and_Fitness/Fitness/Fitness_Instruction_and_Personal_Training
/Beauty_and_Fitness/Fitness/Gyms_and_Health_Clubs
/Beauty_and_Fitness/Fitness/High_Intensity_Interval_Training
/Beauty_and_Fitness/Fitness/Yoga_and_Pilates
/Beauty_and_Fitness/Hair_Care
/Beauty_and_Fitness/Hair_Care/Hair_Loss
/Beauty_and_Fitness/Hair_Care/Shampoos_and_Conditioners
/Beauty_and_Fitness/Weight_Loss
/Books_and_Literature/Audiobooks
/Books_and_Literature/Book_Retailers
/Books_and_Literature/Children's_Literature
/Books_and_Literature/E-Books
/Books_and_Literature/Fan_Fiction
/Books_and_Literature/Literary_Classics
/Books_and_Literature/Poetry
/Books_and_Literature/Writers_Resources
/Business_and_Industrial/Advertising_and_Marketing
/Business_and_Industrial/Advertising_and_Marketing/Brand_Management
/Business_and_Industrial/Advertising_and_Marketing/Marketing
/Business_and_Industrial/Advertising_and_Marketing/Public_Relations
/Business_and_Industrial/Advertising_and_Marketing/Sales
/Business_and_Industrial/Advertising_and_Marketing/Telemarketing
/Business_and_Industrial/Aerospace_and_Defense
/Business_and_Industrial/Aerospace_and_Defense/Aviation_Industry
/Business_and_Industrial/Aerospace_and_Defense/Space_Technology
/Business_and_Industrial/Agriculture_and_Forestry
/Business_and_Industrial/Agriculture_and_Forestry/Agricultural_Equipment
/Business_and_Industrial/Agriculture_and_Forestry/Aquaculture
/Business_and_Industrial/Agriculture_and_Forestry/Crops_and_Seed
/Business_and_Industrial/Agriculture_and_Forestry/Farms_and_Ranches
/Business_and_Industrial/Agriculture_and_Forestry/Forestry
/Business_and_Industrial/Agriculture_and_Forestry/Livestock
/Business_and_Industrial/Automotive_Industry
/Business_and_Industrial/Business_Education
/Business_and_Industrial/Business_Finance
/Business_and_Industrial/Business_Finance/Commercial_Lending
/Business_and_Industrial/Business_Finance/Investment_Banking
/Business_and_Industrial/Business_Finance/Risk_Management
/Business_and_Industrial/Business_Finance/Venture_Capital
/Business_and_Industrial/Business_Operations
/Business_and_Industrial/Business_Operations/Business_Plans_and_Presentations
/Business_and_Industrial/Business_Operations/Flexible_Work_Arrangements
/Business_and_Industrial/Business_Operations/Human_Resources
/Business_and_Industrial/Business_Operations/Management
/Business_and_Industrial/Business_Services
/Business_and_Industrial/Business_Services/Commercial_Distribution
/Business_and_Industrial/Business_Services/Consulting
/Business_and_Industrial/Business_Services/Corporate_Events
/Business_and_Industrial/Business_Services/E-Commerce_Services
/Business_and_Industrial/Business_Services/Fire_and_Security_Services
/Business_and_Industrial/Business_Services/Knowledge_Management
/Business_and_Industrial/Business_Services/Office_Services
/Business_and_Industrial/Business_Services/Office_Supplies
/Business_and_Industrial/Business_Services/Outsourcing
/Business_and_Industrial/Business_Services/Physical_Asset_Management
/Business_and_Industrial/Business_Services/Quality_Control_and_Tracking
/Business_and_Industrial/Business_Services/Shared_Workspaces
/Business_and_Industrial/Business_Services/Signage
/Business_and_Industrial/Business_Services/Warehousing
/Business_and_Industrial/Business_Services/Writing_and_Editing_Services
/Business_and_Industrial/Chemicals_Industry
/Business_and_Industrial/Chemicals_Industry/Agrochemicals
/Business_and_Industrial/Chemicals_Industry/Cleaning_Agents
/Business_and_Industrial/Chemicals_Industry/Coatings_and_Adhesives
/Business_and_Industrial/Chemicals_Industry/Dyes_and_Pigments
/Business_and_Industrial/Chemicals_Industry/Plastics_and_Polymers
/Business_and_Industrial/Construction_and_Maintenance
/Business_and_Industrial/Construction_and_Maintenance/Building_Materials_and_Supplies
/Business_and_Industrial/Construction_and_Maintenance/Civil_Engineering
/Business_and_Industrial/Energy_and_Utilities
/Business_and_Industrial/Energy_and_Utilities/Electricity
/Business_and_Industrial/Energy_and_Utilities/Nuclear_Energy
/Business_and_Industrial/Energy_and_Utilities/Oil_and_Gas
/Business_and_Industrial/Energy_and_Utilities/Renewable_and_Alternative_Energy
/Business_and_Industrial/Energy_and_Utilities/Waste_Management
/Business_and_Industrial/Hospitality_Industry
/Business_and_Industrial/Hospitality_Industry/Event_Planning
/Business_and_Industrial/Hospitality_Industry/Event_Venue_Rentals
/Business_and_Industrial/Hospitality_Industry/Food_Service
/Business_and_Industrial/Industrial_Materials_and_Equipment
/Business_and_Industrial/Industrial_Materials_and_Equipment/Fluid_Handling
/Business_and_Industrial/Industrial_Materials_and_Equipment/Generators
/Business_and_Industrial/Industrial_Materials_and_Equipment/Heavy_Machinery
/Business_and_Industrial/Industrial_Materials_and_Equipment/Industrial_Handling_and_Processing_Equipment
/Business_and_Industrial/Industrial_Materials_and_Equipment/Industrial_Measurement_and_Control_Equipment
/Business_and_Industrial/Manufacturing
/Business_and_Industrial/Manufacturing/Factory_Automation
/Business_and_Industrial/Metals_and_Mining
/Business_and_Industrial/Metals_and_Mining/Precious_Metals
/Business_and_Industrial/Pharmaceuticals_and_Biotech
/Business_and_Industrial/Printing_and_Publishing
/Business_and_Industrial/Printing_and_Publishing/Document_and_Printing_Services
/Business_and_Industrial/Retail_Trade
/Business_and_Industrial/Retail_Trade/Retail_Equipment_and_Technology
/Business_and_Industrial/Shipping_and_Logistics
/Business_and_Industrial/Shipping_and_Logistics/Freight_Transport
/Business_and_Industrial/Shipping_and_Logistics/Freight_Transport/Maritime_Transport
/Business_and_Industrial/Shipping_and_Logistics/Freight_Transport/Rail_Freight
/Business_and_Industrial/Shipping_and_Logistics/Import_and_Export
/Business_and_Industrial/Shipping_and_Logistics/Mail_and_Package_Delivery
/Business_and_Industrial/Shipping_and_Logistics/Moving_and_Relocation
/Business_and_Industrial/Shipping_and_Logistics/Packaging
/Business_and_Industrial/Shipping_and_Logistics/Self_Storage
/Business_and_Industrial/Small_Business
/Business_and_Industrial/Small_Business/Business_Formation
/Business_and_Industrial/Small_Business/Home_Office
/Business_and_Industrial/Small_Business/MLM_and_Business_Opportunities
/Business_and_Industrial/Textiles_and_Nonwovens
/Computers_and_Electronics/CAD_and_CAM
/Computers_and_Electronics/Computer_Hardware
/Computers_and_Electronics/Computer_Hardware/Computer_Components
/Computers_and_Electronics/Computer_Hardware/Computer_Drives_and_Storage
/Computers_and_Electronics/Computer_Hardware/Computer_Peripherals
/Computers_and_Electronics/Computer_Hardware/Computer_Servers
/Computers_and_Electronics/Computer_Hardware/Desktop_Computers
/Computers_and_Electronics/Computer_Hardware/Hardware_Modding_and_Tuning
/Computers_and_Electronics/Computer_Hardware/Laptops_and_Notebooks
/Computers_and_Electronics/Computer_Security
/Computers_and_Electronics/Computer_Security/Antivirus_and_Malware
/Computers_and_Electronics/Computer_Security/Hacking_and_Cracking
/Computers_and_Electronics/Computer_Security/Network_Security
/Computers_and_Electronics/Consumer_Electronics
/Computers_and_Electronics/Consumer_Electronics/Audio_Equipment
/Computers_and_Electronics/Consumer_Electronics/Camera_and_Photo_Equipment
/Computers_and_Electronics/Consumer_Electronics/Car_Electronics
/Computers_and_Electronics/Consumer_Electronics/Drones_and_RC_Aircraft
/Computers_and_Electronics/Consumer_Electronics/Electronic_Accessories
/Computers_and_Electronics/Consumer_Electronics/GPS_and_Navigation
/Computers_and_Electronics/Consumer_Electronics/Gadgets_and_Portable_Electronics
/Computers_and_Electronics/Consumer_Electronics/Game_Systems_and_Consoles
/Computers_and_Electronics/Consumer_Electronics/Home_Automation
/Computers_and_Electronics/Consumer_Electronics/Media_Streaming_Devices
/Computers_and_Electronics/Consumer_Electronics/TV_and_Video_Equipment
/Computers_and_Electronics/Consumer_Electronics/Virtual_Reality_Devices
/Computers_and_Electronics/Electronics_and_Electrical
/Computers_and_Electronics/Electronics_and_Electrical/Data_Sheets_and_Electronics_Reference
/Computers_and_Electronics/Electronics_and_Electrical/Electrical_Test_and_Measurement
/Computers_and_Electronics/Electronics_and_Electrical/Electromechanical_Devices
/Computers_and_Electronics/Electronics_and_Electrical/Electronic_Components
/Computers_and_Electronics/Electronics_and_Electrical/Optoelectronics_and_Fiber
/Computers_and_Electronics/Electronics_and_Electrical/Power_Supplies
/Computers_and_Electronics/Enterprise_Technology
/Computers_and_Electronics/Enterprise_Technology/Customer_Relationship_Management_(CRM)
/Computers_and_Electronics/Enterprise_Technology/Data_Management
/Computers_and_Electronics/Enterprise_Technology/Enterprise_Resource_Planning_(ERP)
/Computers_and_Electronics/Enterprise_Technology/Helpdesk_and_Customer_Support_Systems
/Computers_and_Electronics/Networking
/Computers_and_Electronics/Networking/Data_Formats_and_Protocols
/Computers_and_Electronics/Networking/Distributed_and_Cloud_Computing
/Computers_and_Electronics/Networking/Network_Monitoring_and_Management
/Computers_and_Electronics/Networking/Networking_Equipment
/Computers_and_Electronics/Networking/VPN_and_Remote_Access
/Computers_and_Electronics/Programming
/Computers_and_Electronics/Programming/C_and_C++
/Computers_and_Electronics/Programming/Development_Tools
/Computers_and_Electronics/Programming/Java_(Programming_Language)
/Computers_and_Electronics/Programming/Scripting_Languages
/Computers_and_Electronics/Programming/Windows_and_.NET
/Computers_and_Electronics/Software
/Computers_and_Electronics/Software/Business_and_Productivity_Software
/Computers_and_Electronics/Software/Device_Drivers
/Computers_and_Electronics/Software/Educational_Software
/Computers_and_Electronics/Software/Freeware_and_Shareware
/Computers_and_Electronics/Software/Intelligent_Personal_Assistants
/Computers_and_Electronics/Software/Internet_Software
/Computers_and_Electronics/Software/Monitoring_Software
/Computers_and_Electronics/Software/Multimedia_Software
/Computers_and_Electronics/Software/Open_Source
/Computers_and_Electronics/Software/Operating_Systems
/Computers_and_Electronics/Software/Software_Utilities
/Finance/Accounting_and_Auditing
/Finance/Accounting_and_Auditing/Billing_and_Invoicing
/Finance/Accounting_and_Auditing/Bookkeeping
/Finance/Accounting_and_Auditing/Tax_Preparation_and_Planning
/Finance/Banking
/Finance/Banking/ATMs_and_Branch_Locations
/Finance/Banking/Debit_and_Checking_Services
/Finance/Banking/Mobile_Payments_and_Digital_Wallets
/Finance/Banking/Money_Transfer_and_Wire_Services
/Finance/Banking/Savings_Accounts
/Finance/Credit_and_Lending
/Finance/Credit_and_Lending/Credit_Cards
/Finance/Credit_and_Lending/Credit_Reporting_and_Monitoring
/Finance/Credit_and_Lending/Debt_Collection_and_Repossession
/Finance/Credit_and_Lending/Debt_Management
/Finance/Credit_and_Lending/Loans
/Finance/Crowdfunding
/Finance/Financial_Planning_and_Management
/Finance/Financial_Planning_and_Management/Asset_and_Portfolio_Management
/Finance/Financial_Planning_and_Management/Inheritance_and_Estate_Planning
/Finance/Financial_Planning_and_Management/Retirement_and_Pension
/Finance/Grants,_Scholarships_and_Financial_Aid
/Finance/Grants,_Scholarships_and_Financial_Aid/Government_Grants
/Finance/Grants,_Scholarships_and_Financial_Aid/Study_Grants_and_Scholarships
/Finance/Insurance
/Finance/Insurance/Health_Insurance
/Finance/Insurance/Home_Insurance
/Finance/Insurance/Life_Insurance
/Finance/Insurance/Travel_Insurance
/Finance/Insurance/Vehicle_Insurance
/Finance/Investing
/Finance/Investing/Brokerages_and_Day_Trading
/Finance/Investing/Commodities_and_Futures_Trading
/Finance/Investing/Currencies_and_Foreign_Exchange
/Finance/Investing/Derivatives
/Finance/Investing/Funds
/Finance/Investing/Real_Estate_Investment_Trusts
/Finance/Investing/Socially_Responsible_Investing
/Finance/Investing/Stocks_and_Bonds
/Food_and_Drink/Beverages
/Food_and_Drink/Beverages/Alcohol-Free_Beverages
/Food_and_Drink/Beverages/Alcoholic_Beverages
/Food_and_Drink/Beverages/Bottled_Water
/Food_and_Drink/Beverages/Coffee_and_Tea
/Food_and_Drink/Beverages/Energy_Drinks
/Food_and_Drink/Beverages/Juice
/Food_and_Drink/Beverages/Nutrition_Drinks_and_Shakes
/Food_and_Drink/Beverages/Soft_Drinks
/Food_and_Drink/Beverages/Sports_Drinks
/Food_and_Drink/Cooking_and_Recipes
/Food_and_Drink/Cooking_and_Recipes/BBQ_and_Grilling
/Food_and_Drink/Cooking_and_Recipes/Cuisines
/Food_and_Drink/Cooking_and_Recipes/Culinary_Training
/Food_and_Drink/Cooking_and_Recipes/Desserts
/Food_and_Drink/Cooking_and_Recipes/Healthy_Eating
/Food_and_Drink/Cooking_and_Recipes/Salads
/Food_and_Drink/Cooking_and_Recipes/Soups_and_Stews
/Food_and_Drink/Food
/Food_and_Drink/Food/Baked_Goods
/Food_and_Drink/Food/Breakfast_Foods
/Food_and_Drink/Food/Candy_and_Sweets
/Food_and_Drink/Food/Condiments_and_Dressings
/Food_and_Drink/Food/Cooking_Fats_and_Oils
/Food_and_Drink/Food/Dairy_and_Egg_Substitutes
/Food_and_Drink/Food/Dairy_and_Eggs
/Food_and_Drink/Food/Fruits_and_Vegetables
/Food_and_Drink/Food/Gourmet_and_Specialty_Foods
/Food_and_Drink/Food/Grains_and_Pasta
/Food_and_Drink/Food/Herbs_and_Spices
/Food_and_Drink/Food/Jams,_Jellies_and_Preserves
/Food_and_Drink/Food/Meat_and_Seafood
/Food_and_Drink/Food/Meat_and_Seafood_Substitutes
/Food_and_Drink/Food/Organic_and_Natural_Foods
/Food_and_Drink/Food/Snack_Foods
/Food_and_Drink/Food_and_Grocery_Delivery
/Food_and_Drink/Food_and_Grocery_Delivery/Grocery_Delivery_Services
/Food_and_Drink/Food_and_Grocery_Delivery/Meal_Kits
/Food_and_Drink/Food_and_Grocery_Delivery/Restaurant_Delivery_Services
/Food_and_Drink/Food_and_Grocery_Retailers
/Food_and_Drink/Food_and_Grocery_Retailers/Bakeries
/Food_and_Drink/Food_and_Grocery_Retailers/Butchers
/Food_and_Drink/Food_and_Grocery_Retailers/Convenience_Stores
/Food_and_Drink/Food_and_Grocery_Retailers/Delicatessens
/Food_and_Drink/Food_and_Grocery_Retailers/Farmers'_Markets
/Food_and_Drink/Restaurants
/Food_and_Drink/Restaurants/Catering
/Food_and_Drink/Restaurants/Fast_Food
/Food_and_Drink/Restaurants/Fine_Dining
/Food_and_Drink/Restaurants/Pizzerias
/Food_and_Drink/Restaurants/Restaurant_Reviews_and_Reservations
/Games/Arcade_and_Coin-Op_Games
/Games/Board_Games
/Games/Board_Games/Chess_and_Abstract_Strategy_Games
/Games/Board_Games/Miniatures_and_Wargaming
/Games/Card_Games
/Games/Card_Games/Collectible_Card_Games
/Games/Card_Games/Poker_and_Casino_Games
/Games/Computer_and_Video_Games
/Games/Computer_and_Video_Games/Action_and_Platform_Games
/Games/Computer_and_Video_Games/Adventure_Games
/Games/Computer_and_Video_Games/Browser_Games
/Games/Computer_and_Video_Games/Casual_Games
/Games/Computer_and_Video_Games/Competitive_Video_Gaming
/Games/Computer_and_Video_Games/Driving_and_Racing_Games
/Games/Computer_and_Video_Games/Fighting_Games
/Games/Computer_and_Video_Games/Gaming_Reference_and_Reviews
/Games/Computer_and_Video_Games/Massively_Multiplayer_Games
/Games/Computer_and_Video_Games/Music_and_Dance_Games
/Games/Computer_and_Video_Games/Sandbox_Games
/Games/Computer_and_Video_Games/Shooter_Games
/Games/Computer_and_Video_Games/Simulation_Games
/Games/Computer_and_Video_Games/Sports_Games
/Games/Computer_and_Video_Games/Strategy_Games
/Games/Computer_and_Video_Games/Video_Game_Development
/Games/Computer_and_Video_Games/Video_Game_Emulation
/Games/Computer_and_Video_Games/Video_Game_Mods_and_Add-Ons
/Games/Computer_and_Video_Games/Video_Game_Retailers
/Games/Dice_Games
/Games/Educational_Games
/Games/Family-Oriented_Games_and_Activities
/Games/Family-Oriented_Games_and_Activities/Drawing_and_Coloring
/Games/Family-Oriented_Games_and_Activities/Dress-Up_and_Fashion_Games
/Games/Gambling
/Games/Gambling/Lottery
/Games/Gambling/Sports_Betting
/Games/Party_Games
/Games/Puzzles_and_Brainteasers
/Games/Roleplaying_Games
/Games/Table_Games
/Games/Table_Games/Billiards
/Games/Table_Games/Table_Tennis
/Games/Tile_Games
/Games/Word_Games
/Health/Aging_and_Geriatrics
/Health/Aging_and_Geriatrics/Alzheimer's_Disease
/Health/Alternative_and_Natural_Medicine
/Health/Alternative_and_Natural_Medicine/Acupuncture_and_Chinese_Medicine
/Health/Alternative_and_Natural_Medicine/Cleansing_and_Detoxification
/Health/Health_Conditions
/Health/Health_Conditions/AIDS_and_HIV
/Health/Health_Conditions/Allergies
/Health/Health_Conditions/Allergies/Environmental_Allergies
/Health/Health_Conditions/Allergies/Food_Allergies
/Health/Health_Conditions/Arthritis
/Health/Health_Conditions/Blood_Sugar_and_Diabetes
/Health/Health_Conditions/Cancer
/Health/Health_Conditions/Ear_Nose_and_Throat
/Health/Health_Conditions/Eating_Disorders
/Health/Health_Conditions/Endocrine_Conditions
/Health/Health_Conditions/GERD_and_Digestive_Disorders
/Health/Health_Conditions/Genetic_Disorders
/Health/Health_Conditions/Heart_and_Hypertension
/Health/Health_Conditions/Infectious_Diseases
/Health/Health_Conditions/Infectious_Diseases/Covid-19
/Health/Health_Conditions/Infectious_Diseases/Vaccines_and_Immunizations
/Health/Health_Conditions/Injury
/Health/Health_Conditions/Neurological_Conditions
/Health/Health_Conditions/Obesity
/Health/Health_Conditions/Pain_Management
/Health/Health_Conditions/Respiratory_Conditions
/Health/Health_Conditions/Skin_Conditions
/Health/Health_Conditions/Sleep_Disorders
/Health/Health_Education_and_Medical_Training
/Health/Health_Foundations_and_Medical_Research
/Health/Medical_Devices_and_Equipment
/Health/Medical_Devices_and_Equipment/Assistive_Technology
/Health/Medical_Facilities_and_Services
/Health/Medical_Facilities_and_Services/Doctors'_Offices
/Health/Medical_Facilities_and_Services/Hospitals_and_Treatment_Centers
/Health/Medical_Facilities_and_Services/Medical_Procedures
/Health/Medical_Facilities_and_Services/Medical_Procedures/Surgery
/Health/Medical_Facilities_and_Services/Medical_Procedures/Surgery/Cosmetic_Surgery
/Health/Medical_Facilities_and_Services/Physical_Therapy
/Health/Medical_Literature_and_Resources
/Health/Medical_Literature_and_Resources/Medical_Photos_and_Illustration
/Health/Men's_Health
/Health/Mental_Health
/Health/Mental_Health/Anxiety_and_Stress
/Health/Mental_Health/Compulsive_Gambling
/Health/Mental_Health/Counseling_Services
/Health/Mental_Health/Depression
/Health/Nursing
/Health/Nursing/Assisted_Living_and_Long_Term_Care
/Health/Nutrition
/Health/Nutrition/Special_and_Restricted_Diets
/Health/Nutrition/Vitamins_and_Supplements
/Health/Oral_and_Dental_Care
/Health/Pediatrics
/Health/Pharmacy
/Health/Pharmacy/Drugs_and_Medications
/Health/Public_Health
/Health/Public_Health/Health_Policy
/Health/Public_Health/Occupational_Health_and_Safety
/Health/Public_Health/Toxic_Substances_and_Poisoning
/Health/Reproductive_Health
/Health/Reproductive_Health/Birth_Control
/Health/Reproductive_Health/Infertility
/Health/Reproductive_Health/Male_Impotence
/Health/Reproductive_Health/OBGYN
/Health/Reproductive_Health/Sex_Education_and_Counseling
/Health/Substance_Abuse
/Health/Substance_Abuse/Drug_and_Alcohol_Testing
/Health/Substance_Abuse/Drug_and_Alcohol_Treatment
/Health/Substance_Abuse/Smoking_and_Smoking_Cessation
/Health/Substance_Abuse/Steroids_and_Performance-Enhancing_Drugs
/Health/Vision_Care
/Health/Vision_Care/Eye_Exams_and_Optometry
/Health/Vision_Care/Eyeglasses_and_Contacts
/Health/Vision_Care/Laser_Vision_Correction
/Health/Women's_Health
/Hobbies_and_Leisure/Clubs_and_Organizations
/Hobbies_and_Leisure/Clubs_and_Organizations/Youth_Organizations_and_Resources
/Hobbies_and_Leisure/Crafts
/Hobbies_and_Leisure/Crafts/Art_and_Craft_Supplies
/Hobbies_and_Leisure/Crafts/Ceramics_and_Pottery
/Hobbies_and_Leisure/Crafts/Fiber_and_Textile_Arts
/Hobbies_and_Leisure/Merit_Prizes_and_Contests
/Hobbies_and_Leisure/Outdoors
/Hobbies_and_Leisure/Outdoors/Fishing
/Hobbies_and_Leisure/Outdoors/Hiking_and_Camping
/Hobbies_and_Leisure/Outdoors/Hunting_and_Shooting
/Hobbies_and_Leisure/Paintball
/Hobbies_and_Leisure/Radio_Control_and_Modeling
/Hobbies_and_Leisure/Radio_Control_and_Modeling/Model_Trains_and_Railroads
/Hobbies_and_Leisure/Recreational_Aviation
/Hobbies_and_Leisure/Special_Occasions
/Hobbies_and_Leisure/Special_Occasions/Anniversaries
/Hobbies_and_Leisure/Special_Occasions/Holidays_and_Seasonal_Events
/Hobbies_and_Leisure/Special_Occasions/Weddings
/Hobbies_and_Leisure/Sweepstakes_and_Promotional_Giveaways
/Hobbies_and_Leisure/Water_Activities
/Hobbies_and_Leisure/Water_Activities/Boating
/Hobbies_and_Leisure/Water_Activities/Diving_and_Underwater_Activities
/Hobbies_and_Leisure/Water_Activities/Surf_and_Swim
/Home_and_Garden/Bed_and_Bath
/Home_and_Garden/Bed_and_Bath/Bathroom
/Home_and_Garden/Bed_and_Bath/Bedroom
/Home_and_Garden/Domestic_Services
/Home_and_Garden/Domestic_Services/Cleaning_Services
/Home_and_Garden/HVAC_and_Climate_Control
/Home_and_Garden/HVAC_and_Climate_Control/Air_Conditioners
/Home_and_Garden/HVAC_and_Climate_Control/Air_Filters_and_Purifiers
/Home_and_Garden/HVAC_and_Climate_Control/Fireplaces_and_Stoves
/Home_and_Garden/HVAC_and_Climate_Control/Heaters
/Home_and_Garden/HVAC_and_Climate_Control/Household_Fans
/Home_and_Garden/Home_Appliances
/Home_and_Garden/Home_Appliances/Vacuums_and_Floor_Care
/Home_and_Garden/Home_Appliances/Water_Filters_and_Purifiers
/Home_and_Garden/Home_Furnishings
/Home_and_Garden/Home_Furnishings/Clocks
/Home_and_Garden/Home_Furnishings/Countertops
/Home_and_Garden/Home_Furnishings/Curtains_and_Window_Treatments
/Home_and_Garden/Home_Furnishings/Kitchen_and_Dining_Furniture
/Home_and_Garden/Home_Furnishings/Lamps_and_Lighting
/Home_and_Garden/Home_Furnishings/Living_Room_Furniture
/Home_and_Garden/Home_Furnishings/Outdoor_Furniture
/Home_and_Garden/Home_Furnishings/Rugs_and_Carpets
/Home_and_Garden/Home_Improvement
/Home_and_Garden/Home_Improvement/Construction_and_Power_Tools
/Home_and_Garden/Home_Improvement/Doors_and_Windows
/Home_and_Garden/Home_Improvement/Flooring
/Home_and_Garden/Home_Improvement/House_Painting_and_Finishing
/Home_and_Garden/Home_Improvement/Locks_and_Locksmiths
/Home_and_Garden/Home_Improvement/Plumbing
/Home_and_Garden/Home_Improvement/Roofing
/Home_and_Garden/Home_Safety_and_Security
/Home_and_Garden/Home_Safety_and_Security/Home_Alarm_and_Security_Systems
/Home_and_Garden/Home_Storage_and_Shelving
/Home_and_Garden/Home_Storage_and_Shelving/Cabinetry
/Home_and_Garden/Home_Swimming_Pools,_Saunas_and_Spas
/Home_and_Garden/Home_and_Interior_Decor
/Home_and_Garden/Household_Supplies
/Home_and_Garden/Household_Supplies/Household_Batteries
/Home_and_Garden/Household_Supplies/Household_Cleaning_Supplies
/Home_and_Garden/Kitchen_and_Dining
/Home_and_Garden/Kitchen_and_Dining/Cookware_and_Diningware
/Home_and_Garden/Kitchen_and_Dining/Major_Kitchen_Appliances
/Home_and_Garden/Kitchen_and_Dining/Small_Kitchen_Appliances
/Home_and_Garden/Laundry
/Home_and_Garden/Laundry/Washers_and_Dryers
/Home_and_Garden/Patio,_Lawn_and_Garden
/Home_and_Garden/Patio,_Lawn_and_Garden/Barbecues_and_Grills
/Home_and_Garden/Patio,_Lawn_and_Garden/Garden_Structures
/Home_and_Garden/Patio,_Lawn_and_Garden/Gardening
/Home_and_Garden/Patio,_Lawn_and_Garden/Landscape_Design
/Home_and_Garden/Patio,_Lawn_and_Garden/Yard_Maintenance
/Home_and_Garden/Patio,_Lawn_and_Garden/Yard_Maintenance/Lawn_Mowers
/Home_and_Garden/Pest_Control
/Internet_and_Telecom/Communications_Equipment
/Internet_and_Telecom/Communications_Equipment/Radio_Equipment
/Internet_and_Telecom/Email_and_Messaging
/Internet_and_Telecom/Email_and_Messaging/Electronic_Spam
/Internet_and_Telecom/Email_and_Messaging/Email
/Internet_and_Telecom/Email_and_Messaging/Text_and_Instant_Messaging
/Internet_and_Telecom/Email_and_Messaging/Voice_and_Video_Chat
/Internet_and_Telecom/Mobile_and_Wireless
/Internet_and_Telecom/Mobile_and_Wireless/Mobile_Apps_and_Add-Ons
/Internet_and_Telecom/Mobile_and_Wireless/Mobile_Phones
/Internet_and_Telecom/Mobile_and_Wireless/Mobile_and_Wireless_Accessories
/Internet_and_Telecom/Search_Engines
/Internet_and_Telecom/Search_Engines/People_Search
/Internet_and_Telecom/Service_Providers
/Internet_and_Telecom/Service_Providers/Cable_and_Satellite_Providers
/Internet_and_Telecom/Service_Providers/ISPs
/Internet_and_Telecom/Service_Providers/Phone_Service_Providers
/Internet_and_Telecom/Teleconferencing
/Internet_and_Telecom/Web_Services
/Internet_and_Telecom/Web_Services/Affiliate_Programs
/Internet_and_Telecom/Web_Services/Cloud_Storage
/Internet_and_Telecom/Web_Services/Search_Engine_Optimization_and_Marketing
/Internet_and_Telecom/Web_Services/Web_Design_and_Development
/Internet_and_Telecom/Web_Services/Web_Stats_and_Analytics
/Jobs_and_Education/Education
/Jobs_and_Education/Education/Academic_Conferences_and_Publications
/Jobs_and_Education/Education/Alumni_and_Reunions
/Jobs_and_Education/Education/Colleges_and_Universities
/Jobs_and_Education/Education/Computer_Education
/Jobs_and_Education/Education/Distance_Learning
/Jobs_and_Education/Education/Early_Childhood_Education
/Jobs_and_Education/Education/Homeschooling
/Jobs_and_Education/Education/Open_Online_Courses
/Jobs_and_Education/Education/Primary_and_Secondary_Schooling_(K-12)
/Jobs_and_Education/Education/Private_Tutoring_Services
/Jobs_and_Education/Education/Special_Education
/Jobs_and_Education/Education/Standardized_and_Admissions_Tests
/Jobs_and_Education/Education/Study_Abroad
/Jobs_and_Education/Education/Teaching_and_Classroom_Resources
/Jobs_and_Education/Education/Training_and_Certification
/Jobs_and_Education/Education/Vocational_and_Continuing_Education
/Jobs_and_Education/Internships
/Jobs_and_Education/Jobs
/Jobs_and_Education/Jobs/Career_Resources_and_Planning
/Jobs_and_Education/Jobs/Job_Listings
/Jobs_and_Education/Jobs/Resumes_and_Portfolios
/Law_and_Government/Government
/Law_and_Government/Government/Courts_and_Judiciary
/Law_and_Government/Government/Embassies_and_Consulates
/Law_and_Government/Government/Executive_Branch
/Law_and_Government/Government/Government_Contracting_and_Procurement
/Law_and_Government/Government/Intelligence_and_Counterterrorism
/Law_and_Government/Government/Legislative_Branch
/Law_and_Government/Government/Lobbying
/Law_and_Government/Government/Public_Policy
/Law_and_Government/Government/Royalty
/Law_and_Government/Government/Visa_and_Immigration
/Law_and_Government/Legal
/Law_and_Government/Legal/Accident_and_Personal_Injury_Law
/Law_and_Government/Legal/Bankruptcy
/Law_and_Government/Legal/Business_and_Corporate_Law
/Law_and_Government/Legal/Constitutional_Law_and_Civil_Rights
/Law_and_Government/Legal/Family_Law
/Law_and_Government/Legal/Intellectual_Property
/Law_and_Government/Legal/Labor_and_Employment_Law
/Law_and_Government/Legal/Legal_Education
/Law_and_Government/Legal/Legal_Services
/Law_and_Government/Legal/Product_Liability
/Law_and_Government/Legal/Real_Estate_Law
/Law_and_Government/Military
/Law_and_Government/Military/Air_Force
/Law_and_Government/Military/Army
/Law_and_Government/Military/Marines
/Law_and_Government/Military/Navy
/Law_and_Government/Military/Veterans
/Law_and_Government/Public_Safety
/Law_and_Government/Public_Safety/Crime_and_Justice
/Law_and_Government/Public_Safety/Emergency_Services
/Law_and_Government/Public_Safety/Law_Enforcement
/Law_and_Government/Public_Safety/Security_Products_and_Services
/Law_and_Government/Social_Services
/Law_and_Government/Social_Services/Welfare_and_Unemployment
/News/Business_News
/News/Business_News/Company_News
/News/Business_News/Economy_News
/News/Business_News/Financial_Markets_News
/News/Business_News/Fiscal_Policy_News
/News/Gossip_and_Tabloid_News
/News/Gossip_and_Tabloid_News/Scandals_and_Investigations
/News/Health_News
/News/Local_News
/News/Politics
/News/Politics/Campaigns_and_Elections
/News/Politics/Media_Critics_and_Watchdogs
/News/Politics/Political_Polls_and_Surveys
/News/Sports_News
/News/Technology_News
/News/Weather
/News/World_News
/Online_Communities/Blogging_Resources_and_Services
/Online_Communities/Dating_and_Personals
/Online_Communities/Dating_and_Personals/Matrimonial_Services
/Online_Communities/Dating_and_Personals/Personals
/Online_Communities/Dating_and_Personals/Photo_Rating_Sites
/Online_Communities/File_Sharing_and_Hosting
/Online_Communities/Online_Goodies
/Online_Communities/Online_Goodies/Clip_Art_and_Animated_GIFs
/Online_Communities/Online_Goodies/Skins,_Themes_and_Wallpapers
/Online_Communities/Online_Goodies/Social_Network_Apps_and_Add-Ons
/Online_Communities/Online_Journals_and_Personal_Sites
/Online_Communities/Photo_and_Video_Sharing
/Online_Communities/Photo_and_Video_Sharing/Photo_and_Image_Sharing
/Online_Communities/Photo_and_Video_Sharing/Video_Sharing
/Online_Communities/Social_Networks
/Online_Communities/Virtual_Worlds
/People_and_Society/Family_and_Relationships
/People_and_Society/Family_and_Relationships/Etiquette
/People_and_Society/Family_and_Relationships/Family
/People_and_Society/Family_and_Relationships/Family/Parenting
/People_and_Society/Family_and_Relationships/Family/Parenting/Babies_and_Toddlers
/People_and_Society/Family_and_Relationships/Family/Parenting/Babies_and_Toddlers/Nursery_and_Playroom
/People_and_Society/Family_and_Relationships/Marriage
/People_and_Society/Family_and_Relationships/Romance
/People_and_Society/Family_and_Relationships/Troubled_Relationships
/People_and_Society/Kids_and_Teens
/People_and_Society/Kids_and_Teens/Children's_Interests
/People_and_Society/Kids_and_Teens/Teen_Interests
/People_and_Society/Religion_and_Belief
/People_and_Society/Self-Help_and_Motivational
/People_and_Society/Seniors_and_Retirement
/People_and_Society/Social_Issues_and_Advocacy
/People_and_Society/Social_Issues_and_Advocacy/Charity_and_Philanthropy
/People_and_Society/Social_Issues_and_Advocacy/Discrimination_and_Identity_Relations
/People_and_Society/Social_Issues_and_Advocacy/Drug_Laws_and_Policy
/People_and_Society/Social_Issues_and_Advocacy/Ethics
/People_and_Society/Social_Issues_and_Advocacy/Green_Living_and_Environmental_Issues
/People_and_Society/Social_Issues_and_Advocacy/Housing_and_Development
/People_and_Society/Social_Issues_and_Advocacy/Human_Rights_and_Liberties
/People_and_Society/Social_Issues_and_Advocacy/Poverty_and_Hunger
/People_and_Society/Social_Issues_and_Advocacy/Work_and_Labor_Issues
/People_and_Society/Social_Sciences
/People_and_Society/Social_Sciences/Anthropology
/People_and_Society/Social_Sciences/Archaeology
/People_and_Society/Social_Sciences/Communications_and_Media_Studies
/People_and_Society/Social_Sciences/Demographics
/People_and_Society/Social_Sciences/Economics
/People_and_Society/Social_Sciences/Political_Science
/People_and_Society/Social_Sciences/Psychology
/People_and_Society/Subcultures_and_Niche_Interests
/Pets_and_Animals/Animal_Products_and_Services
/Pets_and_Animals/Animal_Products_and_Services/Animal_Welfare
/Pets_and_Animals/Animal_Products_and_Services/Pet_Food_and_Pet_Care_Supplies
/Pets_and_Animals/Animal_Products_and_Services/Veterinarians
/Pets_and_Animals/Pets
/Pets_and_Animals/Pets/Birds
/Pets_and_Animals/Pets/Cats
/Pets_and_Animals/Pets/Dogs
/Pets_and_Animals/Pets/Exotic_Pets
/Pets_and_Animals/Pets/Fish_and_Aquaria
/Pets_and_Animals/Pets/Horses
/Pets_and_Animals/Pets/Rabbits_and_Rodents
/Pets_and_Animals/Pets/Reptiles_and_Amphibians
/Pets_and_Animals/Wildlife
/Real_Estate/Property_Development
/Real_Estate/Real_Estate_Listings
/Real_Estate/Real_Estate_Listings/Bank-Owned_and_Foreclosed_Properties
/Real_Estate/Real_Estate_Listings/Commercial_Properties
/Real_Estate/Real_Estate_Listings/Lots_and_Land
/Real_Estate/Real_Estate_Listings/Residential_Rentals
/Real_Estate/Real_Estate_Listings/Residential_Sales
/Real_Estate/Real_Estate_Listings/Timeshares_and_Vacation_Properties
/Real_Estate/Real_Estate_Services
/Real_Estate/Real_Estate_Services/Property_Inspections_and_Appraisals
/Real_Estate/Real_Estate_Services/Property_Management
/Real_Estate/Real_Estate_Services/Real_Estate_Agencies
/Real_Estate/Real_Estate_Services/Real_Estate_Title_and_Escrow
/Reference/Directories_and_Listings
/Reference/Directories_and_Listings/Business_and_Personal_Listings
/Reference/General_Reference
/Reference/General_Reference/Biographies_and_Quotations
/Reference/General_Reference/Calculators_and_Reference_Tools
/Reference/General_Reference/Dictionaries_and_Encyclopedias
/Reference/General_Reference/Educational_Resources
/Reference/General_Reference/Forms_Guides_and_Templates
/Reference/General_Reference/How-To,_DIY_and_Expert_Content
/Reference/General_Reference/Public_Records
/Reference/General_Reference/Time_and_Calendars
/Reference/Geographic_Reference
/Reference/Geographic_Reference/Maps
/Reference/Humanities
/Reference/Humanities/History
/Reference/Humanities/Myth_and_Folklore
/Reference/Humanities/Philosophy
/Reference/Language_Resources
/Reference/Language_Resources/Foreign_Language_Resources
/Reference/Libraries_and_Museums
/Reference/Libraries_and_Museums/Libraries
/Reference/Libraries_and_Museums/Museums
/Reference/Technical_Reference
/Science/Astronomy
/Science/Biological_Sciences
/Science/Biological_Sciences/Genetics
/Science/Biological_Sciences/Neuroscience
/Science/Chemistry
/Science/Computer_Science
/Science/Computer_Science/Machine_Learning_and_Artificial_Intelligence
/Science/Earth_Sciences
/Science/Earth_Sciences/Atmospheric_Science
/Science/Earth_Sciences/Geology
/Science/Earth_Sciences/Paleontology
/Science/Ecology_and_Environment
/Science/Ecology_and_Environment/Climate_Change_and_Global_Warming
/Science/Engineering_and_Technology
/Science/Engineering_and_Technology/Augmented_and_Virtual_Reality
/Science/Engineering_and_Technology/Robotics
/Science/Mathematics
/Science/Mathematics/Statistics
/Science/Physics
/Science/Scientific_Equipment
/Science/Scientific_Institutions
/Sensitive_Subjects/Accidents_and_Disasters
/Sensitive_Subjects/Death_and_Tragedy
/Sensitive_Subjects/Firearms_and_Weapons
/Sensitive_Subjects/Recreational_Drugs
/Sensitive_Subjects/Self-Harm
/Sensitive_Subjects/Violence_and_Abuse
/Sensitive_Subjects/War_and_Conflict
/Shopping/Antiques_and_Collectibles
/Shopping/Apparel
/Shopping/Apparel/Apparel_Services
/Shopping/Apparel/Athletic_Apparel
/Shopping/Apparel/Casual_Apparel
/Shopping/Apparel/Children's_Clothing
/Shopping/Apparel/Clothing_Accessories
/Shopping/Apparel/Costumes
/Shopping/Apparel/Eyewear
/Shopping/Apparel/Footwear
/Shopping/Apparel/Formal_Wear
/Shopping/Apparel/Headwear
/Shopping/Apparel/Men's_Clothing
/Shopping/Apparel/Outerwear
/Shopping/Apparel/Pants_and_Shorts
/Shopping/Apparel/Shirts_and_Tops
/Shopping/Apparel/Sleepwear
/Shopping/Apparel/Suits_and_Business_Attire
/Shopping/Apparel/Swimwear
/Shopping/Apparel/Undergarments
/Shopping/Apparel/Uniforms_and_Workwear
/Shopping/Apparel/Women's_Clothing
/Shopping/Auctions
/Shopping/Classifieds
/Shopping/Consumer_Resources
/Shopping/Consumer_Resources/Consumer_Advocacy_and_Protection
/Shopping/Consumer_Resources/Coupons_and_Discount_Offers
/Shopping/Consumer_Resources/Customer_Services
/Shopping/Consumer_Resources/Identity_Theft_Protection
/Shopping/Consumer_Resources/Product_Reviews_and_Price_Comparisons
/Shopping/Discount_and_Outlet_Stores
/Shopping/Entertainment_Media
/Shopping/Entertainment_Media/Entertainment_Media_Rentals
/Shopping/Gifts_and_Special_Event_Items
/Shopping/Gifts_and_Special_Event_Items/Custom_and_Personalized_Items
/Shopping/Gifts_and_Special_Event_Items/Flowers
/Shopping/Gifts_and_Special_Event_Items/Gifts
/Shopping/Gifts_and_Special_Event_Items/Greeting_Cards
/Shopping/Gifts_and_Special_Event_Items/Party_and_Holiday_Supplies
/Shopping/Green_and_Eco-Friendly_Shopping
/Shopping/Luxury_Goods
/Shopping/Mass_Merchants_and_Department_Stores
/Shopping/Photo_and_Video_Services
/Shopping/Photo_and_Video_Services/Event_and_Studio_Photography
/Shopping/Photo_and_Video_Services/Photo_Printing_Services
/Shopping/Photo_and_Video_Services/Stock_Photography
/Shopping/Shopping_Portals
/Shopping/Swap_Meets_and_Outdoor_Markets
/Shopping/Tobacco_and_Vaping_Products
/Shopping/Toys
/Shopping/Toys/Action_Figures
/Shopping/Toys/Building_Toys
/Shopping/Toys/Die-cast_and_Toy_Vehicles
/Shopping/Toys/Dolls_and_Accessories
/Shopping/Toys/Educational_Toys
/Shopping/Toys/Outdoor_Toys_and_Play_Equipment
/Shopping/Toys/Puppets
/Shopping/Toys/Ride-On_Toys_and_Wagons
/Shopping/Toys/Stuffed_Toys
/Shopping/Wholesalers_and_Liquidators
/Sports/Animal_Sports
/Sports/Animal_Sports/Equestrian
/Sports/College_Sports
/Sports/Combat_Sports
/Sports/Combat_Sports/Boxing
/Sports/Combat_Sports/Fencing
/Sports/Combat_Sports/Martial_Arts
/Sports/Combat_Sports/Wrestling
/Sports/Extreme_Sports
/Sports/Extreme_Sports/Climbing_and_Mountaineering
/Sports/Extreme_Sports/Drag_and_Street_Racing
/Sports/Extreme_Sports/Stunts_and_Dangerous_Feats
/Sports/Fantasy_Sports
/Sports/Individual_Sports
/Sports/Individual_Sports/Bowling
/Sports/Individual_Sports/Cycling
/Sports/Individual_Sports/Golf
/Sports/Individual_Sports/Gymnastics
/Sports/Individual_Sports/Racquet_Sports
/Sports/Individual_Sports/Running_and_Walking
/Sports/Individual_Sports/Skate_Sports
/Sports/Individual_Sports/Track_and_Field
/Sports/International_Sports_Competitions
/Sports/International_Sports_Competitions/Olympics
/Sports/Motor_Sports
/Sports/Motor_Sports/Auto_Racing
/Sports/Motor_Sports/Motorcycle_Racing
/Sports/Sport_Scores_and_Statistics
/Sports/Sporting_Goods
/Sports/Sporting_Goods/American_Football_Equipment
/Sports/Sporting_Goods/Baseball_Equipment
/Sports/Sporting_Goods/Basketball_Equipment
/Sports/Sporting_Goods/Bowling_Equipment
/Sports/Sporting_Goods/Combat_Sports_Equipment
/Sports/Sporting_Goods/Cricket_Equipment
/Sports/Sporting_Goods/Electric_Skateboards_and_Scooters
/Sports/Sporting_Goods/Equestrian_Equipment_and_Tack
/Sports/Sporting_Goods/Golf_Equipment
/Sports/Sporting_Goods/Gymnastics_Equipment
/Sports/Sporting_Goods/Hockey_Equipment
/Sports/Sporting_Goods/Ice_Skating_Equipment
/Sports/Sporting_Goods/Roller_Skating_and_Rollerblading_Equipment
/Sports/Sporting_Goods/Skateboarding_Equipment
/Sports/Sporting_Goods/Soccer_Equipment
/Sports/Sporting_Goods/Sports_Memorabilia
/Sports/Sporting_Goods/Squash_and_Racquetball_Equipment
/Sports/Sporting_Goods/Table_Tennis_Equipment
/Sports/Sporting_Goods/Tennis_Equipment
/Sports/Sporting_Goods/Volleyball_Equipment
/Sports/Sporting_Goods/Water_Sports_Equipment
/Sports/Sporting_Goods/Winter_Sports_Equipment
/Sports/Sports_Coaching_and_Training
/Sports/Sports_Fan_Gear_and_Apparel
/Sports/Team_Sports
/Sports/Team_Sports/American_Football
/Sports/Team_Sports/Australian_Football
/Sports/Team_Sports/Baseball
/Sports/Team_Sports/Basketball
/Sports/Team_Sports/Cheerleading
/Sports/Team_Sports/Cricket
/Sports/Team_Sports/Handball
/Sports/Team_Sports/Hockey
/Sports/Team_Sports/Rugby
/Sports/Team_Sports/Soccer
/Sports/Team_Sports/Volleyball
/Sports/Water_Sports
/Sports/Water_Sports/Surfing
/Sports/Water_Sports/Swimming
/Sports/Winter_Sports
/Sports/Winter_Sports/Ice_Skating
/Sports/Winter_Sports/Skiing_and_Snowboarding
/Travel_and_Transportation/Hotels_and_Accommodations
/Travel_and_Transportation/Hotels_and_Accommodations/Vacation_Rentals_and_Short-Term_Stays
/Travel_and_Transportation/Luggage_and_Travel_Accessories
/Travel_and_Transportation/Luggage_and_Travel_Accessories/Backpacks_and_Utility_Bags
/Travel_and_Transportation/Specialty_Travel
/Travel_and_Transportation/Specialty_Travel/Adventure_Travel
/Travel_and_Transportation/Specialty_Travel/Agritourism
/Travel_and_Transportation/Specialty_Travel/Business_Travel
/Travel_and_Transportation/Specialty_Travel/Ecotourism
/Travel_and_Transportation/Specialty_Travel/Family_Travel
/Travel_and_Transportation/Specialty_Travel/Honeymoons_and_Romantic_Getaways
/Travel_and_Transportation/Specialty_Travel/Low_Cost_and_Last_Minute_Travel
/Travel_and_Transportation/Specialty_Travel/Luxury_Travel
/Travel_and_Transportation/Specialty_Travel/Medical_Tourism
/Travel_and_Transportation/Specialty_Travel/Religious_Travel
/Travel_and_Transportation/Tourist_Destinations
/Travel_and_Transportation/Tourist_Destinations/Beaches_and_Islands
/Travel_and_Transportation/Tourist_Destinations/Historical_Sites_and_Buildings
/Travel_and_Transportation/Tourist_Destinations/Mountain_and_Ski_Resorts
/Travel_and_Transportation/Tourist_Destinations/Regional_Parks_and_Gardens
/Travel_and_Transportation/Tourist_Destinations/Theme_Parks
/Travel_and_Transportation/Tourist_Destinations/Vineyards_and_Wine_Tourism
/Travel_and_Transportation/Tourist_Destinations/Zoos,_Aquariums_and_Preserves
/Travel_and_Transportation/Transportation
/Travel_and_Transportation/Transportation/Air_Travel
/Travel_and_Transportation/Transportation/Car_Rentals
/Travel_and_Transportation/Transportation/Carpooling
/Travel_and_Transportation/Transportation/Chartered_Transportation_Rentals
/Travel_and_Transportation/Transportation/Cruises_and_Charters
/Travel_and_Transportation/Transportation/Long_Distance_Bus_and_Rail
/Travel_and_Transportation/Transportation/Parking
/Travel_and_Transportation/Transportation/Parking/Airport_Parking_and_Transportation
/Travel_and_Transportation/Transportation/Scooter_and_Bike_Rentals
/Travel_and_Transportation/Transportation/Taxi_and_Ride_Hail_Services
/Travel_and_Transportation/Transportation/Traffic_and_Route_Planners
/Travel_and_Transportation/Transportation/Urban_Transit
/Travel_and_Transportation/Travel_Agencies_and_Services
/Travel_and_Transportation/Travel_Agencies_and_Services/Guided_Tours_and_Escorted_Vacations
/Travel_and_Transportation/Travel_Agencies_and_Services/Sightseeing_Tours
/Travel_and_Transportation/Travel_Agencies_and_Services/Vacation_Offers
/Travel_and_Transportation/Travel_Guides_and_Travelogues
```

</details>

</details>

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `/v1/rules` | 60 req/min per tap |
| `/v1/stream` | 5 connections/min per tap |

## Error Codes

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid token (management key or tap token) |
| 403 | Resource not owned by your organization |
| 404 | Not found |
| 422 | Validation error / rule limit reached |
| 429 | Rate limit exceeded |

## Examples

### Management Key (curl)

```bash
export FIREHOSE_MGMT_KEY=fhm_your_management_key

# List taps
curl -s -H "Authorization: Bearer $FIREHOSE_MGMT_KEY" https://api.firehose.com/v1/taps

# Create a tap (returns tap token — use it to manage rules)
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_MGMT_KEY" -H "Content-Type: application/json" -d '{"name": "Brand Mentions"}' https://api.firehose.com/v1/taps

# Revoke a tap
curl -s -X DELETE -H "Authorization: Bearer $FIREHOSE_MGMT_KEY" https://api.firehose.com/v1/taps/TAP_UUID
```

### Tap Token (curl)

All examples use `$FIREHOSE_TAP_TOKEN` — set it with `export FIREHOSE_TAP_TOKEN=fh_your_tap_token`.

```bash
# List rules
curl -s -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/rules

# Create a simple rule
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" -H "Content-Type: application/json" -d '{"value": "ahrefs", "tag": "brand"}' https://api.firehose.com/v1/rules

# Create a rule with field-specific query
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" -H "Content-Type: application/json" -d '{"value": "title:tesla AND page_category:\"/News\"", "tag": "market-news"}' https://api.firehose.com/v1/rules

# Get a single rule
curl -s -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/rules/1

# Update a rule
curl -s -X PUT -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" -H "Content-Type: application/json" -d '{"tag": "new-tag"}' https://api.firehose.com/v1/rules/1

# Create a rule with recency filter and quality disabled
curl -s -X POST -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" -H "Content-Type: application/json" \
  -d '{"value": "title:tesla AND recent:24h", "tag": "market-raw", "quality": false}' \
  https://api.firehose.com/v1/rules

# Delete a rule
curl -s -X DELETE -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/rules/1

# Stream matching pages (keep connection open)
curl -N -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" https://api.firehose.com/v1/stream

# Stream with timeout
curl -N -H "Authorization: Bearer $FIREHOSE_TAP_TOKEN" 'https://api.firehose.com/v1/stream?timeout=60'
```

### JavaScript (Node.js / browser with eventsource polyfill)

```javascript
// Note: native EventSource does not support custom headers.
// Use the 'eventsource' npm package or fetch-based SSE for auth support.
const EventSource = require("eventsource"); // npm install eventsource

const es = new EventSource("https://api.firehose.com/v1/stream", {
  headers: { Authorization: `Bearer ${process.env.FIREHOSE_TAP_TOKEN}` },
});

es.addEventListener("update", (event) => {
  const { query_id, matched_at, document } = JSON.parse(event.data);
  console.log(`[${matched_at}] Rule ${query_id}: ${document.url}`);
});

es.addEventListener("error", (event) => {
  console.error("Stream error:", event.data);
});
```

### Python

```python
import json, urllib.request

req = urllib.request.Request(
    "https://api.firehose.com/v1/stream",
    headers={"Authorization": f"Bearer {os.environ['FIREHOSE_TAP_TOKEN']}"},
)

with urllib.request.urlopen(req) as resp:
    for line in resp:
        line = line.decode().strip()
        if line.startswith("data: "):
            data = json.loads(line[6:])
            if "document" in data:
                print(f"Matched: {data['document']['url']}")
```

