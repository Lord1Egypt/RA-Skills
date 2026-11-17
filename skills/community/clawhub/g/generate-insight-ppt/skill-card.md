## Description:

Automates technical report generation by collecting research material, extracting insights, drafting slide content, optimizing it, and producing a PowerPoint deck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieyuantao7](https://clawhub.ai/user/xieyuantao7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and technical teams use this skill to turn a research topic into a structured technical insight presentation with collected sources, extracted insights, generated slide content, and a final PPTX file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL fetching during collection can reach untrusted or internal network resources.

Mitigation: Run the skill with limited network access, allowlist trusted sources, and avoid allowing untrusted URLs to drive downloads.

Risk: Session-file handling may write outside the intended report folder.

Mitigation: Use simple alphanumeric session IDs and inspect configured output paths before execution.

Risk: Runtime dependencies may vary if installed without version pinning.

Mitigation: Pin and review presentation-generation dependencies in an isolated environment before use.

## Reference(s):

- [Tech Report PPT Generator on ClawHub](https://clawhub.ai/xieyuantao7/skills/generate-insight-ppt)
- [User README](artifact/README.md)
- [Scripts README](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [PowerPoint files with Markdown and JSON intermediate artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces collected web-page Markdown, insight and outline JSON, slide content files, logs, and PPTX output under a session directory.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
