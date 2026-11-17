## Description: <br>
Afrexai Knowledge Management Free helps agents capture unstructured notes or documents as structured knowledge entities and relationships, query those relationships, and surface related knowledge from a local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, teams, and automation users can use this skill to capture meeting notes, project documents, technical decisions, and natural-language questions as structured knowledge entries and relationship-based answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read, write, and exec authority can affect local files or run commands. <br>
Mitigation: Review proposed reads, writes, and commands before approval, and run the skill in a sandboxed workspace. <br>
Risk: Inconsistent API, callback URL, and local-only storage guidance can create unclear data flows. <br>
Mitigation: Use non-sensitive documents unless storage locations, callback URLs, and external API behavior are explicitly configured and approved. <br>
Risk: Knowledge extraction and relationship reasoning can produce incorrect, stale, or overconfident links. <br>
Mitigation: Validate captured entities, sources, confidence values, and relationship paths before using outputs for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/afrexai-knowledge-management-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and possible shell command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file reads, writes, or command execution; review before approving actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
