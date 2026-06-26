## Description: <br>
Triggers Bazhuayu RPA workflows through a signed webhook and lets an agent pass custom task parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blogwebsem](https://clawhub.ai/user/blogwebsem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to configure and invoke Bazhuayu RPA webhook triggers from an agent workflow. It supports dry-run testing, configuration inspection, secure checks, and parameterized task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships specific workflow data and configuration values. <br>
Mitigation: Replace config.json with a blank local configuration before running and rotate any webhook or Feishu credentials that may have been exposed. <br>
Risk: Webhook keys and workflow inputs can trigger unattended RPA actions. <br>
Mitigation: Store required secrets outside committed files, run secure-check before use, and only enable scheduled execution for workflows that have been reviewed. <br>
Risk: The security evidence reports inconsistent guidance for secret handling. <br>
Mitigation: Prefer ephemeral or managed secret storage and avoid placing webhook keys in shell profiles or example environment files unless that storage location is explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blogwebsem/bazhuayu-rpa-webhook) <br>
- [Bazhuayu RPA help center](https://rpa.bazhuayu.com/helpcenter) <br>
- [Webhook trigger task documentation](https://rpa.bazhuayu.com/helpcenter/docs/skmvua) <br>
- [Bazhuayu RPA API documentation](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi) <br>
- [README](README.md) <br>
- [Security guide](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the BAZHUAYU_WEBHOOK_URL and BAZHUAYU_WEBHOOK_KEY environment variables.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
