## Description: <br>
当用户提及任何与本地文档、知识库、参考资料、历史记录、配置文件、说明文档、内部资料、已有内容、文件创建/读取等相关需求时，必须使用本技能从 /mnt/data 目录中检索或操作文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianeasy](https://clawhub.ai/user/jianeasy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to ground answers and file-related tasks in a local /mnt/data knowledge base when a request references documents, records, templates, configuration, or existing project material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause broad searches across local knowledge-base files for vague or indirect user requests. <br>
Mitigation: Set clear folder limits for /mnt/data and require user confirmation before recursive searches. <br>
Risk: The skill includes behavior for file creation, reading, and operations against local content. <br>
Mitigation: Require explicit approval before any file creation, editing, moving, or deletion. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses grounded in local file search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or operate on files under /mnt/data when the agent environment grants access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
