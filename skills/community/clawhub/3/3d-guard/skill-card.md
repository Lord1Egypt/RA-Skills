## Description:

3D模型审计技能，用于检查STL、OBJ、3MF等3D模型文件的合规性，包括文件完整性、版权风险、敏感内容和打印尺寸检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuihuar](https://clawhub.ai/user/kuihuar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, makers, and reviewers use this skill to audit 3D model files before printing, sharing, or commercial use. It helps structure checks for file validity, required metadata, print dimensions, copyright risk, and sensitive content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate audit coverage for legal, content-safety, or printer-readiness decisions.

Mitigation: Treat outputs as an advisory checklist and manually review copyright, sensitive-content, and print-readiness conclusions before acting.

Risk: Fragile parsers may mislead or disrupt users handling untrusted 3D model files.

Mitigation: Run validation on untrusted files with resource limits and inspect script output before relying on it.

Risk: The included publishing script can publish the skill to ClawHub.

Mitigation: Do not run publish.sh unless publication is intended and release metadata has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuihuar/skills/3d-guard)
- [Copyright guidelines](artifact/references/copyright-guidelines.md)
- [Printer specifications](artifact/references/printer-specs.md)
- [Sensitive content reference](artifact/references/sensitive-content.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown audit guidance with JSON validation results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts emit JSON for model and metadata validation; final audit conclusions require user review.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
