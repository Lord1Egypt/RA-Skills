## Description: <br>
Build and use a Feishu/Lark cross-app identity master for multi-agent, multi-account routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxfkuq2023](https://clawhub.ai/user/wxfkuq2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to maintain a canonical Feishu/Lark identity master, merge app-local identities into shared subjects, and route outbound messages through the correct account-scoped open_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists sensitive cross-app identity mappings, including Feishu identifiers and contact fields. <br>
Mitigation: Restrict read and edit access to identity files, define retention and deletion rules, and avoid collecting fields that are not needed for routing. <br>
Risk: Incorrect merges can associate one person with the wrong subject or route messages to the wrong app-local open_id. <br>
Mitigation: Use union_id first, fall back to unique user_id only when unambiguous, and send conflicts or missing critical identifiers to pending review. <br>
Risk: Merge and review controls are under-scoped if any workspace actor can update the shared identity database. <br>
Mitigation: Limit who can run merge and review scripts, require review reasons for approvals or rejections, and audit changes to the identity master. <br>
Risk: Batch merging invokes a workspace bin script path, which can be unsafe if that path is not the reviewed merge script. <br>
Mitigation: Confirm the invoked workspace script is the reviewed merge helper before running batch updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wxfkuq2023/feishu-identity-routing) <br>
- [Workflow](references/workflow.md) <br>
- [Outbound Routing Patterns](references/outbound-routing-patterns.md) <br>
- [Pending Review Policy](references/pending-review-policy.md) <br>
- [Schema Example](references/schema-example.json) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON identity files and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates workspace identity data, human-readable summaries, merge/review command guidance, and outbound routing patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
