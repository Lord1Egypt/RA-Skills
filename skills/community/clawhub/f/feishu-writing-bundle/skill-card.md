## Description: <br>
Feishu Writing Bundle helps OpenClaw agents create, update, refine, formalize, and deliver Feishu documents with a returned document link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyilt](https://clawhub.ai/user/tianyilt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent builders use this skill to turn source material, drafts, and existing Feishu documents into structured Feishu deliverables. It guides agents through reading inputs, choosing create or update workflows, performing targeted edits or proposal formalization, and returning a usable document link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, edit, read, and share live Feishu workspace documents. <br>
Mitigation: Install only when that document access is intended, and use the narrowest OAuth and tool permissions that still support the task. <br>
Risk: Broad edits, deletion, overwrite, replace-all, or publication from chats and files could change or expose workspace content unexpectedly. <br>
Mitigation: Require a preview and explicit confirmation before destructive or broad document operations, and specify the exact document or destination before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tianyilt/feishu-writing-bundle) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Best Practices](references/best-practices.md) <br>
- [Open-Box Rules](references/open-box-rules.md) <br>
- [Workflows](references/workflows.md) <br>
- [Style Guide](references/style-guide.md) <br>
- [Skill Map](references/skill-map.md) <br>
- [Reference Docs](references/reference-docs.md) <br>
- [OpenClaw Feishu writing best practices](https://fudan-nlp.feishu.cn/wiki/WZVMwUEnXiHUqLkfzDycSp9en2c?from=from_copylink) <br>
- [Feishu writing reference document](https://fudan-nlp.feishu.cn/docx/HdWfdNomtoGd7yxL3gVcFgrhnnb) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-style tool-call examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected deliverables often include Feishu document URLs after document creation or update.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
