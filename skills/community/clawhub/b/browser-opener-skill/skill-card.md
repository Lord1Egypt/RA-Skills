## Description: <br>
Opens URLs in the system default browser or a selected Chrome, Firefox, Edge, or Safari browser across supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows use this skill to launch URLs in local browsers for page inspection, browser-specific testing, and browser-opening automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open arbitrary URLs in a local browser session. <br>
Mitigation: Confirm URLs before opening them, especially when the URL comes from generated content or an untrusted source. <br>
Risk: Opening sites in a normal browser profile may use existing logged-in sessions or browser state. <br>
Mitigation: Use private or incognito mode for sites that should not load in the user's normal browser session. <br>
Risk: The README suggests installing standard-library modules with pip. <br>
Mitigation: Do not run the README's `pip install webbrowser subprocess argparse` command; these modules are provided by Python's standard library. <br>


## Reference(s): <br>
- [Browser Support Details](references/browser_support.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/panchenbo/browser-opener-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands or code that can open local browser windows and URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
