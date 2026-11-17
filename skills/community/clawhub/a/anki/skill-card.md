## Description:

Builds and repairs Anki decks, including card writing, FSRS and SM-2 deck options, leeches, review workload, imports, and sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create importable Anki cards from source material, tune deck scheduling, diagnose retention and backlog problems, and handle Anki import, sync, backup, and troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards or import settings could introduce incorrect or misleading study material.

Mitigation: Review generated cards and import settings before importing them into an Anki collection.

Risk: Destructive Anki operations or one-way sync decisions could lose review history, media, or collection data.

Mitigation: Make a current .colpkg or other off-machine backup and confirm what will be overwritten before following destructive advice.

Risk: The skill may keep Anki preferences and study context in local files under ~/Clawic/data/anki/.

Mitigation: Review config.yaml and memory.md in that directory if local preference persistence is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/anki)
- [Clawic Anki skill page](https://clawic.com/skills/anki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with TSV, CSV, Markdown, or Anki note content when generating cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Anki preference files under ~/Clawic/data/anki/; does not directly modify the user's Anki collection.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
