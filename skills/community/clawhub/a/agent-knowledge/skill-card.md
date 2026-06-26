## Description: <br>
Agent Knowledge Capture provides unified local capture and retrieval for URLs, external content extracts, social posts, and agent research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to save URLs, extracts, posts, and research notes as searchable local markdown entries for later retrieval and source tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The executable installed as scripts/know was not included in the reviewed artifact. <br>
Mitigation: Confirm the installed know executable is trusted before running the skill. <br>
Risk: Knowledge entries may contain sensitive or secret material in local markdown files. <br>
Mitigation: Keep KNOWLEDGE_DIR pointed at a dedicated notes folder and avoid storing secrets. <br>
Risk: Automatic cleanup can modify local knowledge files. <br>
Mitigation: Run know tidy in audit mode before know tidy --fix and only schedule automatic cleanup after verifying its changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianderrington/agent-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with YAML frontmatter and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and maintains a local markdown knowledge directory and INDEX.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
