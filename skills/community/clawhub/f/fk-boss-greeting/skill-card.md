## Description:

Automates Boss Zhipin job searches and one-by-one HR greetings for Java-related roles using configured company and job filters, deduplication, and rate limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huguiqi](https://clawhub.ai/user/huguiqi)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and developers use this skill to search Boss Zhipin for Java-related roles, filter out configured companies and unrelated postings, and send greetings to HR contacts one at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser login state for Boss Zhipin, which can expose a real account to unintended automated actions.

Mitigation: Use a dedicated Boss Zhipin account or browser profile and review the login scope before running the skill.

Risk: Automated greetings or scheduled runs can contact HR accounts before the user has checked the selected postings.

Mitigation: Require a visible candidate review and approval step before any greeting is sent or scheduled.

Risk: Dependency and update instructions can install or refresh CLI code that has not been reviewed.

Mitigation: Pin and verify the CLI dependency, and avoid pull-and-reinstall updates until the source has been reviewed.

## Reference(s):

- [Filter rules configuration](references/filter-rules.json)
- [kabi-boss-cli](https://github.com/jackwener/boss-cli)
- [Boss Zhipin](https://www.zhipin.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute account actions through the Boss Zhipin CLI and write local greeting logs when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
