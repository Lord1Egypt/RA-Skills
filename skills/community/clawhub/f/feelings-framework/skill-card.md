## Description:

Provides OpenClaw agents with persistent emotional states, tracking mood and feelings over time to influence response tone and behavior consistently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blaspat](https://clawhub.ai/user/blaspat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building OpenClaw or other AI agents can use this skill to add persistent mood state, calibrated emotional triggers, and response modifiers that shape tone across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent mood data can reveal interaction-derived emotional history if stored in a readable JSON file or browser localStorage.

Mitigation: Decide the storage location, access controls, retention policy, and reset or deletion workflow before enabling persistent state for an agent.

Risk: A registry package that differs from the reviewed artifact could change the behavior an agent runs.

Mitigation: Install from the bundled reviewed source or a verified exact package version.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blaspat/skills/feelings-framework)
- [README](README.md)
- [Framework Specification](CORE.md)
- [OpenClaw Integration Example](examples/openclaw/claire_feelings.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JavaScript code examples, JSON state data, and response modifier dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist mood state to a JSON file or browser localStorage, depending on the selected memory implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata, pyproject.toml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
