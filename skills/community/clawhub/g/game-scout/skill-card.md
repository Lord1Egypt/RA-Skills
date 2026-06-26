## Description: <br>
Game Scout researches current video game tactics, builds, guides, patch-sensitive meta knowledge, and game mechanics across community, video, wiki, social, and database sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rclark4958](https://clawhub.ai/user/rclark4958) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and gaming-focused agents use this skill to research current game builds, loadouts, mechanics, tier lists, strategies, patch impacts, and esports or high-level play recommendations. It helps synthesize actionable answers with source attribution and confidence notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game-related prompts and source URLs may be sent to Exa, Bright Data, and YouTube tooling. <br>
Mitigation: Avoid private URLs, account details, sensitive notes, and access tokens in prompts or source lists. <br>
Risk: The skill requires third-party API credentials for search and scraping workflows. <br>
Mitigation: Store API keys in ~/.openclaw/.env, keep them out of source control, and avoid sharing logs that may contain credential values. <br>
Risk: Gaming recommendations can become stale after game patches or balance changes. <br>
Mitigation: Use the skill's patch-aware source checks, cite source dates, and flag low-confidence or pre-patch guidance. <br>


## Reference(s): <br>
- [Game Scout Skill Page](https://clawhub.ai/rclark4958/game-scout) <br>
- [Game Scout README](artifact/README.md) <br>
- [Sample Query Pipelines](artifact/examples/sample-queries.md) <br>
- [Search Strategies](artifact/references/search-strategies.md) <br>
- [Source Extraction](artifact/references/source-extraction.md) <br>
- [Game Database Directory](artifact/references/game-databases.md) <br>
- [Exa AI](https://exa.ai) <br>
- [Bright Data](https://brightdata.com) <br>
- [Bright Data Web Unlocker Zone Dashboard](https://brightdata.com/cp/zones) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with source lists, tables, concise recommendations, confidence labels, and inline shell commands when research tools are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include TL;DR summaries, structured build or strategy sections, caveats about patch recency, and numbered source citations.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
