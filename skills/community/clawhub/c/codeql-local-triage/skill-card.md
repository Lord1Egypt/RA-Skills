## Description:

Helps developers investigate one Python CodeQL alert by inspecting local source and SARIF, testing candidate taint sources, and checking whether a fix removes the finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to trace and verify a single Python CodeQL sensitive-data alert using local source and SARIF. It is not a whole-repository audit or an alert-dismissal tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Specified source and SARIF files may contain sensitive information.

Mitigation: Provide only the files needed for the alert and review outputs before sharing them.

Risk: Variant experiments create full temporary copies under _bisect or a chosen work directory.

Mitigation: Use an appropriate work directory and exclude _bisect from version control when it is inside a repository.

Risk: Optional local CodeQL execution or an unverified mirror download can introduce tool or supply-chain risk.

Mitigation: Use an approved local CodeQL binary; prefer official downloads and independently verify the official SHA-256 before using a mirror.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/elisabeth15501/skills/codeql-local-triage)
- [CodeQL CLI setup and local analysis](artifact/references/running-codeql-cli.md)
- [Sensitive-data heuristics](artifact/references/sensitive-data-heuristics.md)
- [Triage FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with source locations, result tables, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes measured results from unverified hypotheses; does not dismiss alerts.]

## Skill Version(s):

1.0.8 (source: server-resolved release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
