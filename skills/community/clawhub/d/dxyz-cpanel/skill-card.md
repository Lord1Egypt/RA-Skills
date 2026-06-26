## Description: <br>
Manage cPanel/WHM hosting accounts and server resources through WHM API, UAPI, and legacy cPanel API 2 command and script examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picodozbotdoz](https://clawhub.ai/user/picodozbotdoz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hosting administrators use this skill to generate cPanel/WHM API calls, helper shell commands, and configuration guidance for account, DNS, email, database, SSL, file, backup, and bandwidth administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer real cPanel/WHM servers, including destructive account, DNS, email, database, restore, and password-change operations. <br>
Mitigation: Use it only for intended live administration, require manual confirmation for destructive changes, and review each generated command before execution. <br>
Risk: API tokens and credentials can grant broad server control if over-permissioned, stored insecurely, or pointed at the wrong host. <br>
Mitigation: Use least-privilege, IP-restricted tokens; verify CPANEL_HOST targets the intended HTTPS server; avoid plain long-lived config secrets; and rotate or audit tokens regularly. <br>
Risk: Example passwords and command parameters may be copied into real operations without environment-specific validation. <br>
Mitigation: Replace all example credentials and parameters with approved values, enforce local password policy, and test non-destructive read operations before writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/picodozbotdoz/dxyz-cpanel) <br>
- [API reference](references/api-reference.md) <br>
- [Quick reference](references/quick-reference.md) <br>
- [Error codes](references/error-codes.md) <br>
- [Version 134 changes](references/version-134-changes.md) <br>
- [cPanel API documentation](https://api.docs.cpanel.net/) <br>
- [cPanel 134 release notes](https://docs.cpanel.net/release-notes/134-release-notes/) <br>
- [Upgrade to cPanel & WHM 134](https://docs.cpanel.net/installation-guide/upgrade-to-cpanel-whm-134/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, cPanel/WHM API examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that call live cPanel/WHM APIs and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
