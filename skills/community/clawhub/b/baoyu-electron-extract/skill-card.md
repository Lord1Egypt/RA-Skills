## Description:

Baoyu Electron Extract helps agents extract resources and JavaScript from installed Electron app .asar bundles, restoring original sources from embedded source maps when available or formatting bundled JS/CSS otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect installed Electron desktop apps by unpacking app.asar, restoring readable source trees from source maps when possible, and producing formatted extracted code for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs downloaded npm packages during use.

Mitigation: Prefer a locally reviewed, pinned dependency setup before running extraction.

Risk: Formatting untrusted extracted app code can create local code-execution exposure.

Mitigation: Use --skip-format for untrusted apps and review extracted files before opening or executing them.

Risk: Using --force on an important non-empty output path can overwrite existing files.

Mitigation: Write outputs to a dedicated directory and avoid --force unless the target directory is disposable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-electron-extract)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-electron-extract)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files, JSON]

**Output Format:** [Markdown guidance with bash commands and generated filesystem outputs, including extracted/restored code files and extract-report.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for an app name, path, output directory, or overwrite decision; supports dry-run and JSON summary modes.]

## Skill Version(s):

1.119.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
