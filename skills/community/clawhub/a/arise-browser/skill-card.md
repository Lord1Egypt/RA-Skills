## Description: <br>
Arise Browser lets AI agents control a local Chromium browser through CLI commands, persistent element references, YAML accessibility snapshots, and WebRTC live view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yourens](https://clawhub.ai/user/Yourens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Arise Browser to automate browser navigation, page inspection, form interactions, screenshots, and tab workflows through a local browser service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful local controls over a browser session. <br>
Mitigation: Use a dedicated fresh profile, keep API and live-view ports local and unforwarded, set ARISE_BROWSER_TOKEN, and stop the daemon when finished. <br>
Risk: Profile, cookie, and JavaScript evaluation features can expose sensitive logged-in sessions or page data. <br>
Mitigation: Avoid sensitive logged-in accounts, do not use a daily browser profile, and review any cookie or /evaluate use before running it. <br>


## Reference(s): <br>
- [Arise Browser on ClawHub](https://clawhub.ai/Yourens/arise-browser) <br>
- [AriseBrowser API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, YAML, JSON, images] <br>
**Output Format:** [Markdown guidance with shell commands; runtime commands return YAML snapshots, JSON responses, screenshots, PDFs, or exported browser workflow data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and Docker. Browser state is session-scoped by default; profile mode and file-export commands can access or write local browser data.] <br>

## Skill Version(s): <br>
0.4.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
