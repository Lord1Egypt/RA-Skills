## Description:

Masks selected phone numbers, email addresses, ID numbers, long digit strings, and specified names before text is shared with AI, returning masked text and match counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users preparing text for an AI service can mask supported identifiers and specified names, then inspect the masked text and a count of replacements before sharing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared permissions do not match file and command access, and the tool grants are broader than needed.

Mitigation: Review the manifest before installation and limit access to necessary local files and script execution; remove or justify WebFetch and other excess grants.

Risk: Documented command flags and output schema differ from the actual script, which can disrupt integrations.

Mitigation: Check the script's --help and test --file or --text with --json before relying on its output.

Risk: Pattern-based masking covers only supported identifiers and explicitly supplied names; sensitive text may remain.

Mitigation: Review masked output for remaining sensitive information before sharing it with an AI service.

## Reference(s):

- [Data Minimizer ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/data-minimizer)
- [LGD governance theory linked in the README](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Masked text and replacement counts on standard output, optionally as JSON; masked text may also be written to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON includes masked_text, counts, and out; numeric masks retain some original digits.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
