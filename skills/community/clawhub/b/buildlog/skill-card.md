## Description:

Record, export, and share your AI coding sessions as replayable buildlogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[espetey](https://clawhub.ai/user/espetey)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to record AI-assisted coding sessions, export them as replayable buildlogs, add notes or chapters, and optionally upload them for sharing or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buildlogs may be public by default, which can expose private code, internal URLs, customer data, or credentials.

Mitigation: Set buildlogs private by default, review each recording before upload, and avoid sharing sessions that contain sensitive material.

Risk: File-content snapshots can include proprietary source code or secrets from the workspace.

Mitigation: Disable file-content snapshots unless they are required, limit captured file sizes, and scan or redact exported content before sharing.

Risk: Recorded AI coding sessions can preserve prompts, responses, notes, and implementation details that were not intended for external audiences.

Mitigation: Use private exports for internal review, add only necessary annotations, and delete buildlogs that should no longer be available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/espetey/skills/buildlog)
- [Buildlog homepage](https://buildlog.ai)
- [Artifact-declared repository](https://github.com/buildlog/openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Text status messages, exported buildlog content, configuration snippets, and shareable links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recorded session exchanges, notes, chapter markers, and optional file-content snapshots depending on configuration.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
