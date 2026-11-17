## Description:

Generate, validate, and submit BracketsBot NCAA tournament brackets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbauch](https://clawhub.ai/user/sbauch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, agents, and developers use this skill to create NCAA tournament bracket picks with chat, policy, or coded workflows, validate 63-game predictions, and prepare share links or unsigned transaction payloads for human or wallet-based submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sharing workflow may upload bracket picks and persist a draft token or API URL in local picks files, allowing later syncs through stored remote endpoints.

Mitigation: Review local picks files before reuse, avoid sharing sensitive picks, and use only trusted BracketsBot API and frontend URLs.

Risk: Untrusted policy modules or picks files can affect bracket generation and local walk state.

Mitigation: Run only reviewed policy modules, keep picks files from trusted sources, and validate picks with the CLI before submission.

Risk: Unsigned transaction payloads can target unexpected chain, recipient, value, or calldata.

Mitigation: Verify chainId, recipient or to address, value, and calldata before signing with Bankr or any wallet.

## Reference(s):

- [README](README.md)
- [2026 NCAA Tournament Season Guide](reference/2026-season-guide.md)
- [Walk State Contract](reference/WALK_STATE.md)
- [Wallet Integration Examples](reference/WALLET_INTEGRATIONS.md)
- [Bracket Output Schema](schema/bracket-output.schema.json)
- [Tournament Schema](schema/tournament.schema.json)
- [Sports Reference 2026 ratings](https://www.sports-reference.com/cbb/seasons/men/2026-ratings.html)
- [KenPom](https://kenpom.com)
- [Barttorvik](https://barttorvik.com)
- [ESPN BPI](https://www.espn.com/mens-college-basketball/bpi)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON outputs, schemas, and optional JavaScript policy code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bracket pick workflows, validation commands, share links, and unsigned EVM transaction payload guidance; final signing remains outside the skill.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
