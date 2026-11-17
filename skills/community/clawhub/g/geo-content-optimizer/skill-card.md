## Description:

Optimizes existing content for AI citation readiness across ChatGPT, Perplexity, AI Overviews, Gemini, Claude, and Copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and content teams use this skill to audit and transform existing content for AI-generated answer and citation surfaces. It produces GEO analysis, implementation-ready content changes, schema guidance, and handoff notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent memory updates that may store confidential launches, private URLs, client names, or sensitive campaign terms.

Mitigation: Use it only where memory writes are acceptable, confirm exactly what will be saved, and avoid entering confidential or client-sensitive material unless approved.

Risk: The optional Tavily AI-citation probe can send a target query or URL to an external service.

Mitigation: Skip the probe unless sharing that query or URL externally is acceptable; use provided evidence or local review instead when external sharing is not approved.

Risk: The security scan reports that memory writes and the external Tavily probe are not clearly covered by the lite manifest.

Mitigation: Review the behavior before installing and constrain use to the capabilities and data handling posture approved for the workspace.

## Reference(s):

- [Geo Content Optimizer on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/geo-content-optimizer)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Instructions Detail](references/instructions-detail.md)
- [GEO Optimization Techniques](references/geo-optimization-techniques.md)
- [AI Citation Patterns](references/ai-citation-patterns.md)
- [AI Overview Recovery Playbook](references/ai-overview-recovery.md)
- [Medium and GitHub as AI-Citation Surfaces](references/medium-github-surfaces.md)
- [Quotable Content Examples](references/quotable-content-examples.md)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional JSON-LD, HTML/schema snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes GEO analysis, before/after scores, AI Query Coverage, self-check results, and an optional memory handoff summary.]

## Skill Version(s):

19.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
