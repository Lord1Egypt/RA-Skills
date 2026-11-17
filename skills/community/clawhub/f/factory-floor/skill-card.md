## Description:

Startup coach for founders and early-stage teams that diagnoses the current startup constraint and assigns a focused weekly experiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmichelli](https://clawhub.ai/user/mmichelli)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and early-stage teams use this skill to clarify what to focus on, identify bottlenecks in growth or execution, and turn the diagnosis into a one-week experiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer automatically runs an npm dependency install for diagram rendering, creating avoidable supply-chain execution risk.

Mitigation: Prefer a controlled ClawHub install flow, pin package versions when using npx, and review the diagram renderer dependency before setup.

Risk: Startup coaching guidance can be misapplied when the founder provides incomplete or inaccurate business context.

Mitigation: Use the skill's intake and funnel-break scan to establish context before acting on diagnoses or weekly experiments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmichelli/skills/factory-floor)
- [npm package](https://www.npmjs.com/package/@swiftner/factory-floor)
- [Open Agent Skills standard](https://agentskills.io)
- [Intake](references/intake.md)
- [Common Misdiagnoses](references/misdiagnoses.md)
- [Coaching Patterns](references/coaching-patterns.md)
- [Theory of Constraints reference](references/pillar-goldratt.md)
- [Customer Factory reference](references/pillar-maurya.md)
- [Mental and Physical Availability reference](references/pillar-sharp.md)
- [Marketing Strategy Discipline reference](references/pillar-ritson.md)
- [Jobs To Be Done reference](references/jtbd.md)
- [Strategic Thinking reference](references/pillar-strategy.md)
- [Estimation reference](references/estimation.md)
- [Weekly Review](references/weekly-review.md)
- [Weekly Review Diagram](references/weekly-diagrams.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown responses with diagnostic questions, constraint statements, weekly experiments, and occasional shell commands for installation or diagram rendering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route to stage-specific or reference material based on startup context]

## Skill Version(s):

3.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
