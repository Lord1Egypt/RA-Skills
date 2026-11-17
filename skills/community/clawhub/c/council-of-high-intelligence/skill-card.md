## Description:

Convene the Council of High Intelligence - multi-persona deliberation with historical thinkers for deeper analysis of complex problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnyk](https://clawhub.ai/user/0xnyk)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to convene multiple historical thinker personas for structured analysis of complex decisions, technical questions, strategy, ethics, product, and risk. It selects a triad, full council, or custom members, then synthesizes a Council Verdict with consensus, dissent, unresolved questions, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Council personas may have broad local file, shell, and outbound web access when installed.

Mitigation: Install only in workspaces where that access is acceptable, prefer a sandboxed workspace, and remove Bash, WebSearch, and WebFetch permissions from personas that do not need them.

Risk: Council Verdicts are deliberative recommendations and may contain incorrect, incomplete, or misleading guidance.

Mitigation: Treat outputs as decision support, verify important claims independently, and require human review before acting on high-impact security, legal, financial, or operational recommendations.

## Reference(s):

- [Council skill page](https://clawhub.ai/0xnyk/skills/council-of-high-intelligence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Council Verdict with problem statement, council composition, consensus position, member insights, agreements, disagreements, minority report, unresolved questions, and recommended next steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
