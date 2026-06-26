## Description: <br>
TypeScript (Node.js 20+) AI news-driven BNB strategy trading bot for BSC that uses news sentiment, risk controls, dry-run safety, panic mode, status reporting, and approval revoke tooling for WBNB-to-stablecoin swaps. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[happyRstudent](https://clawhub.ai/user/happyRstudent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system reviewers use this skill to run or assess a BSC news-driven BNB trading workflow with configurable news ingestion, sentiment scoring, dry-run mode, wallet key handling, status checks, and risk gates. It is appropriate for research and controlled testing, not unmanaged live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can automatically move wallet funds and cause irreversible financial loss. <br>
Mitigation: Use only a dedicated low-balance wallet, keep DRY_RUN=true through full-flow testing, and never provide a main wallet private key. <br>
Risk: Trading decisions depend on external RPC, news, 1inch, and token configuration that may be wrong or unavailable. <br>
Mitigation: Verify RPC, news source, 1inch API, token addresses, slippage, and trade limits before any live run. <br>
Risk: The panic command should not be treated as the only emergency stop for a running trading process. <br>
Mitigation: Stop the running process directly and confirm no live trading process remains active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyRstudent/ai-news-bnb-trader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/happyRstudent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON status output, and TypeScript configuration/code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can start a long-running trading process, report status, set panic state, revoke approvals, or encrypt a wallet key depending on the command used.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
