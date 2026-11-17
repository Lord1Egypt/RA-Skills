## Description:

Command-line client for the Bank of Korea ECOS API to list statistic tables and fetch time series data as JSON by code and frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Bank of Korea ECOS statistics from a command-line workflow, including listing statistic tables and fetching time series by code, frequency, and date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ECOS API key can be exposed through raw request URLs, debug logs, shell history, or shared output.

Mitigation: Keep BOK_API_KEY in a secret store or local environment variable, avoid publishing raw requests or debug logs, and rotate the key if exposure is suspected.

Risk: The submitted artifact contains documentation only, so users may assume the CLI implementation is included when it is not present in this release artifact.

Mitigation: Install only from a trusted CLI implementation source and verify the package contents before using the skill in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/bank-of-korea-ecos-cli)
- [ECOS API portal](https://ecos.bok.or.kr/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOK_API_KEY; ECOS API responses are direct JSON passthroughs.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
