## Description: <br>
Distills chat history, photos, social posts, or user descriptions into an AI buddy skill with Vibe Memory, Persona, and update workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, list, update, roll back, and delete personalized buddy skills from provided descriptions or imported personal materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process private chats, photos, and descriptions through an external EvoLink API. <br>
Mitigation: Review privacy tradeoffs before installation, use synthetic or redacted material where possible, and do not upload another person's material without permission. <br>
Risk: Generated buddy files and source materials may persist locally after creation or updates. <br>
Mitigation: Review generated buddy files before use and remove stored source materials that should not be retained. <br>
Risk: Untrusted imports and generated helper behavior may introduce unsafe or unwanted content into buddy skills. <br>
Mitigation: Avoid processing untrusted imports until API helper and write safeguards are tightened, and scan generated skills before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/evolinkai/buddy-skill-creator) <br>
- [Configured homepage](https://github.com/EvoLinkAI/buddy-skill-for-openclaw) <br>
- [EvoLink Claude Messages API documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=buddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions, generated skill files, JSON metadata, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update buddy skill directories containing SKILL.md, vibe.md, persona.md, meta.json, version archives, and stored source materials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
