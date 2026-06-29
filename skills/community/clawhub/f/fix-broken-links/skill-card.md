## Description: <br>
Scan web files for broken hyperlinks and weak SEO anchor text, then interactively replace, strip, or skip each dead URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit website and documentation files for dead absolute HTTP(S) links, repair broken links interactively, and flag weak anchor text for SEO cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broken URLs may be sent to GitHub Copilot for replacement suggestions, which could expose internal links, private documentation paths, signed URLs, or tokens in query strings. <br>
Mitigation: Use deterministic link checking without Copilot suggestions for sensitive repositories, or review and redact links before running the repair flow. <br>
Risk: Agent-suggested replacement URLs may be inaccurate or misleading. <br>
Mitigation: Inspect each suggested replacement URL before accepting it, and use the custom replacement or skip option when uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhauga/fix-broken-links) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline Bash and PowerShell commands plus interactive terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may update target files when the user accepts an interactive replace, custom URL, or strip-link action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
