## Description: <br>
API-key-free online research via the built-in browser tool for cases where web_search fails due to missing keys and web evidence is still needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to perform browser-based web retrieval when API-key-backed search is unavailable. It guides source selection, cross-checking, concise fact extraction, and fallback behavior when browser access is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser guard reads tails of recent local OpenClaw session logs to infer browser availability. <br>
Mitigation: Review the configured sessions directory and disclose local session-log access before installation or execution. <br>
Risk: The skill invokes the OpenClaw CLI from PATH to check browser status. <br>
Mitigation: Run it only in environments where the OpenClaw CLI path and browser extension setup are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanng-ide/browser-research-lite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON status from the browser guard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The browser guard reports availability status and recent browser failure signals before the agent proceeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
