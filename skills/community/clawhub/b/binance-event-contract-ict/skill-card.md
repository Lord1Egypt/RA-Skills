## Description: <br>
Automatically identifies ICT structures such as Order Blocks, Fair Value Gaps, liquidity sweeps, and inducement patterns on Binance BTC/ETH event-contract K-line data to support SSS-tier signal review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acwxpunh](https://clawhub.ai/user/acwxpunh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-analysis agents use this skill to review Binance BTC/ETH event-contract K-line data for ICT structures and produce structured confirmation reports for downstream risk management. It is intended to analyze supporting market structure, not to execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review reported a suspicious verdict for this release. <br>
Mitigation: Install only if the publisher is trusted and review the skill behavior before using it in live market-analysis workflows. <br>
Risk: The artifact describes market-structure scoring that could be mistaken for trading advice. <br>
Mitigation: Use outputs as analysis for human or downstream risk review; do not treat them as automated trade execution instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acwxpunh/binance-event-contract-ict) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include ICT structure findings, score bands, and data-unavailable handling when required K-line data is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
