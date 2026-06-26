## Description: <br>
Ganidhuz-FoxX lets an agent browse X/Twitter through Firefox with a logged-in session for profile viewing, tweet fetching, search, scrolling, screenshots, and content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ganidhuz](https://clawhub.ai/user/Ganidhuz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control Firefox with a logged-in X/Twitter session when they need browser-based access to profiles, tweets, searches, screenshots, or selected page text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a real logged-in X/Twitter session and operate with that account's access. <br>
Mitigation: Use a dedicated Firefox profile and, ideally, a dedicated X account for agent-driven browsing. <br>
Risk: Exported cookies, storage-state files, screenshots, and temporary cookie database copies can expose session or account data. <br>
Mitigation: Delete or tightly protect those files after each run, including the exported cookie JSON and /tmp cookie database copy. <br>
Risk: Browser automation steps such as click, fill, type, and press can make interactive account changes. <br>
Mitigation: Inspect every plan before execution and avoid interactive actions unless account changes are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ganidhuz/ganidhuz-foxx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, Text] <br>
**Output Format:** [Markdown usage guidance, JSON plan inputs and results, screenshot files, and extracted page text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Firefox profile with an active X/Twitter login and optional exported cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
