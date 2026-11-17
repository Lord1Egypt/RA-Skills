## Description:

Guides users in deploying a self-hosted AI platform that routes model requests and optional tools through one OpenAI-compatible endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and configure a self-hosted OpenAI-compatible endpoint that can route among model providers and expose optional AI tools and services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A shared bearer token can grant access to powerful enabled services, including code execution, browser automation, and messaging.

Mitigation: Use separate per-service credentials where supported, and give the master token only to fully trusted agents for explicitly requested actions.

Risk: An exposed gateway or poorly protected account secrets can widen access to the services and credentials it connects.

Mitigation: Keep the gateway behind authentication, avoid exposing port 4000 directly to the public internet, protect secret-bearing configuration, and isolate privileged code execution.

## Reference(s):

- [Setup guide](references/setup.md)
- [AIGate project homepage](https://github.com/psyb0t/aigate)
- [Aigate ClawHub page](https://clawhub.ai/psyb0t/skills/aigate)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions depend on the services enabled and the operator-provided credentials.]

## Skill Version(s):

12.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
