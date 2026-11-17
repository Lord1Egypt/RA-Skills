## Description:

Cn Meeting Minutes generates structured Markdown meeting minutes from local text, JSON, or standard input, extracting discussion points, decisions, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers who work with Chinese meeting notes can use this skill to convert local plain-text, JSON, or standard-input meeting content into a structured Markdown minutes file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted meeting input can influence the generated Markdown content.

Mitigation: Review generated minutes before sharing, and open Markdown from untrusted inputs in a viewer that disables raw HTML and automatic remote-resource loading.

Risk: Rule-based extraction can miss, truncate, or misclassify discussion points, decisions, and action items.

Mitigation: Treat the generated minutes as a draft and have a human review important decisions, owners, and deadlines before relying on them.

Risk: Meeting files may contain confidential business or personal information.

Mitigation: Use the skill in a local environment appropriate for the data sensitivity and avoid sharing generated minutes without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-meeting-minutes)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands]

**Output Format:** [Markdown meeting-minutes document with CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only Python standard-library script; rule-based extraction; writes a Markdown file to the requested or default output path.]

## Skill Version(s):

1.4.3 (source: server release metadata; artifact frontmatter says 1.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
