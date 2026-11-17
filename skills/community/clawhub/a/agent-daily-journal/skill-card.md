## Description:

Write a daily journal from the agent's own activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexhuiyi](https://clawhub.ai/user/alexhuiyi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents running in Hermes can turn their own activity into first-person daily journal entries, either manually or on a schedule. Users can check that each collected session is represented before keeping an entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable remote model endpoint may receive historical activity content; the security scan was partial.

Mitigation: Review the configured endpoint and its data handling before use, and avoid sending journal or activity content to a remote service unless that sharing is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexhuiyi/skills/agent-daily-journal)
- [Collector design](artifact/references/collector-design.md)
- [Writer and prompt](artifact/references/writer-and-prompt.md)
- [Deployment guide](artifact/references/deployment.md)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [First-person Markdown journal entries; the collector can also emit a JSON digest.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One entry per completed day window; the recommended character ceiling varies with the number of events.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
