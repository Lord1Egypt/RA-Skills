## Description: <br>
Helps agents plan, review, implement, audit, and improve responsive email templates, component systems, dark-mode behavior, accessibility, and design-to-email handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, ESP operators, and agents use this skill to audit or improve email templates, modules, and handoffs with concrete rendering, accessibility, and approval-gate guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations or edits could affect live email sends, contacts, DNS/authentication, suppression lists, migrations, or production automations. <br>
Mitigation: Keep the skill's explicit approval gates in place and require user approval before any live-system action. <br>
Risk: Email templates can render poorly across clients because of Outlook tables, Gmail clipping, dark-mode inversions, unsupported CSS, webfont fallbacks, and image blocking. <br>
Mitigation: Use the operating checklist to document responsive behavior, dark-mode contrast, image alt text, clipping risk, CSS support risk, and fallback behavior before release. <br>


## Reference(s): <br>
- [Email Design Skill on ClawHub](https://clawhub.ai/polnikale/emaildesignskill) <br>
- [Email Design Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance, QA tables, implementation notes, and code diffs when source is provided] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS or authentication changes, suppression edits, provider migrations, destructive cleanup, or production automation changes.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
