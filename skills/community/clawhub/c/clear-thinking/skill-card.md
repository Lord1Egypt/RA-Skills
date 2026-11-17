## Description:

Critical thinking skills and decision-making frameworks for evaluating conflicting information, making difficult decisions, spotting manipulation or misinformation, and thinking more clearly about problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate claims, recognize manipulation, compare incomplete information, and make clearer personal or professional decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access for a primarily reasoning-oriented workflow.

Mitigation: Review the skill before installation and grant filesystem access only in environments where the skill has a clear need for it.

Risk: The install command uses an unpinned npx package invocation.

Mitigation: Prefer a pinned, trusted installer version and verify the package source before installation.

Risk: Decision-making and misinformation guidance can be misapplied when context is incomplete or culturally specific.

Mitigation: Treat the output as critical-thinking support, seek primary sources where possible, and adapt examples to the user's local media and decision context.

## Reference(s):

- [Clear Thinking ClawHub page](https://clawhub.ai/howtousehumans/skills/clear-thinking)
- [First Draft / Credibility Coalition](https://firstdraftnews.org)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with checklists, decision frameworks, and structured prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt examples to the user's media landscape, culture, and decision context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
