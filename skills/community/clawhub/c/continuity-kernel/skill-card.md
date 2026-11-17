## Description:

OpenClaw continuity kernel for fail-open llm_input injection, deterministic runtime contracts, and shadow-mode eval receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add bounded local continuity memory for OpenClaw agents, persist Soul Card and Mission Ticket state, and generate deterministic runtime and shadow-evaluation receipts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable local continuity memory can retain sensitive profile, preference, or mission data.

Mitigation: Keep the SQLite database path private and avoid storing secrets or highly sensitive personal data in continuity fields.

Risk: Injected continuity context could influence an agent if treated as higher-priority instruction text.

Mitigation: Treat continuity fields as untrusted context and ensure they cannot override system, developer, or other higher-priority instructions.

Risk: Synthetic shadow-evaluation receipts are useful for regression checks but are not equivalent to observed production traces.

Mitigation: Use trace-backed evaluation inputs when relying on results for release or deployment decisions.

## Reference(s):

- [ClawHub continuity-kernel release page](https://clawhub.ai/tkuehnl/skills/continuity-kernel)
- [CacheForge skills repository](https://github.com/cacheforge-ai/cacheforge-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code references, and JSON receipt paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite continuity state and machine-readable JSON evaluation or runtime proof receipts when its commands are run.]

## Skill Version(s):

0.2.0 (source: frontmatter and changelog, released 2026-02-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
