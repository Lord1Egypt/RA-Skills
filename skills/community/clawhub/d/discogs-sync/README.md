# Discogs Sync

CLI tool to synchronize wantlists and collections with Discogs, and search marketplace pricing.

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Setup

### 1. Generate a Personal Access Token

1. Go to https://www.discogs.com/settings/developers
2. Click "Generate new token"

### 2. Authenticate

Either set the token in the environment (takes precedence):

```bash
export DISCOGS_USER_TOKEN=your-token
```

or store it once:

```bash
discogs-sync auth
```

`auth` prompts for the token (input hidden), validates it, and stores it in `~/.discogs-sync/config.json` with owner-only permissions.

### 3. Verify

```bash
discogs-sync whoami
```

## Input File Formats

### CSV

Header row required. Columns: `artist` (required), `album` (required), `format`, `year`, `notes`.

```csv
artist,album,format,year,notes
Radiohead,OK Computer,Vinyl,,Must have
Miles Davis,Kind of Blue,,1959,Original pressing
Nirvana,Nevermind,CD,1991,
```

### JSON

Array of objects with the same fields:

```json
[
    {"artist": "Radiohead", "album": "OK Computer", "format": "Vinyl"},
    {"artist": "Miles Davis", "album": "Kind of Blue", "year": 1959}
]
```

### Format Normalization

The following synonyms are automatically normalized:
- `LP`, `record`, `12"`, `12 inch` → **Vinyl**
- `compact disc` → **CD**
- `tape`, `mc` → **Cassette**

## Commands

### Authentication

```bash
discogs-sync auth                          # Store a personal access token
discogs-sync whoami [--output-format json] # Show authenticated user
```

### Wantlist

```bash
# Batch sync from file
discogs-sync wantlist sync <file> [--remove-extras] [--yes] [--dry-run] [--threshold 0.7] [--output-format json]

# Add individual items
discogs-sync wantlist add --artist "Radiohead" --album "OK Computer" [--format Vinyl]
discogs-sync wantlist add --master-id 3425
discogs-sync wantlist add --release-id 7890

# Remove items
discogs-sync wantlist remove --artist "Radiohead" --album "OK Computer" [--yes]
discogs-sync wantlist remove --release-id 7890 [--yes]

# List current wantlist
discogs-sync wantlist list [--search "radiohead"] [--no-cache] [--output-format json]
```

### Collection

```bash
# Batch sync from file
discogs-sync collection sync <file> [--folder-id 1] [--remove-extras] [--yes] [--dry-run] [--threshold 0.7] [--output-format json]

# Add individual items
discogs-sync collection add --artist "Radiohead" --album "OK Computer" [--format Vinyl] [--allow-duplicate]
discogs-sync collection add --master-id 3425 [--folder-id 1]
discogs-sync collection add --release-id 7890 [--folder-id 1]

# Remove items
discogs-sync collection remove --artist "Radiohead" --album "OK Computer" [--yes]
discogs-sync collection remove --release-id 7890 [--yes]

# List collection
discogs-sync collection list [--folder-id 0] [--search "miles"] [--no-cache] [--output-format json]
```

### Marketplace

```bash
# Search by artist/album
discogs-sync marketplace search --artist "Radiohead" --album "OK Computer" [--format Vinyl] [--country US] [--min-price 10] [--max-price 50] [--currency USD] [--output-format json]

# Search by master ID
discogs-sync marketplace search --master-id 3425 [--format Vinyl] [--country US]

# Search by specific release ID (skips master version scan)
discogs-sync marketplace search --release-id 7890

# Batch search from file
discogs-sync marketplace search <file> [--format Vinyl] [--country US] [--min-price N] [--max-price N] [--currency USD] [--max-versions 25] [--output-format json]

# Show detailed progress / condition grade prices
discogs-sync marketplace search --artist "Radiohead" --album "OK Computer" --verbose --details
```

## Options

### Global Options

| Option | Description |
|--------|-------------|
| `--output-format` | `table` (default) or `json` for machine-readable output |
| `--threshold` | Match score threshold 0.0-1.0 (default: 0.7) |
| `--dry-run` | Show what would be done without making changes |

### Wantlist/Collection Options

| Option | Description |
|--------|-------------|
| `--remove-extras` | Remove items not in the input file (requires `--dry-run` or `--yes`; aborts if any input record fails to resolve) |
| `--yes` | Confirm a removal (`remove` or `sync --remove-extras`); without it the command only previews the target, exits 2, and changes nothing |
| `--folder-id` | Collection folder ID (default: 1 for adds, 0 for reads) |
| `--allow-duplicate` | Allow adding duplicate copies to collection |
| `--search` | Client-side filter for `list` commands (case-insensitive substring match on artist, title, year) |
| `--no-cache` | Bypass cache and fetch fresh data from Discogs (`list` commands only; cache is still updated) |

### Marketplace Options

| Option | Description |
|--------|-------------|
| `--format` | Filter versions by format (Vinyl, CD) |
| `--country` | Filter by country of pressing (exact match: US, UK, Germany, etc.) |
| `--release-id` | Fetch stats for a specific release (bypasses master version scan) |
| `--min-price` | Minimum price filter |
| `--max-price` | Maximum price filter |
| `--currency` | Currency code (default: USD) |
| `--max-versions` | Max versions to check per master (default: 25) |
| `--details` | Include suggested prices by condition grade |
| `--no-cache` | Bypass cache; fresh results are still written back to cache |
| `--verbose` | Show detailed progress and API call logging |

## Caching

`wantlist list`, `collection list`, and `marketplace search` (single-item) cache fetched results locally for **24 hours** (default) to avoid redundant API calls. The TTL is configurable via `cache_ttl_hours` in `~/.discogs-sync/config.json`.

### Wantlist / Collection

- Cache files are stored in `~/.discogs-sync/` as `wantlist_cache.json` and `collection_cache.json`.
- The collection cache only applies when `--folder-id` is the default (`0` / All). Non-default folder IDs always fetch live.
- Any `add`, `remove`, or `sync` command automatically invalidates the relevant cache.

### Marketplace

- Results are cached using MD5-hashed keys based on the lookup parameters (artist, album, format, country, currency, etc.).
- `--details` (condition grade price suggestions) is handled via a separate **details cache** entry: when `--details` is requested and only the base cache is warm, the tool fetches just the price-suggestion data and writes a details cache entry — no full re-search needed.
- Batch mode (`marketplace search <file>`) never reads or writes the cache.

### General

- Pass `--no-cache` to force a fresh fetch. The result is still written to cache so the next call benefits.
- To change the cache TTL, add `"cache_ttl_hours": <number>` to `~/.discogs-sync/config.json` (e.g. `0.5` for 30 minutes, `48` for 2 days). Defaults to `24`.

## Release Matching

The tool uses a multi-pass search to match input records to Discogs releases:

1. **Structured search**: Uses artist, album, format, and year
2. **Relaxed search**: Drops format and year constraints
3. **Free text search**: Searches `"artist album"` as plain text

Each result is scored (0.0-1.0) based on:
- 40% artist name similarity
- 40% album title similarity
- 10% year match
- 10% format match

Results below the threshold (default 0.7) are rejected.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Partial failure (some items failed) |
| 2 | Complete failure |

## Running Tests

```bash
pytest
pytest --cov=discogs_sync
```
