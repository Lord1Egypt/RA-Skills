## Description:

Instant access to 100K+ nonfiction book summaries with 1-minute audio previews. Free demo key included — no signup needed. Search, browse, and listen via FizzRead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1997434](https://clawhub.ai/user/yang1997434)

### License/Terms of Use:


## Use Case:

External users use this skill to discover nonfiction book summaries, search or browse FizzRead recommendations, and request short audio preview links through an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if pasted into chat or printed while checking environment configuration.

Mitigation: Use a low-privilege FizzRead key, prefer environment configuration, and avoid printing or echoing secret values.

Risk: Responses can include external FizzRead download links that are not independently verified by the skill.

Mitigation: Treat generated download links as external destinations and review them before opening or sharing.

Risk: Shell commands include user-provided keys and search text in API calls.

Mitigation: Validate and encode user input before command execution, and avoid unsafe shell interpolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1997434/skills/fizzread-skill)
- [FizzRead](https://www.fizzread.ai)
- [FizzRead Skill API](https://skill.fizzread.ai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline links and curl command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on FizzRead API responses and may include external app download or audio preview links.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
