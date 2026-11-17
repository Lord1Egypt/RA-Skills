## Description:

Fetches Douyin hot-list and trending-search data and returns ranked items with titles, heat values, labels, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media operators use this skill to retrieve current Douyin trending topics for hot-topic tracking, trend analysis, marketing planning, and social media operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML report path may render untrusted remote Douyin data in a browser.

Mitigation: Review and harden the report generator before use by escaping text, validating links, and avoiding unsafe innerHTML behavior.

Risk: The skill depends on Douyin web interfaces whose response shape and access controls may change or rate-limit frequent requests.

Mitigation: Use reasonable request volumes, handle empty or changed responses, and review failures before relying on output for operational decisions.

Risk: Local database and reporting scripts expand the skill beyond the basic fetch command.

Mitigation: Review those scripts before enabling database storage or HTML reporting in a deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/douyin-hot)
- [Douyin website](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Files]

**Output Format:** [Console text or JSON records; optional local SQLite data and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Items may include rank, title, popularity, link, label, and type.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
