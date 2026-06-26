## Description: <br>
Queries public GitHub release pages and changelogs to report latest versions and recent changes for Claude Code, OpenClaw, and NousResearch Hermes Agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzx0](https://clawhub.ai/user/jzx0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check current versions, release notes, and recent update history for selected AI agent tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad update or version wording could trigger the skill in the wrong context. <br>
Mitigation: Ask the user to specify the exact tool when the request is ambiguous. <br>
Risk: Upgrade commands may be mistaken for commands to execute immediately. <br>
Mitigation: Present upgrade commands as references and run them only after explicit user approval. <br>
Risk: Public GitHub release pages or changelog files may be unavailable, incomplete, or too large to fetch fully. <br>
Mitigation: Report unavailable sources, keep fetches bounded, and use the defined changelog fallback when release details are insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jzx0/ai-agent-tools-version-changelog) <br>
- [Claude Code releases](https://github.com/anthropics/claude-code/releases) <br>
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases) <br>
- [OpenClaw changelog](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md) <br>
- [Hermes Agent releases](https://github.com/nousresearch/hermes-agent/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown version summaries, release tables, and optional upgrade command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public GitHub release pages and changelog files; no credential environment variables were detected in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
