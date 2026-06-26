## Description: <br>
Search and manage Confluence pages and spaces using confluence-cli. Read documentation, create pages, and navigate spaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[francisbrero](https://clawhub.ai/user/francisbrero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, support engineers, and documentation maintainers use this skill to search, read, create, update, and export Confluence pages and spaces from an agent session through confluence-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party CLI that can access Confluence content using an Atlassian API token. <br>
Mitigation: Install confluence-cli only if you trust the package and grant the token only the Confluence permissions needed for the task. <br>
Risk: Confluence credentials and local CLI configuration can expose account access if mishandled. <br>
Mitigation: Treat the Atlassian API token and ~/.confluence-cli/config.json as sensitive secrets and avoid sharing them in prompts, logs, or repositories. <br>
Risk: Create and update commands can change Confluence pages or place content in the wrong space or page. <br>
Mitigation: Review page IDs, space keys, parent pages, and generated content before allowing create, create-child, or update commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/francisbrero/confluence) <br>
- [confluence-cli project](https://github.com/pchuri/confluence-cli) <br>
- [confluence-cli npm package](https://www.npmjs.com/package/confluence-cli) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires confluence-cli and a CONFLUENCE_TOKEN or configured Atlassian API token.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
