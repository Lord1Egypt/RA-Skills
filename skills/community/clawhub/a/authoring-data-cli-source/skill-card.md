## Description:

Use when the user needs to add or redesign an agent-data-cli source for RSS, news, social media, finance, APIs, scraping, browser automation, authentication, or remote content sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[severinzhong](https://clawhub.ai/user/severinzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to research, specify, implement, and verify new or redesigned agent-data-cli sources. It is intended for source work involving RSS, APIs, scraping, browser automation, authentication, remote sync, and explicit interaction flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote install commands may install a changing upstream version.

Mitigation: Prefer a pinned release or reviewed commit and run setup in a restricted environment without production credentials.

Risk: Authenticated, browser, scraping, or interact-capable sources may handle credentials or trigger remote side effects.

Mitigation: Confirm user authorization, keep credentials least-privilege, and require explicit confirmation before remote side effects.

## Reference(s):

- [Source Contract](artifact/references/source-contract.md)
- [Source Testing](artifact/references/source-testing.md)
- [API Source Guidance](artifact/references/source-type-api.md)
- [Browser Source Guidance](artifact/references/source-type-browser.md)
- [Interact Source Guidance](artifact/references/source-type-interact.md)
- [RSS Source Guidance](artifact/references/source-type-rss.md)
- [Source Review Checklist](artifact/references/source-review-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with code blocks, command examples, implementation plans, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows a staged research, spec, plan, approval, implement, and verify workflow for source-authoring tasks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
