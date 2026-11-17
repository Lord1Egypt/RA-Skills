## Description:

Helps merchants use 1688 to search for products, review bound downstream shops, publish selected products to supported commerce platforms, and configure a 1688 access key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yclovebf-stack](https://clawhub.ai/user/yclovebf-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and commerce operators use this skill to find product candidates on 1688, evaluate search results, check connected shops, and publish selected items to Douyin, Pinduoduo, Xiaohongshu, or Taobao stores. The skill also guides first-time setup and AK configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AK can authorize 1688 account and shop actions, including product publishing, and may be exposed if pasted into chat, command text, transcripts, or logs.

Mitigation: Use a secure OpenClaw secret-entry mechanism where available, avoid sharing the AK in chat or command text, and rotate the AK if it has already appeared in transcripts or logs.

Risk: The skill can publish products to connected downstream shops, which may create incorrect listings, platform compliance issues, or unintended commercial activity.

Mitigation: Review selected products, target shop, item count, and dry-run results before publishing; use the skill's confirmation and dry-run flow for product publishing.

Risk: A nontrusted gateway endpoint could receive sensitive configuration or commerce commands.

Mitigation: Keep OPENCLAW_GATEWAY_URL restricted to a trusted local endpoint before configuring or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yclovebf-stack/skills/1688-shopkeeper)
- [1688 AI App](https://air.1688.com/kapp/1688-ai-app/pages/home?from=1688-shopkeeper)
- [Search guide](artifact/references/search.md)
- [Publishing guide](artifact/references/publish.md)
- [AK configuration guide](artifact/references/configure.md)
- [Operations FAQ index](artifact/references/FAQ.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with a Markdown display field, plus concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs include success, markdown, and data fields; publishing and search actions are limited to 20 products per command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
