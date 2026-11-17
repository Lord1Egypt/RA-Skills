# What each platform accepts

These are the limits of each platform's own posting API, which is what WoopSocial posts through.
`check_video.py` and `plan.py` hold the same numbers. Platforms change them; when a platform
rejects something these say is fine, trust the platform and tell the user.

## The video file

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Length | 3 s up to the account's own limit (up to 10 min; some accounts get less, so read it per account) | 3 s to 15 min | up to 3 min, or it becomes a normal video |
| Shape | any; 9:16 fills the screen | any; 9:16 fills the screen | square or vertical, or it isn't a Short |
| Size | 4 GB | 300 MB | 256 GB |
| Width | 360 to 4096 px per side | up to 1920 px | plays at up to 1080p |
| Frame rate | 23 to 60 | 23 to 60 | not restricted |
| Video | H.264 recommended | H.264 or HEVC, 4:2:0, standard colour (no HDR), up to 25 Mbps; 8-bit is the safe choice (10-bit gets a warning) | not restricted |
| Sound | not restricted | AAC, mono or stereo (5.1 is an error), up to 48 kHz | not restricted |
| File | MP4 recommended | MP4 or MOV with its index at the start ("fast start") | MP4 is the norm |

Sizes are decimal: 300 MB is 300,000,000 bytes, the stricter of the two ways to count, so a file
that passes here passes either way. `--fix` aims at 285,000,000 bytes.

**One file that passes everywhere:** MP4, H.264, 8-bit, standard colour, 1080x1920 (anything up to
1920 px wide passes), 23 to 60 fps, AAC stereo 48 kHz, index at the start, under 300 MB, 3 to 180
seconds. `check_video.py --fix` writes that from the user's file. It keeps the picture size and
scales down only a video over 1920 px wide or 4096 px on a side: a 1920x1080 or 1920x1920 file
stays that size. It never changes length or shape.

Instagram is the strictest. A file that passes Instagram passes the other two, apart from length.

## Things that surprise people

- **A Short is decided by YouTube, not by you.** Square or vertical and up to 3 minutes: a Short.
  Longer or horizontal: a normal video. There is no switch, and #Shorts changes nothing.
- **A Short over 1 minute with an active copyright claim is blocked everywhere.** Under 1 minute
  this rule doesn't apply.
- **TikTok's maximum length belongs to the account.** `social_accounts_get_platform_inputs` returns
  it. Don't assume 10 minutes.
- **Sounds don't travel.** A sound picked inside TikTok or Instagram exists only there. An exported
  copy posted elsewhere can be muted or blocked. Post the original export with your own or licensed
  audio. If a TikTok needs a sound from TikTok's library, send it as a draft (`"tiktok_draft":
  true`) and add the sound in the app; on the other platforms, post that one by hand in its app.
- **Another app's watermark.** Instagram says it doesn't recommend videos with a visible watermark.
  Always post the original export, never a copy saved from another app.
- **Instagram over 3 minutes** posts, but reports say such Reels aren't recommended to people who
  don't follow the account.
- **HDR.** Newer iPhones record HDR (extra-bright colour) by default, and schedulers report that
  Instagram rejects it. `--fix` converts HDR to standard colour only when the installed ffmpeg has
  the `zscale` filter (`check_setup.py` says whether it does), and checks the result. Without it
  `--fix` writes nothing and says how to get a standard-colour file: export or share it as a
  standard (SDR / Most Compatible) video if your phone offers that, or turn off HDR video in the
  camera settings and film again; in an editing app, export as Rec. 709 (SDR).
- **A recording without a stored length** (a browser or screen recording). The checker measures it
  from the frames. If that fails it says it can't read the length, and `--fix` re-saves it as MP4.

## Text

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Title | none | none | required, 100 characters, no `<` or `>` |
| Text | caption, 2,200 | caption, 2,200 | description, 5,000 bytes, no `<` or `>` |
| Hashtags | 5 at most is what the app reports | 5 per post (Instagram's limit since December 2025) | 3 show by the title; above 60, all are ignored |
| Hidden tags | none | none | 500 characters in total |
| @mentions | from the caption | 20 at most | not a feature |
| Links | not clickable | not clickable | not clickable in Shorts |

How each length is counted (the plan page shows the same number the check uses):

- YouTube counts the description in bytes: an emoji or a non-Latin letter is 2 to 4 bytes. Hidden
  tags: the commas between tags count, and a tag with a space counts 2 more.
- TikTok counts most emoji as 2.
- X counts every link as 23, and Chinese, Japanese and Korean characters and emoji as 2.
- Bluesky counts characters as a reader sees them: a joined emoji or a letter with its accent is 1.
- For joined emoji and accented scripts the X and Bluesky counts are approximate. The plan then
  says "about", and going over the limit is a warning to check in the app, not an error.
- A hashtag needs a letter: "#1" is a number and is not counted.

## Cover

- The skill sends the cover image to TikTok and Instagram as WoopSocial's schema defines it. After
  the first post to a new account, look at the live post once to confirm the cover is right. It
  must really be a JPEG under 8 MB: `plan.py` reads the file's content, so a PNG renamed to `.jpg`
  is caught before upload.
- `cover.py` records the second the cover came from; the plan and every by-hand page print it, so
  a frame picked by hand in an app matches.
- Instagram's profile grid shows the middle 3:4 of a 9:16 cover: 240 px are cut from the top and
  the bottom of a 1080x1920 image. Keep the face and any title in the middle.
- YouTube: the cover isn't set through WoopSocial. Pick the frame in the YouTube app after it's live.

## Settings the owner must choose

| Platform | Setting | Why |
|---|---|---|
| TikTok | who can see the post | TikTok requires the user to choose it for every post; no default |
| TikTok | comments, duets, stitches | same |
| TikTok | "Promotional content" / "Paid partnership" | required when the video promotes something |
| TikTok, Instagram | AI label | required for realistic AI-generated content |
| YouTube | made for kids | a legal declaration by the channel owner |
| YouTube | public, unlisted or private | chosen per video |
| YouTube | "Altered content" (AI) and "Paid promotion" | required when they apply; set in YouTube Studio, not through WoopSocial |

## Several accounts on one platform

YouTube's spam policy names the same video across many channels, including edits made to disguise
copies (speed, crop, filters). Instagram recommends only the original of identical copies. TikTok's
guidelines don't name it, but make reused material ineligible for the For You feed. Posting one
video to accounts with different audiences (a language each, a region each, separate brands) is
normal practice: write each account's `audience` and give each its own text. The plan warns once
per job with that platform's rule (a single note when every account has a different audience),
and the user decides. It never alters a video to make copies differ.

## Other platforms

| | Length | Size | Text |
|---|---|---|---|
| Facebook (Page) | 3 s at least; vertical and up to 90 s posts as a Reel, anything else as a normal video (the plan says which) | 4 GB | 5,000 |
| LinkedIn (profile or Page) | 3 s to 15 min | 5 GB | 3,000 |
| Pinterest | 4 s to 15 min | 2 GB | title 100, description 800 |
| Threads | up to 5 min | 1 GB | 500 |
| X | up to 2 min 20 s | 512 MB | 280 |
| Bluesky | up to 3 min | 100 MB | 300 |
