## Description: <br>
Buy and sell on Facebook Marketplace with pricing discipline, safer messaging, shipping guardrails, scam detection, and account-safe workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for practical Facebook Marketplace buying and selling support, including deal screening, listing and pricing help, safer messaging, shipping decisions, scam detection, and account-health workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Marketplace notes may contain personal location, pricing, transaction, or account-health context. <br>
Mitigation: Create and update ~/facebook-marketplace/ only after user consent, avoid sensitive personal details, and continue in stateless mode if persistence is declined. <br>
Risk: Live Facebook or Messenger actions can expose listing, message, and transaction data to Meta or affect the user's account. <br>
Mitigation: Require explicit user approval before signed-in Marketplace, Messenger, posting, messaging, payment, report, dispute, or appeal actions. <br>
Risk: Unsupported automation, mass messaging, scraping behind login, or restriction-bypass workflows can create account and policy risk. <br>
Mitigation: Keep irreversible or signed-in actions manual and explicit, refuse account evasion or anti-detection paths, and limit automation to user-approved read-only public-page research. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/facebook-marketplace) <br>
- [Skill Homepage](https://clawic.com/skills/facebook-marketplace) <br>
- [Facebook Marketplace](https://www.facebook.com) <br>
- [Messenger](https://www.messenger.com) <br>
- [Facebook Help](https://www.facebook.com/help) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with local note templates and concise action plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain user-approved local notes under ~/facebook-marketplace/; no binaries or API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
