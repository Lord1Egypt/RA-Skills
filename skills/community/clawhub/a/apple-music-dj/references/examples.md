# Example Interactions

How typical requests map to the skill's features. `SKILL.md`'s Quick Commands table is the short
version; read this when a request doesn't obviously match one of its rows.

**"I've been in a funk, make me something uplifting"**
→ Strategy 2 (Mood). Target: uplifting energy from their preferred genres.

**"I keep listening to the same 20 songs"**
→ Strategy 4 (Constellation). Start from heavy rotation, expand outward.

**"Make me a running playlist"**
→ Strategy 2 (Activity). 140–180 BPM feel, high energy, filtered through taste.

**"What's trending that I'd actually like?"**
→ Strategy 3 (Trend Radar). Charts filtered through taste fingerprint + wildcards.

**"I love Radiohead and Björk but I've heard everything"**
→ Strategy 1 (Deep Cuts) + Strategy 4 (Constellation) combined.

**"My gym playlist is getting stale"**
→ Strategy 5 (Refresh). Analyze vibe, add fresh tracks, prune overplayed ones.

**"Set me up with weekly auto-playlists"**
→ Cron config. The opt-in `weekly-mix` job (a Trend Radar playlist every Monday); preview the
  lines with `--dry-run`, then install with `--confirm` after a yes.

**"Show me my taste card"**
→ Generate Taste DNA Card. Present text version in chat, offer SVG export.

**"How compatible am I with Tyler, the Creator?"**
→ Compatibility score. Show percentage, verdict, matching genres.

**"What albums am I missing from Radiohead?"**
→ Catalog gap analysis. List unheard albums, recommend starting points.

**"Tell me about In Rainbows"**
→ Album deep dive. Track listing, deep cuts vs singles, discography context.

**"Take me on a rabbit hole from Radiohead"**
→ Artist chain: Radiohead → Talk Talk → Bark Psychosis → Disco Inferno. Offer playlist.

**"Give me one song for today"**
→ Daily song drop. One track, one reason, done.

**"What should I listen to right now?"**
→ Context-aware pick. Time of day + taste → instant recommendation.

**"I'm seeing Phoebe Bridgers next month"**
→ Concert prep playlist. Show the preview (top songs + deep cuts); create it in Apple Music on a yes.

**"Any new releases from my artists?"**
→ New release radar. Scan top artists + genre discoveries, report findings.

**"How was my 2025 in music?"**
→ Year in review. Listen time, top artists, obscurity score, narrative insights.

**"Give me songs like Phoebe Bridgers"**
→ Strategy 6 (Similar). Her best songs plus similar artists, weighted toward the user's taste.

**"Make me a 90s throwback"**
→ Strategy 7 (Era). 90s albums from their own top artists, plus genre-matched finds.

**"Make a playlist for me and my sister"**
→ Strategy 8 (Blend). Ask for her taste code (or profile JSON); shared artists first, balanced 60/40 at most.

**"Remix Today's Hits for me" (with the link)**
→ Strategy 9 (Remix). Keeps the tracks that fit their taste, swaps the rest, and says "you'd keep 14 of 50".

**"How has my taste changed since spring?"**
→ Taste drift with `--from`. Rising/falling genres, new top artists, archetype change.

**"I didn't like track 7 of that playlist"**
→ Feedback. Rate it down, update the profile, confirm it won't come back.

**"Move my Spotify playlist over"**
→ Import. Preview match counts, list unmatched tracks, then create on a yes.
