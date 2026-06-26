## Description: <br>
Automates DataHive sign-in using a magic link workflow: requests the link, retrieves it from Gmail via gog, and opens it in a Chrome DevTools tab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuleyko](https://clawhub.ai/user/tuleyko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to automate DataHive dashboard authentication through a magic-link flow. It is limited to login setup and does not manage DataHive datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer applies persistent, privileged Chrome policy changes and creates local Chrome profile state. <br>
Mitigation: Run only on a trusted machine, review the managed Chrome extension policy before use, and document how to remove the policy and ~/.chrome-datahive state afterward. <br>
Risk: The skill leaves Chrome running with a local DevTools endpoint and opens short-lived magic-link tokens. <br>
Mitigation: Use a dedicated browser profile and Gmail account where possible, keep magic links private, and stop the Chrome supervisor when the login flow is complete. <br>


## Reference(s): <br>
- [DataHive Installer on ClawHub](https://clawhub.ai/tuleyko/datahive-installer) <br>
- [DataHive dashboard authentication endpoint](https://dashboard.datahive.ai/auth) <br>
- [DataHive magic-link request endpoint](https://api.datahive.ai/api/auth/magic-link/request) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gog, curl, and websocat; opens the retrieved magic link in a Chrome DevTools tab.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
