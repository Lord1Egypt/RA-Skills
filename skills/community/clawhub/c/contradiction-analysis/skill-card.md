## Description: <br>
Trigger when a problem contains competing forces, unclear priorities, or no obvious entry point; use this skill to identify contradictions, isolate the principal contradiction, classify its nature, and choose the right response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arg0](https://clawhub.ai/user/arg0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and teams use this skill to analyze complex trade-offs, unclear priorities, bottlenecks, root causes, or competing constraints before choosing a response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the agent to apply this analysis framework when another approach would be more suitable. <br>
Mitigation: Be explicit when you do not want contradiction analysis used for a task, and review outputs for fit before acting on them. <br>
Risk: The artifact content is Chinese-first and may shape terminology or framing in generated analysis. <br>
Mitigation: Specify the desired output language and terminology when using the skill in English or multilingual workflows. <br>
Risk: The skill produces reasoning guidance and classification judgments that can be incomplete or misleading if the input facts are weak. <br>
Mitigation: Validate the identified contradictions, priorities, and proposed response against current evidence before making decisions. <br>


## Reference(s): <br>
- [Contradiction Analysis ClawHub Page](https://clawhub.ai/arg0/contradiction-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/arg0) <br>
- [contradiction-mapper-prompt.md](artifact/contradiction-mapper-prompt.md) <br>
- [contradiction-types-reference.md](artifact/contradiction-types-reference.md) <br>
- [original-texts.md](artifact/original-texts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis report, tables, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May classify contradictions, identify the principal contradiction, and flag transition risks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
