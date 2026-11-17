## Description:

Automatically accesses a configured airoom.ltd WordPress page and downloads detected financial data files with configurable limits and basic file-type blocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to configure a Playwright-based downloader that retrieves financial data documents from an airoom.ltd WordPress page for local review and downstream analysis. The bundled finance strategy material is reference content, not authorization to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loose download and credential safeguards may expose users to unexpected downloads or unnecessary credential handling.

Mitigation: Install in an isolated environment, prefer HTTPS-only URLs, avoid providing WordPress credentials unless required, and set a small WP_MAX_FILES limit.

Risk: Downloaded files may be unsafe, malformed, or unsuitable for downstream workflows.

Mitigation: Inspect and scan downloaded files before opening them or feeding them into other tools.

Risk: Bundled financial strategy text could be mistaken for permission to trade or coordinate trading behavior.

Mitigation: Treat all strategy material as reference only and require human or registered-broker review before any trading action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/airoom-ltd-global-finance-data-platform)
- [Artifact skill documentation](artifact/SKILL.md)
- [Product manual](artifact/README.md)
- [English product manual](artifact/README airoom ltd Global Finance Data Platform English.txt)
- [Default configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration, and locally downloaded data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download supported document, data, archive, media, or web files from the configured target; WP_MAX_FILES can limit downloads.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
