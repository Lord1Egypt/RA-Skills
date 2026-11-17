## Description:

CNexus 2.0 is a local-first personal cognitive OS prototype for running a six-step cognitive loop with memory, reflection, local model support, code projection, and observability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plusunm](https://clawhub.ai/user/plusunm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically skilled users use this skill to run and inspect a local personal second-brain runtime that records conversations, evolves memory state, and exposes dashboards, traces, tests, and audit tools for experimentation and daily use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local APIs and model configuration can expose personal memory and prompts too broadly.

Mitigation: Require an auth token, bind to local trusted interfaces only, remove wildcard CORS, and avoid running the server while browsing untrusted sites.

Risk: Configured cloud model providers may receive personal text or memory context.

Mitigation: Restrict allowed provider URLs and leave cloud API keys unset until users understand what data may be sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plusunm/skills/cnexus2-cognitive-os)
- [README](artifact/README.md)
- [Runtime specification](artifact/01_runtime_spec/01_loop_execution.md)
- [Stability specification](artifact/02_stability_spec/01_drift_detection.md)
- [Security evidence](evidence.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, code/configuration edits, shell commands, and JSON or text runtime responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide a local HTTP runtime that stores personal memory and can call local or configured cloud model providers.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
