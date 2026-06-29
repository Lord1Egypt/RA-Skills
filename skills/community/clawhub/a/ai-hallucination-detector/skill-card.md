## Description: <br>
Detects and analyzes factual errors, inconsistencies, and hallucination risks in LLM-generated text, producing structured scores, issue details, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content reviewers, researchers, legal and medical reviewers, journalists, and enterprise teams use this skill to assess AI-generated text for factuality, temporal consistency, citation reliability, numerical accuracy, terminology quality, and related hallucination indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or regulated documents may be submitted for fact-checking. <br>
Mitigation: Only provide content that is appropriate for local model processing and any first-run model download behavior in the target agent environment. <br>
Risk: Hallucination detection results may miss issues or assign imperfect confidence scores, especially for specialized legal, medical, academic, or time-sensitive claims. <br>
Mitigation: Use the report as review support and have qualified reviewers verify high-impact claims against authoritative sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/ai-hallucination-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Structured JSON hallucination report with scores, risk level, issue instances, corrections, confidence values, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally after installation; first use may require model download depending on the agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
