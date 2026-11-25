## Description:

Provides advisory guidance for designing AI agent evaluations, interpreting benchmarks, comparing frameworks, and drafting evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

AI engineers, ML teams, product managers, and QA engineers use the skill to design evaluation suites, interpret benchmark results, compare agent frameworks, analyze failures, and draft reports. Its guidance is advisory and does not execute agents or approve releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign but has medium confidence because inspection was incomplete and some static checks were degraded.

Mitigation: Treat the clean verdict as limited assurance; review the skill and consider the stated inspection uncertainty before installing.

Risk: Illustrative thresholds, benchmark comparisons, and generated go/no-go drafts could be mistaken for validated release decisions.

Mitigation: Calibrate criteria to the target use case and have qualified ML and security reviewers assess results before release decisions.

Risk: Agent logs or transcripts supplied for analysis may contain personal, customer, or regulated information.

Mitigation: Share only necessary, anonymized material and remove credentials, identifying details, and regulated data.

Risk: Red-team test ideas could be misapplied to systems without authorization.

Mitigation: Use defensive probes only on systems the user owns or is authorized to test, in a controlled environment.

## Reference(s):

- [AI Agent Evaluator on ClawHub](https://clawhub.ai/gechengling/skills/ai-agent-evaluator)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Conversational text with Markdown tables, scorecards, checklists, and report drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory drafts for human review; does not run agents, execute code, call APIs, access systems, or save files.]

## Skill Version(s):

3.0.6 (source: artifact/SKILL.md frontmatter, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
