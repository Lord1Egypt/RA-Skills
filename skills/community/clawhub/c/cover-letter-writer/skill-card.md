## Description: <br>
CareerMax AI generates tailored cover letters from resume text and job descriptions for cover letters, application letters, role-specific pitches, and customized job application messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rahulphenomenon](https://clawhub.ai/user/rahulphenomenon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-focused agents use this skill to generate cover letters that connect a candidate resume to a specific job description. It can also use a stored CareerMax job ID through the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a CareerMax API key. <br>
Mitigation: Install only in environments where the agent process may access CAREERMAX_API_KEY, and avoid exposing the key in logs or shared command history. <br>
Risk: Cover-letter generation sends resume and job-description content to CareerMax. <br>
Mitigation: Use the skill only when the user is comfortable sharing that application content with CareerMax. <br>
Risk: The documented MCP and CLI commands install @careermax/agent-toolkit@latest at runtime. <br>
Mitigation: For stricter environments, review and pin the npm package version before use. <br>


## Reference(s): <br>
- [CareerMax AI Agent](https://careermax.ai/ai-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated cover letter text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAREERMAX_API_KEY and uses preview/confirm before AI-generation operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
