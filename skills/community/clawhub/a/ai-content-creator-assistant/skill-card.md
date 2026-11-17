## Description:

Generates three to five platform-adapted content drafts for channels such as Xiaohongshu, Douyin, Kuaishou, WeChat, Zhihu, and Twitter/X through a clawtip payment-verified AI conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request multiple Chinese-language content options, compare different creative angles, and adapt copy or short-form scripts for specific social platforms after payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the user's prompt in local order files used for payment verification.

Mitigation: Use it only for prompts appropriate for local persistence and remove order files when they are no longer needed.

Risk: Payment verification is weak enough that the clawtip authorization boundary should not be treated as robust.

Mitigation: Review the payment flow before relying on it for access control or monetized service delivery.

Risk: The workflow includes an npx sandbox payment command and promotes a separate pro package.

Mitigation: Run sandbox commands only in a constrained environment and inspect the pro package separately before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/ai-content-creator-assistant)
- [Publisher profile](https://clawhub.ai/user/jinyu12166)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell commands and JSON status lines from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multiple candidate drafts with titles, body copy, tags, platform-specific tone guidance, and payment authorization status.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
