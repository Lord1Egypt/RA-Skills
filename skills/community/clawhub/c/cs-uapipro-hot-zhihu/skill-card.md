## Description:

Fetches Zhihu hot-list entries through the UAPIPRO API when a user asks for Zhihu trending topics and requires a UAPIPRO API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savior1987](https://clawhub.ai/user/savior1987)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and format current Zhihu hot-board items for agent responses or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a UAPIPRO API key to uapis.cn and depends on that third-party service for Zhihu hot-list data.

Mitigation: Install only if the publisher and UAPIPRO service are trusted, scope and rotate the API key where possible, and review outbound API use before deployment.

Risk: The skill depends on a Chinese-oriented third-party API provider and may return service-specific or regionally oriented content.

Mitigation: Confirm the API provider, data source, language expectations, and operational fit before using the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/savior1987/skills/cs-uapipro-hot-zhihu)
- [Publisher profile](https://clawhub.ai/user/savior1987)
- [UAPIPRO Zhihu hotboard API endpoint](https://uapis.cn/api/v1/misc/hotboard?type=zhihu)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Plain text or JSON produced by a Python script, with optional Markdown-facing summaries in agent replies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UAPIPRO_API_KEY and may include Zhihu item titles, links, hot values, descriptions, labels, and image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
