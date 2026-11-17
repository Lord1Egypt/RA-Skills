## Description:

Monitors social conversations and sentiment around brands, topics, or industries by searching tweets and discussions to surface insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, communications, and growth teams use this skill to monitor brand, topic, industry, or competitor conversations and synthesize directional sentiment, key voices, themes, and opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-style search examples can mishandle untrusted brand or topic text if an agent interpolates user input into commands naively.

Mitigation: Pass search terms as inert arguments in a runtime or tool wrapper instead of constructing shell commands from raw user text.

Risk: Product marketing context files may contain sensitive internal plans that could be used during social-search work.

Mitigation: Review `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md` for sensitive content before allowing the skill to use that context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-social-listening)
- [Publisher profile](https://clawhub.ai/user/mariokarras)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, quotes, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sentiment volumes are approximate and based on sampled search results.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
