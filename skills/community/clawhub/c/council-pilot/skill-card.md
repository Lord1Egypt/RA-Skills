## Description:

Council Pilot is an autonomous expert-forum and project-maturity engine that distills public expert sources, builds project code, scores maturity, debugs, and iterates toward a GitHub-ready result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn an idea or domain brief into an expert-guided project build loop with research, scoring, debugging, maturity reporting, and optional GitHub PR submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously change repository files and generate project code.

Mitigation: Use it only in repositories where autonomous edits are acceptable, review diffs before accepting changes, and require approval before file writes in sensitive workspaces.

Risk: The workflow can create commits, push branches, and open GitHub PRs.

Mitigation: Require manual approval before git commits, pushes, or PR creation, and review the generated maturity report before submission.

Risk: Forum state, build logs, and generated reports may persist private paths, secrets, or unwanted source-derived content.

Mitigation: Inspect generated data and logs before committing or sharing them, and scan for secrets, private code, internal paths, and inappropriate source-derived content.

Risk: Expert profiles are distilled from public sources and may overstate, misattribute, or stale-date an expert's views.

Mitigation: Treat expert profiles as analysis lenses, preserve source links and freshness metadata, avoid fabricated quotes, and prefer current project evidence over distilled expert memory.

## Reference(s):

- [Council Pilot ClawHub page](https://clawhub.ai/wd041216-bit/skills/council-pilot)
- [Council Pilot repository](https://github.com/wd041216-bit/council-pilot)
- [README](artifact/README.md)
- [Build Integration](artifact/references/build-integration.md)
- [Council Protocol](artifact/references/council-protocol.md)
- [GitHub Submission](artifact/references/github-submission.md)
- [Loop State Machine](artifact/references/loop-state-machine.md)
- [Expert Profile Contract](artifact/references/profile-contract.md)
- [Maturity Scoring Rubric](artifact/references/scoring-rubric.md)
- [Source Gates](artifact/references/source-gates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands, generated code, JSON state files, Markdown reports, and GitHub PR metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates repository files, forum state, expert profiles, scoring reports, gap analyses, build logs, maturity reports, and optional GitHub branch/PR records.]

## Skill Version(s):

1.0.0 (source: evidence release, target metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
