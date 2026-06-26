## Description: <br>
ByteRover helps agents query and curate project memory with the `brv` CLI, storing project patterns, decisions, and architectural rules under `.brv/context-tree` through a configured LLM provider. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qxbcn](https://clawhub.ai/user/qxbcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve existing project knowledge before work and save durable implementation patterns or decisions after work. It also guides LLM provider setup and optional cloud sync for shared ByteRover spaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, curation text, and attached file contents may be sent to the configured LLM provider. <br>
Mitigation: Require explicit approval before querying or curating sensitive context, avoid secrets, and review provider settings before use. <br>
Risk: Cloud sync can send local knowledge to ByteRover cloud spaces. <br>
Mitigation: Use cloud sync only with authenticated, intended spaces and require approval before running `brv push`, `brv pull`, or `brv space` commands. <br>
Risk: Agent-managed project memory can persist incorrect or sensitive facts in `.brv/context-tree`. <br>
Mitigation: Review stored Markdown before committing or sharing it and decide whether `.brv` belongs in version control for the project. <br>
Risk: The skill depends on the external `byterover-cli` package. <br>
Mitigation: Verify the package source and installed version before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qxbcn/byterover-2-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to run `brv query`, `brv curate`, provider setup, and optional cloud sync commands; curation can attach up to 5 project-scoped files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json version is 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
