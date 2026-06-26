## Description: <br>
Deploy a single self-contained HTML page to htmlcode.fun for instant sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520xiaomumu](https://clawhub.ai/user/520xiaomumu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish, update, inspect, and manage shareable single-file HTML pages on htmlcode.fun when lightweight hosting is sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML deployments may accidentally publish secrets, private content, or unintended page state. <br>
Mitigation: Review the HTML before deployment and install the skill only when publishing to htmlcode.fun is intended. <br>
Risk: Overwriting, unpublishing, switching the current public version, or deleting a version can affect a live shared page. <br>
Mitigation: Verify the target code and version first, require explicit confirmation for sensitive changes, and append a new version when a liked version is locked. <br>


## Reference(s): <br>
- [htmlcode.fun live guide](https://www.htmlcode.fun/s/htmlcode-fun-guide) <br>
- [ClawHub skill page](https://clawhub.ai/520xiaomumu/easy-html-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return htmlcode.fun deployment URLs, detail URLs, version URLs, version numbers, QR codes, preserve hints, and troubleshooting fields from API responses.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
