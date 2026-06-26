## Description: <br>
Fetch and display BBC News stories from various sections and regions via RSS feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddrayne](https://clawhub.ai/user/ddrayne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to fetch current BBC headlines from top-level, topic-specific, UK regional, and world regional RSS feeds in text or JSON form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires network access to BBC RSS feeds. <br>
Mitigation: Allow network access only where live BBC headline fetching is intended and restrict egress to the documented BBC RSS feed domains when possible. <br>
Risk: The skill requires a manual install of the feedparser Python dependency. <br>
Mitigation: Install feedparser from a trusted package source in an isolated Python environment before using the skill. <br>


## Reference(s): <br>
- [BBC News RSS Feeds](references/feeds.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ddrayne/bbc-news) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text headline lists or JSON arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports selecting a BBC section or region and limiting the number of returned stories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
