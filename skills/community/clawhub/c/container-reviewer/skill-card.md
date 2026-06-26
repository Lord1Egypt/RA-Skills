## Description: <br>
Reviews Dockerfiles and docker-compose files for security, image size, build efficiency, and best-practice issues, then returns a severity-rated report with fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lnguyen1996](https://clawhub.ai/user/Lnguyen1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to review Dockerfiles, docker-compose files, and .dockerignore files for container security, image size, build correctness, and operational best-practice issues before production or CI use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste real secrets into Dockerfiles or compose files during review. <br>
Mitigation: Use redacted examples and keep secrets out of prompts and artifacts. <br>
Risk: Suggested container changes may be unsuitable for a production environment without review. <br>
Mitigation: Review recommendations against deployment requirements and test changes before applying them. <br>
Risk: Self-improvement notes could retain overly specific details from reviewed files. <br>
Mitigation: Keep learning notes generic and avoid storing project-specific or sensitive details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lnguyen1996/container-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown report with severity sections and corrected before/after examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity ratings, corrected snippets, a summary, and optional notes about recurring Dockerfile mistakes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
