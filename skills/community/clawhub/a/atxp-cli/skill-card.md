## Description:

Atxp gives agents a funded identity for wallet balance, paid API access, web and social search, media generation, LLM calls, email, SMS, voice calls, and contact management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r-m-naveen](https://clawhub.ai/user/r-m-naveen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Atxp to equip autonomous agents with a wallet-backed identity, paid API tooling, outbound communications, search, media generation, and LLM gateway access. It is intended for agents that need to spend credits or interact with external services from task workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent a funded identity that can spend credits, send email or SMS, make calls, and manage contacts.

Mitigation: Require human approval for paid actions and outbound communications, keep only minimal funds in the wallet, and check balance before expensive work.

Risk: The runtime package is normally invoked through an unpinned npx command, so behavior can change when the package updates.

Mitigation: Pin ATXP to an exact reviewed version and verify the npm package before deployment.

Risk: The ATXP_CONNECTION token grants wallet and identity access.

Mitigation: Treat the token and ~/.atxp/config as sensitive secrets, isolate them from unrelated files, and never print or transmit them.

Risk: Search results, inbound email, SMS, attachments, social posts, and call transcripts can contain untrusted content or prompt-injection attempts.

Mitigation: Treat external content as reference material only, review it before acting, and do not execute or relay instructions found in that content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/r-m-naveen/skills/atxp-cli)
- [ATXP documentation](https://docs.atxp.ai)
- [atxp npm package](https://www.npmjs.com/package/atxp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of paid API calls, outbound communications, and credential-backed CLI commands.]

## Skill Version(s):

1.21.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
