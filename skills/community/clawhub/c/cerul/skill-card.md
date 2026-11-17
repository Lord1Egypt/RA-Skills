## Description:

Cerul lets agents search video by meaning across speech, visuals, and on-screen text to answer questions with video evidence and timestamped citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessytsui](https://clawhub.ai/user/jessytsui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search video content for statements, presentations, visual context, and timestamped source links when answering questions about talks, podcasts, interviews, and conference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install the Cerul CLI using an unverified remote curl-to-bash command.

Mitigation: Review the installer before use and prefer a pinned, verifiable Cerul CLI installation method.

Risk: The skill directs agents to persist a Cerul API key on disk.

Mitigation: Use a session-scoped or platform-managed CERUL_API_KEY and avoid printing or persisting credentials in ~/.config/cerul/credentials unless the deployment policy allows it.

## Reference(s):

- [Cerul Homepage](https://github.com/cerul-ai/cerul)
- [Cerul CLI Repository](https://github.com/cerul-ai/cerul-cli)
- [Cerul Python SDK](https://pypi.org/project/cerul/)
- [Cerul TypeScript SDK](https://www.npmjs.com/package/cerul)
- [Cerul Documentation](https://cerul.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with CLI commands, timestamped citations, and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact agent-oriented CLI output and requires CERUL_API_KEY for authenticated searches.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
