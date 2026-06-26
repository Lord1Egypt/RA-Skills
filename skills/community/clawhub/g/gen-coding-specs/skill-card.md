## Description: <br>
基于模板为当前工作空间生成完整技术编码规范，写入 docs/coding-specs/，供 gen-code 与其它技能消费。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lf951515851](https://clawhub.ai/user/lf951515851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze a workspace and generate project-specific coding standards under docs/coding-specs/. The generated Markdown gives gen-code, review-code, and human contributors a shared reference for API, architecture, data model, style, testing, security, performance, documentation, review, version-control, and Vue conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or update project coding-spec Markdown under docs/coding-specs/, which may affect later agent behavior and team conventions. <br>
Mitigation: Review the generated files before committing them or allowing other skills to rely on them. <br>
Risk: The broad trigger phrase "技术规范" may activate the skill when the user intended a narrower documentation discussion. <br>
Mitigation: Remove or narrow the broad trigger if accidental activation would be disruptive. <br>
Risk: Existing coding specifications can be overwritten when regeneration is confirmed or forced. <br>
Mitigation: Use the built-in existing-spec check and review diffs before accepting regenerated docs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lf951515851/gen-coding-specs) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Generation Workflow](artifact/prompt.md) <br>
- [Coding Specs Template Overview](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with optional shell commands and structured project guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes bounded coding-spec files under docs/coding-specs/ and asks before overwriting existing specs unless forced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact instructions mention 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
