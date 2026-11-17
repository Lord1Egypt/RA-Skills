## Description:

Corpus Search helps agents search a corpus built with corpus-builder using semantic search and metadata filters for scene, emotion, pace, and quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agent workflows use this skill to retrieve relevant Chinese fiction corpus passages, filter results by metadata, and export matches for downstream writing or analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may change behavior or introduce dependency hygiene concerns over time.

Mitigation: Install in a virtual environment and review or pin dependency versions before use.

Risk: The skill reads local corpus directories and can export search results to user-selected paths.

Mitigation: Run it only against corpus directories and export paths you choose.

## Reference(s):

- [Corpus Search Skill Page](https://clawhub.ai/yuzhihui886/skills/corpus-search)
- [SKILL.md](artifact/SKILL.md)
- [Default Configuration](artifact/configs/default_config.yml)
- [Search Script](artifact/scripts/search_corpus.py)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text or JSON search results, with optional exported files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked corpus matches with similarity, metadata, and content previews.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
