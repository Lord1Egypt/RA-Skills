## Description: <br>
Feishu Advanced Builder helps agents create Feishu whiteboard diagrams from Mermaid or PlantUML, manipulate Bitable rows and fields, and convert complex Markdown into native Feishu document blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydreamhorse](https://clawhub.ai/user/mydreamhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to automate Feishu workspace updates, including architecture diagrams, DevOps or Auto-RCA tracking tables, and richly formatted PRD or analysis documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Feishu workspace content, including documents, whiteboards, and Bitable data. <br>
Mitigation: Use a least-privilege Feishu app, confirm target document, board, table, and folder IDs before running write commands, and review generated content before execution. <br>
Risk: Tenant access tokens and Feishu secrets can be exposed in prompts, logs, transcripts, or command output. <br>
Mitigation: Keep Feishu secrets out of prompts and shared logs, protect token output, and avoid token-printing commands unless specifically needed. <br>
Risk: Changing FEISHU_BASE_URL could redirect API traffic away from the intended Feishu endpoint. <br>
Mitigation: Do not set FEISHU_BASE_URL unless the endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [Feishu Board API Notes](references/feishu-board-api.md) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with Node.js command examples and Feishu API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and appropriate document, whiteboard, and Bitable permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
