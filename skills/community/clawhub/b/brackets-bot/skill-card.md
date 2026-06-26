## Description: <br>
Generate, validate, and submit BracketsBot NCAA tournament brackets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sbauch](https://clawhub.ai/user/sbauch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agents, and developers use this skill to generate NCAA tournament bracket picks, validate the 63-pick output, create share links for human review, and prepare unsigned transaction payloads for wallet-based submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Share links upload or expose bracket picks to the configured BracketsBot frontend/API. <br>
Mitigation: Use share links only when the user wants browser review or submission, and treat generated links as containing the selected bracket picks. <br>
Risk: Prepared transaction payloads can lead to on-chain submission if signed by a wallet. <br>
Mitigation: Before signing, verify chainId, destination contract, value, and data with the user's wallet runtime. <br>
Risk: Custom coded policy modules execute local JavaScript selected by the user or agent. <br>
Mitigation: Run only policy modules the user wrote or trusts, and prefer natural-language policy execution unless the user asks for coded logic. <br>
Risk: Stepwise bracket state is single-writer oriented and can be overwritten by concurrent writers. <br>
Mitigation: Treat the picks file as the source of truth and use external locking or a single writer when multiple processes may update it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sbauch/brackets-bot) <br>
- [README](README.md) <br>
- [Walk State Contract](reference/WALK_STATE.md) <br>
- [Wallet Integration Examples](reference/WALLET_INTEGRATIONS.md) <br>
- [2026 NCAA Tournament Season Guide](reference/2026-season-guide.md) <br>
- [Bracket Output Schema](schema/bracket-output.schema.json) <br>
- [Sports Reference 2026 ratings](https://www.sports-reference.com/cbb/seasons/men/2026-ratings.html) <br>
- [KenPom](https://kenpom.com) <br>
- [Barttorvik](https://barttorvik.com) <br>
- [ESPN BPI](https://www.espn.com/mens-college-basketball/bpi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON outputs, bracket prediction files, share URLs, and unsigned EVM transaction payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bracket predictions use winner seed IDs from 1 to 64 and complete brackets contain 63 picks.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
