## Description: <br>
Query headlines and articles from a self-hosted FreshRSS instance with category, time range, unread, and count filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users with a self-hosted FreshRSS account use this skill to retrieve latest, unread, category-specific, or recent headlines from their reader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses FreshRSS account credentials to authenticate to the user's server. <br>
Mitigation: Use HTTPS, configure a dedicated API password, and revoke that password when the skill is no longer needed. <br>
Risk: The skill can access feeds, categories, and headlines available to the configured FreshRSS account. <br>
Mitigation: Install only from a trusted publisher and use credentials scoped to the intended FreshRSS account. <br>


## Reference(s): <br>
- [FreshRSS Reader on ClawHub](https://clawhub.ai/nickian/freshrss-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text command output with setup and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FRESHRSS_URL, FRESHRSS_USER, and FRESHRSS_API_PASSWORD; category names are case-sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-01-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
