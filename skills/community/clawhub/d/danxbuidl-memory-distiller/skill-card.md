## Description:

Distill repeated user preferences, successful patterns, and durable working rules into reusable memory notes or prompt-ready context blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danxbuidl](https://clawhub.ai/user/danxbuidl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to convert conversation history, task outcomes, or existing memory notes into concise, evidence-backed memory rules and reusable prompt context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated memory notes may preserve sensitive personal details or one-off preferences if stored without review.

Mitigation: Review generated memory before storing it and remove sensitive, temporary, or non-durable items.

Risk: Weak signals could be over-converted into durable user preferences.

Mitigation: Keep only explicit, repeated, or clearly generalizable evidence; mark uncertain candidates as tentative or exclude them.

## Reference(s):

- [Output Format Guide](references/output-format.md)
- [Example Prompts](references/example-prompts.md)
- [ClawHub Skill Page](https://clawhub.ai/danxbuidl/skills/danxbuidl-memory-distiller)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections or concise prompt-ready text blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are user-directed memory notes, cleaned lists, review reports, or reusable context blocks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
