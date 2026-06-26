## Description: <br>
High-quality Feishu/Lark Docx writing via OpenClaw. Use when you want to turn Markdown into well-formatted Feishu Docx (headings, lists, nesting, code blocks) using feishu_docx_write_markdown; includes safe workflows, templates, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongjjlj](https://clawhub.ai/user/xiongjjlj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to turn Markdown into well-formatted Feishu/Lark Docx content, including meeting notes, weekly updates, and proposals. It supports append-first document workflows and cautious full-document replacement when explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Replace mode can overwrite the target Feishu/Lark Docx document. <br>
Mitigation: Prefer append mode, verify the target document ID before writing, and use replace mode only when the user explicitly requests a full overwrite. <br>
Risk: Feishu app credentials, tokens, and document links can expose private workspace data if copied into skill files or shared prompts. <br>
Mitigation: Use the user's own Feishu app credentials and scopes, and do not hardcode tokens, chat IDs, open IDs, or document links in the skill. <br>
Risk: Insufficient Feishu Docx or Drive permissions can cause failed writes or writes to the wrong accessible document. <br>
Mitigation: Confirm the app has the required Docx/Drive scopes and that the bot or app has collaborator access to the intended document. <br>


## Reference(s): <br>
- [Docx templates](references/templates.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Feishu/Lark Docx write parameters and optional shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided Feishu app credentials and document identifiers; replace mode is destructive and requires explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
