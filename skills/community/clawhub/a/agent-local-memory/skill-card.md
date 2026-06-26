## Description: <br>
Persistent local memory system for AI agents across conversations using local Markdown files and zero external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyu-hu](https://clawhub.ai/user/siyu-hu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent save preferences, project context, behavior feedback, and reference notes locally so future conversations can resume with relevant context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory can retain sensitive or stale information across conversations. <br>
Mitigation: Periodically inspect the memory directory, remove stale or sensitive entries, and avoid storing secrets, credentials, private keys, or regulated personal information. <br>
Risk: A broad memory index can cause future sessions to surface irrelevant or outdated notes. <br>
Mitigation: Follow the skill's index maintenance guidance: scan MEMORY.md before writing, update existing entries when possible, and trim or merge old entries when the index grows too large. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with example memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory conventions and prompts for agents; no network calls or credentials are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
