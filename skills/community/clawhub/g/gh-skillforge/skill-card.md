## Description: <br>
Generate valid, ClawHub-ready SKILL.md files from product metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use Skillforge to turn product metadata, instructions, optional environment variables, and optional binary requirements into ClawHub-ready SKILL.md content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SKILL.md content may carry incorrect or unsuitable instructions when the input instructions come from an untrusted source. <br>
Mitigation: Review and scan generated SKILL.md files before publishing or deployment. <br>
Risk: Use requires installing Python dependencies and running a local FastAPI server. <br>
Mitigation: Install only if the dependency set is acceptable for the target environment and run the server locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/gh-skillforge) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, text] <br>
**Output Format:** [JSON response containing generated SKILL.md Markdown and a normalized slug.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SKILL.md content can include optional environment variable and binary requirement declarations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
