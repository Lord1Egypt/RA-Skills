## Description:

Generates PPT presentations through SkillBoss API Hub with smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create PowerPoint presentations from a topic, optionally selecting a template style or letting the workflow choose one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPT topics are sent to the external SkillBoss API Hub service.

Mitigation: Avoid confidential, private, regulated, or sensitive material unless the service privacy terms have been reviewed and accepted.

Risk: The inspected artifact only contains SKILL.md while the documented workflow depends on Python scripts.

Mitigation: Verify the required scripts are present in the installed package before using the skill.

Risk: PPT generation depends on a SkillBoss API key.

Mitigation: Provide the API key only through the expected SkillBoss_API_KEY environment variable and manage it as a secret.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis-ai-ppt-generator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PPT URL after streaming generation completes; generation may take 2-5 minutes.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
