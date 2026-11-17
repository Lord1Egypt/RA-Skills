## Description:

Generate branded CompleteTech LLC printable #10 addressed envelope PDFs and delivery packages with sender, recipient, optional attention line, postage box text, return-address toggle, logo, brand palette, attachment manifests, filenames, recipient metadata, and delivery-readiness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[completetech](https://clawhub.ai/user/completetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to prepare CompleteTech-branded envelope PDFs, attachment manifests, package filenames, and delivery-readiness notes for physical mail, digital handoff, or internal archive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local generator reads user-provided INI files and logo paths.

Mitigation: Review config and override files before running the generator, and use only trusted local logo paths.

Risk: An envelope or delivery package could be prepared with an incorrect recipient, address, attachment list, or approval state.

Mitigation: Verify recipient details, delivery mode, attachments, and approval status before external mailing or handoff.

## Reference(s):

- [Agentic Envelope Skill ClawHub Page](https://clawhub.ai/completetech/skills/agentic-envelope-skill)
- [Agentic Envelope Skill Homepage](https://github.com/CompleteTech-LLC/agentic-envelope-skill)
- [OpenClaw Skill Metadata](artifact/SKILL.md)
- [References](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and delivery package metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to generate a local PDF at the selected output path and report missing recipient, attachment, or approval facts.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
