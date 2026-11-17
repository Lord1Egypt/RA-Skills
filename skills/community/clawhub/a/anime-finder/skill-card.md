## Description:

Find anime releases from natural-language Chinese or English requests, verify anime identity, search public torrent sources, and return results, magnet links, or queued download status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiggy-chan](https://clawhub.ai/user/tiggy-chan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to resolve anime search or follow-up download requests, inspect ranked release results, and optionally queue a selected torrent through Transmission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically queue torrent downloads and start Transmission from broad natural-language requests.

Mitigation: Prefer search-only or cli-only operation in cautious deployments, and review any proposed torrent before allowing a download.

Risk: The skill persists local user preferences and last-download state.

Mitigation: Inspect or clear state/user_profile.json and state/last_download.json when saved preferences or download history should not be retained.

Risk: The skill searches public anime torrent sources.

Mitigation: Use it only where public torrent search and any resulting downloads are acceptable under local policy and applicable rights.

## Reference(s):

- [Intent Examples](references/intent_examples.md)
- [Bangumi Subject Search API](https://api.bgm.tv/search/subject/{query}?type=2)
- [Bangumi Subject API](https://api.bgm.tv/subject/{subject_id})
- [Nyaa RSS Search](https://nyaa.si/?page=rss&q={query})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON workflow payloads with optional plain-text CLI summaries, magnet links, torrent URLs, and Transmission status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local preference state and last-download state when requests explicitly ask for persistent preferences or status tracking.]

## Skill Version(s):

1.4.0 (source: server release metadata and changelog, released 2026-04-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
