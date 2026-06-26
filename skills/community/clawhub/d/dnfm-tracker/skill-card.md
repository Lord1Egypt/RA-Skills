## Description: <br>
Tracks DNFM weekly dungeon progress for new transcendence, old transcendence, weekly, thunder dragon, and raid activities, with configurable totals and scheduled resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crazzies](https://clawhub.ai/user/Crazzies) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check and update DNFM weekly activity completion counts, adjust per-activity totals, and enable or disable tracked activities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local progress and configuration JSON files under /root/.openclaw/workspace/dnfm-tracker/. <br>
Mitigation: Install only where local persistence in that path is acceptable, and review or back up those JSON files before replacing the skill. <br>
Risk: Checking status on scheduled refresh days after 6 AM can reset matching activity progress. <br>
Mitigation: Confirm the refresh schedule before status checks or updates, and keep a backup if preserving pre-reset progress matters. <br>
Risk: The bundle includes an unrelated MLOL documentation file that is not used by the tracker code. <br>
Mitigation: Review bundled files during deployment and ignore or remove unrelated documentation if a minimal package is required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command-line status and update messages, with local JSON progress and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists progress and configuration under /root/.openclaw/workspace/dnfm-tracker/.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
