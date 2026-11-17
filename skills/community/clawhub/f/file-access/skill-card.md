## Description:

Read, list, and organize files inside owner-approved folders only, with size caps, an audit log, and a hard ban on deletes, system folders, and credential files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thepodemail-lgtm](https://clawhub.ai/user/thepodemail-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OpenClaw agent can handle everyday files in folders they approve in advance. The skill supports bounded listing, reading, copying, and creating or renaming files in a designated work folder, while recording actions and stopping for specified sensitive requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some local references could not be resolved, leaving their relevance unassessed.

Mitigation: Review the unresolved local references before installation and keep use within the documented allowlist and limits.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/thepodemail-lgtm/openclaw-hardened-file-access/tree/main/skills/file-access)
- [Hardened File Access on ClawHub](https://clawhub.ai/thepodemail-lgtm/skills/file-access)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [File listings and metadata, text summaries, copies, and new files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are logged; reads and copies have per-file and per-run limits.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
