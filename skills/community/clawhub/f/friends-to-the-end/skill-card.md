## Description:

Helps Hermes agents, profiles, and app-embedded agents coordinate structured handoffs, context sharing, verification, and cross-agent collaboration when another Hermes instance should participate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newsense2004](https://clawhub.ai/user/newsense2004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let Hermes-capable profiles or embedded app agents call on another profile for tool access, fallback reasoning, or cross-system workflows while preserving compact prompts and verifiable results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile cloning can duplicate credentials or broader access than the receiving agent needs.

Mitigation: Use clean, least-privilege dedicated profiles instead of `--clone-all` when real credentials are present, and share only the context needed for the handoff.

Risk: Service environment inspection can expose secrets in logs or chat transcripts.

Mitigation: Avoid printing full service environments; inspect only required keys or redact secret values before sharing.

Risk: Agent handoffs or service restarts can create side effects that are reported before they are verified.

Mitigation: Require explicit confirmation before handoffs or restarts, then verify results through files, health checks, APIs, or logs before reporting success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newsense2004/skills/friends-to-the-end)
- [Publisher profile](https://clawhub.ai/user/newsense2004)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on structured handoff prompts, verification checklists, and profile hygiene practices.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
