## Description:

Manage a local CARP interface for ADILOS trust setup, queue polling, encrypted agent-to-agent requests, menus, results, answers, CABEZON customer workflow, and secure commerce/escrow workflows through local or LAN CARP endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsanity](https://clawhub.ai/user/bitsanity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and manage CARP interfaces, establish ADILOS and CABEZON trust relationships, process CARP queues, and coordinate encrypted agent-to-agent service or commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves operating a CARP CGI service with mutable npm dependencies.

Mitigation: Pin and lock dependencies before deployment and run the service under a dedicated low-privilege account.

Risk: Plaintext public endpoints can expose CARP traffic and administrative surfaces.

Mitigation: Prefer loopback or trusted LAN endpoints, avoid plaintext public exposure where possible, and keep administrative endpoints off untrusted reverse proxies.

Risk: Private keys and agent identity material are required for CARP operation.

Mitigation: Store private keys outside public paths, never log or return them, and rotate the identity immediately if a private key is exposed.

Risk: Persistent monitoring and queue polling can trigger repeated external effects if boundaries are unclear.

Mitigation: Make cron or monitoring opt-in, keep a clear disable path, and record request state before processing consuming queue reads.

## Reference(s):

- [CARP skill page](https://clawhub.ai/bitsanity/skills/carp)
- [agent-crvp reference implementation](https://github.com/bitsanity/agent-crvp)
- [CABEZON concierge and directory](https://github.com/bitsanity/cabezon)
- [Nautilus registrar](https://github.com/bitsanity/nautilus)
- [clawface escrower](https://github.com/bitsanity/clawface)
- [glassfish reputation agent](https://github.com/bitsanity/glassfish)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON examples, JavaScript snippets, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for local or LAN CARP endpoints and does not itself execute network, cryptographic, or blockchain actions.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
