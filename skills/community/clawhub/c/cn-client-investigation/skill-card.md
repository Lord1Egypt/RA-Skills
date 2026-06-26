## Description: <br>
Provides a China mainland company investigation workflow with controls for Chinese text accuracy, data provenance, and banker-style memo and deck delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and financial services teams use this skill to research China-market entities and produce analyst memo or deck deliverables with source tracking and QA gates for numbers and Chinese text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged the release as suspicious because it contacts external financial and business-data services and handles credentials. <br>
Mitigation: Install and run it only in a sandboxed environment with no unrelated secrets, and review credential configuration before use. <br>
Risk: Credential exposure or insecure credential transmission could occur if embedded or local API tokens are reused carelessly. <br>
Mitigation: Remove or rotate embedded Tushare credentials, prefer HTTPS for credentialed API calls, and use least-privilege credentials. <br>
Risk: External build or helper code can run during deliverable generation. <br>
Mitigation: Review generated scripts and helper files before execution, and avoid the /tmp DOCX helper override unless that file is fully controlled. <br>
Risk: Financial figures or Chinese text in client deliverables may be wrong if provenance and typo checks are skipped. <br>
Mitigation: Run the skill's strict provenance, raw-data, source-authenticity, and Chinese typo validation gates before relying on generated deliverables. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackdark425/cn-client-investigation) <br>
- [CN lexicon reference](references/cn-lexicon.js) <br>
- [CN data sources guide](references/data-sources.md) <br>
- [Compile with typo gate template](references/compile_with_typo_gate.template.js.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated deliverable files such as analysis notes, provenance tables, slide code, PPTX decks, and QA reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source provenance records and validation gates for hard numbers, raw data snapshots, and Chinese text typo scans.] <br>

## Skill Version(s): <br>
0.9.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
