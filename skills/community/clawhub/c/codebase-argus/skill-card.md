## Description: <br>
Portable Codebase Argus agent playbook for evidence-first multi-agent review of GitHub pull requests, CI failures, GitHub Actions logs, GitHub App webhook review, /argus PR comment commands, autofix branch planning, OpenAI/Claude/Gemini/Codex provider tribunals, downstream merge/rebase work, and long-lived fork sync against an upstream repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronz345](https://clawhub.ai/user/aaronz345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review GitHub pull requests, CI failures, GitHub Actions logs, and downstream fork integration work with evidence-first review steps and optional multi-provider analysis. It also guides GitHub App webhook review, /argus comment commands, and cautious autofix or sync planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the referenced Codebase Argus checkout may execute code from an external repository. <br>
Mitigation: Pin and inspect the checkout before installation or execution, and install only when the referenced repository is trusted. <br>
Risk: GitHub, GitHub App, and AI provider credentials can expose private repositories, CI logs, or source content if over-scoped or mishandled. <br>
Mitigation: Use read-only or least-privileged GitHub tokens, limit GitHub App access to intended repositories, protect provider API keys, and send private code or logs to providers only when permitted. <br>
Risk: Automated PR and webhook workflows can post review comments or act on repository events if configured too broadly. <br>
Mitigation: Keep webhook secrets configured, restrict app installation scope, and require explicit user direction before approve, merge, push, or PR-creation actions. <br>


## Reference(s): <br>
- [Codebase Argus homepage](https://github.com/AaronZ345/codebase-argus) <br>
- [ClawHub skill page](https://clawhub.ai/aaronz345/codebase-argus) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aaronz345) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, review findings, and command plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference optional GitHub, GitHub App, OpenAI, Anthropic, and Gemini credentials when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
