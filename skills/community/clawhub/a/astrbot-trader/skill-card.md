## Description: <br>
Astrbot Trader defines a crypto trading assistant persona for monitoring OKX positions, preparing backtest-based trading recommendations, and drafting market content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers can use this skill to guide an agent through recurring crypto portfolio checks, OKX-related trading operations, backtesting-driven recommendations, and market-content drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports apparent live OKX credentials in the skill content. <br>
Mitigation: Rotate exposed credentials before use and replace embedded secrets with secure runtime secrets. <br>
Risk: The security review reports broad recurring financial-account activity without enough safeguards. <br>
Mitigation: Require explicit user approval before account access, order placement, or other trading operations, and apply account-level trading limits. <br>
Risk: The skill behavior includes promotional outreach drafting for customer development. <br>
Mitigation: Review outreach manually before sending and follow the target platform's rules and applicable marketing requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sg345662365-oss/astrbot-trader) <br>
- [Publisher profile](https://clawhub.ai/user/sg345662365-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or concise text with trading checks, trade recommendations, configuration notes, and content drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account-check steps and outreach copy when permitted by runtime tools and explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
