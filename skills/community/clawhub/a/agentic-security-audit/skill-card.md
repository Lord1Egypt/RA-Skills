## Description: <br>
Audit codebases, infrastructure, and agentic AI systems for dependency vulnerabilities, secrets, OWASP web risks, TLS issues, file permissions, prompt injection, identity spoofing, memory poisoning, multi-agent communication, and agent permission boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingrubic](https://clawhub.ai/user/kingrubic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and agent operators use this skill to run structured security reviews of software projects and agent workspaces. It provides checklists and command snippets for dependency auditing, secret detection, OWASP web review, TLS checks, file permission review, and agentic security threat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command snippets can inspect local workspaces and may expose sensitive findings in terminal output. <br>
Mitigation: Run commands only in trusted workspaces and redact or avoid sharing raw scan output because it may contain secrets. <br>
Risk: Dependency-fix commands can change project files or dependency versions. <br>
Mitigation: Run dependency fixes on a branch and review the resulting diff and tests before merging. <br>
Risk: The included secret-check hook documents a bypass path that could allow a risky commit. <br>
Mitigation: Use hook bypass only through a deliberate exception process, and rotate any exposed credentials. <br>
Risk: Audit commands and findings are guidance, not a complete security assessment. <br>
Mitigation: Review commands before execution and treat results as inputs to a broader security review. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/kingrubic/agentic-security-audit) <br>
- [Agents of Chaos](https://arxiv.org/abs/2602.20021) <br>
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) <br>
- [NIST AI Agent Standards Initiative](https://www.nist.gov/caisi/ai-agent-standards-initiative) <br>
- [OpenClaw Security Crisis](https://conscia.com/blog/the-openclaw-security-crisis/) <br>
- [Trivy documentation](https://aquasecurity.github.io/trivy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may inspect local files, install scanners, or apply dependency fixes when the user chooses to run them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
