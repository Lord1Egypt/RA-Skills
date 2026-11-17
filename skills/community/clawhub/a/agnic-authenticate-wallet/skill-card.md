## Description:

Authenticates an Agnic wallet through browser OAuth or a headless API token for CLI and agent environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to authenticate an Agnic wallet, verify authentication status, configure API-token based headless access, run browser OAuth login, or resolve not-authenticated CLI errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm CLI while handling wallet credentials.

Mitigation: Use a pinned, reviewed Agnic CLI version and install only when the Agnic npm package and publisher are trusted.

Risk: API tokens can be exposed through command lines, shell history, or agent-visible transcripts.

Mitigation: Prefer protected environment variables or a secret manager, avoid inline token flags for real credentials, keep token scopes and spending limits tight, and revoke or log out when access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/skills/agnic-authenticate-wallet)
- [Agnic App API Tokens](https://app.agnic.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers browser OAuth, AGNIC_TOKEN, --token authentication, status checks, token storage, and logout.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
