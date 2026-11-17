## Description:

Fridge Manager tracks household fridge, freezer, and pantry inventory, calculates expiry dates from a bilingual food-storage knowledge base, and supports inventory queries and expiry reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiangm1](https://clawhub.ai/user/qiangm1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a household food inventory through conversation, including adding, consuming, discarding, and querying items. It also helps users check expiry dates, receive scheduled expiry reminders, and get basic storage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local inventory and change log can reveal household food habits to other users who share the same workspace.

Mitigation: Keep the workspace private when possible and periodically clear or trim family/fridge.json if the history is no longer needed.

Risk: Expiry dates are estimates for opened or loose items and may not match packaged-food labels or actual storage conditions.

Mitigation: Use package labels and user judgment as the authority for sealed foods, spoiled food, or uncertain storage history.

## Reference(s):

- [Food Storage Knowledge Base (English)](references/food-knowledge-en.md)
- [Food Storage Knowledge Base (Chinese)](references/food-knowledge-zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text with JSON inventory updates and optional Markdown-style expiry alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a workspace-relative family/fridge.json inventory and change log when used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
