## Description:

Provides correct pronunciation guides for complex drug generic names, including IPA transcriptions and SSML-compatible audio generation markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, clinicians, educators, and developers can use this skill to generate pronunciation guidance for supported medication names with IPA, syllable breakdowns, emphasis markers, and optional SSML output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional JSON export path can overwrite arbitrary writable files.

Mitigation: Run the skill in a sandbox and avoid absolute, traversal, or important existing output paths until exports are restricted to a dedicated workspace directory and silent overwrites are prevented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/drug-pronunciation)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON or plain terminal text, depending on command options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports detailed, simple, and IPA-only output formats, plus optional JSON file export.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
