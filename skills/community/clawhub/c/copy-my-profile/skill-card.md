## Description: <br>
Extract a standardized cross-tool user profile from an AI agent's long-term memory so it can be reused in another AI tool without retraining. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-tool users use this skill to export instructions, identity, profession, projects, and preferences from one agent's memory into a portable Markdown profile for another agent or AI tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated profile may consolidate sensitive details from AI memory or configuration files. <br>
Mitigation: Review and redact my-profile.md before saving it in synced folders, committing it, or importing it into another tool's long-term memory. <br>
Risk: Using the skill requires allowing the agent to read local AI memory and configuration files. <br>
Mitigation: Install and run it only when that access is acceptable, and limit provided files when using the paste-based fallback path. <br>


## Reference(s): <br>
- [Copy My Profile on ClawHub](https://clawhub.ai/songhonglei/copy-my-profile) <br>
- [Profile Template](references/profile-template.md) <br>
- [AI Tools Memory File Map](references/tools-memory-map.md) <br>
- [Import Prompts](references/import-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown profile file and inline Markdown response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes ./my-profile.md and asks for confirmation before overwriting an existing profile file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
