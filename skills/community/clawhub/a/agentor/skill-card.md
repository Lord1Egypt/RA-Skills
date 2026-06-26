## Description: <br>
Use agenTOR for Tor-routed browser sessions with receipts, HTML capture, screenshots, and compact research runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use agenTOR when a browsing task should run through Tor or another proxy and leave local receipts, HTML capture, screenshots, summaries, or compact research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may overestimate anonymity from Tor or proxy routing. <br>
Mitigation: Treat Tor routing as network-path privacy only; avoid logged-in browser state when privacy separation matters. <br>
Risk: Captured pages, screenshots, receipts, and reports may preserve sensitive browsing evidence locally. <br>
Mitigation: Review and control the configured artifact directory, and retain or delete receipts according to the task's evidence and privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/builtbyecho/agentor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and descriptions of generated local artifact files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can produce local receipts, HTML, text summaries, screenshots, and report.md files under an artifacts directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
