## Description: <br>
Open pages with the real CN or global browser profile on spark and return the live page title plus final URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a task explicitly requires opening a site in a live browser session, especially when CN and global browser routing matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses live browser profiles, which may expose cookies, login state, or unrelated tab data to the agent workflow. <br>
Mitigation: Install and run it only on hosts where a live browser session is intended, and avoid sensitive logged-in profiles unless the task requires them. <br>
Risk: If the requested URL cannot be matched, the script can return an existing browser tab as a fallback. <br>
Mitigation: Review returned titles and final URLs before relying on the result; consider changing the script to fail when no matching page is found. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jackdark425/aigroup-browser-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jackdark425) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [JSON from the browser-opening script, with human-facing guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns browser-reported ok, mode, port, title, and final URL fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
