# Synoclips connector: tools and limits

Facts below come from the connector's own tool descriptions (read 2026-11-24; `get_video_upload_link` added 2026-11-25). Check again if a call behaves differently: tools change.

## Setup and account

| Tool | What it does | Approval |
|---|---|---|
| `list_accounts` | Connected YouTube, Instagram, TikTok and Facebook accounts (`account_id`, platform, name) and a link to connect more on the website. | no |
| `get_credits_and_plan` | Plan, credits left, storage, videos today (daily cap), clip retention days, and which features the plan includes (auto-posting, schedule, analytics, Story Studio, dubbing...). | no |

Accounts are connected only on the website (Settings → Integrations). The connector cannot connect them.

## Making clips

| Tool | Key inputs | Notes |
|---|---|---|
| `get_video_upload_link` | the same clip settings as `create_clips_from_link`, without `url` | For a **local file** (mp4, mov, mkv, webm). Returns a private link (valid one hour) where the person drops the file, and for Claude Code a script that uploads a file from this computer. Clips start by themselves after the upload. Follow with `list_videos` (newest first) and `get_video_status`. Ask before uploading. Added after 2026-11-24; a session connected earlier needs a reconnect to see it. |
| `create_clips_from_link` | `url` (YouTube, Twitch or Kick), `mode` ai/custom, `count` 1–20, `min_length` 5–120 s, `max_length` 10–180 s, `start_at`/`end_at`, `layout` face/blur/zoom/crop/split, `quality` 360/480/720/1080, `caption_style`, `music` off/auto/mood, `enhance_audio`, `auto_zoom`, `sound_effects`, `transitions`, `beep_bad_words`, `color` natural/vivid, `highlight_reel_seconds` 0/30/45/60 | Uses credits. Returns `video_id` at once; clips are made in the background (a few minutes). For local files use `get_video_upload_link`. |
| `get_video_status` | `video_id` | Waiting, running, done or failed, with finished clips (best first). |
| `list_videos` | `limit`, `status` | The user's videos, newest first. |
| `get_clip_options` | — | Framings, caption looks, music moods, dubbing languages. |

Layout guide: `blur` for stock footage or slides (full frame on a blurred fill), `face` for a talking head, `crop` to fill the screen, `split` for gaming facecam.

## Reviewing and editing clips

| Tool | Key inputs | Limits |
|---|---|---|
| `list_clips` | `video_id`, `sort` best/newest, `min_score` 0–100, `limit` 1–50 | Scores are the tool's own estimate, not a guarantee. |
| `get_clip` | `video_id`, `clip_id` | Title, hook, score, times, look, status, links. |
| `get_clip_caption_text` | `video_id`, `clip_id`, `platform` | The post text each platform will get. |
| `get_clip_transcript` | `video_id`, `clip_id` | Word times, for caption fixes. |
| `rename_or_retitle_clip` | `title`, `hook`, `description` | title ≤ 100, hook ≤ 60, description ≤ 2,000 characters. |
| `set_clip_hashtags` | `hashtags` | ≤ 30, with or without `#`; replaces the list. |
| `edit_clip` | `start`, `end`, `hook`, `title`, `description`, `caption_style`, `layout`, `cut_pauses`, `speed` 0.5–2, `caption_fixes`, `beep_bad_words` | Re-makes the clip; changing times or captions may use credits. |

## Publishing (always ask first)

| Tool | Key inputs | Notes |
|---|---|---|
| `schedule_clip` | `video_id`, `clip_id`, `account_ids`, `time` (ISO 8601 with time zone, up to 120 days ahead) | Goes through the platform posting checks. |
| `publish_clip_now` | `video_id`, `clip_id`, `account_ids` | Posts immediately. Use only when the user asked for "now". |
| `change_post_time` | `post_id`, `time` | Approval first. |
| `cancel_scheduled_post` | `post_id` | Approval first. |
| `retry_post` | `post_id` | Approval first. |

Time format example: `2026-12-01T20:00:00+05:00` (Pakistan time).

## Follow-up

| Tool | What it does |
|---|---|
| `list_scheduled_posts` | Posts waiting to go out, soonest first. |
| `list_posts` | Recent posts by status: scheduled, posted (with links and views), failed (with the reason), held. |
| `get_analytics` | Views of posted clips by video, clip, platform and day (7/14/30/90 days). |

## Other tools in the connector (not used by this skill's main flow)

Story Studio (`create_story_video`, `make_story_video`, `edit_story_scenes`, ...) makes videos from an idea or script; it is a separate plan feature. Live capture and streamer tools (`add_streamer`, `start_live_capture`, `clip_live_now`, ...) are for streamers. `dub_clip` dubs a clip into another language (plan feature). `make_highlight_reel` joins the best clips. For continuously watching a channel and clipping each new upload, the separate `synoclips-autopilot` plugin covers that workflow.
