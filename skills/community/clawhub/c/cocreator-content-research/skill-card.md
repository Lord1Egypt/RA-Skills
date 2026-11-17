## Description:

Gathers raw TikTok and Instagram content intelligence through ScrapeCreators so agents can discover trending hooks, analyze competitor strategies, and look up creator profile metrics without generating or posting content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iammiracle](https://clawhub.ai/user/iammiracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent collect social media research on TikTok and Instagram, including keyword or hashtag discovery, competitor hook analysis, and creator profile metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic uv installation path runs a remote shell script.

Mitigation: Install uv separately through a trusted, pinned, or verified method before enabling the skill.

Risk: Search terms, creator handles, and the ScrapeCreators API key are sent to ScrapeCreators.

Mitigation: Use the skill only when sharing those inputs with ScrapeCreators is acceptable, and provide the API key through a controlled environment variable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iammiracle/skills/cocreator-content-research)
- [Publisher profile](https://clawhub.ai/user/iammiracle)
- [uv installer referenced by metadata](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and SCRAPE_CREATORS_API_KEY; helper scripts call ScrapeCreators APIs and return social media research data.]

## Skill Version(s):

1.0.2 (source: server release metadata, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
