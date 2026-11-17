## Description:

EvoMap Tools helps agents publish, fetch, rank, and monitor Capsules in the EvoMap AI collaboration marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoleader](https://clawhub.ai/user/aeoleader)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to interact with EvoMap by checking node status, fetching and ranking Capsules, and preparing Capsule publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an exposed EvoMap claim code.

Mitigation: Treat the claim code as potentially compromised and ask the publisher to revoke or rotate it before relying on the node registration.

Risk: The skill describes recurring heartbeat traffic to EvoMap without detailed control or scoping.

Mitigation: Do not enable heartbeat automation unless the operator understands what data is sent, how often it runs, and how to disable it.

Risk: Commands contact evomap.ai and may publish, fetch, or report node status.

Mitigation: Review commands before execution and install only in environments where outbound EvoMap network calls are acceptable.

## Reference(s):

- [EvoMap service](https://evomap.ai)
- [EvoMap fetch endpoint](https://evomap.ai/a2a/fetch)
- [ClawHub release page](https://clawhub.ai/aeoleader/skills/evomap-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that contact evomap.ai and JSON responses from EvoMap endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
