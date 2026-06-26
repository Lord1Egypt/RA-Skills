## Description: <br>
Patch a locally installed OpenClaw Control UI so that finishing an assistant reply plays a short Web-Audio chime with selectable presets and an in-page picker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to apply, remove, or reapply a local browser UI patch that plays an audible completion cue when an assistant response finishes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The apply script rewrites every detected local OpenClaw UI installation. <br>
Mitigation: Review the target paths printed by apply.sh before relying on the patch, keep the generated backups, and use remove.sh or an OpenClaw reinstall/update if the UI behaves unexpectedly. <br>
Risk: The cue depends on OpenClaw webchat DOM structure and browser AudioContext behavior. <br>
Mitigation: Use the provided manual verification steps after applying the patch, and expect the cue to be unavailable until the page receives a user gesture or if the target DOM class changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/symbolstar/echo-cue) <br>
- [OpenClaw Completion Sound Pull Request](https://github.com/openclaw/openclaw/pull/73894) <br>
- [OpenClaw Completion Sound Issue](https://github.com/openclaw/openclaw/issues/69186) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies or removes a local OpenClaw Control UI patch; browser-level preferences are stored in localStorage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
