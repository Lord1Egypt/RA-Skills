## Description:

Send an idea to the Council of the Wise for multi-perspective feedback. Spawns sub-agents to analyze from multiple expert perspectives. Auto-discovers agent personas from agents/ folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External ClawHub and Clawdbot users use this skill to stress-test business ideas, project designs, content strategies, and major decisions through multiple agent perspectives. It returns synthesized feedback, disagreements, prioritized action items, and a confidence signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad invocation phrases may start a longer council review when the user intended a quick answer.

Mitigation: Use the skill for explicit council requests and prefer a direct agent response for quick questions, simple decisions, or time-sensitive tasks.

Risk: Council reports may include a promotional footer link.

Mitigation: Review generated reports before sharing externally and remove promotional footer text when it is not appropriate.

Risk: The skill auto-discovers local markdown personas from the agents folder.

Mitigation: Install or modify persona files only from trusted sources and review custom persona files before using them.

## Reference(s):

- [Council of the Wise ClawHub listing](https://clawhub.ai/jeffaf/skills/council-of-the-wise)
- [Publisher profile](https://clawhub.ai/user/jeffaf)
- [Daniel Miessler](https://danielmiessler.com/)
- [Council self-review](docs/council-self-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with synthesis, perspective sections, action items, and confidence signal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include follow-up guidance for a single council member; normal runs can take 2-5 minutes and use a 5-minute timeout.]

## Skill Version(s):

1.4.0 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
