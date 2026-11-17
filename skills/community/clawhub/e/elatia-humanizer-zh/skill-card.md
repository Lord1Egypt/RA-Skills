## Description:

Humanizer-zh rewrites Chinese text to reduce common AI-writing patterns and make prose sound more natural while preserving the intended meaning and tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0122](https://clawhub.ai/user/ken0122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing teams use this skill to polish, rewrite, and humanize Chinese emails, copy, articles, reports, and AI-generated drafts. It is intended for prose editing workflows where the user asks for more natural wording rather than strict formal preservation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate local narrative-voice instruction file that is outside the reviewed package.

Mitigation: Review that dependency before installation, or remove or inline the reference so all behavior is contained in the reviewed package.

Risk: The skill can rewrite Chinese prose more aggressively than a normal proofreader.

Mitigation: Use it for humanizing and style-editing tasks where substantive rewriting is acceptable, and review the rewritten text before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken0122/skills/elatia-humanizer-zh)
- [Publisher profile](https://clawhub.ai/user/ken0122)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with rewritten Chinese prose, quality scores, and concise change notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a before-and-after comparison table when requested by the user.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
