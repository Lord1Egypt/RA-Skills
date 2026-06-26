## Description: <br>
Create a new skill through a guided conversation for authoring skills from scratch, choosing quick or full guidance, analyzing documentation for behavior patterns, generating a functional skill workflow, and explaining how to activate it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohaoxing](https://clawhub.ai/user/xiaohaoxing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create new AgentSkills-compatible skills through a concise, CLI-style guided conversation. It helps collect purpose, triggers, tools, workflow, outputs, constraints, install location, and confirmation before writing skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist generated skill files, which may introduce incorrect triggers, workflow steps, tool use, or constraints into future agent behavior. <br>
Mitigation: Review the generated trigger conditions, tools, workflow, constraints, and file preview before confirming writes; scan the generated skill before deployment. <br>
Risk: Documentation-derived workflows can omit context or transform source material into unsuitable behavioral instructions. <br>
Mitigation: Verify extracted installation commands, CLI usage, configuration parameters, limitations, and expected outputs against the source documentation before using the generated skill. <br>
Risk: Installing at shared scope can make a generated skill available across projects where its behavior may not be appropriate. <br>
Mitigation: Prefer workspace scope unless shared availability is intentional. <br>


## Reference(s): <br>
- [Create New Skill release page](https://clawhub.ai/xiaohaoxing/create-new-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown skill files, CLI-style prompts, summaries, previews, and activation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SKILL.md and README.md only after user confirmation; stops and asks if the destination directory already exists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
