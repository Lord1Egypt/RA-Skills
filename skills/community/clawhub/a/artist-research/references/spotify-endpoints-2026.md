# Spotify Web API Endpoints — Post February 2026 Changes

Source: https://developer.spotify.com/documentation/web-api/references/changes/february-2026
Last updated: 2026-03-16

## ❌ REMOVED Endpoints

| Endpoint | Description | Workaround |
|----------|-------------|------------|
| `GET /artists/{id}/top-tracks` | Artist's top tracks by country | kworb.net, search |
| `GET /artists` | Several artists (bulk) | Individual `GET /artists/{id}` |
| `GET /tracks` | Several tracks (bulk) | Individual `GET /tracks/{id}` |
| `GET /albums` | Several albums (bulk) | Individual `GET /albums/{id}` |
| `GET /episodes` | Several episodes (bulk) | Individual `GET /episodes/{id}` |
| `GET /shows` | Several shows (bulk) | Individual `GET /shows/{id}` |
| `GET /audiobooks` | Several audiobooks (bulk) | Individual `GET /audiobooks/{id}` |
| `GET /chapters` | Several chapters (bulk) | Individual `GET /chapters/{id}` |
| `GET /browse/new-releases` | New album releases | None |
| `GET /browse/categories` | Browse categories | None |
| `GET /browse/categories/{id}` | Single category | None |
| `GET /markets` | Available markets | None |
| `GET /users/{id}` | User profile | `GET /me` (current user only) |
| `GET /users/{id}/playlists` | User's playlists | `GET /me/playlists` (current user) |
| `POST /users/{user_id}/playlists` | Create playlist for user | `POST /me/playlists` |
| `GET /me/following/contains` | Check follows | `GET /me/library/contains` |
| `GET /playlists/{id}/followers/contains` | Check playlist follow | `GET /me/library/contains` |
| `GET /me/tracks/contains` | Check saved tracks | `GET /me/library/contains` |
| `GET /me/albums/contains` | Check saved albums | `GET /me/library/contains` |
| `GET /me/episodes/contains` | Check saved episodes | `GET /me/library/contains` |
| `GET /me/shows/contains` | Check saved shows | `GET /me/library/contains` |
| `GET /me/audiobooks/contains` | Check saved audiobooks | `GET /me/library/contains` |
| `PUT /me/tracks` | Save tracks | `PUT /me/library` |
| `PUT /me/albums` | Save albums | `PUT /me/library` |
| `PUT /me/episodes` | Save episodes | `PUT /me/library` |
| `PUT /me/shows` | Save shows | `PUT /me/library` |
| `PUT /me/audiobooks` | Save audiobooks | `PUT /me/library` |
| `PUT /me/following` | Follow artists | `PUT /me/library` |
| `PUT /playlists/{id}/followers` | Follow playlist | `PUT /me/library` |
| `DELETE /me/tracks` | Remove tracks | `DELETE /me/library` |
| `DELETE /me/albums` | Remove albums | `DELETE /me/library` |
| `DELETE /me/episodes` | Remove episodes | `DELETE /me/library` |
| `DELETE /me/shows` | Remove shows | `DELETE /me/library` |
| `DELETE /me/audiobooks` | Remove audiobooks | `DELETE /me/library` |
| `DELETE /me/following` | Unfollow artists | `DELETE /me/library` |
| `DELETE /playlists/{id}/followers` | Unfollow playlist | `DELETE /me/library` |
| `POST /playlists/{id}/tracks` | Add items to playlist | `POST /playlists/{id}/items` |
| `GET /playlists/{id}/tracks` | Get playlist items | `GET /playlists/{id}/items` |
| `DELETE /playlists/{id}/tracks` | Remove playlist items | `DELETE /playlists/{id}/items` |
| `PUT /playlists/{playlist_id}/tracks` | Update playlist items | `PUT /playlists/{id}/items` |

## ✅ AVAILABLE Endpoints

### Library
- `GET /me/tracks` — Get saved tracks
- `GET /me/albums` — Get saved albums
- `GET /me/audiobooks` — Get saved audiobooks
- `GET /me/episodes` — Get saved episodes
- `GET /me/shows` — Get saved shows
- `GET /me/playlists` — Get current user's playlists
- `PUT /me/library` — Save items (NEW — replaces type-specific endpoints)
- `DELETE /me/library` — Remove items (NEW)
- `GET /me/library/contains` — Check if saved (NEW)
- `PUT /playlists/{id}` — Change playlist details
- `POST /me/playlists` — Create playlist
- `GET /me/following` — Get followed artists

### Metadata
- `GET /artists/{id}` — Single artist (limited fields!)
- `GET /artists/{id}/albums` — Artist's albums
- `GET /albums/{id}` — Single album (limited fields!)
- `GET /albums/{id}/tracks` — Album tracks
- `GET /tracks/{id}` — Single track (limited fields!)
- `GET /audiobooks/{id}` — Single audiobook
- `GET /audiobooks/{id}/chapters` — Audiobook chapters
- `GET /chapters/{id}` — Single chapter
- `GET /episodes/{id}` — Single episode
- `GET /shows/{id}` — Single show
- `GET /shows/{id}/episodes` — Show episodes
- `GET /search` — Search (max 10 results, default 5)

### User
- `GET /me` — Current user profile (limited fields!)
- `GET /me/top/{type}` — User's top artists/tracks

### Player
- `GET /me/player` — Playback state
- `GET /me/player/currently-playing` — Now playing
- `GET /me/player/recently-played` — Recent tracks
- `GET /me/player/devices` — Available devices
- `GET /me/player/queue` — Current queue
- `PUT /me/player/play` — Start/resume playback
- `PUT /me/player/pause` — Pause
- `POST /me/player/next` — Skip next
- `POST /me/player/previous` — Skip previous
- `PUT /me/player/seek` — Seek to position
- `PUT /me/player/volume` — Set volume
- `PUT /me/player/repeat` — Set repeat mode
- `PUT /me/player/shuffle` — Toggle shuffle
- `POST /me/player/queue` — Add to queue

### Playlists
- `POST /playlists/{id}/items` — Add items (NEW)
- `GET /playlists/{id}/items` — Get items (NEW)
- `DELETE /playlists/{id}/items` — Remove items (NEW)
- `PUT /playlists/{id}/items` — Update/reorder items (NEW)

## ⚠️ Removed Fields

### Artist object
- `followers` ❌
- `popularity` ❌

### Track object
- `popularity` ❌
- `available_markets` ❌
- `linked_from` ❌
- `external_ids` — REVERTED (available again, see March 2026 changelog)

### Album object
- `popularity` ❌
- `label` ❌
- `available_markets` ❌
- `album_group` ❌
- `external_ids` — REVERTED (available again)

### User object (GET /me)
- `country` ❌
- `email` ❌
- `followers` ❌
- `product` ❌
- `explicit_content` ❌

### Show object
- `available_markets` ❌
- `publisher` ❌

### Audiobook/Chapter object
- `available_markets` ❌
- `publisher` ❌ (audiobook only)

## 🔧 Search Changes

| Parameter | Before | After |
|-----------|--------|-------|
| `limit` max | 50 | 10 |
| `limit` default | 20 | 5 |

## 📋 Development Mode Requirements (as of Feb 2026)

- Spotify Premium required
- Max 1 Client ID per developer
- Max 5 authorized users
- Limited to supported endpoints (see above)
