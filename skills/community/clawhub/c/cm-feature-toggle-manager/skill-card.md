## Description: <br>
Audit, manage, and clean up feature flags across codebases to reduce toggle debt <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit feature flags, identify stale or orphaned toggles, plan safe cleanup, and design rollout lifecycles across codebases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to use repository access and service tokens for feature flag or monitoring systems. <br>
Mitigation: Use read-only or narrowly scoped API keys for audits, and avoid granting write access unless a reviewed change plan requires it. <br>
Risk: Cleanup plans may remove or collapse flag-controlled code paths incorrectly if service state, git history, or external configuration is incomplete. <br>
Mitigation: Review the generated cleanup plan, verify blast radius and tests, deploy to staging first, and require owner approval with a rollback plan before production flag deletion or archival. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/cm-feature-toggle-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and plans with inline shell commands and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls requiring scoped service tokens for feature flag or monitoring systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
