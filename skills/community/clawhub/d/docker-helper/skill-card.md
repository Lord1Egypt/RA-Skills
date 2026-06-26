## Description: <br>
Docker Helper provides Dockerfile templates, Docker Compose examples, command references, debugging guidance, image optimization tips, and registry configuration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create starter Dockerfiles and docker-compose configurations, consult Docker command references, debug containers, optimize images, and configure container registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Dockerfiles and compose files may include development defaults such as default passwords, exposed ports, or disabled service security. <br>
Mitigation: Replace default credentials, enable service security, restrict exposed ports, and review each generated configuration before running it. <br>
Risk: Cleanup and Docker management commands can remove local containers, images, volumes, or other development resources. <br>
Mitigation: Review cleanup commands in context and run them only against intended local resources. <br>
Risk: The generic helper script records command activity in a local history log, which may capture sensitive arguments. <br>
Mitigation: Avoid passing secrets or sensitive values as command arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/docker-helper) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Docker Helper tips](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with Dockerfile, docker-compose, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are development starting points and command references; generated container configurations require review before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
