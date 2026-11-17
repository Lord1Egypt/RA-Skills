## Description:

Bookmark intelligence for developers. Browse, search, triage, and manage your AI-analyzed library. Submit URLs, assign projects, trigger deep analysis, and execute staged items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonesvinyl](https://clawhub.ai/user/bonesvinyl)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to browse, search, submit, triage, and manage AI-analyzed bookmarks against coding projects, including staging high-value items and triggering deeper analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BKMRK API key and can read or modify the user's bookmark library.

Mitigation: Install only when that access is acceptable, and review bulk status changes such as trashing or staging before execution.

Risk: Submitted or synced bookmark content may be sent to Claude for analysis, including private pages, transcripts, secrets, or sensitive project metadata if the user submits them.

Mitigation: Do not submit confidential or sensitive content unless sharing it with BKMRK and Claude is acceptable.

## Reference(s):

- [BKMRK Homepage](https://bkmrkapp.com)
- [BKMRK Agent API Documentation](https://bkmrkapp.com/agent.json)
- [ClawHub Skill Listing](https://clawhub.ai/bonesvinyl/skills/bkmrk)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and modify a user's BKMRK bookmark library through authenticated API requests.]

## Skill Version(s):

1.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
