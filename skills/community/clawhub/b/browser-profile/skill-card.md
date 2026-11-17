## Description:

Shortest English alias for site-profile / external-site-profile-learning. Use this when turning an already-proven site flow into a stable reusable external profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allens0104](https://clawhub.ai/user/allens0104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow authors use this skill to probe external sites, classify blocked or special-case flows, add reusable data-only site profiles when justified, and validate heuristic and Gemini planning behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alias is not self-contained and depends on the referenced external-site-profile-learning playbook.

Mitigation: Before installing or using it, confirm that the referenced playbook is available from the same trusted package or repository.

Risk: The skill is intended to probe sites and create reusable profiles, which can encode misleading behavior if the site flow was not validated.

Mitigation: Use it only for intended site-profile work and validate both heuristic and Gemini flows before reusing the profile.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allens0104/skills/browser-profile)
- [Publisher Profile](https://clawhub.ai/user/allens0104)
- [External Site Profile Learning Playbook](skills/external-site-profile-learning/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown instructions with text invocation templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for reusable data-only external site profiles; no code execution, credential handling, persistence, or hidden actions are included.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
