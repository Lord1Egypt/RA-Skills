## Description: <br>
Collects and formats daily game-industry AI news from game, AI, and technology sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuhuimin0224-create](https://clawhub.ai/user/zhuhuimin0224-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current game AI daily reports, weekly reports, topical roundups, and concise shareable briefings with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a Python news-fetching workflow that contacts public RSS and API sources and updates local cache files. <br>
Mitigation: Install only in environments where network access to those sources and local cache updates are acceptable. <br>
Risk: Generated reports may include loosely related or non-authoritative game AI items. <br>
Mitigation: Treat outputs as curated news leads, verify important claims against linked primary sources, and review source attribution before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuhuimin0224-create/ai-game) <br>
- [Source catalog](references/sources.json) <br>
- [Keyword and category rules](references/keywords.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown news briefings with source links and concise recommendations; JSON cache files may be read or refreshed by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily reports are intended to stay under 10 items and weekly reports under 15 items, with category grouping and full URLs.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
