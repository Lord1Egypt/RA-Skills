## Description: <br>
Bookmark Intelligence monitors X bookmarks, fetches linked article content, analyzes it with AI or keyword matching, and surfaces project-relevant insights through local storage and optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkrigmo1](https://clawhub.ai/user/bkrigmo1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn X bookmarks and linked articles into searchable, project-aware summaries, actionable items, and notifications. It is intended for personal or team bookmark intelligence workflows across free, pro, and enterprise tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles reusable X session cookies that can provide account access if exposed. <br>
Mitigation: Treat the .env file as a password file, keep it local with restrictive permissions, rotate cookies if exposure is suspected, and avoid sharing logs or configuration that may contain credentials. <br>
Risk: Daemon mode can continuously fetch, analyze, and retain bookmark-derived content. <br>
Mitigation: Use daemon mode only when continuous monitoring is intended, review the storage location regularly, and stop the PM2 process when monitoring is no longer needed. <br>
Risk: Bookmark content and linked article text may be sent to LLM providers or notification services when AI analysis and integrations are enabled. <br>
Mitigation: Disable LLM analysis or notifications for sensitive bookmarks, review provider settings before use, and limit project context to information that is acceptable to process externally. <br>
Risk: Payment and admin scripts add operational risk around license issuance and payment handling. <br>
Mitigation: Use test mode during evaluation, keep payment configuration private, verify payment provider settings before production use, and restrict admin-script access to trusted operators. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bkrigmo1/bookmark-intelligence) <br>
- [Publisher Profile](https://clawhub.ai/user/bkrigmo1) <br>
- [README](README.md) <br>
- [Skill Documentation](SKILL.md) <br>
- [Sample Analysis](examples/sample-analysis.json) <br>
- [Sample Notification](examples/sample-notification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON configuration, and JSON bookmark-analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analyzed bookmark records to a local knowledge base and send notification summaries when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
