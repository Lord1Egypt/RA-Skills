## Description: <br>
Full-featured Confluence Cloud REST API v2 skill for managing pages, spaces, blog posts, attachments, comments, labels, and related Confluence resources through direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Confluence administrators use this skill to guide agent-assisted Confluence Cloud REST API work, including creating, reading, updating, deleting, and searching content across spaces, pages, attachments, comments, labels, users, and version history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for tenant-changing Confluence operations such as admin-key, invitation, delete, purge, and redact actions. <br>
Mitigation: Use least-privilege Atlassian API tokens and require explicit human approval before executing admin, invitation, delete, purge, redact, or other tenant-changing operations. <br>
Risk: The skill relies on direct Confluence Cloud API credentials in environment variables. <br>
Mitigation: Store CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, and CONFLUENCE_DOMAIN in the agent runtime secret manager and avoid exposing tokens in prompts, logs, or generated command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffersonling1217-png/confluence-atlassian) <br>
- [Publisher profile](https://clawhub.ai/user/jeffersonling1217-png) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, and CONFLUENCE_DOMAIN environment variables for authenticated examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
