## Description: <br>
AlphaGBM Buffett Analysis produces a Warren Buffett-style scorecard for a US stock ticker, scoring business simplicity, moat, management, and valuation before returning a weighted HOLDABLE, WATCHABLE, or AVOID verdict. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research agents use this skill to request a mechanical Buffett-style assessment of a US stock ticker, including lens-level scores, a weighted verdict, and concise reasoning for long-term hold research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the scorecard for personalized investment advice. <br>
Mitigation: Present outputs as mechanical financial research only, and require users to make their own investment decisions. <br>
Risk: The skill may be invoked accidentally on broad investing questions. <br>
Mitigation: Use explicit Buffett-lens prompts with a confirmed US ticker before requesting an analysis. <br>
Risk: Uncached ticker calls may consume stock-analysis credits. <br>
Mitigation: Reuse cached results when appropriate and make cost expectations clear before repeated ticker analysis. <br>


## Reference(s): <br>
- [AlphaGBM](https://alphagbm.com) <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-buffett-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown narrative with structured scorecard fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a US stock ticker; API usage may consume one stock-analysis credit per uncached ticker and cache results for 30 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
