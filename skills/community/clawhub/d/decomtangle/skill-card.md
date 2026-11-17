## Description:

Decomtangle teaches OpenClaw-style agents to execute multi-step procedures as atomic tool calls, observing each result before choosing the next action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-vaughan](https://clawhub.ai/user/jason-vaughan)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and external agent builders use this skill to prevent silent stalls, opaque parser failures, and unsafe retries during browser automation, API sequences, migrations, and other stateful tool workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages more, smaller tool calls, which can increase call count during stateful workflows.

Mitigation: Apply it to multi-step or stateful procedures, keep genuinely one-step actions as single calls, and use targeted reads to keep each result small.

Risk: Adapting the curl and eval examples could expose bearer tokens or send requests to an untrusted bridge endpoint.

Mitigation: Use only trusted local bridge endpoints, avoid exposing bearer tokens, and prefer safer native tool endpoints when available.

Risk: Side effects can be reported as complete before the live system confirms them.

Mitigation: Treat side-effecting calls as attempted until a fresh observation confirms the resulting state, and avoid automatic retries from an unknown state.

## Reference(s):

- [Decomtangle ClawHub release page](https://clawhub.ai/jason-vaughan/skills/decomtangle)
- [SKILL.md](SKILL.md)
- [Decomposition heuristics](references/decomposition-heuristics.md)
- [Atomic-call checklist](references/atomic-call-checklist.md)
- [Bad mega-script stall example](examples/bad-mega-script-stall.md)
- [Good multicalendar atomic example](examples/good-multicalendar-atomic.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with example tool calls and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Doctrine-only; changes tool-call sequencing and verification behavior, and does not install tools or execute code by itself.]

## Skill Version(s):

0.1.2 (source: server release metadata; release changelog says content is identical to 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
