## Description: <br>
Automates 12306 train-ticket login, search, and purchase workflows through a Playwright-based Python client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiyang2007](https://clawhub.ai/user/feiyang2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to work with Python-based 12306 login, ticket search, and booking automation for accounts they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates real 12306 account login and ticket-booking flows, including actions that may change an account or initiate a purchase. <br>
Mitigation: Use it only with an account you control, require explicit confirmation before any account-changing or purchase step, and prefer dry-run review before live execution. <br>
Risk: The automation can create or reuse local session-cookie files and relies on credential handling. <br>
Mitigation: Protect credentials and cookie files, do not commit or share them, and clear saved sessions when they are no longer needed. <br>
Risk: The release under-discloses account, purchase, and session-cookie risks. <br>
Mitigation: Review the source and security guidance before installing, and use a version that documents credential handling and confirmation safeguards when available. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/feiyang2007/12306-old) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill notes](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve browser automation, environment variables for credentials, and local session-cookie files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
