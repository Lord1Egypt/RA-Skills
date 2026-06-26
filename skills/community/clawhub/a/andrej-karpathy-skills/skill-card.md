## Description: <br>
Behavioral guidelines for coding agents that reduce common LLM coding mistakes by encouraging explicit assumptions, simple implementations, focused edits, and verifiable success criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding-agent users apply this skill when writing, reviewing, or refactoring code so the agent surfaces assumptions, avoids overcomplication, limits changes to the task, and verifies outcomes against clear success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional npm or clone installation can modify agent instruction files, and --force or --global can overwrite or persist instructions beyond one project. <br>
Mitigation: Review the target agent file before installation and use --force or --global only when intentionally replacing or installing persistent instructions. <br>


## Reference(s): <br>
- [Andrej Karpathy observation on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876) <br>
- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/andrej-karpathy-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional inline shell commands for installing agent instruction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides behavioral instructions for coding agents and optional installer commands; it does not require credentials or external API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
