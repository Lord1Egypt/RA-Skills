## Description: <br>
Helps agents plan and run Chinese website data scraping workflows with platform-specific Scrapling guidance, adaptive selector patterns, compliance boundaries, and a helper script for supported public search pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to draft scraping approaches, selector strategies, Scrapling configurations, and optional shell-driven extraction runs for Chinese websites. It is intended for legitimate, authorized data collection with legal and platform-compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses anti-bot behavior, login-cookie scraping, and platform-specific scraping techniques that could be misused against sites where the user lacks authorization. <br>
Mitigation: Use it only for legitimate, authorized scraping; prefer approved APIs; and do not bypass login walls, paywalls, platform defenses, or terms that prohibit the activity. <br>
Risk: Cookies and tokens used for scraping are sensitive credentials and may expose accounts or private access if mishandled. <br>
Mitigation: Treat cookies and tokens as secrets, keep them out of prompts, logs, commits, and shared files, and rotate or revoke them after use. <br>
Risk: Scraping can collect personal data, copyrighted material, gated content, or data subject to local legal restrictions. <br>
Mitigation: Collect only necessary public or explicitly permitted data, avoid private personal data and copyrighted redistribution, anonymize when appropriate, and complete legal review before commercial use. <br>


## Reference(s): <br>
- [ClawHub cn-data-scraper](https://clawhub.ai/lm203688/cn-data-scraper) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>
- [Scrapling Chinese Documentation](https://github.com/D4Vinci/Scrapling/blob/main/docs/README_CN.md) <br>
- [Camoufox](https://github.com/nicegamer7/camoufox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and optional JSON output from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script accepts a platform, keyword, and optional output path, then writes JSON with the platform, keyword, source URL, extracted content count, and preview text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
