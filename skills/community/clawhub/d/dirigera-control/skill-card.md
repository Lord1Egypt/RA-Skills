## Description:

Control IKEA Dirigera smart home devices, check device status, run light, outlet, and scene actions, and help find hub IP addresses or generate API tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[falderebet](https://clawhub.ai/user/falderebet)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate an IKEA Dirigera smart home through an agent, including status checks, light and outlet control, scene triggering, battery reports, hub IP discovery, and token setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control smart-home devices, including outlets, scenes, and whole-home actions.

Mitigation: Require explicit user confirmation before outlet, scene, or broad shutdown actions, and confirm target rooms or devices before sending commands.

Risk: Dirigera API tokens are smart-home credentials that could allow device control if exposed.

Mitigation: Store tokens only in protected secret storage or private local files, avoid shared or synced folders, and do not display tokens in normal responses.

Risk: Token generation disables TLS certificate checks while contacting the hub.

Mitigation: Run token generation only on trusted local networks and avoid using the token workflow on untrusted or shared networks.

## Reference(s):

- [Dirigera API Complete Reference](references/api.md)
- [Common Usage Patterns](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/falderebet/skills/dirigera-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local script invocations, configuration steps, status summaries, and smart-home control code using a Dirigera token.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
