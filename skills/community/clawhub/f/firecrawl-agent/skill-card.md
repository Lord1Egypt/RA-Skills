## Description:

AI-powered autonomous data extraction that navigates complex sites and returns structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Firecrawl Agent for structured extraction from complex, multi-page websites, including pricing tiers, product listings, directory entries, and schema-shaped JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned runtime execution through npx can run a different Firecrawl CLI version than the reviewer expected.

Mitigation: Prefer a preinstalled, pinned Firecrawl CLI and review npx commands before allowing the agent to run them.

Risk: Agentic extraction can consume more Firecrawl credits than simple scraping.

Mitigation: Use --max-credits for costly runs and prefer simple scrape workflows for single-page extraction.

Risk: CLI execution can expose unnecessary environment secrets to the runtime.

Mitigation: Run with the minimum required environment and avoid exposing unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/firecrawl-agent)
- [Publisher profile](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; Firecrawl command results are JSON or output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent runs can take 2-5 minutes; --wait returns results inline, -o writes files, and --max-credits caps credit use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
