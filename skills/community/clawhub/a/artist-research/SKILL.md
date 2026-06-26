# Artist Research — Skill for OpenClaw

Comprehensive artist analysis using Spotify API (Feb 2026 Development Mode limits) + web data sources. Generates professional reports with streaming data, market positioning, and monetization potential.

## When to Use

- User asks about an artist's performance, potential, or market position
- User requests music industry analysis or artist comparison
- User wants streaming data, chart history, or audience demographics
- User is evaluating signing, managing, or collaborating with an artist

## Prerequisites

- Spotify API credentials in `.env` (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
- `spotipy` and `python-dotenv` packages installed
- Internet access for web_fetch data sources

## Methodology

### Step 1: Spotify API Data Collection

Run `spotify_api_lookup.py` with artist name or ID. Collects:
- Artist metadata (name, images, URI, genres)
- Discography (albums, singles, track listings)
- Related artists (for market positioning)
- Search results for artist tracks

**NOTE:** Since Feb 2026, Development Mode does NOT return:
- followers, popularity (for artists)
- popularity (for tracks/albums)
- top-tracks endpoint (REMOVED)
- bulk fetch endpoints (REMOVED)

See `references/spotify-endpoints-2026.md` for full list.

### Step 2: External Data Sources (web_fetch)

| Source | URL Pattern | Data Available | Reliability |
|--------|-------------|----------------|-------------|
| **kworb.net** | `kworb.net/spotify/artist/{ID}.html` | Chart history, total streams, peak positions, per-track streams | ⭐⭐⭐⭐⭐ Best source |
| **kworb.net** | `kworb.net/spotify/track/{ID}.html` | Individual track daily streams | ⭐⭐⭐⭐⭐ |
| **Spotify Profile** | `open.spotify.com/artist/{ID}` | Monthly listeners (visible in browser), verification status | ⭐⭐⭐⭐ (requires browser for ML) |
| **Google** | Google search artist name + "monthly listeners" | AI overview with context | ⭐⭐⭐ |
| **Instagram** | `instagram.com/{handle}` | Follower count, engagement | ⭐⭐⭐ (requires browser) |

**Sources that DON'T work with web_fetch (JS-heavy):**
- songstats.com (returns empty)
- chosic.com (404)
- chartmasters.org (404/broken)
- tunemunk.com (no useful data)

### Step 3: Data Synthesis

Combine all sources into a structured report:

```
## ARTIST ANALYSIS: [Name]

### PROFILE
- Spotify ID, verified status, profile completeness
- Monthly listeners (from web/browser)
- Followers (not available via API since Feb 2026)

### DISCOGRAPHY
- Albums/singles count, release timeline
- Featured appearances and collaborations
- Label/distribution info

### STREAMING PERFORMANCE (from kworb.net)
- Total tracked streams
- Top tracks by streams
- Chart peaks (country-specific)
- Average streams per release

### MARKET POSITION
- Related artists comparison
- Genre positioning
- Audience tier classification

### MONETIZATION ANALYSIS
- Estimated monthly streaming revenue
- Concert potential (based on ML tier)
- Sync licensing opportunities
- Merch potential

### RECOMMENDATIONS
- Specific growth opportunities
- Release strategy suggestions
- Collaboration targets
```

### Step 4: Report Output

Save report as:
- `reports/artist-report-{name}-{date}.md` for storage
- Present summary in chat with key metrics

## Scripts

All scripts are in this skill directory. Usage:

```bash
# Step 1: Spotify API data
python spotify_api_lookup.py "Artist Name"
python spotify_api_lookup.py --id SPOTIFY_ID

# Step 2: kworb.net data (automated via web_fetch in main flow)

# Step 3: Full report (combines all sources)
python generate_report.py "Artist Name"
```

## Data Tiers — Artist Classification

| Tier | Monthly Listeners | Revenue Potential | Examples |
|------|-------------------|-------------------|----------|
| Underground | 0-5K | 200-1K PLN/mo | local acts |
| Emerging | 5-20K | 1-4K PLN/mo | first buzz |
| Developing | 20-60K | 4-12K PLN/mo | growing fanbase |
| **Established Indie** | **60-200K** | **12-40K PLN/mo** | **Michał Anioł, schafter** |
| Top Indie | 200-500K | 40-100K PLN/mo | Quebonafide tier |
| Mainstream | 500K-2M | 100-400K PLN/mo | Dawid Podsiadło |
| Star | 2M-10M | 400K-2M PLN/mo | sanah, PRO8L3M |
| Mega-star | 10M+ | 2M+ PLN/mo | global acts |

## Revenue Estimation Formula

```
Monthly streaming revenue = Monthly Streams × $0.003-0.005 (per stream)
Concert revenue = (Capacity × Ticket Price × 0.7) per show
Sync licensing = 5K-50K PLN per placement (one-time)
```

## Spotify API — Available vs Removed (Feb 2026)

### ✅ Available Endpoints
- GET /artists/{id} — Artist metadata (limited fields)
- GET /artists/{id}/albums — Artist's albums
- GET /albums/{id} — Album details
- GET /albums/{id}/tracks — Album tracks
- GET /tracks/{id} — Track details
- GET /search — Search (max 10 results)
- GET /me/player/currently-playing — Now playing
- GET /me/player/recently-played — Recent tracks
- GET /me/top/{type} — User's top artists/tracks
- GET /me — Current user profile
- GET /me/playlists — User's playlists
- POST /me/playlists — Create playlist
- PUT/DELETE /me/library — Save/remove items
- Full player control endpoints

### ❌ Removed/Restricted Endpoints
- GET /artists/{id}/top-tracks — REMOVED
- GET /artists (bulk) — REMOVED
- GET /tracks (bulk) — REMOVED
- GET /albums (bulk) — REMOVED
- GET /users/{id} — REMOVED
- GET /users/{id}/playlists — REMOVED
- GET /browse/new-releases — REMOVED
- GET /browse/categories — REMOVED
- GET /markets — REMOVED

### ⚠️ Removed Fields
- Artist: followers, popularity
- Track: popularity, available_markets, linked_from
- Album: popularity, label, available_markets, album_group
- User: country, email, followers, product, explicit_content

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 403 on /top-tracks | Endpoint removed Feb 2026 | Use kworb.net |
| 404 on artist ID | Invalid ID or regional restriction | Check ID, try search |
| Missing followers/popularity | Dev Mode restriction | Use kworb.net or SfA |
| Encoding error (cp1250) | Polish characters in output | Replace emojis with [OK]/[!] |
| web_search 404 | Token limit exceeded | Use web_fetch instead |

## Notes

- Always cross-reference data from multiple sources
- kworb.net is the most reliable source for streaming numbers
- Spotify for Artists (SfA) dashboard has the richest data but requires manual access
- web_search is currently unavailable (token limit) — use web_fetch on known URLs
- Polish artist names may cause encoding issues — use ASCII-safe output

## Version History

- v1.0 (2026-03-16) — Initial skill creation, post-Spotify Feb 2026 changes
