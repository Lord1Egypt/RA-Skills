## Description: <br>
Multi-perspective structured debate for complex topics that spawns parallel subagents with opposing stances, cross-injects arguments for rebuttal, then synthesizes a neutral consensus report with recommendations and a scenario matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caius-kong](https://clawhub.ai/user/caius-kong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and decision makers use this skill to compare complex technical or strategic options through structured opposing arguments, rebuttals, optional evidence audit, and a neutral recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debate topics and generated arguments may be processed by configured LLM providers. <br>
Mitigation: Avoid highly sensitive topics and use provider configurations appropriate for the data being discussed. <br>
Risk: Phase 1 uses web search, which can affect cost, latency, and exposure of topic details. <br>
Mitigation: Keep plan confirmation enabled so the user can review scope and expected subagent calls before execution. <br>
Risk: The skill can write a report when output_path is set. <br>
Mitigation: Set output_path only to a location where the user intends a report to be written. <br>


## Reference(s): <br>
- [Design Decisions](references/design-decisions.md) <br>
- [Prompt Templates](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown debate research report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be returned in conversation or written to output_path; reports can include completion status, evidence audit, recommendation, open questions, and scenario matrix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
