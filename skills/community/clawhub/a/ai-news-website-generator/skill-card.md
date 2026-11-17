## Description:

AI资讯网站生成器 - 一键构建智能内容聚合平台

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to scaffold a full-stack AI or RSS news aggregation website with a Next.js frontend, FastAPI backend, Docker Compose deployment, configurable feeds, filtering, and scheduled refresh.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can delete a user-selected output directory when overwriting an existing project.

Mitigation: Run it only in a disposable or clearly chosen workspace, and do not target an existing project, repository root, home directory, or sensitive path.

Risk: The generated web service uses exposed unsafe defaults and dependencies that require review before deployment.

Mitigation: Before deploying, update dependencies, add lockfiles or hashes, restrict CORS, bind the backend appropriately, and protect or rate-limit the refresh endpoint.

Risk: The generated local and Docker startup flows can leave services running in the background.

Mitigation: Review the generated start and Docker commands, track background process IDs, and confirm how to stop containers or local services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninetyhe-90/skills/ai-news-website-generator)
- [Next.js documentation](https://nextjs.org/docs)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Docker documentation](https://docs.docker.com/)
- [Tailwind CSS](https://tailwindcss.com/)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated project files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated project includes frontend, backend, Docker Compose, README, and startup scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
