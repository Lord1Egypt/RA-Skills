## Description: <br>
Helps developers discover, compare, switch, and check free AI model resources through CLI-oriented guidance and configuration examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, students, and small-project builders use this skill to find free AI model options, switch model configuration, test connectivity, and understand limits before relying on a provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to install or run an external free-finder CLI that changes model configuration. <br>
Mitigation: Verify the package source before installation and back up existing model configuration before running switch, import, export, or reset commands. <br>
Risk: Using free model providers can send prompts or data to third-party APIs. <br>
Mitigation: Use scoped API keys and avoid sending secrets, regulated data, or confidential project content to free model providers. <br>
Risk: Free model providers can have rate limits, downtime, or changing availability. <br>
Mitigation: Run connectivity checks before relying on a selected model and keep fallback options for non-critical workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/free-resource-finder-free) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest commands that install or run an external CLI, update model configuration, and contact third-party model provider APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
