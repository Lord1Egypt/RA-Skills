## Description:

Scans OpenClaw skills before installation for security risks using static and dynamic analysis to identify potentially malicious code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjj09090](https://clawhub.ai/user/jjj09090)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw or ClawHub skills before installation, review static and dynamic findings, and decide whether a skill should be installed, rejected, or sandboxed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default dynamic analysis can run scanned Python code in-process.

Mitigation: Run scans of untrusted skills with dynamic analysis disabled or inside a disposable sandbox.

Risk: A low-risk result can understate risk for non-Python, instruction-only, JavaScript, shell, or mixed-language skills.

Mitigation: Treat the result as one review signal and add manual review or complementary scanners for unsupported formats.

Risk: The skill records local quota and license files under the user's home directory.

Mitigation: Use an isolated user profile or review local data handling before running it in shared or sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jjj09090/skills/clawscan-vigil)
- [Publisher Profile](https://clawhub.ai/user/jjj09090)
- [Project Homepage](https://github.com/clawscan/clawscan-vigil)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [CLI text, Markdown summaries, and optional JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results include risk level, finding counts, file paths, categories, descriptions, and recommendations when available.]

## Skill Version(s):

0.2.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
