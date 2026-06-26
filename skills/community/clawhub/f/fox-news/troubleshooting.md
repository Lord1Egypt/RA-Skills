# Troubleshooting - Fox News Desk

## RSS Feed Is Slow or Empty

Symptoms:
- Feed returns stale items or no visible headlines.

Actions:
1. Fall back to the matching section page on `foxnews.com`.
2. Compare latest feed against the section page before claiming nothing changed.
3. Label the result as a page-based read instead of an RSS sweep.

## Live Coverage Is Gated or Not Useful

Symptoms:
- Live stream asks for a provider login or the page is video-heavy without enough text.

Actions:
1. Use `live-news` article coverage first.
2. Fall back to `video` clips or the closest section article.
3. State the access boundary instead of pushing credentialed playback.

## Opinion and News Keep Mixing

Symptoms:
- Search results or homepage links include opinion content in a straight-news request.

Actions:
1. Re-route to the specific section feed or page.
2. Exclude `opinion` unless the user asked for it.
3. Relabel any ambiguous item before keeping it in the briefing.

## Story Feels Too One-Sided

Symptoms:
- The user wants analysis, controversy review, or credibility checking.

Actions:
1. Keep the Fox summary as the first block.
2. Add one or more independent follow-up sources as a separate block.
3. State clearly where the extra context came from and why it was added.
