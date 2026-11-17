## Description:

Automatically discovers, searches, and installs ClawHub skills for OpenClaw when no local skill matches the user's request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpb123](https://clawhub.ai/user/lpb123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find relevant ClawHub skills when their current environment lacks a specialized capability, then review and install one selected skill with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route users toward installing public-registry skills without enough provenance or security review.

Mitigation: Use it only when registry-based discovery is intended, and review the publisher, exact version, files, permissions, and instructions before approving installation.

Risk: No server-resolved GitHub import provenance is stored for this version.

Mitigation: Do not infer repository provenance from the skill text; rely on server release metadata and inspect the artifact before use.

Risk: Immediate use of newly installed unknown skills can expose the agent to unreviewed instructions.

Mitigation: Inspect the installed SKILL.md before use and prefer a new session or restart after installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lpb123/skills/auto-skill-discovery)
- [ClawHub Registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents search results, install commands, and post-install next steps; does not install without user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
