## Description: <br>
Guides agents through safe readability and formatting edits for Feishu/Lark documents, emphasizing minimal changes, spacing fixes, bold/list conventions, and protection of rich-text blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and operators use this skill before editing mi.feishu.cn documents to improve document readability while preserving existing content, comments, history, images, and special rich-text blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect document, range, or edit intent could change content or formatting the user did not intend to modify. <br>
Mitigation: Confirm the exact document, selected range, and edit intent before applying changes. <br>
Risk: Broad replacements or edits around images, callouts, formulas, or other rich-text blocks could damage preserved document tokens. <br>
Mitigation: Use minimal targeted edits; fetch and preserve complete tokens before changing any paragraph that contains special blocks. <br>
Risk: The formatting guidance reflects Chinese Feishu document conventions that may not fit every document. <br>
Mitigation: Confirm that the target document should follow these conventions before applying readability changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqunabc/feishu-readability) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls] <br>
**Output Format:** [Markdown guidance with Feishu MCP update examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no hidden code, installation behavior, credential handling, or persistence was identified in the provided security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
