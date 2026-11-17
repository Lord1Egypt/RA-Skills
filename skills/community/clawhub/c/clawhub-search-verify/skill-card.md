## Description:

Safely search and review ClawHub skills by keyword, showing details and risk before asking for explicit approval to install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viktorbjorn](https://clawhub.ai/user/viktorbjorn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search ClawHub for relevant skills, inspect basic trust signals, and request explicit approval before proceeding with installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be written to a local plaintext log.

Mitigation: Avoid entering sensitive project names, credentials, or confidential identifiers as search terms; review or disable logging before installation where possible.

Risk: The release evidence reports a mismatch between claimed read-only behavior and persistent local logging.

Mitigation: Review the wrapper behavior before use and prefer a version that accurately documents logging behavior or disables it by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viktorbjorn/skills/clawhub-search-verify)
- [Publisher profile](https://clawhub.ai/user/viktorbjorn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style terminal text with inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before installation guidance proceeds.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
