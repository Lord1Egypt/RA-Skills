## Description:

Query GitHub repository documentation, wiki structure, and ask AI-powered questions via SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect public GitHub repository documentation, retrieve DeepWiki structure or page content, and ask documentation-grounded questions from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository targets and user questions are sent to SkillBoss/HeyBossAI.

Mitigation: Use the skill for public repositories as documented and avoid including secrets or proprietary details in questions.

Risk: AI answers may be influenced by untrusted repository documentation.

Mitigation: Treat responses as advisory and verify important technical decisions against authoritative project sources.

## Reference(s):

- [DeepWiki MCP documentation](https://docs.devin.ai/work-with-devin/deepwiki-mcp)
- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/abe-deepwiki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned as command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and is documented for public GitHub repositories.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
