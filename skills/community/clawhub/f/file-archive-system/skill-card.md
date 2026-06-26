## Description: <br>
本地文件归档系统。把习惯、偏好、日程、每日记录和长期知识结构化存放到四层记忆目录，并通过 index.json 建立可检索索引。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmoon96-dev](https://clawhub.ai/user/lingmoon96-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to organize personal AI memory into a local file archive with identity, working-memory, short-term log, long-term memory, archive, and index structures. It also provides local-first sync guidance and maintenance commands for indexing and archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal memory files and synced archives may contain sensitive information. <br>
Mitigation: Keep the memory directory private, avoid storing passwords or secrets, use access-controlled or encrypted sync targets, and limit sync scope to the memory directory. <br>
Risk: Referenced helper scripts or archive commands may affect local files. <br>
Mitigation: Review helper scripts and command effects before running them, especially before archiving or syncing memory data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is centered on local file organization, indexing, archiving, and sync boundaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
