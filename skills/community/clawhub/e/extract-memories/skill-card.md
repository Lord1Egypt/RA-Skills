## Description: <br>
Extracts durable user decisions, preferences, project constraints, and references from a conversation into memory topic files and an index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jofiction918](https://clawhub.ai/user/jofiction918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture durable memory from completed conversations, including preferences, decisions, project constraints, and external references, while filtering temporary task state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation details as long-term memories without a clear review or approval step. <br>
Mitigation: Review extracted memories before saving and avoid storing secrets, account identifiers, private URLs, internal paths, or confidential project details. <br>


## Reference(s): <br>
- [Extract Memories ClawHub page](https://clawhub.ai/jofiction918/extract-memories) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown status summary plus memory topic files with YAML frontmatter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends to memory/topics/ and MEMORY.md; intended memories should be reviewed before saving.] <br>

## Skill Version(s): <br>
3.0.10 (source: server release metadata; artifact frontmatter states 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
