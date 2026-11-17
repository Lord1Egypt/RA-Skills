## Description:

Builds a per-deal US account brief from public filings and company pages, with every fact tied to a source and a date checked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US sales representatives use this skill to prepare concise context for a specific live account or deal before a buyer call, using public records and company sources.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Research claims, source URLs, or checked dates may be inaccurate or out of date.

Mitigation: Treat the result as an unverified draft and check every claim, URL, and date against the cited source before relying on or sharing it.

Risk: The bundled script expects Markdown headings, while the supplied starter template is YAML.

Mitigation: Provide Markdown-heading input that matches the script, or resolve the format mismatch before running it.

Risk: Running the script may replace an existing digest.md in the selected output directory.

Mitigation: Choose a dedicated output directory where replacing digest.md is acceptable.

Risk: The release also includes an optional unsigned Windows app outside the bundled workflow.

Mitigation: The Windows app is unnecessary for the bundled workflow; assess it separately before use.

## Reference(s):

- [Account research sources](references/account-research-sources.md)
- [Publisher homepage (skill metadata)](https://github.com/rapidworker1)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/account-research-brief)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown account-research digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized by deal context, key facts, risks, open questions, next step, and sources; facts should include source URLs and checked dates.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
