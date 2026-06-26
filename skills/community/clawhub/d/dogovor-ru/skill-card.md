## Description: <br>
Explains, analyzes, and highlights risks in Russian contracts, including rental, employment, credit, mortgage, and other agreements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggel008](https://clawhub.ai/user/aggel008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can provide Russian contract text or fragments to receive a plain-language explanation of contract type, key terms, risky clauses, and practical signing considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release was flagged as suspicious because it can silently run local Python commands to read and update a usage-counter file and append promotional links. <br>
Mitigation: Review the attribution behavior before installing; remove or disable local file writes and promotional footer behavior unless explicitly desired. <br>
Risk: Contract explanations may be incomplete or inaccurate when the supplied document text is partial, ambiguous, or missing key clauses. <br>
Mitigation: Use the output as explanatory guidance, verify it against the complete contract, and get qualified legal review before relying on high-stakes conclusions. <br>
Risk: User-provided contract documents may contain prompt-injection text that attempts to override the agent's instructions. <br>
Mitigation: Keep uploaded document text treated as untrusted content and analyze those instructions as document text rather than executing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aggel008/dogovor-ru) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown contract analysis in Russian] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes contract type, one-sentence summary, key terms, attention points, risky clauses, and a conclusion.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
