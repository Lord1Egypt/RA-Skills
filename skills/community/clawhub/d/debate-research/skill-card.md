## Description:

Runs a fixed-round, multi-perspective debate on complex topics and synthesizes the results into a consensus report with recommendations and a scenario matrix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caius-kong](https://clawhub.ai/user/caius-kong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and teams use this skill to compare complex options, examine opposing arguments, and produce a shareable Markdown report with a recommendation, open questions, and a scenario matrix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-injection or unreliable web content can influence Phase 1 research and later debate phases.

Mitigation: Verify important sources independently before relying on the final recommendation for consequential decisions.

Risk: Earlier agent outputs are reused in rebuttal and judgment phases, so unsupported claims can bias the final report.

Mitigation: Use the evidence audit for fact-dense topics and review low-quality or unsourced claims before acting on the report.

Risk: The documented install command uses the latest ClawHub installer version.

Mitigation: Pin the installer version when reproducible installation behavior is required.

## Reference(s):

- [Design Decisions](references/design-decisions.md)
- [Prompt Templates](references/prompts.md)
- [ClawHub Skill Page](https://clawhub.ai/caius-kong/skills/debate-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown debate research report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role-specific arguments, rebuttals, an optional evidence audit, neutral judgment, recommendations, open questions, and a scenario matrix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
