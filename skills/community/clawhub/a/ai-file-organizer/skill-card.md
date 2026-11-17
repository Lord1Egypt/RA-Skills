## Description:

AI File Organizer helps agents organize local files by category, rename copied outputs, find duplicate files, and export run reports through a command-line workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to organize directories, apply configurable naming and classification rules, move duplicate files into a duplicates folder, and generate JSON reports for file-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags this release as suspicious because it requests cloud or network credentials and advertises safety features that are not actually implemented.

Mitigation: Review the skill before installing, test it only on a disposable folder first, and avoid enabling cloud credentials or network permissions unless a reviewed cloud implementation is added.

Risk: Duplicate cleanup performs a real file-moving operation by moving duplicate files into a duplicate folder.

Mitigation: Run duplicate cleanup on test data first, back up important files, and inspect the duplicate folder before deleting or archiving moved files.

Risk: The documentation includes cron examples that could repeatedly organize folders without a human review step.

Mitigation: Do not schedule automated runs until the behavior, target paths, and report output have been verified for the intended directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/ai-file-organizer)
- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, YAML or JSON configuration examples, command-line text output, and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy files into categorized folders, move duplicate files into a duplicate folder, and write cache, log, or report files depending on the selected command and configuration.]

## Skill Version(s):

3.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json, and CHANGELOG dated 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
