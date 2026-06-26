## Description: <br>
Installs and deploys DeepSlide, enables Docker-based TeX compilation, and can clone/star the repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PUITAR](https://clawhub.ai/user/PUITAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, start, health-check, and stop DeepSlide services while using Docker for TeX compilation instead of a local TeX installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may attempt to star PUITAR/DeepSlide by default using existing GitHub CLI authentication or GITHUB_TOKEN. <br>
Mitigation: Explicitly say not to star the repository or set DEEPSLIDE_SKIP_STAR=1 before using the skill. <br>
Risk: The skill directs the agent to clone a third-party repository and run dependency installs, a Docker build, and service startup scripts. <br>
Mitigation: Review or sandbox the cloned repository, dependency installs, Docker build, and startup scripts before running them. <br>
Risk: The setup flow can involve API keys or tokens through environment variables and .env files. <br>
Mitigation: Keep secrets in environment variables or .env files and do not print or echo token values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PUITAR/deepslide) <br>
- [DeepSlide repository](https://github.com/PUITAR/DeepSlide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, Docker build, dependency installation, service operation, and health-check guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
