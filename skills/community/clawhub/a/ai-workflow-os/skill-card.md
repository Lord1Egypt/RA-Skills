## Description: <br>
A bilingual AI workflow operating system that combines project lifecycle planning, project memory, task handoff, web and file intake, source filtering, knowledge-base governance, cross-source synthesis, and audit tracking into one unified skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and knowledge workers use this skill to structure project planning, preserve handoff-ready project memory, govern research and file intake, and synthesize knowledge across web, document, and local-file sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive materials could be archived or uploaded before review. <br>
Mitigation: Require explicit user confirmation before cloud upload or permanent archive; stage uncertain sources for review and keep audit records. <br>
Risk: Uploaded files, cloud documents, or OCR-derived content may be outdated, duplicated, confidential, or unverified. <br>
Mitigation: Classify each source type and trust level before intake; mark ambiguous or sensitive sources as review-required. <br>


## Reference(s): <br>
- [AI Workflow Operating System ClawHub listing](https://clawhub.ai/englandtong/ai-workflow-os) <br>
- [Migration Guide](references/migration-guide.md) <br>
- [Source Trust Levels](references/source-trust-levels.md) <br>
- [Usage Examples](references/usage-examples.md) <br>
- [Knowledge Record Schema](templates/knowledge-record-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured operational records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Docs/ project-memory, knowledge-governance, queue, index, and audit-log files when the user asks the agent to persist workflow state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
