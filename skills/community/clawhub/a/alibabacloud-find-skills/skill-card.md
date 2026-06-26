## Description: <br>
Searches, browses, and inspects Alibaba Cloud agent skills, then guides installation when the user requests it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find Alibaba Cloud skills by intent, keyword, or category; inspect relevant skill details; and install selected skills only when installation is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation examples can persistently add selected skills globally and skip confirmation. <br>
Mitigation: Install only when the user explicitly requests it; prefer interactive or project-local installation, and review the selected skill source before use. <br>
Risk: Search queries may be sent to the external AgentExplorer service. <br>
Mitigation: Avoid including secrets, credentials, personal data, or internal project details in search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-find-skills) <br>
- [AgentExplorer HTTP API reference](references/agentexplorer-api.md) <br>
- [Search examples](references/search-examples.md) <br>
- [Verification methods](references/verification-method.md) <br>
- [Curl shell compatibility guide](references/curl-shell-compatibility.md) <br>
- [Category examples](references/category-examples.md) <br>
- [Supported npx skills agents](references/npx-skills-agents.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include skill names, display names, descriptions, categories, install counts, detail summaries, and installation guidance.] <br>

## Skill Version(s): <br>
0.0.10 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
