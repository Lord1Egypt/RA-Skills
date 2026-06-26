## Description: <br>
Generates Markdown reports from public mall.yy.com and gamemarket.yy.com game-account listing samples, including market trends, price distributions, and representative listing links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-lin](https://clawhub.ai/user/arc-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to inspect game-account market listings, recent listing activity, price ranges, and sample records for supported games. It is intended for market-level trend reports, not for valuing a single account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public web requests to mall.yy.com and gamemarket.yy.com. <br>
Mitigation: Use it only where requests to those domains are acceptable, and do not provide cookies, credentials, or browser session headers. <br>
Risk: Temporary JSON files may contain public listing samples used to build reports. <br>
Mitigation: Store sample files only as needed for traceability and remove them when the report no longer needs raw data. <br>
Risk: Listing-sample reports can be mistaken for full-market coverage or completed transaction prices. <br>
Mitigation: Treat reports as sampled asking-price analysis and keep the generated note that listings do not represent成交价 or the full market. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arc-lin/game-account-price-trends) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/arc-lin) <br>
- [mall.yy.com](https://mall.yy.com) <br>
- [gamemarket.yy.com](https://gamemarket.yy.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands] <br>
**Output Format:** [Markdown report generated from temporary JSON listing samples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sampled listing statistics, warning notes, and detail links when goodsId is present; raw JSON is not returned unless requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
