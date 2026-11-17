## Description:

Docker image build, test, security scan, and GitHub Actions release pipeline support for containerized application delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to generate Dockerfiles, docker-compose configuration, GitHub Actions CI workflows, container integration tests, and related release guidance for containerized applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI workflows can publish container images to a registry.

Mitigation: Review workflows before committing them, confirm target registries and tags, and restrict publishing to intended branches or protected releases.

Risk: The bundled example uses an unpinned third-party GitHub Action.

Mitigation: Pin third-party GitHub Actions to reviewed versions or commit SHAs before use.

Risk: Overbroad workflow permissions can expose release credentials or allow unintended publishing.

Mitigation: Set least-privilege GitHub Actions permissions and review required secrets before enabling release workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/docker-ci-release-pipeline)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Dockerfile, YAML, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Dockerfile, docker-compose.yml, .dockerignore, GitHub Actions workflow files, tests, CI status summaries, and failure log summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
