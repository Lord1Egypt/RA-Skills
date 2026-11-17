## Description:

Query chinadrugtrials.org.cn, the Chinese Drug Clinical Trial Registration and Information Disclosure Platform, for Chinese clinical trial registration records by drug, indication, company, CTR number, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zephyrlucky-skills](https://clawhub.ai/user/zephyrlucky-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research operations teams, and external agents use this skill to retrieve public ChinaDrugTrials records and return registration details such as applicant/company, first public disclosure date, trial status, and official detail links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation against a public website can fail or return incomplete data when the site changes, times out, blocks automation, or requires a specific Chromium/Chrome executable.

Mitigation: Run with Playwright and an available Chromium/Chrome executable, keep waits bounded, and verify the official result count and detail links before relying on the output.

Risk: Incorrect keyword encoding or fallback parsing can produce irrelevant or stale clinical trial records.

Mitigation: Use UTF-8 query handling, confirm the result page matches the intended keyword or CTR number, and clearly mark any detail field that could not be verified from the official page.

## Reference(s):

- [ChinaDrugTrials platform](https://www.chinadrugtrials.org.cn/)
- [ClawHub skill listing](https://clawhub.ai/zephyrlucky-skills/skills/chinadrugtrials-query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown table by default, or JSON when requested; guidance may include shell commands and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one row per registration and may include official detail links plus unverified-field markers when a detail value cannot be confirmed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
