## Description:

Search Douyin for a user-specified topic and time range, then return the top hotspot videos ranked by visible engagement signals with strict no-fabrication rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eanpeng0-debug](https://clawhub.ai/user/eanpeng0-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, content operations teams, topic analysts, and learners use this skill to collect and rank recent Douyin videos for a chosen topic and time range using only visible engagement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser and network access to view public Douyin search results, so network restrictions, browser unavailability, or platform access changes can prevent collection.

Mitigation: Check access before collecting and use the documented failure response when the environment cannot reach or read Douyin results.

Risk: Export mode writes collected results to the user-specified folder or Desktop.

Mitigation: Enable export only for intended destinations and keep writes limited to the requested result file.

Risk: Engagement fields may be unavailable or incomplete because the skill relies on public visible page data.

Mitigation: Exclude entries missing required fields, mark unavailable optional fields as missing, and rank only by visible engagement signals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eanpeng0-debug/skills/douyin-topic-hotspot-collector)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown table with concise status notes; optional exported result file when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on public visible Douyin fields and must mark missing optional fields instead of fabricating data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
