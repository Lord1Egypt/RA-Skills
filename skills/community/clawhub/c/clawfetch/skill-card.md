## Description:

Thin OpenClaw and ClawHub wrapper for the published clawfetch npm CLI, used to fetch web pages, GitHub READMEs, and Reddit threads as markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ernestyu](https://clawhub.ai/user/ernestyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web content, GitHub README pages, and Reddit threads as markdown for knowledge-base ingestion, source review, and compact reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads and runs npm code that is not fully pinned or reviewed with the skill.

Mitigation: Install only when the published clawfetch npm package and its dependencies are trusted; prefer a pinned, lockfile-backed, integrity-verified install path for sensitive environments.

Risk: Bootstrap and runtime setup require executing dependency installation steps.

Mitigation: Run bootstrap and runtime installation in a low-privilege environment without sensitive credentials, then verify readiness with the CLI runtime check before fetching pages.

Risk: Fetched web content can be untrusted, misleading, or unsuitable for direct knowledge-base ingestion.

Mitigation: Review fetched markdown and source metadata before using it as evidence, training material, or operational guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ernestyu/skills/clawfetch)
- [clawfetch homepage](https://github.com/ernestyu/clawfetch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown output and setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch behavior depends on the installed clawfetch npm CLI, browser runtime readiness, network access, and optional FlareSolverr configuration.]

## Skill Version(s):

1.0.12 (source: server release metadata, SKILL.md frontmatter, manifest.yaml, bootstrap fallback)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
