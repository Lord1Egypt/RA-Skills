## Description: <br>
FreshBooks CLI for managing invoices, clients, and billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haseebuchiha](https://clawhub.ai/user/haseebuchiha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to install and operate a FreshBooks CLI for OAuth setup, client management, invoice creation, invoice updates, invoice archiving, and billing lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify FreshBooks clients, invoices, and billing records. <br>
Mitigation: Confirm with the user before running commands that create invoices, update clients or invoices, or archive invoices. <br>
Risk: OAuth credentials and refreshed tokens grant access to the connected FreshBooks account. <br>
Mitigation: Use credentials only for the intended account, keep local token storage protected, and run the logout command when stored credentials should be removed. <br>
Risk: The release installs a third-party npm package. <br>
Mitigation: Verify the npm package and publisher before installation. <br>


## Reference(s): <br>
- [FreshBooks CLI ClawHub release](https://clawhub.ai/haseebuchiha/freshbooks-cli) <br>
- [haseebuchiha publisher profile](https://clawhub.ai/user/haseebuchiha) <br>
- [GitHub Package Registry](https://npm.pkg.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands produce JSON to stdout; billing mutations should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
