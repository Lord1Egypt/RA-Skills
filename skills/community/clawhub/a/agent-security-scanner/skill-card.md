## Description:

Scans AI agent skills and code for risky patterns using multi-language static analysis, intent detection, and optional LLM verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketplace reviewers, and security teams use this skill to scan AI agent skills or code for malicious patterns, credential exposure, data exfiltration, prompt injection, and supply-chain indicators before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can produce misleading safe results according to the security summary.

Mitigation: Use it as an advisory signal only and require manual or independent review before accepting a skill as safe.

Risk: Security guidance identifies whitelist bypass, fixed-benign LLM paths, suppressed intent failures, fabricated batch results, and unsafe dependency declarations as unresolved concerns.

Mitigation: Install only after review, verify dependencies in an isolated environment, and do not use the tool as a final security gate until those concerns are remediated.

Risk: Daemon or scheduled modes may scan or write reports outside the intended scope if deployment is under-specified.

Mitigation: Run with explicit scan roots, least-privilege filesystem access, and restricted report destinations; avoid unattended modes until scope is documented.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caidongyun/skills/agent-security-scanner)
- [Publisher Profile](https://clawhub.ai/user/caidongyun)
- [Project Homepage](https://github.com/caidongyun/agent-security-skill-scanner#readme)
- [User Guide](docs/USER_GUIDE.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Delivery Report](docs/DELIVERY_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples and structured scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional LLM verification requires API configuration; findings should be reviewed before use as a security decision.]

## Skill Version(s):

4.1.6 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
