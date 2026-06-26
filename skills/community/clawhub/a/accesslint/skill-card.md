## Description: <br>
Web accessibility and WCAG compliance scanner that detects WCAG 2.1 violations, missing ARIA attributes, color contrast issues, keyboard navigation problems, and semantic HTML failures across HTML, JSX, Vue, and Svelte. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use AccessLint to scan frontend code for accessibility issues, generate WCAG-oriented reports, and optionally install pre-commit checks that block high-risk accessibility regressions before commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing hooks persists a lefthook.yml file in the repository and can block future commits. <br>
Mitigation: Review the generated lefthook.yml before committing or sharing it, and uninstall the hook if it does not match the repository policy. <br>
Risk: Custom policy regexes in shared configuration can create noisy or unexpected scan behavior. <br>
Mitigation: Use custom policies only when they are owned and reviewed by the team responsible for the repository. <br>
Risk: Paid features require a license key stored in an environment variable or local OpenClaw configuration. <br>
Mitigation: Treat ACCESSLINT_LICENSE_KEY as sensitive, keep it out of committed files, and prefer local environment or private user configuration. <br>


## Reference(s): <br>
- [AccessLint ClawHub listing](https://clawhub.ai/suhteevah/accesslint) <br>
- [suhteevah publisher profile](https://clawhub.ai/user/suhteevah) <br>
- [AccessLint website](https://accesslint.pages.dev) <br>
- [AccessLint pricing](https://accesslint.pages.dev/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, Markdown accessibility reports, SARIF JSON, and lefthook configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free scans are limited to 5 files; Pro and Team features require ACCESSLINT_LICENSE_KEY and may write report, SARIF, or lefthook configuration files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
