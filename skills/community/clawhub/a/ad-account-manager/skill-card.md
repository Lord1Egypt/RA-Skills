## Description: <br>
Manage ad accounts for Guangdiantong and Ocean Engine through browser automation with cookie-based login, account switching, and account status overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang259797](https://clawhub.ai/user/wang259797) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and agents use this skill to manage saved Guangdiantong and Ocean Engine ad accounts, open browser login sessions, and review basic account status such as balance, daily spend, budget, and abnormal-account alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable ad-platform login cookies are saved locally in plaintext. <br>
Mitigation: Install only on a trusted machine, restrict filesystem access to the skill data directory, and treat stored account data like passwords. <br>
Risk: Saved cookies may continue to grant ad-platform access after the original login session. <br>
Mitigation: Delete saved accounts when they are no longer needed and rotate or revoke sessions from the ad platform if a workspace may have been exposed. <br>
Risk: Browser automation can open authenticated advertiser or agency consoles with sensitive budget and spend information. <br>
Mitigation: Use the skill only from private workspaces and avoid shared, synced, or backed-up directories unless cookie storage is encrypted or moved to an OS credential store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang259797/ad-account-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Interactive command-line text with locally stored JSON account data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Launches a Playwright Chromium session for QR-code login and cookie-based account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
