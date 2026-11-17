## Description:

Use when users need daily news summaries, current events, or want to stay informed about world news in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaceymarvin99](https://clawhub.ai/user/jaceymarvin99)

### License/Terms of Use:


## Use Case:

External users and agents use Daily News to fetch Chinese daily briefings, daily quotes, or recent historical news in text, Markdown, JSON, or image URL formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the requested date and output format to the external 60s API.

Mitigation: Review or constrain shell and network permissions when strict least privilege is required.

Risk: News availability and response content depend on the external API service.

Mitigation: Handle empty or unavailable responses by trying recent dates and verify important news before relying on it.

## Reference(s):

- [60s API endpoint](https://60s.viki.moe/v2/60s)
- [ClawHub skill page](https://clawhub.ai/jaceymarvin99/skills/daliy-news)
- [Publisher profile](https://clawhub.ai/user/jaceymarvin99)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Plain text, Markdown, JSON, or image URLs written to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional date and encoding parameters; recent-date availability depends on the 60s API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
