## Description:

Web automation toolkit that provides a gated arXiv search script and a local TCP relay for browser-control workflows.

This skill is for research and development only.

## Publisher:

[biogod2020](https://clawhub.ai/user/biogod2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run a guarded search helper and, when intentionally enabled, a local relay for browser debugging or automation workflows. The bundled evidence states it is for authorized educational research and isolated sandbox use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local TCP relay can expose access to a sensitive browser-control port.

Mitigation: Run only in an isolated environment and start the relay only when local forwarding to the browser debugging port is intentionally required.

Risk: The package overstates its safety controls and should not be trusted solely because it advertises human gating.

Mitigation: Review and scan the package before installation, and enforce independent sandboxing and approval controls outside the skill.

Risk: The server security verdict is suspicious.

Mitigation: Avoid deploying this skill in production or sensitive environments without a security review and explicit acceptance of the relay behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biogod2020/skills/drission-agent)
- [Publisher profile](https://clawhub.ai/user/biogod2020)
- [arXiv search endpoint used by main_engine.py](https://arxiv.org/search/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance, Python scripts, shell commands, and generated JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit environment gating before bundled scripts execute; the relay listens locally and forwards to a browser debugging port when run.]

## Skill Version(s):

2.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
