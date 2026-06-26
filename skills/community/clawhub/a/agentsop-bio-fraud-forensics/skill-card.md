## Description: <br>
Screens biomedical and life-science papers for observable research-integrity anomalies in images, statistics, paper-mill signals, and prior-publication status while framing outputs as reproducible questions rather than accusations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, editors, reviewers, and integrity-screening users can use this skill to triage biomedical papers, figures, DOIs, and supplementary data for reproducible anomalies. It helps produce neutral observations, verification routing, statistical checks, and PubPeer-style notes without making misconduct determinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research-integrity screening output could be mistaken for a misconduct finding or used as an accusation. <br>
Mitigation: Treat results as preliminary observations, keep language neutral and reproducible, and reserve misconduct determinations for authorized journals, institutions, or official bodies. <br>
Risk: Automated or visual anomaly checks can produce false positives or miss benign explanations. <br>
Mitigation: Verify every cited anomaly against the source artifact, record the exact test and location, and evaluate innocent alternatives before escalating a concern. <br>


## Reference(s): <br>
- [Operation Models](references/sop_models.md) <br>
- [Research Notes](references/research_notes.md) <br>
- [Misconduct Taxonomy and Honest-Error Discriminators](references/R01-misconduct-taxonomy.md) <br>
- [Image Forensics](references/R02-image-forensics.md) <br>
- [Statistical Forensics](references/R03-statistical-forensics.md) <br>
- [Exposure Sites as Method Source](references/R04-exposure-sites-method.md) <br>
- [Evidence Strength and Red Lines](references/R05-evidence-red-lines.md) <br>
- [Screening Workflow and Forensic Record](references/R06-screening-workflow.md) <br>
- [Paper Mill and Systemic Signals](references/R07-paper-mill-signals.md) <br>
- [Worked Screening Examples](examples/demo_screening.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentsope/agentsop-bio-fraud-forensics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, code] <br>
**Output Format:** [Markdown screening notes with neutral findings, reproducible annotations, optional statistical recomputation steps, and verification routing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state what each observation can and cannot prove, avoid accusatory wording, and remain grounded in visible evidence or cited status checks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and target metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
