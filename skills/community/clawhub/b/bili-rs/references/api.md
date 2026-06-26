# Bilibili API Endpoints & Payloads

Base URL: `https://api.bilibili.com`

Required headers are defined in `src/config.rs` as constants (`USER_AGENT`, `REFERER`, `ORIGIN`).
All requests need `User-Agent` and `Referer`; write operations additionally need `Origin`.

**Important:** Enable reqwest `brotli` + `deflate` features — some endpoints (e.g. search) return `Content-Encoding: br`.

## Video API

| Function | Method | Endpoint | Notes |
|----------|--------|----------|-------|
| `get_video_info(bvid)` | GET | `/x/web-interface/view` | |
| `get_player_info(bvid, cid)` | GET | `/x/player/wbi/v2` | subtitle list |
| `fetch_subtitle_json(url)` | GET | subtitle CDN URL | prepend `https:` to `//` URLs |
| `get_video_comments(aid, page)` | GET | `/x/v2/reply/main` | fallback: `/x/v2/reply`, `sort=2` |
| `get_video_ai_conclusion(bvid,cid,aid,up_mid)` | GET | `/x/web-interface/view/conclusion/get` | Requires WBI signing + login; pass up_mid |
| `get_related_videos(bvid)` | GET | `/x/web-interface/archive/related` | |

## User API

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_self_info()` | GET | `/x/space/myinfo` |
| `get_user_info(uid)` | GET | `/x/space/wbi/acc/info` |
| `get_user_relation(uid)` | GET | `/x/relation/stat` |
| `get_user_videos(uid, pn, ps)` | GET | `/x/space/wbi/arc/search` |
| `get_followings(uid, pn, ps)` | GET | `/x/relation/followings` |
| `modify_relation(uid, act)` | POST | `/x/relation/modify` |

## Search API

| Function | Method | Endpoint | Notes |
|----------|--------|----------|-------|
| `search_user(keyword, page, ps)` | GET | `/x/web-interface/search/type` | `search_type=bili_user` |
| `search_video(keyword, page, ps)` | GET | `/x/web-interface/search/type` | `search_type=video` |

## Collections & History

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_favorite_list(uid)` | GET | `/x/v3/fav/folder/created/list-all` |
| `get_favorite_videos(fav_id, page)` | GET | `/x/v3/fav/resource/list` |
| `get_watch_history(count)` | GET | `/x/web-interface/history/cursor` |
| `get_toview()` | GET | `/x/v2/history/toview` |

## Dynamics API

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_dynamic_feed(offset)` | GET | `/x/polymer/web-dynamic/v1/feed/all` |
| `get_user_dynamics(uid, offset, need_top)` | GET | `/x/polymer/web-dynamic/v1/feed/space` |
| `post_text_dynamic(text)` | POST | `/x/dynamic/feed/create/dyn` |
| `delete_dynamic(dynamic_id)` | POST | `/x/dynamic/feed/operate/remove` |

## Discovery

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_hot_videos(pn, ps)` | GET | `/x/web-interface/popular` |
| `get_rank_videos(day)` | GET | `/x/web-interface/ranking/v2` |

## Interactions

| Function | Method | Endpoint |
|----------|--------|----------|
| `like_video(bvid, like)` | POST | `/x/web-interface/archive/like` |
| `coin_video(bvid, multiply)` | POST | `/x/web-interface/coin/add` |
| `triple_video(bvid)` | POST | `/x/web-interface/archive/like/triple` |

## Audio

| Function | Method | Endpoint |
|----------|--------|----------|
| `get_audio_url(bvid, cid)` | GET | `/x/player/wbi/playurl` |

## Error Code Mapping

| Code(s) | BiliError variant |
|---------|-------------------|
| -101, -111 | `NotAuthenticated` |
| -403 | `PermissionDenied` |
| -404, 62002, 62004 | `NotFound` |
| -412, 412 | `RateLimited` |
| other | `Upstream { code, message }` |

## Key Payload Structs

```rust
VideoSummary { id, bvid, aid, title, description, duration_seconds, duration, url, owner: Owner, stats: VideoStats }
VideoStats { view, danmaku, like, coin, favorite, share }
User { id, name, username, level, coins, sign, vip }
Relation { following, follower }
DynamicItem { id, author, published_at, published_label, title, text, stats }
SubtitleItem { from: f64, to: f64, content }
Comment { id, author: CommentAuthor, message, like, reply_count }
```

### Helper functions (in `payloads/`)

```rust
fn format_duration(secs: u64) -> String   // "MM:SS" or "H:MM:SS"
fn strip_html(text: &str) -> String       // regex <[^>]+> → ""
fn to_u64(v: &Value) -> u64              // Number or String
fn extract_bvid(input: &str) -> Option<String>  // regex \bBV[0-9A-Za-z]{10}\b
fn format_count(n: u64) -> String        // ≥10000 → "X.X万"
```
