## Description:

Professional Web Intelligence & Automation Toolkit. Features Protocol Phantom (TLS/JA4), Local Socket Relaying, and Hardened physical gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biogod2020](https://clawhub.ai/user/biogod2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web automation users can use this skill for web search, web intelligence gathering, and controlled browser automation workflows. Its local browser-control utilities should be evaluated only in isolated test environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines ordinary web search with high-risk local browser-control features.

Mitigation: Evaluate it only in a disposable VM or container with no personal browser profile and no authenticated sessions.

Risk: Registry metadata understates the bundled high-risk browser-control capabilities.

Mitigation: Align the manifest with SKILL.md, declared dependencies, and autonomous invocation controls before publication or trusted use.

Risk: CDP takeover and relay paths can control a local browser session.

Mitigation: Expose Chrome DevTools only to a dedicated test browser, remove or strongly broker CDP takeover paths, and keep relay access constrained to loopback.

Risk: Wrapper path validation, dependency drift, or disabled browser sandboxing could expand local execution risk.

Mitigation: Fix wrapper path validation, pin dependencies, and keep Chromium sandboxing enabled before trusted use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biogod2020/skills/drission-sota-toolkit)
- [Publisher profile](https://clawhub.ai/user/biogod2020)
- [Skill definition](SKILL.md)
- [Security explanation](SECURITY_EXPLAINED.md)
- [Runtime requirements](requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON report files under an assets directory when bundled scripts are run.]

## Skill Version(s):

7.1.0 (source: server release and SKILL.md version line)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
