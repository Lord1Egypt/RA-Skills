## Description: <br>
Review and optimize Dockerfiles to reduce layer count, minimize image size, and improve build times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to review Dockerfiles, produce optimized Dockerfile examples, and explain changes that reduce image size, improve build caching, and address container security best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Dockerfile rewrites can change application behavior when base images, Alpine/musl, non-root users, or multi-stage builds are introduced. <br>
Mitigation: Review and test generated Dockerfiles before use, and verify base image and user changes against application runtime requirements. <br>
Risk: Dockerfiles or related snippets may expose secrets or sensitive project files. <br>
Mitigation: Avoid pasting secrets into Dockerfiles or manifests, and use a .dockerignore file to keep credentials and unnecessary files out of images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunny0826/dockerfile-optimizer) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown report with Dockerfile code blocks and explanatory guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adapts the report language to Chinese or English based on the user's prompt.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
