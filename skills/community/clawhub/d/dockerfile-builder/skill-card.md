## Description: <br>
Generate and lint Dockerfiles for common languages and frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create starter Dockerfiles, lint existing Dockerfiles, receive optimization suggestions, generate common templates, and scan Dockerfiles for likely secret-related strings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Dockerfiles or optimization suggestions may be incomplete or unsuitable for a production image. <br>
Mitigation: Review generated Dockerfiles before building or deploying containers. <br>
Risk: The scan command may display matching lines from files that contain sensitive strings. <br>
Mitigation: Run scans only on intended Dockerfiles or non-sensitive files. <br>


## Reference(s): <br>
- [Dockerfile Builder on ClawHub](https://clawhub.ai/ckchzh/dockerfile-builder) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Dockerfile snippets emitted by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local data storage at ~/.local/share/dockerfile-builder when the helper runs.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
