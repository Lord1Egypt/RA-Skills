## Description: <br>
Fetches recent Binance Square-style posts, filters out verified and institutional accounts, and prints summaries with author, publish time, view count, and comment count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taibaiup](https://clawhub.ai/user/taibaiup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts can use this skill to inspect recent retail discussion topics from Binance Square-style data and review a compact table of post activity. It is intended for retrieving public-style market discussion summaries, not for account-specific Binance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a disclosed external bmwweb.cc endpoint to retrieve Binance Square-style data. <br>
Mitigation: Install only if external requests to that endpoint are acceptable in the target environment. <br>
Risk: Adding personal Binance cookies, tokens, or account credentials could expose account-specific data. <br>
Mitigation: Use only the disclosed public-style request headers unless the skill is re-reviewed for credentialed use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taibaiup/binancesquare) <br>
- [Disclosed Binance Square-style endpoint](https://www.bmwweb.cc/bapi/composite/v9/friendly/pgc/feed/feed-recommend/list) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints up to 15 filtered posts sorted by comment count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
