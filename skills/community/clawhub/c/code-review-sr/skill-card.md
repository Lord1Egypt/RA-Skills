## Description:

Code Review provides AI-assisted code review with local static analysis, optional Anthropic, OpenAI, or Ollama review, and fallback local findings for bugs, security, performance, and style issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to review individual files or source directories for bugs, security issues, performance concerns, style problems, and maintainability feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory review may follow symlinks outside the selected folder and send unintended local files to a configured AI provider.

Mitigation: Use local-only mode for sensitive repositories, avoid directory review on untrusted repositories or repositories containing symlinks, and review the file set before enabling external AI providers.

Risk: When Anthropic, OpenAI, or Ollama is configured, reviewed source code and static-analysis findings are sent to the selected provider.

Mitigation: Do not analyze code containing secrets or sensitive data with external providers unless the data-sharing path has been approved; run without an API key for local-only analysis.

Risk: AI-generated review findings can be incomplete or incorrect.

Mitigation: Treat results as review assistance and confirm security decisions with separate static analysis, tests, and human review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/code-review-sr)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Configuration, Guidance]

**Output Format:** [JSON review objects and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review output can include score, issues, suggestions, summary, line counts, model name, and whether AI review was used; files sent to AI are truncated at 8000 characters.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
