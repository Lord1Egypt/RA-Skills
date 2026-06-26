## Description: <br>
Generates an end-to-end Docker CI release pipeline that builds, tests, scans, and publishes container images with GitHub Actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to containerize applications and generate Docker, test, security scanning, and GitHub Actions release artifacts for image publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated release workflows can publish images to the wrong registry, visibility scope, branch, or tag if enabled without review. <br>
Mitigation: Verify publish branches and tags, registry destination, image visibility, workflow permissions, and secret usage before merging or running generated workflows; require explicit confirmation before enabling push-to-registry steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/docker-ci-release-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Docker, YAML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed Dockerfiles, docker-compose files, GitHub Actions workflows, integration tests, dockerignore files, and CI status guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
