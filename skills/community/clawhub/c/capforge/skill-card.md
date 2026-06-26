## Description: <br>
CapForge helps agents scan GitHub repositories, extract reusable capability documentation, classify capability domains, validate generated files, and sync repositories safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldx-person](https://clawhub.ai/user/ldx-person) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect open-source GitHub repositories, produce reusable capability summaries, compare capability domains across projects, and validate the resulting Markdown assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external capforge npm package and may execute repository import, scan, describe, transform, classify, validate, or update commands. <br>
Mitigation: Use the installed capforge binary or a pinned reviewed package version, and review each proposed command and repository URL before approval. <br>
Risk: CapForge writes cloned repositories and generated summaries to a local workspace such as ~/.capforge. <br>
Mitigation: Keep the workspace limited to repositories and generated summaries that are acceptable to store locally. <br>
Risk: Repository synchronization can write to disk when importing, pulling, or updating repositories. <br>
Mitigation: Require explicit user confirmation before running commands, especially git clone, git pull, capforge import, and capforge update. <br>


## Reference(s): <br>
- [CapForge ClawHub release](https://clawhub.ai/ldx-person/capforge) <br>
- [CapForge project homepage](https://github.com/ldx-person/capforge) <br>
- [Publisher profile](https://clawhub.ai/user/ldx-person) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or guides creation of capability.md, domains.md, validation-report.md, and optional transform-plan.md files in the configured CapForge workspace.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
