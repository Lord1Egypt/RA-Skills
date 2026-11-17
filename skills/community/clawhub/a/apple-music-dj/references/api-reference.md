# Apple Music API Reference

Base URL: `https://api.music.apple.com`

**All requests** require `Authorization: Bearer <DEV_TOKEN>`.
**Personalized** endpoints (`/v1/me/...`) also require `Music-User-Token: <USER_TOKEN>`.

---

## Personalized Endpoints

### Recently Played Tracks
```
GET /v1/me/recent/played/tracks?types=songs&limit=10&offset=0
```
Max 10 per request. Paginate: offset 0, 10, 20, 30, 40. Max 50 total.
Returns deduplicated (repeat listens collapsed).

### Recently Played Resources
```
GET /v1/me/recent/played?limit=10
```
Returns albums, playlists, stations (not individual tracks).

### Heavy Rotation
```
GET /v1/me/history/heavy-rotation?limit=10
```
Albums and playlists on heavy repeat. May be empty for new users.

### Ratings
```
GET /v1/me/ratings/songs?limit=100
GET /v1/me/ratings/albums?limit=100
```
Returns items with `value`: 1 (loved) or -1 (disliked).

### Library Artists
```
GET /v1/me/library/artists?limit=25&offset=0
```

### Library Songs
```
GET /v1/me/library/songs?limit=100&offset=0&include=catalog
```
Use `include=catalog` to get catalog IDs alongside library IDs.

### Recommendations
```
GET /v1/me/recommendations?limit=10
```
Returns recommendation groups containing albums, playlists, stations.

### Replay / Music Summaries
```
GET /v1/me/music-summaries
GET /v1/me/music-summaries?filter[year]=2025
GET /v1/me/music-summaries/milestones
GET /v1/me/music-summaries/milestones?filter[year]=2025
```
Annual listening stats: top artists, albums, songs, listen time, milestones.
Not available for all users/regions.

### User Storefront
```
GET /v1/me/storefront
```
Returns the user's storefront (country code). Use to auto-detect locale.

### Create Playlist
```
POST /v1/me/library/playlists
Content-Type: application/json
```
```json
{
  "attributes": {
    "name": "Playlist Name",
    "description": "Optional description"
  },
  "relationships": {
    "tracks": {
      "data": [
        {"id": "CATALOG_SONG_ID", "type": "songs"}
      ]
    }
  }
}
```
Use **catalog** song IDs (not library IDs). Returns 201.

### Add Tracks to Playlist
```
POST /v1/me/library/playlists/{id}/tracks
Content-Type: application/json
```
```json
{"data": [{"id": "CATALOG_SONG_ID", "type": "songs"}]}
```

### Get Playlist Tracks
```
GET /v1/me/library/playlists/{id}/tracks?limit=100
```

### Recently Added
```
GET /v1/me/library/recently-added?limit=25
```
Albums and playlists recently added to the library. Albums carry `artistName` and
`genreNames`; playlists don't, so the profiler skips them. Used as a "what I'm into now" signal.

### Recent Radio Stations
```
GET /v1/me/recent/radio-stations?limit=10
```
Station resources have no genre attribute, so the profiler only picks up genres that appear
in the station *title* (e.g. "Alternative Radio") and treats them as a very light signal.

### Add Albums / Songs to Library
```
POST /v1/me/library?ids[albums]=ID1,ID2      (or ids[songs]=...)
```
No request body; answers `202` with an empty body (not JSON — call `call_api(..., raw=True)`).
Wrapper: `apple_music_api.sh add-to-library <albums|songs> <ids> --yes`. **Writes to the account** (previews and exits 3 without `--yes`).

### Add to Favorites
```
POST /v1/me/favorites?ids[songs]=ID1,ID2     (also albums, artists, playlists)
```
Empty-body response. Wrapper: `apple_music_api.sh favorite <type> <ids> --yes`. **Writes to the account** (needs `--yes`).
Apple documents only this write endpoint — there is no documented way to *read* favorites,
so the profiler keeps using ratings (loved/disliked) as its explicit-preference signal.

### Rate a Song
```
PUT    /v1/me/ratings/songs/{id}     body: {"type":"rating","attributes":{"value":1}}   (1 = love, -1 = dislike)
DELETE /v1/me/ratings/songs/{id}
```
Wrappers: `apple_music_api.sh rate <id> <1|-1> --yes` and `unrate <id> --yes`. **Writes to the account** (need `--yes`).

---

## Catalog Endpoints

### Search
```
GET /v1/catalog/{storefront}/search?term=query&types=songs,artists,albums&limit=25
```

### Charts
```
GET /v1/catalog/{storefront}/charts?types=songs,albums&limit=25&genre=GENRE_ID
```
Supports `with=dailyGlobalTopCharts,cityCharts` for chart playlists.

### Artist Albums
```
GET /v1/catalog/{storefront}/artists/{id}/albums?limit=25
```

### Artist Top Songs
```
GET /v1/catalog/{storefront}/artists/{id}?views=top-songs
```

### Song Details
```
GET /v1/catalog/{storefront}/songs/{id}?include=artists,albums
```

### Genres
```
GET /v1/catalog/{storefront}/genres?limit=40
```

### Similar Artists
```
GET /v1/catalog/{storefront}/artists/{id}/view/similar-artists?limit=20
```
Wrapper: `apple_music_api.sh similar-artists <storefront> <artist_id>`.

### Songs by ISRC
```
GET /v1/catalog/{storefront}/songs?filter[isrc]=ISRC1,ISRC2
```
Max 25 ISRCs per request. Each song's `attributes.isrc` identifies which input it matched; one ISRC
can return several catalog songs (different albums), so importers take the first.
Wrapper: `apple_music_api.sh songs-by-isrc <storefront> <isrcs>`.

---

## Common Genre IDs (US)

| Genre | ID | Genre | ID |
|---|---|---|---|
| Alternative | 20 | Jazz | 11 |
| Classical | 5 | Metal | 1153 |
| Country | 6 | Pop | 14 |
| Dance | 17 | R&B/Soul | 15 |
| Electronic | 7 | Rock | 21 |
| Hip-Hop/Rap | 18 | Indie | 50 |

Genre IDs vary by storefront. Fetch dynamically via the genres endpoint.

## Pagination

Most endpoints support `limit` and `offset`. Check for `next` in response.

## Rate Limits

Undocumented. ~20 req/s is safe. Exponential backoff on 429.
