## Description:

Extracts structured personal memories from ChatGPT export data into organized timelines, people profiles, and thematic records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyresearch](https://clawhub.ai/user/cyresearch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert their own ChatGPT export into a searchable personal memory archive with quarterly timelines, people profiles, topic records, and extraction progress logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create durable local archives from highly sensitive ChatGPT export data, including third-party personal details, direct quotes, emotional summaries, and topic indexes.

Mitigation: Use a private or encrypted workspace, avoid cloud-synced folders unless intentional, redact sensitive or third-party information, and review outputs before sharing or importing them into another assistant.

Risk: The security verdict is suspicious because the privacy scoping and safeguards may be insufficient for the sensitivity of the exported data.

Mitigation: Review the skill before installing, prefer pinned or verified install sources, and confirm that the handling of plaintext exports matches the user's privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyresearch/skills/chatgpt-memory-extraction)
- [Output Format Specification](references/output-format.md)
- [Quality Rules](references/quality-rules.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files and plaintext conversation extracts organized in a directory structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory archive files, including timelines, people profiles, topic records, raw extracted conversation text, and progress logs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
