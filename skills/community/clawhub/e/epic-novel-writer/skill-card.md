## Description:

Novel writing full workflow from world-building and character design to chapter planning, manuscript writing, validation, version archiving, and HTML guide generation for medium to super-long serialized novels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, editors, and AI-assisted writing teams use this skill to structure long-form serialized novel projects, maintain global chapter numbering, draft and validate chapters, and create archive packages with character data and HTML navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive and reverse-merge workflows can create many files or overwrite files under the active manuscript directory.

Mitigation: Confirm archive and reverse-merge prompts carefully, verify the target scope and destination, and back up the active manuscript before reverse-merge.

Risk: Archive operations may use shell commands with user-provided titles or paths.

Mitigation: Sanitize titles with the documented allowlist, quote path expansions, verify destinations remain inside the archive root, and prefer file tools when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshinejnjn/skills/epic-novel-writer)
- [Project structure](references/project-structure.md)
- [Lifecycle workflow](references/lifecycle.md)
- [Naming rules](references/name-rules.md)
- [Archive template](references/archive-template.md)
- [World setting template](references/world-setting-template.md)
- [Character card template](references/character-card-template.md)
- [Chapter blueprint template](references/chapter-blueprint-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown project files, manuscript text, JSON character data, HTML guide files, validation reports, and shell command proposals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow the user's project language; the workflow documentation is primarily Chinese with an English README.]

## Skill Version(s):

1.2.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
