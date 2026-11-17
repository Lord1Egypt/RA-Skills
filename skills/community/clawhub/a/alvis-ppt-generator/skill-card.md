## Description:

Generate PPT with SkillBoss API Hub. Smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate PowerPoint presentations from a topic, either by choosing a template style or by letting the skill select a suitable template automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics and supplied content may be sent to SkillBoss API Hub for generation.

Mitigation: Avoid submitting confidential business, personal, or regulated information unless organizational policy permits that external processing.

Risk: The release evidence references scripts, but the packaged artifact evidence only contains SKILL.md.

Mitigation: Verify that the package includes the referenced scripts before relying on the skill for end-to-end PPT generation.

Risk: PowerPoint generation can take several minutes and depends on the external API returning completion status.

Mitigation: Use a sufficient timeout and wait for the final status with is_end set to true before treating the output URL as complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis-ppt-generator)
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the SkillBoss_API_KEY environment variable; final generation returns a PowerPoint URL when complete.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
