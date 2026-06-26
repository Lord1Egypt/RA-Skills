## Description: <br>
Search, browse, and manage Audible audiobooks, including catalog search, library and wishlist views, title details, and confirmed purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeathridge](https://clawhub.ai/user/ryandeathridge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Audible users and their agents use this skill to authenticate with Audible, search for audiobooks, inspect account library and wishlist data, retrieve title details, and execute a purchase only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored Audible authentication can grant access to account data. <br>
Mitigation: Protect ~/.config/audible/auth.json like a password, keep owner-only permissions, and re-authenticate or remove the file when access should be revoked. <br>
Risk: Runtime dependency installation can fetch packages into the execution environment. <br>
Mitigation: Run the skill in a virtual environment with reviewed versions of audible and httpx already installed. <br>
Risk: Purchase commands can spend Audible credits or money if the wrong title or marketplace is selected. <br>
Mitigation: Verify the exact title, ASIN, narrator, marketplace, and cost with the user before running any buy command with --confirm. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryandeathridge/clawdible-audiobooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses may be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one-time Audible authentication and explicit confirmation before purchase commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
