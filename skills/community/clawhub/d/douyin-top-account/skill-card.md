## Description:

Tracks Douyin daily, weekly, and monthly top account rankings by category, returns ranking summaries, and can generate local HTML reports from RedFox API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, brands, MCN teams, and analysts use this skill to inspect Douyin account leaderboards, compare categories, monitor account performance, and request downloadable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key.

Mitigation: Confirm the key source, scope, validity period, and revocation path before use; provide it through environment configuration and avoid exposing it in prompts, logs, or output files.

Risk: The security summary reports unsafe automatic opening, unescaped report data, external JavaScript, and Windows shell-opening risk in the HTML report workflow.

Mitigation: Treat generated reports as untrusted until report fields are escaped, default auto-open behavior is removed, Windows shell invocation is avoided, and JavaScript is bundled or integrity-pinned.

Risk: The authoritative security verdict for this release is suspicious.

Mitigation: Review and scan the skill before deployment, and avoid using it in sensitive environments until the reported report-generation risks are addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-top-account)
- [API documentation](references/api_docs.md)
- [Category mapping rules](references/category_map.md)
- [Score rules](references/score_rules.md)
- [Update rules](references/update_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML files, shell commands, configuration, guidance]

**Output Format:** [Markdown ranking summaries, JSON data files, and local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated reports may include clickable Douyin profile links.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
