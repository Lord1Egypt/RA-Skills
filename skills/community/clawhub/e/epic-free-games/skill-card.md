## Description: <br>
Auto-claim free games from Epic Games Store with persistent login state and checkout automation. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[anlinxi](https://clawhub.ai/user/anlinxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to automate claiming weekly free games from Epic Games Store after completing a manual login. The skill is intended for users who understand the account, checkout, and terms-of-service risks of automated store actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates Epic Games Store account checkout actions, which may create account or terms-of-service risk. <br>
Mitigation: Use only if you accept the Epic account and terms-of-service risk, and review the order flow before relying on automation. <br>
Risk: The login flow saves browser authentication state in epic_auth.json. <br>
Mitigation: Protect epic_auth.json as sensitive account data, keep it out of public repositories and shared backups, and delete or regenerate it when no longer needed. <br>
Risk: The artifact includes Cloudflare anti-detection guidance and supports unattended cron execution. <br>
Mitigation: Avoid the anti-detection instructions and do not enable scheduled unattended claiming unless you are comfortable with automated account actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anlinxi/epic-free-games) <br>
- [Epic Games Store free games page](https://store.epicgames.com/zh-CN/free-games) <br>
- [agent-browser](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or use a local epic_auth.json browser state file when the user runs the login flow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
