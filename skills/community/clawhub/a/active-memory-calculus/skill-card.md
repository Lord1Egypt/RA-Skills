## Description:

Active Memory for Calculus Teaching captures calculus learning preferences, concept mastery, and error patterns to personalize tutoring and generate study summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT

## Use Case:

Educators, tutors, and learning-agent developers use this skill to maintain student-specific calculus memory, adapt explanations and difficulty, warn about repeated mistakes, and summarize learning progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores and reuses student learning data, including preferences, mastery signals, error patterns, and session-derived summaries.

Mitigation: Use it only with explicit student or administrator consent, document what is collected, and provide a process to inspect and delete stored profiles and summaries.

Risk: Persistent memory, transcript, dream-summary, and knowledge-graph files may contain sensitive student records.

Mitigation: Set a dedicated private memory directory, avoid shared or cloud-synced storage, and apply retention controls appropriate for the classroom or institution.

Risk: Weak path-safety controls and student identifier handling can expose or mix records if deployed without guardrails.

Mitigation: Validate student identifiers, constrain file paths to the approved memory directory, and review configuration before use with minors or regulated student records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daigxok/skills/active-memory-calculus)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Structured JSON memory context, Markdown-style dream summaries, and plain-text tutoring guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist student profiles, recent memories, dream summaries, and knowledge-graph files under the configured memory directory.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
