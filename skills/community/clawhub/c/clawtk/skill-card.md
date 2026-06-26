## Description: <br>
Automatically reduce OpenClaw API costs by 60-80%. One-command setup: config optimization, spend caps, retry loop protection, and ClawTK Engine compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skl3](https://clawhub.ai/user/skl3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce API spend by applying reversible configuration optimizations, enforcing spend caps, detecting retry loops, and optionally enabling token compression and semantic caching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow persistently changes OpenClaw configuration, including heartbeat behavior, context limits, image sizing, and some model routing. <br>
Mitigation: Run setup only after reviewing the documented config patches, and use the restore or uninstall commands to revert from the backup if the changes are not acceptable. <br>
Risk: Pro features can install a global command-output compression hook that changes what command output reaches the agent. <br>
Mitigation: Confirm the rtk hook behavior before enabling Pro features, keep the documented bypass available for commands that need full output, and verify hook removal during uninstall. <br>
Risk: Pro or Cloud activation and sync can transmit a license key and local spend metadata to ClawTK's cloud. <br>
Mitigation: Inspect the local spend log before syncing and avoid activation or sync when the user does not want that metadata transmitted. <br>
Risk: Spend caps and retry-loop detection may block legitimate repeated or high-volume work. <br>
Mitigation: Use the temporary override command for intentional bursts and review spend-cap settings before long-running work. <br>


## Reference(s): <br>
- [ClawTK Homepage](https://clawtk.co) <br>
- [ClawTK Config Patches](references/config-patches.md) <br>
- [ClawTK Savings Guide](references/savings-guide.md) <br>
- [ClawTK Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts that update OpenClaw configuration, install hooks, write local state, and optionally sync spend metadata for Pro or Cloud tiers.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
