## Description:

Track fishing spots, gear, catches, and conditions with personalized recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to maintain a fishing journal, track spots, catches, conditions, and gear inventory, and receive personalized fishing recommendations based on that history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fishing history, precise locations, gear inventory, and optional license notes may be recorded in local files.

Mitigation: Review what is stored under ~/fishing before sharing files or recording sensitive locations or personal details.

Risk: Recommendations may become inaccurate if local catch logs, spot notes, gear inventory, or regulation notes are stale.

Mitigation: Keep local memory files current and verify local regulations before relying on trip or tackle recommendations.

## Reference(s):

- [ClawHub Fishing skill page](https://clawhub.ai/ivangdavila/skills/fishing)
- [Fishing skill homepage](https://clawic.com/skills/fishing)
- [Memory Setup - Fishing](artifact/memory-template.md)
- [Species Guide - Fishing](artifact/species.md)
- [Tackle Reference - Fishing](artifact/tackle.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command snippets and local Markdown file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain local Markdown memory files under ~/fishing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
