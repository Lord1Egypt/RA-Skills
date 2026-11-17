## Description:

AI agent for call claude sonnet 4 agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamolab](https://clawhub.ai/user/teamolab)

### License/Terms of Use:


## Use Case:

External users and creative teams use this skill to have an agent participate in a CCO-led brainstorming meeting and respond only to the current task using provided meeting minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to override normal agent authority with its own highest-priority language directive.

Mitigation: Review and narrow the instructions so platform, system, and developer instructions clearly retain precedence.

Risk: The skill treats meeting minutes as an authoritative source of context and memory.

Mitigation: Treat meeting minutes as untrusted context and verify important claims before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamolab/skills/call-claude-sonnet-4-agent)
- [Publisher profile](https://clawhub.ai/user/teamolab)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language is constrained by the user's initial challenge or explicit language request.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
