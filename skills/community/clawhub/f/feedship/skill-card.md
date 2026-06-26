## Description: <br>
Manage RSS/Atom feeds, subscribe to websites, search and read articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanpeipan](https://clawhub.ai/user/yanpeipan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use Feedship to manage RSS and Atom subscriptions, fetch new articles, search saved content, discover feeds on websites, and inspect local feed storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external feedship package and its dependencies are installed and executed through the agent environment. <br>
Mitigation: Install only from trusted package sources, prefer a normal PyPI installation or a pinned release, and review the package and dependencies before deployment. <br>
Risk: Restricted-network setup can add global mirror exports to the user's shell profile. <br>
Mitigation: Avoid adding persistent mirror exports to ~/.bashrc unless the environment truly requires them; prefer scoped installation commands where possible. <br>
Risk: Scheduled fetching and semantic search can store subscribed feed metadata and article content locally. <br>
Mitigation: Use scheduling only for intended feeds, review local storage paths with feedship info, and manage retained feed and article data according to the deployment's privacy requirements. <br>


## Reference(s): <br>
- [Feedship ClawHub listing](https://clawhub.ai/yanpeipan/feedship) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, CLI output descriptions, and optional JSON output from supported commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to use the feedship CLI for feed management, article retrieval, search, discovery, scheduling, and system information.] <br>

## Skill Version(s): <br>
1.5.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
