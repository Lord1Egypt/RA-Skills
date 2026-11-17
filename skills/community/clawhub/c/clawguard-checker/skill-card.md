## Description:

ClawGuard Security Checker v3 provides OpenClaw configuration analysis, runtime integrity checks, permission modeling, and hardening recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stardreaming](https://clawhub.ai/user/stardreaming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to assess the security posture of OpenClaw configuration files, identify risky settings, and produce actionable hardening guidance or hardened configuration output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad sensitive-data inspection can expose secrets from configuration, environment, log, or memory sources.

Mitigation: Run the skill only against explicitly scoped OpenClaw configuration paths and avoid broad scans unless the user has intentionally opted in.

Risk: Generated reports or hardened configuration files may contain live tokens, passwords, or other sensitive values.

Mitigation: Treat all generated reports and hardened configs as sensitive artifacts; restrict access, avoid sharing them publicly, and remove secrets before distribution.

Risk: Automatically generated hardened configuration may change runtime behavior or lock down legitimate workflows.

Mitigation: Review the hardened configuration before applying it and keep a backup of the previous OpenClaw configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stardreaming/skills/clawguard-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown-style guidance, JSON reports, and generated configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report JSON via --output and a hardened configuration file as <config>.hardened.json when --fix is used.]

## Skill Version(s):

3.0.0 (source: release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
