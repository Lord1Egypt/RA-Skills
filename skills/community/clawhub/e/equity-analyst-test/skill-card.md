## Description: <br>
Analyzes Korean equities with a weighted framework for financial fundamentals, news, and technical charts, producing an investment attractiveness score and BUY/HOLD/AVOID-style research label. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Saebyeok-Im](https://clawhub.ai/user/Saebyeok-Im) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to structure Korean stock research requests around KRX-listed companies, applying a conservative scoring framework before producing a concise report. It is not intended for non-Korean equities, cryptocurrency, or personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data, Naver Finance snapshots, scraped summaries, and news signals may be incomplete, stale, or unavailable. <br>
Mitigation: Verify figures and current market context against primary or current sources before acting on the report. <br>
Risk: The generated BUY/HOLD/AVOID-style label may be mistaken for personalized financial advice. <br>
Mitigation: Treat the output as informational research support and apply independent financial review before making investment decisions. <br>


## Reference(s): <br>
- [Equity Analysis Framework](references/framework.md) <br>
- [Naver Finance ticker page](https://finance.naver.com/item/main.naver?code={ticker}) <br>
- [ClawHub skill page](https://clawhub.ai/Saebyeok-Im/equity-analyst-test) <br>
- [Saebyeok-Im publisher profile](https://clawhub.ai/user/Saebyeok-Im) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured markdown-style text report with numeric subscores, final score, verdict, and reasoning summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a 0-100 investment attractiveness score and BUY, BUY_LEAN, HOLD, or AVOID labels.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
