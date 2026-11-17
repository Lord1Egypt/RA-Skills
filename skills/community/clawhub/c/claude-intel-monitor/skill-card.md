## Description:

Detect intelligence degradation in Claude, GPT, and DeepSeek using 30 standardized Chinese benchmark questions across Math, Reasoning, and Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to benchmark Claude, GPT, and DeepSeek models against fixed Chinese math, reasoning, and code questions, compare results with historical baselines, and identify possible model quality degradation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports provider API key handling and recurring external calls with under-disclosed endpoint and persistence risks.

Mitigation: Use an isolated environment, limited-scope API keys, trusted endpoints, cost limits, and a clear stop and cleanup plan before enabling watch or cron mode.

Risk: The security verdict is suspicious for this release.

Mitigation: Review carefully before installing and prefer a pinned, audited package version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/claude-intel-monitor)
- [Project homepage](https://github.com/minirr890112-byte/claude-intel-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with command examples and benchmark result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference provider API keys, recurring watch mode, and local benchmark history.]

## Skill Version(s):

1.1.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
