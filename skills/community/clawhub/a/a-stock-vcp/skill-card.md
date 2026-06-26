## Description: <br>
A paid A-share stock screening skill that returns VCP volume-breakout candidates with prices, sectors, strength ratings, stop-loss levels, targets, and buy reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as short-term traders, technical-analysis users, and investors use this skill to request A-share VCP screening results as paid reference information, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a paid stock-picking workflow and may charge 0.01 USDC per call. <br>
Mitigation: Confirm the fee, recipient, and chain before use, and only invoke it when the payment is acceptable. <br>
Risk: Security evidence says the included API code appears to use simulated hard-coded stock signals while the description presents backend market-data screening. <br>
Mitigation: Treat outputs as unverified reference information and validate any result against independent market data before relying on it. <br>
Risk: Stock screening output could be mistaken for investment advice. <br>
Mitigation: Use the output only as informational screening support and apply independent financial judgment and risk controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/a-stock-vcp) <br>
- [Declared backend endpoint](https://a-stock-signals.vercel.app/v) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Markdown or structured text with stock codes, prices, sectors, strength ratings, stop-loss levels, targets, and rationale.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger a paid x402 API call at 0.01 USDC per use; security evidence says the included implementation appears to return simulated stock signals rather than verified live market screening.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence; artifact frontmatter lists 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
