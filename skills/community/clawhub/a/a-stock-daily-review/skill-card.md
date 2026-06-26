## Description: <br>
Generates a nightly A-share market review with portfolio tracking, technical analysis, sector commentary, candidate stocks, and a next-day trading plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkx161](https://clawhub.ai/user/lkx161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short-term A-share investors and agent operators use this skill to draft daily market summaries, review holdings, track technical signals, and prepare a next-day action plan. It is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for private portfolio details and may send reports to WeChat without clearly documented privacy controls. <br>
Mitigation: Review before installing, use minimal or test portfolio data first, and confirm how credentials, report delivery, and data redaction are handled. <br>
Risk: The skill depends on other stock-analysis skills and produces trading recommendations that may be incomplete or incorrect. <br>
Mitigation: Review dependency skills separately and treat generated analysis as informational rather than investment advice. <br>
Risk: The artifact describes an automatic nightly task that could continue sending reports after setup. <br>
Mitigation: Verify the schedule, delivery destination, and disable procedure before enabling the skill in a live environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lkx161/a-stock-daily-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces financial analysis and trading-plan guidance that requires human review before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
