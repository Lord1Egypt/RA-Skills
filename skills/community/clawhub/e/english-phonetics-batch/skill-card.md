## Description:

English Phonetics Batch helps agents batch annotate English word lists with American IPA pronunciations, check existing phonetic entries, and save results in text, CSV, or Markdown formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe1984](https://clawhub.ai/user/pe1984)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and content maintainers use this skill to convert English vocabulary files into pronunciation-annotated outputs and to repair corrupted or missing IPA entries in existing word lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input words are sent to a public dictionary API.

Mitigation: Avoid sensitive internal vocabulary lists or replace the lookup source with an approved internal or offline dictionary before sensitive use.

Risk: The script writes to a user-selected output path.

Mitigation: Review output paths before execution and use versioned or temporary destinations when preserving existing files matters.

Risk: The skill depends on the unpinned requests package range from requirements.txt.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pe1984/skills/english-phonetics-batch)
- [Usage examples](artifact/references/usage-examples.md)
- [API notes and IPA reference](artifact/references/api-notes.md)
- [Free Dictionary API](https://dictionaryapi.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated text, CSV, or Markdown vocabulary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated entries include word, American IPA phonetic text, part of speech when available, and a validity flag for CSV output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
