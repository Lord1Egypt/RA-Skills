## Description:

Fetches Bilibili video danmaku from a video URL or BVID and analyzes keyword frequency, word clouds, sentiment distribution, and public-opinion reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartloe](https://clawhub.ai/user/smartloe)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content operations teams use this skill to collect public Bilibili danmaku and turn it into review-ready keyword, sentiment, word-cloud, and opinion-report outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs Python dependencies and the release evidence does not provide a reviewed lockfile.

Mitigation: Run it in a normal non-privileged environment and pin or review dependencies before routine use.

Risk: The skill contacts public Bilibili endpoints and writes files under the selected output directory.

Mitigation: Use it only for permitted public-data analysis and choose an output directory where generated CSV, JSON, TXT, PNG, and Markdown files are expected.

Risk: Generated Markdown reports may include public-content output that is unsafe to trust blindly.

Mitigation: Review generated Markdown before sharing it or opening it in renderers that load remote images or raw HTML.

## Reference(s):

- [Bilibili Danmaku ClawHub Skill](https://clawhub.ai/smartloe/skills/bilibili-danmaku)
- [Methodology](references/methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; runtime artifacts include CSV, JSON, TXT, PNG, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports and charts should be reviewed before business decisions or publication.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
