## Description:

Generates Chinese A-share market daily reports with major index levels, index changes, advance/decline counts, and manually supplied trading volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize daily Chinese A-share market data into shareable Markdown reports and JSON data. It supports market review workflows where users can manually supplement trading-volume figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted date argument can read, modify, or delete JSON files outside the intended data folder.

Mitigation: Use only canonical YYYY-MM-DD dates, do not pass untrusted date strings, and avoid --clear until path validation is fixed.

Risk: The skill writes reports and JSON files under both the workspace and the user's Desktop folder.

Mitigation: Run it from a controlled workspace and review generated files before sharing or automating downstream use.

Risk: Automatic fetching uses iWenCai as an external data source and appears incomplete in this version.

Mitigation: Validate market figures against a trusted source and manually supplement or review missing volume data before relying on the report.

## Reference(s):

- [Cn Stock Volume on ClawHub](https://clawhub.ai/shinelp100/skills/cn-stock-volume)
- [README](artifact/README.md)
- [Design Document](artifact/DESIGN.md)
- [Usage Examples](artifact/EXAMPLES.md)
- [Tonghuashun iWenCai](https://www.iwencai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports, JSON data, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under the workspace output directory and the user's Desktop; volume fields may require manual input.]

## Skill Version(s):

3.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
