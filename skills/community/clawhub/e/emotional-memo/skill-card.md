## Description:

A shared emotional memo for relationships — records emotional moments and gently reminds before old wounds are touched.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zj-zc](https://clawhub.ai/user/zj-zc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to keep a local relationship memo: initialize a shared notebook, record emotional events, surface related prior entries, translate difficult feelings, review timelines, update status, and detect recurring patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores relationship notes, names, triggers, and follow-ups in data/memo.json, which can contain sensitive private information.

Mitigation: Use nicknames, avoid unnecessary details, protect the workspace, and delete or secure data/memo.json when the history is no longer needed.

Risk: Relationship conflict, abuse, self-harm, persistent despair, or safety concerns may exceed the skill's role as a memo and translator.

Mitigation: Follow the artifact boundary to avoid diagnosis or taking sides and gently suggest professional support for abuse, self-harm, persistent despair, or safety concerns.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown conversation responses and local JSON records in data/memo.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local data/memo.json file containing relationship notes, triggers, emotions, statuses, follow-ups, and detected patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
