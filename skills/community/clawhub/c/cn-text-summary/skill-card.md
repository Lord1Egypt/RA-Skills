## Description: <br>
Cn Text Summary summarizes provided Chinese text and extracts keywords using a local Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize long Chinese text and extract keywords locally for articles, emails, product descriptions, and similar documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or private text submitted for summarization may be processed by the local agent environment. <br>
Mitigation: Do not provide secrets or private text unless local processing in the agent environment is acceptable. <br>
Risk: Promotional website links are outside the inspected local script. <br>
Mitigation: Review external links separately before relying on them or sharing data through them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-text-summary) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing original length, summary length, summary text, and keyword list; agent-facing guidance may accompany use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; optional jieba support improves Chinese keyword extraction when installed.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
