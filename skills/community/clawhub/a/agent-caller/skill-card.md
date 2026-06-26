## Description: <br>
Call 179 professional agents on demand from a local prompt catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[717986230](https://clawhub.ai/user/717986230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to search, browse, and retrieve preconfigured specialist agent prompts for coding, strategy, design, marketing, testing, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled prompt catalog includes high-impact capabilities such as wallet use, purchases, transaction signing, and OAuth-token workflows. <br>
Mitigation: Treat retrieved prompts as untrusted templates; grant scoped tools only after explicit approval and keep payment, credential, and transaction actions behind human review. <br>
Risk: Package documentation includes unsafe credential-sharing guidance. <br>
Mitigation: Use only official browser login or local CLI token entry, and do not share ClawHub API tokens with a skill author, assistant, or chat. <br>
Risk: Retrieved prompts may introduce unsafe or unsuitable instructions into downstream agents. <br>
Mitigation: Review prompts before deployment and require environment and tool restrictions for email, posting, persistent memory, credentials, and other sensitive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/717986230/agent-caller) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/717986230) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python dictionaries or CLI text containing agent metadata and prompt content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The catalog contains 179 bundled agent prompts across 15 categories and can return full prompt text for downstream agent use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
