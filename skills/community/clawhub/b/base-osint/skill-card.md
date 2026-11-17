## Description:

Kybera wallet control and token research assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xipzer](https://clawhub.ai/user/xipzer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research Base network tokens and coordinate Kybera wallet actions, including market analysis, identity checks, wallet queries, and guided wallet operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's update flow can replace cached instructions from a remote URL without signed release or hash verification.

Mitigation: Avoid the built-in update flow unless integrity verification is added; review remote changes before enabling updated instructions.

Risk: Wallet actions and paid data access can involve sensitive wallet/account data, x402 budgets, approved domains, or destructive operations.

Mitigation: Install only when the publisher is trusted, review domain and budget settings carefully, and require clear confirmation before paid or destructive wallet actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xipzer/skills/base-osint)
- [Kybera homepage](https://app.kybera.xyz)
- [Arkham Intel](https://intel.arkm.com/)
- [Get Moni](https://getmoni.io/)
- [Bubblemaps](https://app.bubblemaps.io/)
- [DEXScreener](https://dexscreener.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON action blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit wallet action JSON blocks and Kybera UI blocks when supported by the host platform.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
