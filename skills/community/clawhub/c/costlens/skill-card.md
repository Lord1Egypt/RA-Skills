## Description: <br>
Calculate OpenClaw usage cost from offline event logs, apply budget thresholds, and export operator-facing reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use CostLens to analyze OpenClaw token usage logs, check spend against budgets, and export cost reports for handoff or audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may contain content derived from local usage logs. <br>
Mitigation: Review exported reports before sharing and use trusted event logs as input. <br>
Risk: Event-provided pricing overrides can change budget results. <br>
Mitigation: Verify event pricing fields and budget thresholds before relying on the output for enforcement. <br>
Risk: Incorrect input or output paths can read the wrong log file or write reports to an unintended location. <br>
Mitigation: Confirm --events and --out paths before running the CLI. <br>


## Reference(s): <br>
- [CostLens ClawHub page](https://clawhub.ai/mike007jd/costlens) <br>
- [CostLens README](README.md) <br>
- [CostLens source homepage](https://github.com/mike007jd/openclaw-skills/tree/main/costlens) <br>
- [CostLens issue tracker](https://github.com/mike007jd/openclaw-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, code] <br>
**Output Format:** [CLI text tables, JSON envelopes, and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected JSON event files, optionally writes report files, and returns exit code 2 for critical budget overruns.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
