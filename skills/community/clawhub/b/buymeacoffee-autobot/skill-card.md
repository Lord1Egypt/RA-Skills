## Description: <br>
Automates Buy Me a Coffee and Ko-fi creator-page workflows by drafting content updates, thanking supporters, promoting pages, and tracking earnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators use this skill to plan and generate automation for monetized Buy Me a Coffee or Ko-fi pages, including content posting, supporter thank-you flows, cross-promotion, and earnings summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use account credentials for monetized creator platforms. <br>
Mitigation: Store credentials in a secure secret manager, avoid plaintext credential files, and grant access only to accounts you explicitly approve. <br>
Risk: Automated posting, messaging, and promotion can send public or supporter-facing content without adequate review. <br>
Mitigation: Require manual review before posts, thank-you messages, or promotional messages are published or sent. <br>
Risk: Browser automation and earnings scraping may affect creator accounts and platform compliance. <br>
Mitigation: Limit automation to approved accounts and platforms, and confirm the workflow aligns with the applicable platform rules before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/buymeacoffee-autobot) <br>
- [Buy Me a Coffee](https://buymeacoffee.com) <br>
- [Ko-fi](https://ko-fi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets and configuration file outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser-automation scripts and account credential environment variable names; generated actions should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
