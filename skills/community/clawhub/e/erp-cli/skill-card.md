## Description: <br>
物达通 ERP lets agents use erp-cli to answer property-management knowledge questions and perform authenticated ERP tasks such as work-order lookup, creation, assignment, and status review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingwenkai](https://clawhub.ai/user/xingwenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property-management employees and agents use this skill to route natural-language requests to ERP knowledge search, authentication, configuration, and work-order operations. It is intended for WindaKa ERP environments where the user has authorized access and can confirm write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authenticated ERP access, including work-order and fallback API operations. <br>
Mitigation: Install only for trusted users, restrict raw API invocation, and require explicit confirmation before write, delete, or bulk-access operations. <br>
Risk: The skill requires sensitive credentials and RAGFlow API configuration. <br>
Mitigation: Protect and rotate configured API keys, avoid exposing tokens in responses, and use the documented per-user --as identity separation. <br>
Risk: Broad knowledge-search routing may answer questions outside the intended ERP or property-management scope. <br>
Mitigation: Limit use to relevant WindaKa ERP and property-management workflows and review outputs before acting on operational guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xingwenkai/erp-cli) <br>
- [Publisher profile](https://clawhub.ai/user/xingwenkai) <br>
- [Global ERP reference](references/global-reference.md) <br>
- [Intent routing guide](references/intent-guide.md) <br>
- [Knowledge product reference](references/products/knowledge.md) <br>
- [Work-order product reference](references/products/workorder.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require an explicit --as user identity, authenticated ERP access, and confirmation before write or destructive operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
