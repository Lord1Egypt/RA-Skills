## Description: <br>
Helps an agent maintain personal local skill files by detecting reusable session knowledge, checking for similar skills, drafting proposed skill changes, and applying them only after explicit approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drjzhou](https://clawhub.ai/user/drjzhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to identify reusable local skill material from conversations, compare it with existing skills, and draft reviewed skill creations or updates before any approved file changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable skill edits can change future agent behavior or preserve sensitive information. <br>
Mitigation: Review every proposed path, full skill text, and diff before approval, and keep secrets, private URLs, customer details, and credentials out of saved skills. <br>
Risk: Skill proposals may introduce incorrect guidance, surprising capabilities, scripts, or third-party integrations. <br>
Mitigation: Require explicit user approval before writing, installing, enabling, or materially rewriting skills, and make the purpose of any scripts or tool integrations visible in the skill text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drjzhou/autoskill-local-skill-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, proposed file contents, diffs, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before creating, updating, deleting, installing, or enabling skill files.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
