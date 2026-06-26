## Description: <br>
Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity & credential documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI agent builders, and operations teams use this skill to invoke Laiye ADP from the terminal for document parsing, structured field extraction, task polling, application management, and batch processing workflows. <br>

### Deployment Geography for Use: <br>
Global, with separate Chinese Mainland and overseas public-cloud endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: Installer commands may execute downloaded shell or PowerShell scripts. <br>
Mitigation: Prefer the npm package or a pinned, verified release; inspect any curl-to-bash or downloaded PowerShell installer before running it. <br>
Risk: Documents may be sent to Laiye ADP public-cloud services for parsing or extraction. <br>
Mitigation: Only process documents your organization permits to leave its environment, especially IDs, HR files, invoices, receipts, and financial records. <br>
Risk: API keys are required and may be exposed through unsafe handling. <br>
Mitigation: Use a limited API key, store it in approved configuration or environment storage, and avoid placing secrets directly on command lines. <br>
Risk: Some commands can delete apps, clear configuration, or batch-process local folders. <br>
Mitigation: Require explicit user approval before destructive actions or broad local-folder batch processing. <br>
Risk: Large or repeated document processing can consume paid service credits. <br>
Mitigation: Check the credit balance and confirm scope before large batch jobs or workflows likely to incur usage charges. <br>


## Reference(s): <br>
- [ADP CLI command reference](references/commands.md) <br>
- [ADP CLI response schema](references/response-schema.md) <br>
- [ADP CLI error handling guide](references/error-handling.md) <br>
- [ADP CLI examples](references/examples.md) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh) <br>
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd) <br>
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe) <br>
- [Laiye ADP skill page](https://clawhub.ai/laiye-adp/agentic-doc-parse-and-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with ADP CLI commands; ADP CLI operations return JSON for parsing, extraction, app management, credit, and task-query results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local, URL, and base64 document inputs; asynchronous workflows return task IDs; export options may write result files.] <br>

## Skill Version(s): <br>
1.10.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
