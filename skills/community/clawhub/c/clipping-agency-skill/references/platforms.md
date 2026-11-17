# Platforms: limits and the rules that matter for an agency

`agencylib.py` holds the same numbers `check_clips.py` uses. Platforms change them; when a platform
rejects something these say is fine, trust the platform and tell the user.

## The file

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Length | 3 s up to the account's own limit (read it per account) | 3 s to 15 min | up to 3 min, or it becomes a normal video |
| Size | 4 GB | 300 MB | 256 GB |
| Frame rate | 23 to 60 | 23 to 60 | not restricted |
| Video | H.264 | H.264 or HEVC, standard colour, up to 25 Mbps | not restricted |
| Sound | not restricted | AAC, up to 48 kHz | not restricted |
| File | MP4 | MP4 or MOV with its index at the start | MP4 |

`make_clips.py` writes one file that passes all three: 1080x1920 (or `--width`), H.264 High,
yuv420p, BT.709, AAC 48 kHz stereo, index at the start, -14 LUFS.

## Text

| | TikTok | Instagram Reels | YouTube Shorts |
|---|---|---|---|
| Title | none | none | required, 100 characters |
| Caption | 2,200 (most emoji count 2) | 2,200, at most 5 hashtags | description, 5,000 bytes |
| Links | not clickable | not clickable | not clickable in Shorts |

Put the full-episode link in the client's bio, not in the caption: it is the one viewers can tap.

## Paid content settings

A clip that includes a sponsor segment of the episode is paid content, wherever it is posted.

| | Through WoopSocial | By hand |
|---|---|---|
| TikTok | `isBrandedContent: true` (TikTok's "Paid partnership" label). A branded post can't be "only me". | nothing |
| Instagram | WoopSocial can't set it | turn on the paid partnership label in the app after the Reel is live |
| YouTube | WoopSocial can't set it | tick "includes paid promotion" in YouTube Studio |

Every caption of such a clip says it is paid too (`#ad`, "Sponsored by ...", "Paid partnership with
..."): `check_clips.py` refuses one that doesn't. A clip that promotes the client's own product or
business (`promotes_client_business`) gets TikTok's "Your brand" label. A plain show clip gets
neither.

## Music

Podcast and stream episodes often carry intro music, stings and background tracks the client licensed
for the episode only. Short clips with that music can be muted, claimed or blocked on the client's
account. `check_clips.py` warns when a clip may hold music: a caption cue like `[MUSIC]`, a stretch
the batch marks, or several seconds with sound and no words. It is a hint, never a guarantee either
way: someone listens before the page goes to the client. The skill never adds music; the client adds
licensed music in the app if they want it.

## One client's clip, one client's accounts

The same file never goes to two clients (the ledger and every other client's clips are checked), and
a clip goes only to the accounts in its own client's file. Never speed up, mirror or filter a clip:
it changes nothing about who owns the footage, and it is the pattern the platforms' reused-content
rules describe.

## Safe area

The apps draw their own buttons over the video: TikTok's tabs at the top, the like and share rail
on the right, the caption and account name at the bottom. `make_clips.py` keeps the hook, the
captions and the client's logo between x 80 and 900 and y 420 and 1340, so nothing is hidden. When
the hook would cover the logo, the hook moves under it, or the logo waits until the hook is gone.
