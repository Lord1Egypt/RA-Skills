## Description: <br>
Generates a full-stack RSS news aggregation website with a Next.js frontend, FastAPI backend, Docker Compose setup, and scheduled feed refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to scaffold an RSS-based AI or industry news website with generated frontend, backend, deployment configuration, and setup documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated projects can run Docker, pip, and npm commands and expose local web services. <br>
Mitigation: Review generated files before execution, use a new empty target directory, and only run dependency installation or Docker commands in an environment approved for that project. <br>
Risk: RSS feed inputs and public deployment settings can introduce untrusted content or unintended network exposure. <br>
Mitigation: Validate RSS feed URLs and add authentication, restricted CORS, localhost binding or firewall controls, and other hardening before exposing the generated site publicly. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/ninetyhe-90/ai-news-website-generator) <br>
- [Next.js documentation](https://nextjs.org/docs) <br>
- [FastAPI documentation](https://fastapi.tiangolo.com/) <br>
- [Docker documentation](https://docs.docker.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Generated project files plus Markdown setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local Next.js, FastAPI, and Docker Compose project scaffold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
