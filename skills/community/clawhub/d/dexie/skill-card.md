## Description:

Track Chia DEX offers, tokens, pairs, prices, and platform stats using the Dexie.space API via CLI or chat commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to answer Chia DEX questions by retrieving Dexie.space offers, token prices, liquidity, trading pairs, and platform statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dexie-related queries are sent to the public Dexie.space API.

Mitigation: Use the skill only when sharing query terms and requested market data with Dexie.space is acceptable.

Risk: Installing with npm link adds dex and dexie commands to the local shell environment.

Mitigation: Review installation steps before linking commands globally, especially on shared or sensitive systems.

Risk: Dependencies may become outdated before use in a sensitive environment.

Mitigation: Update and review npm dependencies before deployment in security-sensitive contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/koba42corp/skills/dexie)
- [Dexie.space](https://dexie.space)
- [Dexie.space API](https://api.dexie.space/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text responses with command examples and JavaScript integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are suitable for terminal output and chat messages.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
