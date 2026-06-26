## Description: <br>
Analyzes public article links for structure, memorable lines, topic logic, emotional arc, and reusable writing patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, marketers, and content operators use this skill to break down public articles and learn repeatable title, structure, opening, ending, and quotation patterns. It can produce a full Markdown analysis report or a shorter quick breakdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens article links supplied by the user. <br>
Mitigation: Avoid using private, internal, or sensitive URLs and only analyze links the user is comfortable sharing with the agent. <br>
Risk: Generated analysis can be incomplete or misleading if the article is inaccessible, truncated, or interpreted incorrectly. <br>
Mitigation: Review the analysis against the source article before reusing recommendations or publishing derivative content. <br>
Risk: When asked to create a Feishu document, the report is stored outside the chat. <br>
Mitigation: Confirm the report does not contain sensitive content before requesting Feishu document creation. <br>


## Reference(s): <br>
- [Popular Title Patterns and Common Article Structures](artifact/references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally create a Feishu document when the user asks.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
