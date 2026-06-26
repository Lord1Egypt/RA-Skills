## Description: <br>
PKM（个人知识管理）三分支记忆系统。使用时机：(1) 接收记忆，(2) 检索上下文，(3) 搜索记忆，(4) 添加事实，(5) 检查 Qdrant。三分支：L1 复位（索引）、L2 索引、L3 日志、L4 Qdrant、L5 Obsidian、L6 Nebula、L7 情景记忆。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent in storing, retrieving, searching, and checking personal knowledge management memories through local PKM API and Qdrant services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store user-provided notes or personal information in local PKM and Qdrant services. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or sensitive personal information unless storage locations, review procedures, and deletion procedures are understood. <br>
Risk: The skill depends on local PKM API and Qdrant services being trusted and available. <br>
Mitigation: Install and use it only when the local services it contacts are understood and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/chinese-pkm-memory) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides command examples for local PKM API and Qdrant endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
