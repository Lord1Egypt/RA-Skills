## Description:

Analyzes Spanish and English text for AI-writing patterns, statistical uniformity, and inflated vocabulary, then gives guidance and optional edits to make authorized writing sound more natural.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sitost](https://clawhub.ai/user/sitost)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to review authorized Spanish or English drafts for recognizable AI-writing patterns, statistical uniformity, and over-polished vocabulary. Agents can return pattern analysis, prioritized rewriting guidance, Markdown reports, CLI commands, MCP tool calls, and configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to make AI-assisted writing appear more human, which may conflict with disclosure rules or authorship expectations.

Mitigation: Use it only on your own or explicitly authorized content, and disclose AI assistance when required by a platform, institution, employer, or policy.

Risk: The CLI and MCP setup references external npm/GitHub code that is not included in the reviewed ClawHub artifact.

Mitigation: Inspect and pin the external code before use, avoid global installs for sensitive environments, and register the MCP server only where that code is trusted.

Risk: Directory scans can process more local content than intended if pointed at a broad path.

Mitigation: Confirm the exact scan path before running directory analysis and scope scans to the smallest relevant folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sitost/skills/bilingual-humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON, and inline shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference pattern IDs, scores, statistical metrics, prioritized suggestions, and optional autofix results.]

## Skill Version(s):

3.2.1 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
