## Description: <br>
Anubis Pro generates a full career application package, including a tailored resume, three cover letter tones, interview Q&A preparation, follow-up emails, and an application tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to turn a resume and job description into an application package for a specific role. It helps draft ATS-oriented resume content, cover letters in multiple tones, interview preparation, follow-up emails, and an application log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive resume and job-description text may be printed to the console during use. <br>
Mitigation: Run the skill in a private session, avoid confidential inputs unless acceptable for terminal or agent logs, and remove or disable the diagnostic print statements before use. <br>
Risk: The install command uses pip with --break-system-packages. <br>
Mitigation: Prefer installing dependencies in a virtual environment before running the skill. <br>


## Reference(s): <br>
- [Anubis Pro ClawHub listing](https://clawhub.ai/occupythemilkyway/anubis-pro) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, code, shell commands, configuration] <br>
**Output Format:** [Markdown files with setup commands and Python execution snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JOB_DESCRIPTION, RESUME_PATH, and LICENSE_KEY; writes seven documents to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
