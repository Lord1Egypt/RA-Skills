## Description: <br>
Transfers ownership of Feishu documents, spreadsheets, bitables, mind maps, and files created by an AI robot to a specified user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to move Feishu document ownership from AI-created accounts or bot-owned files to a target human user by token or in bulk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk transfer mode can reassign control of many Feishu documents without an interactive confirmation step. <br>
Mitigation: Run the listing dry-run first, verify the target open_id and file scope, and prefer a single-token transfer or explicit owner filter before using --all. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/feishu-owner-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke lark-cli to list files, inspect Feishu file metadata, and transfer ownership for a single token or root-folder batch.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
