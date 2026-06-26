## Description: <br>
Search Google using scrapling and return structured results with title, link, and snippet fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QipengGuo](https://clawhub.ai/user/QipengGuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to run a Google search from a Python script and return structured search results for downstream agent reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Google through automated browsing, which can expose sensitive prompts, credentials, private project details, or personal data. <br>
Mitigation: Do not use the skill for secrets or sensitive information, and review queries before execution. <br>
Risk: The release uses stealth-style browser automation and was flagged as suspicious by the server security scan. <br>
Mitigation: Review the source before installing, run it only in an environment where browser automation is acceptable, and monitor the visible browser session. <br>
Risk: Dependencies include an unpinned flagged network library, which can change behavior across installs. <br>
Mitigation: Pin and review dependency versions before deployment, including curl_cffi and browser automation packages. <br>
Risk: The script requires a GUI browser environment and may fail on headless servers or CI systems. <br>
Mitigation: Run it on a machine with a graphical browser session, or configure a virtual display such as Xvfb before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QipengGuo/free-google-search-with-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results emitted by a Python command, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each result includes title, link, and snippet fields; snippets are truncated to 300 characters by the script.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
