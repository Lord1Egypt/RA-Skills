## Description: <br>
Domain Monitor helps agents check domain expiration dates, WHOIS information changes, and SSL certificate status for domains the user provides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, webmasters, and domain investors use this skill to add domains to a local watchlist, inspect current WHOIS and SSL status, list monitored domains, and run checks across the watchlist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local whois and openssl checks against domains supplied by the user. <br>
Mitigation: Use explicit requests naming the domain to check, and review commands before execution when the target domain is sensitive. <br>
Risk: The skill saves a local watchlist in ~/.domain_monitor.json. <br>
Mitigation: Add only domains that are appropriate to store locally and remove or protect the watchlist according to local data-handling requirements. <br>
Risk: The security summary notes that triggers and permission disclosure could be clearer. <br>
Mitigation: Prefer direct invocations such as asking domain-monitor to check a named domain, and confirm expected local tool usage before enabling automated checks. <br>


## Reference(s): <br>
- [Domain Monitor ClawHub page](https://clawhub.ai/SxLiuYu/domain-monitor) <br>
- [SxLiuYu publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and plain-text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores the domain watchlist locally in ~/.domain_monitor.json and reports WHOIS and SSL check results for user-provided domains.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
