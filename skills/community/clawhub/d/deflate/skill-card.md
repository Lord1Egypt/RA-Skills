## Description:

Intelligent context compression for OpenClaw agents that tracks topics, recommends /new versus /compact, and uses Cornell-MapReduce style summaries to preserve important session details while reducing token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thevibestack](https://clawhub.ai/user/thevibestack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage long OpenClaw sessions, decide when to start a new chat or compact context, and preserve key project details in memory before reducing context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may preserve secrets or credentials exactly during compression or memory flushes.

Mitigation: Require redaction rules for API keys, tokens, passwords, session cookies, private keys, and other secrets before using the skill.

Risk: The skill may write broad conversation details into persistent memory files without enough scoping or consent.

Mitigation: Use explicit opt-in for memory writes, restrict memory file locations, and avoid shared or source-controlled workspaces unless data handling is reviewed.

Risk: Compressed summaries can omit or distort context that the user still needs.

Mitigation: Review compression output before relying on it, verify preserved IDs and configuration values, and start a new session when compression is ineffective.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thevibestack/skills/deflate)
- [ClawHub publisher profile](https://clawhub.ai/user/thevibestack)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured checklists, status reports, memory-entry templates, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend context compaction, new-session transitions, memory writes, and preservation of exact IDs, dates, URLs, file paths, and configuration values.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
