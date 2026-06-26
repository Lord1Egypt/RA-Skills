## Description: <br>
Controls a user's local Chromium browser through an HTTP relay to work around data-center IP blocks and optionally send screenshots to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esojourn](https://clawhub.ai/user/esojourn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent automate a local Chromium session for sites that block data-center IPs. It supports browser navigation, page interaction, screenshots, JavaScript evaluation for UI automation, and tab management through local relay API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay gives an agent broad control over a local Chromium browser and any logged-in sessions available in that profile. <br>
Mitigation: Run it in a VM, container, or fresh dedicated browser profile and avoid opening sensitive accounts in the controlled browser. <br>
Risk: The JavaScript evaluation endpoint can access page context such as DOM data, cookies, localStorage, and sessionStorage. <br>
Mitigation: Limit evaluation to UI automation tasks, keep the relay bound to localhost, and do not expose the relay to untrusted clients. <br>
Risk: Screenshot delivery through Telegram can disclose visible browser content or use the wrong bot or chat configuration. <br>
Mitigation: Verify Telegram bot and chat settings before sending screenshots, use a dedicated low-privilege bot, and send screenshots only when explicitly requested. <br>
Risk: Unpinned dependencies and remote-debugging Chromium increase operational exposure during automation. <br>
Mitigation: Pin dependencies when deploying and stop both the relay and remote-debugging Chromium when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/esojourn/browser-relay-xiaohongshu) <br>
- [Publisher profile](https://clawhub.ai/user/esojourn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash command templates and JSON HTTP responses; screenshots may be returned as base64 image data or saved image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local screenshot files and send screenshots through Telegram when explicitly requested.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
