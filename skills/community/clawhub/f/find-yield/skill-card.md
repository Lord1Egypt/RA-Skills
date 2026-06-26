## Description: <br>
Finds high-yield Uniswap LP pools filtered by risk tolerance and minimum TVL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi researchers use this skill to request ranked Uniswap LP yield candidates filtered by chain, risk tolerance, available capital, and minimum TVL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APY rankings are based on pool data and historical fee estimates that may change or omit impermanent-loss assumptions. <br>
Mitigation: Treat results as research, verify current pool data independently, and review impermanent-loss exposure before making allocation decisions. <br>
Risk: Chain scans may fail or return incomplete opportunity data. <br>
Mitigation: Review any chain-specific error messages and rerun the query or narrow the chain scope when data appears incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/find-yield) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown ranked table with concise notes and user-facing error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters can include chains, risk tolerance, capital amount, and minimum TVL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
