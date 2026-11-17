## Description:

Framework Analysis guides an agent through Qian Xuesen-inspired structural framework analysis for geopolitical conflicts, international crises, historical events, and other complex systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydearzsy](https://clawhub.ai/user/mydearzsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured terminal-deduction reports that identify hard constraints, verified facts, causal chains, a single conclusion, and falsifiable predictions. It is intended for requests that explicitly ask for framework-method analysis rather than broad, open-ended analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs automatic execution of a local Markdown-to-PDF converter.

Mitigation: Review the converter path and generated Markdown before running the conversion, and run only trusted local scripts.

Risk: The skill directs automatic sending of generated reports to Feishu without a clear approval step.

Mitigation: Require explicit confirmation of the output path, recipient, and file contents before any send action.

Risk: The workflow can delegate research on current events and produce strong single-outcome conclusions.

Mitigation: Check cited sources, distinguish verified facts from claims, and treat falsifiable predictions as analysis rather than settled fact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mydearzsy/skills/framework-analysis)
- [Publisher Profile](https://clawhub.ai/user/mydearzsy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report with optional PDF file generation and Feishu delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to create a structured report, convert it to PDF when possible, and send the report through Feishu.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
