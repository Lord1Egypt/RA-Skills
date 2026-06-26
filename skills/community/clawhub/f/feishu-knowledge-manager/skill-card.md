## Description: <br>
This skill helps agents save external article content to Feishu Docs, summarize key points into a Feishu knowledge base, and periodically organize duplicate or outdated knowledge entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subwukong](https://clawhub.ai/user/subwukong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and knowledge workers use this skill to capture linked articles into Feishu, preserve source content, summarize key points, classify them by topic, and maintain a cleaner knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write article content and summaries into Feishu, which may affect shared documents or knowledge bases. <br>
Mitigation: Use a limited-permission Feishu account, constrain the target folder or knowledge base, and require confirmation before saving or reorganizing content. <br>
Risk: The daily cleanup task may reorganize or remove duplicate documents without enough user review. <br>
Mitigation: Enable scheduled cleanup only with dry-run review, logs, rollback, and a simple disable path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/subwukong/feishu-knowledge-manager) <br>
- [Publisher profile](https://clawhub.ai/user/subwukong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Feishu document-update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu documents when the required Feishu tools and permissions are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
