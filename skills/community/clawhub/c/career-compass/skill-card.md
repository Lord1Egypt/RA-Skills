## Description: <br>
职场罗盘 by Barry is a job-search assistant skill that combines resume parsing and optimization, employment-focused company research, local job search, and mock interview practice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barry0-0](https://clawhub.ai/user/barry0-0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this skill to prepare for interviews, improve resumes, research target employers from an employment-risk perspective, search local BOSS/Zhipin roles, and rehearse mock interviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The BOSS/Zhipin integration can read or import account session cookies and store credentials locally. <br>
Mitigation: Review the installation before use, prefer QR login, avoid BOSS_COOKIES unless necessary, and delete ~/.config/boss-cli/credential.json after use or on shared machines. <br>
Risk: The bundled CLI includes employer-contact commands beyond the skill's advertised read-only workflow. <br>
Mitigation: Use only intentional read-only job-search commands unless outreach is explicitly desired; do not run greet or batch-greet casually. <br>
Risk: The install flow may add a Python CLI and optional PDF tooling to the local environment. <br>
Mitigation: Review INSTALL.sh and dependency commands before running them, especially in managed or shared environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/barry0-0/career-compass) <br>
- [BOSS CLI README](boss-cli/README.md) <br>
- [BOSS CLI command schema](boss-cli/SCHEMA.md) <br>
- [Interview simulator reference](ref/interview-simulator/README.md) <br>
- [Poppler Windows releases](https://github.com/oschwartz10612/poppler-windows/releases) <br>
- [Tesseract Windows documentation](https://github.com/UB-Mannheim/tesseract/wiki) <br>
- [Ghostscript releases](https://ghostscript.com/releases/gsdnld.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, checklists, scoring rubrics, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resume optimization notes, company research summaries, job-search command guidance, mock interview questions, and interview scoring cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
