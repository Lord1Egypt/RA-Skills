## Description: <br>
Accessibility Tester specializes in WCAG 2.1 compliance testing, screen reader compatibility, keyboard navigation, color contrast, and ARIA validation for application accessibility reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alshowse-tech](https://clawhub.ai/user/alshowse-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to plan and run accessibility checks for web applications, with attention to WCAG rules, keyboard navigation, color contrast, ARIA landmarks, and remediation reporting. Treat its compliance scores as preliminary because the server security review warns that current behavior can produce results for pages it does not actually inspect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overstate accessibility coverage and produce compliance results for pages it has not loaded or checked. <br>
Mitigation: Use it as a prototype or reference aid; verify results with a real browser-backed accessibility audit before relying on scores, WCAG levels, CI pass/fail output, or legal compliance claims. <br>
Risk: The artifact claims broad WCAG 2.1 and 2.2 coverage while the implemented checks are limited and partly simulated. <br>
Mitigation: Document the actual implemented rule coverage and require human review or established accessibility tooling for unsupported WCAG criteria. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alshowse-tech/accessibility-tester) <br>
- [W3C WCAG 2.1 Understanding: Non-text Content](https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html) <br>
- [W3C WCAG 2.1 Understanding: Contrast Minimum](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Structured accessibility reports, remediation guidance, TypeScript examples, and CI/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WCAG status, severity, affected elements, score summaries, compliance flags, and remediation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
