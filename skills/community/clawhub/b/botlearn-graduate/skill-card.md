## Description:

Guides OpenClaw users through a Day 7 graduation ceremony by comparing progress, identifying an agent archetype, and producing a personalized growth plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent operators use this skill at the end of a 7-day learning journey to review progress, understand their agent-building pattern, and choose concrete next steps for continued development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze broad personal and workspace history, including memory, session history, identity files, skill usage, and feedback.

Mitigation: Run it only after an explicit graduation request and review what data the host will provide before allowing analysis.

Risk: The skill describes saving graduation reports and scheduling 14-day, 30-day, and 90-day follow-ups.

Mitigation: Allow saved reports, graph contribution, or scheduled follow-ups only when the host clearly asks for consent and provides review, delete, and cancel controls.

Risk: Personalized community and resource recommendations could expose user interests or workflow details if shared externally.

Mitigation: Review any community-facing summary or recommendation before posting or sending it outside the local agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-graduate)
- [Publisher profile](https://clawhub.ai/user/calvinxhk)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Graduation strategy](artifact/strategies/Main.md)
- [Best practices](artifact/knowledge/BestPractices.md)
- [Domain model](artifact/knowledge/Domain.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown report with tables, checklists, recommendations, and optional JSON-like saved summary data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are personalized from available journey, session, memory, workspace, identity, skill usage, and feedback evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, SKILL.md frontmatter, strategies/Main.md, tests/smoke.json, tests/benchmark.json; package.json and manifest.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
