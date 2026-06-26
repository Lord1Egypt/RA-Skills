## Description: <br>
Windows-friendly Chrome automation for attaching an agent to an existing Chrome profile over CDP, validating browser access, navigating pages, drafting guarded X replies, and sending optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugurinanc12](https://clawhub.ai/user/ugurinanc12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to drive a dedicated local Chrome profile through CDP, verify live browser attachment, search X, produce reviewable reply drafts, and optionally apply approved replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in Chrome or X session and publish replies when live mode is enabled. <br>
Mitigation: Use a dedicated low-risk browser profile, keep CDP bound to the local machine, run draft mode first, and enable apply mode only after accepting the posting risk. <br>
Risk: The skill can extract contact details from posts and send optional notifications. <br>
Mitigation: Enable Telegram notifications only for an approved destination and review whether contact detail collection is appropriate for the account and workflow. <br>
Risk: Browser automation attached to a real profile can act with the permissions of that logged-in account. <br>
Mitigation: Keep the Chrome debugging port disabled when not actively using the skill and avoid using a profile that contains unrelated personal or production accounts. <br>


## Reference(s): <br>
- [CDP Setup](artifact/references/cdp-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/ugurinanc12/chrome-cdp-browser-operator) <br>
- [Publisher profile](https://clawhub.ai/user/ugurinanc12) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Command-line JSON responses, generated configuration files, draft JSON bundles, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local state and output files; live posting requires explicit apply mode plus configuration that allows public replies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
