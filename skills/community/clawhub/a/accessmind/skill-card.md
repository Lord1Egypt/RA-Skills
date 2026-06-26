## Description: <br>
AccessMind helps agents run WCAG 2.2, WCAG 2.1, and EN 301 549 accessibility audits using browser inspection, keyboard navigation checks, ACT rules, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarperarikan](https://clawhub.ai/user/sarperarikan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, accessibility reviewers, and QA teams use this skill to assess websites for accessibility issues, map findings to WCAG criteria, and produce human-readable HTML, JSON, or Markdown audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses broad browser access and may collect full-page HTML, screenshots, URLs, and behavioral data during audits. <br>
Mitigation: Run it only in an isolated browser profile or test environment and only against sites you are authorized to audit. <br>
Risk: Local AI or gateway services may receive audit data from sensitive pages. <br>
Mitigation: Avoid use on sensitive accounts or private internal applications unless that data flow is approved. <br>
Risk: Legacy stealth or VoiceOver cleanup scripts can disrupt Chrome sessions or clear Chrome cache. <br>
Mitigation: Do not run those scripts on a normal workstation unless the operational impact is understood and accepted. <br>


## Reference(s): <br>
- [AccessMind ClawHub release](https://clawhub.ai/sarperarikan/accessmind) <br>
- [WCAG-EM](https://www.w3.org/TR/WCAG-EM/) <br>
- [ACT Rules](https://www.w3.org/WAI/standards-guidelines/act/) <br>
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) <br>
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) <br>
- [Axe-core Rules](https://dequeuniversity.com/rules/axe/4.10/) <br>
- [ARIA Guide](references/aria-guide.md) <br>
- [Browser Tool Workflow](references/browser-tool-workflow.md) <br>
- [WCAG 2.2 Criteria](references/wcag-2.2-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, HTML reports, shell commands, and accessibility findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WCAG criteria mappings, severity summaries, keyboard navigation metrics, screenshots, and remediation guidance.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
