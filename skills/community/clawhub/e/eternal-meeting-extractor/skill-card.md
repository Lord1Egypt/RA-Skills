## Description:

Extracts summaries, decisions, action items, key points, questions, and attendees from meeting transcripts or notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse meeting notes or transcripts into concise summaries, decisions, action items, open questions, and attendee lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting-language heuristics may over-trigger on unrelated meeting-like wording.

Mitigation: Review extracted summaries, decisions, and action items against the original transcript before relying on them.

Risk: Some advertised output modes are incomplete.

Mitigation: Use the text or JSON output paths as primary outputs and verify Markdown or follow-up behavior before workflow integration.

Risk: Meeting transcripts may contain sensitive information.

Mitigation: Provide only intended local transcript files and handle generated summaries according to the user's data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-meeting-extractor)
- [Publisher profile](https://clawhub.ai/user/eternal0404)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Plain text summary or JSON object; Markdown output is advertised but uses the same formatter as text in the artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local transcript file and emits extracted meeting fields without network access or persistence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
