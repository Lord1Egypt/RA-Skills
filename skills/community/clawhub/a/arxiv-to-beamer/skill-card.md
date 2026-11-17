## Description:

Given an arxiv identifier or arxiv abs/pdf URL, download the LaTeX source or fall back to MinerU PDF-to-Markdown, ask an OpenRouter model to generate a Beamer presentation introducing the work, and package the result as an Overleaf-uploadable zip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirtycomputer](https://clawhub.ai/user/dirtycomputer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic authors use this skill to turn an arXiv paper ID or URL into an Overleaf-ready Beamer project. It is useful when a user asks for slides or a presentation derived from a paper's LaTeX source or PDF content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded archives are handled unsafely and could affect local files or resources.

Mitigation: Review before installing and run only in a contained workspace until archive-safety fixes are in place.

Risk: Paper-derived content is sent to OpenRouter, and PDF URLs or content may be sent through MinerU.

Mitigation: Do not use the skill on untrusted or sensitive papers; use --no-mineru-fallback to avoid MinerU when appropriate.

Risk: The skill reads API tokens from environment variables.

Mitigation: Use scoped API tokens and avoid running the skill in shared or untrusted shell environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dirtycomputer/skills/arxiv-to-beamer)
- [arXiv](https://arxiv.org)
- [MinerU](https://mineru.net)
- [OpenRouter API](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, plus an Overleaf-uploadable zip containing LaTeX project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; PDF-only fallback may require MINERU_API_TOKEN; default source text cap is 200000 characters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
