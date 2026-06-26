## Description: <br>
Controls AdGuard Home DNS filtering through its HTTP API to check domains, manage allowlists and blocklists, view status and statistics, toggle protection, and clear DNS cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rowbotik](https://clawhub.ai/user/rowbotik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and network operators use this skill to administer an AdGuard Home instance from the command line. It supports routine DNS filtering tasks such as checking filtered domains, changing custom rules, viewing statistics, toggling protection, and clearing DNS cache. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials could be sent to an unintended AdGuard Home host if the URL is not explicitly configured. <br>
Mitigation: Set ADGUARD_URL to the intended AdGuard Home address and verify the host before running commands that authenticate. <br>
Risk: Allow, block, toggle, and cache-clear commands can change DNS filtering behavior. <br>
Mitigation: Require explicit user approval before running commands that alter rules, protection state, or cache. <br>
Risk: The status command accesses DNS query-log data while reporting summary statistics. <br>
Mitigation: Avoid status checks in sensitive environments unless query-log access is appropriate for the user and deployment. <br>


## Reference(s): <br>
- [AdGuard Home API Reference](references/api.md) <br>
- [Official AdGuard Home API documentation](https://github.com/AdguardTeam/AdGuardHome/wiki/API) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured AdGuard Home URL and admin credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
