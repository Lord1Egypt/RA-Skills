## Description:

Run Mission Control visual QA on SAPCONET over SSH using Puppeteer screenshots and basic DOM checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run read-only visual QA against authorized Mission Control pages, capture screenshots, and collect basic DOM checks from a SAPCONET host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment-controlled SSH target and remote path values can affect shell commands on the remote host.

Mitigation: Use only trusted environment variables and trusted SSH targets; avoid overriding remote paths unless you control them.

Risk: Generated screenshots may contain sensitive internal application data.

Mitigation: Store screenshots only in approved locations and handle them as sensitive internal artifacts.

Risk: The shell helper has unsafe remote command construction around environment-controlled paths.

Mitigation: Validate or safely quote remote paths before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/billy-mission-control-visual-qa)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output includes PNG screenshots and a JSON summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted SSH target, Puppeteer, Chromium, and authorized Mission Control URLs.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
