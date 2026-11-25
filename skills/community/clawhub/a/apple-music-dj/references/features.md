# Engagement Features: details

The full description of each feature: what it computes and how to present it. `SKILL.md` keeps each
feature's triggers, run command and safety rules; read this when you need the detail.

Beyond playlist strategies, these features drive daily engagement and deeper music discovery.

### Taste DNA Card
**Triggers:** "taste card", "taste DNA", "share my taste", "my music identity", "listener profile"
Generate a shareable visual card (SVG or text) summarizing the user's taste: archetype label
(e.g., "Deep Catalog Digger", "Genre Drifter"), top genres with bars, top artists, era mix,
and stats (energy, variety, mainstream, velocity).

Run: `python3 {baseDir}/scripts/taste_card.py <profile.json> [--format svg|text] [--output card.svg]`

Archetype detection is automatic based on profile data. Always present the text version
in chat; offer to generate the SVG for sharing. The card is designed to be screenshot-friendly.

### Compatibility Score
**Triggers:** "how compatible am I with [artist]", "compatibility", "do I match [artist]",
"compare my taste with", "would I like [artist]"
Score how well the user's taste aligns with an artist's catalog DNA (0-100%).
Also supports comparing two user profiles if both have run the taste profiler.

Run:
- `python3 {baseDir}/scripts/compatibility.py artist <profile.json> <storefront> <artist_name>`
- `python3 {baseDir}/scripts/compatibility.py profile <profile1.json> <profile2.json or amdj1:code>`

Present the percentage, a verdict ("Deeply compatible", "Strong overlap", "Wild card"),
matching genres, and whether the artist is already in their library.

### Listening Insights
**Triggers:** "listening timeline", "how has my taste changed", "listening streaks",
"milestones", "year in review", "my [year] in music", "wrapped", "listening stats"

Three subcommands:

**Timeline:** `python3 {baseDir}/scripts/listening_insights.py timeline <profile.json>`
Shows taste evolution across Replay years — top artist, genre, and listen time per year.
Present as a narrative: "In 2022 you were deep into shoegaze, by 2024 you shifted to jazz."

**Streaks:** `python3 {baseDir}/scripts/listening_insights.py streaks <profile.json>`
Surfaces milestones (from Replay API) and computed insights: artist loyalty, genre dominance,
discovery rate, library size, rating activity.

**Year in Review:** `python3 {baseDir}/scripts/listening_insights.py year-review <profile.json> [--year 2025]`
Comprehensive year analysis — deeper than Apple Replay. Includes obscurity score, variety
analysis, top songs/artists/albums, total listen time, and narrative insights.
Card: `python3 {baseDir}/scripts/listening_insights.py year-review <profile.json> > review.json` then
`python3 {baseDir}/scripts/taste_card.py <profile.json> --mode year-review --data review.json [--format text]`.
Offer the output's `caption` as ready-to-post text alongside the card. Without Replay for that year,
hours show as "—", the top artist and genre come from the current profile (the card labels them "(now)"),
and the caption describes current taste ("My Apple Music taste right now: …") instead of that year.

### Catalog Gap Analysis
**Triggers:** "what have I missed", "what am I missing from [artist]", "catalog gaps",
"albums I haven't heard", "discography check"
Scans the user's favorite artists' full discographies and identifies albums with zero tracks
in the user's library. Ranks recommendations by release date.

Run: `python3 {baseDir}/scripts/catalog_explorer.py gap-analysis <profile.json> <storefront>`

Present as: "You love Radiohead but you've only heard 3 of their 9 albums. Here's what
you're missing, ranked by how much you'd probably like each one."

**Add them to the library:** `... gap-analysis <profile.json> <storefront> --add-missing 5`
previews the newest 5 missing albums and changes nothing. **Adding writes to the user's
library — show them the preview and get a yes before re-running with `--yes`.**

### Taste Drift
**Triggers:** "taste drift", "how has my taste changed lately", "what's changed since [date]",
"am I listening to different stuff", "what's new in my taste"
Every fresh `taste_profiler.py` build saves a small dated snapshot (no song IDs) to
`~/.apple-music-dj/snapshots/`. Drift compares the newest one with the snapshot closest to
the chosen date: genres rising and falling, artists entering or leaving the top 20, era shift,
variety/mainstream/energy changes, and whether the listener archetype changed.

Run: `python3 {baseDir}/scripts/taste_drift.py [--since 90d | --from 2026-01-01] [--profile <profile.json>] --format text`
Needs at least two snapshots from different days. If there are fewer, say so and suggest
setting up the monthly drift job (below); use Listening Insights → Timeline for long-range history from Replay.
Card: `python3 {baseDir}/scripts/taste_drift.py > drift.json` then
`python3 {baseDir}/scripts/taste_card.py <profile.json> --mode drift --data drift.json [--format text]`.

### Import a Playlist
**Triggers:** "import my Spotify playlist", "move this playlist to Apple Music", "rebuild this list in Apple Music"
Rebuilds a playlist from a CSV (e.g. a Spotify export from a tool like Exportify) or a text file of
`Artist - Title` lines. Matches by ISRC when the CSV has that column, otherwise by a strict title +
artist search; anything unclear is reported as unmatched instead of guessed. The user's steps for
getting a playlist out of Spotify are in `references/spotify-import.md`.

Preview: `python3 {baseDir}/scripts/import_playlist.py <file>`
Create: `python3 {baseDir}/scripts/import_playlist.py <file> --create --name "<name>"` (writes to the library — confirm first)
Show the user the exact / fuzzy / unmatched counts and list the unmatched ones.

### Feedback
**Triggers:** "I didn't like track 7", "thumbs down that song", "I loved track 3", "never play that again"
Rates the song in Apple Music and updates the cached profile so later playlists skip it
immediately: `python3 {baseDir}/scripts/feedback.py dislike --playlist-name "<name>" --position 7 --profile <profile.json>`
(or pass song IDs; `like` and `clear` also exist). Without `--yes` it only previews; add `--yes` once the user has confirmed. Positions are 1-based within playlists the DJ
created; omit `--playlist-name` for the most recent one. **This writes a rating to the user's account**,
so only do it on the user's explicit say-so, and name the song and the rating you are about to write
when it isn't obvious which track they mean.

**How ratings steer playlists.** Each rating also updates the profile's `rating_signals`: each rated
song's artist and genres (`songs`), and the like/dislike counts per artist and per genre that are
always recomputed from them. Clearing a song therefore removes exactly what it added. `feedback.py` looks the song up once to learn
its artist and genres, and `taste_profiler.py` rebuilds the counts from your Apple Music ratings
on every refresh (it looks up at most 25 rated songs it hasn't already fetched). Every strategy
and the daily pick then apply them:

- A disliked song is always skipped. One dislike changes nothing for the artist.
- An artist with 2 or more dislikes and no likes is left out, unless you play them a lot (play
  weight ≥ 0.05). Then their tracks are only scored down.
- A liked artist gets +0.05 per net like (max +0.15), and a liked genre +0.02 per net like (max +0.1).
- A boosted or scored-down track says so in its `reason`, and the playlist JSON lists the
  affected artists under `steered_by_ratings`.
- In a blend, both listeners' ratings count. An artist one listener disliked twice is left out
  unless that listener plays them a lot or the other listener likes them; then the two
  listeners' score changes add up.

### Album Deep Dive
**Triggers:** "tell me about [album]", "album deep dive", "what's on [album]",
"should I listen to [album]", "break down [album]"
Pull track listing, classify each track as single vs deep cut, show where the album sits
in the artist's discography, and recommend which deep cuts to try first.

Run: `python3 {baseDir}/scripts/catalog_explorer.py album-dive <storefront> <album_name> [--artist <name>]`

### Artist Rabbit Hole
**Triggers:** "rabbit hole from [artist]", "take me on a journey from [artist]",
"artist chain", "explore from [artist]", "where does [artist] lead"
Interactive chain exploration. Starts from one artist, searches for adjacent artists,
maps outward step by step. Each step tagged as familiar/adjacent/frontier zone.
Outputs tracks from each artist for a potential journey playlist.

Run: `python3 {baseDir}/scripts/catalog_explorer.py rabbit-hole <profile.json> <storefront> <artist_name> [--depth 4]`

Present each step with the artist name, zone, genres, and sample tracks. Ask if the user
wants to go deeper or turn the exploration into a playlist.

### Daily Song Drop
**Triggers:** "daily song", "song of the day", "give me one track", "daily pick"
One track per day with a one-sentence rationale. Uses a date-based seed for consistency
(same pick all day). Draws from deep cuts and trending tracks scored against the user's taste.

Run: `python3 {baseDir}/scripts/daily_pick.py daily <profile.json> <storefront>`

### What Should I Listen To Right Now?
**Triggers:** "what should I listen to", "what should I play", "recommend something now",
"I need music", "play something"
Context-aware instant recommendation. Factors in time of day (morning → gentle indie,
late night → ambient), maps to genre boosts, and scores candidates accordingly.

Run: `python3 {baseDir}/scripts/daily_pick.py now <profile.json> <storefront>`

### Concert Prep Playlist
**Triggers:** "seeing [artist] live", "concert prep", "going to [artist] show",
"setlist for [artist]", "get ready for [artist] concert"
Builds a prep playlist: top songs (likely setlist material) + deep cuts to learn before
the show. **Preview first:** by default the script writes nothing to Apple Music — it prints the
proposed name, description and track list as JSON. Show that to the user and, only after they
say yes, re-run the same command with `--create`. If the preview shows `"name_exists": true`, a
playlist with that name is already in the library and creation would be skipped — pick another name.

Run: `{baseDir}/scripts/concert_prep.sh <storefront> <artist_name> [playlist_name] [--create]`

### Personalized New Release Radar
**Triggers:** "new releases", "what's new from my artists", "any new music",
"release radar", "new albums this week"
Scans the user's top 20 artists for releases in the last 7 days, plus searches for
genre-relevant new releases from adjacent artists. Can optionally create a playlist.

Run: `{baseDir}/scripts/new_releases.sh <profile.json> <storefront> [--create-playlist]`
