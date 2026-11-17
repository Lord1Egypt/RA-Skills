## Description:

This skill helps WeChat Official Account creators analyze high-performing cover patterns from RedFox data and generate content-matched cover design proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat Official Account creators, content operators, MCN teams, designers, and media editors use this skill to query recent cover-trend data, summarize visual patterns, produce an HTML analysis report, and prepare three cover design proposals with image-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on RedFox API data and API-returned image URLs that are not clearly validated before use.

Mitigation: Use the skill only when the RedFox data provider is trusted, keep network access restricted where practical, and validate remote URLs before opening or embedding them.

Risk: The skill creates local HTML reports from user and API data without clear escaping controls.

Mitigation: Open generated HTML cautiously and add HTML escaping or sanitization before deploying the workflow in a shared or higher-trust environment.

Risk: The workflow requires a REDFOX_API_KEY credential.

Mitigation: Store the key in the environment, avoid logging or hard-coding it, and ensure it can be reset or revoked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/explosive-cover-generator-gzh)
- [Publisher profile](https://clawhub.ai/user/yuanyi-github)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [WeChat trend data format](references/gzh_trend_data_format.md)
- [Report template](references/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON or Markdown API data, a local HTML report, and image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local HTML report and, after user selection, produce a 2.35:1 900x383 cover image.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
