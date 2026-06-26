## Description: <br>
Generates weekly Markdown research reports on LLM and VLM applications in search, advertising, and recommendation systems, then syncs them to Tencent IMA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fandywang87](https://clawhub.ai/user/fandywang87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical operators use this skill to collect recent AI recommendation-system material, produce a structured weekly report, and publish it to an IMA knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires IMA Client ID and API key credentials to sync reports. <br>
Mitigation: Store credentials with restrictive file permissions, avoid committing or backing them up, and install only when IMA syncing is intended. <br>
Risk: Generated reports may be uploaded to the wrong IMA knowledge base if the target ID is incorrect. <br>
Mitigation: Verify the knowledge-base ID and test manually before enabling weekly automation. <br>
Risk: The generated technical report may include stale, incomplete, or misleading research interpretation. <br>
Mitigation: Review cited papers and source links before distributing or relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fandywang87/ai-recsys-weekly-report) <br>
- [Research scope](references/research-scope.md) <br>
- [Tencent IMA agent interface](https://ima.qq.com/agent-interface) <br>
- [OneTrans paper](https://arxiv.org/abs/2510.26104) <br>
- [MixFormer paper](https://arxiv.org/abs/2602.14110) <br>
- [STRec paper](https://dl.acm.org/doi/10.1145/3604915.3608779) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline commands and upload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 2000-4000 word report file named AI搜广推技术周报_YYYY-MM-DD.md and can upload it to a user-specified IMA knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
