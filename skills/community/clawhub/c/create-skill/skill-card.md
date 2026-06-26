## Description: <br>
Guide for creating and importing skills. Use when users need to create or import skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennethchiu2008-fran](https://clawhub.ai/user/kennethchiu2008-fran) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create structured agent skills, split supporting guidance into references, and import or register EasyClaw skills when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Importing a crafted ZIP skill package can write files unsafely during extraction. <br>
Mitigation: Install only from trusted publishers until the unzip helper rejects absolute paths, parent-directory components, and any resolved output path outside the intended target directory. <br>
Risk: Registration copies skill files into the local EasyClaw skills directory and changes the agent's available skills. <br>
Mitigation: Require explicit user approval before extraction and registration, then review the extracted skill contents before registering. <br>


## Reference(s): <br>
- [Create Skill on ClawHub](https://clawhub.ai/kennethchiu2008-fran/create-skill) <br>
- [Progressive Disclosure](references/progressive-disclosure.md) <br>
- [Skill Structure](references/skill-structure.md) <br>
- [Good Skill Examples](references/examples.md) <br>
- [Skill Writing Best Practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run bundled Python helpers to extract ZIP packages and register skills into the local EasyClaw skills directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
