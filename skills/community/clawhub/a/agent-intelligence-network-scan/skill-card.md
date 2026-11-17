## Description:

Query agent reputation, detect threats, and discover agents across platforms using reputation scores, identity links, leaderboards, trends, and threat labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent operators use this skill to evaluate agent trustworthiness, search for agents by reputation or platform, check threat flags, review leaderboards and trends, and resolve identities across platforms. Its reputation scores and threat labels should be treated as advisory inputs alongside independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces reputation scores and threat labels that could affect collaboration, investment, moderation, or exclusion decisions.

Mitigation: Use scores and labels as advisory signals only, require human review for consequential decisions, and corroborate findings with independent evidence.

Risk: The skill profiles agents across platforms and links identities, which can raise privacy and accuracy concerns.

Mitigation: Use only with appropriate privacy review, minimize retained data, and give affected users a path to contest or correct identity and reputation claims.

Risk: Backend or cached data may be unavailable, stale, incomplete, or inconsistent with current agent behavior.

Mitigation: Check data freshness before relying on results, disclose when cached data is used, and avoid automated enforcement based solely on cached outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvcidpsyche/skills/agent-intelligence-network-scan)
- [Publisher Profile](https://clawhub.ai/user/lvcidpsyche)
- [API Reference](artifact/references/API_REFERENCE.md)
- [Reputation Algorithm](artifact/references/REPUTATION_ALGORITHM.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, query result structures, shell snippets, and configuration details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query a backend or local cache; reputation scores, identity links, and threat labels are advisory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
