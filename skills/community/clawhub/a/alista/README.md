# Alista - Restaurant Bookmark Skill

An OpenClaw skill that saves restaurants, bars, and cafes from TikTok and Instagram videos to a local database. Search your collection and get personalized weekend suggestions.

## Features

- **Agent-driven extraction**: Paste an Instagram or TikTok URL — the agent reasons about captions, tagged users, alt text, and images to identify places
- **Video frame analysis**: Extracts key frames from reels for visual identification when text data is insufficient
- **Google Places verification**: Automatically verifies places with addresses and coordinates
- **Local SQLite storage**: All data stays on your machine
- **Full-text search**: FTS5-powered search across your saved places
- **Smart suggestions**: Nudge algorithm considers freshness, urgency, and variety

## Setup

### 1. Install dependencies

Requires **Node.js 22+** and **tsx** (TypeScript executor).

```bash
npm install -g tsx
npm install
```

Optional: Install **ffmpeg** for video frame extraction (needed for reels where place info is only visible in the video).

```bash
# macOS
brew install ffmpeg

# Debian/Ubuntu
apt-get install ffmpeg
```

### 2. Set API keys

Export these environment variables:

```bash
# Required: Google Places (place verification)
export GOOGLE_PLACES_API_KEY="your-google-places-key"

# Required: Apify (Instagram/TikTok metadata fetching)
export APIFY_API_KEY="your-apify-key"
```

**Getting API keys:**
- **Google Places**: [Google Cloud Console](https://console.cloud.google.com/apis/library/places-backend.googleapis.com) — requires billing, but generous free tier
- **Apify**: [Apify Console](https://console.apify.com/) — free tier available, used to fetch post metadata from Instagram and TikTok

### 3. Verify setup
```bash
tsx scripts/lookup-place.ts --name "Eleven Madison Park" --city "New York"
```

## Usage

### Fetch post metadata (preferred)
```bash
tsx scripts/fetch-post.ts "https://www.instagram.com/reel/ABC123/"
tsx scripts/fetch-post.ts "https://www.instagram.com/reel/ABC123/" --download-images ./images
tsx scripts/fetch-post.ts "https://www.instagram.com/reel/ABC123/" --extract-frames ./frames
```

Returns raw metadata (caption, tagged users, alt text, images, video URL, transcript). The OpenClaw agent reasons about this data to identify places, then verifies and saves them.

### Save a place
```bash
tsx scripts/save-place.ts --name "Restaurant Name" --city "NYC" --category restaurant --verify
```

### Look up a place
```bash
tsx scripts/lookup-place.ts --name "Restaurant Name" --city "NYC"
```

### Search
```bash
tsx scripts/search-places.ts --query "sushi"
tsx scripts/search-places.ts --list --type bar
tsx scripts/search-places.ts --list
```

### Get suggestions
```bash
tsx scripts/nudge.ts --count 5
```

## Architecture

```
scripts/
├── fetch-post.ts           # Fetch raw post metadata from social media URLs
├── lookup-place.ts         # Verify a place via Google Places
├── save-place.ts           # Save a place to local database
├── search-places.ts        # Search saved places (FTS5)
├── nudge.ts                # Get weekend suggestions
└── lib/
    ├── types.ts            # Shared TypeScript interfaces
    ├── db.ts               # SQLite database layer
    ├── place-verifier.ts   # Google Places verification + fuzzy matching
    ├── metadata-fetcher.ts # Apify + OG tag fetching
    ├── nudge-scorer.ts     # Suggestion scoring algorithm
    └── utils/
        ├── index.ts
        ├── text.ts         # Name normalization, transliteration, token overlap
        ├── retry.ts        # Retry with backoff
        ├── circuit-breaker.ts  # Circuit breaker for API calls
        ├── html.ts         # OG tag & HTML parsing
        └── url-normalizer.ts   # URL normalization
```

## How Extraction Works

1. **`fetch-post.ts`** calls Apify to get raw post metadata (caption, tagged users, location tag, alt text, image URLs, video URL)
2. **The OpenClaw agent** reasons about the metadata to identify places:
   - Tagged users → often the featured places in listicle/carousel posts
   - Caption → place names, addresses, city mentions
   - Alt text → Instagram auto-descriptions with place names and neighborhoods
   - Location tag → verified in context (not blindly trusted)
3. **If text data is insufficient**, the agent uses `--download-images` or `--extract-frames` for visual analysis
4. **Each identified place** is verified via `lookup-place.ts` (Google Places API)
5. **Confirmed places** are saved via `save-place.ts`

## Tech Stack

- **Runtime**: Node.js (via tsx)
- **Database**: SQLite (via better-sqlite3) with FTS5
- **Places API**: Google Places (New) Text Search
- **Scraping**: Apify (Instagram/TikTok metadata)
- **Video**: ffmpeg (optional, for frame extraction)
