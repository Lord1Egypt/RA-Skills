## Description: <br>
Evaluates user-provided brand, product, article, FAQ, or sales copy for how easily Doubao can understand, summarize, quote, and recommend it, then returns a concise Chinese GEO audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, brand owners, content creators, and agent developers use this skill to audit supplied Chinese-language content for Doubao-oriented generative engine optimization. It scores clarity, target audience, scenario fit, structure, quotability, and recommendation triggers, then suggests practical content improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill does not measure live Doubao rankings, crawl websites, store monitoring history, or support account-based workflows. <br>
Mitigation: Use it as a lightweight audit of content supplied by the user, and use separate measurement or monitoring tools when live ranking or longitudinal tracking is required. <br>
Risk: Sparse or vague source content can lead to low-confidence brand interpretation or incomplete recommendations. <br>
Mitigation: Provide complete brand, audience, scenario, product, and FAQ material, and review the generated report before using it for customer-facing or strategic decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljseeking/geo-analysis-doubao) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [doubao_geo_audit_report.md](artifact/templates/doubao_geo_audit_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Chinese Markdown audit report with scored sections, tables, recommendations, and FAQ suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default compact mode limits repeated explanation, keeps major problems to three items, optimization suggestions to five items, and FAQ suggestions to five items.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
