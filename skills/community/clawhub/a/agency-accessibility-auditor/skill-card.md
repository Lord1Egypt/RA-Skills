## Description: <br>
Accessibility Auditor helps agents evaluate digital interfaces against WCAG 2.2, combine automated scans with manual assistive-technology checks, and produce actionable remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouqkt](https://clawhub.ai/user/zhouqkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, QA teams, and accessibility reviewers use this agent to audit products or features for WCAG conformance, assistive-technology behavior, keyboard access, and inclusive design issues. It returns issue findings with severity, user impact, standards references, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested audit commands such as npx-based tooling may fetch packages at runtime. <br>
Mitigation: Review commands before execution and run them in an approved, controlled environment. <br>
Risk: Claims about screen-reader, keyboard, zoom, high-contrast, or reduced-motion behavior depend on a correctly provisioned test environment and real user-flow coverage. <br>
Mitigation: Verify findings with the named assistive technologies, browsers, operating systems, and manual interaction paths before relying on conformance conclusions. <br>


## Reference(s): <br>
- [ClawHub skill release: Accessibility Auditor](https://clawhub.ai/zhouqkt/agency-accessibility-auditor) <br>
- [ClawHub publisher profile: zhouqkt](https://clawhub.ai/user/zhouqkt) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown accessibility audit reports, testing protocols, remediation examples, and optional shell commands for audit tooling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference automated tools such as axe-core or Lighthouse and may require human verification with screen readers, keyboard navigation, zoom, high contrast, and reduced-motion settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
