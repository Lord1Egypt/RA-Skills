## Description: <br>
Website Audit helps agents audit websites with 230+ checks across SEO, performance, security, technical, and content issues, including health scores and recommended actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and site operators use this skill to run website audits and interpret SEO, performance, security, technical, and content findings with prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on an external `squirrel` command that is not bundled with the skill. <br>
Mitigation: Verify which `squirrel` CLI will run on the target machine before executing examples. <br>
Risk: Website audits can touch systems outside the user's control. <br>
Mitigation: Audit only sites the user is authorized to test. <br>
Risk: Audit reports may contain sensitive site details before they are shared with external AI services. <br>
Mitigation: Review report contents before piping them to external services. <br>


## Reference(s): <br>
- [LLM Format Output Reference](references/OUTPUT-FORMAT.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/akkualle/akkualle-audit-website) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured audit report references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can reference JSON and compact LLM-oriented XML/text audit report formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
