## Description: <br>
Detect and flag hallucinations in LLM outputs by cross-referencing claims against source documents, code, and verifiable data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI content reviewers, and RAG application teams use this skill to check AI-generated documentation, summaries, API references, and release notes against source material before publication or merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require reading workspace documents and source code to verify claims, which can expose sensitive project material to the active agent session. <br>
Mitigation: Run the skill in a scoped project and provide only the source material needed for the review. <br>
Risk: Findings can be limited by incomplete or ambiguous source evidence, especially for unverifiable or high-impact claims. <br>
Mitigation: Have a human reviewer confirm uncertain, security-related, legal, performance, or release-critical findings before publication or merge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/cm-hallucination-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis report with verification findings, confidence scores, issue classifications, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested local commands for checking claims against source code, documentation, and repository history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
