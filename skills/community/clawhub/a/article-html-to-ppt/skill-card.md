## Description:

Create PPTX, reconstruct slides, or reuse PPTX templates; produce editable native objects, real previews and hash-bound review. Use for revisions too.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillmelody](https://clawhub.ai/user/skillmelody)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and other knowledge workers use PPT Smith to create presentations from source material, reconstruct supplied slide designs, or adapt existing PowerPoint templates. They can also revise decks and review editable output, previews, and supporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some compatibility build or rendering tools may remove previous presentation output before a replacement succeeds.

Mitigation: Use fresh, dedicated work and output directories, and keep backups before running compatibility builders or renderers.

Risk: Advanced author-provided Python can run with the operator's permissions after it is explicitly enabled; this is not a sandbox.

Mitigation: Prefer fixed declarative workflows. Review the script and its imports before authorizing it, and use an external isolation environment for untrusted code.

Risk: Optional external image tools may receive selected presentation content.

Mitigation: Send only content authorized for the selected service, and omit sensitive material when it is not needed.

## Reference(s):

- [PPT Smith on ClawHub](https://clawhub.ai/skillmelody/skills/article-html-to-ppt)
- [Declarative design workflow](references/declarative-design.md)
- [Native template workflow](references/native-template-workflow.md)
- [Security and compatibility boundaries](references/security-boundaries.md)

## Skill Output:

**Output Type(s):** [Files, PPTX presentations, Preview images, JSON review records, Guidance]

**Output Format:** [Editable PPTX presentations with rendered previews and structured review records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Native editable objects; slide count, supported edits, and review evidence depend on the selected workflow and available tools.]

## Skill Version(s):

5.3.1 (source: SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
