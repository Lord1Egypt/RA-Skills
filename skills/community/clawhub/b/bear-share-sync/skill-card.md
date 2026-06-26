## Description: <br>
Bear Share Sync detects new Bear notes tagged #share, adds them as JSON Canvas knowledge nodes, and formats a BlueBubbles iMessage preview for sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to sync intentionally shared Bear notes into an Obsidian-compatible JSON Canvas knowledge graph and prepare compact iMessage previews for a configured work group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bear note excerpts can be shared outside Bear through BlueBubbles when sensitive notes are tagged #share or the target is misconfigured. <br>
Mitigation: Use this only for notes intentionally meant for sharing, verify BEAR_SHARE_TARGET before sending, and review tagged notes before enabling scheduled runs. <br>
Risk: Polling issues can resend notes or mishandle note content. <br>
Mitigation: Fix and test the polling script's JSON handling and processed-note condition before enabling cron or one-shot automation. <br>


## Reference(s): <br>
- [Canvas Schema Reference](references/canvas-schema.md) <br>
- [JSON Canvas 1.0 Specification](https://jsoncanvas.org/spec/1.0/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON note arrays, JSON Canvas file updates, and plain-text message previews with shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Bear/grizzly access, a configured BlueBubbles channel, and a configured share target.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
