## Description: <br>
Automate George online banking (Erste Bank / Sparkasse Austria): login/logout, list accounts, and fetch transactions via Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate George banking workflows for Erste Bank and Sparkasse Austria, including interactive login, account and portfolio retrieval, transaction export, and data-carrier upload or signing. It is intended for trusted environments where the user can personally approve 2FA and banking actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive banking account data. <br>
Mitigation: Run it only in a private workspace on a trusted machine and share outputs only with systems approved to handle financial data. <br>
Risk: The skill caches banking session tokens and browser state. <br>
Mitigation: Run logout after each workflow and protect the workspace where george session files are stored. <br>
Risk: The skill can initiate data-carrier uploads and signing flows. <br>
Mitigation: Personally verify each upload and signing approval in the George mobile app before confirming it. <br>
Risk: Debug mode may write raw financial payloads. <br>
Mitigation: Avoid --debug unless troubleshooting requires raw payloads, and remove debug files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/george) <br>
- [Skill homepage](https://github.com/odrobnik/george-skill) <br>
- [Setup](SETUP.md) <br>
- [Unified Banking Schema](docs/unified-banking-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; script commands can emit human-readable text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cached session state under workspace/george and temporary exports under /tmp/openclaw/george.] <br>

## Skill Version(s): <br>
1.5.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
