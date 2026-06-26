## Description: <br>
Automatically install skills from ClawHub with retry logic, automatic confirmation prompts, rate-limit retries, and a 30-minute failure timeout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z448577223](https://clawhub.ai/user/z448577223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install named ClawHub skills through a shell helper that retries on rate limits and installation failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bypasses normal safety prompts by passing --force automatically and can retry installation of warning-flagged skills. <br>
Mitigation: Install only intentionally selected skills, review each target skill before installation, and avoid using this helper for untrusted or warning-flagged skills. <br>
Risk: The installer may continue retrying for up to 30 minutes after rate limits or failures. <br>
Mitigation: Monitor installation attempts and stop the process when the requested skill name or trust status is uncertain. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a shell installer that may retry for up to 30 minutes and passes --force automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
