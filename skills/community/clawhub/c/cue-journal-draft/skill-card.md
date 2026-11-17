## Description:

Produces editable corporate journal and newsletter drafts from supplied materials or public research, with source tracing and editorial quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

Editors and communications teams use the skill to turn issue materials or researched sources into editable corporate journal, customer newsletter, investor letter, and ESG drafts with traceable citations and review checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection check sends CUE_API_KEY to a server-provided address without verifying that destination.

Mitigation: Before running the credential-bearing command, independently confirm the destination is an approved HTTPS endpoint; do not send the key otherwise.

Risk: Optional research or reading-channel use may involve uploads or usage costs.

Mitigation: Review the material to be shared and approve each upload and any associated cost separately.

Risk: Release-cleanup commands may affect files in the current or target directories.

Mitigation: Check the working directory and target folders before running cleanup.

Risk: Imported Word edits and generated imagery may lose draft context or required AI-image labels.

Mitigation: Retain original drafts when importing Word edits and preserve AI-image labels.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-journal-draft)
- [Publisher profile](https://clawhub.ai/user/huhoo)
- [Cue API key setup](https://cuecue.cn/hub/api-key)
- [Cue service](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, PDF, DOCX]

**Output Format:** [Editable editorial drafts, outlines, evidence records, review reports, and publication files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports source-linked claims and human-reviewed editorial and layout checks; the skill does not replace editorial sign-off.]

## Skill Version(s):

0.15.27 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
