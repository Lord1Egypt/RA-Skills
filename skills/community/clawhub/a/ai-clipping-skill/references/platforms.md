# Platforms: limits and the rules that matter for clippers

`cliplib.py` holds the same numbers `check_clips.py` uses. Platforms change them; when a platform
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

A link the brief requires in the caption goes in anyway (the campaign checks for it); the bio link
is the one viewers can tap.

## Paid content settings

| | Through WoopSocial | By hand |
|---|---|---|
| TikTok | `isBrandedContent: true` on every campaign post (TikTok's "Paid partnership" label). A branded post can't be "only you". | nothing |
| Instagram | WoopSocial can't set it | turn on the paid partnership label in the app, inside the 30 minutes |
| YouTube | WoopSocial can't set it (YouTube's own API has the field; WoopSocial doesn't send it) | tick "includes paid promotion" in YouTube Studio, inside the 30 minutes |

Your own content on your own account (`own_content`): no paid partnership label; TikTok gets
`isYourBrand: true` ("Your brand") only when the clips promote your own product, service or
business (`promotes_own_business`); nothing to set on Instagram or YouTube.

TikTok tells a creator when it detects undisclosed branded content and gives 24 hours before the
video loses For You eligibility. Content Rewards requires the platform's paid-partnership setting
where it exists, and "#Ad" at the top of the caption.

## Reused content and many accounts (2026)

Clippers often run several accounts. The platforms act on the same content spread across them:

- **TikTok** keeps reposts with nothing new added out of For You, and limits reused material.
- **Instagram** (since 30 April 2026) stops recommending accounts that mostly repost, and shows the
  original of identical copies. A watermark or a speed change doesn't count as original.
- **YouTube** names networks of channels posting the same content in its spam policy, and its
  reused-content rules can block monetisation of a clip channel even with permission.

So the skill gives every account its own edit: another moment of the footage, or at least its own
hook and caption, and `check_clips.py` blocks the same file twice and two accounts on the same
platform sharing most of their footage. It never speeds up, mirrors, crops differently or filters
a clip to dodge duplicate detection: the platforms don't treat that as new, and it is the pattern
their spam rules describe.

Keep the pace modest per account. A handful of good posts beats a flood that gets the account
limited.

## Sounds

No posting API can pick a sound from an app's library, and a sound can't be added to a post once
it is live. When the brief requires one, that post is planned by hand from the start: the by-hand
page has the sound as a step before posting. On Instagram the same, when the brief names it for
Reels (`required_sound.platforms`).

## Safe area

The apps draw their own buttons over the video: TikTok's tabs at the top, the like and share rail
on the right, the caption and account name at the bottom. `make_clips.py` keeps the on-screen
disclosure below the top tabs (from y 300 of 1920), and a watermark or logo between x 80 and 900
and y 420 and 1340, so nothing the brief requires is hidden.
