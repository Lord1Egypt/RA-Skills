## Description: <br>
End-to-end operator for a Gougoubi pump-style prediction market that creates proposals and conditions, supervises trading liquidity, submits deadline results, handles disputes, and settles rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to run a Gougoubi pump prediction-market lifecycle on BNB Chain, from market creation through trading, settlement, disputes, and claims. It is intended for wallet-connected workflows where the user reviews transaction details before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signed on-chain actions can affect funds through market creation, trades, settlement, disputes, claims, approvals, or LP actions. <br>
Mitigation: Use a dedicated low-balance wallet, avoid unlimited token approvals, verify proposal and condition IDs, and require a full transaction preview before signing. <br>
Risk: Incorrect deadlines, result submissions, or missing evidence can create costly transactions or disputed market outcomes. <br>
Mitigation: Confirm market parameters before write transactions, require public evidence for settlement, simulate contract calls first, and pause when estimates or state checks look abnormal. <br>


## Reference(s): <br>
- [Gougoubi Pump Lifecycle on ClawHub](https://clawhub.ai/chinasong/ggb-pump-lifecycle) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown stage summaries with transaction previews and contract or subgraph call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before wallet-signed transactions and responds in the user's language.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
