## Description:

Audit and rewrite content to remove AI-generated feel by stripping markdown artifacts, eliminating AI vocabulary patterns, flagging hallucination risks, and restoring natural human voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to audit AI-sounding drafts, remove common formatting and vocabulary artifacts, flag claims that need verification, and produce more natural revised copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can flag hallucination risks, but the evidence says not to rely on it for factual verification, hallucination detection, scoring, or a complete audit.

Mitigation: Review rewritten content manually and verify factual, legal, pricing, version, statistical, and comparative claims against authoritative sources before publication.

Risk: The local helper script can write to a caller-selected output path, which may overwrite an existing file.

Mitigation: Choose a new output filename or back up existing files before running the script with an output path.

## Reference(s):

- [Human Voice Checklist](references/human-voice-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/skills/geo-human-editor)
- [GEOLY AI Publisher Profile](https://clawhub.ai/user/geoly-geo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown audit with rewritten text, issue notes, scores, summaries, and optional local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads a local input file and can write the rewritten content to a caller-selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
