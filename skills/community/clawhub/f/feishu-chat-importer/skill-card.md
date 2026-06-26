## Description: <br>
Convert Feishu chat history exports into OpenClaw episodic memory format by parsing feishu_chat_YYYYMMDD.json files, normalizing messages, and writing daily episodic summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arkerro](https://clawhub.ai/user/arkerro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to import Feishu chat exports into episodic memory so the conversations can be processed by OpenClaw memory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported conversations may contain private or business-sensitive content and are stored in persistent episodic memory files. <br>
Mitigation: Run with --dry-run first, choose only the intended Feishu export directory, and set OPENCLAW_WORKSPACE explicitly when working with multiple OpenClaw workspaces. <br>


## Reference(s): <br>
- [Feishu Chat Importer on ClawHub](https://clawhub.ai/arkerro/feishu-chat-importer) <br>
- [ClawHub](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown files and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily episodic memory files under memory/episodic/ and supports dry-run, date filtering, and verbose options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
