## Description:

Security scanner for AI agent skills that detects hardcoded secrets, unsafe code execution, prompt injection, and malware patterns before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

Developers, security reviewers, and agent operators use this skill to run a local first-line scan of agent skill directories for risky text patterns before installation or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undisclosed module can load and run code from an external workspace path if imported.

Mitigation: Remove or clearly justify brain_enhance.py and avoid loading code from /data/.openclaw/workspace/company-brain before deployment.

Risk: The scanner is a first-line text-pattern scan and can miss secrets or malicious behavior in skipped paths such as .env or in obfuscated logic.

Mitigation: Document the exact filesystem scope, review skipped paths separately, and use manual review or deeper analysis for high-risk skills.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/certainlogicai/skills/ai-agent-skill-scanner)
- [Usage guide](docs/USAGE.md)
- [CertainLogic product documentation](https://certainlogic.ai/docs/skill-vetter-plus)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text scan report or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns process exit code 0 when no findings are found and 1 when findings are found; scanner coverage is limited by configured skip paths and text-pattern signatures.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
