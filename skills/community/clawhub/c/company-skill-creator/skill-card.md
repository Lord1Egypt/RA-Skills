## Description: <br>
Create company-internal skills interactively for internal workflows, APIs, business processes, or tools by guiding users through requirements, documentation, scripts, references, validation, and packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opentouchtouch](https://clawhub.ai/user/opentouchtouch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and internal operations teams use this skill to turn company-specific process knowledge, API details, schemas, templates, and scripts into reusable agent skills. It is intended for creating and packaging internal workflow or integration skills while clearly flagging inferred information for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide live credentials, secrets, private connection strings, or sensitive production data while describing internal APIs or workflows. <br>
Mitigation: Provide redacted documentation and authentication-flow descriptions instead of live secrets, and review generated files before installing or sharing the resulting skill. <br>
Risk: Generated scripts, references, or trigger descriptions may contain inferred company-specific behavior that has not been verified by a subject matter expert. <br>
Mitigation: Review and correct generated files, especially sections flagged for confirmation, before packaging or deploying the skill. <br>


## Reference(s): <br>
- [Company Context Template](references/company-context.md) <br>
- [Interviewer Agent](agents/interviewer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown skill files with supporting code, references, shell commands, and packaged skill artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content may include inferred sections that require user review before installation or sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
