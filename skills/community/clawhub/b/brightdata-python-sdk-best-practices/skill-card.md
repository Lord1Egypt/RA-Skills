## Description:

Guides agents writing, modifying, debugging, or reviewing Python code that uses the Bright Data Python SDK for scraping, search, datasets, or browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to produce correct Bright Data Python SDK code for web scraping, search, datasets, and browser automation. It emphasizes async client use, context managers, authentication handling, result checks, error handling, and export patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bright Data requests can transmit target URLs, prompts, browser activity, and collected data to a third-party service.

Mitigation: Use the skill only for approved sites and datasets, and confirm that the target data and Bright Data service use fit the applicable policy and terms.

Risk: Generated examples may create or delete Bright Data zones or otherwise change account state.

Mitigation: Require explicit confirmation before running account-changing actions such as zone creation or deletion.

Risk: API tokens and browser credentials can be exposed if they are hardcoded, logged, or committed.

Mitigation: Load credentials from environment variables or approved secret stores, keep them out of logs and code, and review generated snippets before execution.

Risk: The installation guidance uses an unpinned `pip install brightdata-sdk` command.

Mitigation: Use a virtual environment and pin or review the package version before production use.

Risk: Dataset exports can write collected data to local files.

Mitigation: Choose approved output paths and handle exported JSON, CSV, or JSONL files according to data handling requirements.

## Reference(s):

- [Bright Data Python SDK API Reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/meirk-brd/skills/brightdata-python-sdk-best-practices)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API usage patterns, credential handling guidance, async/sync client choices, and export recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
