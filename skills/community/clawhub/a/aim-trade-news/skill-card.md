## Description: <br>
Queries recent foreign trade news from the last 1 to 3 days and returns AI-generated titles and summaries for trade news, import/export policy updates, and international trade information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[focus-aim](https://clawhub.ai/user/focus-aim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve recent foreign trade news, import/export policy updates, and international trade information. It is not intended for domestic news, entertainment news, or real-time stock, currency, or exchange-rate market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide an AEP authorization token and can save it locally in a .env file. <br>
Mitigation: Use only a dedicated, low-privilege AEP token, prefer a managed secret store or manual local setup, and rotate or delete the token when no longer using the skill. <br>
Risk: The skill performs live network requests to the AEP Gateway trending_hub API and may return API errors or unavailable results. <br>
Mitigation: Run the credential self-check before use, review returned error messages, and avoid relying on the output for real-time market, currency, or stock decisions. <br>


## Reference(s): <br>
- [AEP credential setup guide](references/aep-setup.md) <br>
- [AEP token registration](https://tools.mentarc.cn/aim-skills/) <br>
- [ClawHub listing](https://clawhub.ai/focus-aim/aim-trade-news) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown summary backed by JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns AI-generated titles, summaries, publish dates, source links, update time, and result count for a 1, 2, or 3 day window.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
