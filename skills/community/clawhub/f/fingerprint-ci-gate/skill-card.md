## Description:

Gate a build on browser fingerprint regressions with liarjs by saving a baseline scan as JSON, diffing later runs against it, and failing the job when the consistency score falls below a configured floor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liarjsdev](https://clawhub.ai/user/liarjsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add browser fingerprint regression checks to GitHub Actions, GitLab CI, Docker, or Playwright/Puppeteer pipelines. It helps catch changes in Chromium builds or scraping harnesses before they ship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CI examples that install packages dynamically can introduce normal supply-chain exposure in sensitive pipelines.

Mitigation: Pin npm dependencies exactly, commit a lockfile, and pin CI actions and container images where practical.

Risk: Default network checks may expose outbound request metadata from the runner environment.

Mitigation: Use --offline or a self-hosted endpoint when outbound request metadata is sensitive.

## Reference(s):

- [CI recipes](references/ci-recipes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, Dockerfile, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CI gate recommendations, pinned liarjs command examples, baseline refresh guidance, and notes about offline or self-hosted endpoint use.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
