## Description: <br>
Fridge Manager helps households track food inventory, expiry dates, storage locations, and bilingual storage advice through conversational updates and optional local reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiangm1](https://clawhub.ai/user/qiangm1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External household users use this skill to add, remove, query, and audit fridge, freezer, pantry, and counter inventory. It also supports expiry checks, food storage advice, and optional local cron-style reminders for items expiring soon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household food inventory, quantities, expiry dates, and change timestamps in a workspace-visible JSON file. <br>
Mitigation: Use it only in workspaces where this household inventory data is acceptable to store, and review family/fridge.json access before sharing the workspace. <br>
Risk: Optional daily reminders may create recurring local expiry checks. <br>
Mitigation: Enable the cron or heartbeat workflow only when recurring local checks are desired, and disable it when reminders are no longer needed. <br>
Risk: Shelf-life guidance can be approximate for foods not covered by the knowledge base or when packaging labels differ. <br>
Mitigation: Prefer package labels and food-safety judgment over generated expiry estimates, and keep conservative notes when the skill estimates an item. <br>


## Reference(s): <br>
- [Food Storage Knowledge Base (English)](references/food-knowledge-en.md) <br>
- [食品保存知识库（中文版）](references/food-knowledge-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with structured inventory summaries, expiry alerts, confirmations, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write and update a workspace-relative family/fridge.json inventory and log when used by an agent with file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
