## Description:

Prefer explicit /firstwhy invocation. Without the command, activate only in three situations: a requirement too vague to act on, a design tradeoff that needs defensible justification, or the same problem returning after it was supposedly fixed. Drills down by asking why until the answer hardens into an unexamined assumption ("that's just how it's done"), splits that assumption into real constraints versus inherited habits, rebuilds the solution from the constraints alone, walks back up the chain to prove every layer is explained, then verifies the load-bearing assumption with the cheapest available evidence. Triggers: firstwhy, 5why, five whys, first principles, first-principles thinking, root cause, root cause analysis, why does this keep happening. Not for single reproducible crashes or test failures — route those to a debugging workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4444433333](https://clawhub.ai/user/h4444433333)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use FirstWhy to investigate recurring problems, clarify vague requirements, and justify design tradeoffs. It guides a bounded why-chain, separates constraints from inherited habits, and checks the load-bearing assumptions before treating a conclusion as established.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A coherent reasoning chain may be mistaken for a verified conclusion.

Mitigation: Keep consequential conclusions pending until each load-bearing assumption is checked against evidence.

Risk: Example workflows may suggest commands or persistent project changes.

Mitigation: Review proposed commands and lasting changes before applying them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/h4444433333/skills/firstwhy)
- [Server-resolved source repository](https://github.com/h4444433333/firstwhy)
- [Publisher profile](https://clawhub.ai/user/h4444433333)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with labeled reasoning chains, constraint and assumption lists, and a closed or pending status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence-based verification steps; conclusions remain pending until load-bearing assumptions are verified.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
