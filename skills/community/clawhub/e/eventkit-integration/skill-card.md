## Description: <br>
EventKit integration patterns, permission handling, zero-width character steganography, and batch operations for macOS/iOS apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement EventKit reminders or events in macOS and iOS apps, including authorization, calendar management, bidirectional sync, batch operations, and test patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches hidden zero-width note markers that can obscure tracking metadata from users. <br>
Mitigation: Disclose any sync markers placed in notes, prefer visible or app-local metadata, and provide a way to inspect and remove markers. <br>
Risk: Bulk delete patterns can remove user calendar or reminder data at scale if identifiers or scopes are wrong. <br>
Mitigation: Require explicit confirmation, preview affected items, restrict operations to scoped identifiers, keep logs, and plan recovery before deleting. <br>
Risk: EventKit examples may request broad calendar and reminder access. <br>
Mitigation: Request only the EventKit permissions actually needed for the app workflow and check authorization before operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soponcd/eventkit-integration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Swift and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples are implementation templates and should be reviewed, scoped, and hardened before use in an app.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
