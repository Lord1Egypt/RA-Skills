## Description:

Records baby daily care data from paper form photos or conversational descriptions, including temperature, jaundice, bathing, weight, sleep, feeding, diaper changes, symptoms, and notes, then stores the data as local JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cake-26](https://clawhub.ai/user/cake-26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill in Chinese to capture, update, query, and summarize a baby's daily care records from natural-language notes or confirmed photo extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file handling can read, overwrite, or delete JSON files outside the intended data folder.

Mitigation: Validate dates and paths, confine file access to the configured data directory, and review filesystem behavior before installation.

Risk: Permanent deletion of sensitive baby-care records is under-disclosed.

Mitigation: Require explicit user confirmation before saving or deleting sensitive records and clearly disclose destructive actions.

## Reference(s):

- [Baby daily data field schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese conversational responses with JSON-backed local record files and occasional markdown tables or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill saves one JSON file per day and can merge incremental updates into existing daily records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
