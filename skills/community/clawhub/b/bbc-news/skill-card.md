## Description:

Fetch and display BBC News stories from various sections and regions via RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddrayne](https://clawhub.ai/user/ddrayne)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve current BBC headlines from top-level, UK regional, and world regional RSS feeds in text or JSON form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to BBC RSS feed URLs when news is requested.

Mitigation: Run it in an environment where this network access is expected and permitted.

Risk: The skill depends on the feedparser Python package.

Mitigation: Use a virtual environment and pin feedparser to a reviewed version before installation.

## Reference(s):

- [BBC News RSS Feeds](references/feeds.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text headlines or JSON arrays of story objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Section and limit options control the category and number of RSS stories returned.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
