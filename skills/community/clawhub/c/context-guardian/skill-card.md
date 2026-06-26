## Description: <br>
Proactive context monitoring with smart 3-level alerts. Know when to restart before quality degrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucey0017-cloud](https://clawhub.ai/user/brucey0017-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to monitor OpenClaw context usage during heartbeat or manual checks and receive threshold-based alerts before quality degrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local OpenClaw session status output and jq; missing tools or unexpected output may prevent alerts from appearing. <br>
Mitigation: Verify jq and the OpenClaw CLI are available before enabling recurring checks, and test a manual check in the target environment. <br>
Risk: The skill writes local alert history, and resetting state can cause prior alert suppression history to be lost. <br>
Mitigation: Review the configured history path and reset the state file only when intentionally retesting or clearing local alert history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucey0017-cloud/context-guardian) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/brucey0017-cloud) <br>
- [README](README.md) <br>
- [Heartbeat Integration Example](examples/heartbeat-integration.md) <br>
- [Manual Check Example](examples/manual-check.md) <br>
- [Custom Configuration Example](examples/custom-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local alert state is stored under memory/context-guardian-state.json when tracking is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
