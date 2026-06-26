## Description: <br>
Helps agents guide ClawHub OAuth login on headless servers by obtaining authorization URLs, checking login status, and managing the local ClawHub token through the ClawHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengwuzhi](https://clawhub.ai/user/mengwuzhi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill on headless servers to complete ClawHub CLI OAuth login without launching a local browser. It guides the user through manual authorization, login verification, and logout when token cleanup is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth callback URLs and the local ClawHub token can grant account access if exposed. <br>
Mitigation: Use the skill only in a trusted terminal, do not share callback URLs or ~/.clawhub/token, and rotate the token by logging in again if exposure is suspected. <br>
Risk: The skill runs the clawhub executable found on PATH. <br>
Mitigation: Verify that the installed clawhub CLI is legitimate before use, especially on shared or newly provisioned systems. <br>


## Reference(s): <br>
- [ClawHub Login Helper page](https://clawhub.ai/mengwuzhi/clawhub-login) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [clawhub_login.py](artifact/scripts/clawhub_login.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal guidance with inline shell commands and OAuth URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display OAuth authorization URLs and local login status; treats token files and callback URLs as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, README.md, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
