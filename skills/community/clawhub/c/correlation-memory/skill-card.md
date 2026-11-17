## Description:

Correlation-aware memory search plugin for OpenClaw that retrieves related decision contexts from user-defined correlation rules when memory is queried.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ether-btc](https://clawhub.ai/user/ether-btc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to enrich memory search with correlated context names, confidence-filtered rule matches, and debug output for rule tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and dependency metadata may not be reproducible enough for a local-only security claim.

Mitigation: Install from a pinned tag or commit, regenerate the lockfile with npm ci, and review the OpenClaw dependency graph before enabling the plugin.

Risk: Broad or poorly tuned correlation rules can surface sensitive or irrelevant memory context names too often.

Mitigation: Keep rule keywords specific, use confidence thresholds and lifecycle states, and verify behavior with the correlation_check debug tool before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ether-btc/skills/correlation-memory)
- [README](artifact/README.md)
- [Deployment Guide](artifact/docs/deployment.md)
- [Production Guide](artifact/docs/production-guide.md)
- [Research Background](artifact/docs/research.md)
- [Example Correlation Rules](artifact/correlation-rules.example.json)
- [OpenClaw](https://openclaw.dev)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns matched rule metadata, suggested additional memory searches, summaries, and debug information; result counts are limited by max_results.]

## Skill Version(s):

2.1.0 (source: CHANGELOG, package.json, OpenClaw plugin manifest, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
