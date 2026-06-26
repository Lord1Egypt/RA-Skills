## Description: <br>
Creates a local Codegirl agent skill from chat logs, GitHub activity, code snippets, photos, and user notes, generating coding memory and persona files that can evolve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmlans](https://clawhub.ai/user/xmlans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create and maintain local personalized pair-programming companion skills from private chat, code, and media evidence for personal reflection and coding support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive chats, photos, locations, and relationship or personality notes locally. <br>
Mitigation: Use only data you have permission to process, keep generated files private, and review or remove sensitive content before enabling the generated skill. <br>
Risk: Generated personas may present themselves as a real person, creating impersonation or unhealthy attachment risks. <br>
Mitigation: Treat outputs as simulation, do not use them to contact or impersonate a real person, and stop or seek support if use becomes obsessive. <br>
Risk: Generated .agents rules or SKILL.md content may introduce unsafe or misleading behavior. <br>
Mitigation: Review generated files and run security scans before deployment; do not enable rules that override privacy, consent, or safety boundaries. <br>


## Reference(s): <br>
- [ClawHub release: Codegirl Skill](https://clawhub.ai/xmlans/codegirl-skill) <br>
- [ClawHub publisher profile: xmlans](https://clawhub.ai/user/xmlans) <br>
- [Artifact README_EN.md](artifact/README_EN.md) <br>
- [Artifact INSTALL.md](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and generated skill files with JSON metadata and optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local gfs/{slug}/ memory, persona, meta, and SKILL files; may parse local chat, code, and image metadata inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
