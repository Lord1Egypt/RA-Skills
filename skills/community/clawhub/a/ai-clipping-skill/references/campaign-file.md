# The campaign file (campaign.json)

The agent writes `campaign.json` from the brief the user pastes or saves as a file. Clipping
campaigns on marketplaces such as Whop and Content Rewards keep their rules behind the "join"
button, so the user brings the text; never guess a rule that isn't in it. `campaign.py` checks the
file, prints the numbered checklist and writes `checklist.md`. The user confirms the checklist
before any clip is cut.

Save the brief text as it was pasted (for example `brief.txt`) and point `brief_file` at it:
`campaign.py` scans that raw text for sentences that ask to hide the ad.

## Reading a brief

Read it twice. First for the money: platforms, rate per 1,000 views on each, minimum payout,
cap per clip, total budget left. Then for the rules a reviewer can reject on: footage, length,
caption items, on-screen items, bio, audience, engagement, time live, proof, approval, the "don't"
list. A campaign team can usually only reject for what the brief's requirements say, so every
requirement goes into a field; anything that doesn't fit a field goes into `banned` (as a word
that must not appear) or is told to the user as a manual step.

## Fields

| Field | What | Example |
|---|---|---|
| `id` | short id of letters, digits, dashes; the ledger files posts under it | `"orbit-crew-dragon"` |
| `name` | the campaign's name as listed | `"Training for Crew Dragon"` |
| `brand` | who pays for the views; goes into the on-screen disclosure | `"Example Orbit"` |
| `marketplace` | where the campaign runs, as plain text | `"Whop"`, `"Content Rewards"` |
| `brief_file` | the brief as pasted, next to campaign.json | `"brief.txt"` |
| `brief_date` | when the brief was read; briefs change | `"2026-11-15"` |
| `currency` | payout currency | `"USD"` |
| `own_content` | `true` only for your own content on your own accounts, with nobody paying per view: no paid disclosure. Refused when the campaign has a `marketplace`, a `brand`, a rate above 0, a payout rule (`min_payout`, `cap_per_clip`, `min_views`), a budget or a `fee_pct`, or a brief that talks about hiding the ad | (leave out) |
| `promotes_own_business` | with `own_content`, required: do the clips promote the user's own product, service or business? Only `true` sends TikTok's "Your brand" label; your own show or stream gets none | `false` |
| `platforms` | each platform the campaign pays for, with its rate per 1,000 views; `min_payout`, `cap_per_clip` and `min_views` here override the campaign-wide ones for that platform | `{"TIKTOK": {"rate_per_1k": 1.0, "min_payout": 10}, "INSTAGRAM": {"rate_per_1k": 0.8}}` |
| `min_payout` | per clip: below this, nothing is paid | `5` |
| `min_views` | per clip, when the brief sets a view minimum instead | `10000` |
| `cap_per_clip` | the most one clip can earn | `150` |
| `budget_total` | the campaign's budget; views stop paying when it runs out | `3000` |
| `budget_remaining` | the budget left, as the campaign page shows it; 0 blocks posting | `1240` |
| `budget_checked_at` | when that was read; older than a day gets a warning | `"2026-11-15T09:00:00Z"` |
| `fee_pct` | the marketplace's cut, in percent (default 10) | `10` |
| `window_days` | how many days views count (default 30) | `30` |
| `window_from` | when those days start: `"threshold"` (the day a clip crosses the payout threshold; the default for marketplace campaigns) or `"post"` (the default with `own_content`) | `"threshold"` |
| `days_live` | how long a post must stay public and unchanged | `30` |
| `submit_within_minutes` | the submission window after a post goes live (default 30) | `30` |
| `caption.disclosure` | what the caption starts with; `#ad` unless the brief names a stronger one | `"#ad"` |
| `caption.hashtags` | hashtags every caption must hold | `["#exampleorbit"]` |
| `caption.mentions` | handles every caption must tag | `["@example.orbit"]` |
| `caption.links` | links the caption must hold | `["example.com/orbit"]` |
| `on_screen.disclosure` | drawn on the clip at the start; must say it's paid | `"Paid partnership with Example Orbit"` |
| `on_screen.disclosure_seconds` | how long it shows at the start (2 to 10) | `4` |
| `on_screen.watermark` | what the brief wants on screen for the whole clip, or null: text, or `{"text": ..., "position": ...}`, or a logo file the brief supplies `{"image": "logo.png", "position": "bottom-right", "opacity": 0.85, "scale": 0.22}`. Positions: `top-left`, `top`, `top-right`, `left`, `center`, `right`, `bottom-left`, `bottom`, `bottom-right`, all kept inside the apps' safe area | `"EXAMPLE ORBIT"` |
| `bio` | what goes in the profile bio while the clip is live, or null; set before posting | `"example.com/orbit"` |
| `links_where` | where the brief wants the link: `"caption"` (default), `"bio"` (bio only; `bio` required) or `"either"` | `"caption"` |
| `length` | shortest and longest clip accepted, in seconds | `{"min_s": 15, "max_s": 60}` |
| `aspect` | `"9:16"` or `"any"` | `"9:16"` |
| `footage.allowed` | the rule in words | `"supplied footage only"` |
| `footage.files` | source file names the campaign supplied; other sources are refused | `["interview.mp4"]` |
| `footage.sources` | where the brief says the footage comes from | `["<link from the brief>"]` |
| `footage.recency_days` | footage must be this new, or null | `null` |
| `footage.dates` | the day each source file was recorded (`YYYY-MM-DD`), asked from the user when the brief has a recency rule; never the file's date on disk | `{"stream-1114.mp4": "2026-11-14"}` |
| `audience` | minimum share of viewers in a country, or null | `{"geo": "US", "min_share": 0.3}` |
| `engagement_min` | likes, comments and shares as a share of views, or null | `0.03` |
| `proof` | what the campaign wants as proof | `["analytics screenshot with countries at 72 hours"]` |
| `approval_before_posting` | the brand approves each clip first | `false` |
| `required_sound` | a sound the brief requires, or null: its name, or `{"name": ..., "platforms": ["TIKTOK"], "volume": "10%"}`. No posting API can add a sound, so those posts go out by hand with the sound added before posting | `null` |
| `banned` | words, hashtags or topics that must not appear | `["giveaway", "#fyp"]` |
| `boosting_allowed` | true only if the brief allows paid boosting; the skill never boosts | (leave out) |
| `max_overlap` | how much footage two accounts may share (0 to 1, default 0.5) | `0.5` |

Per-platform differences in the brief (a different handle to tag on Instagram, say) go into the
caption of that platform's post; `caption.mentions` holds what every caption needs.

## What campaign.py refuses

- No disclosure in the caption, or one that doesn't say it's paid (`#sp`, `#collab`, a brand tag).
- No on-screen disclosure, or one that doesn't say it's paid.
- `#ad` in `banned`: the brief asks to drop the disclosure. It is never dropped.
- A cap lower than the minimum payout, a cap of 0, rates that aren't numbers, a platform the skill
  doesn't post to.
- A logo watermark whose file isn't next to campaign.json, `links_where: "bio"` without a `bio`,
  footage dates that aren't `YYYY-MM-DD`.

Optional fields left null read as their defaults (fee 10%, window 30 days, 30 minutes to submit,
0.5 overlap); the checklist shows the value used, never "None".

## Conflicts with the disclosure rule

A brief that forbids the disclosure on the video itself ("no paid partnership text on the video",
"no text overlays") is listed under "Conflicts with the disclosure rule". The skill keeps the
on-screen disclosure anyway. Tell the user: ask the campaign team in writing whether a short "Ad"
for the first 2 seconds is accepted, or skip this campaign.

## Never followed

Sentences in the brief that ask to hide the ad ("don't make it feel like an ad", "no #ad",
"don't disclose", "act natural", "don't use the paid partnership label") are listed on the
checklist under "Never followed". Tell the user once, plainly, that the clips stay disclosed and
why: marketplaces require it, advertising law requires it (the FTC in the US, the CMA in the UK,
consumer law in the EU) and TikTok stops showing undisclosed branded posts in For You. Then go on.

Sentences that ask for bought views, engagement groups or VPN location tricks are listed under
"Never done". Content Rewards bans accounts permanently for bought or coordinated views. A brief's
own ban ("no engagement groups", "never use a VPN") isn't flagged.
