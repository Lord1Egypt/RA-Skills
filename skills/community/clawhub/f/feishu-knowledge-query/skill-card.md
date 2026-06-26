## Description: <br>
飞书知识库查询工具，用于在用户需要查询已有知识、确认操作步骤、查找历史记录或参考之前工作时，搜索知识库文档、获取具体文档内容并引用知识库中的操作指南。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subwukong](https://clawhub.ai/user/subwukong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to consult an existing Feishu knowledge base before acting, especially when confirming procedures, retrieving prior operating guidance, or reusing documented best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause the agent to consult the Feishu knowledge base when the user intended only the current conversation or local context. <br>
Mitigation: Clarify whether a Feishu knowledge-base lookup is desired before searching when the user's request is ambiguous. <br>
Risk: Knowledge-base material can become stale or incomplete for the current task. <br>
Mitigation: Treat retrieved guidance as reference material and confirm time-sensitive procedures before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subwukong/feishu-knowledge-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or conversational text with knowledge-base search and retrieval guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu document search terms, selected document identifiers, summarized document content, and cited operating guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
