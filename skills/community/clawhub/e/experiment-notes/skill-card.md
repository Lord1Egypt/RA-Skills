## Description:

Track, search, and learn from experiments. Automatic logging of trial-and-error, success/failure patterns, and distilled lessons. Prevents repeating mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record experiment attempts, search prior failures or fixes, review local statistics, and distill repeated lessons into reusable guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local experiment notes may expose secrets, tokens, credentials, private customer data, authentication headers, or raw error dumps if users or agents log sensitive content.

Mitigation: Configure agents and users to avoid logging sensitive data, review entries before saving, and periodically delete or protect ~/.openclaw/memory/experiments/ on shared machines or backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/besty0121/skills/experiment-notes)
- [Agent Integration Snippet](templates/agents-snippet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [CLI text output, Markdown integration snippets, and local JSONL records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores experiment and lesson history locally under ~/.openclaw/memory/experiments/.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
