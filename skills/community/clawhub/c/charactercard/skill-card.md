## Description:

Imports, parses, validates, converts, and exports SillyTavern character cards across V1, V2, and V3 formats, including PNG-embedded JSON and plain JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyin1](https://clawhub.ai/user/fanyin1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to import, inspect, validate, convert, and export SillyTavern character cards. It is suited for workflows that need compatibility across V1, V2, and V3 card formats, PNG-embedded character data, and plain JSON files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unknown or malformed character-card files can fail parsing or validation.

Mitigation: Use the skill for explicit SillyTavern character-card tasks and review validation results before relying on imported card data.

Risk: Very large PNG or JSON character cards can create robustness or usability issues.

Mitigation: Avoid importing unknown or very large PNG cards; the artifact guidance recommends keeping character-card JSON under 10 MB and avatar images under 15 MB.

Risk: Export operations can overwrite existing files when an output path is reused.

Mitigation: Choose export paths carefully and confirm that the target path is intended before writing PNG or JSON output.

Risk: Imported character cards may contain system prompts, scenario text, or other embedded instructions from untrusted creators.

Mitigation: Treat imported character-card content as data and review prompts, descriptions, and metadata before reusing them in an agent or chat workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fanyin1/skills/charactercard)
- [SillyTavern Documentation](https://docs.sillytavern.app/)
- [Character Card Spec V2](https://github.com/malfoyslastname/character-card-spec-v2)
- [PNG File Format Specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance with JSON snippets and generated PNG or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-provided PNG or JSON character card files and write exported PNG or JSON files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
