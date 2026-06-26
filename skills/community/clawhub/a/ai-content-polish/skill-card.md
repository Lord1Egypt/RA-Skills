## Description: <br>
Detects AI-writing traces in Chinese text, provides evidence-backed polish suggestions, and can return a human-readability score or revised wording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caingao](https://clawhub.ai/user/caingao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, editors, marketers, students, researchers, and product teams use this skill to review Chinese text for AI-like style patterns and receive concrete readability feedback. Use should remain transparent and compliant with disclosure, academic integrity, publication, moderation, provenance, and platform rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to make AI-generated Chinese text look less AI-generated. <br>
Mitigation: Use it only for transparent readability and style review, and require users to follow disclosure, academic integrity, publication, moderation, provenance, and platform rules. <br>
Risk: The server security review reports no built-in guardrails against deceptive use. <br>
Mitigation: Review outputs before deployment or publication and reject requests intended to hide AI authorship or bypass policy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caingao/ai-content-polish) <br>
- [Publisher profile](https://clawhub.ai/user/caingao) <br>
- [README](artifact/README.md) <br>
- [Detection rules](artifact/detection-rules.md) <br>
- [Test cases](artifact/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, revised Chinese text, tabular change lists, or brief scoring summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Modes include report, rewrite, and score; style controls include strictness, target style, and edit aggressiveness.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
