## Description:

Analyzes AI agent decision logs to find reasoning errors and suggest fixes to enhance performance and reduce hallucinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to analyze AI agent trace logs, identify repeated reasoning loops, possible unsupported claims, and inefficient tool routing, and generate suggested patches for future agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input logs, knowledge-base files, and generated reports may contain sensitive prompt, thought, observation, or knowledge content.

Mitigation: Run the tool only on files appropriate for local analysis, restrict access to generated reports, and scrub sensitive content before sharing outputs.

Risk: Patch suggestions are heuristic recommendations and may not be appropriate for every agent workflow.

Mitigation: Review suggested patches before applying them to production agents or automated decision flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/agent-reflect-engine)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Text]

**Output Format:** [JSON report with optional plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include detected issues, timestamps, total log entries, and patch suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
