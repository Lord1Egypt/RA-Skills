## Description:

Let the fly decide between tasks or PRs in Chrome; watch, veto, then Accept & start the chosen work in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grahammcbain](https://clawhub.ai/user/grahammcbain)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to present a small set of actionable tasks, watch a browser-based fly simulation choose one, veto unwanted picks, and accept only the selected task into the owning conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required companion plugin is unpinned and can interact with authenticated OpenClaw sessions.

Mitigation: Review the companion plugin listing, publisher, requested capabilities, and preferably an exact version or digest before installation.

Risk: The browser bootstrap URL grants private access to the local Gateway pairing flow.

Mitigation: Treat the bootstrap URL as private, avoid printing or sharing it, and do not weaken Gateway authentication.

Risk: Accepting a pick sends the selected task into the current OpenClaw conversation.

Mitigation: Only the human should click Accept & start, and only after confirming the selected work should be sent to the owning conversation.

Risk: An uncertain handoff could lead to duplicate or unintended task dispatch if retried blindly.

Mitigation: Check the conversation and round status before any manual retry after an uncertain handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grahammcbain/skills/fly-coworker)
- [Companion setup and verification](plugin-install.md)
- [Scope and limitations](docs/SCOPE.md)
- [Browser launch procedure](references/browser-launch.md)
- [Third-party notices](THIRD_PARTY.md)
- [FlyGym / NeuroMechFly](https://github.com/NeLy-EPFL/flygym)
- [MaleCNS](https://male-cns.janelia.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser workflow steps and handoff/status guidance; it does not itself complete the selected downstream task.]

## Skill Version(s):

0.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
