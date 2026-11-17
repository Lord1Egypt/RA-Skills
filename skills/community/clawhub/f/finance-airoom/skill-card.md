## Description:

Provides agents with a supervised downloader and guidance for retrieving structured, simulated global finance data files from airoom.ltd and using them as reference inputs for market monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoom-ai](https://clawhub.ai/user/airoom-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a Playwright-based downloader for airoom.ltd financial data files and feed downloaded data into supervised analysis or monitoring workflows. It should be used as reference data support, not as an autonomous trading system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-directed financial strategy use could be mistaken for investment advice or autonomous trading instruction.

Mitigation: Use only as a supervised downloader and analysis aid; require human or qualified professional review before any financial decision and do not allow autonomous trade execution.

Risk: Broad network and download behavior can retrieve unexpected files from a configured target page.

Mitigation: Restrict WP_URL and WP_TARGET_URL to trusted pages, use a dedicated output directory, set WP_MAX_FILES where appropriate, and inspect downloaded files before opening or passing them to other tools.

Risk: Optional WordPress credentials may be exposed if used on HTTP or untrusted sites.

Mitigation: Avoid entering WordPress credentials unless the site uses HTTPS and credential use is necessary; prefer the public no-login workflow when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airoom-ai/skills/finance-airoom)
- [Publisher profile](https://clawhub.ai/user/airoom-ai)
- [airoom.ltd target data page](http://airoom.ltd/index.php/airoom/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration examples; runtime commands produce console text and locally downloaded files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WP_URL, WP_TARGET_URL, optional WordPress credentials, WP_OUTPUT_DIR, and WP_MAX_FILES to control the target page and download behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
