## Description: <br>
Uses Chrome DevTools MCP for accessibility (a11y) debugging and auditing based on web.dev guidelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[POIUY1318](https://clawhub.ai/user/POIUY1318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit web pages for accessibility issues, including semantic structure, accessible names, keyboard focus, tap targets, and color contrast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser inspection snippets execute in the context of the page being audited. <br>
Mitigation: Run the snippets only on pages the user intends to inspect and review the narrow diagnostic behavior before execution. <br>
Risk: Automated accessibility checks may miss issues such as complex color contrast over gradients, images, or transparency. <br>
Mitigation: Use screenshots and manual review alongside Lighthouse, accessibility tree snapshots, and the provided diagnostic snippets. <br>


## Reference(s): <br>
- [Accessibility Debugging Snippets](references/a11y-snippets.md) <br>
- [Accessible Tap Targets](https://web.dev/articles/accessible-tap-targets) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include accessibility findings, remediation guidance, and diagnostic snippets for browser inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
