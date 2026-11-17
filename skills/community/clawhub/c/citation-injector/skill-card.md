## Description:

Applies a citation-diversifier budget report by injecting in-scope citations into an existing draft without adding new facts, so the draft can meet a global unique-citation target without citation dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, writers, and agent pipeline operators use this skill to update a Markdown draft when a citation budget report shows too few globally unique citations or excessive citation reuse. The skill is intended to add only citation keys already allowed for each subsection and already present in the bibliography.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package contains broader research-pipeline tooling beyond the narrow citation-injection behavior described by the release.

Mitigation: Review the bundled files before use and install or run the skill only in a sandboxed workspace.

Risk: The citation script can modify draft files and accepts custom input and output paths.

Mitigation: Prefer the documented default paths, avoid path overrides from untrusted sources, and keep workspace backups or version control before execution.

Risk: Injected citations may still be inappropriate for the surrounding claim even when the citation key is in scope.

Mitigation: Verify the resulting draft against citations/ref.bib and output/CITATION_BUDGET_REPORT.md before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/citation-injector)
- [ClawHub publisher profile](https://clawhub.ai/user/willoscar)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/scripts/run.py](artifact/scripts/run.py)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, guidance]

**Output Format:** [Markdown draft updates, Markdown report, and optional Python command invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates output/DRAFT.md in place and writes output/CITATION_INJECTION_REPORT.md with pass/fail status and citation counts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
