## Description: <br>
Screens A-share stocks for N-pattern technical setups and returns stock signals with stage, strength, volume, stop-loss, target, and rationale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and technical-analysis users use this skill to request A-share N-pattern stock signals through a paid x402 API call. Outputs should be treated as unverified market information, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each use may trigger a 0.01 USDC paid x402 call to the disclosed Base wallet. <br>
Mitigation: Install or invoke the skill only when the user accepts the disclosed payment amount, chain, and recipient. <br>
Risk: Security evidence says the submitted code returns fixed stock recommendations rather than substantiating real-time market-data screening. <br>
Mitigation: Treat outputs as unverified financial information and compare any signal against independent market data before acting. <br>
Risk: The skill provides stock-selection guidance that could be mistaken for investment advice. <br>
Mitigation: Use outputs only as informational screening support and apply independent risk controls and professional judgment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jinboh68-prog/a-stock-n-pattern) <br>
- [Publisher Profile](https://clawhub.ai/user/jinboh68-prog) <br>
- [Paid API Endpoint](https://a-stock-signals.vercel.app/n) <br>
- [Service Base URL](https://a-stock-signals.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON stock-signal objects or text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes stock code, name, sector, N-pattern stage, strength rating, volume condition, stop-loss, target, rationale, and payment metadata.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter says 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
