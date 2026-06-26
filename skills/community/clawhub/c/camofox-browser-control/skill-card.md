## Description: <br>
Control a standalone camofox-browser server over its REST API for tab creation, navigation, page snapshots, clicks, typing, key presses, scrolling, storage-state export, cookie import, and browser automation debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to control an existing local or remote camofox-browser server through REST endpoints and a helper CLI. It supports browser workflows such as opening tabs, taking snapshots, interacting with page refs, navigating directly, and managing cookies or storage state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad control over logged-in browser sessions and session artifacts. <br>
Mitigation: Use it only with trusted camofox-browser servers, supervise sensitive logged-in sessions, and isolate userId and session values per task. <br>
Risk: API keys, cookies, and exported storage-state files can expose account access. <br>
Mitigation: Treat CAMOFOX_API_KEY, imported cookies, and storage-state files as secrets; clear persisted browser state when finished. <br>
Risk: Browser actions can affect live web accounts or submit unintended changes. <br>
Mitigation: Use the snapshot-after-action workflow, prefer short verified steps, and require manual handling for MFA, CAPTCHA, and brittle authentication flows. <br>


## Reference(s): <br>
- [camofox-browser API cheatsheet](references/api-cheatsheet.md) <br>
- [ClawHub release page](https://clawhub.ai/lotfinity/camofox-browser-control) <br>
- [Publisher profile](https://clawhub.ai/user/lotfinity) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON request examples, and Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include browser snapshots, REST responses, storage-state guidance, and CLI command examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
