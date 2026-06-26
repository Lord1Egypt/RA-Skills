## Description: <br>
Automatically recognizes accounting details from payment, shopping, and food delivery screenshots and records them in the YiRi accounting app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taobaoaz](https://clawhub.ai/user/taobaoaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users of Xiaoyi Claw use this skill to extract transaction details from financial screenshots and create accounting records in the YiRi accounting app. It is intended for Android phone workflows that have Xiaoyi Claw, the YiRi accounting app, and the required Xiaoyi image-understanding and GUI-agent components available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes financial screenshots, which may contain sensitive transaction details. <br>
Mitigation: Use only in trusted Xiaoyi Claw environments and prefer a workflow that previews extracted fields before saving records. <br>
Risk: The security summary notes that records may be written without a clear confirmation step. <br>
Mitigation: Require user confirmation before committing extracted amount, merchant, category, time, and transaction type to the accounting app. <br>
Risk: The security guidance flags unclear retention and deletion behavior for transaction history or failed records. <br>
Mitigation: Ask the publisher to document whether any transaction history or failed records are stored, where they are stored, and how users can delete them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taobaoaz/auto-accounting) <br>
- [Project homepage](https://github.com/taobaoaz/auto-accounting) <br>
- [README](artifact/README.md) <br>
- [Security audit](artifact/SECURITY_AUDIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style status messages with extracted accounting fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also operate the connected phone/accounting app through the required GUI-agent dependency.] <br>

## Skill Version(s): <br>
1.0.8 (source: SKILL.md frontmatter, _meta.json, server release; package.json lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
