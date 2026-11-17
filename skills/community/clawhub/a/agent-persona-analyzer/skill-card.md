## Description:

Generates a fictional agent persona profile and self-introduction using randomized MBTI, gender presentation, psychological age, career interests, traits, and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcdjl](https://clawhub.ai/user/tcdjl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill when they want an agent to answer self-introduction, personality-test, capability, gender, age, or style prompts with a persistent fictional persona. Reviewers should confirm that this broad trigger behavior is desired before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can unexpectedly answer broad prompts such as capability or analysis requests with a fictional dating-style self-introduction.

Mitigation: Use explicit opt-in triggers and label persona output as fictional before enabling the skill for normal assistant workflows.

Risk: The skill may persist and reuse a persona profile file in the workspace root.

Mitigation: Document the created file, validate profile contents before reuse, and provide reset or delete controls for agent-persona-name.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tcdjl/skills/agent-persona-analyzer)
- [Publisher profile](https://clawhub.ai/user/tcdjl)
- [questionnaires.md](references/questionnaires.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown-style conversational text and a persistent JSON persona profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reuse agent-persona-name.json in the workspace root.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
