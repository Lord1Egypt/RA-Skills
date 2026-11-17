## Description:

Captures quick post-experience ratings for restaurants, hotels, trips, events, or meetings and stores them as Fulcra annotations for a personal preference graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keng009](https://clawhub.ai/user/keng009)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-agent operators use this skill to capture a fast, low-friction rating after an experience and save structured notes, scores, tags, and companions into Fulcra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships broader credentialed Fulcra and CRM utilities than the quick rating workflow requires.

Mitigation: Review before installing, run only in a trusted agent environment, and remove or isolate unused Attio, health/calendar, historical-read, update, and delete utilities when only rating capture is needed.

Risk: Credentialed API endpoint overrides could redirect requests away from expected Fulcra or Attio services.

Mitigation: Keep default API base settings, avoid custom API base environment variables, and pin the Fulcra CLI version used by the runtime.

Risk: Ratings, companions, and free-text notes can contain sensitive personal preference and relationship data.

Mitigation: Keep outputs private, avoid using the skill in public or group contexts, and use dry-run review when the user has not clearly confirmed what should be stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-post-experience-rater)
- [Publisher profile](https://clawhub.ai/user/keng009)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a Fulcra Post-Experience Rating annotation after user confirmation; supports dry-run previews through the bundled save command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
