## Description: <br>
Gaokao Volunteer Research helps agents turn Chinese Gaokao application questions into official-source research packages with candidate matrices, data checks, family briefs, and explicit limits against admission promises or form submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hacksing](https://clawhub.ai/user/hacksing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, families, counselors, and agents use this skill to research Chinese Gaokao application options from official current-year sources, verify score/rank and batch-line data, and prepare auditable decision-support files. It is for research support only and does not submit applications, promise admission outcomes, or replace final checks in official systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Gaokao research can be mistaken for guaranteed admissions advice or final application instructions. <br>
Mitigation: Review outputs before relying on them, keep admission outcomes framed as research support, and complete final decisions in the official provincial or school systems. <br>
Risk: Missing or stale province, year, rank, batch, or subject-group data can lead to misleading candidate matrices. <br>
Mitigation: Require current official sources and key inputs before producing concrete candidates; otherwise produce only a research checklist or data-check package. <br>
Risk: Non-official rankings, screenshots, social posts, or commercial tables may conflict with authoritative admissions sources. <br>
Mitigation: Use those materials only as leads and verify material facts against provincial exam authorities, Ministry of Education platforms, university admissions sites, and original policy documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hacksing/gaokao-volunteer-research) <br>
- [Source policy](references/source-policy.md) <br>
- [Tooling guide](references/tooling.md) <br>
- [Test scenarios](references/test-scenarios.md) <br>
- [Official source index](data/official-source-index.json) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown research package files with source tables, candidate matrices, risk notes, family briefs, and optional JSON outputs from helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated research packages should preserve province, year, subject group, score/rank, batch, source URL, publication or applicable year, and unresolved verification items.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter/changelog report 0.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
