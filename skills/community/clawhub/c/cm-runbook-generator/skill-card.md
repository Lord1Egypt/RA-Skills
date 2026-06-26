## Description: <br>
Generate operational runbooks from project files by scanning Dockerfiles, docker-compose.yml, systemd units, Makefiles, package.json, and config files to produce step-by-step operational procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations engineers use this skill to generate Markdown or JSON runbooks from a project's local infrastructure and configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated runbooks may expose operational metadata such as environment variable names, absolute paths, service names, ports, scripts, or project structure. <br>
Mitigation: Review generated Markdown or JSON before sharing, committing, or using it in production documentation. <br>
Risk: The skill reads files from the project directory supplied by the user. <br>
Mitigation: Run it only against project directories that the user is comfortable allowing the skill to inspect. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON with operational procedures and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project paths, service names, ports, environment variable names, and generated commands that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
