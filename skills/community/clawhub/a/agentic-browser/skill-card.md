## Description: <br>
Agent Browser gives AI agents browser automation through inference.sh, including navigation, element interaction with @e refs, screenshots, JavaScript execution, file upload, proxy support, and video recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to automate authorized browser workflows such as navigation, form filling, data extraction, screenshot capture, test evidence collection, and authenticated session work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated browsing and cookie access can expose account data or session secrets. <br>
Mitigation: Use the skill only on sites and accounts you are authorized to automate, avoid exporting or logging cookies, and close sessions promptly. <br>
Risk: JavaScript execution can change page state or expose sensitive page data. <br>
Mitigation: Review JavaScript before execution and limit it to the minimum code needed for the task. <br>
Risk: Screenshots and video recordings may capture credentials, private account data, or regulated information. <br>
Mitigation: Disable recording around sensitive pages and handle screenshot or video outputs as sensitive artifacts. <br>
Risk: File upload automation can submit unintended or unapproved local files. <br>
Mitigation: Upload only explicitly approved files and verify the target element before each upload. <br>
Risk: Proxy support can obscure traffic origin or be misused for rate-limit evasion. <br>
Mitigation: Use trusted proxies only, respect site terms and rate limits, and avoid proxy rotation intended to bypass controls. <br>


## Reference(s): <br>
- [Agent Browser on ClawHub](https://clawhub.ai/okaris/agentic-browser) <br>
- [Command Reference](references/commands.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Session Management](references/session-management.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh Sessions](https://inference.sh/docs/extend/sessions) <br>
- [inference.sh Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps) <br>
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash snippets and JSON command inputs; runtime calls may return JSON, screenshots, and video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser element refs are session-scoped and should be refreshed after navigation or page changes.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
