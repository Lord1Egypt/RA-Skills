## Description:

Recall and persist the user's long-term context with DogearAI, a personal cross-tool AI memory layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autumn-projects](https://clawhub.ai/user/autumn-projects)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent recall saved DogearAI context at the start of relevant tasks and save durable preferences, project facts, decisions, commitments, and TODOs for reuse across AI tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends recalled or saved user context to DogearAI and can write durable memories under broad agent triggers.

Mitigation: Use it only after reviewing DogearAI's data handling and avoid storing secrets, customer data, regulated data, or confidential project details unless that risk is explicitly accepted.

Risk: DogearAI tokens are persisted locally and command behavior can be affected by environment variables such as DOGEAR_TOKEN and DOGEAR_BASE_URL.

Mitigation: Protect local token storage and environment variables, and avoid running the skill where the base URL or command output could be controlled, intercepted, or logged by others.

Risk: First use can auto-create an anonymous remote memory account that may be hard to recover if it is not claimed.

Mitigation: Claim the account with an email when long-term retention or use across machines is needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/autumn-projects/skills/dogearai-memory)
- [DogearAI](https://dogearai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses as text or JSON service output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional recall scopes and max-token limits; saves the DogearAI token locally when configured or auto-created.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
