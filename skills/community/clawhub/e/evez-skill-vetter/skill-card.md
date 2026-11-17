## Description:

Security review for OpenClaw skills before installation, covering static analysis, permission auditing, dependency scanning, data-exfiltration checks, and risk scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess third-party OpenClaw skills before installation, reviewing permission scope, suspicious code patterns, potential secret exposure, dependency risks, and risk scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted skill folders may be handled too loosely, including links that can lead reads outside the selected folder.

Mitigation: Run the vetter only against a constrained directory or sandbox until symlink rejection and stronger path boundaries are added.

Risk: Large or specially structured inputs can consume excessive local resources.

Mitigation: Apply file-size and archive limits before scanning untrusted skills, and avoid running it directly on fully untrusted archives.

Risk: Terminal output may include paths or findings from untrusted input.

Mitigation: Review output in a controlled terminal and add terminal-safe path escaping before using results in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-skill-vetter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with risk scores and categorized findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a 0-100 risk score, risk level, finding count, and categorized findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
