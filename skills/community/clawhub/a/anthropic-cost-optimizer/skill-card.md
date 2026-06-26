## Description: <br>
Audits and rewrites OpenClaw configuration to reduce Anthropic API token costs by checking prompt caching, model routing, thinking level, context-window use, and fast-mode settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw YAML or JSON configuration for Anthropic API cost issues, review recommended diffs and estimates, and optionally apply confirmed changes to the same config file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read live OpenClaw configuration files, which may contain sensitive credentials or cost-impacting settings. <br>
Mitigation: Confirm the exact config path before analysis and redact secrets before pasting configuration content into an agent session. <br>
Risk: The skill can rewrite OpenClaw configuration in ways that affect credentials, cost, and agent behavior. <br>
Mitigation: Review the generated diff, keep a backup, and approve only intended changes before allowing any write. <br>
Risk: Generated configuration edits may be invalid for the original YAML or JSON file type. <br>
Mitigation: Validate the resulting file format before restarting OpenClaw or relying on the updated configuration. <br>


## Reference(s): <br>
- [Pricing Reference](references/pricing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nextfrontierbuilds/anthropic-cost-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with issue summaries, cost estimates, config diffs, YAML or JSON configuration changes, and follow-up shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose and, after user confirmation, write changes back to an OpenClaw configuration file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
