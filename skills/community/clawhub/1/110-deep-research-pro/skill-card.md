## Description:

110 Deep Research Pro is a multi-source research skill that searches the web, synthesizes findings, and delivers cited reports without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run multi-source web research, evaluate source credibility and recency, and produce cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make unrestricted external web requests and fetch arbitrary pages during research.

Mitigation: Run it in a sandboxed environment where page fetches cannot reach internal services or sensitive metadata endpoints; add URL validation or a safer fetch helper before use.

Risk: Research output can be incomplete or misleading when sources are weak, stale, or single-sourced.

Mitigation: Review cited sources, prefer reputable and recent sources, and clearly flag unsupported or single-source claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/110-deep-research-pro)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [uv](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with citations, optional JSON, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local research reports; no paid API keys are required.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
