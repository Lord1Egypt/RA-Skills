## Description:

Guides an agent through planning, drafting, validating, and archiving long-form serialized novels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn)

### License/Terms of Use:

BSD 3-Clause

## Use Case:

Novelists and writing teams use it to plan and draft serialized novels, track characters and continuity, validate manuscripts, and prepare archives with character data and an HTML guide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign, medium-confidence scan notes ambiguous archive write boundaries and incomplete review of some referenced paths.

Mitigation: Review archive destinations and referenced files before running the workflow, and keep archive operations within the intended project tree.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshinejnjn/skills/epic-novel-writer)
- [Skill homepage](https://clawhub.ai/sunshinejnjn/epic-novel-writer)
- [Novel lifecycle workflow](references/lifecycle.md)
- [Project structure](references/project-structure.md)
- [Archive template](references/archive-template.md)
- [Chapter blueprint template](references/chapter-blueprint-template.md)
- [Character card template](references/character-card-template.md)
- [World setting template](references/world-setting-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Guidance]

**Output Format:** [Novel manuscripts and planning or validation documents in Markdown; character data in JSON; archive guide pages in HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The project language follows the user's preference; chapter files use global continuous numbering.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata; artifact VERSION and frontmatter report 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
