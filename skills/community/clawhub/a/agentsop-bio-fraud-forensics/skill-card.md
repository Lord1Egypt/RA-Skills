## Description:

Screens biomedical and life-science papers for observable signs of image manipulation, statistical anomalies, paper-mill patterns, and prior integrity flags while framing outputs as questions for clarification rather than accusations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, reviewers, editors, and research-integrity analysts use this skill to triage biomedical papers, figures, supplementary data, and DOIs for reproducible anomalies, verification routes, and neutral PubPeer-style clarification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may expose API-key values if an agent follows troubleshooting steps too literally.

Mitigation: Do not read, print, paste, or transmit API-key contents; only confirm that expected configuration files or environment variables exist.

Risk: Biomedical papers, peer-review files, embargoed manuscripts, proprietary data, or personal data may be disclosed to third-party services during status checks or forensic review.

Mitigation: Prefer DOI lookups and local analysis; upload sensitive files only after explicit authorization and review of the destination service terms.

Risk: Integrity-screening outputs can be misread as accusations or adjudicated findings.

Mitigation: Keep conclusions neutral and evidence-bound, state what each observation cannot prove, and route unresolved concerns to authors, editors, institutions, or official records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsope/skills/agentsop-bio-fraud-forensics)
- [Bio-Fraud Forensics README](artifact/README.md)
- [Bio-Fraud Forensics Usage Guide](artifact/USAGE.md)
- [Operation Models - Full Cards (M1-M7)](artifact/references/sop_models.md)
- [Research Notes - Evidence Summary, Routing Table, Seed Lists](artifact/references/research_notes.md)
- [R01 - Misconduct Taxonomy and Honest-Error Discriminators](artifact/references/R01-misconduct-taxonomy.md)
- [R02 - Image Forensics](artifact/references/R02-image-forensics.md)
- [R03 - Statistical Forensics](artifact/references/R03-statistical-forensics.md)
- [R04 - Exposure Sites as Method Source](artifact/references/R04-exposure-sites-method.md)
- [R05 - Evidence Strength and Red Lines](artifact/references/R05-evidence-red-lines.md)
- [R06 - Screening Workflow and Forensic Record](artifact/references/R06-screening-workflow.md)
- [R07 - Paper Mill and Systemic Signals](artifact/references/R07-paper-mill-signals.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown screening notes with reproducible checks, neutral findings, verification routing, and occasional inline shell or Python commands for local analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify the test used, the input checked, what was observed, what the observation cannot prove, and any benign explanations considered.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
