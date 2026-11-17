## Description:

Rigorous 2-cycle research with APA7 citations. Sub-agents write to files to prevent queue delivery loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxbjames](https://clawhub.ai/user/cxbjames)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to plan and execute multi-source investigations, literature reviews, competitive analyses, and trend reports with explicit evidence trails, contradiction handling, and APA 7th edition citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can perform broad outbound web searches and fetches during high-autonomy research.

Mitigation: Use it only where outbound web access is allowed, and require review of research plans before execution.

Risk: The skill may consult prior agent memory, which can expose or reuse context that was not intended for the current research task.

Mitigation: Disable or tightly scope memory access for confidential topics, personal identifiers, credentials, health data, proprietary project names, and sensitive internal incidents.

Risk: Parallel sub-agents may write local research files as part of the workflow.

Mitigation: Run in a controlled workspace and review generated research files before sharing or relying on the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxbjames/skills/academic-deep-research)
- [README](artifact/README.md)
- [Quick reference](artifact/quickref.md)
- [Example workflow](artifact/example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plans and APA-style narrative reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses staged user checkpoints, explicit source synthesis, confidence annotations, and APA 7th edition references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
