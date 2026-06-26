## Description: <br>
Performance-optimized strategies for editing Feishu (Lark) documents via OpenClaw's feishu_doc tool, including targeted block updates, positioned image insertion, table edits, chunking, rate-limit handling, rich-text preservation, and conflict avoidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents working with Feishu or Lark documents use this skill to plan faster, lower-risk block-level edits, image placement, table updates, and large-document changes while preserving existing formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may update or delete Feishu document blocks incorrectly or affect shared work. <br>
Mitigation: Review planned edits before applying them to important shared documents, especially when collaborators may be editing at the same time. <br>
Risk: Blind block updates can remove existing rich-text formatting. <br>
Mitigation: Read affected blocks first, skip unchanged blocks, and use style-specific actions for formatting-only changes where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqunabc/feishu-doc-editing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents toward targeted Feishu document operations and asks them to review planned document mutations before applying them.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
