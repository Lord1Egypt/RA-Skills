## Description: <br>
Browser Proof helps agents capture browser QA and debugging sessions as machine-readable manifests, evidence-backed step logs, bundle checks, and shareable Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and release reviewers use this skill to turn browser test runs, debugging sessions, and Chrome extension review flows into portable evidence bundles for handoff and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser evidence bundles can include secrets, cookies, tokens, private URLs, account data, or personal information in manifests, reports, screenshots, DOM dumps, console logs, network logs, or videos. <br>
Mitigation: Review and redact generated evidence before sharing it outside the local QA context. <br>
Risk: Absolute or private artifact paths can expose local environment details and make a bundle harder to reproduce. <br>
Mitigation: Run the bundled browser proof check and use relative artifact paths before publishing or handing off the report. <br>


## Reference(s): <br>
- [Browser Proof project homepage](https://github.com/zack-dev-cm/browser-proof) <br>
- [Browser Proof on ClawHub](https://clawhub.ai/zack-dev-cm/browser-proof) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples; bundled scripts create JSON manifests, JSON bundle checks, and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 or python. Generated evidence may reference screenshots, DOM dumps, console logs, network logs, or videos captured during local browser QA.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
