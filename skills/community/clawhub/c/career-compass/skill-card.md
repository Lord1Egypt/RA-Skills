## Description:

职场罗盘 by Barry is a job-search assistant skill that helps users optimize resumes, research employers from an employment perspective, search local roles, and run mock interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barry0-0](https://clawhub.ai/user/barry0-0)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and interview candidates use this skill to prepare applications and interviews by collecting resume, target-company, and job-description context, then producing resume improvement guidance, company research, role-search results, mock interview prompts, and interview review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can import browser cookies and store reusable BOSS credentials locally.

Mitigation: Review the security guidance before installing or running boss login/status, and proceed only if this local credential handling is acceptable.

Risk: The install flow may install an unpinned package from the Python registry.

Mitigation: Review the package and version source before running INSTALL.sh, or install in a controlled environment.

Risk: The bundled tooling may include recruiter-contact commands beyond read-only job search.

Mitigation: Use only read-only query commands unless recruiter contact is intentional, and avoid greet or batch-greet.

## Reference(s):

- [Career Compass ClawHub Page](https://clawhub.ai/barry0-0/skills/career-compass)
- [Poppler Windows Releases](https://github.com/oschwartz10612/poppler-windows/releases)
- [Tesseract Windows Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local resume text, PDF extraction tools, web search results, and BOSS job-search command output when available.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
