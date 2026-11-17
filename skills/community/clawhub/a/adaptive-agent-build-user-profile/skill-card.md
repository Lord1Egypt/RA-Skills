## Description:

Build or update a user profile memory by observing workspace context, git history, and conversation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenorth-lj](https://clawhub.ai/user/truenorth-lj)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and developers use this skill to bootstrap or refresh a concise user profile from observable workspace signals. The profile helps future agent sessions tailor collaboration style, technical context, and communication preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect Git identities, repository history, configuration-like files, memory files, and documents before the user has clearly opted in.

Mitigation: Require explicit user approval before reading workspace or Git sources, and limit collection to the current workspace and stated profile-update purpose.

Risk: The skill saves inferred personal or work-style details into cross-session memory, which can persist incorrect or sensitive assumptions.

Mitigation: Show the proposed profile to the user before writing or indexing it, incorporate corrections immediately, and omit sensitive facts that are not needed for collaboration.

Risk: Git history and workspace files can expose personal identifiers such as names and email addresses.

Mitigation: Minimize or redact personal identifiers unless the user confirms they should be included in the profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/truenorth-lj/skills/adaptive-agent-build-user-profile)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown profile with YAML frontmatter, plus a conversational summary and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile guidance asks the agent to keep saved profile memory under 2KB and date current interests for staleness detection.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
