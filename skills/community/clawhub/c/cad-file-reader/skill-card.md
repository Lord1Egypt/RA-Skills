## Description:

Reads DWG and DXF drawings to produce traceable annotation, geometry, layer and block semantics, MEP topology, drawing comparison, and standards lookup candidates; it does not calculate final quantities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Architects, engineers, and drawing reviewers use the skill to extract traceable evidence and reviewable interpretation candidates from CAD drawings and related PDFs. It supports drawing review and downstream workflows without producing final quantities or cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks the release suspicious because reported capabilities and setup actions may exceed its stated drawing-reading scope, and it notes data handling, persistence, and dependency concerns. The scan was incomplete.

Mitigation: Review the installer, capabilities, persistence, and dependencies before use; run in an environment appropriate to the project’s access controls.

Risk: CAD drawings may contain sensitive project information.

Mitigation: Keep processing local by default and share drawing data only within an explicitly approved scope and with user consent.

## Reference(s):

- [CAD 图纸识图与证据提取 on ClawHub](https://clawhub.ai/lisong2003-lgtm/skills/cad-file-reader)
- [Base contract and evidence format](docs/base-contract.md)
- [PDF drawing pipeline](docs/pdf-pipeline.md)
- [lis-skill-bus integration](https://github.com/lisong2003-lgtm/lis-skill-bus)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, CSV, Excel workbooks, Word reports]

**Output Format:** [Structured drawing evidence and review candidates in JSON or human-readable reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidates retain evidence locations and confidence or review status; final_quantity is always false.]

## Skill Version(s):

0.41.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
