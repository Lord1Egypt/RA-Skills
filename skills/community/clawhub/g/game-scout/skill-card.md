## Description:

Video game strategy specialist that amalgamates tactics, builds, guides, and meta knowledge from Reddit, YouTube creators, wikis, Twitter/X, and game databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rclark4958](https://clawhub.ai/user/rclark4958)

### License/Terms of Use:

MIT-0

## Use Case:

Players and gaming-focused agents use this skill to research current game strategy, builds, loadouts, mechanics, patch impacts, tier lists, and pro-play meta. It helps synthesize web, Reddit, YouTube, wiki, Twitter/X, and game-database evidence into actionable, sourced recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game-related searches, URLs, Reddit/Twitter/X targets, and YouTube targets may be sent to third-party services including Exa, Bright Data, and yt-dlp-backed retrieval.

Mitigation: Use public, non-sensitive targets only; avoid private, internal, authenticated, or sensitive URLs; keep API keys scoped and revocable.

Risk: Game strategy and meta guidance can become stale or conflict across patches, sources, regions, or skill levels.

Mitigation: Cross-check recent sources, verify patch dates, surface source disagreement, and include confidence and caveats in final guidance.

## Reference(s):

- [ClawHub Game Scout release page](https://clawhub.ai/rclark4958/skills/game-scout)
- [Search Strategies Reference](artifact/references/search-strategies.md)
- [Source Extraction Patterns](artifact/references/source-extraction.md)
- [Game Database Directory](artifact/references/game-databases.md)
- [Sample Query Pipelines](artifact/examples/sample-queries.md)
- [Exa AI](https://exa.ai)
- [Bright Data](https://brightdata.com)
- [Bright Data dashboard](https://brightdata.com/cp/zones)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with source lists, confidence notes, tables, and inline shell commands when retrieval is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are patch-aware and source-grounded, with caveats for recency, source disagreement, and confidence.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
