## Description: <br>
Fetches up to five currently live Kalshi sports markets with game names and probabilities using a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanakamedalasumanth](https://clawhub.ai/user/kanakamedalasumanth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent browse Kalshi live sports markets and summarize up to five games with their probabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live market probabilities can change quickly or be extracted incorrectly from the browser session. <br>
Mitigation: Independently verify market information on Kalshi before relying on it, especially before making financial decisions. <br>
Risk: A user request could push the workflow beyond its intended read-only scope into login, credential handling, or trading. <br>
Mitigation: Use the skill only for browsing and summarizing public market information, and stop if account access, credentials, or order placement are requested. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kanakamedalasumanth/get-kalshi-live-games) <br>
- [Kalshi](https://kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text or Markdown list with game names and probabilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limited to up to five currently live games; does not trade, log in, or handle credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
