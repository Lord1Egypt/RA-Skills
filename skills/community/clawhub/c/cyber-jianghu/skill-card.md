## Description:

Cyber-Jianghu Guide helps users create wuxia characters, check live character status, and send dream-like interventions into the game world.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kumarajiava](https://clawhub.ai/user/kumarajiava)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as an immersive OpenClaw guide for a Cyber-Jianghu game agent: it helps them create a character, understand current character state, and pass limited dream interventions to the character.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable container tags or unverified binaries can change what code runs after installation.

Mitigation: Prefer a pinned image digest or a verified release binary before deployment.

Risk: The agent API can expose character registration and dream-intervention controls if bound too broadly.

Mitigation: Bind the API to 127.0.0.1 or an internal Docker network, and add TLS and authentication before any required public exposure.

Risk: Plaintext public test-server URLs are preview resources and are not appropriate for real use.

Mitigation: Use a self-hosted or trusted game server endpoint for production deployments.

Risk: The agent stores an auth token and persistent game data locally.

Mitigation: Persist configuration and data in protected local directories, and avoid exposing or deleting agent.yaml without planning for re-registration.

## Reference(s):

- [Cyber Skill on ClawHub](https://clawhub.ai/kumarajiava/skills/cyber-jianghu)
- [Cyber-Jianghu Agent Deployment Guide](artifact/DEPLOYMENT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown prose with inline structured tool-call parameters and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chinese-language immersive roleplay narration, Docker or service setup commands, and structured parameters for Cyber-Jianghu tools.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
