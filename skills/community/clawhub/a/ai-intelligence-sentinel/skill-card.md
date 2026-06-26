## Description: <br>
AI前沿哨兵 tracks public AI and big-data industry signals and helps generate morning, evening, and daily intelligence reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaopengs](https://clawhub.ai/user/xiaopengs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, product managers, data leaders, and executives use this skill to collect public AI, open-source, academic, social, and big-data industry signals and turn them into structured intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad public web collection and arbitrary feed fetching can expose the agent to untrusted content or misleading sources. <br>
Mitigation: Run in an isolated environment, pin dependencies, and review custom RSS or source URLs before fetching them. <br>
Risk: Optional credentials, including Twitter/X bearer tokens, may be mishandled if entered into unsafe storage locations. <br>
Mitigation: Prefer environment variables or secrets-file storage, avoid placing secrets in USER.md or MEMORY.md, and do not enter a Twitter/X bearer token in the web UI unless necessary. <br>
Risk: The follow-builders integration executes a separate skill path and adds another trust boundary. <br>
Mitigation: Do not enable the integration unless that separate skill and its scripts have been reviewed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaopengs/ai-intelligence-sentinel) <br>
- [API setup guide](artifact/references/api_setup.md) <br>
- [Information source guide](artifact/references/sources_guide.md) <br>
- [Big data insight requirement](artifact/docs/BIGDATA_INSIGHT_REQUIREMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with supporting text, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report templates cover AI morning/evening reports, big-data daily reports, and Xiaohongshu-style summaries.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
