## Description: <br>
Anubis Lite -- Career Application Engine. Paste a job description and get tailored resume bullet points in seconds. Free tier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to analyze pasted job descriptions, identify ATS keywords and experience requirements, and draft tailored resume bullets plus a short positioning statement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted job descriptions may contain recruiter contact details, internal hiring notes, private compensation data, tracking links, or other sensitive text. <br>
Mitigation: Remove sensitive or private job-posting details before setting JOB_DESCRIPTION or sharing terminal output. <br>
Risk: The skill asks the agent to install the Python rich package with pip. <br>
Mitigation: Install dependencies in a virtual environment before running the Python snippets. <br>


## Reference(s): <br>
- [Anubis Lite on ClawHub](https://clawhub.ai/occupythemilkyway/anubis-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks, plus generated career guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JOB_DESCRIPTION environment variable; the bundled parser prints the pasted job description to terminal output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
