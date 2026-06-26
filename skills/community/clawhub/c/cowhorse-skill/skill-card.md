## Description: <br>
A skill that actively extracts and quantifies workflow requirements from users through structured Q&A about inputs, outputs, and objectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SPA3K](https://clawhub.ai/user/SPA3K) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn repeatable AI-assisted tasks into clarified workflow requirements and reusable skills. It guides discovery, confirms inputs and outputs, outlines build steps, and can produce skill structure, scripts, references, packaging guidance, and memory-update guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation or modification of skill files, scripts, packages, and memory entries. <br>
Mitigation: Review target paths, generated scripts, packaged output, and any memory updates before approving build or finalize steps. <br>
Risk: Incomplete or incorrect requirements could be turned into a reusable workflow skill. <br>
Mitigation: Confirm the structured input, output, process, and constraint summary with the user before building or relying on the generated skill. <br>


## Reference(s): <br>
- [Workflow Patterns Reference](references/workflow_guide.md) <br>
- [Cowhorse Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with structured summaries, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated skill-file structure, scripts, references, packaging steps, and memory-update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
