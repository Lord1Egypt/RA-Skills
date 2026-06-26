## Description: <br>
Command-line tool to create, list, and retrieve Notion pages using the Notion API with JSON output for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this CLI to create pages, list database pages, retrieve page details, and check Notion API status through a user-supplied Notion integration key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion API key can expose pages and databases shared with the integration. <br>
Mitigation: Use a dedicated least-privilege Notion integration, share only the required workspace content, and keep NOTION_API_KEY out of logs and repositories. <br>
Risk: The create-page command can add content to important Notion workspaces. <br>
Mitigation: Supervise create-page use in sensitive workspaces and restrict the integration to the target database. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaising-openclaw1/cli-notion) <br>
- [Artifact README](artifact/README.md) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON emitted by command-line operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion API key and access to pages or databases shared with the integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
