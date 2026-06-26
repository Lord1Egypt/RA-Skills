## Description: <br>
Identifies insufficiently evidenced conclusions in reports, proposals, or presentations and prioritizes follow-up evidence collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, reviewers, researchers, and decision-support teams use this skill to turn drafts, claims, and existing evidence into a structured evidence-gap review with priorities, weaker fallback wording, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can read local input files or directories and write an intended output file. <br>
Mitigation: Run it in a normal project sandbox, review the input and output paths before execution, and avoid sensitive directories unless they are explicitly in scope. <br>
Risk: Evidence-gap results may be incomplete or misleading when the supplied draft, claims, or evidence are incomplete. <br>
Mitigation: Treat the output as a review draft, keep the listed pending confirmations visible, and require human review before using findings in decisions. <br>
Risk: The skill does not fetch external facts or independently validate claims. <br>
Mitigation: Use it to identify evidence needs, then collect and cite external evidence through an approved research workflow when validation is required. <br>
Risk: Inputs may contain personal, confidential, or regulated information. <br>
Mitigation: De-identify sensitive material where possible and keep generated Markdown or JSON outputs within the same access-controlled workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/evidence-gap-mapper) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Output specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Structured Markdown report, with optional JSON wrapper from the local helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can write an intended output file when invoked with --output and otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
