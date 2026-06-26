## Description: <br>
Creates and manages SubAgents for development, research, writing, and data-analysis tasks, including creation, listing, guidance, and termination workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aning35](https://clawhub.ai/user/aning35) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to create task-specific SubAgents, choose preset roles, and manage their lifecycle through documented commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SubAgents may receive overly broad instructions or run longer than intended. <br>
Mitigation: Prefer run mode for one-off tasks, give SubAgents narrow instructions, review logs, and terminate sessions when finished. <br>
Risk: Secrets or sensitive information could be shared with spawned SubAgents. <br>
Mitigation: Avoid sharing secrets with SubAgents and review their instructions before use. <br>
Risk: The README references a separate script that is not included in this bundle. <br>
Mitigation: Review any separate script independently before using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aning35/create-subagent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command, prompt, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SubAgent task prompts, labels, mode choices, management commands, and configuration checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
