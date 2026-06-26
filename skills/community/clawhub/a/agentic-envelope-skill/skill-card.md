## Description: <br>
Generates branded CompleteTech LLC printable #10 addressed envelope PDFs and delivery-package metadata from verified recipient, attachment, branding, and delivery facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[completetech](https://clawhub.ai/user/completetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to package CompleteTech delivery workflows with printable envelopes, attachment manifests, recipient metadata, filenames, and delivery-readiness notes. It is intended for mailing or external handoff of contracts, certificates, invoices, proposals, notices, and related artifacts after recipient and approval facts are verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or external delivery material could be packaged before recipient details, addresses, attachments, or approval status are verified. <br>
Mitigation: Confirm recipient and approval facts before packaging; return missing facts or a blocked delivery-readiness note instead of guessing. <br>
Risk: The generator writes a local PDF to the configured output path, which could place delivery material in an unintended location. <br>
Mitigation: Choose the --out path deliberately and review the generated path before sharing, printing, or archiving the envelope. <br>
Risk: Demo configuration values or default branding could be mistaken for final delivery data. <br>
Mitigation: Use per-recipient override INI files for real deliveries and verify live sender, recipient, and brand details before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/completetech/agentic-envelope-skill) <br>
- [Homepage](https://github.com/CompleteTech-LLC/agentic-envelope-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration references, generated file paths, manifests, and delivery-readiness notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local envelope PDF at the selected output path when the generator is run.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
