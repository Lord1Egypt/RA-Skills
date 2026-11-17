## Description:

1688 Shopkeeper helps agents search and evaluate 1688 products, inspect connected shops, publish listings to Douyin, Pinduoduo, Xiaohongshu, and Taobao, view opportunity and trend data, configure AK credentials, and generate shop daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyongzhen](https://clawhub.ai/user/chenyongzhen)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and agents use this skill to source products from 1688, manage connected downstream shops, publish selected products, answer store-operation questions, and review trends or daily operating reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive 1688 marketplace AK credentials.

Mitigation: Use only an AK you are comfortable granting to this workflow, prefer a secure secret mechanism over pasting credentials into chat, and verify OpenClaw configuration permissions if fallback storage is used.

Risk: The skill can publish products to connected live stores.

Mitigation: Review the skill before installing, run dry-run checks for publish actions, and require explicit confirmation before any live publish action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyongzhen/skills/1688-shopkeeper-bak)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Search capability guide](artifact/references/capabilities/search.md)
- [Publish capability guide](artifact/references/capabilities/publish.md)
- [Configure capability guide](artifact/references/capabilities/configure.md)
- [Data contracts](artifact/references/common/data-contracts.md)
- [Error handling](artifact/references/common/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON command output containing a human-facing markdown field, with follow-on agent guidance when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a 1688 AK credential through ALI_1688_AK or OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
