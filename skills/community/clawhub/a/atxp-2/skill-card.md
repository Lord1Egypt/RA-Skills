## Description:

ATXP gives agents a funded identity with wallet, email, and paid API access for web search, media generation, X/Twitter search, email, and LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r-m-naveen](https://clawhub.ai/user/r-m-naveen)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to register funded agent identities, manage balances, and access paid tools such as web search, generated media, email, and LLM inference through ATXP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable npm package while handling wallet, identity, and email credentials.

Mitigation: Review the package before use and prefer a pinned, reviewed atxp CLI version instead of an unpinned latest release.

Risk: ATXP_CONNECTION grants access to the agent wallet and identity.

Mitigation: Avoid printing or logging ATXP_CONNECTION, do not pass it on the command line, and keep it out of outbound messages or third-party prompts.

Risk: Use with real funds, private email, or production credentials can increase impact from misuse or credential exposure.

Mitigation: Restrict wallet balances and run the skill in a least-privileged environment before production use.

## Reference(s):

- [ATXP Documentation](https://docs.atxp.ai)
- [ATXP npm Package](https://www.npmjs.com/package/atxp)
- [ClawHub Skill Page](https://clawhub.ai/r-m-naveen/skills/atxp-2)
- [ATXP LLM Gateway](https://docs.atxp.ai/agents/llm-gateway)
- [ATXP TypeScript SDK](https://www.npmjs.com/package/@atxp/client)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for Node.js >=18, npx, ATXP_CONNECTION, and ~/.atxp/config.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
