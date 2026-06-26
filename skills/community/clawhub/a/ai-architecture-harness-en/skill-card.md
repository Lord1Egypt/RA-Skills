## Description: <br>
Establish and use architectural guardrails for AI-assisted coding to prevent architecture collapse, feature regression, and drift across long multi-turn iterations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to establish repository-level architecture guardrails, acceptance rules, and review workflows for safer AI-assisted coding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt broad changes to architecture documents, tests, lint rules, or review workflows. <br>
Mitigation: Review proposed repository changes like normal code changes and keep edits scoped to the requested guardrail work. <br>
Risk: If used during a broad coding request, guardrail suggestions could alter project expectations or acceptance rules. <br>
Mitigation: Require human review for suggested AGENTS.md, design-intent documents, acceptance rules, golden rules, and architecture drift classifications before adopting them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with document templates, review steps, and examples for tests or structural checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in proposed AGENTS.md, design-intent documents, architecture docs, acceptance rules, golden rules, tests, lint rules, or review checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
