## Description:

Builds concept, process, and case-application supervision datasets from markdown books or long markdown documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[technomad-ds](https://clawhub.ai/user/technomad-ds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset builders use this skill to convert markdown books or long documents into structured supervision data for concept QA, process QA, and case-application training. It is suited to book-to-SFT pipelines that need resumable batch work, chunk status tracking, validation, and coverage auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and transforms local markdown corpora, so pointing it at private or unrelated folders can expose or mix unintended content.

Mitigation: Install and run it only for corpora intended for transformation, and use a dedicated work directory.

Risk: Merge or coverage mistakes can leave supervision records without matching chunk status or can include merge output as one of the merge inputs.

Mitigation: Keep merge outputs separate from merge inputs, then inspect validation and coverage JSON reports for unprocessed chunks and mismatch previews.

## Reference(s):

- [Quality rubric](reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and JSON/JSONL file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces JSONL supervision batches, chunk status records, merged JSONL datasets, and validation/coverage JSON reports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
