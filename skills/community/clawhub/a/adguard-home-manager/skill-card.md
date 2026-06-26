## Description: <br>
Manage AdGuard Home network-wide DNS ad blocking. Query blocklist stats, add/remove custom DNS rules, check filtering status, and view top blocked domains from your self-hosted DNS server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and self-hosted infrastructure administrators use this skill to inspect AdGuard Home DNS filtering status, review blocking statistics, manage custom rules, and toggle network-wide filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive DNS activity through AdGuard Home statistics and query-log access. <br>
Mitigation: Install only where the agent is allowed to view network DNS activity, and use a dedicated account with the least privilege AdGuard Home supports. <br>
Risk: The skill can change network-wide filtering behavior and custom DNS rules. <br>
Mitigation: Require review before allowing rule changes or filtering toggles, and review scripts/rules.sh before enabling add or remove actions. <br>
Risk: Unsafe endpoint choices can expose credentials or administrative traffic. <br>
Mitigation: Prefer HTTPS or a strictly local AdGuard Home endpoint for ADGUARD_BASE_URL. <br>


## Reference(s): <br>
- [AdGuard Home project](https://github.com/Adguard/AdGuardHome) <br>
- [AdGuard Home overview](https://adguard.com/adguard-home/overview.html) <br>
- [AdGuard Home web interface API documentation](https://github.com/AdguardTeam/AdGuardHome/wiki/Config#web-interface) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADGUARD_USERNAME, ADGUARD_PASSWORD, ADGUARD_BASE_URL, curl, and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
