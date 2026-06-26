## Description: <br>
Find email addresses for a domain by combining website scraping, search dorking, pattern guessing, DNS analysis, and SMTP verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and outreach teams use this skill for small, authorized domain lookups to find published or likely contact email addresses and inspect related email infrastructure signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts target websites, search or directory services, DNS infrastructure, and mail servers. <br>
Mitigation: Use it only for lawful, targeted lookups and avoid bulk prospecting. <br>
Risk: SMTP recipient checks can trigger rate limits, blocks, or IP reputation issues. <br>
Mitigation: Prefer --no-verify when SMTP verification is unnecessary and keep SMTP checks small and rate-limited. <br>
Risk: Page fetching disables HTTPS certificate verification. <br>
Mitigation: Use caution on untrusted networks and review results before relying on fetched content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying script prints JSON results to stdout and progress messages to stderr.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
