## Description:

Searches Nowcoder interview-experience posts and prepares structured interview-preparation reports for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[champagne315](https://clawhub.ai/user/champagne315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with an agent to search Nowcoder interview-experience posts by keyword, time window, and tag, then generate Markdown interview-preparation reports in Chinese, English, or bilingual format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Nowcoder and processes scraped interview-post content.

Mitigation: Install and run it only when this external network access and local processing of Nowcoder content are acceptable for the user and environment.

Risk: Security evidence reports insecure HTTPS settings and TLS weakening.

Mitigation: Review network code before deployment and prefer a version that restores certificate verification and avoids weakened TLS configuration.

Risk: Security evidence reports unsafe prompt and file handling while the artifact supports local configuration, prompt, and report-data writes.

Mitigation: Constrain execution to a trusted workspace, validate prompt names and file paths, and review generated report data before reuse.

Risk: Scraped post content can influence report generation.

Mitigation: Treat Nowcoder content as untrusted source data, not as agent instructions, and review outputs before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/champagne315/skills/follow-nowcoder)
- [Nowcoder discussion pages](https://www.nowcoder.com/discuss)
- [Nowcoder feed detail pages](https://www.nowcoder.com/feed/main/detail)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON metadata and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally written JSON report data, user configuration, custom prompts, and generated report text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
