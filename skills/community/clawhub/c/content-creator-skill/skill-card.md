## Description:

Meta-skill for orchestrating humanizer, de-ai-ify, copywriting, and tweet-writer to produce high-quality, platform-ready content that sounds authentic and human while preserving factual integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to turn explicit topic, audience, goal, voice, and author-context inputs into platform-ready LinkedIn copy and an X thread adaptation. It is intended for persuasive social content that preserves factual integrity and avoids fabricated anecdotes, guaranteed virality claims, or manipulative tactics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands and a broad update command can change dependencies or unrelated installed skills over time.

Mitigation: Pin ClawHub and required skill versions, avoid update --all, and install only reviewed versions in a least-privileged environment.

Risk: The skill depends on four separate upstream writing skills, so output quality and behavior depend on the installed versions of those skills.

Mitigation: Verify the installed humanizer, de-ai-ify, copywriting, and tweet-writer versions before use and review their behavior for the intended deployment.

Risk: Generated persuasive content can include unsupported claims if the user does not provide sufficient factual context.

Mitigation: Collect explicit author context and constraints before drafting, and review final copy for factual support, fabricated anecdotes, and overpromised outcomes.

## Reference(s):

- [Content Creator Skill Page](https://clawhub.ai/h4gen/skills/content-creator-skill)
- [Publisher Profile](https://clawhub.ai/user/h4gen)
- [ClawHub Homepage](https://clawhub.ai)
- [Inspected Upstream Skills](references/inspected-skills.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sections containing final LinkedIn copy, edit summary, persuasion structure, a five-tweet X thread, and optional hooks and closing questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user inputs before drafting and depends on locally installed humanizer, de-ai-ify, copywriting, and tweet-writer skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
